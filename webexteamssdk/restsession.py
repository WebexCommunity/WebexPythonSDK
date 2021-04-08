# -*- coding: utf-8 -*-
"""RestSession class for creating connections to the Webex Teams APIs.

Copyright (c) 2016-2020 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from future import standard_library
standard_library.install_aliases()

import json
import logging
import platform
import sys
import time
import urllib
import urllib.parse
import warnings

import requests
from past.builtins import basestring

from ._metadata import __title__, __version__
from .config import DEFAULT_SINGLE_REQUEST_TIMEOUT, DEFAULT_WAIT_ON_RATE_LIMIT
from .exceptions import MalformedResponse, RateLimitError, RateLimitWarning
from .response_codes import EXPECTED_RESPONSE_CODE
from .utils import (
    check_response_code, check_type, extract_and_parse_json, validate_base_url,
)


logger = logging.getLogger(__name__)


# Helper Functions
def _fix_next_url(next_url):
    """Remove max=null parameter from URL.

    Patch for Webex Teams Defect: "next" URL returned in the Link headers of
    the responses contain an errant "max=null" parameter, which  causes the
    next request (to this URL) to fail if the URL is requested as-is.

    This patch parses the next_url to remove the max=null parameter.

    Args:
        next_url(basestring): The "next" URL to be parsed and cleaned.

    Returns:
        basestring: The clean URL to be used for the "next" request.

    Raises:
        AssertionError: If the parameter types are incorrect.
        ValueError: If "next_url" does not contain a valid API endpoint URL
            (scheme, netloc and path).

    """
    next_url = str(next_url)
    parsed_url = urllib.parse.urlparse(next_url)

    if not parsed_url.scheme or not parsed_url.netloc or not parsed_url.path:
        raise ValueError(
            "`next_url` must be a valid API endpoint URL, minimally "
            "containing a scheme, netloc and path."
        )

    if parsed_url.query:
        query_list = parsed_url.query.split("&")
        if "max=null" in query_list:
            query_list.remove("max=null")
            warnings.warn("`max=null` still present in next-URL returned "
                          "from Webex Teams", RuntimeWarning)
        new_query = "&".join(query_list)
        parsed_url = list(parsed_url)
        parsed_url[4] = new_query

    return urllib.parse.urlunparse(parsed_url)


def user_agent(be_geo_id=None, caller=None):
    """Build a User-Agent HTTP header string."""

    product = __title__
    version = __version__

    # Add platform data to comment portion of the User-Agent header.
    # Inspired by PIP"s User-Agent header; serialize the data in JSON format.
    # https://github.com/pypa/pip/blob/master/src/pip/_internal/network
    data = dict()

    # Python implementation
    data["implementation"] = {
        "name": platform.python_implementation(),
    }

    # Implementation version
    if data["implementation"]["name"] == "CPython":
        data["implementation"]["version"] = platform.python_version()

    elif data["implementation"]["name"] == "PyPy":
        if sys.pypy_version_info.releaselevel == "final":
            pypy_version_info = sys.pypy_version_info[:3]
        else:
            pypy_version_info = sys.pypy_version_info
        data["implementation"]["version"] = ".".join(
            [str(x) for x in pypy_version_info]
        )
    elif data["implementation"]["name"] == "Jython":
        data["implementation"]["version"] = platform.python_version()
    elif data["implementation"]["name"] == "IronPython":
        data["implementation"]["version"] = platform.python_version()

    # Platform information
    if sys.platform.startswith("darwin") and platform.mac_ver()[0]:
        dist = {"name": "macOS", "version": platform.mac_ver()[0]}
        data["distro"] = dist

    if platform.system():
        data.setdefault("system", {})["name"] = platform.system()

    if platform.release():
        data.setdefault("system", {})["release"] = platform.release()

    if platform.machine():
        data["cpu"] = platform.machine()

    data["organization"] = {}
    
    # Add self-identified organization information to the User-Agent Header.
    if be_geo_id:
        data["organization"]["be_geo_id"] = be_geo_id

    if caller:
        data["organization"]["caller"] = caller

    # Create the User-Agent string
    user_agent_string = "{product}/{version} {comment}".format(
        product=product,
        version=version,
        comment=json.dumps(data),
    )

    logger.info("User-Agent: " + user_agent_string)

    return user_agent_string


# Main module interface
class RestSession(object):
    """RESTful HTTP session class for making calls to the Webex Teams APIs."""

    def __init__(self, access_token, base_url,
                 single_request_timeout=DEFAULT_SINGLE_REQUEST_TIMEOUT,
                 wait_on_rate_limit=DEFAULT_WAIT_ON_RATE_LIMIT,
                 proxies=None,
                 be_geo_id=None,
                 caller=None,
                 disable_ssl_verify=False):
        """Initialize a new RestSession object.

        Args:
            access_token(basestring): The Webex Teams access token to be used
                for this session.
            base_url(basestring): The base URL that will be suffixed onto API
                endpoint relative URLs to produce a callable absolute URL.
            single_request_timeout(int): The timeout (seconds) for a single
                HTTP REST API request.
            wait_on_rate_limit(bool): Enable or disable automatic rate-limit
                handling.
            proxies(dict): Dictionary of proxies passed on to the requests
                session.
            be_geo_id(basestring): Optional partner identifier for API usage
                tracking.  Defaults to checking for a BE_GEO_ID environment
                variable.
            caller(basestring): Optional  identifier for API usage tracking.
                Defaults to checking for a WEBEX_PYTHON_SDK_CALLER environment
                variable.
            disable_ssl_verify(bool): Optional boolean flag to disable ssl
                verification. Defaults to False. If set to true, the requests
                session won't verify ssl certs anymore.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(access_token, basestring)
        check_type(base_url, basestring)
        check_type(single_request_timeout, int, optional=True)
        check_type(wait_on_rate_limit, bool)
        check_type(proxies, dict, optional=True)
        check_type(disable_ssl_verify, bool, optional=True)

        super(RestSession, self).__init__()

        # Initialize attributes and properties
        self._base_url = str(validate_base_url(base_url))
        self._access_token = str(access_token)
        self._single_request_timeout = single_request_timeout
        self._wait_on_rate_limit = wait_on_rate_limit

        # Initialize a new session
        self._req_session = requests.session()

        # Disable ssl cert verification if chosen by user
        if disable_ssl_verify:
            self._req_session.verify = False


        if proxies is not None:
            self._req_session.proxies.update(proxies)

        # Update the HTTP headers for the session
        self.update_headers({
            "Authorization": "Bearer " + access_token,
            "Content-type": "application/json;charset=utf-8",
            "User-Agent": user_agent(be_geo_id=be_geo_id, caller=caller),
        })

    @property
    def base_url(self):
        """The base URL for the API endpoints."""
        return self._base_url

    @property
    def access_token(self):
        """The Webex Teams access token used for this session."""
        return self._access_token

    @property
    def single_request_timeout(self):
        """The timeout (seconds) for a single HTTP REST API request."""
        return self._single_request_timeout

    @single_request_timeout.setter
    def single_request_timeout(self, value):
        """The timeout (seconds) for a single HTTP REST API request."""
        check_type(value, int, optional=True)
        if value is not None and value <= 0:
            raise ValueError("single_request_timeout must be positive integer")
        self._single_request_timeout = value

    @property
    def wait_on_rate_limit(self):
        """Automatic rate-limit handling.

        This setting enables or disables automatic rate-limit handling.  When
        enabled, rate-limited requests will be automatically be retried after
        waiting `Retry-After` seconds (provided by Webex Teams in the
        rate-limit response header).

        """
        return self._wait_on_rate_limit

    @wait_on_rate_limit.setter
    def wait_on_rate_limit(self, value):
        """Enable or disable automatic rate-limit handling."""
        check_type(value, bool)
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
        check_type(headers, dict)
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
        """Abstract base method for making requests to the Webex Teams APIs.

        This base method:
            * Expands the API endpoint URL to an absolute URL
            * Makes the actual HTTP request to the API endpoint
            * Provides support for Webex Teams rate-limiting
            * Inspects response codes and raises exceptions as appropriate

        Args:
            method(basestring): The request-method type ("GET", "POST", etc.).
            url(basestring): The URL of the API endpoint to be called.
            erc(int): The expected response code that should be returned by the
                Webex Teams API endpoint to indicate success.
            **kwargs: Passed on to the requests package.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        # Ensure the url is an absolute URL
        abs_url = self.abs_url(url)

        # Update request kwargs with session defaults
        kwargs.setdefault("timeout", self.single_request_timeout)

        while True:
            # Make the HTTP request to the API endpoint
            response = self._req_session.request(method, abs_url, **kwargs)

            try:
                # Check the response code for error conditions
                check_response_code(response, erc)
            except RateLimitError as e:
                # Catch rate-limit errors
                # Wait and retry if automatic rate-limit handling is enabled
                if self.wait_on_rate_limit:
                    warnings.warn(RateLimitWarning(response))
                    time.sleep(e.retry_after)
                    continue
                else:
                    # Re-raise the RateLimitError
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
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, basestring)
        check_type(params, dict, optional=True)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["GET"])

        response = self.request("GET", url, erc, params=params, **kwargs)
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
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, basestring)
        check_type(params, dict, optional=True)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["GET"])

        # First request
        response = self.request("GET", url, erc, params=params, **kwargs)

        while True:
            yield extract_and_parse_json(response)

            if response.links.get("next"):
                next_url = response.links.get("next").get("url")

                # Patch for Webex Teams "max=null" in next URL bug.
                # Testing shows that patch is no longer needed; raising a
                # warnning if it is still taking effect;
                # considering for future removal
                next_url = _fix_next_url(next_url)

                # Subsequent requests
                response = self.request("GET", next_url, erc, **kwargs)

            else:
                break

    def get_items(self, url, params=None, **kwargs):
        """Return a generator that GETs and yields individual JSON `items`.

        Yields individual `items` from Webex Teams"s top-level {"items": [...]}
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
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.
            MalformedResponse: If the returned response does not contain a
                top-level dictionary with an "items" key.

        """
        # Get generator for pages of JSON data
        pages = self.get_pages(url, params=params, **kwargs)

        for json_page in pages:
            assert isinstance(json_page, dict)

            items = json_page.get("items")

            if items is None:
                error_message = "'items' key not found in JSON data: " \
                                "{!r}".format(json_page)
                raise MalformedResponse(error_message)

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
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, basestring)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["POST"])

        response = self.request("POST", url, erc, json=json, data=data,
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
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, basestring)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["PUT"])

        response = self.request("PUT", url, erc, json=json, data=data,
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
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, basestring)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["DELETE"])

        self.request("DELETE", url, erc, **kwargs)
