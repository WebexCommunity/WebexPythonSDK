# -*- coding: utf-8 -*-
"""Cisco Spark People API."""


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


API_ENDPOINT = 'people'
OBJECT_TYPE = 'person'


class PeopleAPI(object):
    """Cisco Spark People API.

    Wraps the Cisco Spark People API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new PeopleAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(PeopleAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, email=None, displayName=None, id=None, orgId=None, max=None,
             **request_parameters):
        """List people

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all people returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            email(basestring): The e-mail address of the person to be found.
            displayName(basestring): The complete or beginning portion of
                the displayName to be searched.
            id(basestring): List people by ID. Accepts up to 85 person IDs
                separated by commas.
            orgId(basestring): The organization ID.
            max(int): Limit the maximum number of items returned from the Spark
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
                yields the people returned by the Cisco Spark query.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(id, basestring)
        check_type(email, basestring)
        check_type(displayName, basestring)
        check_type(orgId, basestring)
        check_type(max, int)

        params = dict_from_items_with_values(
            request_parameters,
            id=id,
            email=email,
            displayName=displayName,
            orgId=orgId,
            max=max,
        )

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield person objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def create(self, emails, displayName=None, firstName=None, lastName=None,
               avatar=None, orgId=None, roles=None, licenses=None,
               **request_parameters):
        """Create a new user account for a given organization

        Only an admin can create a new user account.

        Args:
            emails(list): Email address(es) of the person (list of strings).
            displayName(basestring): Full name of the person.
            firstName(basestring): First name of the person.
            lastName(basestring): Last name of the person.
            avatar(basestring): URL to the person's avatar in PNG format.
            orgId(basestring): ID of the organization to which this
                person belongs.
            roles(list): Roles of the person (list of strings containing
                the role IDs to be assigned to the person).
            licenses(list): Licenses allocated to the person (list of
                strings - containing the license IDs to be allocated to the
                person).
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Person: A Person object with the details of the created person.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(emails, list, may_be_none=False)
        check_type(displayName, basestring)
        check_type(firstName, basestring)
        check_type(lastName, basestring)
        check_type(avatar, basestring)
        check_type(orgId, basestring)
        check_type(roles, list)
        check_type(licenses, list)

        post_data = dict_from_items_with_values(
            request_parameters,
            emails=emails,
            displayName=displayName,
            firstName=firstName,
            lastName=lastName,
            avatar=avatar,
            orgId=orgId,
            roles=roles,
            licenses=licenses,
        )

        # API request
        json_data = self._session.post(API_ENDPOINT, json=post_data)

        # Return a person object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, personId):
        """Get a person's details, by ID.

        Args:
            personId(basestring): The ID of the person to be retrieved.

        Returns:
            Person: A Person object with the details of the requested person.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(personId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get(API_ENDPOINT + '/' + personId)

        # Return a person object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def update(self, personId, emails=None, displayName=None, firstName=None,
               lastName=None, avatar=None, orgId=None, roles=None,
               licenses=None, **request_parameters):
        """Update details for a person, by ID.

        Only an admin can update a person's details.

        Email addresses for a person cannot be changed via the Spark API.

        Include all details for the person. This action expects all user
        details to be present in the request. A common approach is to first GET
        the person's details, make changes, then PUT both the changed and
        unchanged values.

        Args:
            personId(basestring): The person ID.
            emails(list): Email address(es) of the person (list of strings).
            displayName(basestring): Full name of the person.
            firstName(basestring): First name of the person.
            lastName(basestring): Last name of the person.
            avatar(basestring): URL to the person's avatar in PNG format.
            orgId(basestring): ID of the organization to which this
                person belongs.
            roles(list): Roles of the person (list of strings containing
                the role IDs to be assigned to the person).
            licenses(list): Licenses allocated to the person (list of
                strings - containing the license IDs to be allocated to the
                person).
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Person: A Person object with the updated details.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(emails, list)
        check_type(displayName, basestring)
        check_type(firstName, basestring)
        check_type(lastName, basestring)
        check_type(avatar, basestring)
        check_type(orgId, basestring)
        check_type(roles, list)
        check_type(licenses, list)

        put_data = dict_from_items_with_values(
            request_parameters,
            emails=emails,
            displayName=displayName,
            firstName=firstName,
            lastName=lastName,
            avatar=avatar,
            orgId=orgId,
            roles=roles,
            licenses=licenses,
        )

        # API request
        json_data = self._session.put(API_ENDPOINT + '/' + personId,
                                      json=put_data)

        # Return a person object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, personId):
        """Remove a person from the system.

        Only an admin can remove a person.

        Args:
            personId(basestring): The ID of the person to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(personId, basestring, may_be_none=False)

        # API request
        self._session.delete(API_ENDPOINT + '/' + personId)

    def me(self):
        """Get the details of the person accessing the API.

        Raises:
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # API request
        json_data = self._session.get(API_ENDPOINT + '/me')

        # Return a person object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
