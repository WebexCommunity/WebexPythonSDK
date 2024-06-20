# -*- coding: utf-8 -*-
"""Webex Teams Room Tabs API wrapper.

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


API_ENDPOINT = "room/tabs"
OBJECT_TYPE = "room_tab"


class RoomTabsAPI(object):
    """Webex Teams Room Tabs API.

    Wraps the Webex Teams Room Tabs API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new RoomTabsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(RoomTabsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, roomId, **request_parameters):
        """Lists all Room Tabs of a room.

        This method supports Webex Teams's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all room tabs returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            roomId(basestring): List Room Tabs associated with a room, by ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the room tabs returned by the Webex Teams query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomId, basestring)

        params = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
        )

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield room objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def create(self, roomId, contentUrl, displayName, **request_parameters):
        """Create a room tab.

        Add a tab with a content url to a room that can be accessed in the room

        Args:
            roomId(basestring): A unique identifier for the room.
            contentUrl(basestring): Content Url of the Room Tab.
                Needs to use the https protocol.
            displayName(basestring): A user-friendly name for the room.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).
        Returns:
            RoomTab: A Room Tab with the details of the created room tab.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomId, basestring)
        check_type(contentUrl, basestring)
        check_type(displayName, basestring)

        post_data = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
            contentUrl=contentUrl,
            displayName=displayName,
        )

        # API request
        json_data = self._session.post(API_ENDPOINT, json=post_data)

        # Return a room object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, roomTabId):
        """Get the details of a room tab, by ID.

        Args:
            roomTabId(basestring): The ID of the room tab to be retrieved.

        Returns:
            Room: A RoomTab object with the details of the requested room tab.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomTabId, basestring)

        # API request
        json_data = self._session.get(API_ENDPOINT + "/" + roomTabId)

        # Return a room object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def update(
        self, roomTabId, roomId, contentUrl, displayName, **request_parameters
    ):
        """Updates the content url of a Room Tab by ID.

        Args:
            roomTabId(basestring): The unique identifier for the Room Tab.
            roomId(basestring): The room ID.
            contentUrl(basestring): Content Url of the Room Tab.
                Needs to use the https protocol.
            displayName(basestring): A user-friendly name for the room.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Room: A Room object with the updated Webex Teams room details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomTabId, basestring)
        check_type(roomId, basestring)
        check_type(contentUrl, basestring)
        check_type(displayName, basestring)

        put_data = dict_from_items_with_values(
            request_parameters,
            roomTabId=roomTabId,
            roomId=roomId,
            contentUrl=contentUrl,
            displayName=displayName,
        )

        # API request
        json_data = self._session.put(
            API_ENDPOINT + "/" + roomTabId, json=put_data
        )

        # Return a room object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, roomTabId):
        """Delete a room tab.

        Args:
            roomTabId(basestring): The ID of the room tab to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roomTabId, basestring)

        # API request
        self._session.delete(API_ENDPOINT + "/" + roomTabId)
