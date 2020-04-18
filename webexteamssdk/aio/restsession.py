# -*- coding: utf-8 -*-
"""RestSession class for creating connections to the Webex Teams APIs.

Copyright (c) 2016-2019 Cisco and/or its affiliates.

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

import time
import urllib.parse
import warnings
from builtins import *

import aiohttp
import asyncio

from webexteamssdk.config import (
    DEFAULT_SINGLE_REQUEST_TIMEOUT,
    DEFAULT_WAIT_ON_RATE_LIMIT,
)
from webexteamssdk.exceptions import MalformedResponse
from webexteamssdk.aio.exceptions import (
    AsyncRateLimitError,
    AsyncRateLimitWarning,
    prepare_async_api_error,
)

from webexteamssdk.response_codes import EXPECTED_RESPONSE_CODE
from webexteamssdk.aio.utils import (
    async_check_response_code,
    check_type,
    async_extract_and_parse_json,
    validate_base_url,
)


async def on_request_start(session, trace_config_ctx, params):
    print("Starting request")
    print(trace_config_ctx.trace_request_ctx)


async def on_request_end(session, trace_config_ctx, params):
    print("Ending request")


trace_config = aiohttp.TraceConfig()
trace_config.on_request_start.append(on_request_start)
trace_config.on_request_end.append(on_request_end)

# Helper Functions
def _fix_next_url(next_url: str) -> str:
    """Remove max=null parameter from URL.

    Patch for Webex Teams Defect: 'next' URL returned in the Link headers of
    the responses contain an errant 'max=null' parameter, which  causes the
    next request (to this URL) to fail if the URL is requested as-is.

    This patch parses the next_url to remove the max=null parameter.

    Args:
        next_url(str): The 'next' URL to be parsed and cleaned.

    Returns:
        str: The clean URL to be used for the 'next' request.

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
        query_list = parsed_url.query.split("&")
        if "max=null" in query_list:
            query_list.remove("max=null")
            warnings.warn(
                "`max=null` still present in next-URL returned " "from Webex Teams",
                RuntimeWarning,
            )
        new_query = "&".join(query_list)
        parsed_url = list(parsed_url)
        parsed_url[4] = new_query

    return urllib.parse.urlunparse(parsed_url)


# Main module interface
class AsyncRestSession:
    """RESTful HTTP session class for making calls to the Webex Teams APIs."""

    def __init__(
        self,
        access_token,
        base_url,
        single_request_timeout=DEFAULT_SINGLE_REQUEST_TIMEOUT,
        wait_on_rate_limit=DEFAULT_WAIT_ON_RATE_LIMIT,
        proxies=None,
    ):
        """Initialize a new RestSession object.

        Args:
            access_token(str): The Webex Teams access token to be used
                for this session.
            base_url(str): The base URL that will be suffixed onto API
                endpoint relative URLs to produce a callable absolute URL.
            single_request_timeout(int): The timeout (seconds) for a single
                HTTP REST API request.
            wait_on_rate_limit(bool): Enable or disable automatic rate-limit
                handling.
            proxies(dict): Dictionary of proxies passed on to the requests
                session.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(access_token, str)
        check_type(base_url, str)
        check_type(single_request_timeout, int, optional=True)
        check_type(wait_on_rate_limit, bool)
        check_type(proxies, dict, optional=True)

        super().__init__()

        # Initialize attributes and properties
        self._base_url = str(validate_base_url(base_url))
        self._access_token = str(access_token)
        self._single_request_timeout = single_request_timeout
        self._wait_on_rate_limit = wait_on_rate_limit

        # Initialize a new `requests` session
        self._req_session = aiohttp.ClientSession(
            trace_configs=[trace_config],
            timeout=aiohttp.ClientTimeout(total=single_request_timeout),
        )

        if proxies is not None:
            if "https" in proxies.keys():
                self.proxy = proxies["https"]
            elif (
                "http" in proxies.keys()
            ):  # use the http proxy as fallback, even for https
                self.proxy = proxies["http"]
        else:
            self.proxy = None

        self.update_headers(
            {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json;charset=utf-8",
            }
        )

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
        return self._req_session._default_headers.copy()

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
        self._req_session._default_headers.update(headers)

    def abs_url(self, url):
        """Given a relative or absolute URL; return an absolute URL.

        Args:
            url(str): A relative or absolute URL.

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

    async def request(self, method, url, erc, **kwargs) -> aiohttp.ClientResponse:
        """Abstract base method for making requests to the Webex Teams APIs.

        This base method:
            * Expands the API endpoint URL to an absolute URL
            * Makes the actual HTTP request to the API endpoint
            * Provides support for Webex Teams rate-limiting
            * Inspects response codes and raises exceptions as appropriate

        Args:
            method(str): The request-method type ('GET', 'POST', etc.).
            url(str): The URL of the API endpoint to be called.
            erc(int): The expected response code that should be returned by the
                Webex Teams API endpoint to indicate success.
            **kwargs: Passed on to the requests package.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        # Ensure the url is an absolute URL
        abs_url = self.abs_url(url)

        while True:
            # Make the HTTP request to the API endpoint
            response = await self._req_session.request(
                method, abs_url, proxy=self.proxy, **kwargs
            )

            try:
                # Check the response code for error conditions
                await async_check_response_code(response, erc)
            except AsyncRateLimitError as e:
                # Catch rate-limit errors
                # Wait and retry if automatic rate-limit handling is enabled
                if self.wait_on_rate_limit:
                    warnings.warn(AsyncRateLimitWarning(response))
                    await asyncio.sleep(e.retry_after)
                    continue
                else:
                    # Re-raise the RateLimitError
                    raise
            else:
                return response

    async def get(self, url, params=None, **kwargs):
        """Sends a GET request.

        Args:
            url(str): The URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            erc(int): The expected (success) response code for the request.
            **kwargs:
                others: Passed on to the requests package.

        Raises:
            AsyncApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, str)
        check_type(params, dict, optional=True)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["GET"])

        response = await self.request("GET", url, erc, params=params, **kwargs)
        return await async_extract_and_parse_json(response)

    async def get_pages(self, url, params=None, **kwargs):
        """Return a generator that GETs and yields pages of data.

        Provides native support for RFC5988 Web Linking.

        Args:
            url(str): The URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, str)
        check_type(params, dict, optional=True)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["GET"])

        # First request
        response = await self.request("GET", url, erc, params=params, **kwargs)

        while True:
            yield await async_extract_and_parse_json(response)

            if response.links.get("next"):
                next_url = response.links.get("next").get("url")

                # Patch for Webex Teams 'max=null' in next URL bug.
                # Testing shows that patch is no longer needed; raising a
                # warnning if it is still taking effect;
                # considering for future removal
                next_url = _fix_next_url(next_url)

                # Subsequent requests
                response = await self.request("GET", next_url, erc, **kwargs)

            else:
                break

    async def get_items(self, url, params=None, **kwargs):
        """Return a generator that GETs and yields individual JSON `items`.

        Yields individual `items` from Webex Teams's top-level {'items': [...]}
        JSON objects. Provides native support for RFC5988 Web Linking.  The
        generator will request additional pages as needed until all items have
        been returned.

        Args:
            url(str): The URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.
            MalformedResponse: If the returned response does not contain a
                top-level dictionary with an 'items' key.

        """
        # Get generator for pages of JSON data
        pages = self.get_pages(url, params=params, **kwargs)

        async for json_page in pages:
            assert isinstance(json_page, dict)

            items = json_page.get("items")

            if items is None:
                error_message = "'items' key not found in JSON data: " "{!r}".format(
                    json_page
                )
                raise MalformedResponse(error_message)

            else:
                for item in items:
                    yield item

    async def post(self, url, json=None, data=None, **kwargs):
        """Sends a POST request.

        Args:
            url(str): The URL of the API endpoint.
            json: Data to be sent in JSON format in tbe body of the request.
            data: Data to be sent in the body of the request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, str)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["POST"])

        response = await self.request("POST", url, erc, json=json, data=data, **kwargs)
        return await async_extract_and_parse_json(response)

    async def put(self, url, json=None, data=None, **kwargs):
        """Sends a PUT request.

        Args:
            url(str): The URL of the API endpoint.
            json: Data to be sent in JSON format in tbe body of the request.
            data: Data to be sent in the body of the request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, str)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["PUT"])

        response = await self.request("PUT", url, erc, json=json, data=data, **kwargs)
        return await async_extract_and_parse_json(response)

    async def delete(self, url, **kwargs):
        """Sends a DELETE request.

        Args:
            url(str): The URL of the API endpoint.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.

        """
        check_type(url, str)

        # Expected response code
        erc = kwargs.pop("erc", EXPECTED_RESPONSE_CODE["DELETE"])

        await self.request("DELETE", url, erc, **kwargs)

    async def close(self):
        """ Closes the underlying connection session """
        await self._req_session.close()
