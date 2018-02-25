# -*- coding: utf-8 -*-
"""Cisco Spark Person data model."""


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


class Person(SparkData):
    """Model a Spark person JSON object as a native Python object."""

    def __init__(self, json):
        """Initialize a Person data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Person, self).__init__(json)

    @property
    def type(self):
        """The type of object returned by Cisco Spark (should be `person`)."""
        return self._json_data.get('type')

    @property
    def id(self):
        """The person's unique ID."""
        return self._json_data.get('id')

    @property
    def emails(self):
        """Email address(es) of the person."""
        return self._json_data['emails']

    @property
    def displayName(self):
        """Full name of the person."""
        return self._json_data.get('displayName')

    @property
    def nickName(self):
        """'Nick name' or preferred short name of the person."""
        return self._json_data.get('nickName')

    @property
    def firstName(self):
        """First name of the person."""
        return self._json_data.get('firstName')

    @property
    def lastName(self):
        """Last name of the person."""
        return self._json_data.get('lastName')

    @property
    def avatar(self):
        """URL to the person's avatar in PNG format."""
        return self._json_data.get('avatar')

    @property
    def orgId(self):
        """ID of the organization to which this person belongs."""
        return self._json_data.get('orgId')

    @property
    def roles(self):
        """Roles of the person."""
        return self._json_data.get('roles')

    @property
    def licenses(self):
        """Licenses allocated to the person."""
        return self._json_data.get('licenses')

    @property
    def created(self):
        """The date and time the person was created."""
        return self._json_data.get('created')

    @property
    def status(self):
        """The person's current status."""
        return self._json_data.get('status')

    @property
    def lastActivity(self):
        """The date and time of the person's last activity."""
        return self._json_data.get('lastActivity')

    @property
    def invitePending(self):
        """Person has been sent an invite, but hasn't responded."""
        return self._json_data.get('invitePending')

    @property
    def loginEnabled(self):
        """Person is allowed to login."""
        return self._json_data.get('loginEnabled')
