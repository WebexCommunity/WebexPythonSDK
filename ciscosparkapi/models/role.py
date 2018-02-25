# -*- coding: utf-8 -*-
"""Cisco Spark Role data model."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from .sparkdata import SparkData


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


class Role(SparkData):
    """Model a Spark Role JSON object as a native Python object."""

    def __init__(self, json):
        """Initialize a new Role data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Role, self).__init__(json)

    @property
    def id(self):
        """The unique ID for the Role."""
        return self._json_data.get('id')

    @property
    def name(self):
        """The name of the Role."""
        return self._json_data.get('name')
