# -*- coding: utf-8 -*-
"""pytest configuration and top-level fixtures."""


import os
import string
import tempfile

import pytest

from tests.utils import download_file


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
TEST_FILE_URL = "https://developer.ciscospark.com/images/logo_spark_lg@256.png"


email_template = string.Template("test${number}@" + TEST_DOMAIN)


# Helper Functions
def new_email_generator():
    i = 50
    while True:
        email_address = email_template.substitute(number=i)
        i += 1
        yield email_address


# pytest Fixtures

@pytest.fixture("session")
def temp_directory():
    directory_abs_path = tempfile.mkdtemp()

    yield directory_abs_path

    os.rmdir(directory_abs_path)


@pytest.fixture("session")
def local_file(temp_directory):
        file = download_file(TEST_FILE_URL, temp_directory)

        yield file

        os.remove(file)


@pytest.fixture(scope="session")
def get_new_email_address():
    generator = new_email_generator()

    def inner_function():
        return next(generator)

    return inner_function
