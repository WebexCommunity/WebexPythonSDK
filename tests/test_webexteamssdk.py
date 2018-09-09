# -*- coding: utf-8 -*-
"""Test suite for the community-developed Python SDK for the Webex Teams APIs.

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

import webexteamssdk


class TestWebexTeamsSDK:
    """Test the package-level code."""

    def test_package_contents(self):
        """Ensure the package contains the correct top-level objects."""
        # Webex Teams API Wrapper
        assert hasattr(webexteamssdk, "WebexTeamsAPI")

        # Exceptions
        assert hasattr(webexteamssdk, "ApiError")
        assert hasattr(webexteamssdk, "AccessTokenError")
        assert hasattr(webexteamssdk, "RateLimitError")
        assert hasattr(webexteamssdk, "RateLimitWarning")
        assert hasattr(webexteamssdk, "webexteamssdkException")

        # Data Models
        assert hasattr(webexteamssdk, "dict_data_factory")
        assert hasattr(webexteamssdk, "AccessToken")
        assert hasattr(webexteamssdk, "Event")
        assert hasattr(webexteamssdk, "License")
        assert hasattr(webexteamssdk, "Membership")
        assert hasattr(webexteamssdk, "Message")
        assert hasattr(webexteamssdk, "Organization")
        assert hasattr(webexteamssdk, "Person")
        assert hasattr(webexteamssdk, "Role")
        assert hasattr(webexteamssdk, "Room")
        assert hasattr(webexteamssdk, "Team")
        assert hasattr(webexteamssdk, "TeamMembership")
        assert hasattr(webexteamssdk, "Webhook")
        assert hasattr(webexteamssdk, "WebhookEvent")
        assert hasattr(webexteamssdk, "immutable_data_factory")
        assert hasattr(webexteamssdk, "SimpleDataModel")
        assert hasattr(webexteamssdk, "simple_data_factory")
