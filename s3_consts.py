# File: s3_consts.py
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
S3_JSON_ACCESS_KEY = "access_key"
S3_JSON_SECRET_KEY = "secret_key"  # pragma: allowlist secret
S3_JSON_BOTO_CONFIG = "boto_config"

S3_BAD_BUCKET_MESSAGE = "The specified bucket does not exist"

S3_PERMISSIONS_LIST = ["FULL_CONTROL", "WRITE", "WRITE_ACP", "READ", "READ_ACP"]

S3_BUCKET_INFO_LIST = [
    "Accelerate_Configuration",
    "ACL",
    "CORS",
    "Encryption",
    "Lifecycle_Configuration",
    "Location",
    "Logging",
    "Notification_Configuration",
    "Policy",
    "Replication",
    "Request_Payment",
    "Tagging",
    "Versioning",
    "Website",
]

S3_REGION_DICT = {
    "US East (Ohio)": "us-east-2",
    "US East (N. Virginia)": "us-east-1",
    "US West (N. California)": "us-west-1",
    "US West (Oregon)": "us-west-2",
    "Canada (Central)": "ca-central-1",
    "Asia Pacific (Mumbai)": "ap-south-1",
    "Asia Pacific (Tokyo)": "ap-northeast-1",
    "Asia Pacific (Seoul)": "ap-northeast-2",
    "Asia Pacific (Singapore)": "ap-southeast-1",
    "Asia Pacific (Sydney)": "ap-southeast-2",
    "China (Ningxia)": "cn-northwest-1",
    "EU (Frankfurt)": "eu-central-1",
    "EU (Ireland)": "eu-west-1",
    "EU (London)": "eu-west-2",
    "South America (Sao Paulo)": "sa-east-1",
    "US GovCloud East": "us-gov-east-1",
    "US GovCloud West": "us-gov-west-1",
}

# This value is set by trial and error by quering AWS
S3_ERROR_INVALID_PARAM = "Please provide non-zero positive integer in {param}"
S3_ERROR_CODE_UNAVAILABLE = "Error code unavailable"
S3_ERROR_MESSAGE_UNAVAILABLE = "Error message unavailable. Please check the asset configuration and|or action parameters."
S3_UNICODE_DAMMIT_TYPE_ERROR_MESSAGE = "Error occurred while connecting to the AWS server. \
Please check the asset configuration and|or the action parameters."
S3_BUCKET_LIMIT = 1000

# Integer Validation Keys
S3_LIMIT = "'limit' action parameter"
S3_VALIDATE_INTEGER = "Please provide a valid integer value in the {param}"
S3_BAD_ASSET_CONFIG_MESSAGE = "Please provide access keys or select assume role check box in asset configuration"
