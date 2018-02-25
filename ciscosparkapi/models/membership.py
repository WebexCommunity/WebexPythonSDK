# -*- coding: utf-8 -*-
"""Cisco Spark Membership data model."""


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


class Membership(SparkData):
    """Model a Spark 'membership' JSON object as a native Python object."""

    def __init__(self, json):
        """Initialize a Membership object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Membership, self).__init__(json)

    @property
    def id(self):
        """The membership's unique ID."""
        return self._json_data.get('id')

    @property
    def roomId(self):
        """The ID of the room."""
        return self._json_data.get('roomId')

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
        """Person is a moderator for the room."""
        return self._json_data.get('isModerator')

    @property
    def isMonitor(self):
        """Person is a monitor for the room."""
        return self._json_data.get('isMonitor')

    @property
    def created(self):
        """The date and time the membership was created."""
        return self._json_data.get('created')
