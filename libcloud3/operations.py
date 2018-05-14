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

Operation = namedtuple('Operation', ['name', 'description'])

Provision = Operation('provision', 'Provision a resource')
Deprovision = Operation('deprovision', 'Provision a resource')

# For resources where the operation is
Start = Operation('start', 'Start the operation of a resource')
Stop = Operation('stop', 'Stop the operation of a resource')
Pause = Operation('pause', 'Pause the operation a resource')
GetState = Operation('getstate', 'Get the state of operation of a resource')

# Low-level operations resources
Create = Operation('create', 'Create a new resource')
Delete = Operation('delete', 'Delete an existing resource')
Describe = Operation('describe', 'Get detailed information on a resource')
Get = Operation('get', 'Retrieves a list of resources of this type')

BASE = {Provision, Deprovision, Start, Stop, Pause, GetState, Create, Delete, Read}
