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

"""

Requires google-cloud SDK

See: https://googlecloudplatform.github.io/google-cloud-python/
"""

from libcloud3.types import Driver, ResourceType, Resource
import libcloud3.operations as operations

import googleapiclient.discovery


class GcpComputeInstanceType(ResourceType):
    supports = [operations.Get, operations.Stop]
    alias = 'ComputeInstance'
    attributes = ['id', 'name']

    def __init__(self, driver):
        self.driver = driver
        super().__init__()

    def get(self, zone, *args, **kwargs):
        result = compute.instances().list(
            project=self.driver.project_id,
            zone=zone, *args, **kwargs).execute()
        items = result['items']
        return [self.t(self.driver, i) for i in items]

    @staticmethod
    def stop(instance, *args):
        return "Stopping instance {0} has a name {1}".format(instance.id, instance.name)


class GcpDriver(Driver):
    requires=['googleapiclient']
    provides=[GcpComputeInstanceType]

    def __init__(self, project_id, auth_json=None, developer_key=None, *args):
        self.project_id = project_id
        self.compute = googleapiclient.discovery.build('compute', 'v1', developerKey=developer_key)
        super().__init__(self)
