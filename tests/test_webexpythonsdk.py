"""Test suite for the community-developed Python SDK for the Webex APIs.

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
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import webexpythonsdk


class TestWebexPythonSDK:
    """Test the package-level code."""

    def test_package_contents(self):
        """Ensure the package contains the correct top-level objects."""
        # Webex API Wrapper
        assert hasattr(webexpythonsdk, "WebexAPI")

        # Exceptions
        assert hasattr(webexpythonsdk, "ApiError")
        assert hasattr(webexpythonsdk, "AccessTokenError")
        assert hasattr(webexpythonsdk, "RateLimitError")
        assert hasattr(webexpythonsdk, "RateLimitWarning")
        assert hasattr(webexpythonsdk, "webexpythonsdkException")

        # Data Models
        assert hasattr(webexpythonsdk, "dict_data_factory")
        assert hasattr(webexpythonsdk, "AccessToken")
        assert hasattr(webexpythonsdk, "AttachmentAction")
        assert hasattr(webexpythonsdk, "Event")
        assert hasattr(webexpythonsdk, "License")
        assert hasattr(webexpythonsdk, "Membership")
        assert hasattr(webexpythonsdk, "Message")
        assert hasattr(webexpythonsdk, "Organization")
        assert hasattr(webexpythonsdk, "Person")
        assert hasattr(webexpythonsdk, "Role")
        assert hasattr(webexpythonsdk, "Room")
        assert hasattr(webexpythonsdk, "Team")
        assert hasattr(webexpythonsdk, "TeamMembership")
        assert hasattr(webexpythonsdk, "Webhook")
        assert hasattr(webexpythonsdk, "WebhookEvent")
        assert hasattr(webexpythonsdk, "Recording")
        assert hasattr(webexpythonsdk, "immutable_data_factory")
        assert hasattr(webexpythonsdk, "SimpleDataModel")
        assert hasattr(webexpythonsdk, "simple_data_factory")
