# -*- coding: utf-8 -*-

"""pytest Team Memberships functions, fixtures and tests."""


import pytest

import ciscosparkapi
from tests.utils import create_string


# Helper Functions

def add_people_to_team(api, team, emails):
    for email in emails:
        api.team_memberships.create(team.id, personEmail=email)


def empty_team(api, me, team):
    """Remove all memberships from a team (except the caller's membership)."""
    memberships = api.team_memberships.list(team.id)
    for membership in memberships:
        if membership.personId != me.id:
            api.team_memberships.delete(membership.id)


# pytest Fixtures

@pytest.fixture(scope="session")
def team_with_members(api, me, team, email_addresses):
    add_people_to_team(api, team, email_addresses)
    yield team
    empty_team(api, me, team)
