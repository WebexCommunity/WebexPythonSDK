# -*- coding: utf-8 -*-
"""Webex Teams Message data model.

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


class AttachmentActionBasicPropertiesMixin(object):
    """Attachment Action basic properties."""

    @property
    def id(self):
        """A unique identifier for the action."""
        return self._json_data.get('id')

    @property
    def personId(self):
        """The ID of the person who performed the action."""
        return self._json_data.get('personId')

    @property
    def roomId(self):
        """The ID of the room the action was performed within."""
        return self._json_data.get('roomId')

    @property
    def type(self):
        """The type of action performed.

        Attachment action enum:
            'submit': submit filled in inputs
        """
        return self._json_data.get('type')

    @property
    def messageId(self):
        """The parent message the attachment action was performed on."""
        return self._json_data.get('messageId')

    @property
    def inputs(self):
        """The attachment action's inputs"""
        return self._json_data.get('inputs')

    @property
    def created(self):
        """The date and time the action was created."""
        created = self._json_data.get('created')
        if created:
            return WebexTeamsDateTime.strptime(created)
        else:
            return None
