# -*- coding: utf-8 -*-

"""pytest Team functions, fixtures and tests."""


import pytest

import ciscosparkapi
from tests.utils import create_string


# Helper Functions

def create_team(api, name):
    return api.teams.create(name)


def delete_team(api, team):
    api.teams.delete(team.id)


# pytest Fixtures

@pytest.fixture(scope="session")
def team(api):
    team =  create_team(api, create_string("Team"))
    yield team
    delete_team(api, team)
