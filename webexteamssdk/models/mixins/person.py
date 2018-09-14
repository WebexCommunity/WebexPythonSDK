# -*- coding: utf-8 -*-
"""Webex Teams Person data model.

Copyright (c) 2016-2018 Cisco and/or its affiliates.

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


class PersonBasicPropertiesMixin(object):
    """Person basic properties."""

    @property
    def type(self):
        """The type of object returned by Webex Teams (should be `person`)."""
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
        created = self._json_data.get('created')
        if created:
            return WebexTeamsDateTime.strptime(created)
        else:
            return None

    @property
    def status(self):
        """The person's current status."""
        return self._json_data.get('status')

    @property
    def lastActivity(self):
        """The date and time of the person's last activity."""
        last_activity = self._json_data.get('lastActivity')
        if last_activity:
            return WebexTeamsDateTime.strptime(last_activity)
        else:
            return None

    @property
    def invitePending(self):
        """Person has been sent an invite, but hasn't responded."""
        return self._json_data.get('invitePending')

    @property
    def loginEnabled(self):
        """Person is allowed to login."""
        return self._json_data.get('loginEnabled')
