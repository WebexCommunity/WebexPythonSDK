# -*- coding: utf-8 -*-
"""Webex Teams Teams-API wrapper.

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


API_ENDPOINT = 'teams'
OBJECT_TYPE = 'team'


class TeamsAPI(object):
    """Webex Teams Teams API.

    Wraps the Webex Teams Teams API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new TeamsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(TeamsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, max=100, **request_parameters):
        """List teams to which the authenticated user belongs.

        This method supports Webex Teams's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all teams returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            max(int): Limit the maximum number of items returned from the Webex
                Teams service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the teams returned by the Webex Teams query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(max, int, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            max=max,
        )

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield team objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def create(self, name, **request_parameters):
        """Create a team.

        The authenticated user is automatically added as a member of the team.

        Args:
            name(basestring): A user-friendly name for the team.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Team: A Team object with the details of the created team.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(name, basestring)

        post_data = dict_from_items_with_values(
            request_parameters,
            name=name,
        )

        # API request
        json_data = self._session.post(API_ENDPOINT, json=post_data)

        # Return a team object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, teamId):
        """Get the details of a team, by ID.

        Args:
            teamId(basestring): The ID of the team to be retrieved.

        Returns:
            Team: A Team object with the details of the requested team.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(teamId, basestring)

        # API request
        json_data = self._session.get(API_ENDPOINT + '/' + teamId)

        # Return a team object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def update(self, teamId, name, **request_parameters):
        """Update details for a team, by ID.

        Args:
            teamId(basestring): The team ID.
            name(basestring): A user-friendly name for the team.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Team: A Team object with the updated Webex Teams team details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(teamId, basestring)
        check_type(name, basestring)

        put_data = dict_from_items_with_values(
            request_parameters,
            name=name,
        )

        # API request
        json_data = self._session.put(API_ENDPOINT + '/' + teamId,
                                      json=put_data)

        # Return a team object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, teamId):
        """Delete a team.

        Args:
            teamId(basestring): The ID of the team to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(teamId, basestring)

        # API request
        self._session.delete(API_ENDPOINT + '/' + teamId)
