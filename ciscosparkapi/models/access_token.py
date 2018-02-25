# -*- coding: utf-8 -*-
"""Cisco Spark Access-Token data model."""


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


class AccessToken(SparkData):
    """Model a Spark 'access token' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new AccessToken data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(AccessToken, self).__init__(json)

    @property
    def access_token(self):
        """Cisco Spark access token."""
        return self._json_data.get('access_token')

    @property
    def expires_in(self):
        """Access token expiry time (in seconds)."""
        return self._json_data.get('expires_in')

    @property
    def refresh_token(self):
        """Refresh token used to request a new/refreshed access token."""
        return self._json_data.get('refresh_token')

    @property
    def refresh_token_expires_in(self):
        """Refresh token expiry time (in seconds)."""
        return self._json_data.get('refresh_token_expires_in')
