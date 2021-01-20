# -*- coding: utf-8 -*-
"""Webex Teams Rooms API wrapper.

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


API_ENDPOINT = 'rooms'
OBJECT_TYPE = 'room'


class RoomsAPI(object):
    """Webex Teams Rooms API.

    Wraps the Webex Teams Rooms API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new RoomsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(RoomsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, teamId=None, type=None, sortBy=None, max=100,
             **request_parameters):
        """List rooms.

        By default, lists rooms to which the authenticated user belongs.

        This method supports Webex Teams's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all rooms returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            teamId(basestring): Limit the rooms to those associated with a
                team, by ID.
            type(basestring): 'direct' returns all 1-to-1 rooms. `group`
                returns all group rooms. If not specified or values not
                matched, will return all room types.
            sortBy(basestring): Sort results by room ID (`id`), most recent
                activity (`lastactivity`), or most recently created
                (`created`).
            max(int): Limit the maximum number of items returned from the Webex
                Teams service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the rooms returned by the Webex Teams query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(teamId, basestring, optional=True)
        check_type(type, basestring, optional=True)
        check_type(sortBy, basestring, optional=True)
        check_type(max, int, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            teamId=teamId,
            type=type,
            sortBy=sortBy,
            max=max,
        )

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield room objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def create(self, title, teamId=None, **request_parameters):
        """Create a room.

        The authenticated user is automatically added as a member of the room.

        Args:
            title(basestring): A user-friendly name for the room.
            teamId(basestring): The team ID with which this room is
                associated.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Room: A Room with the details of the created room.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(title, basestring, optional=True)
        check_type(teamId, basestring, optional=True)

        post_data = dict_from_items_with_values(
            request_parameters,
            title=title,
            teamId=teamId,
        )

        # API request
        json_data = self._session.post(API_ENDPOINT, json=post_data)

        # Return a room object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, roomId):
        """Get the details of a room, by ID.

        Args:
            roomId(basestring): The ID of the room to be retrieved.

        Returns:
            Room: A Room object with the details of the requested room.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomId, basestring)

        # API request
        json_data = self._session.get(API_ENDPOINT + '/' + roomId)

        # Return a room object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get_meeting_info(self, roomId):
        """Get the meeting details for a room.

        Args:
            roomId(basestring): The unique identifier for the room.

        Returns:
            RoomMeetingInfo: A Room Meeting Info object with the meeting
            details for the room such as the SIP address, meeting URL,
            toll-free and toll dial-in numbers.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomId, basestring)

        # API request
        json_data = self._session.get(
            API_ENDPOINT + '/' + roomId + '/meetingInfo',
        )

        # Return a room meeting info object created from the response JSON data
        return self._object_factory("room_meeting_info", json_data)

    def update(self, roomId, title, **request_parameters):
        """Update details for a room, by ID.

        Args:
            roomId(basestring): The room ID.
            title(basestring): A user-friendly name for the room.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Room: A Room object with the updated Webex Teams room details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomId, basestring)
        check_type(title, basestring)

        put_data = dict_from_items_with_values(
            request_parameters,
            title=title,
        )

        # API request
        json_data = self._session.put(API_ENDPOINT + '/' + roomId,
                                      json=put_data)

        # Return a room object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, roomId):
        """Delete a room.

        Args:
            roomId(basestring): The ID of the room to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomId, basestring)

        # API request
        self._session.delete(API_ENDPOINT + '/' + roomId)
