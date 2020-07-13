# -*- coding: utf-8 -*-
"""Webex Teams Room data model.

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


class RoomBasicPropertiesMixin(object):
    """Room basic properties."""

    @property
    def id(self):
        """A unique identifier for the room."""
        return self._json_data.get("id")

    @property
    def title(self):
        """A user-friendly name for the room."""
        return self._json_data.get("title")

    @property
    def type(self):
        """The room type.

        Room Type Enum:
            `direct`: 1:1 room

            `group`: Group room
        """
        return self._json_data.get("type")

    @property
    def isLocked(self):
        """Whether the room is moderated (locked) or not."""
        return self._json_data.get("isLocked")

    @property
    def teamId(self):
        """The ID for the team with which this room is associated."""
        return self._json_data.get("teamId")

    @property
    def lastActivity(self):
        """The date and time of the room"s last activity."""
        last_activity = self._json_data.get("lastActivity")
        if last_activity:
            return WebexTeamsDateTime.strptime(last_activity)
        else:
            return None

    @property
    def creatorId(self):
        """The ID of the person who created this room."""
        return self._json_data.get("creatorId")

    @property
    def created(self):
        """The date and time the room was created."""
        created = self._json_data.get("created")
        if created:
            return WebexTeamsDateTime.strptime(created)
        else:
            return None

    @property
    def ownerId(self):
        """The ID of the organization which owns this room."""
        return self._json_data.get("ownerId")
