# -*- coding: utf-8 -*-
"""Package helper functions and classes.

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

import json
import mimetypes
import os
import sys
import urllib.parse

from collections import OrderedDict, namedtuple
from datetime import datetime, timedelta, tzinfo

import aiohttp

from webexteamssdk.config import WEBEX_TEAMS_DATETIME_FORMAT
from webexteamssdk.aio.exceptions import AsyncApiError, AsyncRateLimitError, prepare_async_api_error

from webexteamssdk.response_codes import RATE_LIMIT_RESPONSE_CODE

from webexteamssdk.utils import *

async def async_check_response_code(
    response: aiohttp.ClientResponse, expected_response_code: int
):
    """Check response code against the expected code; raise ApiError.

    Checks the requests.response.status_code against the provided expected
    response code (erc), and raises a ApiError if they do not match.

    Args:
        response(requests.response): The response object returned by a request
            using the requests package.
        expected_response_code(int): The expected response code (HTTP response
            code).

    Raises:
        ApiError: If the requests.response.status_code does not match the
            provided expected response code (erc).

     """
    if response.status == expected_response_code:
        pass
    elif response.status == RATE_LIMIT_RESPONSE_CODE:
        raise await prepare_async_api_error(AsyncRateLimitError, response)
    else:
        raise await prepare_async_api_error(AsyncApiError, response)


async def async_extract_and_parse_json(response: aiohttp.ClientResponse) -> OrderedDict:
    """Extract and parse the JSON data from an requests.response object.

    Args:
        response(aiohttp.ClientResponse): The response object returned by a request
            using the requests package.

    Returns:
        The parsed JSON data as the appropriate native Python data type.

    """
    return json.loads(response.text, object_hook=OrderedDict)
