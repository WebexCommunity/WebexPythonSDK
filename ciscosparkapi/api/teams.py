"""Cisco Spark Teams-API wrapper classes.

Classes:
    Team: Models a Spark 'team' JSON object as a native Python object.
    TeamsAPI: Wrappers the Cisco Spark Teams-API and exposes the API calls as
        Python method calls that return native Python objects.

"""


from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.helper import utf8, generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData


class Team(SparkData):
    """Model a Spark 'team' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Team data object from a JSON dictionary or string.

        Args:
            json(dict, unicode, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Team, self).__init__(json)

    @property
    def id(self):
        return self._json[u'id']

    @property
    def name(self):
        return self._json[u'name']

    @property
    def created(self):
        return self._json[u'created']


class TeamsAPI(object):
    """Cisco Spark Teams-API wrapper class.

    Wrappers the Cisco Spark Teams-API and exposes the API calls as Python
    method calls that return native Python objects.

    Attributes:
        session(RestSession): The RESTful session object to be used for API
            calls to the Cisco Spark service.

    """

    def __init__(self, session):
        """Init a new TeamsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(session, RestSession)
        super(TeamsAPI, self).__init__()
        self.session = session

    @generator_container
    def list(self, max=None):
        """List teams to which the authenticated user belongs.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yield all teams returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            max(int): Limits the maximum number of teams returned from the
                Spark service per request.

        Yields:
            Team: The the next team from the Cisco Spark query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert max is None or isinstance(max, int)
        params = {}
        if max:
            params[u'max'] = max
        # API request - get items
        items = self.session.get_items('teams', params=params)
        # Yield Team objects created from the returned items JSON objects
        for item in items:
            yield Team(item)

    def create(self, name):
        """Create a team.

        The authenticated user is automatically added as a member of the team.

        Args:
            name(unicode, str): A user-friendly name for the team.

        Returns:
            Team: With the details of the created team.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(name, basestring)
        post_data = {}
        post_data[u'name'] = utf8(name)
        # API request
        json_obj = self.session.post('teams', json=post_data)
        # Return a Team object created from the response JSON data
        return Team(json_obj)

    def get(self, teamId):
        """Get the details of a team, by ID.

        Args:
            teamId(unicode, str): The teamId of the team.

        Returns:
            Team: With the details of the requested team.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(teamId, basestring)
        # API request
        json_obj = self.session.get('teams/'+teamId)
        # Return a Team object created from the response JSON data
        return Team(json_obj)

    def update(self, teamId, **update_attributes):
        """Update details for a team.

        Args:
            teamId(unicode, str): The teamId of the team to be updated.

        **update_attributes:
            name(unicode, str): A user-friendly name for the team.

        Returns:
            Team: With the updated Spark team details.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If an update attribute is not provided.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(teamId, basestring)
        # Process update_attributes keyword arguments
        if not update_attributes:
            error_message = "At least one **update_attributes keyword " \
                            "argument must be specified."
            raise ciscosparkapiException(error_message)
        put_data = {}
        for param, value in update_attributes.items():
            if isinstance(value, basestring):
                value = utf8(value)
            put_data[utf8(param)] = value
        # API request
        json_obj = self.session.post('teams/'+teamId, json=put_data)
        # Return a Team object created from the response JSON data
        return Team(json_obj)

    def delete(self, teamId):
        """Delete a team.

        Args:
            teamId(unicode, str): The teamId of the team to be deleted.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(teamId, basestring)
        # API request
        self.session.delete('teams/'+teamId)
