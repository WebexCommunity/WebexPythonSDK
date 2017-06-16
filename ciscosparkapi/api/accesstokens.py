# -*- coding: utf-8 -*-
"""Cisco Spark Access-Tokens-API wrapper classes.

Classes:
    AccessToken: Models a Spark 'access token' JSON object as a native Python
        object.
    AccessTokensAPI: Wrappers the Cisco Spark AccessTokens-API and exposes the
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
from future import standard_library
standard_library.install_aliases()

import urllib.parse

import requests

from ciscosparkapi.sparkdata import SparkData
from ciscosparkapi.utils import (
    ERC,
    validate_base_url,
    check_response_code,
    extract_and_parse_json,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


API_ENDPOINT = "access_token"


class AccessToken(SparkData):
    """Model a Spark 'access token' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new AccessToken data object from a JSON dictionary or string.

        Args:
            json(dict, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(AccessToken, self).__init__(json)

    @property
    def access_token(self):
        """Cisco Spark access_token."""
        return self._json.get('access_token')

    @property
    def expires_in(self):
        """Access token expires_in number of seconds."""
        return self._json.get('expires_in')

    @property
    def refresh_token(self):
        """refresh_token used to request a new/refreshed access_token."""
        return self._json.get('refresh_token')

    @property
    def refresh_token_expires_in(self):
        """refresh_token_expires_in number of seconds."""
        return self._json.get('refresh_token_expires_in')


class AccessTokensAPI(object):
    """Cisco Spark Access-Tokens-API wrapper class.

    Wrappers the Cisco Spark Access-Tokens-API and exposes the API calls as
    Python method calls that return native Python objects.

    """

    def __init__(self, base_url, timeout=None):
        """Init a new AccessTokensAPI object with the provided RestSession.

        Args:
            base_url(str): The base URL the API endpoints.
            timeout(int): Timeout in seconds for the API requests.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(base_url, str)
        assert timeout is None or isinstance(timeout, int)
        super(AccessTokensAPI, self).__init__()
        self._base_url = str(validate_base_url(base_url))
        self._timeout = timeout
        self._endpoint_url = urllib.parse.urljoin(self.base_url, API_ENDPOINT)
        self._request_kwargs = {}
        self._request_kwargs["timeout"] = timeout

    @property
    def base_url(self):
        return self._base_url

    @property
    def timeout(self):
        return self._timeout

    def get(self, client_id, client_secret, code, redirect_uri):
        """Exchange an Authorization Code for an Access Token.

        Exchange an Authorization Code for an Access Token that can be used to
        invoke the APIs.

        Args:
            client_id(str): Provided when you created your
                integration.
            client_secret(str): Provided when you created your
                integration.
            code(str): The Authorization Code provided by the user
                OAuth process.
            redirect_uri(str): The redirect URI used in the user OAuth
                process.

        Returns:
            AccessToken: With the access token provided by the Cisco Spark
                cloud.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(client_id, str)
        assert isinstance(client_secret, str)
        assert isinstance(code, str)
        assert isinstance(redirect_uri, str)
        # Build request parameters
        data = {}
        data["grant_type"] = "authorization_code"
        data["client_id"] = client_id
        data["client_secret"] = client_secret
        data["code"] = code
        data["redirect_uri"] = redirect_uri
        # API request
        response = requests.post(self._endpoint_url, data=data,
                                 **self._request_kwargs)
        check_response_code(response, ERC['POST'])
        json_data = extract_and_parse_json(response)
        # Return a AccessToken object created from the response JSON data
        return AccessToken(json_data)

    def refresh(self, client_id, client_secret, refresh_token):
        """Return a refreshed Access Token via the provided refresh_token.

        Args:
            client_id(str): Provided when you created your
                integration.
            client_secret(str): Provided when you created your
                integration.
            refresh_token(str): Provided when you requested the Access
                Token.

        Returns:
            AccessToken: With the access token provided by the Cisco Spark
                cloud.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(client_id, str)
        assert isinstance(client_secret, str)
        assert isinstance(refresh_token, str)
        # Build request parameters
        data = {}
        data["grant_type"] = "refresh_token"
        data["client_id"] = client_id
        data["client_secret"] = client_secret
        data["refresh_token"] = refresh_token
        # API request
        response = requests.post(self._endpoint_url, data=data,
                                 **self._request_kwargs)
        check_response_code(response, ERC['POST'])
        json_data = extract_and_parse_json(response)
        # Return a AccessToken object created from the response JSON data
        return AccessToken(json_data)
