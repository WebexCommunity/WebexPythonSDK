# -*- coding: utf-8 -*-
"""Webex Teams Team-Membership data model.

Copyright (c) 2016-2020 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from webexteamssdk.utils import WebexTeamsDateTime


class TeamMembershipBasicPropertiesMixin(object):
    """Team Membership basic properties."""

    @property
    def id(self):
        """A unique identifier for the team membership."""
        return self._json_data.get('id')

    @property
    def teamId(self):
        """The team ID."""
        return self._json_data.get('teamId')

    @property
    def personId(self):
        """The person ID."""
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
        """The organization ID of the person."""
        return self._json_data.get('personOrgId')

    @property
    def isModerator(self):
        """Whether or not the participant is a team moderator."""
        return self._json_data.get('isModerator')

    @property
    def created(self):
        """The date and time when the team membership was created."""
        created = self._json_data.get('created')
        if created:
            return WebexTeamsDateTime.strptime(created)
        else:
            return None
