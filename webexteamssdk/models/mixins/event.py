# -*- coding: utf-8 -*-
"""Webex Teams Event data model.

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


class EventBasicPropertiesMixin(object):
    """Event basic properties."""

    @property
    def id(self):
        """The unique identifier for the event."""
        return self._json_data.get('id')

    @property
    def resource(self):
        """The type of resource in the event.

        Event Resource Enum:
            `messages`
            `memberships`
        """
        return self._json_data.get('resource')

    @property
    def type(self):
        """The action which took place in the event.

        Event Type Enum:
            `created`
            `updated`
            `deleted`
        """
        return self._json_data.get('type')

    @property
    def appId(self):
        """The ID of the application for the event."""
        return self._json_data.get('appId')

    @property
    def actorId(self):
        """The ID of the person who performed the action."""
        return self._json_data.get('actorId')

    @property
    def orgId(self):
        """The ID of the organization for the event."""
        return self._json_data.get('orgId')

    @property
    def created(self):
        """The date and time of the event."""
        created = self._json_data.get('created')
        if created:
            return WebexTeamsDateTime.strptime(created)
        else:
            return None
