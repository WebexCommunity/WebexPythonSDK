# -*- coding: utf-8 -*-
"""Cisco Spark Access-Tokens API."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from future import standard_library
standard_library.install_aliases()

from builtins import *
import urllib.parse

from past.builtins import basestring
import requests

from ..response_codes import EXPECTED_RESPONSE_CODE
from ..utils import (
    check_response_code,
    check_type,
    dict_from_items_with_values,
    extract_and_parse_json,
    validate_base_url,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"




API_ENDPOINT = 'access_token'
OBJECT_TYPE = 'access_token'


class AccessTokensAPI(object):
    """Cisco Spark Access-Tokens API.

    Wraps the Cisco Spark Access-Tokens API and exposes the API as native
    Python methods that return native Python objects.

    """

    def __init__(self, base_url, object_factory, timeout=None):
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

        self._object_factory = object_factory

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
            ciscosparkapi.AccessToken: An AccessToken object with the access token provided
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

        # Return a access_token object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

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
        return self._object_factory(OBJECT_TYPE, json_data)
