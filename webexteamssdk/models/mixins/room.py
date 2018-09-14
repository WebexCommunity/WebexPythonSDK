# -*- coding: utf-8 -*-
"""Webex Teams Room data model.

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


class RoomBasicPropertiesMixin(object):
    """Room basic properties."""

    @property
    def id(self):
        """The rooms's unique ID."""
        return self._json_data.get('id')

    @property
    def title(self):
        """A user-friendly name for the room."""
        return self._json_data.get('title')

    @property
    def type(self):
        """The type of room (i.e. 'group', 'direct' etc.)."""
        return self._json_data.get('type')

    @property
    def isLocked(self):
        """Whether or not the room is locked and controlled by moderator(s)."""
        return self._json_data.get('isLocked')

    @property
    def lastActivity(self):
        """The date and time when the room was last active."""
        last_activity = self._json_data.get('lastActivity')
        if last_activity:
            return WebexTeamsDateTime.strptime(last_activity)
        else:
            return None

    @property
    def created(self):
        """The date and time when the room was created."""
        created = self._json_data.get('created')
        if created:
            return WebexTeamsDateTime.strptime(created)
        else:
            return None

    @property
    def creatorId(self):
        """The ID of the person who created the room."""
        return self._json_data.get('creatorId')

    @property
    def teamId(self):
        """The ID for the team with which this room is associated."""
        return self._json_data.get('teamId')
