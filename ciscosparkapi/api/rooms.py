# -*- coding: utf-8 -*-
"""Cisco Spark Rooms API wrapper.

Classes:
    Room: Models a Spark 'room' JSON object as a native Python object.
    RoomsAPI: Wraps the Cisco Spark Rooms API and exposes the API as native
        Python methods that return native Python objects.

"""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
from past.builtins import basestring

from ..restsession import RestSession
from ..sparkdata import SparkData
from ..utils import (
    check_type,
    dict_from_items_with_values,
    generator_container,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


class Room(SparkData):
    """Model a Spark 'room' JSON object as a native Python object."""

    def __init__(self, json):
        """Initialize a Room data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Room, self).__init__(json)

    @property
    def id(self):
        """The rooms's unique ID."""
        return self._json_data.get('id')

    @property
    def title(self):
        """A user-friendly name for the room."""
        return self._json_data.get('title')

    @property
    def type(self):
        """The type of room (i.e. 'group', 'direct' etc.)."""
        return self._json_data.get('type')

    @property
    def isLocked(self):
        """Whether or not the room is locked and controled by moderator(s)."""
        return self._json_data.get('isLocked')

    @property
    def lastActivity(self):
        """The date and time when the room was last active."""
        return self._json_data.get('lastActivity')

    @property
    def created(self):
        """The date and time when the room was created."""
        return self._json_data.get('created')

    @property
    def creatorId(self):
        """The ID of the person who created the room."""
        return self._json_data.get('creatorId')

    @property
    def teamId(self):
        """The ID for the team with which this room is associated."""
        return self._json_data.get('teamId')


class RoomsAPI(object):
    """Cisco Spark Rooms API wrapper.

    Wraps the Cisco Spark Rooms API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session):
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
        items = self._session.get_items('rooms', params=params)

        # Yield Room objects created from the returned items JSON objects
        for item in items:
            yield Room(item)

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
        json_data = self._session.post('rooms', json=post_data)

        # Return a Room object created from the response JSON data
        return Room(json_data)

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
        json_data = self._session.get('rooms/' + roomId)

        # Return a Room object created from the response JSON data
        return Room(json_data)

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
        json_data = self._session.put('rooms/' + roomId, json=put_data)

        # Return a Room object created from the response JSON data
        return Room(json_data)

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
        self._session.delete('rooms/' + roomId)
