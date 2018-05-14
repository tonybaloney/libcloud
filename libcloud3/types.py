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

import types

from libcloud3.operations import Operation
from libcloud3.exceptions import MissingDependencyException


def make_type(cls):
    def operation_method(targetcls, name):
        return getattr(targetcls, name)

    def body(ns):
        def __init__(self, driver, data, *args, **kwargs):
            self.driver = driver
            for k, v in data.items():
                setattr(self, k, v)

        def __str__(self):
            return '{0} id={1}'.format(cls.alias, self.id)

        def __repr__(self):
            return '<{0} id={1}>'.format(type(self).__name__, self.id)

        d = {
            '__doc__': 'An instance of {0}'.format(cls.alias),
            '__init__': __init__,
            '__str__': __str__,
            '__repr__': __repr__
        }

        for supported_operation in cls.supports:
            d[supported_operation.name] = operation_method(cls, supported_operation.name)

        for attribute in cls.attributes:
            d[attribute] = None

        ns.update(d)
    return types.new_class(cls.alias, bases=(Resource,), exec_body=body)


class MissingDependencyCollection(object):
    def __init__(self, missing):
        self.missing = missing

    def __bool__(self):
        return false

    def __iter__(self):
        return self.missing.__iter__


class Driver(object):
    """
    Wrapper for the fetching and provisioning of resources from a cloud
    """

    """
    Describes what resource types are provided by this driver

    Class attribute of :class:`ResourceType`
    """
    provides = []

    """
    Describes what package dependencies are required for this driver
    e.g boto3

    ``list`` of ``str``
    """
    requires = []
    
    def do_operation(self, operation, resource_type, instance, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def supported(cls):
        """
        Checks all packages required are installed.

        :returns: ``True`` if supported, instance of :class:`MissingDependencyCollection`
        """
        errors = []
        for dependency in cls.provides:
            try:
                _temp = __import__(dependency)
            except ImportError as ie:
                errors.append(dependency)
        if not errors:
            return True
        else:
            return MissingDependencyCollection(errors)

    def __getattr__(self, name):
        """
        Returns a redirect to the type accessor
        """
        for provided_type in self.provides:
            if name == provided_type.alias:
                return provided_type


class ResourceType(object):
    """
    Meta type for resources provided by a Driver
    """

    """
    List of supported operations

    :type: ``list`` of :class:`Operation`
    """
    supports = []

    """
    A short-hand alias for this type

    :type: ``str``
    """
    alias = None

    def __init__(self):
        self.t = make_type(self)

class Resource(object):
    """
    Base instance type for a resource from a driver
    """
    pass
