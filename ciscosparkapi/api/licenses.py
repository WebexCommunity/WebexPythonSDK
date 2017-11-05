# -*- coding: utf-8 -*-
"""Cisco Spark Licenses API wrapper.

Classes:
    License: Models a Spark License JSON object as a native Python object.
    LicensesAPI: Wraps the Cisco Spark Licenses API and exposes the API as
        native Python methods that return native Python objects.

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


class License(SparkData):
    """Model a Spark License JSON object as a native Python object."""

    def __init__(self, json):
        """Initialize a License data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(License, self).__init__(json)

    @property
    def id(self):
        """The unique ID for the License."""
        return self._json_data.get('id')

    @property
    def name(self):
        """The name of the License."""
        return self._json_data.get('name')

    @property
    def totalUnits(self):
        """The total number of license units."""
        return self._json_data.get('totalUnits')

    @property
    def consumedUnits(self):
        """The total number of license units consumed."""
        return self._json_data.get('consumedUnits')


class LicensesAPI(object):
    """Cisco Spark Licenses API wrapper.

    Wraps the Cisco Spark Licenses API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session):
        """Initialize a new LicensesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        check_type(session, RestSession, may_be_none=False)

        super(LicensesAPI, self).__init__()

        self._session = session

    @generator_container
    def list(self, orgId=None, max=None, **request_parameters):
        """List all licenses for a given organization.

        If no orgId is specified, the default is the organization of the
        authenticated user.

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
            orgId(basestring): Specify the organization, by ID.
            max(int): Limit the maximum number of items returned from the Spark
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
                yields the licenses returned by the Cisco Spark query.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(orgId, basestring)
        check_type(max, int)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
            max=max,
        )

        # API request - get items
        items = self._session.get_items('licenses', params=params)

        # Yield License objects created from the returned JSON objects
        for item in items:
            yield License(item)

    def get(self, licenseId):
        """Get the details of a License, by ID.

        Args:
            licenseId(basestring): The ID of the License to be retrieved.

        Returns:
            License: A License object with the details of the requested
                License.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(licenseId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get('licenses/' + licenseId)

        # Return a License object created from the returned JSON object
        return License(json_data)
