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

from libcloud3.types import Driver, ResourceType, Resource
import libcloud3.operations as operations


class DemoComputeInstanceType(ResourceType):
    supports = [operations.Get, operations.Stop]
    alias = 'ComputeInstance'
    attributes = ['id', 'name']

    def __init__(self, driver):
        self.driver = driver
        super().__init__()

    def get(self, *args):
        # do read command..
        result = [{"id": 1, "name": "test"}]
        return [self.t(self.driver, i) for i in result]

    @staticmethod
    def stop(instance, *args):
        print(instance.id)
        return "Hello world!!"


class DemoDriver(Driver):
    requires=[]
    provides=[DemoComputeInstanceType]

    def __init__(self, subscription_id, *args):
        self.subscription_id = subscription_id
        self.connection = "immutable thing"
        
        for t in self.provides:
            setattr(self, t.alias, t(self))

    def do_operation(self, operation, resource_type, instance, *args, **kwargs):
        print("Doing operation!")
