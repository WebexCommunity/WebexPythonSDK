# -*- coding: utf-8 -*-
"""pytest configuration and top-level fixtures."""


import string

import pytest


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
    'tests.api.test_organizations',
    'tests.api.test_licenses',
    'tests.api.test_roles',
]


TEST_DOMAIN = "cmlccie.com"

email_template = string.Template("test${number}@" + TEST_DOMAIN)


# Helper Functions
def new_email_generator():
    i = 0
    while True:
        email_address = email_template.substitute(number=i)
        i += 1
        yield email_address


# pytest Fixtures

@pytest.fixture(scope="session")
def get_new_email_address():
    generator = new_email_generator()

    def inner_function():
        return generator.next()

    return inner_function
