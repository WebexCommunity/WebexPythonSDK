# -*- coding: utf-8 -*-
"""Webex Teams License data model.

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


class LicenseBasicPropertiesMixin(object):
    """License basic properties."""

    @property
    def id(self):
        """A unique identifier for the license."""
        return self._json_data.get("id")

    @property
    def name(self):
        """Name of the licensed feature."""
        return self._json_data.get("name")

    @property
    def totalUnits(self):
        """Total number of license units allocated."""
        return self._json_data.get("totalUnits")

    @property
    def consumedUnits(self):
        """Total number of license units consumed."""
        return self._json_data.get("consumedUnits")

    @property
    def subscriptionId(self):
        """The subscription ID associated with this license.

        This ID is used in other systems, such as Webex Control Hub.
        """
        return self._json_data.get("subscriptionId")

    @property
    def siteUrl(self):
        """The Webex Meetings site associated with this license."""
        return self._json_data.get("siteUrl")

    @property
    def siteType(self):
        """The type of site associated with this license.

        `Control Hub managed site` the site is managed by Webex Control Hub.

        `Linked site` the site is a linked site

        `Site Admin managed site` the site is managed by Site Administration
        """
        return self._json_data.get("siteType")
