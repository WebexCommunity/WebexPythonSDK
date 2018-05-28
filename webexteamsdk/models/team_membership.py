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


class TeamMembershipBasicPropertiesMixin(object):
    """A mixin for :class:`SparkData` classes."""

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
