# File: s3_connector.py
#
# Copyright (c) 2018-2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
import ast
import json
import os
import sys
import tempfile
from datetime import datetime

import phantom.app as phantom
import phantom.rules as phantom_rules
import six
from boto3 import Session, client
from botocore.config import Config
from bs4 import UnicodeDammit
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from phantom.vault import Vault

from s3_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class AwsS3Connector(BaseConnector):
    def __init__(self):
        # Call the BaseConnectors init first
        super().__init__()

        self._state = None
        self._region = None
        self._access_key = None
        self._secret_key = None
        self._session_token = None
        self._boto_config = None
        self._proxy = None

    def initialize(self):
        # Fetching the Python major version
        try:
            self._python_version = int(sys.version_info[0])
        except:
            return self.set_status(phantom.APP_ERROR, "Error occurred while fetching the Phantom server's Python major version")

        self._state = self.load_state()

        config = self.get_config()

        self._region = S3_REGION_DICT.get(config["region"])
        if not self._region:
            return self.set_status(phantom.APP_ERROR, "Specified region is not valid")

        self._proxy = {}
        env_vars = config.get("_reserved_environment_variables", {})
        if "HTTP_PROXY" in env_vars:
            self._proxy["http"] = env_vars["HTTP_PROXY"]["value"]
        if "HTTPS_PROXY" in env_vars:
            self._proxy["https"] = env_vars["HTTPS_PROXY"]["value"]

        if config.get("use_role"):
            credentials = self._handle_get_ec2_role()
            if not credentials:
                return self.set_status(phantom.APP_ERROR, "Failed to get EC2 role credentials")
            self._access_key = credentials.access_key
            self._secret_key = credentials.secret_key
            self._session_token = credentials.token

            return phantom.APP_SUCCESS

        self._access_key = config.get(S3_JSON_ACCESS_KEY)
        self._secret_key = config.get(S3_JSON_SECRET_KEY)

        boto_config_str = config.get(S3_JSON_BOTO_CONFIG)
        if boto_config_str:
            try:
                self._boto_config = json.loads(boto_config_str)
            except (json.JSONDecodeError, TypeError) as e:
                return self.set_status(phantom.APP_ERROR, f"Invalid boto_config JSON format: {e}")

        if not (self._access_key and self._secret_key):
            return self.set_status(phantom.APP_ERROR, S3_BAD_ASSET_CONFIG_MESSAGE)

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved accross actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def _handle_get_ec2_role(self):
        session = Session(region_name=self._region)
        credentials = session.get_credentials()
        return credentials

    def _handle_py_ver_compat_for_input_str(self, input_str, always_encode=False):
        """
        This method returns the encoded|original string based on the Python version.
        :param input_str: Input string to be processed
        :param always_encode: Used if the string needs to be encoded for python 3
        :return: input_str (Processed input string based on following logic 'input_str - Python 3; encoded input_str - Python 2')
        """

        try:
            if input_str and (self._python_version == 2 or always_encode):
                input_str = UnicodeDammit(input_str).unicode_markup.encode("utf-8")
        except:
            self.debug_print("Error occurred while handling python 2to3 compatibility for the input string")

        return input_str

    def _get_error_message_from_exception(self, e):
        """This method is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """
        error_code = S3_ERROR_CODE_UNAVAILABLE
        error_message = S3_ERROR_MESSAGE_UNAVAILABLE

        try:
            if e.args:
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_message = e.args[1]
                elif len(e.args) == 1:
                    error_code = S3_ERROR_CODE_UNAVAILABLE
                    error_message = e.args[0]
            else:
                error_code = S3_ERROR_CODE_UNAVAILABLE
                error_message = S3_ERROR_MESSAGE_UNAVAILABLE
        except:
            error_code = S3_ERROR_CODE_UNAVAILABLE
            error_message = S3_ERROR_MESSAGE_UNAVAILABLE

        try:
            error_message = self._handle_py_ver_compat_for_input_str(error_message)
        except TypeError:
            error_message = S3_UNICODE_DAMMIT_TYPE_ERROR_MESSAGE
        except:
            error_message = S3_ERROR_MESSAGE_UNAVAILABLE

        return f"Error Code: {error_code}. Error Message: {error_message}"

    def _validate_integer(self, action_result, parameter, key, allow_zero=False):
        if parameter is not None:
            try:
                if not float(parameter).is_integer():
                    return action_result.set_status(phantom.APP_ERROR, S3_VALIDATE_INTEGER.format(param=key)), None

                parameter = int(parameter)
            except:
                return action_result.set_status(phantom.APP_ERROR, S3_VALIDATE_INTEGER.format(param=key)), None

            if parameter < 0:
                return action_result.set_status(phantom.APP_ERROR, f"Please provide a valid non-negative integer value in the {key}"), None
            if not allow_zero and parameter == 0:
                return action_result.set_status(phantom.APP_ERROR, S3_ERROR_INVALID_PARAM.format(param=key)), None

        return phantom.APP_SUCCESS, parameter

    def _create_client(self, action_result, param=None):
        if self._boto_config:
            boto_config = Config(**self._boto_config)
        else:
            boto_config = None
        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        # Try getting and using temporary assume role credentials from parameters
        temp_credentials = dict()
        if param and "credentials" in param:
            try:
                temp_credentials = ast.literal_eval(param.get("credentials"))
                self._access_key = temp_credentials.get("AccessKeyId", "")
                self._secret_key = temp_credentials.get("SecretAccessKey", "")
                self._session_token = temp_credentials.get("SessionToken", "")

                self.save_progress("Using temporary assume role credentials for action")
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, f"Failed to get temporary credentials:{e}")

        try:
            if self._access_key and self._secret_key:
                self.debug_print("Creating boto3 client with API keys")

                self._client = client(
                    "s3",
                    region_name=self._region,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                    aws_session_token=self._session_token,
                    config=boto_config,
                )

            else:
                self.debug_print("Creating boto3 client without API keys")

                self._client = client("s3", region_name=self._region, config=boto_config)

        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, f"Could not create boto3 client: {error_message}")

        return phantom.APP_SUCCESS

    def _sanatize_dates(self, cur_obj):
        try:
            json.dumps(cur_obj)
            return cur_obj
        except:
            pass

        if isinstance(cur_obj, dict):
            new_dict = {}
            for k, v in six.iteritems(cur_obj):
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
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Invalid method: {method}"), None)

        try:
            resp_json = boto_func(**kwargs)
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, "boto3 call to S3 failed", error_message), None)

        return phantom.APP_SUCCESS, self._sanatize_dates(resp_json)

    def _get_tag_dicts(self, action_result, tags):
        try:
            tag_dict = json.loads(tags)
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, f"Could not decode JSON object from given tag dictionary: {error_message}")
            )

        tag_dicts = []
        for k, v in six.iteritems(tag_dict):
            tag_dicts.append({"Key": k, "Value": v})

        return RetVal(phantom.APP_SUCCESS, tag_dicts)

    def _get_grant_dict(self, action_result, grants, owner):
        try:
            grants = json.loads(grants)
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, f"Could not decode JSON object from given grant dictionary: {error_message}")
            )

        grants_list = []
        for k, v in six.iteritems(grants):
            if v not in S3_PERMISSIONS_LIST:
                return RetVal(action_result.set_status(phantom.APP_ERROR, f"Given permission, {v}, is invalid"))
            grants_list.append({"Grantee": {"Type": "CanonicalUser", "ID": k}, "Permission": v})

        grant_dict = {"Grants": grants_list, "Owner": {"ID": owner}}

        return RetVal(phantom.APP_SUCCESS, grant_dict)

    def _handle_test_connectivity(self, param):
        self.save_progress("Querying S3 to check credentials")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        ret_val, _ = self._make_boto_call(action_result, "list_buckets")

        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            return ret_val

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_buckets(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        ret_val, resp_json = self._make_boto_call(action_result, "list_buckets")

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(resp_json)
        action_result.set_summary({"num_buckets": len(resp_json.get("Buckets", []))})

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_bucket(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        result_json = {}
        summary = action_result.set_summary({})

        for endpoint in S3_BUCKET_INFO_LIST:
            found = True

            ret_val, resp_json = self._make_boto_call(action_result, f"get_bucket_{endpoint.lower()}", Bucket=param.get("bucket"))

            if phantom.is_fail(ret_val):
                if S3_BAD_BUCKET_MESSAGE in action_result.get_message():
                    return ret_val
                else:
                    resp_json = {"Message": action_result.get_message()}
                    found = False

            if len(resp_json) == 1 and "ResponseMetadata" in resp_json:
                resp_json = {"Message": "{} does not appear to be configured for this bucket".format(endpoint.replace("_", " "))}
                found = False

            result_json[endpoint.replace("_", "")] = resp_json
            summary[f"{endpoint.lower()}_found"] = found

        len_bucket_info = len(S3_BUCKET_INFO_LIST)
        for _, value in result_json.items():
            if "Message" in value:
                len_bucket_info = len_bucket_info - 1

        if len_bucket_info == 0:
            return action_result.set_status(phantom.APP_ERROR, "No bucket found")

        action_result.add_data(result_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved bucket info")

    def _handle_create_bucket(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        location = {"LocationConstraint": S3_REGION_DICT[self.get_config()["region"]]}

        ret_val, resp_json = self._make_boto_call(action_result, "create_bucket", Bucket=param.get("bucket"), CreateBucketConfiguration=location)

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(resp_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully created a bucket")

    def _handle_update_bucket(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        is_tags = False
        is_grants = False
        is_encryption = False
        if "tags" in param:
            is_tags = True
            ret_val, tag_dicts = self._get_tag_dicts(action_result, param.get("tags"))

            if phantom.is_fail(ret_val):
                return ret_val

            ret_val, resp_json = self._make_boto_call(
                action_result, "put_bucket_tagging", Bucket=param.get("bucket"), Tagging={"TagSet": tag_dicts}
            )

            if phantom.is_fail(ret_val):
                return ret_val

            action_result.add_data(resp_json)

        if "grants" in param:
            is_grants = True
            if "owner" not in param:
                return action_result.set_status(phantom.APP_ERROR, "No owner provided with grants parameter")

            ret_val, grant_dict = self._get_grant_dict(action_result, param.get("grants"), param.get("owner"))

            if phantom.is_fail(ret_val):
                return ret_val

            ret_val, resp_json = self._make_boto_call(
                action_result, "put_bucket_acl", Bucket=param.get("bucket"), AccessControlPolicy=grant_dict
            )

            if phantom.is_fail(ret_val):
                return ret_val

            action_result.add_data(resp_json)

        if "encryption" in param:
            is_encryption = True
            if param.get("encryption") == "NONE":
                ret_val, resp_json = self._make_boto_call(action_result, "delete_bucket_encryption", Bucket=param.get("bucket"))

            else:
                if param.get("encryption") == "AES256":
                    encrypt_config = {"SSEAlgorithm": "AES256"}

                elif param.get("encryption") == "AWS:KMS":
                    if "kms_key" not in param:
                        return action_result.set_status(phantom.APP_ERROR, "Encryption set to AWS:KMS, but no KMS Key provided.")
                    encrypt_config = {"SSEAlgorithm": "aws:kms", "KMSMasterKeyID": param.get("kms_key")}

                else:
                    return action_result.set_status(phantom.APP_ERROR, "Invalid encryption parameter")

                ret_val, resp_json = self._make_boto_call(
                    action_result,
                    "put_bucket_encryption",
                    Bucket=param.get("bucket"),
                    ServerSideEncryptionConfiguration={"Rules": [{"ApplyServerSideEncryptionByDefault": encrypt_config}]},
                )

            if phantom.is_fail(ret_val):
                return ret_val

            action_result.add_data(resp_json)

        if is_tags or is_grants or is_encryption:
            return action_result.set_status(phantom.APP_SUCCESS, "Successfully updated bucket")
        return action_result.set_status(phantom.APP_ERROR, "Please provide at least one of these parameters: 'tags', 'grants', 'encryption'")

    def _handle_delete_bucket(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        ret_val, resp_json = self._make_boto_call(action_result, "delete_bucket", Bucket=param.get("bucket"))

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(resp_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully deleted bucket")

    def _handle_list_objects(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        limit = param.get("limit", 1000)
        ret_val, limit = self._validate_integer(action_result, limit, S3_LIMIT)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        if not self._create_client(action_result, param):
            return action_result.get_status()

        nextContinuationToken = ""
        if "continuation_token" in param:
            nextContinuationToken = param.get("continuation_token")

        num_objects = 0
        result_list = []
        bucket_limit = S3_BUCKET_LIMIT

        while True:
            if limit < bucket_limit:
                current_limit = limit
            else:
                current_limit = bucket_limit

            if nextContinuationToken:
                ret_val, resp_json = self._make_boto_call(
                    action_result,
                    "list_objects_v2",
                    Bucket=param.get("bucket"),
                    StartAfter=param.get("key", ""),
                    ContinuationToken=nextContinuationToken,
                    MaxKeys=current_limit,
                    FetchOwner=True,
                )
            else:
                ret_val, resp_json = self._make_boto_call(
                    action_result,
                    "list_objects_v2",
                    Bucket=param.get("bucket"),
                    StartAfter=param.get("key", ""),
                    MaxKeys=current_limit,
                    FetchOwner=True,
                )

            if phantom.is_fail(ret_val):
                return ret_val

            result_list.append(resp_json)
            num_objects = num_objects + resp_json.get("KeyCount", 0)
            limit = limit - current_limit
            if limit <= 0:
                break
            if "NextContinuationToken" not in resp_json:
                break
            else:
                nextContinuationToken = resp_json["NextContinuationToken"]

        action_result.add_data(result_list)
        action_result.set_summary({"num_objects": num_objects})
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_object(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        ret_val, resp_json = self._make_boto_call(action_result, "get_object_tagging", Bucket=param.get("bucket"), Key=param.get("key"))

        if phantom.is_fail(ret_val):
            return ret_val

        result_json = {"Tagging": resp_json}

        ret_val, resp_json = self._make_boto_call(action_result, "get_object_acl", Bucket=param.get("bucket"), Key=param.get("key"))

        if phantom.is_fail(ret_val):
            return ret_val

        result_json["ACL"] = resp_json

        if param.get("download_file"):
            ret_val, resp_json = self._make_boto_call(action_result, "get_object", Bucket=param.get("bucket"), Key=param.get("key"))

            if phantom.is_fail(ret_val):
                return ret_val

            try:
                file_data = resp_json.pop("Body").read()
            except:
                return action_result.set_status(phantom.APP_ERROR, "Could not retrieve object body from boto response")

            if hasattr(Vault, "get_vault_tmp_dir"):
                vault_path = Vault.get_vault_tmp_dir()
            else:
                vault_path = "/vault/tmp/"

            file_desc, file_path = tempfile.mkstemp(dir=vault_path)
            outfile = open(file_path, "wb")
            outfile.write(file_data)
            outfile.close()
            os.close(file_desc)

            try:
                vault_ret = Vault.add_attachment(file_path, self.get_container_id(), os.path.basename(param.get("key")))
            except Exception as e:
                error_message = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR, f"Could not save file to vault: {error_message}")

            if not vault_ret.get("succeeded"):
                return action_result.set_status(
                    phantom.APP_ERROR, "Could not save file to vault: {}".format(vault_ret.get("message", "Unknown Error"))
                )

            vault_id = vault_ret[phantom.APP_JSON_HASH]
            resp_json["vault_id"] = vault_id
            resp_json["filename"] = os.path.basename(param.get("key"))
            result_json["File"] = resp_json
            action_result.set_summary({"created_vault_id": vault_id})

        action_result.add_data(result_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved object info")

    def _handle_update_object(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        is_tags = False
        is_grants = False
        if "tags" in param:
            is_tags = True
            ret_val, tag_dicts = self._get_tag_dicts(action_result, param.get("tags"))

            if phantom.is_fail(ret_val):
                return ret_val

            ret_val, resp_json = self._make_boto_call(
                action_result, "put_object_tagging", Bucket=param.get("bucket"), Key=param.get("key"), Tagging={"TagSet": tag_dicts}
            )

            if phantom.is_fail(ret_val):
                return ret_val

            action_result.add_data(resp_json)

        if "grants" in param:
            is_grants = True
            if "owner" not in param:
                return action_result.set_status(phantom.APP_ERROR, "No owner provided with grants parameter")

            ret_val, grant_dict = self._get_grant_dict(action_result, param.get("grants"), param.get("owner"))

            if phantom.is_fail(ret_val):
                return ret_val

            ret_val, resp_json = self._make_boto_call(
                action_result, "put_object_acl", Bucket=param.get("bucket"), Key=param.get("key"), AccessControlPolicy=grant_dict
            )

            if phantom.is_fail(ret_val):
                return ret_val

            action_result.add_data(resp_json)

        if is_tags or is_grants:
            return action_result.set_status(phantom.APP_SUCCESS, "Object successfully updated")
        return action_result.set_status(phantom.APP_ERROR, "Please provide at least one of these parameters: 'tags', 'grants'")

    def _handle_delete_object(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        ret_val, resp_json = self._make_boto_call(action_result, "delete_object", Bucket=param.get("bucket"), Key=param.get("key"))

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(resp_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully deleted object")

    def _handle_post_data(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        vault_id = param.get("vault_id")

        try:
            _, _, file_info = phantom_rules.vault_info(vault_id=vault_id)
            file_path = next(iter(file_info)).get("path")
            if not file_path:
                return action_result.set_status(phantom.APP_ERROR, "Could not find given vault ID in vault")
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, f"Could not find given vault ID.Error message from vault: {error_message}")

        upfile = open(file_path, "rb")
        kwargs = {"Body": upfile, "Bucket": param.get("bucket"), "Key": param.get("key"), "StorageClass": param.get("storage_class")}

        if "metadata" in param:
            try:
                meta_dict = json.loads(param.get("metadata"))
            except Exception as e:
                error_message = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR, f"Could not load JSON object from given metadata: {error_message}")

            kwargs["Metadata"] = meta_dict

        encryption = param.get("encryption")

        if "kms_key" in param and encryption != "AWS:KMS":
            return action_result.set_status(phantom.APP_ERROR, "KMS key has been provided but encryption not set as AWS:KMS")

        if encryption == "AES256":
            kwargs["ServerSideEncryption"] = "AES256"

        elif encryption == "AWS:KMS":
            if "kms_key" not in param:
                return action_result.set_status(phantom.APP_ERROR, "Encryption set to KMS, but no KMS Key has been provided")
            kwargs["ServerSideEncryption"] = "aws:kms"
            kwargs["SSEKMSKeyId"] = param.get("kms_key")

        elif encryption != "NONE":
            return action_result.set_status(phantom.APP_ERROR, "Invalid encryption parameter")

        ret_val, resp_json = self._make_boto_call(action_result, "put_object", **kwargs)

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(resp_json)

        return action_result.set_status(phantom.APP_SUCCESS, "Object successfully created")

    def _handle_generate_presigned_url(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary

        # Required values can be accessed directly
        client_method = param["client_method"]
        bucket_name = param["bucket_name"]
        object_name = param["object_name"]

        # Optional values should use the .get() function
        method_parameters = param.get("method_parameters", "")
        expiration = param.get("expiration", "")

        if not self._create_client(action_result, param):
            return action_result.get_status()

        required_parameters = {"Bucket": bucket_name, "Key": object_name}

        if method_parameters:
            method_parameters = json.loads(method_parameters) | required_parameters
        else:
            method_parameters = required_parameters

        ret_val, resp_json = self._make_boto_call(
            action_result, "generate_presigned_url", ClientMethod=client_method, Params=method_parameters, ExpiresIn=expiration
        )

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data({"url": resp_json})

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully Generated Pre-Signed URL")

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == "generate_presigned_url":
            ret_val = self._handle_generate_presigned_url(param)
        elif action_id == "test_connectivity":
            ret_val = self._handle_test_connectivity(param)
        elif action_id == "list_buckets":
            ret_val = self._handle_list_buckets(param)
        elif action_id == "get_bucket":
            ret_val = self._handle_get_bucket(param)
        elif action_id == "update_bucket":
            ret_val = self._handle_update_bucket(param)
        elif action_id == "create_bucket":
            ret_val = self._handle_create_bucket(param)
        elif action_id == "delete_bucket":
            ret_val = self._handle_delete_bucket(param)
        elif action_id == "list_objects":
            ret_val = self._handle_list_objects(param)
        elif action_id == "get_object":
            ret_val = self._handle_get_object(param)
        elif action_id == "update_object":
            ret_val = self._handle_update_object(param)
        elif action_id == "delete_object":
            ret_val = self._handle_delete_object(param)
        elif action_id == "post_data":
            ret_val = self._handle_post_data(param)

        return ret_val


if __name__ == "__main__":
    import pudb

    pudb.set_trace()

    if len(sys.argv) < 2:
        print("No test json specified as input")
        sys.exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = AwsS3Connector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
