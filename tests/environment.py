# -*- coding: utf-8 -*-
"""Test suite environment variables.

Copyright (c) 2016-2018 Cisco and/or its affiliates.

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

import os
import string

from webexteamssdk.config import ACCESS_TOKEN_ENVIRONMENT_VARIABLE


WEBEX_TEAMS_ACCESS_TOKEN = os.getenv(ACCESS_TOKEN_ENVIRONMENT_VARIABLE)
if WEBEX_TEAMS_ACCESS_TOKEN is None:
    raise RuntimeError(
        "You must set a {} environment variable to run the test suite"
        "".format(ACCESS_TOKEN_ENVIRONMENT_VARIABLE)
    )

WEBEX_TEAMS_TEST_DOMAIN = os.getenv("WEBEX_TEAMS_TEST_DOMAIN")
if WEBEX_TEAMS_TEST_DOMAIN is None:
    raise RuntimeError(
        "You must set a {} environment variable to run the test suite"
        "".format("WEBEX_TEAMS_TEST_DOMAIN")
    )

WEBEX_TEAMS_TEST_ID_START = int(os.getenv("WEBEX_TEAMS_TEST_ID_START"))
if WEBEX_TEAMS_TEST_ID_START is None:
    raise RuntimeError(
        "You must set a {} environment variable to run the test suite"
        "".format("WEBEX_TEAMS_TEST_ID_START")
    )

WEBEX_TEAMS_TEST_FILE_URL = os.getenv("WEBEX_TEAMS_TEST_FILE_URL")
if WEBEX_TEAMS_TEST_FILE_URL is None:
    raise RuntimeError(
        "You must set a {} environment variable to run the test suite"
        "".format("WEBEX_TEAMS_TEST_FILE_URL")
    )

WEBEX_TEAMS_TEST_STRING_PREFIX = os.getenv(
    "WEBEX_TEAMS_TEST_STRING_PREFIX", default="webexteamssdk py.test",
)

WEBEX_TEAMS_TEST_STRING_TEMPLATE = string.Template(os.getenv(
    "WEBEX_TEAMS_TEST_STRING_TEMPLATE", default="$prefix $item [$datetime]",
))
