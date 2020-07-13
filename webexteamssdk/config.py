# -*- coding: utf-8 -*-
"""Package configuration.

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


# Package Constants
DEFAULT_BASE_URL = "https://webexapis.com/v1/"

DEFAULT_SINGLE_REQUEST_TIMEOUT = 60

DEFAULT_WAIT_ON_RATE_LIMIT = True

ACCESS_TOKEN_ENVIRONMENT_VARIABLE = "WEBEX_TEAMS_ACCESS_TOKEN"

LEGACY_ACCESS_TOKEN_ENVIRONMENT_VARIABLES = [
    "SPARK_ACCESS_TOKEN",
    "CISCO_SPARK_ACCESS_TOKEN",
]

WEBEX_TEAMS_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
