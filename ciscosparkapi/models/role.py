# -*- coding: utf-8 -*-
"""Cisco Spark Role data model."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


class RoleBasicPropertiesMixin(object):
    """A mixin for :class:`SparkData` classes."""

    @property
    def id(self):
        """The unique ID for the Role."""
        return self._json_data.get('id')

    @property
    def name(self):
        """The name of the Role."""
        return self._json_data.get('name')
