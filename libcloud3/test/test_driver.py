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

import pytest

from libcloud3.types import Driver, ResourceType
import libcloud3.operations as operations


class ExampleResourceType(ResourceType):
    supports = [operations.Read, operations.Create]
    alias = 'example'


class DummyDriver(Driver):
    provides = [ExampleResourceType]
    requires = []


@pytest.fixture
def driver():
    return DummyDriver()


def test_unsupported_driver():
    """
    Test that a driver which depends on a package you don't have installed
    shows unsupported
    """

    class BadDriver(Driver):
        provides = []
        requires = ['yabbadabbadoo']

    supported = BadDriver.supported()
    assert supported is not True


def test_provides(driver):
    assert isinstance(driver.provides, list)

    for provides in driver.provides:
        assert issubclass(provides, ResourceType)
