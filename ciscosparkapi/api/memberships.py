# -*- coding: utf-8 -*-
"""Cisco Spark Memberships API wrapper.

Classes:
    Membership: Models a Spark 'membership' JSON object as a native Python
        object.
    MembershipsAPI: Wraps the Cisco Spark Memberships API and exposes the
        APIs as native Python methods that return native Python objects.

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


class Membership(SparkData):
    """Model a Spark 'membership' JSON object as a native Python object."""

    def __init__(self, json):
        """Initialize a Membership object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Membership, self).__init__(json)

    @property
    def id(self):
        """The membership's unique ID."""
        return self._json_data.get('id')

    @property
    def roomId(self):
        """The ID of the room."""
        return self._json_data.get('roomId')

    @property
    def personId(self):
        """The ID of the person."""
        return self._json_data.get('personId')

    @property
    def personEmail(self):
        """The email address of the person."""
        return self._json_data.get('personEmail')

    @property
    def personDisplayName(self):
        """The display name of the person."""
        return self._json_data.get('personDisplayName')

    @property
    def personOrgId(self):
        """The ID of the organization that the person is associated with."""
        return self._json_data.get('personOrgId')

    @property
    def isModerator(self):
        """Person is a moderator for the room."""
        return self._json_data.get('isModerator')

    @property
    def isMonitor(self):
        """Person is a monitor for the room."""
        return self._json_data.get('isMonitor')

    @property
    def created(self):
        """The date and time the membership was created."""
        return self._json_data.get('created')


class MembershipsAPI(object):
    """Cisco Spark Memberships API wrapper.

    Wraps the Cisco Spark Memberships API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session):
        """Init a new MembershipsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(MembershipsAPI, self).__init__()

        self._session = session

    @generator_container
    def list(self, roomId=None, personId=None, personEmail=None, max=None,
             **request_parameters):
        """List room memberships.

        By default, lists memberships for rooms to which the authenticated user
        belongs.

        Use query parameters to filter the response.

        Use `roomId` to list memberships for a room, by ID.

        Use either `personId` or `personEmail` to filter the results.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all memberships returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            roomId(basestring): Limit results to a specific room, by ID.
            personId(basestring): Limit results to a specific person, by ID.
            personEmail(basestring): Limit results to a specific person, by
                email address.
            max(int): Limit the maximum number of items returned from the Spark
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
                yields the memberships returned by the Cisco Spark query.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(roomId, basestring)
        check_type(personId, basestring)
        check_type(personEmail, basestring)
        check_type(max, int)

        params = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
            personId=personId,
            personEmail=personEmail,
            max=max,
        )

        # API request - get items
        items = self._session.get_items('memberships', params=params)

        # Yield Person objects created from the returned items JSON objects
        for item in items:
            yield Membership(item)

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
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(roomId, basestring, may_be_none=False)
        check_type(personId, basestring)
        check_type(personEmail, basestring)
        check_type(isModerator, bool)

        post_data = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
            personId=personId,
            personEmail=personEmail,
            isModerator=isModerator,
        )

        # API request
        json_data = self._session.post('memberships', json=post_data)

        # Return a Membership object created from the response JSON data
        return Membership(json_data)

    def get(self, membershipId):
        """Get details for a membership, by ID.

        Args:
            membershipId(basestring): The membership ID.

        Returns:
            Membership: A Membership object with the details of the requested
                membership.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(membershipId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get('memberships/' + membershipId)

        # Return a Membership object created from the response JSON data
        return Membership(json_data)

    def update(self, membershipId, isModerator=None, **request_parameters):
        """Update properties for a membership, by ID.

        Args:
            membershipId(basestring): The membership ID.
            isModerator(bool): Set to True to make the person a room moderator.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Membership: A Membership object with the updated Spark membership
                details.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(membershipId, basestring, may_be_none=False)
        check_type(isModerator, bool)

        put_data = dict_from_items_with_values(
            request_parameters,
            isModerator=isModerator,
        )

        # API request
        json_data = self._session.put('memberships/' + membershipId,
                                      json=put_data)

        # Return a Membership object created from the response JSON data
        return Membership(json_data)

    def delete(self, membershipId):
        """Delete a membership, by ID.

        Args:
            membershipId(basestring): The membership ID.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(membershipId, basestring)

        # API request
        self._session.delete('memberships/' + membershipId)
