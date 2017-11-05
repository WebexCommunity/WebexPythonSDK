# -*- coding: utf-8 -*-
"""Cisco Spark Teams API wrapper.

Classes:
    Team: Models a Spark 'team' JSON object as a native Python object.
    TeamsAPI: Wraps the Cisco Spark Teams API and exposes the API as native
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


class Team(SparkData):
    """Model a Spark 'team' JSON object as a native Python object."""

    def __init__(self, json):
        """Initialize a new Team data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Team, self).__init__(json)

    @property
    def id(self):
        """The team's unique ID."""
        return self._json_data.get('id')

    @property
    def name(self):
        """A user-friendly name for the team."""
        return self._json_data.get('name')

    @property
    def created(self):
        """The date and time the team was created."""
        return self._json_data.get('created')

    @property
    def creatorId(self):
        """The ID of the person who created the team."""
        return self._json_data.get('creatorId')


class TeamsAPI(object):
    """Cisco Spark Teams API wrapper.

    Wraps the Cisco Spark Teams API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session):
        """Initialize a new TeamsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession, may_be_none=False)

        super(TeamsAPI, self).__init__()

        self._session = session

    @generator_container
    def list(self, max=None, **request_parameters):
        """List teams to which the authenticated user belongs.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all teams returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            max(int): Limit the maximum number of items returned from the Spark
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
                yields the teams returned by the Cisco Spark query.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(max, int)

        params = dict_from_items_with_values(
            request_parameters,
            max=max,
        )

        # API request - get items
        items = self._session.get_items('teams', params=params)

        # Yield Team objects created from the returned items JSON objects
        for item in items:
            yield Team(item)

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
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(name, basestring, may_be_none=False)

        post_data = dict_from_items_with_values(
            request_parameters,
            name=name,
        )

        # API request
        json_data = self._session.post('teams', json=post_data)

        # Return a Team object created from the response JSON data
        return Team(json_data)

    def get(self, teamId):
        """Get the details of a team, by ID.

        Args:
            teamId(basestring): The ID of the team to be retrieved.

        Returns:
            Team: A Team object with the details of the requested team.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(teamId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get('teams/' + teamId)

        # Return a Team object created from the response JSON data
        return Team(json_data)

    def update(self, teamId, name=None, **request_parameters):
        """Update details for a team, by ID.

        Args:
            teamId(basestring): The team ID.
            name(basestring): A user-friendly name for the team.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Team: A Team object with the updated Spark team details.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(teamId, basestring, may_be_none=False)
        check_type(name, basestring)

        put_data = dict_from_items_with_values(
            request_parameters,
            name=name,
        )

        # API request
        json_data = self._session.put('teams/' + teamId, json=put_data)

        # Return a Team object created from the response JSON data
        return Team(json_data)

    def delete(self, teamId):
        """Delete a team.

        Args:
            teamId(basestring): The ID of the team to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(teamId, basestring, may_be_none=False)

        # API request
        self._session.delete('teams/' + teamId)
