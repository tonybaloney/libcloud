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
 - Operations that can be performed on a resource.
 - Operations are a namedtuple of (Name)
 - Operations are extendable by each provider

"""

from collections import namedtuple

Operation = namedtuple('Operation', ['name', 'description', 'applies_to_collection', 'applies_to_instance'])

Provision = Operation('provision', 'Provision a resource', True, False)
Deprovision = Operation('deprovision', 'Provision a resource', True, True)

# For resources where the operation is
Start = Operation('start', 'Start the operation of a resource', False, True)
Stop = Operation('stop', 'Stop the operation of a resource', False, True)
Pause = Operation('pause', 'Pause the operation a resource', False, True)
GetState = Operation('getstate', 'Get the state of operation of a resource', False, True)

# Low-level operations resources
Create = Operation('create', 'Create a new resource', True, False)
Delete = Operation('delete', 'Delete an existing resource', True, True)
Describe = Operation('describe', 'Get detailed information on a resource', False, True)
Get = Operation('get', 'Retrieves a list of resources of this type', True, False)

BASE = {Provision, Deprovision, Start, Stop, Pause, GetState, Create, Delete, Describe, Get}
