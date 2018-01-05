# --
# File: s3_consts.py
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

S3_JSON_ACCESS_KEY = "access_key"
S3_JSON_SECRET_KEY = "secret_key"

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
        "Website"
    ]

S3_REGION_DICT = {
        "US East (Ohio)": "us-east-1",
        "US East (N. Virginia)": "us-east-2",
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
        "South Americia (Sao Paulo)": "sa-east-1"
    }
