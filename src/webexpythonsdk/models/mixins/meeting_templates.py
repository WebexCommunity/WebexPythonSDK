"""Webex MeetingTemplates data model.

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


class MeetingTemplateBasicPropertiesMixin(object):
    """MeetingTemplate basic properties."""

    @property
    def id(self):
        """Unique id for meeting template"""
        return self._json_data.get("id")

    @property
    def name(self):
        """Name of the meeting template"""
        return self._json_data.get("name")

    @property
    def locale(self):
        """Locale for the meeting template"""
        return self._json_data.get("locale")

    @property
    def siteUrl(self):
        """Site URL for the meeting template"""
        return self._json_data.get("siteUrl")

    @property
    def templateType(self):
        """Type of the meeting template (meeting, webinar)"""
        return self._json_data.get("templateType")

    @property
    def isDefault(self):
        """Whether or not the meeting template is a default template"""
        return self._json_data.get("isDefault")

    @property
    def isStandard(self):
        """Whether or not the meeting template is a standard template"""
        return self._json_data.get("isStandard")

    @property
    def meeting(self):
        """Meeting object which is used as a template to create a meeting.

        Meeting object which is used to create a meeting by the meeting
        template. Please note that the meeting object should be used to create
        a meeting immediately.
        """
        return self._json_data.get("meeting")
