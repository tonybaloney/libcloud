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


from libcloud3.types import Driver, ResourceType
import libcloud3.operations as operations
import asyncio
import aioboto3


class EC2InstanceType(ResourceType):
    """Represents an AWS EC2 Instance"""

    supports = [operations.Get, operations.Describe, operations.GetState]
    alias = 'EC2Instances'
    attributes = ['id']

    def __init__(self, driver):
        self.driver = driver
        super().__init__()

    def get(self, region):
        return asyncio.get_event_loop().run_until_complete(self.async_get(region))

    async def async_get(self, region):
        async with aioboto3.client('ec2', region, aws_access_key_id=self.driver.access_key, aws_secret_access_key=self.driver.access_secret) as ec2:
            instances = await ec2.describe_instances()
            if len(instances['Reservations']) > 0:
                return [self.t(self.driver, instance, id=instance['InstanceId'], region=region) for instance in instances['Reservations'][0]['Instances']]
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


class AWSDriver(Driver):
    """Enables operations with AWS accounts"""

    requires=['boto3']
    provides=[EC2InstanceType]

    def __init__(self, access_key, access_secret):
        super().__init__()
        self.access_key = access_key
        self.access_secret = access_secret
