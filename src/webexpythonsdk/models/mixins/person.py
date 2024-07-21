"""Webex Person data model.

Copyright (c) 2016-2024 Cisco and/or its affiliates.

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

from webexpythonsdk.utils import WebexDateTime


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

    @property
    def phoneNumbers(self):
        """Phone numbers for the person."""
        return self._json_data.get("phoneNumbers")

    @property
    def extension(self):
        """The Webex Calling extension for the person."""
        return self._json_data.get("extension")

    @property
    def locationId(self):
        """The location ID for the person."""
        return self._json_data.get("locationId")

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
        """List of roles for the person.

        An list of role strings representing the roles to which this
        person belongs.
        """
        return self._json_data.get("roles")

    @property
    def licenses(self):
        """An list of license strings allocated to this person."""
        return self._json_data.get("licenses")

    @property
    def department(self):
        """The business department the user belongs to."""
        return self._json_data.get("department")

    @property
    def manager(self):
        """A manager identifier."""
        return self._json_data.get("manager")

    @property
    def managerId(self):
        """Person ID of the manager."""
        return self._json_data.get("managerId")

    @property
    def title(self):
        """The person's title."""
        return self._json_data.get("title")

    @property
    def addresses(self):
        """A person's addresses."""
        return self._json_data.get("addresses")

    @property
    def created(self):
        """The date and time the person was created."""
        created = self._json_data.get("created")
        if created:
            return WebexDateTime.strptime(created)
        else:
            return None

    @property
    def lastModified(self):
        """The date and time the person was last changed."""
        last_modified = self._json_data.get("lastModified")
        if last_modified:
            return WebexDateTime.strptime(last_modified)
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
        """The date and time of the person"s last activity within Webex."""
        last_activity = self._json_data.get("lastActivity")
        if last_activity:
            return WebexDateTime.strptime(last_activity)
        else:
            return None

    @property
    def siteUrls(self):
        """One or several site names where this user has a role."""
        return self._json_data.get("siteUrls")

    @property
    def sipAddresses(self):
        """The user's SIP addresses."""
        return self._json_data.get("sipAddresses")

    @property
    def xmppFederationJid(self):
        """XMPP federation identifier.

        Identifier for intra-domain federation with other XMPP based messenger
        systems.
        """
        return self._json_data.get("xmppFederationJid")

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

            `unknown`: The user's status could not be determined
        """
        return self._json_data.get("status")

    @property
    def invitePending(self):
        """Whether or not an invite is pending for the user to complete account
        activation.

        Person Invite Pending Enum:
            `true`: The person has been invited to Webex but has not
                created an account

            `false`: An invite is not pending for this person
        """
        return self._json_data.get("invitePending")

    @property
    def loginEnabled(self):
        """Whether or not the user is allowed to use Webex.

        Person Login Enabled Enum:
            `true`: The person can log into Webex

            "false": The person cannot log into Webex
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
