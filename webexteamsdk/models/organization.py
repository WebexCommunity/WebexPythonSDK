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


class OrganizationBasicPropertiesMixin(object):
    """A mixin for :class:`SparkData` classes."""

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
