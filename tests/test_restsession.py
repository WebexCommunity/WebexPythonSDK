# -*- coding: utf-8 -*-
"""ciscosparkapi/restsession.py Fixtures & Tests"""


import logging

import pytest


# Helper Classes
class RateLimitDetector(logging.Handler):
    """Detects occurrences of rate limiting."""

    def __init__(self):
        super(RateLimitDetector, self).__init__()

        self.rate_limit_detected = False

    def emit(self, record):
        """Check record to see if it is a rate-limit message."""
        assert isinstance(record, logging.LogRecord)

        if record.msg.startswith("Received rate-limit message"):
            self.rate_limit_detected = True


# CiscoSparkAPI Tests
class TestRestSession:
    """Test edge cases of core RestSession functionality."""

    @pytest.mark.ratelimit
    def test_rate_limit_retry_indefinitely(self, api, rooms_list, add_rooms):
        logger = logging.getLogger(__name__)

        # Save state and initialize test setup
        original_rate_limit_timer = api._session.rate_limit_timeout
        api._session.rate_limit_timeout = None

        # Add log handler
        root_logger = logging.getLogger()
        rate_limit_detector = RateLimitDetector()
        root_logger.addHandler(rate_limit_detector)

        try:
            # Try and trigger a rate-limit
            rooms = api.rooms.list(max=1)
            request_count = 0
            while not rate_limit_detector.rate_limit_detected:
                for room in rooms:
                    request_count += 1
                    if rate_limit_detector.rate_limit_detected:
                        break

        finally:
            logger.info("Rate-limit reached with approximately %s requests.",
                        request_count)
            # Remove the log handler and restore the pre-test state
            root_logger.removeHandler(rate_limit_detector)
            api._session.rate_limit_timeout = original_rate_limit_timer

        # Assert test condition
        assert rate_limit_detector.rate_limit_detected == True
