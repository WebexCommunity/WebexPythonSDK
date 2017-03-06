# -*- coding: utf-8 -*-

"""pytest configuration and top-level fixtures."""

import pytest


EMAIL_ADDRESSES = [
    'test98@cmlccie.com',
    'test99@cmlccie.com',
]


pytest_plugins = [
    'tests.test_ciscosparkapi',
    'tests.api.test_accesstokens',
    'tests.api.test_memberships',
    'tests.api.test_messages',
    'tests.api.test_people',
    'tests.api.test_rooms',
    'tests.api.test_teammemberships',
    'tests.api.test_teams',
    'tests.api.test_webhooks',
]


# pytest Fixtures

@pytest.fixture(scope="session")
def email_addresses():
    return EMAIL_ADDRESSES
