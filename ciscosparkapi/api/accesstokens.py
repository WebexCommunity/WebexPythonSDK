"""Cisco Spark Access-Tokens-API wrapper classes.

Classes:
    AccessToken: Models a Spark 'access token' JSON object as a native Python
        object.
    AccessTokensAPI: Wrappers the Cisco Spark AccessTokens-API and exposes the
        API calls as Python method calls that return native Python objects.

"""


import urlparse

import requests

from ciscosparkapi.helper import utf8, ERC, validate_base_url, \
    check_response_code, extract_and_parse_json
from ciscosparkapi.sparkdata import SparkData


API_ENDPOINT = u"access_token"


class AccessToken(SparkData):
    """Model a Spark 'access token' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new AccessToken data object from a JSON dictionary or string.

        Args:
            json(dict, unicode, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(AccessToken, self).__init__(json)

    @property
    def access_token(self):
        """Cisco Spark access_token."""
        return self._json.get(u'access_token')

    @property
    def expires_in(self):
        """Access token expires_in number of seconds."""
        return self._json.get(u'expires_in')

    @property
    def refresh_token(self):
        """refresh_token used to request a new/refreshed access_token."""
        return self._json.get(u'refresh_token')

    @property
    def refresh_token_expires_in(self):
        """refresh_token_expires_in number of seconds."""
        return self._json.get(u'refresh_token_expires_in')


class AccessTokensAPI(object):
    """Cisco Spark Access-Tokens-API wrapper class.

    Wrappers the Cisco Spark Access-Tokens-API and exposes the API calls as
    Python method calls that return native Python objects.

    """

    def __init__(self, base_url, timeout=None):
        """Init a new AccessTokensAPI object with the provided RestSession.

        Args:
            base_url(unicode, str): The base URL the API endpoints.
            timeout(int): Timeout in seconds for the API requests.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(base_url, basestring)
        assert timeout is None or isinstance(timeout, int)
        super(AccessTokensAPI, self).__init__()
        self._base_url = validate_base_url(base_url)
        self._timeout = timeout
        self._endpoint_url = urlparse.urljoin(self.base_url, API_ENDPOINT)
        self._request_kwargs = {}
        self._request_kwargs[u"timeout"] = timeout

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
            client_id(unicode, str): Provided when you created your
                integration.
            client_secret(unicode, str): Provided when you created your
                integration.
            code(unicode, str): The Authorization Code provided by the user
                OAuth process.
            redirect_uri(unicode, str): The redirect URI used in the user OAuth
                process.

        Returns:
            AccessToken: With the access token provided by the Cisco Spark
                cloud.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(client_id, basestring)
        assert isinstance(client_secret, basestring)
        assert isinstance(code, basestring)
        assert isinstance(redirect_uri, basestring)
        # Build request parameters
        data = {}
        data[u"grant_type"] = u"authorization_code"
        data[u"client_id"] = utf8(client_id)
        data[u"client_secret"] = utf8(client_secret)
        data[u"code"] = utf8(code)
        data[u"redirect_uri"] = utf8(redirect_uri)
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
            client_id(unicode, str): Provided when you created your
                integration.
            client_secret(unicode, str): Provided when you created your
                integration.
            refresh_token(unicode, str): Provided when you requested the Access
                Token.

        Returns:
            AccessToken: With the access token provided by the Cisco Spark
                cloud.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(client_id, basestring)
        assert isinstance(client_secret, basestring)
        assert isinstance(refresh_token, basestring)
        # Build request parameters
        data = {}
        data[u"grant_type"] = u"refresh_token"
        data[u"client_id"] = utf8(client_id)
        data[u"client_secret"] = utf8(client_secret)
        data[u"refresh_token"] = utf8(refresh_token)
        # API request
        response = requests.post(self._endpoint_url, data=data,
                                 **self._request_kwargs)
        check_response_code(response, ERC['POST'])
        json_data = extract_and_parse_json(response)
        # Return a AccessToken object created from the response JSON data
        return AccessToken(json_data)
