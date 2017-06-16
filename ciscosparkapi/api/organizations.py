# -*- coding: utf-8 -*-
"""Cisco Spark Organizations API wrapper.

Classes:
    Organization: Models a Spark Organization JSON object as a native Python
        object.
    OrganizationsAPI: Wraps the Cisco Spark Organizations API and exposes the
        API calls as Python method calls that return native Python objects.

"""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *

from ciscosparkapi.utils import generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


class Organization(SparkData):
    """Model a Spark Organization JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Organization data object from a dict or JSON string.

        Args:
            json(dict, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Organization, self).__init__(json)

    @property
    def id(self):
        """The unique id for the Organization."""
        return self._json.get('id')

    @property
    def displayName(self):
        """The human-friendly display name of the Organization."""
        return self._json.get('displayName')

    @property
    def created(self):
        """The date and time the Organization was created."""
        return self._json.get('created')


class OrganizationsAPI(object):
    """Cisco Spark Organizations API wrapper.

    Wraps the Cisco Spark Organizations API and exposes the API calls as Python
    method calls that return native Python objects.

    """

    def __init__(self, session):
        """Init a new OrganizationsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(session, RestSession)
        super(OrganizationsAPI, self).__init__()
        self._session = session

    @generator_container
    def list(self, max=None):
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
            max(int): Limits the maximum number of entries returned from the
                Spark service per request (page size; requesting additional
                pages is handled automatically).

        Returns:
            GeneratorContainer: When iterated, the GeneratorContainer, yields
                the objects returned from the Cisco Spark query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert max is None or isinstance(max, int)
        params = {}
        if max:
            params['max'] = max
        # API request - get items
        items = self._session.get_items('organizations', params=params)
        # Yield Organization objects created from the returned JSON objects
        for item in items:
            yield Organization(item)

    def get(self, orgId):
        """Get the details of an Organization, by id.

        Args:
            orgId(str): The id of the Organization.

        Returns:
            Organization: With the details of the requested Organization.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(orgId, str)
        # API request
        json_obj = self._session.get('organizations/' + orgId)
        # Return a Organization object created from the returned JSON object
        return Organization(json_obj)
