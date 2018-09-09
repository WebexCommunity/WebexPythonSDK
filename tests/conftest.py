# -*- coding: utf-8 -*-
"""pytest configuration and top-level fixtures.

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

import os
import random
import string
import tempfile

import pytest

from tests.environment import (
    WEBEX_TEAMS_TEST_DOMAIN, WEBEX_TEAMS_TEST_FILE_URL,
    WEBEX_TEAMS_TEST_ID_START,
)
from tests.utils import download_file


pytest_plugins = [
    'tests.test_webexteamssdk',
    'tests.api',
    'tests.api.test_licenses',
    'tests.api.test_memberships',
    'tests.api.test_messages',
    'tests.api.test_organizations',
    'tests.api.test_people',
    'tests.api.test_roles',
    'tests.api.test_rooms',
    'tests.api.test_teammemberships',
    'tests.api.test_teams',
    "tests.api.test_events",
]

email_template = string.Template("test${number}@" + WEBEX_TEAMS_TEST_DOMAIN)


# Helper Functions
def new_email_generator():
    i = WEBEX_TEAMS_TEST_ID_START
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
        file = download_file(WEBEX_TEAMS_TEST_FILE_URL, temp_directory)

        yield file

        os.remove(file)


@pytest.fixture(scope="session")
def get_new_email_address():
    generator = new_email_generator()

    def inner_function():
        return next(generator)

    return inner_function


@pytest.fixture()
def get_random_email_address():
    def inner_function():
        i = random.randint(1000, 9999)
        return email_template.substitute(number=i)

    return inner_function
