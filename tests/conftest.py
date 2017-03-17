# -*- coding: utf-8 -*-
<<<<<<< HEAD
"""pytest configuration and top-level fixtures."""


import string

import pytest
=======

"""pytest configuration and top-level fixtures."""

import pytest


EMAIL_ADDRESSES = [
    'test98@cmlccie.com',
    'test99@cmlccie.com',
]
>>>>>>> master


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
_email_addresses = []


# Helper Functions
def new_email_generator():
    i = 0
    while True:
        email_address = email_template.substitute(number=i)
        _email_addresses.append(email_address)
        i += 1
        yield email_address


# pytest Fixtures

@pytest.fixture(scope="session")
def email_addresses():
    return _email_addresses


@pytest.fixture(scope="session")
def get_email_addresses():
    def inner_function(num):
        if len(email_addresses) < num:
            for i in range(num - len(email_addresses)):
                new_email_address()
        return email_addresses[:num]
    return inner_function


@pytest.fixture(scope="session")
def get_new_email_address():
    generator = new_email_generator()
    def inner_function():
        return generator.next()
    return inner_function
