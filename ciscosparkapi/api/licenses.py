# -*- coding: utf-8 -*-
"""Cisco Spark Licenses API wrapper.

Classes:
    License: Models a Spark License JSON object as a native Python object.
    LicensesAPI: Wraps the Cisco Spark Licenses API and exposes the
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


class License(SparkData):
    """Model a Spark License JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new License data object from a dict or JSON string.

        Args:
            json(dict, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(License, self).__init__(json)

    @property
    def id(self):
        """The unique id for the License."""
        return self._json.get('id')

    @property
    def name(self):
        """The name of the License."""
        return self._json.get('name')

    @property
    def totalUnits(self):
        """The total number of license units."""
        return self._json.get('totalUnits')

    @property
    def consumedUnits(self):
        """The total number of license units consumed."""
        return self._json.get('consumedUnits')


class LicensesAPI(object):
    """Cisco Spark Licenses API wrapper.

    Wraps the Cisco Spark Licenses API and exposes the API calls as Python
    method calls that return native Python objects.

    """

    def __init__(self, session):
        """Init a new LicensesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(session, RestSession)
        super(LicensesAPI, self).__init__()
        self._session = session

    @generator_container
    def list(self, orgId=None, max=None):
        """List Licenses.

        Optionally filtered by Organization (orgId parameter).

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
            orgId(str): Filters the returned licenses to only include
                those liceses associated with the specified Organization
                (orgId).
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
        assert orgId is None or isinstance(orgId, str)
        assert max is None or isinstance(max, int)
        params = {}
        if orgId:
            params['orgId'] = orgId
        if max:
            params['max'] = max
        # API request - get items
        items = self._session.get_items('licenses', params=params)
        # Yield License objects created from the returned JSON objects
        for item in items:
            yield License(item)

    def get(self, licenseId):
        """Get the details of a License, by id.

        Args:
            licenseId(str): The id of the License.

        Returns:
            License: With the details of the requested License.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(licenseId, str)
        # API request
        json_obj = self._session.get('licenses/' + licenseId)
        # Return a License object created from the returned JSON object
        return License(json_obj)
