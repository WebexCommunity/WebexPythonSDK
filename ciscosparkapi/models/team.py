# -*- coding: utf-8 -*-
"""Cisco Spark Team data model."""


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


class Team(SparkData):
    """Model a Spark 'team' JSON object as a native Python object."""

    def __init__(self, json):
        """Initialize a new Team data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Team, self).__init__(json)

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
