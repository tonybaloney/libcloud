# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio

from libcloud3.types import Driver, ResourceType
import libcloud3.operations as operations

try:
    import aioboto3
    _IMPORT_WARNING = False
except ImportError:
    _IMPORT_WARNING = True


class EC2InstanceType(ResourceType):
    """Represents an AWS EC2 Instance"""

    supports = [operations.Get, operations.Describe, operations.GetState]
    supports_async = True
    alias = 'EC2Instance'
    attributes = ['id']

    def __init__(self, driver):
        super().__init__(driver)

    def get(self, region):
        return asyncio.get_event_loop().run_until_complete(self.async_get(region))

    async def async_get(self, region):
        async with aioboto3.client('ec2', region, aws_access_key_id=self.driver.access_key, aws_secret_access_key=self.driver.access_secret) as ec2:
            instances = await ec2.describe_instances()
            if len(instances['Reservations']) > 0:
                return [self.map(self.driver, instance, id=instance['InstanceId'], region=region) for instance in instances['Reservations'][0]['Instances']]
            else:
                return []

    @staticmethod
    def status(self):
        return asyncio.get_event_loop().run_until_complete(self.async_status())

    @staticmethod
    async def async_status(instance):
        async with aioboto3.client('ec2', instance.region, aws_access_key_id=instance.driver.access_key, aws_secret_access_key=instance.driver.access_secret) as ec2:
            resp = await ec2.describe_instance_status(InstanceIds=[instance.InstanceId])
            return None if len(resp['InstanceStatuses']) == 0 else resp['InstanceStatuses'][0]

    @staticmethod
    def describe(self):
        return asyncio.get_event_loop().run_until_complete(self.async_describe())

    @staticmethod
    async def async_describe(instance):
        async with aioboto3.client('ec2', instance.region, aws_access_key_id=instance.driver.access_key, aws_secret_access_key=instance.driver.access_secret) as ec2:
            resp = await ec2.describe_instances(InstanceIds=[instance.InstanceId])
            return None if len(resp['Reservations']) == 0 else resp['Reservations'][0]['Instances'][0]


class S3BucketType(ResourceType):
    """Represents an AWS S3 Bucket"""

    supports = [operations.Get]
    supports_async = True
    alias = 'S3Bucket'
    attributes = ['id']

    def __init__(self, driver):
        super().__init__(driver)

    def get(self):
        return asyncio.get_event_loop().run_until_complete(self.async_get())

    async def async_get(self):
        async with aioboto3.client('s3', aws_access_key_id=self.driver.access_key, aws_secret_access_key=self.driver.access_secret) as s3:
            buckets = await s3.list_buckets()
            if len(buckets['Buckets']) > 0:
                return [self.map(self.driver, bucket, id=bucket['Name']) for bucket in buckets['Buckets']]
            else:
                return []


class S3ObjectType(ResourceType):
    """Represents an AWS S3 Object"""

    supports = [operations.Get]
    supports_async = True
    alias = 'S3Object'
    attributes = ['id']

    def __init__(self, driver):
        super().__init__(driver)

    def get(self, bucket):
        return asyncio.get_event_loop().run_until_complete(self.async_get(bucket))

    async def async_get(self, bucket):
        async with aioboto3.client('s3', aws_access_key_id=self.driver.access_key, aws_secret_access_key=self.driver.access_secret) as s3:
            objs = await s3.list_objects_v2(Bucket=bucket)
            if len(objs['Contents']) > 0:
                return [self.map(self.driver, obj, id=obj['Key']) for obj in objs['Contents']]
            else:
                return []


class AWSDriver(Driver):
    """
    Enables operations with AWS accounts
    """

    requires=['aioboto3']
    provides=[EC2InstanceType, S3BucketType, S3ObjectType]

    def __init__(self, access_key, access_secret):
        super().__init__()
        self.access_key = access_key
        self.access_secret = access_secret
