# -*- coding: utf-8 -*-
"""Cisco Spark People-API wrapper classes.

Classes:
    Person: Models a Spark 'person' JSON object as a native Python object.
    PeopleAPI: Wrappers the Cisco Spark People-API and exposes the API calls as
        Python method calls that return native Python objects.

"""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *

from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.utils import generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


class Person(SparkData):
    """Model a Spark 'person' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Person data object from a JSON dictionary or string.

        Args:
            json(dict, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Person, self).__init__(json)

    @property
    def id(self):
        """The person's unique ID."""
        return self._json.get('id')

    @property
    def emails(self):
        """Email address(es) of the person.

        CURRENT LIMITATION: Spark (today) only allows you to provide a single
        email address for a person. The list data type was selected to enable
        future support for providing multiple email address.

        """
        return self._json['emails']

    @property
    def displayName(self):
        """Full name of the person."""
        return self._json.get('displayName')

    @property
    def firstName(self):
        """First name of the person."""
        return self._json.get('firstName')

    @property
    def lastName(self):
        """Last name of the person."""
        return self._json.get('lastName')

    @property
    def avatar(self):
        """URL to the person's avatar in PNG format."""
        return self._json.get('avatar')

    @property
    def orgId(self):
        """ID of the organization to which this person belongs."""
        return self._json.get('orgId')

    @property
    def roles(self):
        """Roles of the person."""
        return self._json.get('roles')

    @property
    def licenses(self):
        """Licenses allocated to the person."""
        return self._json.get('licenses')

    @property
    def created(self):
        """The date and time the person was created."""
        return self._json.get('created')

    @property
    def status(self):
        """The person's current status."""
        return self._json.get('status')

    @property
    def lastActivity(self):
        """The date and time of the person's last activity."""
        return self._json.get('lastActivity')


class PeopleAPI(object):
    """Cisco Spark People-API wrapper class.

    Wrappers the Cisco Spark People-API and exposes the API calls as Python
    method calls that return native Python objects.

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
        self._session = session

    @generator_container
    def list(self, email=None, displayName=None, max=None):
        """List people

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
            email(str): The e-mail address of the person to be found.
            displayName(str): The complete or beginning portion of
                the displayName to be searched.
            max(int): Limits the maximum number of people returned from the
                Spark service per request.

        Returns:
            GeneratorContainer: When iterated, the GeneratorContainer, yields
                the people returned by the Cisco Spark query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert email is None or isinstance(email, str)
        assert displayName is None or isinstance(displayName, str)
        assert max is None or isinstance(max, int)
        params = {}
        if email:
            params['email'] = email
        elif displayName:
            params['displayName'] = displayName
        if max:
            params['max'] = max
        # API request - get items
        items = self._session.get_items('people', params=params)
        # Yield Person objects created from the returned items JSON objects
        for item in items:
            yield Person(item)

    def create(self, emails, **person_attributes):
        """Create a new user account for a given organization

        Only an admin can create a new user account.

        You must specify displayName and/or firstName and lastName.

        Args:
            emails(list): Email address(es) of the person. (list of strings)
                CURRENT LIMITATION: Spark (today) only allows you to provide a
                single email address for a person. The list data type was
                selected to enable future support for providing multiple email
                address.
            **person_attributes
            displayName(str): Full name of the person
            firstName(str): First name of the person
            lastName(str): Last name of the person
            avatar(str): URL to the person's avatar in PNG format
            orgId(str): ID of the organization to which this
                person belongs
            roles(list): Roles of the person (list of strings containing
                the role IDs to be assigned to the person)
            licenses(list): Licenses allocated to the person (list of
                strings containing the license IDs to be allocated to the
                person)

        Returns:
            Person: With the details of the created person.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If required parameters have been omitted.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(emails, list) and len(emails) == 1
        post_data = {}
        post_data['emails'] = emails
        post_data.update(person_attributes)

        # API request
        json_obj = self._session.post('people', json=post_data)

        # Return a Room object created from the returned JSON object
        return Person(json_obj)

    def update(self, personId, **person_attributes):
        """Update details for a person, by ID.

        Only an admin can update a person details.

        Args:
            personId(str): The ID of the person to be updated.
            **person_attributes
            emails(list): Email address(es) of the person. (list of
                strings) CURRENT LIMITATION: Spark (today) only allows you
                to provide a single email address for a person. The list
                data type was selected to enable future support for
                providing multiple email address.
            displayName(str): Full name of the person
            firstName(str): First name of the person
            lastName(str): Last name of the person
            avatar(str): URL to the person's avatar in PNG format
            orgId(str): ID of the organization to which this
                person belongs
            roles(list): Roles of the person (list of strings containing
                the role IDs to be assigned to the person)
            licenses(list): Licenses allocated to the person (list of
                strings containing the license IDs to be allocated to the
                person)

        Returns:
            Person: With the updated person details.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If an update attribute is not provided.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(personId, str)

        # Process update_attributes keyword arguments
        if not person_attributes:
            error_message = "At least one **update_attributes keyword " \
                            "argument must be specified."
            raise ciscosparkapiException(error_message)

        # API request
        json_obj = self._session.put('people/' + personId,
                                     json=person_attributes)

        # Return a Person object created from the returned JSON object
        return Person(json_obj)

    def get(self, personId):
        """Get person details, by personId.

        Args:
            personId(str): The personID of the person.

        Returns:
            Person: With the details of the requested person.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(personId, str)
        # API request
        json_obj = self._session.get('people/' + personId)
        # Return a Person object created from the response JSON data
        return Person(json_obj)

    def delete(self, personId):
        """Remove a person from the system.

        Only an admin can remove a person.

        Args:
            personId(str): The personID of the person.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(personId, str)
        # API request
        self._session.delete('people/' + personId)

    def me(self):
        """Get the person details of the account accessing the API 'me'.

        Raises:
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # API request
        json_obj = self._session.get('people/me')
        # Return a Person object created from the response JSON data
        return Person(json_obj)
