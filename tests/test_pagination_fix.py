"""Test file for the pagination fix in _fix_next_url function.

This test file specifically tests the fix for the max parameter issue
in the list_messages() function and other list methods.
"""

import pytest
import urllib.parse
from unittest.mock import Mock, patch

from webexpythonsdk.restsession import _fix_next_url


class TestFixNextUrl:
    """Test cases for the _fix_next_url function."""

    def test_remove_max_null_parameter(self):
        """Test that max=null parameter is properly removed."""
        next_url = "https://webexapis.com/v1/messages?max=null&roomId=123"
        params = {"max": 10, "roomId": "123"}

        result = _fix_next_url(next_url, params)
        parsed = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed.query)

        # max=null should be removed
        assert "null" not in query_params.get("max", [])
        # max should be set to the original value
        assert query_params["max"] == ["10"]
        assert query_params["roomId"] == ["123"]

    def test_preserve_critical_parameters(self):
        """Test that critical parameters are always preserved."""
        next_url = "https://webexapis.com/v1/messages?max=5&roomId=456"
        params = {
            "max": 10,
            "roomId": "123",
            "parentId": "parent123",
            "mentionedPeople": "me",
            "before": "2024-01-01T00:00:00Z",
            "beforeMessage": "msg123"
        }

        result = _fix_next_url(next_url, params)
        parsed = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed.query)

        # Critical parameters should be preserved with original values
        assert query_params["max"] == ["10"]  # Should override the 5 in next_url
        assert query_params["roomId"] == ["123"]  # Should override the 456 in next_url
        assert query_params["parentId"] == ["parent123"]
        assert query_params["mentionedPeople"] == ["me"]
        assert query_params["before"] == ["2024-01-01T00:00:00Z"]
        assert query_params["beforeMessage"] == ["msg123"]

    def test_handle_non_critical_parameters(self):
        """Test that non-critical parameters are handled correctly."""
        next_url = "https://webexapis.com/v1/messages?max=10&roomId=123&custom=value"
        params = {
            "max": 10,
            "roomId": "123",
            "custom": "new_value",
            "additional": "param"
        }

        result = _fix_next_url(next_url, params)
        parsed = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed.query)

        # Custom parameter should be preserved from next_url (not overridden)
        assert query_params["custom"] == ["value"]
        # Additional parameter should be added
        assert query_params["additional"] == ["param"]

    def test_no_query_parameters(self):
        """Test handling of URLs without query parameters."""
        next_url = "https://webexapis.com/v1/messages"
        params = {"max": 10, "roomId": "123"}

        result = _fix_next_url(next_url, params)
        parsed = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed.query)

        # Parameters should be added
        assert query_params["max"] == ["10"]
        assert query_params["roomId"] == ["123"]

    def test_empty_params_dict(self):
        """Test handling when params is empty or None."""
        next_url = "https://webexapis.com/v1/messages?max=10&roomId=123"

        # Test with empty dict
        result = _fix_next_url(next_url, {})
        parsed = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed.query)

        # Original parameters should remain unchanged
        assert query_params["max"] == ["10"]
        assert query_params["roomId"] == ["123"]

        # Test with None
        result = _fix_next_url(next_url, None)
        parsed = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed.query)

        # Original parameters should remain unchanged
        assert query_params["max"] == ["10"]
        assert query_params["roomId"] == ["123"]

    def test_complex_url_with_multiple_parameters(self):
        """Test handling of complex URLs with multiple parameters."""
        next_url = (
            "https://webexapis.com/v1/messages?"
            "max=5&roomId=456&parentId=old_parent&"
            "custom1=value1&custom2=value2"
        )
        params = {
            "max": 20,
            "roomId": "789",
            "parentId": "new_parent",
            "mentionedPeople": "me",
            "custom3": "value3"
        }

        result = _fix_next_url(next_url, params)
        parsed = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed.query)

        # Critical parameters should be overridden
        assert query_params["max"] == ["20"]
        assert query_params["roomId"] == ["789"]
        assert query_params["parentId"] == ["new_parent"]
        assert query_params["mentionedPeople"] == ["me"]

        # Non-critical parameters should be preserved from next_url
        assert query_params["custom1"] == ["value1"]
        assert query_params["custom2"] == ["value2"]

        # New non-critical parameters should be added
        assert query_params["custom3"] == ["value3"]

    def test_max_parameter_edge_cases(self):
        """Test various edge cases for the max parameter."""
        # Test with max=0
        next_url = "https://webexapis.com/v1/messages?max=null"
        params = {"max": 0, "roomId": "123"}

        result = _fix_next_url(next_url, params)
        parsed = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed.query)

        assert query_params["max"] == ["0"]
        assert query_params["roomId"] == ["123"]

        # Test with max as string
        next_url = "https://webexapis.com/v1/messages?max=null"
        params = {"max": "50", "roomId": "123"}

        result = _fix_next_url(next_url, params)
        parsed = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed.query)

        assert query_params["max"] == ["50"]
        assert query_params["roomId"] == ["123"]

    def test_invalid_url_handling(self):
        """Test that invalid URLs raise appropriate errors."""
        # Test with missing scheme
        with pytest.raises(ValueError, match="valid API endpoint URL"):
            _fix_next_url("webexapis.com/v1/messages", {"max": 10})

        # Test with missing netloc
        with pytest.raises(ValueError, match="valid API endpoint URL"):
            _fix_next_url("https:///v1/messages", {"max": 10})

        # Test with missing path
        with pytest.raises(ValueError, match="valid API endpoint URL"):
            _fix_next_url("https://webexapis.com", {"max": 10})


class TestPaginationIntegration:
    """Integration tests for pagination behavior with the fix."""

    def test_messages_list_pagination_preserves_max(self):
        """Test that list_messages pagination properly preserves the max parameter."""
        from webexpythonsdk.api.messages import MessagesAPI
        from webexpythonsdk.restsession import RestSession

        # Mock the RestSession
        mock_session = Mock(spec=RestSession)
        mock_object_factory = Mock()

        # Mock get_items to return an empty list (iterable)
        mock_session.get_items.return_value = []

        # Create MessagesAPI instance
        messages_api = MessagesAPI(mock_session, mock_object_factory)

        # Test parameters
        room_id = "room123"
        max_param = 5

        # Call list method and trigger the generator by converting to list
        # This ensures get_items is actually called
        list(messages_api.list(roomId=room_id, max=max_param))

        # Verify that get_items was called with correct parameters
        mock_session.get_items.assert_called_once()
        call_args = mock_session.get_items.call_args

        # Check that the max parameter is included in the call
        assert call_args[1]['params']['max'] == max_param
        assert call_args[1]['params']['roomId'] == room_id

    def test_fix_next_url_integration_scenario(self):
        """Test a realistic pagination scenario."""
        # Simulate first request parameters
        original_params = {
            "max": 10,
            "roomId": "room123",
            "parentId": "parent456",
            "mentionedPeople": "me"
        }

        # Simulate next URL returned by Webex (with max=null issue)
        next_url = (
            "https://webexapis.com/v1/messages?"
            "max=null&roomId=room123&parentId=parent456&"
            "mentionedPeople=me&nextPageToken=abc123"
        )

        # Apply the fix
        fixed_url = _fix_next_url(next_url, original_params)

        # Parse the result
        parsed = urllib.parse.urlparse(fixed_url)
        query_params = urllib.parse.parse_qs(parsed.query)

        # Verify critical parameters are preserved
        assert query_params["max"] == ["10"]  # Should be the original value, not null
        assert query_params["roomId"] == ["room123"]
        assert query_params["parentId"] == ["parent456"]
        assert query_params["mentionedPeople"] == ["me"]
        assert query_params["nextPageToken"] == ["abc123"]  # Should be preserved from next_url

        # Verify max=null was removed
        assert "null" not in str(query_params)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
