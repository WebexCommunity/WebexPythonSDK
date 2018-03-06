# -*- coding: utf-8 -*-
"""RestSession class for creating 'connections' to the Cisco Spark APIs."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from future import standard_library


standard_library.install_aliases()

from builtins import *
import logging
import time
import urllib.parse
import warnings

from past.builtins import basestring
import requests

from .exceptions import (
    SparkRateLimitError, SparkRateLimitWarning, ciscosparkapiException
)
from .response_codes import EXPECTED_RESPONSE_CODE
from .utils import (
    check_type, check_response_code, extract_and_parse_json, validate_base_url,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


# Module Constants
DEFAULT_SINGLE_REQUEST_TIMEOUT = 60
DEFAULT_WAIT_ON_RATE_LIMIT = True


# Helper Functions
def _fix_next_url(next_url):
    """Remove max=null parameter from URL.

    Patch for Cisco Spark Defect: 'next' URL returned in the Link headers of
    the responses contain an errant 'max=null' parameter, which  causes the
    next request (to this URL) to fail if the URL is requested as-is.

    This patch parses the next_url to remove the max=null parameter.

    Args:
        next_url(basestring): The 'next' URL to be parsed and cleaned.

    Returns:
        basestring: The clean URL to be used for the 'next' request.

    Raises:
        AssertionError: If the parameter types are incorrect.
        ValueError: If 'next_url' does not contain a valid API endpoint URL
            (scheme, netloc and path).

    """
    next_url = str(next_url)
    parsed_url = urllib.parse.urlparse(next_url)

    if not parsed_url.scheme or not parsed_url.netloc or not parsed_url.path:
        raise ValueError(
            "'next_url' must be a valid API endpoint URL, minimally "
            "containing a scheme, netloc and path."
        )

    if parsed_url.query:
        query_list = parsed_url.query.split('&')
        if 'max=null' in query_list:
            query_list.remove('max=null')
            warnings.warn("`max=null` still present in next-URL returned "
                          "from Cisco Spark", RuntimeWarning)
        new_query = '&'.join(query_list)
        parsed_url = list(parsed_url)
        parsed_url[4] = new_query

    return urllib.parse.urlunparse(parsed_url)


# Main module interface
class RestSession(object):
    """RESTful HTTP session class for making calls to the Cisco Spark APIs."""

    def __init__(self, access_token, base_url, timeout=None,
                 single_request_timeout=DEFAULT_SINGLE_REQUEST_TIMEOUT,
                 wait_on_rate_limit=DEFAULT_WAIT_ON_RATE_LIMIT):
        """Initialize a new RestSession object.

        Args:
            access_token(basestring): The Spark access token to be used for
                this session.
            base_url(basestring): The base URL that will be suffixed onto API
                endpoint relative URLs to produce a callable absolute URL.
            timeout: [Deprecated] The timeout (seconds) for an API request.
            single_request_timeout(int): The timeout (seconds) for a single
                HTTP REST API request.
            wait_on_rate_limit(bool): Enable or disable automatic rate-limit
                handling.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(access_token, basestring, may_be_none=False)
        check_type(base_url, basestring, may_be_none=False)
        check_type(timeout, int)
        check_type(single_request_timeout, int)
        check_type(wait_on_rate_limit, bool, may_be_none=False)

        super(RestSession, self).__init__()

        # Initialize attributes and properties
        self._base_url = str(validate_base_url(base_url))
        self._access_token = str(access_token)
        self._single_request_timeout = single_request_timeout
        self._wait_on_rate_limit = wait_on_rate_limit
        if timeout:
            self.timeout = timeout

        # Initialize a new `requests` session
        self._req_session = requests.session()

        # Update the headers of the `requests` session
        self.update_headers({'Authorization': 'Bearer ' + access_token,
                             'Content-type': 'application/json;charset=utf-8'})

    @property
    def base_url(self):
        """The base URL for the API endpoints."""
        return self._base_url

    @property
    def access_token(self):
        """The Cisco Spark access token used for this session."""
        return self._access_token

    @property
    def timeout(self):
        """[Deprecated] The timeout (seconds) for an API request.

        We are deprecating the timeout property in favor of the more
        descriptive single_request_timeout property.

        """
        warnings.warn("The 'timeout' property is being deprecated. Please use "
                      "the 'single_request_timeout' instead.",
                      DeprecationWarning)
        return self._single_request_timeout

    @timeout.setter
    def timeout(self, value):
        """[Deprecated] The timeout (seconds) for an API request.

        We are deprecating the timeout property in favor of the more
        descriptive single_request_timeout property.

        """
        warnings.warn("The 'timeout' property is being deprecated. Please use "
                      "the 'single_request_timeout' instead.",
                      DeprecationWarning)
        check_type(value, int)
        assert value is None or value > 0
        self._single_request_timeout = value

    @property
    def single_request_timeout(self):
        """The timeout (seconds) for a single HTTP REST API request."""
        return self._single_request_timeout

    @single_request_timeout.setter
    def single_request_timeout(self, value):
        """The timeout (seconds) for a single HTTP REST API request."""
        check_type(value, int)
        assert value is None or value > 0
        self._single_request_timeout = value

    @property
    def wait_on_rate_limit(self):
        """Automatic rate-limit handling.

        This setting enables or disables automatic rate-limit handling.  When
        enabled, rate-limited requests will be automatically be retried after
        waiting `Retry-After` seconds (provided by Cisco Spark in the
        rate-limit response header).

        """
        return self._wait_on_rate_limit

    @wait_on_rate_limit.setter
    def wait_on_rate_limit(self, value):
        """Enable or disable automatic rate-limit handling."""
        check_type(value, bool, may_be_none=False)
        self._wait_on_rate_limit = value

    @property
    def headers(self):
        """The HTTP headers used for requests in this session."""
        return self._req_session.headers.copy()

    def update_headers(self, headers):
        """Update the HTTP headers used for requests in this session.

        Note: Updates provided by the dictionary passed as the `headers`
        parameter to this method are merged into the session headers by adding
        new key-value pairs and/or updating the values of existing keys. The
        session headers are not replaced by the provided dictionary.

        Args:
             headers(dict): Updates to the current session headers.

        """
        check_type(headers, dict, may_be_none=False)
        self._req_session.headers.update(headers)

    def abs_url(self, url):
        """Given a relative or absolute URL; return an absolute URL.

        Args:
            url(basestring): A relative or absolute URL.

        Returns:
            str: An absolute URL.

        """
        parsed_url = urllib.parse.urlparse(url)
        if not parsed_url.scheme and not parsed_url.netloc:
            # url is a relative URL; combine with base_url
            return urllib.parse.urljoin(str(self.base_url), str(url))
        else:
            # url is already an absolute URL; return as is
            return url

    def request(self, method, url, erc, **kwargs):
        """Abstract base method for making requests to the Cisco Spark APIs.

        This base method:
            * Expands the API endpoint URL to an absolute URL
            * Makes the actual HTTP request to the API endpoint
            * Provides support for Spark rate-limiting
            * Inspects response codes and raises exceptions as appropriate

        Args:
            method(basestring): The request-method type ('GET', 'POST', etc.).
            url(basestring): The URL of the API endpoint to be called.
            erc(int): The expected response code that should be returned by the
                Cisco Spark API endpoint to indicate success.
            **kwargs: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        # Ensure the url is an absolute URL
        abs_url = self.abs_url(url)

        # Update request kwargs with session defaults
        kwargs.setdefault('timeout', self.single_request_timeout)

        while True:
            # Make the HTTP request to the API endpoint
            response = self._req_session.request(method, abs_url, **kwargs)

            try:
                # Check the response code for error conditions
                check_response_code(response, erc)
            except SparkRateLimitError as e:
                # Catch rate-limit errors
                # Wait and retry if automatic rate-limit handling is enabled
                if self.wait_on_rate_limit:
                    warnings.warn(SparkRateLimitWarning(response))
                    time.sleep(e.retry_after)
                    continue
                else:
                    # Re-raise the SparkRateLimitError
                    raise
            else:
                return response

    def get(self, url, params=None, **kwargs):
        """Sends a GET request.

        Args:
            url(basestring): The URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        check_type(url, basestring, may_be_none=False)
        check_type(params, dict)

        # Expected response code
        erc = kwargs.pop('erc', EXPECTED_RESPONSE_CODE['GET'])

        response = self.request('GET', url, erc, params=params, **kwargs)
        return extract_and_parse_json(response)

    def get_pages(self, url, params=None, **kwargs):
        """Return a generator that GETs and yields pages of data.

        Provides native support for RFC5988 Web Linking.

        Args:
            url(basestring): The URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        check_type(url, basestring, may_be_none=False)
        check_type(params, dict)

        # Expected response code
        erc = kwargs.pop('erc', EXPECTED_RESPONSE_CODE['GET'])

        # First request
        response = self.request('GET', url, erc, params=params, **kwargs)

        while True:
            yield extract_and_parse_json(response)

            if response.links.get('next'):
                next_url = response.links.get('next').get('url')

                # Patch for Cisco Spark 'max=null' in next URL bug.
                # Testing shows that patch is no longer needed; raising a
                # warnning if it is still taking effect;
                # considering for future removal
                next_url = _fix_next_url(next_url)

                # Subsequent requests
                response = self.request('GET', next_url, erc, **kwargs)

            else:
                break

    def get_items(self, url, params=None, **kwargs):
        """Return a generator that GETs and yields individual JSON `items`.

        Yields individual `items` from Cisco Spark's top-level {'items': [...]}
        JSON objects. Provides native support for RFC5988 Web Linking.  The
        generator will request additional pages as needed until all items have
        been returned.

        Args:
            url(basestring): The URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.
            ciscosparkapiException: If the returned response does not contain a
                top-level dictionary with an 'items' key.

        """
        # Get generator for pages of JSON data
        pages = self.get_pages(url, params=params, **kwargs)

        for json_page in pages:
            assert isinstance(json_page, dict)

            items = json_page.get('items')

            if items is None:
                error_message = "'items' key not found in JSON data: " \
                                "{!r}".format(json_page)
                raise ciscosparkapiException(error_message)

            else:
                for item in items:
                    yield item

    def post(self, url, json=None, data=None, **kwargs):
        """Sends a POST request.

        Args:
            url(basestring): The URL of the API endpoint.
            json: Data to be sent in JSON format in tbe body of the request.
            data: Data to be sent in the body of the request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        check_type(url, basestring, may_be_none=False)

        # Expected response code
        erc = kwargs.pop('erc', EXPECTED_RESPONSE_CODE['POST'])

        response = self.request('POST', url, erc, json=json, data=data,
                                **kwargs)
        return extract_and_parse_json(response)

    def put(self, url, json=None, data=None, **kwargs):
        """Sends a PUT request.

        Args:
            url(basestring): The URL of the API endpoint.
            json: Data to be sent in JSON format in tbe body of the request.
            data: Data to be sent in the body of the request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        check_type(url, basestring, may_be_none=False)

        # Expected response code
        erc = kwargs.pop('erc', EXPECTED_RESPONSE_CODE['PUT'])

        response = self.request('PUT', url, erc, json=json, data=data,
                                **kwargs)
        return extract_and_parse_json(response)

    def delete(self, url, **kwargs):
        """Sends a DELETE request.

        Args:
            url(basestring): The URL of the API endpoint.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        check_type(url, basestring, may_be_none=False)

        # Expected response code
        erc = kwargs.pop('erc', EXPECTED_RESPONSE_CODE['DELETE'])

        self.request('DELETE', url, erc, **kwargs)
