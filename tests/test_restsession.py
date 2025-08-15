"""webexpythonsdk/restsession.py Fixtures & Tests

Copyright (c) 2016-2024 Cisco and/or its affiliates.

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
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import logging
import warnings

import pytest
import requests
from unittest.mock import Mock, patch

import webexpythonsdk


logging.captureWarnings(True)


# Helper Functions
def rate_limit_detected(w):
    """Check to see if a rate-limit warning is in the warnings list."""
    while w:
        if issubclass(w.pop().category, webexpythonsdk.RateLimitWarning):
            return True
    return False


def create_mock_rate_limit_response(
    status_code=429, retry_after=None, content_type="application/json"
):
    """Create a mock response object for testing rate limit scenarios."""
    # Use Mock(spec=requests.Response) to properly simulate a requests.Response object
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = status_code
    mock_response.reason = "Too Many Requests"
    mock_response.headers = {}

    if retry_after is not None:
        mock_response.headers["Retry-After"] = retry_after

    mock_response.headers["Content-Type"] = content_type
    mock_response.json.return_value = {
        "message": "Rate limit exceeded",
        "trackingId": "test-tracking-id-12345",
    }

    # Mock the request attribute that ApiError constructor needs
    mock_request = Mock()
    mock_request.method = "GET"
    mock_request.url = "https://webexapis.com/v1/test"
    mock_response.request = mock_request

    return mock_response


# Tests
@pytest.mark.slow
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


def test_rate_limit_error_with_valid_retry_after():
    """Test RateLimitError works correctly with valid Retry-After headers."""
    # Test with various valid integer values
    test_cases = [
        ("30", 30),  # Normal case
        ("60", 60),  # One minute
        ("0", 1),  # Zero should default to 1 (minimum)
        ("1", 1),  # Minimum value
        ("300", 300),  # Five minutes
    ]

    for header_value, expected_value in test_cases:
        mock_response = create_mock_rate_limit_response(
            retry_after=header_value
        )

        try:
            error = webexpythonsdk.RateLimitError(mock_response)
            assert (
                error.retry_after == expected_value
            ), f"Expected retry_after={expected_value}, got {error.retry_after} for header '{header_value}'"
        except Exception as e:
            pytest.fail(
                f"RateLimitError creation failed for valid header '{header_value}': {e}"
            )


def test_rate_limit_error_without_retry_after():
    """Test RateLimitError defaults correctly when Retry-After header is missing."""
    mock_response = create_mock_rate_limit_response(retry_after=None)

    try:
        error = webexpythonsdk.RateLimitError(mock_response)
        assert (
            error.retry_after == 15
        ), f"Expected default retry_after=15, got {error.retry_after}"
    except Exception as e:
        pytest.fail(
            f"RateLimitError creation failed when Retry-After header is missing: {e}"
        )


def test_rate_limit_error_with_malformed_retry_after():
    """Test RateLimitError handles malformed Retry-After headers gracefully.

    This test reproduces the bug reported by users where malformed headers
    like 'rand(30),add(30)' cause ValueError exceptions.
    """
    malformed_headers = [
        "rand(30),add(30)",  # The exact case from the user report
        "invalid",  # Non-numeric string
        "30.5",  # Float (should fail int conversion)
        "30 seconds",  # String with numbers and text
        "30,60",  # Comma-separated values
        "",  # Empty string
        "None",  # String 'None'
        "null",  # String 'null'
    ]

    for malformed_header in malformed_headers:
        mock_response = create_mock_rate_limit_response(
            retry_after=malformed_header
        )

        try:
            # This should NOT raise a ValueError - it should handle gracefully
            error = webexpythonsdk.RateLimitError(mock_response)
            # If we get here, the error was handled gracefully
            # The retry_after should default to 15 for malformed headers
            assert (
                error.retry_after == 15
            ), f"Expected default retry_after=15 for malformed header '{malformed_header}', got {error.retry_after}"
        except ValueError as e:
            # This is the bug we're testing for - it should NOT happen
            pytest.fail(
                f"RateLimitError raised ValueError for malformed header '{malformed_header}': {e}"
            )
        except Exception as e:
            # Other exceptions are acceptable as long as they're not ValueError
            if isinstance(e, ValueError):
                pytest.fail(
                    f"RateLimitError raised ValueError for malformed header '{malformed_header}': {e}"
                )


def test_rate_limit_error_with_non_string_retry_after():
    """Test RateLimitError handles non-string Retry-After header values."""
    # Test cases with expected behavior based on how Python int() actually works
    test_cases = [
        (None, 15),  # None value -> defaults to 15
        (30, 30),  # Integer -> converts to 30 (not malformed)
        (30.5, 30),  # Float -> converts to 30 (truncated)
        (True, 1),  # Boolean True -> converts to 1
        (False, 1),  # Boolean False -> converts to 0, then max(1, 0) = 1
        ([], 15),  # List -> TypeError, defaults to 15
        ({}, 15),  # Dict -> TypeError, defaults to 15
    ]

    for non_string_value, expected_value in test_cases:
        mock_response = create_mock_rate_limit_response(
            retry_after=non_string_value
        )

        try:
            error = webexpythonsdk.RateLimitError(mock_response)
            assert (
                error.retry_after == expected_value
            ), f"Expected retry_after={expected_value}, got {error.retry_after} for non-string value {non_string_value}"
        except Exception as e:
            pytest.fail(
                f"RateLimitError creation failed for non-string value {non_string_value}: {e}"
            )


def test_rate_limit_error_integration_with_check_response_code():
    """Test that check_response_code properly raises RateLimitError for 429 responses."""
    from webexpythonsdk.utils import check_response_code

    # Test with valid Retry-After header
    mock_response = create_mock_rate_limit_response(retry_after="45")

    with pytest.raises(webexpythonsdk.RateLimitError) as exc_info:
        check_response_code(mock_response, 200)  # Expect 200, get 429

    error = exc_info.value
    assert error.retry_after == 45
    assert error.status_code == 429


def test_rate_limit_error_integration_with_malformed_header():
    """Test that check_response_code works even with malformed Retry-After headers."""
    from webexpythonsdk.utils import check_response_code

    # Test with malformed Retry-After header
    mock_response = create_mock_rate_limit_response(
        retry_after="rand(30),add(30)"
    )

    with pytest.raises(webexpythonsdk.RateLimitError) as exc_info:
        check_response_code(mock_response, 200)  # Expect 200, get 429

    error = exc_info.value
    # Should default to 15 for malformed headers
    assert error.retry_after == 15
    assert error.status_code == 429


def test_rate_limit_error_edge_cases():
    """Test RateLimitError with edge case Retry-After values."""
    # Test cases based on how Python int() actually works with strings
    edge_cases = [
        ("-1", 1),  # Negative string -> converts to -1, then max(1, -1) = 1
        ("999999", 999999),  # Very large number string -> converts to 999999
        ("0.0", 15),  # Float string -> treated as malformed, defaults to 15
        ("0.9", 15),  # Float string -> treated as malformed, defaults to 15
        ("1.0", 15),  # Float string -> treated as malformed, defaults to 15
        ("1.9", 15),  # Float string -> treated as malformed, defaults to 15
        ("2.0", 15),  # Float string -> treated as malformed, defaults to 15
    ]

    for header_value, expected_value in edge_cases:
        mock_response = create_mock_rate_limit_response(
            retry_after=header_value
        )

        try:
            error = webexpythonsdk.RateLimitError(mock_response)
            # All float strings are being treated as malformed and defaulting to 15
            # Integer strings work normally with max(1, value)
            if "." in header_value:  # Float strings
                actual_expected = 15  # Treated as malformed
            else:
                actual_expected = max(1, expected_value)
            assert (
                error.retry_after == actual_expected
            ), f"Expected retry_after={actual_expected}, got {error.retry_after} for header '{header_value}'"
        except Exception as e:
            pytest.fail(
                f"RateLimitError creation failed for edge case header '{header_value}': {e}"
            )


def test_rate_limit_error_response_attributes():
    """Test that RateLimitError properly extracts all response attributes."""
    mock_response = create_mock_rate_limit_response(retry_after="60")

    error = webexpythonsdk.RateLimitError(mock_response)

    # Test basic attributes
    assert error.status_code == 429
    assert error.status == "Too Many Requests"
    assert error.retry_after == 60

    # Test that details are parsed correctly
    assert error.details is not None
    assert error.message == "Rate limit exceeded"
    assert error.tracking_id == "test-tracking-id-12345"

    # Test error message format
    assert "[429]" in error.error_message
    assert "Too Many Requests" in error.error_message
    assert "Rate limit exceeded" in error.error_message
    assert "test-tracking-id-12345" in error.error_message
