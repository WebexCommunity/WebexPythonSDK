# -*- coding: utf-8 -*-
"""Cisco Spark Roles API wrapper.

Classes:
    Role: Models a Spark Role JSON object as a native Python object.
    RolesAPI: Wraps the Cisco Spark Roles API and exposes the API as native
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
__role__ = "MIT"


class Role(SparkData):
    """Model a Spark Role JSON object as a native Python object."""

    def __init__(self, json):
        """Initialize a new Role data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Role, self).__init__(json)

    @property
    def id(self):
        """The unique ID for the Role."""
        return self._json_data.get('id')

    @property
    def name(self):
        """The name of the Role."""
        return self._json_data.get('name')


class RolesAPI(object):
    """Cisco Spark Roles API wrapper.

    Wraps the Cisco Spark Roles API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session):
        """Initialize a new RolesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession, may_be_none=False)

        super(RolesAPI, self).__init__()

        self._session = session

    @generator_container
    def list(self, max=None, **request_parameters):
        """List all roles.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all objects returned by the
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
                yields the roles returned by the Cisco Spark query.

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
        items = self._session.get_items('roles', params=params)

        # Yield Role objects created from the returned JSON objects
        for item in items:
            yield Role(item)

    def get(self, roleId):
        """Get the details of a Role, by ID.

        Args:
            roleId(basestring): The ID of the Role to be retrieved.

        Returns:
            Role: A Role object with the details of the requested Role.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(roleId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get('roles/' + roleId)

        # Return a Role object created from the returned JSON object
        return Role(json_data)
