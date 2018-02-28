# -*- coding: utf-8 -*-
"""Cisco Spark Team data model."""


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


class TeamBasicPropertiesMixin(object):
    """A mixin for :class:`SparkData` classes."""

    @property
    def id(self):
        """The team's unique ID."""
        return self._json_data.get('id')

    @property
    def name(self):
        """A user-friendly name for the team."""
        return self._json_data.get('name')

    @property
    def created(self):
        """The date and time the team was created."""
        return self._json_data.get('created')

    @property
    def creatorId(self):
        """The ID of the person who created the team."""
        return self._json_data.get('creatorId')
