# -*- coding: utf-8 -*-
"""Cisco Spark Organization data model."""


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


class Organization(SparkData):
    """Model a Spark Organization JSON object as a native Python object."""

    def __init__(self, json):
        """Init a Organization data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Organization, self).__init__(json)

    @property
    def id(self):
        """The unique ID for the Organization."""
        return self._json_data.get('id')

    @property
    def displayName(self):
        """The human-friendly display name of the Organization."""
        return self._json_data.get('displayName')

    @property
    def created(self):
        """Creation date and time in ISO8601 format."""
        return self._json_data.get('created')
