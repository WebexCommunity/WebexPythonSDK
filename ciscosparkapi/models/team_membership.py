# -*- coding: utf-8 -*-
"""Cisco Spark Team-Membership data model."""


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


class TeamMembership(SparkData):
    """Model a Spark 'team membership' JSON object as a native Python object.
    """

    def __init__(self, json):
        """Initialize a TeamMembership object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(TeamMembership, self).__init__(json)

    @property
    def id(self):
        """The team membership's unique ID."""
        return self._json_data.get('id')

    @property
    def teamId(self):
        """The ID of the team."""
        return self._json_data.get('teamId')

    @property
    def personId(self):
        """The ID of the person."""
        return self._json_data.get('personId')

    @property
    def personEmail(self):
        """The email address of the person."""
        return self._json_data.get('personEmail')

    @property
    def personDisplayName(self):
        """The display name of the person."""
        return self._json_data.get('personDisplayName')

    @property
    def personOrgId(self):
        """The ID of the organization that the person is associated with."""
        return self._json_data.get('personOrgId')

    @property
    def isModerator(self):
        """Person is a moderator for the team."""
        return self._json_data.get('isModerator')

    @property
    def created(self):
        """The date and time the team membership was created."""
        return self._json_data.get('created')
