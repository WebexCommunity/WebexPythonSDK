# -*- coding: utf-8 -*-
"""Webex Teams Memberships API wrapper.

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


API_ENDPOINT = 'memberships'
OBJECT_TYPE = 'membership'


class MembershipsAPI(object):
    """Webex Teams Memberships API.

    Wraps the Webex Teams Memberships API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new MembershipsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(MembershipsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, roomId=None, personId=None, personEmail=None, max=None,
             **request_parameters):
        """List room memberships.

        By default, lists memberships for rooms to which the authenticated user
        belongs.

        Use query parameters to filter the response.

        Use `roomId` to list memberships for a room, by ID.

        Use either `personId` or `personEmail` to filter the results.

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
            roomId(basestring): Limit results to a specific room, by ID.
            personId(basestring): Limit results to a specific person, by ID.
            personEmail(basestring): Limit results to a specific person, by
                email address.
            max(int): Limit the maximum number of items returned from the Webex
                Teams service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the memberships returned by the Webex Teams query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomId, basestring, optional=True)
        check_type(personId, basestring, optional=True)
        check_type(personEmail, basestring, optional=True)
        check_type(max, int, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
            personId=personId,
            personEmail=personEmail,
            max=max,
        )

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield membership objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def create(self, roomId, personId=None, personEmail=None,
               isModerator=False, **request_parameters):
        """Add someone to a room by Person ID or email address.

        Add someone to a room by Person ID or email address; optionally
        making them a moderator.

        Args:
            roomId(basestring): The room ID.
            personId(basestring): The ID of the person.
            personEmail(basestring): The email address of the person.
            isModerator(bool): Set to True to make the person a room moderator.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Membership: A Membership object with the details of the created
            membership.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomId, basestring)
        check_type(personId, basestring, optional=True)
        check_type(personEmail, basestring, optional=True)
        check_type(isModerator, bool, optional=True)

        post_data = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
            personId=personId,
            personEmail=personEmail,
            isModerator=isModerator,
        )

        # API request
        json_data = self._session.post(API_ENDPOINT, json=post_data)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, membershipId):
        """Get details for a membership, by ID.

        Args:
            membershipId(basestring): The membership ID.

        Returns:
            Membership: A Membership object with the details of the requested
            membership.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(membershipId, basestring)

        # API request
        json_data = self._session.get(API_ENDPOINT + '/' + membershipId)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def update(self, membershipId, isModerator=None, **request_parameters):
        """Update properties for a membership, by ID.

        Args:
            membershipId(basestring): The membership ID.
            isModerator(bool): Set to True to make the person a room moderator.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Membership: A Membership object with the updated Webex Teams
            membership details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(membershipId, basestring)
        check_type(isModerator, bool, optional=True)

        put_data = dict_from_items_with_values(
            request_parameters,
            isModerator=isModerator,
        )

        # API request
        json_data = self._session.put(API_ENDPOINT + '/' + membershipId,
                                      json=put_data)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, membershipId):
        """Delete a membership, by ID.

        Args:
            membershipId(basestring): The membership ID.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(membershipId, basestring)

        # API request
        self._session.delete(API_ENDPOINT + '/' + membershipId)
