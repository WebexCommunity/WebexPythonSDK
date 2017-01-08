# -*- coding: utf-8 -*-

"""pytest People functions, fixtures and tests."""


import pytest

import ciscosparkapi
from tests.utils import create_string


# Helper Functions




# pytest Fixtures

@pytest.fixture(scope="session")
def me(api):
    return api.people.me()
