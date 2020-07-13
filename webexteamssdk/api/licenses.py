# -*- coding: utf-8 -*-
"""Webex Teams Licenses API wrapper.

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

from past.builtins import basestring

from ..generator_containers import generator_container
from ..restsession import RestSession
from ..utils import (
    check_type,
    dict_from_items_with_values,
)


API_ENDPOINT = 'licenses'
OBJECT_TYPE = 'license'


class LicensesAPI(object):
    """Webex Teams Licenses API.

    Wraps the Webex Teams Licenses API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new LicensesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        check_type(session, RestSession)

        super(LicensesAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, orgId=None, **request_parameters):
        """List all licenses for a given organization.

        If no orgId is specified, the default is the organization of the
        authenticated user.

        Args:
            orgId(basestring): Specify the organization, by ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the licenses returned by the Webex Teams query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(orgId, basestring, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
        )

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield license objects created from the returned JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def get(self, licenseId):
        """Get the details of a License, by ID.

        Args:
            licenseId(basestring): The ID of the License to be retrieved.

        Returns:
            License: A License object with the details of the requested
            License.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(licenseId, basestring)

        # API request
        json_data = self._session.get(API_ENDPOINT + '/' + licenseId)

        # Return a license object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)
