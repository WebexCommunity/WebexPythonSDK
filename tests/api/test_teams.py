# -*- coding: utf-8 -*-
"""WebexTeamsAPI Team API fixtures and tests.

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

import itertools

import pytest

import webexteamssdk
from tests.utils import create_string


# Helper Functions

def is_valid_team(obj):
    return isinstance(obj, webexteamssdk.Team) and obj.id is not None


def are_valid_teams(iterable):
    return all([is_valid_team(obj) for obj in iterable])


# Fixtures

@pytest.fixture(scope="session")
def team(api):
    team = api.teams.create(create_string("Team"))

    yield team

    api.teams.delete(team.id)


@pytest.fixture(scope="session")
def teams_list(api, team):
    return list(api.teams.list())


@pytest.fixture
def temp_team(api):
    team = api.teams.create(create_string("Temp Team"))

    yield team

    try:
        api.teams.delete(team.id)
    except webexteamssdk.ApiError:
        pass


@pytest.fixture
def add_teams(api):
    teams = []

    def inner(num_teams):
        for i in range(num_teams):
            teams.append(api.teams.create(create_string("Additional Team")))
        return teams

    yield inner

    for team in teams:
        try:
            api.teams.delete(team.id)
        except webexteamssdk.ApiError:
            pass


# Tests

def test_list_teams(teams_list):
    assert len(teams_list) > 0
    assert are_valid_teams(teams_list)


def test_list_teams_with_paging(api, teams_list, add_teams):
    page_size = 1
    pages = 3
    num_teams = pages * page_size
    if len(teams_list) < num_teams:
        add_teams(num_teams - len(teams_list))
    teams = api.teams.list(max=page_size)
    teams_list = list(itertools.islice(teams, num_teams))
    assert len(teams_list) == num_teams
    assert are_valid_teams(teams_list)


def test_create_team(team):
    assert is_valid_team(team)


def test_get_team_details(api, team):
    details = api.teams.get(team.id)
    assert is_valid_team(details)


def test_update_team_name(api, team):
    new_name = create_string("Updated Team")
    updated_team = api.teams.update(team.id, name=new_name)
    assert is_valid_team(updated_team)
    assert updated_team.name == new_name


def test_delete_team(api, temp_team):
    api.teams.delete(temp_team.id)
