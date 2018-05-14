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

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient


class AzureComputeInstanceType(ResourceType):
    supports = [operations.Get]
    alias = 'ComputeInstance'

    def get(self, driver, *args):
        groups = self.driver.resource_mgmt.list_all()
        return [self.t(self.driver, g) for g in groups]


class AzureResourceGroupType(ResourceType):
    supports = [operations.Get]
    alias = 'ResourceGroup'

    attributes = ['id', 'name']

    @classmethod
    def get(cls, driver, *args):
        # do read command.. do the meta generation here
        return driver.resource_mgmt.list_all()


class AzureDriver(Driver):
    requires=['azure']
    provides=[AzureResourceGroupType]

    def __init__(self, subscription_id, client_id, secret, tenant, *args):
        self.subscription_id = subscription_id
        self.credentials = ServicePrincipalCredentials(
            client_id=client_id,
            secret=secret,
            tenant=tenant
        )
        self.resource_mgmt = ResourceManagementClient(credentials, subscription_id)
