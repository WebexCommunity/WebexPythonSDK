# -*- coding: utf-8 -*-
"""Cisco Spark Memberships-API wrapper classes.

Classes:
    TeamMembership: Models a Spark 'team membership' JSON object as a native
        Python object.
    TeamMembershipsAPI: Wrappers the Cisco Spark Memberships-API and exposes
        the API calls as Python method calls that return native Python objects.

"""


from builtins import object
from six import string_types

from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.helper import generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData


class TeamMembership(SparkData):
    """Model a Spark 'team membership' JSON object as a native Python object.
    """

    def __init__(self, json):
        """Init a new TeamMembership object from a JSON dictionary or string.

        Args:
            json(dict, string_types): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(TeamMembership, self).__init__(json)

    @property
    def id(self):
        return self._json['id']

    @property
    def teamId(self):
        return self._json['teamId']

    @property
    def personId(self):
        return self._json['personId']

    @property
    def personEmail(self):
        return self._json['personEmail']

    @property
    def personDisplayName(self):
        return self._json['personDisplayName']

    @property
    def isModerator(self):
        return self._json['isModerator']

    @property
    def created(self):
        return self._json['created']


class TeamMembershipsAPI(object):
    """Cisco Spark Team-Memberships-API wrapper class.

    Wrappers the Cisco Spark Team-Memberships-API and exposes the API calls as
    Python method calls that return native Python objects.

    Attributes:
        session(RestSession): The RESTful session object to be used for API
            calls to the Cisco Spark service.

    """

    def __init__(self, session):
        """Init a new TeamMembershipsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(session, RestSession)
        super(TeamMembershipsAPI, self).__init__()
        self.session = session

    @generator_container
    def list(self, teamId=None, max=None):
        """Lists all team memberships.

        By default, lists memberships for teams to which the authenticated user
        belongs.

        Use teamId to list memberships for a team, by ID.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yield all team memberships returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            teamId(string_types): List memberships for the team with teamId.
            max(int): Limits the maximum number of memberships returned from
                the Spark service per request.


        Yields:
            TeamMembership: The the next team membership from the Cisco Spark
                query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert teamId is None or isinstance(teamId, string_types)
        assert max is None or isinstance(max, int)
        params = {}
        if teamId:
            params['teamId'] = teamId
        if max:
            params['max'] = max
        # API request - get items
        items = self.session.get_items('team/memberships', params=params)
        # Yield Person objects created from the returned items JSON objects
        for item in items:
            yield TeamMembership(item)

    def create(self, teamId, personId=None, personEmail=None,
               isModerator=False):
        """Add someone to a team by Person ID or email address.

        Add someone to a team by Person ID or email address; optionally making
        them a moderator.

        Args:
            teamId(string_types): ID of the team to which the person will be
                added.
            personId(string_types): ID of the person to be added to the team.
            personEmail(string_types): Email address of the person to be added
                to the team.
            isModerator(bool): If True, adds the person as a moderator for the
                team. If False, adds the person as normal member of the team.

        Returns:
            TeamMembership: With the details of the created team membership.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If neither a personId or personEmail are
                provided.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(teamId, string_types)
        assert personId is None or isinstance(personId, string_types)
        assert personEmail is None or isinstance(personEmail, string_types)
        assert isModerator is None or isinstance(isModerator, bool)
        post_data = {}
        post_data['teamId'] = teamId
        if personId:
            post_data['personId'] = personId
        elif personEmail:
            post_data['personEmail'] = personEmail
        else:
            error_message = "personId or personEmail must be provided to " \
                            "add a person to a team.  Neither were provided."
            raise ciscosparkapiException(error_message)
        post_data['isModerator'] = isModerator
        # API request
        json_obj = self.session.post('team/memberships', json=post_data)
        # Return a TeamMembership object created from the response JSON data
        return TeamMembership(json_obj)

    def get(self, membershipId):
        """Get details for a team membership by ID.

        Args:
            membershipId(string_types): The membershipId of the team
                membership.

        Returns:
            TeamMembership: With the details of the requested team membership.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(membershipId, string_types)
        # API request
        json_obj = self.session.get('team/memberships/'+membershipId)
        # Return a TeamMembership object created from the response JSON data
        return TeamMembership(json_obj)

    def update(self, membershipId, **update_attributes):
        """Update details for a team membership.

        Args:
            membershipId(string_types): The membershipId of the team membership
                to be updated.

        **update_attributes:
            isModerator(bool): If True, sets the person as a moderator for the
                team. If False, removes the person as a moderator for the team.

        Returns:
            TeamMembership: With the updated Spark team membership details.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If an update attribute is not provided.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(membershipId, string_types)
        # Process update_attributes keyword arguments
        if not update_attributes:
            error_message = "At least one **update_attributes keyword " \
                            "argument must be specified."
            raise ciscosparkapiException(error_message)
        # API request
        json_obj = self.session.post('team/memberships/'+membershipId,
                                     json=update_attributes)
        # Return a TeamMembership object created from the response JSON data
        return TeamMembership(json_obj)

    def delete(self, membershipId):
        """Delete a team membership, by ID.

        Args:
            membershipId(string_types): The membershipId of the team membership
                to be deleted.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(membershipId, string_types)
        # API request
        self.session.delete('team/memberships/'+membershipId)
