"""Webex Organization Contact data model.

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

from webexpythonsdk.utils import WebexDateTime


class OrganizationContactBasicPropertiesMixin(object):
    """Organization contact basic properties."""

    @property
    def id(self):
        """A unique identifier for the contact."""
        return self._json_data.get("id")

    @property
    def emails(self):
        """The email addresses of the contact."""
        return self._json_data.get("emails")

    @property
    def contactType(self):
        """The contact type."""
        return self._json_data.get("contactType")

    @property
    def schemas(self):
        """The schema identifier for the contact."""
        return self._json_data.get("schemas")

    @property
    def phoneNumbers(self):
        """Phone numbers for the contact."""
        return self._json_data.get("phoneNumbers")

    @property
    def extension(self):
        """The Webex Calling extension for the contact."""
        return self._json_data.get("extension")

    @property
    def displayName(self):
        """The full name of the contact."""
        return self._json_data.get("displayName")

    @property
    def firstName(self):
        """The first name of the contact."""
        return self._json_data.get("firstName")

    @property
    def lastName(self):
        """The last name of the contact."""
        return self._json_data.get("lastName")

    @property
    def avatar(self):
        """The URL to the contact's avatar in PNG format."""
        return self._json_data.get("avatar")

    @property
    def orgId(self):
        """The ID of the organization to which this contact belongs."""
        return self._json_data.get("orgId")

    @property
    def department(self):
        """The business department the contact belongs to."""
        return self._json_data.get("department")

    @property
    def manager(self):
        """A manager identifier."""
        return self._json_data.get("manager")

    @property
    def managerId(self):
        """Person ID of the manager."""
        return self._json_data.get("managerId")

    @property
    def title(self):
        """The contact's title."""
        return self._json_data.get("title")

    @property
    def addresses(self):
        """A contact's addresses."""
        return self._json_data.get("addresses")

    @property
    def customAttributes(self):
        """A contact's custom attributes."""
        return self._json_data.get("customAttributes")

    @property
    def created(self):
        """The date and time the contact was created."""
        created = self._json_data.get("created")
        if created:
            return WebexDateTime.strptime(created)
        else:
            return None

    @property
    def lastModified(self):
        """The date and time the contact was last changed."""
        last_modified = self._json_data.get("lastModified")
        if last_modified:
            return WebexDateTime.strptime(last_modified)
        else:
            return None
