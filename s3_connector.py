# --
# File: s3_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2018
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
from phantom.vault import Vault

# Usage of the consts file is recommended
from s3_consts import *
from boto3 import client
from datetime import datetime
from botocore.config import Config

import os
import json
import tempfile


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class AwsS3Connector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(AwsS3Connector, self).__init__()

        self._state = None
        self._region = None
        self._access_key = None
        self._secret_key = None
        self._proxy = None

    def initialize(self):

        self._state = self.load_state()

        config = self.get_config()

        self._region = S3_REGION_DICT.get(config['region'])
        if not self._region:
            return self.set_status(phantom.APP_ERROR, "Specified region is not valid")

        if S3_JSON_ACCESS_KEY in config:
            self._access_key = config.get(S3_JSON_ACCESS_KEY)
        if S3_JSON_SECRET_KEY in config:
            self._secret_key = config.get(S3_JSON_SECRET_KEY)

        self._proxy = {}
        env_vars = config.get('_reserved_environment_variables', {})
        if 'HTTP_PROXY' in env_vars:
            self._proxy['http'] = env_vars['HTTP_PROXY']['value']
        if 'HTTPS_PROXY' in env_vars:
            self._proxy['https'] = env_vars['HTTPS_PROXY']['value']

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved accross actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def _create_client(self, action_result):

        boto_config = None
        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        try:

            if self._access_key and self._secret_key:

                self.debug_print("Creating boto3 client with API keys")

                self._client = client(
                        's3',
                        region_name=self._region,
                        aws_access_key_id=self._access_key,
                        aws_secret_access_key=self._secret_key,
                        config=boto_config)

            else:

                self.debug_print("Creating boto3 client without API keys")

                self._client = client(
                        's3',
                        region_name=self._region,
                        config=boto_config)

        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 client: {0}".format(e))

        return phantom.APP_SUCCESS

    def _sanatize_dates(self, cur_obj):

        try:
            json.dumps(cur_obj)
            return cur_obj
        except:
            pass

        if isinstance(cur_obj, dict):
            new_dict = {}
            for k, v in cur_obj.iteritems():
                new_dict[k] = self._sanatize_dates(v)
            return new_dict

        if isinstance(cur_obj, list):
            new_list = []
            for v in cur_obj:
                new_list.append(self._sanatize_dates(v))
            return new_list

        if isinstance(cur_obj, datetime):
            return cur_obj.strftime("%Y-%m-%d %H:%M:%S")

        return cur_obj

    def _make_boto_call(self, action_result, method, **kwargs):

        try:
            boto_func = getattr(self._client, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), None)

        try:
            resp_json = boto_func(**kwargs)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, 'boto3 call to S3 failed', e), None)

        return phantom.APP_SUCCESS, self._sanatize_dates(resp_json)

    def _get_tag_dicts(self, action_result, tags):

        try:
            tag_dict = json.loads(tags)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Could not decode JSON object from given tag dictionary: {0}".format(e)))

        tag_dicts = []
        for k, v in tag_dict.iteritems():
            tag_dicts.append({'Key': k, 'Value': v})

        return RetVal(phantom.APP_SUCCESS, tag_dicts)

    def _get_grant_dict(self, action_result, grants, owner):

        try:
            grants = json.loads(grants)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Could not decode JSON object from given grant dictionary: {0}".format(e)))

        grants_list = []
        for k, v in grants.iteritems():
            if v not in S3_PERMISSIONS_LIST:
                return RetVal(action_result.set_status(phantom.APP_ERROR, "Given permission, {0}, is invalid".format(v)))
            grants_list.append({'Grantee': {'Type': 'CanonicalUser', 'ID': k}, 'Permission': v})

        grant_dict = {
                    'Grants': grants_list,
                    'Owner': {'ID': owner}
                }

        return RetVal(phantom.APP_SUCCESS, grant_dict)

    def _handle_test_connectivity(self, param):

        self.save_progress("Querying S3 to check credentials")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        ret_val, resp_json = self._make_boto_call(action_result, 'list_buckets')

        if (phantom.is_fail(ret_val)):
            self.save_progress("Test Connectivity Failed")
            return ret_val

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_buckets(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        ret_val, resp_json = self._make_boto_call(action_result, 'list_buckets')

        if (phantom.is_fail(ret_val)):
            return ret_val

        action_result.add_data(resp_json)
        action_result.set_summary({"num_buckets": len(resp_json.get('Buckets', []))})

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_bucket(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        result_json = {}
        summary = action_result.set_summary({})

        for endpoint in S3_BUCKET_INFO_LIST:

            found = True

            ret_val, resp_json = self._make_boto_call(action_result, 'get_bucket_{0}'.format(endpoint.lower()), Bucket=param['bucket'])

            if (phantom.is_fail(ret_val)):
                if S3_BAD_BUCKET_MESSAGE in action_result.get_message():
                    return ret_val
                else:
                    resp_json = {'Message': action_result.get_message()}
                    found = False

            if len(resp_json) == 1 and 'ResponseMetadata' in resp_json:
                resp_json = {'Message': '{0} does not appear to be configured for this bucket'.format(endpoint.replace('_', ' '))}
                found = False

            result_json[endpoint.replace('_', '')] = resp_json
            summary['{0}_found'.format(endpoint.lower())] = found

        action_result.add_data(result_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved bucket info")

    def _handle_create_bucket(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        location = {'LocationConstraint': S3_REGION_DICT[self.get_config()['region']]}

        ret_val, resp_json = self._make_boto_call(action_result, 'create_bucket', Bucket=param['bucket'], CreateBucketConfiguration=location)

        if (phantom.is_fail(ret_val)):
            return ret_val

        action_result.add_data(resp_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved bucket info")

    def _handle_update_bucket(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        if 'tags' in param:

            ret_val, tag_dicts = self._get_tag_dicts(action_result, param['tags'])

            if (phantom.is_fail(ret_val)):
                return ret_val

            ret_val, resp_json = self._make_boto_call(action_result, 'put_bucket_tagging', Bucket=param['bucket'], Tagging={'TagSet': tag_dicts})

            if (phantom.is_fail(ret_val)):
                return ret_val

            action_result.add_data(resp_json)

        if 'grants' in param:

            if 'owner' not in param:
                return action_result.set_status(phantom.APP_ERROR, "No owner provided with grants parameter")

            ret_val, grant_dict = self._get_grant_dict(action_result, param['grants'], param['owner'])

            if (phantom.is_fail(ret_val)):
                return ret_val

            ret_val, resp_json = self._make_boto_call(action_result, 'put_bucket_acl', Bucket=param['bucket'], AccessControlPolicy=grant_dict)

            if (phantom.is_fail(ret_val)):
                return ret_val

            action_result.add_data(resp_json)

        if 'encryption' in param:

            if param['encryption'] == 'AES256':
                encrypt_config = {"SSEAlgorithm": "AES256"}

            elif param['encryption'] == 'AWS:KMS':

                if 'kms_key' not in param:
                    return action_result.set_status(phantom.APP_ERROR, "Encryption set to AWS:KMS, but no KMS Key provided.")

                encrypt_config = {"SSEAlgorithm": "aws:kms", "KMSMasterKeyID": param["kms_key"]}

            ret_val, resp_json = self._make_boto_call(action_result, 'put_bucket_encryption',
                    Bucket=param['bucket'], ServerSideEncryptionConfiguration={"Rules": [{"ApplyServerSideEncryptionByDefault": encrypt_config}]})

            if (phantom.is_fail(ret_val)):
                return ret_val

            action_result.add_data(resp_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully updated bucket")

    def _handle_list_objects(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        if 'continuation_token' in param:
            ret_val, resp_json = self._make_boto_call(
                    action_result,
                    'list_objects_v2',
                    Bucket=param['bucket'],
                    StartAfter=param.get('key', ''),
                    ContinuationToken=param['continuation_token'],
                    MaxKeys=int(param.get('limit', 1000)),
                    FetchOwner=True)

        else:
            ret_val, resp_json = self._make_boto_call(
                    action_result,
                    'list_objects_v2',
                    Bucket=param['bucket'],
                    StartAfter=param.get('key', ''),
                    MaxKeys=int(param.get('limit', 1000)),
                    FetchOwner=True)

        if (phantom.is_fail(ret_val)):
            return ret_val

        action_result.add_data(resp_json)
        action_result.set_summary({"num_objects": resp_json.get('KeyCount', 0)})

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_object(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        ret_val, resp_json = self._make_boto_call(action_result, 'get_object_tagging', Bucket=param['bucket'], Key=param['key'])

        if (phantom.is_fail(ret_val)):
            return ret_val

        result_json = {"Tagging": resp_json}

        ret_val, resp_json = self._make_boto_call(action_result, 'get_object_acl', Bucket=param['bucket'], Key=param['key'])

        if (phantom.is_fail(ret_val)):
            return ret_val

        result_json["ACL"] = resp_json

        if param['download_file']:

            ret_val, resp_json = self._make_boto_call(action_result, 'get_object', Bucket=param['bucket'], Key=param['key'])

            if (phantom.is_fail(ret_val)):
                return ret_val

            try:
                file_data = resp_json.pop('Body').read()
            except:
                return action_result.set_status(phantom.APP_ERROR, "Could not retrieve object body from boto response")

            file_desc, file_path = tempfile.mkstemp(dir='/vault/tmp/')
            outfile = open(file_path, 'w')
            outfile.write(file_data)
            outfile.close()
            os.close(file_desc)

            try:
                vault_ret = Vault.add_attachment(file_path, self.get_container_id(), os.path.basename(param['key']))
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Could not file to vault: {0}".format(e))

            if not vault_ret.get('succeeded'):
                return action_result.set_status(phantom.APP_ERROR, "Could not save file to vault: {0}".format(vault_ret.get('message', "Unknown Error")))

            vault_id = vault_ret[phantom.APP_JSON_HASH]
            resp_json['vault_id'] = vault_id
            resp_json['filename'] = os.path.basename(param['key'])
            result_json["File"] = resp_json
            action_result.set_summary({"created_vault_id": vault_id})

        action_result.add_data(result_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved object info")

    def _handle_update_object(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        if 'tags' in param:

            ret_val, tag_dicts = self._get_tag_dicts(action_result, param['tags'])

            if (phantom.is_fail(ret_val)):
                return ret_val

            ret_val, resp_json = self._make_boto_call(action_result, 'put_object_tagging', Bucket=param['bucket'], Key=param['key'], Tagging={'TagSet': tag_dicts})

            if (phantom.is_fail(ret_val)):
                return ret_val

            action_result.add_data(resp_json)

        if 'grants' in param:

            if 'owner' not in param:
                return action_result.set_status(phantom.APP_ERROR, "No owner provided with grants parameter")

            ret_val, grant_dict = self._get_grant_dict(action_result, param['grants'], param['owner'])

            if (phantom.is_fail(ret_val)):
                return ret_val

            ret_val, resp_json = self._make_boto_call(action_result, 'put_object_acl', Bucket=param['bucket'], Key=param['key'], AccessControlPolicy=grant_dict)

            if (phantom.is_fail(ret_val)):
                return ret_val

            action_result.add_data(resp_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Object successfully updated")

    def _handle_post_data(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        vault_id = param['vault_id']
        file_path = Vault.get_file_path(vault_id)
        if not file_path:
            return action_result.set_status(phantom.APP_ERROR, "Could not find given vault ID in vault")
        upfile = open(file_path, 'rb')

        kwargs = {
                    'Body': upfile,
                    'Bucket': param['bucket'],
                    'Key': param['key'],
                    'StorageClass': param['storage_class']
                 }

        if 'metadata' in param:

            try:
                meta_dict = json.loads(param['metadata'])
            except Exception as e:
                return RetVal(action_result.set_status(phantom.APP_ERROR, "Could not decode JSON object from given metadata: {0}".format(e)))

            kwargs['Metadata'] = meta_dict

        encryption = param['encryption']

        if encryption == 'AES256':
            kwargs['ServerSideEncryption'] = 'AES256'

        elif encryption == 'AWS:KMS':
            if 'kms_key' not in param:
                action_result.set_status(phantom.APP_ERROR, "Encryption set to KMS, but no KMS Key has been provided")
            kwargs['ServerSideEncryption'] = 'aws:kms'
            kwargs['SSEKMSKeyId'] = param['kms_key']

        ret_val, resp_json = self._make_boto_call(action_result, 'put_object', **kwargs)

        if (phantom.is_fail(ret_val)):
            return ret_val

        action_result.add_data(resp_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Object successfully created")

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)
        elif action_id == 'list_buckets':
            ret_val = self._handle_list_buckets(param)
        elif action_id == 'get_bucket':
            ret_val = self._handle_get_bucket(param)
        elif action_id == 'update_bucket':
            ret_val = self._handle_update_bucket(param)
        elif action_id == 'create_bucket':
            ret_val = self._handle_create_bucket(param)
        elif action_id == 'list_objects':
            ret_val = self._handle_list_objects(param)
        elif action_id == 'get_object':
            ret_val = self._handle_get_object(param)
        elif action_id == 'update_object':
            ret_val = self._handle_update_object(param)
        elif action_id == 'post_data':
            ret_val = self._handle_post_data(param)

        return ret_val


if __name__ == '__main__':

    import sys
    import pudb
    pudb.set_trace()

    if (len(sys.argv) < 2):
        print "No test json specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = AwsS3Connector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
