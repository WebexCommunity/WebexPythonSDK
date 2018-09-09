# -*- coding: utf-8 -*-
"""webexteamssdk/restsession.py Fixtures & Tests

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


import logging
import warnings

import pytest

import webexteamssdk


logging.captureWarnings(True)


# Helper Functions
def rate_limit_detected(w):
    """Check to see if a rate-limit warning is in the warnings list."""
    while w:
        if issubclass(w.pop().category, webexteamssdk.RateLimitWarning):
            return True
    return False


# Tests
@pytest.mark.ratelimit
def test_rate_limit_retry(api, list_of_rooms, add_rooms):
    # Save state and initialize test setup
    original_wait_on_rate_limit = api._session.wait_on_rate_limit
    api._session.wait_on_rate_limit = True

    with warnings.catch_warnings(record=True) as w:
        rooms = api.rooms.list()
        while True:
            # Try and trigger a rate-limit
            list(rooms)
            if rate_limit_detected(w):
                break

    api._session.wait_on_rate_limit = original_wait_on_rate_limit
