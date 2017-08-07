# -*- coding: utf-8 -*-
"""RestSession class for creating 'connections' to the Cisco Spark APIs."""


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

import logging
import time
import urllib.parse
import warnings

import requests

from ciscosparkapi.exceptions import ciscosparkapiException, SparkApiError
from ciscosparkapi.utils import (
    ERC,
    validate_base_url,
    raise_if_extra_kwargs,
    check_response_code,
    extract_and_parse_json,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


# Module Constants
DEFAULT_SINGLE_REQUEST_TIMEOUT = 20
DEFAULT_RATE_LIMIT_TIMEOUT = 60
RATE_LIMIT_EXCEEDED_RESPONSE_CODE = 429


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
        ciscosparkapiException: If 'next_url' does not contain a valid API
            endpoint URL (scheme, netloc and path).

    """
    next_url = str(next_url)
    parsed_url = urllib.parse.urlparse(next_url)
    if not parsed_url.scheme or not parsed_url.netloc or not parsed_url.path:
        error_message = "'next_url' must be a valid API endpoint URL, " \
                        "minimally containing a scheme, netloc and path."
        raise ciscosparkapiException(error_message)
    if parsed_url.query:
        query_list = parsed_url.query.split('&')
        if 'max=null' in query_list:
            query_list.remove('max=null')
        new_query = '&'.join(query_list)
        parsed_url = list(parsed_url)
        parsed_url[4] = new_query
    return urllib.parse.urlunparse(parsed_url)


class RestSession(object):
    """RESTful HTTP session class for making calls to the Cisco Spark APIs."""

    def __init__(self, access_token, base_url, timeout=None,
                 single_request_timeout=DEFAULT_SINGLE_REQUEST_TIMEOUT,
                 rate_limit_timeout=DEFAULT_RATE_LIMIT_TIMEOUT):
        """Initialize a new RestSession object."""
        super(RestSession, self).__init__()

        # Initialize attributes and properties
        self._base_url = str(validate_base_url(base_url))
        self._access_token = access_token
        self._single_request_timeout = single_request_timeout
        self._rate_limit_timeout = rate_limit_timeout
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
        assert value is None or value > 0
        self._single_request_timeout = value

    @property
    def single_request_timeout(self):
        """The timeout (seconds) for a single HTTP REST API request."""
        return self._single_request_timeout

    @single_request_timeout.setter
    def single_request_timeout(self, value):
        """The timeout (seconds) for a single HTTP REST API request."""
        assert value is None or value > 0
        self._single_request_timeout = value

    @property
    def rate_limit_timeout(self):
        """Maximum time (s) to wait for a response with rate-limit handling."""
        return self._rate_limit_timeout

    @rate_limit_timeout.setter
    def rate_limit_timeout(self, value):
        """Maximum time (s) to wait for a response with rate-limit handling."""
        assert value is None or value > 0
        self._rate_limit_timeout = value

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
        assert isinstance(headers, dict)
        self._req_session.headers.update(headers)

    def abs_url(self, url):
        """Convert a relative URL to an absolute URL.

        Args:
            url(basestring): A relative URL.

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

    def request(self, method, relative_url, erc, **kwargs):
        """Abstract base method for making requests to the Cisco Spark APIs.

        This base method:
            * Expands the relative API endpoint URL to an absolute URL
            * Makes the actual HTTP request to the API endpoint
            * Provides support for Spark rate-limiting
            * Inspects response codes and raises exceptions as appropriate

        Args:
            method(basestring): The request-method type ('GET', 'POST', etc.).
            relative_url(basestring): The relative URL of the API endpoint to
                be called.
            erc(int): The expected response code that should be returned by the
                Cisco Spark API endpoint to indicate success.
            **kwargs: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        logger = logging.getLogger(__name__)

        # Expand the relative API endpoint URL to an absolute URL
        abs_url = self.abs_url(relative_url)

        # Update request kwargs with session defaults
        kwargs.setdefault('timeout', self.single_request_timeout)

        start_time = time.time()
        finish_time = start_time + self.rate_limit_timeout

        while True:
            # Make the HTTP request to the API endpoint
            response = self._req_session.request(method, abs_url, **kwargs)

            try:
                # Check the response code for error conditions
                check_response_code(response, erc)

            except SparkApiError as e:

                # Catch rate-limit errors
                if e.response_code == RATE_LIMIT_EXCEEDED_RESPONSE_CODE \
                        and response.headers.get('Retry-After'):

                    logger.debug("Received a [{}] {} response."
                                 "".format(e.response_code, e.response_text))

                    rate_limit_wait = response.headers['Retry-After']

                    if self.rate_limit_timeout is None:
                        # Retry indefinitely
                        logger.debug("Waiting {:0.3f} seconds. "
                                     "rate_limit_timeout is None; "
                                     "will retry indefinitely."
                                     "".format(rate_limit_wait))
                        time.sleep(rate_limit_wait)
                        continue
                    elif time.time() + rate_limit_wait < finish_time:
                        # Retry if doing so will not exceed the finish time
                        logger.debug("Waiting {:0.3f} seconds. "
                                     "rate_limit_timeout is {:0.3f} seconds, "
                                     "maximum time remaining for this request "
                                     "is {:0.3f} seconds."
                                     "".format(rate_limit_wait,
                                               self.rate_limit_timeout,
                                               finish_time - time.time()))
                        time.sleep(rate_limit_wait)
                        continue
                    else:
                        # Time exceeded re-raise the rate limit SparkApiError
                        raise

                else:
                    # Some other SparkApiError (re-raise)
                    raise

            else:
                # No errors - return the response object
                return response

    def get(self, url, params=None, **kwargs):
        """Sends a GET request.

        Args:
            url(basestring): The relative URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        assert isinstance(url, basestring)
        assert params is None or isinstance(params, dict)

        # Expected response code
        erc = kwargs.pop('erc', ERC['GET'])

        response = self.request('GET', url, erc, params=params, **kwargs)
        return extract_and_parse_json(response)

    def get_pages(self, url, params=None, **kwargs):
        """Return a generator that GETs and yields pages of data.

        Provides native support for RFC5988 Web Linking.

        Args:
            url(basestring): The relative URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        assert isinstance(url, basestring)
        assert params is None or isinstance(params, dict)

        # Expected response code
        erc = kwargs.pop('erc', ERC['GET'])

        # First request
        response = self.request('GET', url, erc, params=params, **kwargs)

        while True:
            yield extract_and_parse_json(response)

            if response.links.get('next'):
                next_url = response.links.get('next').get('url')

                # TODO: Test to see if fix is still needed.
                # Patch for Cisco Spark 'max=null' in next URL bug.
                # url = _fix_next_url(next_url)

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
            url(basestring): The relative URL of the API endpoint.
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
            url(basestring): The relative URL of the API endpoint.
            json: Data to be sent in JSON format in tbe body of the request.
            data: Data to be sent in the body of the request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        assert isinstance(url, basestring)

        # Expected response code
        erc = kwargs.pop('erc', ERC['POST'])

        response = self.request('POST', url, erc, json=json, data=data,
                                **kwargs)
        return extract_and_parse_json(response)

    def put(self, url, json=None, data=None, **kwargs):
        """Sends a PUT request.

        Args:
            url(basestring): The relative URL of the API endpoint.
            json: Data to be sent in JSON format in tbe body of the request.
            data: Data to be sent in the body of the request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        assert isinstance(url, basestring)

        # Expected response code
        erc = kwargs.pop('erc', ERC['PUT'])

        response = self.request('PUT', url, erc, json=json, data=data,
                                **kwargs)
        return extract_and_parse_json(response)

    def delete(self, url, **kwargs):
        """Sends a DELETE request.

        Args:
            url(basestring): The relative URL of the API endpoint.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            SparkApiError: If anything other than the expected response code is
                returned by the Cisco Spark API endpoint.

        """
        assert isinstance(url, basestring)

        # Expected response code
        erc = kwargs.pop('erc', ERC['DELETE'])

        self.request('DELETE', url, erc, **kwargs)
