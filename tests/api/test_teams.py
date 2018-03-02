# -*- coding: utf-8 -*-
"""pytest Team functions, fixtures and tests."""


import itertools

import pytest

import ciscosparkapi
from tests.utils import create_string


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


# Helper Functions

def create_team(api, name):
    return api.teams.create(name)


def get_team_details_by_id(api, team_id):
    team = api.teams.get(team_id)
    return team


def delete_team(api, team):
    try:
        api.teams.delete(team.id)
    except ciscosparkapi.SparkApiError as e:
        if e.response.status_code == 404:
            # Team doesn't exist
            pass
        else:
            raise


def is_valid_team(obj):
    return isinstance(obj, ciscosparkapi.Team) and obj.id is not None


def are_valid_teams(iterable):
    return all([is_valid_team(obj) for obj in iterable])


def team_exists(api, team):
    try:
        get_team_details_by_id(api, team.id)
    except ciscosparkapi.SparkApiError:
        return False
    else:
        return True



# pytest Fixtures

@pytest.fixture(scope="session")
def team(api):
    team =  create_team(api, create_string("Team"))
    yield team
    delete_team(api, team)


@pytest.fixture(scope="session")
def teams_list(api, team):
    return list(api.teams.list())


@pytest.fixture
def temp_team(api):
    team = create_team(api, create_string("Team"))

    yield team

    if team_exists(api, team):
        delete_team(api, team)


@pytest.fixture
def add_teams(api):
    teams = []
    
    def inner(num_teams):
        for i in range(num_teams):
            teams.append(create_team(api, create_string("Additional Team")))
        return teams
    
    yield inner
    
    for team in teams:
        delete_team(api, team)


# Tests

class TestTeamsAPI(object):
    """Test TeamsAPI methods."""

    def test_create_team(self, team):
        assert is_valid_team(team)

    def test_get_team_details(self, api, team):
        team = get_team_details_by_id(api, team.id)
        assert is_valid_team(team)

    def test_update_team_name(self, api, team):
        new_name = create_string("Updated Team")
        team = api.teams.update(team.id, name=new_name)
        assert is_valid_team(team)
        assert team.name == new_name

    def test_delete_team(self, api, temp_team):
        # The delete method should complete without raising an exception
        api.teams.delete(temp_team.id)
        # Spark API endpoints aren't updating fast enough, deleted rooms are
        # still showing as existing via the `get` the API endpoint
        # assert not team_exists(api, temp_team)

    def test_list_teams(self, teams_list):
        assert len(teams_list) > 0
        assert are_valid_teams(teams_list)

    def test_list_teams_with_paging(self, api, teams_list, add_teams):
        page_size = 1
        pages = 3
        num_teams = pages * page_size
        if len(teams_list) < num_teams:
            add_teams(num_teams - len(teams_list))
        teams = api.teams.list(max=page_size)
        teams_list = list(itertools.islice(teams, num_teams))
        assert len(teams_list) == num_teams
        assert are_valid_teams(teams_list)
