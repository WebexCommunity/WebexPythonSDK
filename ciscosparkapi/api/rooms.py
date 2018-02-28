# -*- coding: utf-8 -*-
"""Cisco Spark Rooms API."""


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


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


API_ENDPOINT = 'rooms'
OBJECT_TYPE = 'room'


class RoomsAPI(object):
    """Cisco Spark Rooms API.

    Wraps the Cisco Spark Rooms API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new RoomsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession, may_be_none=False)

        super(RoomsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, teamId=None, type=None, sortBy=None, max=None,
             **request_parameters):
        """List rooms.

        By default, lists rooms to which the authenticated user belongs.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all rooms returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
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
            max(int): Limit the maximum number of items returned from the Spark
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
                yields the rooms returned by the Cisco Spark query.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(teamId, basestring)
        check_type(type, basestring)
        check_type(sortBy, basestring)
        check_type(max, int)

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
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(title, basestring)
        check_type(teamId, basestring)

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
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(roomId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get(API_ENDPOINT + '/' + roomId)

        # Return a room object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def update(self, roomId, title=None, **request_parameters):
        """Update details for a room, by ID.

        Args:
            roomId(basestring): The room ID.
            title(basestring): A user-friendly name for the room.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Room: A Room object with the updated Spark room details.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(roomId, basestring, may_be_none=False)
        check_type(roomId, basestring)

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
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(roomId, basestring, may_be_none=False)

        # API request
        self._session.delete(API_ENDPOINT + '/' + roomId)
