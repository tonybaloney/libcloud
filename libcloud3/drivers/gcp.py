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
Requires googleapiclient for Python
"""

from libcloud3.types import Driver, ResourceType, Resource
import libcloud3.operations as operations

import googleapiclient.discovery


class GcpComputeInstanceType(ResourceType):
    supports = [operations.Get, operations.Stop]
    alias = 'ComputeInstance'
    attributes = ['id', 'name']

    def get(self, zone, *args, **kwargs):
        result = self.driver.compute.instances().list(
            project=self.driver.project_id,
            zone=zone, *args, **kwargs).execute()
        items = result['items']
        return [self.t(self.driver, i) for i in items]

    @staticmethod
    def stop(instance, *args):
        return "Stopping instance {0} has a name {1}".format(instance.id, instance.name)


class GcpStorageBucketType(ResourceType):
    supports = [operations.Get]
    alias = 'StorageBucket'
    attributes = ['id', 'name']

    def get(self, *args, **kwargs):
        result = self.driver.storage.buckets().list(
            project=self.driver.project_id,
            *args, **kwargs).execute()
        items = result['items']
        return [self.t(self.driver, i) for i in items]


class GcpKubernetesClusterType(ResourceType):
    supports = [operations.Get]
    alias = 'KubernetesCluster'
    attributes = ['id', 'name']

    def get(self, zone, *args, **kwargs):
        parent = "projects/{0}/locations/{1}".format(self.driver.project_id, zone)
        result = self.driver.container.projects().locations().clusters().list(
            parent=parent, *args, **kwargs).execute()

        items = result['clusters']
        return [self.t(self.driver, i) for i in items]


class GcpDriver(Driver):
    requires=['googleapiclient']
    provides=[GcpComputeInstanceType, GcpKubernetesClusterType, GcpStorageBucketType]

    def __init__(self, project_id, auth_json=None, developer_key=None, *args):
        self.project_id = project_id
        self.compute = googleapiclient.discovery.build('compute', 'v1', developerKey=developer_key)
        self.storage = googleapiclient.discovery.build('storage', 'v1', developerKey=developer_key)
        self.container = googleapiclient.discovery.build('container', 'v1', developerKey=developer_key)
        super().__init__()
