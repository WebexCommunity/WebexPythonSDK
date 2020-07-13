# -*- coding: utf-8 -*-
"""Webex Teams Person data model.

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


class PersonBasicPropertiesMixin(object):
    """Person basic properties."""

    @property
    def id(self):
        """A unique identifier for the person."""
        return self._json_data.get("id")

    @property
    def emails(self):
        """The email addresses of the person."""
        return self._json_data.get("emails")

    def phoneNumbers(self):
        """Phone numbers for the person."""
        return self._json_data.get("phoneNumbers")

    @property
    def displayName(self):
        """The full name of the person."""
        return self._json_data.get("displayName")

    @property
    def nickName(self):
        """The nickname of the person if configured.

        If no nickname is configured for the person, this field will not be
        present.
        """
        return self._json_data.get("nickName")

    @property
    def firstName(self):
        """The first name of the person."""
        return self._json_data.get("firstName")

    @property
    def lastName(self):
        """The last name of the person."""
        return self._json_data.get("lastName")

    @property
    def avatar(self):
        """The URL to the person"s avatar in PNG format."""
        return self._json_data.get("avatar")

    @property
    def orgId(self):
        """The ID of the organization to which this person belongs."""
        return self._json_data.get("orgId")

    @property
    def roles(self):
        """An array of role strings representing the roles to which this
        person belongs. """
        return self._json_data.get("roles")

    @property
    def licenses(self):
        """An array of license strings allocated to this person."""
        return self._json_data.get("licenses")

    @property
    def created(self):
        """The date and time the person was created."""
        created = self._json_data.get("created")
        if created:
            return WebexTeamsDateTime.strptime(created)
        else:
            return None

    @property
    def lastModified(self):
        """The date and time the person was last changed."""
        last_modified = self._json_data.get("lastModified")
        if last_modified:
            return WebexTeamsDateTime.strptime(last_modified)
        else:
            return None

    @property
    def timezone(self):
        """The time zone of the person if configured.

        If no timezone is configured on the account, this field will not be
        present.
        """
        return self._json.get("timezone")

    @property
    def lastActivity(self):
        """The date and time of the person"s last activity within Webex
        Teams. """
        last_activity = self._json_data.get("lastActivity")
        if last_activity:
            return WebexTeamsDateTime.strptime(last_activity)
        else:
            return None

    @property
    def status(self):
        """The current presence status of the person.

        Person Status Enum:
            `active`: Active within the last 10 minutes

            `call`: The user is in a call

            `DoNotDisturb`: The user has manually set their status to
                "Do Not Disturb"

            `inactive`: Last activity occurred more than 10 minutes ago

            `meeting`: The user is in a meeting

            `OutOfOffice`: The user or a Hybrid Calendar service has indicated
                that they are "Out of Office"

            `pending`: The user has never logged in; a status cannot be
                determined

            `presenting`: The user is sharing content

            `unknown`: The user’s status could not be determined
        """
        return self._json_data.get("status")

    @property
    def invitePending(self):
        """Whether or not an invite is pending for the user to complete account
        activation.

        Person Invite Pending Enum:
            `true`: The person has been invited to Webex Teams but has not
                created an account

            `false`: An invite is not pending for this person
        """
        return self._json_data.get("invitePending")

    @property
    def loginEnabled(self):
        """Whether or not the user is allowed to use Webex Teams.

        Person Login Enabled Enum:
            `true`: The person can log into Webex Teams

            "false": The person cannot log into Webex Teams
        """
        return self._json_data.get("loginEnabled")

    @property
    def type(self):
        """The type of person account, such as person or bot.

        Person Type Enum:
            `person`: Account belongs to a person
            `bot`: Account is a bot user
            `appuser`: Account is a guest user
        """
        return self._json_data.get("type")
