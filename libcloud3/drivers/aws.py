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
import boto3


class EC2Instance():

    def __init__(self, driver, instance_id):
        self.driver = driver
        self.instance_id = instance_id

    def __str__(self):
        return "EC2Instance<" + self.instance_id + ">"

    def __repr__(self):
        return self.__str__()


class EC2InstanceType(ResourceType):
    """Represents an AWS EC2 Instance"""

    supports = [operations.Get, operations.Describe]
    alias = 'instances'

    def __init__(self, driver):
        self.driver = driver
        self.ec2 = boto3.client('ec2', region, aws_access_key_id=self.driver.access_key, aws_secret_access_key=self.driver.access_secret)

    def get(self, region):
        return [EC2Instance(self.driver, instance['InstanceId']) for instance in self.ec2.describe_instances()['Reservations'][0]['Instances']]


class AWSDriver(Driver):
    """Enables operations with AWS accounts"""

    requires=['boto3']
    provides=[EC2InstanceType]

    def __init__(self, access_key, access_secret):
        self.access_key = access_key
        self.access_secret = access_secret

    @property
    def instances(self):
        return EC2InstanceType(self)
