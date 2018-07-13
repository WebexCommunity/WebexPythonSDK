# -*- coding: utf-8 -*-
"""webexteamsdk/restsession.py Fixtures & Tests"""


import logging
import warnings

import pytest

import webexteamsdk


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


logging.captureWarnings(True)


# Helper Functions
def rate_limit_detected(w):
    """Check to see if a rate-limit warning is in the warnings list."""
    while w:
        if issubclass(w.pop().category, webexteamsdk.RateLimitWarning):
            return True
            break
    return False


# CiscoSparkAPI Tests
class TestRestSession:
    """Test edge cases of core RestSession functionality."""

    @pytest.mark.ratelimit
    def test_rate_limit_retry(self, api, rooms_list, add_rooms):
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
