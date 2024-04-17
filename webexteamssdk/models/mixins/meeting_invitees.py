# -*- coding: utf-8 -*-
"""Webex MeetingInvitees data model.

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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *


class MeetingInviteeBasicPropertiesMixin(object):
    """MeetingInvitee basic properties."""

    @property
    def id(self):
        """Unique id for the meeting invitee"""
        return self._json_data.get("id")

    @property
    def email(self):
        """Email address for the meeting invitee"""
        return self._json_data.get("email")

    @property
    def displayName(self):
        """Display name of the meeting invitee"""
        return self._json_data.get("displayName")

    @property
    def coHost(self):
        """CoHost status of the invitee"""
        return self._json_data.get("coHost")

    @property
    def meetingId(self):
        """Unique id for the meeting that the invitee is part of"""
        return self._json_data.get("meetingId")

    @property
    def panelist(self):
        """Flag to indicate if the invitee is panelist or not"""
        return self._json_data.get("panelist")
