# -*- coding: utf-8 -*-
"""Webex MeetingTemplates API wrapper.

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

from past.builtins import basestring

from ..generator_containers import generator_container
from ..restsession import RestSession
from ..utils import (
    check_type,
    dict_from_items_with_values,
)


API_ENDPOINT = "meetings/templates"
OBJECT_TYPE = "meetingTemplate"


class MeetingTemplatesAPI(object):
    """Webex MeetingTemplates API.

    Wraps the Webex MeetingTemplates API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new MeetingTemplatesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(MeetingTemplatesAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(
        self,
        templateType=None,
        locale=None,
        isDefault=None,
        isStandard=None,
        hostEmail=None,
        siteUrl=None,
        headers=None,
        **request_parameters,
    ):
        """List meetingTemplates.

        Use query parameters to filter the response.

        This method supports Webex Teams's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all memberships returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            templateType (basestring): Meeting template types (meeting,
                webinar).
            locale (basestring): Locale for the meeting template (i.e. en_US).
            isDefault (bool): Flag to indicate if default or non-default
                meeting templates are returned.
            isStandard (bool): Flag to indicate if standard or non-standard
                meeting templates are returned.
            hostEmail (bool): Email address of a meeting host (Requires
                admin-level scope).
            siteUrl (bool): URL of the Webex site from which we are listing.
            headers(dict): Additional headers to be passed.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the meetingTemplates returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(templateType, basestring, optional=True)
        check_type(locale, basestring, optional=True)
        check_type(isDefault, bool, optional=True)
        check_type(isStandard, bool, optional=True)
        check_type(hostEmail, bool, optional=True)
        check_type(siteUrl, bool, optional=True)
        check_type(headers, dict, optional=True)

        headers = headers or {}

        params = dict_from_items_with_values(
            request_parameters,
            templateType=templateType,
            locale=locale,
            isDefault=isDefault,
            isStandard=isStandard,
            hostEmail=hostEmail,
            siteUrl=siteUrl,
        )

        # API request - get items

        # Update headers
        for k, v in headers.items():
            self._session.headers[k] = v
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Remove headers
        for k in headers.keys():
            del self._session.headers[k]

        # Yield membership objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def get(self, meetingTemplateId):
        """Get details for a meetingTemplate, by ID.

        Args:
            meetingTemplateId(basestring): The meetingTemplate ID.

        Returns:
            MeetingTemplate: A MeetingTemplate object with the details of the
            requested meetingTemplate.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(meetingTemplateId, basestring)

        # API request
        json_data = self._session.get(API_ENDPOINT + "/" + meetingTemplateId)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
