# -*- coding: utf-8 -*-
"""Cisco Spark Organizations API wrapper.

Classes:
    Organization: Models a Spark Organization JSON object as a native Python
        object.
    OrganizationsAPI: Wraps the Cisco Spark Organizations API and exposes the
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


class Organization(SparkData):
    """Model a Spark Organization JSON object as a native Python object."""

    def __init__(self, json):
        """Init a Organization data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Organization, self).__init__(json)

    @property
    def id(self):
        """The unique ID for the Organization."""
        return self._json_data.get('id')

    @property
    def displayName(self):
        """The human-friendly display name of the Organization."""
        return self._json_data.get('displayName')

    @property
    def created(self):
        """Creation date and time in ISO8601 format."""
        return self._json_data.get('created')


class OrganizationsAPI(object):
    """Cisco Spark Organizations API wrapper.

    Wraps the Cisco Spark Organizations API and exposes the API as native
    Python methods that return native Python objects.

    """

    def __init__(self, session):
        """Init a new OrganizationsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession, may_be_none=False)

        super(OrganizationsAPI, self).__init__()

        self._session = session

    @generator_container
    def list(self, max=None, **request_parameters):
        """List Organizations.

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
                yields the organizations returned by the Cisco Spark query.

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
        items = self._session.get_items('organizations', params=params)

        # Yield Organization objects created from the returned JSON objects
        for item in items:
            yield Organization(item)

    def get(self, orgId):
        """Get the details of an Organization, by ID.

        Args:
            orgId(basestring): The ID of the Organization to be retrieved.

        Returns:
            Organization: An Organization object with the details of the
                requested organization.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(orgId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get('organizations/' + orgId)

        # Return a Organization object created from the returned JSON object
        return Organization(json_data)
