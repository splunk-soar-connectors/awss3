[comment]: # "Auto-generated SOAR connector documentation"
# AWS S3

Publisher: Splunk  
Connector Version: 2\.4\.15  
Product Vendor: AWS  
Product Name: S3  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

This app integrates with AWS S3 to perform investigative actions

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2018-2022 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
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


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a S3 asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access\_key** |  optional  | password | Access Key
**secret\_key** |  optional  | password | Secret Key
**region** |  required  | string | Default Region
**use\_role** |  optional  | boolean | Use attached role when running Phantom in EC2

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[list buckets](#action-list-buckets) - List all buckets configured on S3  
[get bucket](#action-get-bucket) - Get information about a bucket  
[create bucket](#action-create-bucket) - Create a bucket  
[update bucket](#action-update-bucket) - Update a bucket  
[delete bucket](#action-delete-bucket) - Delete a bucket  
[list objects](#action-list-objects) - List objects in a bucket  
[get object](#action-get-object) - Get information about an object  
[update object](#action-update-object) - Update an object  
[create object](#action-create-object) - Create an object  
[delete object](#action-delete-object) - Delete an object inside a bucket  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list buckets'
List all buckets configured on S3

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.status | string | 
action\_result\.data\.\*\.Buckets\.\*\.Name | string | 
action\_result\.data\.\*\.Buckets\.\*\.CreationDate | string | 
action\_result\.data\.\*\.Owner\.DisplayName | string | 
action\_result\.data\.\*\.Owner\.ID | string |  `aws canonical id`  `sha256` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.num\_buckets | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get bucket'
Get information about a bucket

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** |  required  | Bucket to get | string |  `aws s3 bucket` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.bucket | string |  `aws s3 bucket` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ACL\.Grants\.\*\.Grantee\.DisplayName | string | 
action\_result\.data\.\*\.ACL\.Grants\.\*\.Grantee\.ID | string | 
action\_result\.data\.\*\.ACL\.Grants\.\*\.Grantee\.Type | string | 
action\_result\.data\.\*\.ACL\.Grants\.\*\.Grantee\.URI | string | 
action\_result\.data\.\*\.ACL\.Grants\.\*\.Permission | string | 
action\_result\.data\.\*\.ACL\.Message | string | 
action\_result\.data\.\*\.ACL\.Owner\.DisplayName | string | 
action\_result\.data\.\*\.ACL\.Owner\.ID | string |  `sha256` 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.AccelerateConfiguration\.Message | string | 
action\_result\.data\.\*\.AccelerateConfiguration\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.AccelerateConfiguration\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.AccelerateConfiguration\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.AccelerateConfiguration\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.AccelerateConfiguration\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.AccelerateConfiguration\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.AccelerateConfiguration\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.AccelerateConfiguration\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.AccelerateConfiguration\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.AccelerateConfiguration\.Status | string | 
action\_result\.data\.\*\.CORS\.CORSRules\.\*\.AllowedHeaders | string | 
action\_result\.data\.\*\.CORS\.CORSRules\.\*\.AllowedMethods | string | 
action\_result\.data\.\*\.CORS\.CORSRules\.\*\.AllowedOrigins | string | 
action\_result\.data\.\*\.CORS\.CORSRules\.\*\.MaxAgeSeconds | numeric | 
action\_result\.data\.\*\.CORS\.Message | string | 
action\_result\.data\.\*\.CORS\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.CORS\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.CORS\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.CORS\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.CORS\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.CORS\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.CORS\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.CORS\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.CORS\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Encryption\.Message | string | 
action\_result\.data\.\*\.Encryption\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.Encryption\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.Encryption\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.Encryption\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.Encryption\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.Encryption\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.Encryption\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.Encryption\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.Encryption\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Encryption\.ServerSideEncryptionConfiguration\.Rules\.\*\.ApplyServerSideEncryptionByDefault\.KMSMasterKeyID | string | 
action\_result\.data\.\*\.Encryption\.ServerSideEncryptionConfiguration\.Rules\.\*\.ApplyServerSideEncryptionByDefault\.SSEAlgorithm | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.Message | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.LifecycleConfiguration\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.LifecycleConfiguration\.Rules\.\*\.Filter\.Prefix | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.Rules\.\*\.ID | string | 
action\_result\.data\.\*\.LifecycleConfiguration\.Rules\.\*\.NoncurrentVersionExpiration\.NoncurrentDays | numeric | 
action\_result\.data\.\*\.LifecycleConfiguration\.Rules\.\*\.Status | string | 
action\_result\.data\.\*\.Location\.LocationConstraint | string | 
action\_result\.summary\.encryption\_found | boolean | 
action\_result\.data\.\*\.Location\.Message | string | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.Location\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Logging\.LoggingEnabled\.TargetBucket | string | 
action\_result\.data\.\*\.Logging\.LoggingEnabled\.TargetPrefix | string | 
action\_result\.data\.\*\.Logging\.Message | string | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.Logging\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.NotificationConfiguration\.LambdaFunctionConfigurations\.\*\.Events | string | 
action\_result\.data\.\*\.NotificationConfiguration\.LambdaFunctionConfigurations\.\*\.Id | string | 
action\_result\.data\.\*\.NotificationConfiguration\.LambdaFunctionConfigurations\.\*\.LambdaFunctionArn | string | 
action\_result\.data\.\*\.NotificationConfiguration\.Message | string | 
action\_result\.data\.\*\.NotificationConfiguration\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.NotificationConfiguration\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.NotificationConfiguration\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.NotificationConfiguration\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.NotificationConfiguration\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.NotificationConfiguration\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.NotificationConfiguration\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.NotificationConfiguration\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.NotificationConfiguration\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Policy\.Message | string | 
action\_result\.data\.\*\.Policy\.Policy | string | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.Policy\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Replication\.Message | string | 
action\_result\.data\.\*\.Replication\.ReplicationConfiguration\.Role | string | 
action\_result\.data\.\*\.Replication\.ReplicationConfiguration\.Rules\.\*\.Destination\.Bucket | string | 
action\_result\.data\.\*\.Replication\.ReplicationConfiguration\.Rules\.\*\.ID | string | 
action\_result\.data\.\*\.Replication\.ReplicationConfiguration\.Rules\.\*\.Prefix | string | 
action\_result\.data\.\*\.Replication\.ReplicationConfiguration\.Rules\.\*\.Status | string | 
action\_result\.data\.\*\.Replication\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.Replication\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.Replication\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.Replication\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.Replication\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.Replication\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.Replication\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.Replication\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.Replication\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.RequestPayment\.Message | string | 
action\_result\.data\.\*\.RequestPayment\.Payer | string | 
action\_result\.data\.\*\.RequestPayment\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.RequestPayment\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.RequestPayment\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.RequestPayment\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.RequestPayment\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.RequestPayment\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.RequestPayment\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.RequestPayment\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.RequestPayment\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Tagging\.Message | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Tagging\.TagSet\.\*\.Key | string | 
action\_result\.data\.\*\.Tagging\.TagSet\.\*\.Value | string | 
action\_result\.data\.\*\.Versioning\.Message | string | 
action\_result\.data\.\*\.Versioning\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.Versioning\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.Versioning\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.Versioning\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.Versioning\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.Versioning\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.Versioning\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.Versioning\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.Versioning\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.replication\_found | boolean | 
action\_result\.summary\.notification\_configuration\_found | boolean | 
action\_result\.data\.\*\.Versioning\.Status | string | 
action\_result\.data\.\*\.Website\.ErrorDocument\.Key | string | 
action\_result\.data\.\*\.Website\.IndexDocument\.Suffix | string | 
action\_result\.data\.\*\.Website\.Message | string | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.Website\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.accelerate\_configuration\_found | boolean | 
action\_result\.summary\.acl\_found | boolean | 
action\_result\.summary\.cors\_found | boolean | 
action\_result\.summary\.logging\_found | boolean | 
action\_result\.summary\.lifecycle\_configuration\_found | boolean | 
action\_result\.summary\.location\_found | boolean | 
action\_result\.summary\.policy\_found | boolean | 
action\_result\.summary\.request\_payment\_found | boolean | 
action\_result\.summary\.tagging\_found | boolean | 
action\_result\.summary\.versioning\_found | boolean | 
action\_result\.summary\.website\_found | boolean | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create bucket'
Create a bucket

Type: **generic**  
Read only: **False**

The bucket will be created in the region specified in the asset configuration\. The bucket name provided has to be unique and it should not be already used in the AWS S3 globally\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** |  required  | Name of bucket to create | string |  `aws s3 bucket` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.bucket | string |  `aws s3 bucket` 
action\_result\.status | string | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.Location | string |  `url` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.location | string |  `url` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'update bucket'
Update a bucket

Type: **generic**  
Read only: **False**

The <b>tags</b> parameter takes a JSON dictionary containing the tags that will be given to the specified <b>bucket</b>\. The dictionary should have the format\:<br><br><pre>\{<br>    &quot;tag1\_key&quot;\: &quot;tag1\_value&quot;,<br>    &quot;tag2\_key&quot;\: &quot;tag2\_value&quot;<br>    \.\.\.<br>\}</pre><br>The <b>grants</b> parameter takes a dictionary where each key is a canonical user ID and each value is one of the following permissions\:<ul><li>FULL\_CONTROL</li><li>WRITE</li><li>WRITE\_ACP</li><li>READ</li><li>READ\_ACP</li></ul>An example JSON object would be\:<br><br><pre>\{<br>    &quot;111a11a11aa1111111aa11aaa1111a111a1aa111111a1a1a11aa11aa11a11aa1&quot;\: &quot;FULL\_CONTROL&quot;,<br>    &quot;222b22b22bb2222222bb22bbb2222b222b2bb222222b2b2b22bb22bb22b22bb2&quot;\: &quot;READ&quot;<br>\}</pre><br>The <b>owner</b> parameter takes the canonical ID of an AWS user\. This parameter must be provided if the <b>grants</b> parameter is included \(even if there is no desire to change the owner; in this case, just provide the ID of the current owner of the bucket\)\.<br><br>WARNING\: Calling this action will replace the bucket's current tags and permissions with the tags and permission supplied to this action\. To avoid overwriting the bucket's present data, first run <b>get bucket</b> to get the current tag and permission dictionaries, then add new tags and grants to those dictionaries before calling this action\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** |  required  | Name of bucket to update | string |  `aws s3 bucket` 
**tags** |  optional  | JSON dictionary containing tags to give object | string | 
**encryption** |  optional  | Encryption to apply to bucket | string | 
**kms\_key** |  optional  | KMS Key \(Only if encryption is AWS\:KMS\) | string | 
**grants** |  optional  | JSON dictionary of users and the permissions to grant them | string | 
**owner** |  optional  | Canonical ID of new owner | string |  `aws canonical id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.bucket | string |  `aws s3 bucket` 
action\_result\.status | string | 
action\_result\.parameter\.encryption | string | 
action\_result\.parameter\.grants | string | 
action\_result\.parameter\.kms\_key | string | 
action\_result\.message | string | 
action\_result\.parameter\.owner | string |  `aws canonical id` 
action\_result\.parameter\.tags | string | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'delete bucket'
Delete a bucket

Type: **generic**  
Read only: **False**

The bucket will be deleted\. All objects \(including all object versions and delete markers\) in the bucket must be deleted before the bucket itself can be deleted\. If the bucket is owned by a different account, the request will fail with an HTTP 403 \(Access Denied\) error\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** |  required  | Name of bucket to delete | string |  `aws s3 bucket` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.bucket | string |  `aws s3 bucket` 
action\_result\.status | string | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list objects'
List objects in a bucket

Type: **investigate**  
Read only: **True**

This action will list all objects in the given <b>bucket</b>\. It will recursively list all objects in each folder in the bucket as well\.<br><br>If given the <b>key</b> parameter, the action will start listing objects at the given key \(which could include objects at the same level as the specified key\)\. The <b>key</b> must be a full path from the root of the <b>bucket</b>\.<br><br>The <b>limit</b> parameter has a maximum value of 1000\. If no <b>limit</b> is provided, it will default to 1000\. If more objects than the specified <b>limit</b> exist, the action will return a <b>NextContinuationToken</b>\. To get the next batch of objects, pass this token in a new action as the <b>continuation\_token</b>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** |  required  | List objects in this bucket | string |  `aws s3 bucket` 
**key** |  optional  | List objects under this key | string |  `aws s3 key` 
**limit** |  optional  | Max number of objects to list | numeric | 
**continuation\_token** |  optional  | Use this parameter to get the next set of objects from a previous action | string |  `aws s3 continuation token` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.bucket | string |  `aws s3 bucket` 
action\_result\.parameter\.continuation\_token | string |  `aws s3 continuation token` 
action\_result\.parameter\.key | string |  `aws s3 key` 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.\*\.Contents\.\*\.ETag | string | 
action\_result\.data\.\*\.\*\.Contents\.\*\.StorageClass | string | 
action\_result\.data\.\*\.\*\.Contents\.\*\.Owner\.DisplayName | string | 
action\_result\.data\.\*\.\*\.Contents\.\*\.LastModified | string | 
action\_result\.data\.\*\.\*\.Contents\.\*\.Size | numeric | 
action\_result\.data\.\*\.\*\.Contents\.\*\.Owner\.ID | string |  `aws canonical id`  `sha256` 
action\_result\.data\.\*\.\*\.Contents\.\*\.Key | string |  `aws s3 key` 
action\_result\.data\.\*\.\*\.ContinuationToken | string | 
action\_result\.data\.\*\.\*\.EncodingType | string | 
action\_result\.data\.\*\.\*\.IsTruncated | boolean | 
action\_result\.data\.\*\.\*\.KeyCount | numeric | 
action\_result\.data\.\*\.\*\.MaxKeys | numeric | 
action\_result\.data\.\*\.\*\.Name | string | 
action\_result\.data\.\*\.\*\.NextContinuationToken | string | 
action\_result\.data\.\*\.\*\.Prefix | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-bucket\-region | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.\*\.StartAfter | string | 
action\_result\.summary\.num\_objects | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get object'
Get information about an object

Type: **investigate**  
Read only: **True**

If the <b>download\_file</b> parameter is set to true, this action will download the specified file to the vault\. The downloaded file will be given a name matching the given key\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** |  required  | Object bucket | string |  `aws s3 bucket` 
**key** |  required  | Object Key | string |  `aws s3 key` 
**download\_file** |  optional  | Download File | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.parameter\.bucket | string |  `aws s3 bucket` 
action\_result\.parameter\.download\_file | boolean | 
action\_result\.parameter\.key | string |  `aws s3 key` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ACL\.Grants\.\*\.Grantee\.DisplayName | string | 
action\_result\.data\.\*\.ACL\.Grants\.\*\.Grantee\.ID | string |  `sha256` 
action\_result\.data\.\*\.ACL\.Grants\.\*\.Grantee\.Type | string | 
action\_result\.data\.\*\.ACL\.Grants\.\*\.Permission | string | 
action\_result\.data\.\*\.ACL\.Owner\.DisplayName | string | 
action\_result\.data\.\*\.ACL\.Owner\.ID | string |  `aws canonical id`  `sha256` 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPHeaders\.x\-amz\-version\-id | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ACL\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.File\.AcceptRanges | string | 
action\_result\.data\.\*\.File\.ContentLength | numeric | 
action\_result\.data\.\*\.File\.ContentType | string | 
action\_result\.data\.\*\.File\.ETag | string | 
action\_result\.data\.\*\.File\.LastModified | string | 
action\_result\.data\.\*\.File\.Metadata | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.accept\-ranges | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.etag | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.last\-modified | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.x\-amz\-server\-side\-encryption | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.x\-amz\-server\-side\-encryption\-aws\-kms\-key\-id | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.x\-amz\-tagging\-count | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPHeaders\.x\-amz\-version\-id | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.File\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.File\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.File\.SSEKMSKeyId | string | 
action\_result\.data\.\*\.File\.ServerSideEncryption | string | 
action\_result\.data\.\*\.File\.TagCount | numeric | 
action\_result\.data\.\*\.File\.VersionId | string | 
action\_result\.data\.\*\.File\.filename | string | 
action\_result\.data\.\*\.File\.vault\_id | string |  `sha1`  `vault id` 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.transfer\-encoding | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPHeaders\.x\-amz\-version\-id | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.Tagging\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Tagging\.TagSet\.\*\.Key | string | 
action\_result\.data\.\*\.Tagging\.TagSet\.\*\.Value | string | 
action\_result\.data\.\*\.Tagging\.VersionId | string | 
action\_result\.summary\.created\_vault\_id | string |  `sha1` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'update object'
Update an object

Type: **generic**  
Read only: **False**

The <b>tags</b> parameter takes a JSON dictionary containing the tags that will be given to the specified <b>key</b> in the specified <b>bucket</b>\. The dictionary should have the format\:<br><br><pre>\{<br>    &quot;tag1\_key&quot;\: &quot;tag1\_value&quot;,<br>    &quot;tag2\_key&quot;\: &quot;tag2\_value&quot;<br>    \.\.\.<br>\}</pre><br>The <b>grants</b> parameter takes a dictionary where each key is a canonical user ID and each value is one of the following permissions\:<ul><li>FULL\_CONTROL</li><li>WRITE</li><li>WRITE\_ACP</li><li>READ</li><li>READ\_ACP</li></ul>An example JSON object would be\:<br><br><pre>\{<br>    &quot;111a11a11aa1111111aa11aaa1111a111a1aa111111a1a1a11aa11aa11a11aa1&quot;\: &quot;FULL\_CONTROL&quot;,<br>    &quot;222b22b22bb2222222bb22bbb2222b222b2bb222222b2b2b22bb22bb22b22bb2&quot;\: &quot;READ&quot;<br>\}</pre><br>The <b>owner</b> parameter takes the canonical ID of an AWS user\. This parameter must be provided if the <b>grants</b> parameter is included \(even if there is no desire to change the owner; in this case, just provide the ID of the current owner of the object\)\.<br><br>WARNING\: Calling this action will replace the object's current tags and permissions with the tags and permission supplied to this action\. To avoid overwriting the object's present data, first run <b>get object</b> to get the current tag and permission dictionaries, then add new tags and grants to those dictionaries before calling this action\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** |  required  | Name of the bucket | string |  `aws s3 bucket` 
**key** |  required  | Path to upload file to | string |  `aws s3 key` 
**grants** |  optional  | JSON dictionary of users and the permissions to grant them | string | 
**owner** |  optional  | Canonical ID of new owner | string |  `aws canonical id` 
**tags** |  optional  | JSON dictionary containing tags to give object | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.parameter\.bucket | string |  `aws s3 bucket` 
action\_result\.parameter\.grants | string | 
action\_result\.parameter\.key | string |  `aws s3 key` 
action\_result\.parameter\.owner | string |  `aws canonical id` 
action\_result\.parameter\.tags | string | 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-version\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.VersionId | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create object'
Create an object

Type: **generic**  
Read only: **False**

<p>For this action we need to provide the file extension in the 'key' field to make it work properly e\.g\.My\_file\.txt, My\_image\.png\.</p>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** |  required  | Bucket to upload file to | string |  `aws s3 bucket` 
**key** |  required  | Key to upload file as | string |  `aws s3 key` 
**vault\_id** |  required  | Vault ID of file to upload | string |  `vault id` 
**storage\_class** |  required  | Storage class for object | string | 
**encryption** |  required  | Encryption to apply to object | string | 
**kms\_key** |  optional  | KMS Key \(Only if encryption is AWS\:KMS\) | string | 
**metadata** |  optional  | JSON dictionary containing metadata to give object | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.bucket | string |  `aws s3 bucket` 
action\_result\.parameter\.encryption | string | 
action\_result\.parameter\.key | string |  `aws s3 key` 
action\_result\.parameter\.kms\_key | string | 
action\_result\.parameter\.metadata | string | 
action\_result\.parameter\.storage\_class | string | 
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ETag | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.etag | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-server\-side\-encryption | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-server\-side\-encryption\-aws\-kms\-key\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-storage\-class | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-version\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.SSEKMSKeyId | string | 
action\_result\.data\.\*\.ServerSideEncryption | string | 
action\_result\.data\.\*\.VersionId | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'delete object'
Delete an object inside a bucket

Type: **generic**  
Read only: **False**

The object inside the bucket will be deleted\. If the bucket is owned by a different account, the request will fail with an HTTP 403 \(Access Denied\) error\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**bucket** |  required  | Name of the bucket | string |  `aws s3 bucket` 
**key** |  required  | File include path to be deleted | string |  `aws s3 key` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.bucket | string |  `aws s3 bucket` 
action\_result\.status | string | 
action\_result\.parameter\.key | string |  `aws s3 key` 
action\_result\.parameter\.credentials | string |  `aws credentials` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-id\-2 | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-request\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HostId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 