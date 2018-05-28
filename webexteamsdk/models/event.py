# -*- coding: utf-8 -*-
"""Cisco Spark Event data model."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from .sparkdata import SparkData


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


class EventBasicPropertiesMixin(object):
    """A mixin for :class:`SparkData` classes."""

    @property
    def id(self):
        """Event ID."""
        return self._json_data.get('id')

    @property
    def resource(self):
        """The event resource type (`messagess`, `memberships`)."""
        return self._json_data.get('resource')

    @property
    def type(self):
        """The event type (`created`, `updated`, `deleted`)."""
        return self._json_data.get('type')

    @property
    def actorId(self):
        """The ID of the person that performed this event."""
        return self._json_data.get('actorId')

    @property
    def created(self):
        """The date and time the event was performed."""
        return self._json_data.get('created')

    @property
    def data(self):
        """The event resource data."""
        return SparkData(self._json_data.get('data'))
