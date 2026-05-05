# AWS S3

Publisher: Splunk <br>
Connector Version: 2.5.2 <br>
Product Vendor: AWS <br>
Product Name: S3 <br>
Minimum Product Version: 5.1.0

This app integrates with AWS S3 to perform investigative actions

## SDK and SDK Licensing details for the app

### urllib3

This app uses the urllib3 module, which is licensed under the MIT License (MIT), Copyright (c)
Andrey Petrov.

## Asset Configuration

There are two ways to configure an AWS S3 asset. The first is to configure the **access_key** ,
**secret_key** and **region** variables. If it is preferred to use a role and Phantom is running as
an EC2 instance, the **use_role** checkbox can be checked instead. This will allow the role that is
attached to the instance to be used. Please see the [AWS EC2 and IAM
documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
for more information.

Region parameter provided in the asset configuration parameter and region of the bucket which is
created in AWS console must match otherwise user will get InvalidLocationConstraint error.

For the **Update bucket** action,
API is unable to validate the KMS key. Hence, it is recommended to provide a
valid KMS key in this action parameter otherwise it will affect the S3 bucket.
e.g If we update the S3 bucket with the invalid KMS key and then run create object action on the bucket then the action will not work for encryption = NONE.

## Assumed Role Credentials

The optional **credentials** action parameter consists of temporary **assumed role** credentials
that will be used to perform the action instead of those that are configured in the **asset** . The
parameter is not designed to be configured manually, but should be used in conjunction with the
Phantom AWS Security Token Service app. The output of the **assume_role** action of the STS app with
data path **assume_role\_\<number>:action_result.data.\*.Credentials** consists of a dictionary
containing the **AccessKeyId** , **SecretAccessKey** , **SessionToken** and **Expiration** key/value
pairs. This dictionary can be passed directly into the credentials parameter in any of the following
actions within a playbook. For more information, please see the [AWS Identity and Access Management
documentation](https://docs.aws.amazon.com/iam/index.html) .

### Configuration variables

This table lists the configuration variables required to operate AWS S3. These variables are specified when configuring a S3 asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access_key** | optional | password | Access Key |
**secret_key** | optional | password | Secret Key |
**region** | required | string | Default Region |
**use_role** | optional | boolean | Use attached role when running Phantom in EC2 |
**boto_config** | optional | string | Dictionary of boto3 config options |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration <br>
[list buckets](#action-list-buckets) - List all buckets configured on S3 <br>
[get bucket](#action-get-bucket) - Get information about a bucket <br>
[create bucket](#action-create-bucket) - Create a bucket <br>
[update bucket](#action-update-bucket) - Update a bucket <br>
[delete bucket](#action-delete-bucket) - Delete a bucket <br>
[list objects](#action-list-objects) - List objects in a bucket <br>
[get object](#action-get-object) - Get information about an object <br>
[update object](#action-update-object) - Update an object <br>
[create object](#action-create-object) - Create an object <br>
[delete object](#action-delete-object) - Delete an object inside a bucket <br>
[generate presigned url](#action-generate-presigned-url) - Generate a Pre-Signed S3 URL

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'list buckets'

List all buckets configured on S3

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'AKIAIOSFODNN7EXAMPLE', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', 'SessionToken': 'EXAMPLETESTzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEXAMPLETEST2QpWctS2BGn4n+G8cD6zEweCCEXAMPLETESTYI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jEXAMPLETESToL2v3ZZZZZZ=='} |
action_result.status | string | | success failed |
action_result.data.\*.Buckets.\*.Name | string | | aws-athena-query-results-157568067690-us-west-2 |
action_result.data.\*.Buckets.\*.CreationDate | string | | 2017-09-13 21:33:57 |
action_result.data.\*.Owner.DisplayName | string | | Display Name |
action_result.data.\*.Owner.ID | string | `aws canonical id` `sha256` | 042b3oe6d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string | | application/xml |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Tue, 12 Dec 2017 21:40:22 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | 6Y10uFMWGRF9mu1P94EVq9YpbFFkSxGEGU9ppx6hBVRiaaEANjyS2zuZoM5tt95QYOve9j0l6r4= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | DE264B470D5AD443 |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.HostId | string | | 6Y10uFMWGRF9mu1P94EVq9YpbFFkSxGEGU9ppx6hBVRiaaEANjyS2zuZoM5tt95QYOve9j0l6r4= |
action_result.data.\*.ResponseMetadata.RequestId | string | | DE264B470D5AD443 |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary.num_buckets | numeric | | 4 |
action_result.message | string | | Num buckets: 4 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get bucket'

Get information about a bucket

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** | required | Bucket to get | string | `aws s3 bucket` |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.bucket | string | `aws s3 bucket` | bucket-test-s3-app |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.data.\*.ACL.Grants.\*.Grantee.DisplayName | string | | Display Name |
action_result.data.\*.ACL.Grants.\*.Grantee.ID | string | | 042b3oe6d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444 |
action_result.data.\*.ACL.Grants.\*.Grantee.Type | string | | CanonicalUser |
action_result.data.\*.ACL.Grants.\*.Grantee.URI | string | | http://acs.amazonaws.com/groups/s3/LogDelivery |
action_result.data.\*.ACL.Grants.\*.Permission | string | | FULL_CONTROL |
action_result.data.\*.ACL.Message | string | | |
action_result.data.\*.ACL.Owner.DisplayName | string | | Display Name |
action_result.data.\*.ACL.Owner.ID | string | `sha256` | 042b3oe6d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444 |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.content-type | string | | application/xml |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:58 GMT |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | dVMKBJp6MBOXFeuly8O8SqLkq+lXnEbl+KMvx+LK7EyGpPSm88mUD+juN/JIb4/17votLkWEo5k= |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 400B6B0D1EB90D9B |
action_result.data.\*.ACL.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ACL.ResponseMetadata.HostId | string | | dVMKBJp6MBOXFeuly8O8SqLkq+lXnEbl+KMvx+LK7EyGpPSm88mUD+juN/JIb4/17votLkWEo5k= |
action_result.data.\*.ACL.ResponseMetadata.RequestId | string | | 400B6B0D1EB90D9B |
action_result.data.\*.ACL.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.AccelerateConfiguration.Message | string | | |
action_result.data.\*.AccelerateConfiguration.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:58 GMT |
action_result.data.\*.AccelerateConfiguration.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.AccelerateConfiguration.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.AccelerateConfiguration.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | R6sl3E4MCVoudKZtNHj2gtCFkU1Sm12st2U2xyfEBj4tvjqrqXL3uo88EyrcDn5qZLjzu2B1YD0= |
action_result.data.\*.AccelerateConfiguration.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 7CC77C9375FA19D7 |
action_result.data.\*.AccelerateConfiguration.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.AccelerateConfiguration.ResponseMetadata.HostId | string | | R6sl3E4MCVoudKZtNHj2gtCFkU1Sm12st2U2xyfEBj4tvjqrqXL3uo88EyrcDn5qZLjzu2B1YD0= |
action_result.data.\*.AccelerateConfiguration.ResponseMetadata.RequestId | string | | 7CC77C9375FA19D7 |
action_result.data.\*.AccelerateConfiguration.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.AccelerateConfiguration.Status | string | | Enabled |
action_result.data.\*.CORS.CORSRules.\*.AllowedHeaders | string | | Authorization |
action_result.data.\*.CORS.CORSRules.\*.AllowedMethods | string | | GET |
action_result.data.\*.CORS.CORSRules.\*.AllowedOrigins | string | | * |
action_result.data.\*.CORS.CORSRules.\*.MaxAgeSeconds | numeric | | 3000 |
action_result.data.\*.CORS.Message | string | | |
action_result.data.\*.CORS.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.CORS.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.CORS.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.CORS.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | PobDFB96nb4du4tci/k/JhWRhQ7u7qlKiPTBz5zYhoXLtYiHZrElMv76dnn84ztEhYuDJfKF0jY= |
action_result.data.\*.CORS.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 93C96F053B042568 |
action_result.data.\*.CORS.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.CORS.ResponseMetadata.HostId | string | | PobDFB96nb4du4tci/k/JhWRhQ7u7qlKiPTBz5zYhoXLtYiHZrElMv76dnn84ztEhYuDJfKF0jY= |
action_result.data.\*.CORS.ResponseMetadata.RequestId | string | | 93C96F053B042568 |
action_result.data.\*.CORS.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.Encryption.Message | string | | |
action_result.data.\*.Encryption.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.Encryption.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.Encryption.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.Encryption.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | 88lWjF7Nc6u9SZKgAnm8/XzRl/t+Pp5huR9dMDJPt+X5q8XWG+cuyi+LUNoLeinJ3ZFRO1+9jwE= |
action_result.data.\*.Encryption.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | E2F41A6CA939A2EA |
action_result.data.\*.Encryption.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.Encryption.ResponseMetadata.HostId | string | | 88lWjF7Nc6u9SZKgAnm8/XzRl/t+Pp5huR9dMDJPt+X5q8XWG+cuyi+LUNoLeinJ3ZFRO1+9jwE= |
action_result.data.\*.Encryption.ResponseMetadata.RequestId | string | | E2F41A6CA939A2EA |
action_result.data.\*.Encryption.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.Encryption.ServerSideEncryptionConfiguration.Rules.\*.ApplyServerSideEncryptionByDefault.KMSMasterKeyID | string | | |
action_result.data.\*.Encryption.ServerSideEncryptionConfiguration.Rules.\*.ApplyServerSideEncryptionByDefault.SSEAlgorithm | string | | AES256 |
action_result.data.\*.LifecycleConfiguration.Message | string | | |
action_result.data.\*.LifecycleConfiguration.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.LifecycleConfiguration.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.LifecycleConfiguration.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.LifecycleConfiguration.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | wEO4b0tAeTUv8XlRM2oHp40WpBQtmjjRcYIoMMY2ebf2EAbl4mW0kd0gsKuxSKqHLEOjNvAUnJI= |
action_result.data.\*.LifecycleConfiguration.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | EFEC0AADFC1BAA99 |
action_result.data.\*.LifecycleConfiguration.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.LifecycleConfiguration.ResponseMetadata.HostId | string | | wEO4b0tAeTUv8XlRM2oHp40WpBQtmjjRcYIoMMY2ebf2EAbl4mW0kd0gsKuxSKqHLEOjNvAUnJI= |
action_result.data.\*.LifecycleConfiguration.ResponseMetadata.RequestId | string | | EFEC0AADFC1BAA99 |
action_result.data.\*.LifecycleConfiguration.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.LifecycleConfiguration.Rules.\*.Filter.Prefix | string | | |
action_result.data.\*.LifecycleConfiguration.Rules.\*.ID | string | | Test Rule |
action_result.data.\*.LifecycleConfiguration.Rules.\*.NoncurrentVersionExpiration.NoncurrentDays | numeric | | 365 |
action_result.data.\*.LifecycleConfiguration.Rules.\*.Status | string | | Enabled |
action_result.data.\*.Location.LocationConstraint | string | | us-west-1 |
action_result.summary.encryption_found | boolean | | True False |
action_result.data.\*.Location.Message | string | | |
action_result.data.\*.Location.ResponseMetadata.HTTPHeaders.content-type | string | | application/xml |
action_result.data.\*.Location.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.Location.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.Location.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.Location.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | efUmLHB5XHT43yX1hqt+0UTnJI4W+exTikxVScJleEw3D8apdpVk1/QLDV4rEVNHbosaGoulve0= |
action_result.data.\*.Location.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 974B5B65D55DD88A |
action_result.data.\*.Location.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.Location.ResponseMetadata.HostId | string | | efUmLHB5XHT43yX1hqt+0UTnJI4W+exTikxVScJleEw3D8apdpVk1/QLDV4rEVNHbosaGoulve0= |
action_result.data.\*.Location.ResponseMetadata.RequestId | string | | 974B5B65D55DD88A |
action_result.data.\*.Location.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.Logging.LoggingEnabled.TargetBucket | string | | bucket-test-s3-app |
action_result.data.\*.Logging.LoggingEnabled.TargetPrefix | string | | |
action_result.data.\*.Logging.Message | string | | |
action_result.data.\*.Logging.ResponseMetadata.HTTPHeaders.content-type | string | | application/xml |
action_result.data.\*.Logging.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.Logging.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.Logging.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.Logging.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | SGyUaKSZu5Hdjlv2ZnFK93ylMkS7kfMxiZ+ifIe0dmGHfbRq0qsDLepIRJ90J9gpjTP5VejExcE= |
action_result.data.\*.Logging.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | F175D7AA0B2FADEF |
action_result.data.\*.Logging.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.Logging.ResponseMetadata.HostId | string | | SGyUaKSZu5Hdjlv2ZnFK93ylMkS7kfMxiZ+ifIe0dmGHfbRq0qsDLepIRJ90J9gpjTP5VejExcE= |
action_result.data.\*.Logging.ResponseMetadata.RequestId | string | | F175D7AA0B2FADEF |
action_result.data.\*.Logging.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.NotificationConfiguration.LambdaFunctionConfigurations.\*.Events | string | | s3:ObjectRemoved:Delete |
action_result.data.\*.NotificationConfiguration.LambdaFunctionConfigurations.\*.Id | string | | SendToLambda |
action_result.data.\*.NotificationConfiguration.LambdaFunctionConfigurations.\*.LambdaFunctionArn | string | | arn:aws:lambda:us-west-1:157568067690:function:TestFunction |
action_result.data.\*.NotificationConfiguration.Message | string | | |
action_result.data.\*.NotificationConfiguration.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.NotificationConfiguration.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.NotificationConfiguration.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.NotificationConfiguration.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | 2+pdHq+fCGQoOpCxJQm8dEKEezWKW5cf9sKxGMZRfmuGkHY/D2B4WhP+Wh+V/nqlzgTUoLDtGgE= |
action_result.data.\*.NotificationConfiguration.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 05FC1183F2D73562 |
action_result.data.\*.NotificationConfiguration.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.NotificationConfiguration.ResponseMetadata.HostId | string | | 2+pdHq+fCGQoOpCxJQm8dEKEezWKW5cf9sKxGMZRfmuGkHY/D2B4WhP+Wh+V/nqlzgTUoLDtGgE= |
action_result.data.\*.NotificationConfiguration.ResponseMetadata.RequestId | string | | 05FC1183F2D73562 |
action_result.data.\*.NotificationConfiguration.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.Policy.Message | string | | |
action_result.data.\*.Policy.Policy | string | | {"Version":"2012-10-17","Id":"S3-Console-Auto-Gen-Policy-1515018655847","Statement":[{"Sid":"S3PolicyStmt-DO-NOT-MODIFY-1515018655847","Effect":"Allow","Principal":{"Service":"s3.amazonaws.com"},"Action":"s3:PutObject","Resource":"arn:aws:s3:::bucket-test-s3-app/\*","Condition":{"StringEquals":{"aws:SourceAccount":"157568067690","s3:x-amz-acl":"bucket-owner-full-control"},"ArnLike":{"aws:SourceArn":"arn:aws:s3:::bucket-test-s3-app"}}}]} |
action_result.data.\*.Policy.ResponseMetadata.HTTPHeaders.content-length | string | | 437 |
action_result.data.\*.Policy.ResponseMetadata.HTTPHeaders.content-type | string | | application/json |
action_result.data.\*.Policy.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.Policy.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.Policy.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | eY6Ak2rAXwNc5kYXBuF4hr0ZDcaaE7lg0jLGlIuVvDTkemzt6aaDfIOYVlTmApZrR87xmSnfTMg= |
action_result.data.\*.Policy.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 224AD418821025F9 |
action_result.data.\*.Policy.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.Policy.ResponseMetadata.HostId | string | | eY6Ak2rAXwNc5kYXBuF4hr0ZDcaaE7lg0jLGlIuVvDTkemzt6aaDfIOYVlTmApZrR87xmSnfTMg= |
action_result.data.\*.Policy.ResponseMetadata.RequestId | string | | 224AD418821025F9 |
action_result.data.\*.Policy.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.Replication.Message | string | | |
action_result.data.\*.Replication.ReplicationConfiguration.Role | string | | arn:aws:iam::157568067690:role/service-role/s3crr_role_for-test-s3-app_to-rep-bucket |
action_result.data.\*.Replication.ReplicationConfiguration.Rules.\*.Destination.Bucket | string | | arn:aws:s3:::rep-bucket |
action_result.data.\*.Replication.ReplicationConfiguration.Rules.\*.ID | string | | ODgzNWQyYTYtODhjNC00NWM4LWJkNWMtMDRjZTUxNDRiM2Iz |
action_result.data.\*.Replication.ReplicationConfiguration.Rules.\*.Prefix | string | | |
action_result.data.\*.Replication.ReplicationConfiguration.Rules.\*.Status | string | | Enabled |
action_result.data.\*.Replication.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.Replication.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.Replication.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.Replication.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | VetpF5OhOs7qbLEZl2C9oby4KoU4HLL/+pmwEnnIphoC0qVCajcgloD5D1KClbAuslA+KnwTvZs= |
action_result.data.\*.Replication.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | B657CA18ACC804A2 |
action_result.data.\*.Replication.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.Replication.ResponseMetadata.HostId | string | | VetpF5OhOs7qbLEZl2C9oby4KoU4HLL/+pmwEnnIphoC0qVCajcgloD5D1KClbAuslA+KnwTvZs= |
action_result.data.\*.Replication.ResponseMetadata.RequestId | string | | B657CA18ACC804A2 |
action_result.data.\*.Replication.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.RequestPayment.Message | string | | |
action_result.data.\*.RequestPayment.Payer | string | | BucketOwner |
action_result.data.\*.RequestPayment.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.RequestPayment.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.RequestPayment.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.RequestPayment.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | BJFQ9lc8CXosHwpNY2VFcvrGTp+fVzu+5yANomNE4YKz8LFeVtFO2SZkwCRVrfKrCWqOLuCb4Rs= |
action_result.data.\*.RequestPayment.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | E46C030279C07CD2 |
action_result.data.\*.RequestPayment.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.RequestPayment.ResponseMetadata.HostId | string | | BJFQ9lc8CXosHwpNY2VFcvrGTp+fVzu+5yANomNE4YKz8LFeVtFO2SZkwCRVrfKrCWqOLuCb4Rs= |
action_result.data.\*.RequestPayment.ResponseMetadata.RequestId | string | | E46C030279C07CD2 |
action_result.data.\*.RequestPayment.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.Tagging.Message | string | | |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | wdu+mB75tYS8r9qaZvI+BD3OQixeOliVvs41hF/s8hUEu9MRiZmNKk7s/Gfpw94C2i7hMiS5CPM= |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | AF6A1E6B709EA88A |
action_result.data.\*.Tagging.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.Tagging.ResponseMetadata.HostId | string | | wdu+mB75tYS8r9qaZvI+BD3OQixeOliVvs41hF/s8hUEu9MRiZmNKk7s/Gfpw94C2i7hMiS5CPM= |
action_result.data.\*.Tagging.ResponseMetadata.RequestId | string | | AF6A1E6B709EA88A |
action_result.data.\*.Tagging.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.Tagging.TagSet.\*.Key | string | | A Tag |
action_result.data.\*.Tagging.TagSet.\*.Value | string | | Just to tag |
action_result.data.\*.Versioning.Message | string | | |
action_result.data.\*.Versioning.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.Versioning.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.Versioning.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.Versioning.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | 3D4B9A81VlnFLQWB1mb7FgGXI8pBpI9ZeXOkky1KwD9K56YthaEHB57rzQMsOLgauxIpdDsgEbE= |
action_result.data.\*.Versioning.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 7EBE0E5D70258A40 |
action_result.data.\*.Versioning.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.Versioning.ResponseMetadata.HostId | string | | 3D4B9A81VlnFLQWB1mb7FgGXI8pBpI9ZeXOkky1KwD9K56YthaEHB57rzQMsOLgauxIpdDsgEbE= |
action_result.data.\*.Versioning.ResponseMetadata.RequestId | string | | 7EBE0E5D70258A40 |
action_result.data.\*.Versioning.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary.replication_found | boolean | | True False |
action_result.summary.notification_configuration_found | boolean | | True False |
action_result.data.\*.Versioning.Status | string | | Enabled |
action_result.data.\*.Website.ErrorDocument.Key | string | | error.html |
action_result.data.\*.Website.IndexDocument.Suffix | string | | host.html |
action_result.data.\*.Website.Message | string | | |
action_result.data.\*.Website.ResponseMetadata.HTTPHeaders.content-type | string | | application/xml |
action_result.data.\*.Website.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 00:18:59 GMT |
action_result.data.\*.Website.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.Website.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.Website.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | 73eXrr6SyRHY4R0ED3bwG7yve1R3Oh+mYOqryPrRaoBBqyERwGev67o0S2rPJeHE5wNpi76vixg= |
action_result.data.\*.Website.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | DC1EDDAEAA519ADD |
action_result.data.\*.Website.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.Website.ResponseMetadata.HostId | string | | 73eXrr6SyRHY4R0ED3bwG7yve1R3Oh+mYOqryPrRaoBBqyERwGev67o0S2rPJeHE5wNpi76vixg= |
action_result.data.\*.Website.ResponseMetadata.RequestId | string | | DC1EDDAEAA519ADD |
action_result.data.\*.Website.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary.accelerate_configuration_found | boolean | | True False |
action_result.summary.acl_found | boolean | | True False |
action_result.summary.cors_found | boolean | | True False |
action_result.summary.logging_found | boolean | | True False |
action_result.summary.lifecycle_configuration_found | boolean | | True False |
action_result.summary.location_found | boolean | | True False |
action_result.summary.policy_found | boolean | | True False |
action_result.summary.request_payment_found | boolean | | True False |
action_result.summary.tagging_found | boolean | | True False |
action_result.summary.versioning_found | boolean | | True False |
action_result.summary.website_found | boolean | | True False |
action_result.message | string | | Successfully retrieved bucket info |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'create bucket'

Create a bucket

Type: **generic** <br>
Read only: **False**

The bucket will be created in the region specified in the asset configuration. The bucket name provided has to be unique and it should not be already used in the AWS S3 globally.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** | required | Name of bucket to create | string | `aws s3 bucket` |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.bucket | string | `aws s3 bucket` | automated-bucket |
action_result.status | string | | success failed |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.data.\*.Location | string | `url` | http://automated-bucket.s3.amazonaws.com/ |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | numeric | | 72 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 01:14:36 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.location | string | `url` | http://automated-bucket.s3.amazonaws.com/ |
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | pi+Esw7Nc2VRmCeolShRpzN4kq2fjY4inqIXBTZ1ziI955Nvluh9K2oxN9z+dpmEotWh24K8Pc0= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 6F9DC34BE8E46AA5 |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.HostId | string | | pi+Esw7Nc2VRmCeolShRpzN4kq2fjY4inqIXBTZ1ziI955Nvluh9K2oxN9z+dpmEotWh24K8Pc0= |
action_result.data.\*.ResponseMetadata.RequestId | string | | 6F9DC34BE8E46AA5 |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary | string | | |
action_result.message | string | | Successfully created a bucket |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 0 |

## action: 'update bucket'

Update a bucket

Type: **generic** <br>
Read only: **False**

The <b>tags</b> parameter takes a JSON dictionary containing the tags that will be given to the specified <b>bucket</b>. The dictionary should have the format:<br><br><pre>{<br> "tag1_key": "tag1_value",<br> "tag2_key": "tag2_value"<br> ...<br>}</pre><br>The <b>grants</b> parameter takes a dictionary where each key is a canonical user ID and each value is one of the following permissions:<ul><li>FULL_CONTROL</li><li>WRITE</li><li>WRITE_ACP</li><li>READ</li><li>READ_ACP</li></ul>An example JSON object would be:<br><br><pre>{<br> "111a11a11aa1111111aa11aaa1111a111a1aa111111a1a1a11aa11aa11a11aa1": "FULL_CONTROL",<br> "222b22b22bb2222222bb22bbb2222b222b2bb222222b2b2b22bb22bb22b22bb2": "READ"<br>}</pre><br>The <b>owner</b> parameter takes the canonical ID of an AWS user. This parameter must be provided if the <b>grants</b> parameter is included (even if there is no desire to change the owner; in this case, just provide the ID of the current owner of the bucket).<br><br>WARNING: Calling this action will replace the bucket's current tags and permissions with the tags and permission supplied to this action. To avoid overwriting the bucket's present data, first run <b>get bucket</b> to get the current tag and permission dictionaries, then add new tags and grants to those dictionaries before calling this action.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** | required | Name of bucket to update | string | `aws s3 bucket` |
**tags** | optional | JSON dictionary containing tags to give object | string | |
**encryption** | optional | Encryption to apply to bucket | string | |
**kms_key** | optional | KMS Key (Only if encryption is AWS:KMS) | string | |
**grants** | optional | JSON dictionary of users and the permissions to grant them | string | |
**owner** | optional | Canonical ID of new owner | string | `aws canonical id` |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.bucket | string | `aws s3 bucket` | bucket-test-s3-app |
action_result.status | string | | success failed |
action_result.parameter.encryption | string | | AWS:KMS |
action_result.parameter.grants | string | | {"153b1da9d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444": "FULL_CONTROL", "617d70b19fe7594450bf60dbd5004d026f7ae739872e5a3b81ca16eb15e94df8": "FULL_CONTROL"} |
action_result.parameter.kms_key | string | | 28dc6a18-f1ac-11e7-8c3f-9a214cf093ae |
action_result.message | string | | Successfully retrieved bucket info |
action_result.parameter.owner | string | `aws canonical id` | 042b3oe6d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444 |
action_result.parameter.tags | string | | {"key1": "value1", "key2": "value2"} |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | numeric | | 72 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Fri, 05 Jan 2018 00:10:55 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | YgV/to0Eq1A0cwfqQG2YuGW57E83UrUNprkccKSnMj2ocdWSYXxtQy+4J3NVAMY46IeyWQLgxjQ= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 39ACD3F305817EE3 |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 204 |
action_result.data.\*.ResponseMetadata.HostId | string | | YgV/to0Eq1A0cwfqQG2YuGW57E83UrUNprkccKSnMj2ocdWSYXxtQy+4J3NVAMY46IeyWQLgxjQ= |
action_result.data.\*.ResponseMetadata.RequestId | string | | 39ACD3F305817EE3 |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'delete bucket'

Delete a bucket

Type: **generic** <br>
Read only: **False**

The bucket will be deleted. All objects (including all object versions and delete markers) in the bucket must be deleted before the bucket itself can be deleted. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** | required | Name of bucket to delete | string | `aws s3 bucket` |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.bucket | string | `aws s3 bucket` | automated-bucket |
action_result.status | string | | success failed |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | numeric | | 72 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 01:14:36 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | pi+Esw7Nc2VRmCeolShRpzN4kq2fjY4inqIXBTZ1ziI955Nvluh9K2oxN9z+dpmEotWh24K8Pc0= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 6F9DC34BE8E46AA5 |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.HostId | string | | pi+Esw7Nc2VRmCeolShRpzN4kq2fjY4inqIXBTZ1ziI955Nvluh9K2oxN9z+dpmEotWh24K8Pc0= |
action_result.data.\*.ResponseMetadata.RequestId | string | | 6F9DC34BE8E46AA5 |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary | string | | |
action_result.message | string | | Successfully deleted bucket |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 0 |

## action: 'list objects'

List objects in a bucket

Type: **investigate** <br>
Read only: **True**

This action will list all objects in the given <b>bucket</b>. It will recursively list all objects in each folder in the bucket as well.<br><br>If given the <b>key</b> parameter, the action will start listing objects at the given key (which could include objects at the same level as the specified key). The <b>key</b> must be a full path from the root of the <b>bucket</b>.<br><br>The <b>limit</b> parameter has a maximum value of 1000. If no <b>limit</b> is provided, it will default to 1000. If more objects than the specified <b>limit</b> exist, the action will return a <b>NextContinuationToken</b>. To get the next batch of objects, pass this token in a new action as the <b>continuation_token</b>.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** | required | List objects in this bucket | string | `aws s3 bucket` |
**key** | optional | List objects under this key | string | `aws s3 key` |
**limit** | optional | Max number of objects to list | numeric | |
**continuation_token** | optional | Use this parameter to get the next set of objects from a previous action | string | `aws s3 continuation token` |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.bucket | string | `aws s3 bucket` | bucket-test-s3-app |
action_result.parameter.continuation_token | string | `aws s3 continuation token` | 1gpyNT6V4At5pjvBmQhRU2D2ehqyGrZJaHJ4VLYm5udxQTTi+8xMyUg== |
action_result.parameter.key | string | `aws s3 key` | test_folder/deeper_test_folder |
action_result.parameter.limit | numeric | | 3 |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.data.\*.\*.Contents.\*.ETag | string | | "d41d8cd98f00b204e9800998ecf8427e" |
action_result.data.\*.\*.Contents.\*.StorageClass | string | | STANDARD |
action_result.data.\*.\*.Contents.\*.Owner.DisplayName | string | | Display Name |
action_result.data.\*.\*.Contents.\*.LastModified | string | | 2017-12-13 23:22:47 |
action_result.data.\*.\*.Contents.\*.Size | numeric | | 0 |
action_result.data.\*.\*.Contents.\*.Owner.ID | string | `aws canonical id` `sha256` | 042b3oe6d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444 |
action_result.data.\*.\*.Contents.\*.Key | string | `aws s3 key` | test_folder/deeper_test_folder/ |
action_result.data.\*.\*.ContinuationToken | string | | |
action_result.data.\*.\*.EncodingType | string | | |
action_result.data.\*.\*.IsTruncated | boolean | | True False |
action_result.data.\*.\*.KeyCount | numeric | | 2 |
action_result.data.\*.\*.MaxKeys | numeric | | 3 |
action_result.data.\*.\*.Name | string | | bucket-test-s3-app |
action_result.data.\*.\*.NextContinuationToken | string | | |
action_result.data.\*.\*.Prefix | string | | |
action_result.data.\*.\*.ResponseMetadata.HTTPHeaders.content-type | string | | application/xml |
action_result.data.\*.\*.ResponseMetadata.HTTPHeaders.date | string | | Thu, 14 Dec 2017 00:39:10 GMT |
action_result.data.\*.\*.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.\*.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.\*.ResponseMetadata.HTTPHeaders.x-amz-bucket-region | string | | us-west-1 |
action_result.data.\*.\*.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | Ys1n2EOmKqMX4Z/3VxSzsW7ZQXFgj7/AkkMZLhiliLPKahOTbKTwMzsdthkBMBoSo+blbJvnY7Y= |
action_result.data.\*.\*.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 10B562C38DD0D76A |
action_result.data.\*.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.\*.ResponseMetadata.HostId | string | | Ys1n2EOmKqMX4Z/3VxSzsW7ZQXFgj7/AkkMZLhiliLPKahOTbKTwMzsdthkBMBoSo+blbJvnY7Y= |
action_result.data.\*.\*.ResponseMetadata.RequestId | string | | 10B562C38DD0D76A |
action_result.data.\*.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.\*.StartAfter | string | | test_folder/deeper_test_folder |
action_result.summary.num_objects | numeric | | 2 |
action_result.message | string | | Num objects: 2 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get object'

Get information about an object

Type: **investigate** <br>
Read only: **True**

If the <b>download_file</b> parameter is set to true, this action will download the specified file to the vault. The downloaded file will be given a name matching the given key.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** | required | Object bucket | string | `aws s3 bucket` |
**key** | required | Object Key | string | `aws s3 key` |
**download_file** | optional | Download File | boolean | |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.message | string | | File successfully added to vault |
action_result.parameter.bucket | string | `aws s3 bucket` | bucket-test-s3-app |
action_result.parameter.download_file | boolean | | True False |
action_result.parameter.key | string | `aws s3 key` | test_folder/image.jpg |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.data.\*.ACL.Grants.\*.Grantee.DisplayName | string | | Display Name |
action_result.data.\*.ACL.Grants.\*.Grantee.ID | string | `sha256` | 042b3oe6d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444 |
action_result.data.\*.ACL.Grants.\*.Grantee.Type | string | | CanonicalUser |
action_result.data.\*.ACL.Grants.\*.Permission | string | | FULL_CONTROL |
action_result.data.\*.ACL.Owner.DisplayName | string | | Display Name |
action_result.data.\*.ACL.Owner.ID | string | `aws canonical id` `sha256` | 042b3oe6d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444 |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.content-type | string | | application/xml |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.date | string | | Mon, 18 Dec 2017 21:04:10 GMT |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | ebJirNknxP6Y05DqTzHTBW6ph3Dlzw8XfO7l+d9vOxVcGd0UulOLUN8EwKEQml45TKWx04iLCSk= |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 726A959A95F1E3FF |
action_result.data.\*.ACL.ResponseMetadata.HTTPHeaders.x-amz-version-id | string | | |
action_result.data.\*.ACL.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ACL.ResponseMetadata.HostId | string | | ebJirNknxP6Y05DqTzHTBW6ph3Dlzw8XfO7l+d9vOxVcGd0UulOLUN8EwKEQml45TKWx04iLCSk= |
action_result.data.\*.ACL.ResponseMetadata.RequestId | string | | 726A959A95F1E3FF |
action_result.data.\*.ACL.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.File.AcceptRanges | string | | bytes |
action_result.data.\*.File.ContentLength | numeric | | 164461 |
action_result.data.\*.File.ContentType | string | | image/jpeg |
action_result.data.\*.File.ETag | string | | "081649aeacde0097aeac161be406168d" |
action_result.data.\*.File.LastModified | string | | 2017-12-13 23:23:36 |
action_result.data.\*.File.Metadata | string | | |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.accept-ranges | string | | bytes |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.content-length | string | | 164461 |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.content-type | string | | image/jpeg |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.date | string | | Mon, 18 Dec 2017 21:04:10 GMT |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.etag | string | | "081649aeacde0097aeac161be406168d" |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.last-modified | string | | Wed, 13 Dec 2017 23:23:36 GMT |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | 0c15dTU8vBsBNhlyoKPCGGhpHJtcquJD+vDG0wiTMYVVnX6ValrTB/01iTZVwm8VYrmPBcj276E= |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 8E5ADEED9D510876 |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.x-amz-server-side-encryption | string | | |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.x-amz-server-side-encryption-aws-kms-key-id | string | | |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.x-amz-tagging-count | string | | 2 |
action_result.data.\*.File.ResponseMetadata.HTTPHeaders.x-amz-version-id | string | | |
action_result.data.\*.File.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.File.ResponseMetadata.HostId | string | | 0c15dTU8vBsBNhlyoKPCGGhpHJtcquJD+vDG0wiTMYVVnX6ValrTB/01iTZVwm8VYrmPBcj276E= |
action_result.data.\*.File.ResponseMetadata.RequestId | string | | 8E5ADEED9D510876 |
action_result.data.\*.File.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.File.SSEKMSKeyId | string | | |
action_result.data.\*.File.ServerSideEncryption | string | | |
action_result.data.\*.File.TagCount | numeric | | 2 |
action_result.data.\*.File.VersionId | string | | |
action_result.data.\*.File.filename | string | | image.jpg |
action_result.data.\*.File.vault_id | string | `sha1` `vault id` | cde6248b8367f3a87bb6cc3dfc46fb9786200f88 |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.date | string | | Mon, 18 Dec 2017 21:04:10 GMT |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.transfer-encoding | string | | chunked |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | xHamNM+KJpg3EZSa6FujO8r0QfEoM0FJ4GY6Xh/l0QqkaqC18TPIzMFEJODUOOJIvKX6xO1TtRk= |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 49CB0256C60608F4 |
action_result.data.\*.Tagging.ResponseMetadata.HTTPHeaders.x-amz-version-id | string | | |
action_result.data.\*.Tagging.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.Tagging.ResponseMetadata.HostId | string | | xHamNM+KJpg3EZSa6FujO8r0QfEoM0FJ4GY6Xh/l0QqkaqC18TPIzMFEJODUOOJIvKX6xO1TtRk= |
action_result.data.\*.Tagging.ResponseMetadata.RequestId | string | | 49CB0256C60608F4 |
action_result.data.\*.Tagging.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.Tagging.TagSet.\*.Key | string | | Collorbone |
action_result.data.\*.Tagging.TagSet.\*.Value | string | | Intact |
action_result.data.\*.Tagging.VersionId | string | | |
action_result.summary.created_vault_id | string | `sha1` | cde6248b8367f3a87bb6cc3dfc46fb9786200f88 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'update object'

Update an object

Type: **generic** <br>
Read only: **False**

The <b>tags</b> parameter takes a JSON dictionary containing the tags that will be given to the specified <b>key</b> in the specified <b>bucket</b>. The dictionary should have the format:<br><br><pre>{<br> "tag1_key": "tag1_value",<br> "tag2_key": "tag2_value"<br> ...<br>}</pre><br>The <b>grants</b> parameter takes a dictionary where each key is a canonical user ID and each value is one of the following permissions:<ul><li>FULL_CONTROL</li><li>WRITE</li><li>WRITE_ACP</li><li>READ</li><li>READ_ACP</li></ul>An example JSON object would be:<br><br><pre>{<br> "111a11a11aa1111111aa11aaa1111a111a1aa111111a1a1a11aa11aa11a11aa1": "FULL_CONTROL",<br> "222b22b22bb2222222bb22bbb2222b222b2bb222222b2b2b22bb22bb22b22bb2": "READ"<br>}</pre><br>The <b>owner</b> parameter takes the canonical ID of an AWS user. This parameter must be provided if the <b>grants</b> parameter is included (even if there is no desire to change the owner; in this case, just provide the ID of the current owner of the object).<br><br>WARNING: Calling this action will replace the object's current tags and permissions with the tags and permission supplied to this action. To avoid overwriting the object's present data, first run <b>get object</b> to get the current tag and permission dictionaries, then add new tags and grants to those dictionaries before calling this action.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** | required | Name of the bucket | string | `aws s3 bucket` |
**key** | required | Path to upload file to | string | `aws s3 key` |
**grants** | optional | JSON dictionary of users and the permissions to grant them | string | |
**owner** | optional | Canonical ID of new owner | string | `aws canonical id` |
**tags** | optional | JSON dictionary containing tags to give object | string | |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.message | string | | Object successfully updated |
action_result.parameter.bucket | string | `aws s3 bucket` | bucket-test-s3-app |
action_result.parameter.grants | string | | {"153b1da9d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444": "FULL_CONTROL", "617d70b19fe7594450bf60dbd5004d026f7ae739872e5a3b80ca16ea15e94df8": "FULL_CONTROL"} |
action_result.parameter.key | string | `aws s3 key` | test_folder/deeper_test_folder/abc.jpg |
action_result.parameter.owner | string | `aws canonical id` | 042b3oe6d5faa5cfe9d016645ce14be41295ed6j94c988c6af6550f439e3f444 |
action_result.parameter.tags | string | | {"Adrian Gonzalez": "Braves Legend", "Chipper": "HoFer"} |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | numeric | | 72 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Mon, 18 Dec 2017 21:49:25 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | taFe2lslWgS35TL+WUaQpOG/qsCwJwcB6znO9Xu2/hZge0d4yHXuVbyDXMpwXl9806SfOC4jH2E= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 311807E3C0FBF393 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-version-id | string | | |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.HostId | string | | taFe2lslWgS35TL+WUaQpOG/qsCwJwcB6znO9Xu2/hZge0d4yHXuVbyDXMpwXl9806SfOC4jH2E= |
action_result.data.\*.ResponseMetadata.RequestId | string | | 311807E3C0FBF393 |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.VersionId | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'create object'

Create an object

Type: **generic** <br>
Read only: **False**

<p>For this action we need to provide the file extension in the 'key' field to make it work properly e.g.My_file.txt, My_image.png.</p>

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** | required | Bucket to upload file to | string | `aws s3 bucket` |
**key** | required | Key to upload file as | string | `aws s3 key` |
**vault_id** | required | Vault ID of file to upload | string | `vault id` |
**storage_class** | required | Storage class for object | string | |
**encryption** | required | Encryption to apply to object | string | |
**kms_key** | optional | KMS Key (Only if encryption is AWS:KMS) | string | |
**metadata** | optional | JSON dictionary containing metadata to give object | string | |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.bucket | string | `aws s3 bucket` | bucket-test-s3-app |
action_result.parameter.encryption | string | | AES256 |
action_result.parameter.key | string | `aws s3 key` | 123.png |
action_result.parameter.kms_key | string | | 234b9f7cd382ca2affe10176bf2c04aba6778e45 |
action_result.parameter.metadata | string | | {"Content-Language": "English"} |
action_result.parameter.storage_class | string | | STANDARD_IA |
action_result.parameter.vault_id | string | `vault id` | 306b9e7cd363cb2fdfc11176bc2f04ede7358f00 |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.data.\*.ETag | string | | "1dcdb3d256476fe8e2887c146960e580" |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | numeric | | 72 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Mon, 18 Dec 2017 23:05:11 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.etag | string | | "1dcdb3d256476fe8e2887c146960e580" |
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | Pny7k67Psa0yGvBsQGDEF7AOQXDl0N9AqocGVR08Cqw/Zku+tqrdK7SNkoVFEfJI9xpbsJUpH10= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | C03C87504C56273E |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-server-side-encryption | string | | AES256 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-server-side-encryption-aws-kms-key-id | string | | |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-storage-class | string | | STANDARD_IA |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-version-id | string | | |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.HostId | string | | Pny7k67Psa0yGvBsQGDEF7AOQXDl0N9AqocGVR08Cqw/Zku+tqrdK7SNkoVFEfJI9xpbsJUpH10= |
action_result.data.\*.ResponseMetadata.RequestId | string | | C03C87504C56273E |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.SSEKMSKeyId | string | | |
action_result.data.\*.ServerSideEncryption | string | | AES256 |
action_result.data.\*.VersionId | string | | |
action_result.summary | string | | |
action_result.message | string | | Object successfully updated |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'delete object'

Delete an object inside a bucket

Type: **generic** <br>
Read only: **False**

The object inside the bucket will be deleted. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** | required | Name of the bucket | string | `aws s3 bucket` |
**key** | required | File include path to be deleted | string | `aws s3 key` |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.bucket | string | `aws s3 bucket` | automated-bucket |
action_result.status | string | | success failed |
action_result.parameter.key | string | `aws s3 key` | test_folder/deeper_test_folder/abc.jpg |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2020-12-09 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | numeric | | 72 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Thu, 04 Jan 2018 01:14:36 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string | | AmazonS3 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-id-2 | string | | pi+Esw7Nc2VRmCeolShRpzN4kq2fjY4inqIXBTZ1ziI955Nvluh9K2oxN9z+dpmEotWh24K8Pc0= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-request-id | string | | 6F9DC34BE8E46AA5 |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.HostId | string | | pi+Esw7Nc2VRmCeolShRpzN4kq2fjY4inqIXBTZ1ziI955Nvluh9K2oxN9z+dpmEotWh24K8Pc0= |
action_result.data.\*.ResponseMetadata.RequestId | string | | 6F9DC34BE8E46AA5 |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary | string | | |
action_result.message | string | | Successfully deleted object |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 0 |

## action: 'generate presigned url'

Generate a Pre-Signed S3 URL

Type: **generic** <br>
Read only: **False**

Presigned URLs are a powerful feature in AWS S3 that allows users to grant temporary access to objects without sharing their AWS credentials. This can be particularly useful for sharing files securely or allowing uploads without exposing sensitive information.

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html#generating-a-presigned-url-to-upload-a-file

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**client_method** | required | Currently supported options are put_object | string | |
**bucket_name** | required | Name of the bucket | string | |
**object_name** | required | Name of the Object | string | |
**method_parameters** | optional | Dictionary of parameters to send to the method | string | |
**expiration** | optional | Time in seconds for the presigned URL to remain valid | numeric | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.client_method | string | | |
action_result.parameter.bucket_name | string | | |
action_result.parameter.object_name | string | | |
action_result.parameter.method_parameters | string | | |
action_result.parameter.expiration | numeric | | |
action_result.data.0.url | string | | |
action_result.status | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2026 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
