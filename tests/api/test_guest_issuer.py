# -*- coding: utf-8 -*-
"""WebexTeamsAPI Licenses API fixtures and tests.

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

import os
import time
import pytest

import webexteamssdk


TOKEN_EXPIRATION_SECONDS = 60 * 5
WEBEX_TEAMS_GUEST_ISSUER_ID = os.environ.get("WEBEX_TEAMS_GUEST_ISSUER_ID")
WEBEX_TEAMS_GUEST_ISSUER_SECRET = os.environ.get(
    "WEBEX_TEAMS_GUEST_ISSUER_SECRET"
)

if WEBEX_TEAMS_GUEST_ISSUER_ID is None or not WEBEX_TEAMS_GUEST_ISSUER_SECRET:
    pytest.skip(
        "Required WEBEX_TEAMS_GUEST_ISSUER_ID and/or "
        "WEBEX_TEAMS_GUEST_ISSUER_SECRET environment variables are not set.",
        allow_module_level=True,
    )


# Helper Functions


def is_valid_guest_issuer_token(obj):
    return (
        isinstance(obj, webexteamssdk.GuestIssuerToken)
        and obj.token is not None
    )


# Tests


def test_get_guest_issuer_token(api):
    guest_issuer_token = api.guest_issuer.create(
        sub="test-guest-user",
        name="Test Guest User",
        iss=WEBEX_TEAMS_GUEST_ISSUER_ID,
        exp=str(int(time.time()) + TOKEN_EXPIRATION_SECONDS),
        secret=WEBEX_TEAMS_GUEST_ISSUER_SECRET,
    )

    assert is_valid_guest_issuer_token(guest_issuer_token)
