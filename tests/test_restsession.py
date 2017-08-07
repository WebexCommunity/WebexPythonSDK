# -*- coding: utf-8 -*-
"""ciscosparkapi/restsession.py Fixtures & Tests"""


import logging

import pytest

from ciscosparkapi.exceptions import SPARK_RESPONSE_CODES

# Constants
RATE_LIMIT_RESPONSE_CODE = 429
RATE_LIMIT_RESPONSE_TEXT = SPARK_RESPONSE_CODES[RATE_LIMIT_RESPONSE_CODE]
RATE_LIMIT_LOG_MESSAGE = ("Received a [%s] rate limit response. "
                          "Attempting to retry.")


# Helper Classes
class RateLimitDetector(logging.Handler):
    """Detects occurrences of rate limiting."""

    def __init__(self):
        super(RateLimitDetector, self).__init__()

        self.rate_limit_detected = False

    def emit(self, record):
        """Check record to see if it is a rate-limit message."""
        assert isinstance(record, logging.LogRecord)

        if (RATE_LIMIT_RESPONSE_CODE in record.args
                and record.msg == RATE_LIMIT_LOG_MESSAGE):

            self.rate_limit_detected = True


# CiscoSparkAPI Tests
class TestRestSession:
    """Test edge cases of core RestSession functionality."""

    @pytest.mark.ratelimit
    def test_rate_limit_support(self, api, rooms_list, add_rooms):
        # Add log handler
        root_logger = logging.getLogger()
        rate_limit_detector = RateLimitDetector()
        root_logger.addHandler(rate_limit_detector)

        try:
            # Try and trigger a rate-limit
            rooms = api.rooms.list(max=1)
            while not rate_limit_detector.rate_limit_detected:
                for room in rooms:
                    # Do nothing
                    pass

        finally:
            # Remove the log handler
            root_logger.removeHandler(rate_limit_detector)

        assert rate_limit_detector.rate_limit_detected == True
