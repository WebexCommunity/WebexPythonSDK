# -*- coding: utf-8 -*-
"""Webex Teams Webhook-Event data model.

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


class AdminAuditEventDataBasicPropertiesMixin(object):
    """Admin Audit Event Data basic properties."""

    @property
    def actorOrgName(self):
        """The display name of the organization."""
        return self._json_data.get('actorOrgName')

    @property
    def targetName(self):
        """The name of the resource being acted upon."""
        return self._json_data.get('targetName')

    @property
    def eventDescription(self):
        """A description for the event."""
        return self._json_data.get('eventDescription')

    @property
    def actorName(self):
        """The name of the person who performed the action."""
        return self._json_data.get('actorName')

    @property
    def actorEmail(self):
        """The email of the person who performed the action."""
        return self._json_data.get('actorEmail')

    @property
    def adminRoles(self):
        """Admin roles for the person."""
        return self._json_data.get('adminRoles')

    @property
    def trackingId(self):
        """A tracking identifier for the event."""
        return self._json_data.get('trackingId')

    @property
    def targetType(self):
        """The type of resource changed by the event."""
        return self._json_data.get('targetType')

    @property
    def targetId(self):
        """The identifier for the resource changed by the event."""
        return self._json_data.get('targetId')

    @property
    def eventCategory(self):
        """The category of resource changed by the event."""
        return self._json_data.get('eventCategory')

    @property
    def actorUserAgent(self):
        """The browser user agent of the person who performed the action."""
        return self._json_data.get('actorUserAgent')

    @property
    def actorIp(self):
        """The IP address of the person who performed the action."""
        return self._json_data.get('actorIp')

    @property
    def targetOrgId(self):
        """The orgId of the organization."""
        return self._json_data.get('targetOrgId')

    @property
    def actionText(self):
        """A more detailed description of the change made by the person."""
        return self._json_data.get('actionText')

    @property
    def targetOrgName(self):
        """The name of the organization being acted upon."""
        return self._json_data.get('targetOrgName')


class AdminAuditEventBasicPropertiesMixin(object):
    """Admin Audit Event basic properties."""

    @property
    def id(self):
        """A unique identifier for the event."""
        return self._json_data.get('id')

    @property
    def actorId(self):
        """The personId of the person who made the change."""
        return self._json_data.get('actorId')

    @property
    def orgId(self):
        """The orgId of the person who made the change."""
        return self._json_data.get('orgId')

    @property
    def created(self):
        """The date and time the event took place."""
        created = self._json_data.get('created')
        if created:
            return WebexTeamsDateTime.strptime(created)
        else:
            return None
