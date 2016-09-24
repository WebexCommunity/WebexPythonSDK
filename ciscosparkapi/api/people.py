# -*- coding: utf-8 -*-
"""Cisco Spark People-API wrapper classes.

Classes:
    Person: Models a Spark 'person' JSON object as a native Python object.
    PeopleAPI: Wrappers the Cisco Spark People-API and exposes the API calls as
        Python method calls that return native Python objects.

"""


from builtins import object
from six import string_types

from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.helper import generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData


class Person(SparkData):
    """Model a Spark 'person' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Person data object from a JSON dictionary or string.

        Args:
            json(dict, string_types): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Person, self).__init__(json)

    @property
    def id(self):
        return self._json['id']

    @property
    def emails(self):
        return self._json['emails']

    @property
    def displayName(self):
        return self._json['displayName']

    @property
    def avatar(self):
        return self._json['avatar']

    @property
    def created(self):
        return self._json['created']

    @property
    def lastActivity(self):
        return self._json['lastActivity']

    @property
    def status(self):
        return self._json['status']


class PeopleAPI(object):
    """Cisco Spark People-API wrapper class.

    Wrappers the Cisco Spark People-API and exposes the API calls as Python
    method calls that return native Python objects.

    Attributes:
        session(RestSession): The RESTful session object to be used for API
            calls to the Cisco Spark service.

    """

    def __init__(self, session):
        """Init a new PeopleAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(session, RestSession)
        super(PeopleAPI, self).__init__()
        self.session = session

    @generator_container
    def list(self, email=None, displayName=None, max=None):
        """List people by email or displayName.

        An email address or displayName must be provided.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yield all people returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            email(string_types): The e-mail address of the person to be found.
            displayName(string_types): The complete or beginning portion of
                the displayName to be searched.
            max(int): Limits the maximum number of people returned from the
                Spark service per request.

        Yields:
            Person: The the next person from the Cisco Spark query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If neither an email or displayName argument
                is specified.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert email is None or isinstance(email, string_types)
        assert displayName is None or isinstance(displayName, string_types)
        assert max is None or isinstance(max, int)
        params = {}
        if email:
            params['email'] = email
        elif displayName:
            params['displayName'] = displayName
        else:
            error_message = "An email or displayName argument must be " \
                            "specified."
            raise ciscosparkapiException(error_message)
        if max:
            params['max'] = max
        # API request - get items
        items = self.session.get_items('people', params=params)
        # Yield Person objects created from the returned items JSON objects
        for item in items:
            yield Person(item)

    def get(self, personId):
        """Get person details, by personId.

        Args:
            personId(string_types): The personID of the person.

        Returns:
            Person: With the details of the requested person.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(personId, string_types)
        # API request
        json_obj = self.session.get('people/'+personId)
        # Return a Person object created from the response JSON data
        return Person(json_obj)

    def me(self):
        """Get the person details of the account accessing the API 'me'.

        Raises:
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # API request
        json_obj = self.session.get('people/me')
        # Return a Person object created from the response JSON data
        return Person(json_obj)
