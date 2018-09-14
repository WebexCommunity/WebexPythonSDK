# -*- coding: utf-8 -*-
"""Webex Teams Message data model.

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


class MessageBasicPropertiesMixin(object):
    """Message basic properties."""

    @property
    def id(self):
        """The message's unique ID."""
        return self._json_data.get('id')

    @property
    def roomId(self):
        """The ID of the room."""
        return self._json_data.get('roomId')

    @property
    def roomType(self):
        """The type of room (i.e. 'group', 'direct' etc.)."""
        return self._json_data.get('roomType')

    @property
    def text(self):
        """The message, in plain text."""
        return self._json_data.get('text')

    @property
    def files(self):
        """Files attached to the the message (list of URLs)."""
        return self._json_data.get('files')

    @property
    def personId(self):
        """The person ID of the sender."""
        return self._json_data.get('personId')

    @property
    def personEmail(self):
        """The email address of the sender."""
        return self._json_data.get('personEmail')

    @property
    def markdown(self):
        """The message, in markdown format."""
        return self._json_data.get('markdown')

    @property
    def html(self):
        """The message, in HTML format."""
        return self._json_data.get('html')

    @property
    def mentionedPeople(self):
        """The list of IDs of people mentioned in the message."""
        return self._json_data.get('mentionedPeople')

    @property
    def created(self):
        """The date and time the message was created."""
        created = self._json_data.get('created')
        if created:
            return WebexTeamsDateTime.strptime(created)
        else:
            return None
