# -*- coding: utf-8 -*-
"""Cisco Spark Access-Tokens API wrapper.

Classes:
    AccessToken: Models a Spark 'access token' JSON object as a native Python
        object.
    AccessTokensAPI: Wraps the Cisco Spark Access-Tokens API and exposes the
        API as native Python methods that return native Python objects.

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
from future import standard_library
standard_library.install_aliases()

import urllib.parse

import requests

from ..response_codes import EXPECTED_RESPONSE_CODE
from ..sparkdata import SparkData
from ..utils import (
    check_response_code,
    check_type,
    dict_from_items_with_values,
    extract_and_parse_json,
    validate_base_url,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


API_ENDPOINT = "access_token"


class AccessToken(SparkData):
    """Model a Spark 'access token' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new AccessToken data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(AccessToken, self).__init__(json)

    @property
    def access_token(self):
        """Cisco Spark access token."""
        return self._json_data.get('access_token')

    @property
    def expires_in(self):
        """Access token expiry time (in seconds)."""
        return self._json_data.get('expires_in')

    @property
    def refresh_token(self):
        """Refresh token used to request a new/refreshed access token."""
        return self._json_data.get('refresh_token')

    @property
    def refresh_token_expires_in(self):
        """Refresh token expiry time (in seconds)."""
        return self._json_data.get('refresh_token_expires_in')


class AccessTokensAPI(object):
    """Cisco Spark Access-Tokens API wrapper.

    Wraps the Cisco Spark Access-Tokens API and exposes the API as native
    Python methods that return native Python objects.

    """

    def __init__(self, base_url, timeout=None):
        """Initialize an AccessTokensAPI object with the provided RestSession.

        Args:
            base_url(basestring): The base URL the API endpoints.
            timeout(int): Timeout in seconds for the API requests.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(base_url, basestring, may_be_none=False)
        check_type(timeout, int)

        super(AccessTokensAPI, self).__init__()

        self._base_url = str(validate_base_url(base_url))
        self._timeout = timeout
        self._endpoint_url = urllib.parse.urljoin(self.base_url, API_ENDPOINT)
        self._request_kwargs = {"timeout": timeout}

    @property
    def base_url(self):
        """The base URL the API endpoints."""
        return self._base_url

    @property
    def timeout(self):
        """Timeout in seconds for the API requests."""
        return self._timeout

    def get(self, client_id, client_secret, code, redirect_uri):
        """Exchange an Authorization Code for an Access Token.

        Exchange an Authorization Code for an Access Token that can be used to
        invoke the APIs.

        Args:
            client_id(basestring): Provided when you created your integration.
            client_secret(basestring): Provided when you created your
                integration.
            code(basestring): The Authorization Code provided by the user
                OAuth process.
            redirect_uri(basestring): The redirect URI used in the user OAuth
                process.

        Returns:
            AccessToken: An AccessToken object with the access token provided
                by the Cisco Spark cloud.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(client_id, basestring, may_be_none=False)
        check_type(client_secret, basestring, may_be_none=False)
        check_type(code, basestring, may_be_none=False)
        check_type(redirect_uri, basestring, may_be_none=False)

        post_data = dict_from_items_with_values(
            grant_type="authorization_code",
            client_id=client_id,
            client_secret=client_secret,
            code=code,
            redirect_uri=redirect_uri,
        )

        # API request
        response = requests.post(self._endpoint_url, data=post_data,
                                 **self._request_kwargs)
        check_response_code(response, EXPECTED_RESPONSE_CODE['POST'])
        json_data = extract_and_parse_json(response)

        # Return a AccessToken object created from the response JSON data
        return AccessToken(json_data)

    def refresh(self, client_id, client_secret, refresh_token):
        """Return a refreshed Access Token from the provided refresh_token.

        Args:
            client_id(basestring): Provided when you created your integration.
            client_secret(basestring): Provided when you created your
                integration.
            refresh_token(basestring): Provided when you requested the Access
                Token.

        Returns:
            AccessToken: With the access token provided by the Cisco Spark
                cloud.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(client_id, basestring, may_be_none=False)
        check_type(client_secret, basestring, may_be_none=False)
        check_type(refresh_token, basestring, may_be_none=False)

        post_data = dict_from_items_with_values(
            grant_type="refresh_token",
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
        )

        # API request
        response = requests.post(self._endpoint_url, data=post_data,
                                 **self._request_kwargs)
        check_response_code(response, EXPECTED_RESPONSE_CODE['POST'])
        json_data = extract_and_parse_json(response)

        # Return a AccessToken object created from the response JSON data
        return AccessToken(json_data)
