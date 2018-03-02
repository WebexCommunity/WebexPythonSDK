# -*- coding: utf-8 -*-
"""Cisco Spark Message data model."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


class MessageBasicPropertiesMixin(object):
    """A mixin for :class:`SparkData` classes."""

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
        return self._json_data.get('created')
