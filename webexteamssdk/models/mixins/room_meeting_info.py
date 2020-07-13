# -*- coding: utf-8 -*-
"""Webex Teams Room Meeting Info data model.

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


class RoomMeetingInfoBasicPropertiesMixin(object):
    """Room basic properties."""

    @property
    def roomId(self):
        """A unique identifier for the room."""
        return self._json_data.get("roomId")

    @property
    def meetingLink(self):
        """The Webex meeting URL for the room."""
        return self._json_data.get("meetingLink")

    @property
    def sipAddress(self):
        """The SIP address for the room."""
        return self._json_data.get("sipAddress")

    @property
    def meetingNumber(self):
        """The Webex meeting number for the room."""
        return self._json_data.get("meetingNumber")

    @property
    def callInTollFreeNumber(self):
        """The toll-free PSTN number for the room."""
        return self._json_data.get("callInTollFreeNumber")

    @property
    def callInTollNumber(self):
        """The toll (local) PSTN number for the room."""
        return self._json_data.get("callInTollNumber")
