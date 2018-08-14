# -*- coding: utf-8 -*-
"""pytest Team Memberships functions, fixtures and tests.

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

import pytest

import webexteamssdk


# Helper Functions

def add_person_to_team_by_email(api, team, person, isModerator=False):
    return api.team_memberships.create(team.id,
                                       personEmail=person.emails[0],
                                       isModerator=isModerator)


def add_person_to_team_by_id(api, team, person, isModerator=False):
    return api.team_memberships.create(team.id,
                                       personId=person.id,
                                       isModerator=isModerator)


def get_team_membership_list(api, team, **kwargs):
    return list(api.team_memberships.list(teamId=team.id, **kwargs))


def get_team_membership_by_id(api, id):
    return api.team_memberships.get(id)


def make_moderator(api, team_membership):
    return api.team_memberships.update(team_membership.id, isModerator=True)


def delete_membership(api, team_membership):
    api.team_memberships.delete(team_membership.id)


def empty_team(api, me, team):
    """Remove all team_memberships from a team (except me)."""
    team_memberships = api.team_memberships.list(team.id)
    for membership in team_memberships:
        if membership.personId != me.id:
            delete_membership(api, membership)


def is_valid_team_membership(membership):
    return isinstance(membership, webexteamssdk.TeamMembership) \
           and membership.id is not None


def are_valid_team_memberships(iterable):
    are_valid = (is_valid_team_membership(item) for item in iterable)
    return all(are_valid)


def membership_exists(api, membership):
    try:
        get_team_membership_by_id(api, membership.id)
    except webexteamssdk.ApiError:
        return False
    else:
        return True


# pytest Fixtures

@pytest.fixture(scope="session")
def my_team_membership(api, me, team):
    team_memberships = get_team_membership_list(api, team)
    for membership in team_memberships:
        if membership.personId == me.id:
            return membership


@pytest.fixture(scope="session")
def make_me_team_moderator(api, my_team_membership):
    return make_moderator(api, my_team_membership)


@pytest.fixture(scope="session")
def team_member_added_by_email(api, make_me_team_moderator, team, test_people):
    person = test_people["member_added_by_email"]
    membership = add_person_to_team_by_email(api, team, person)

    yield membership

    delete_membership(api, membership)


@pytest.fixture(scope="session")
def team_member_added_by_id(api, make_me_team_moderator, team, test_people):
    person = test_people["member_added_by_id"]
    membership = add_person_to_team_by_id(api, team, person)

    yield membership

    delete_membership(api, membership)


@pytest.fixture(scope="session")
def team_moderator_added_by_email(api, make_me_team_moderator, team,
                                  test_people):
    person = test_people["moderator_added_by_email"]
    membership = add_person_to_team_by_email(api, team, person,
                                             isModerator=True)

    yield membership

    delete_membership(api, membership)


@pytest.fixture(scope="session")
def team_moderator_added_by_id(api, make_me_team_moderator, team, test_people):
    person = test_people["moderator_added_by_id"]
    membership = add_person_to_team_by_id(api, team, person,
                                          isModerator=True)

    yield membership

    delete_membership(api, membership)


@pytest.fixture(scope="session")
def additional_team_memberships(team_member_added_by_email,
                                team_member_added_by_id,
                                team_moderator_added_by_email,
                                team_moderator_added_by_id):
    return [team_member_added_by_email,
            team_member_added_by_id,
            team_moderator_added_by_email,
            team_moderator_added_by_id]


@pytest.fixture(scope="session")
def team_with_members(team, additional_team_memberships):
    return team


# Tests

class TestTeamMembershipsAPI(object):
    """Test MembershipsAPI methods."""

    def test_get_team_membership_details(self, api, my_team_membership):
        membership = get_team_membership_by_id(api, my_team_membership.id)
        assert is_valid_team_membership(membership)

    def test_create_team_membership_by_email(self, team_member_added_by_email):
        assert is_valid_team_membership(team_member_added_by_email)

    def test_create_team_membership_by_person_id(self,
                                                 team_member_added_by_id):
        assert is_valid_team_membership(team_member_added_by_id)

    def test_create_team_moderator_by_email(self,
                                            team_moderator_added_by_email):
        assert is_valid_team_membership(team_moderator_added_by_email)

    def test_create_team_moderator_by_person_id(self,
                                                team_moderator_added_by_id):
        assert is_valid_team_membership(team_moderator_added_by_id)

    def test_update_membership_make_moderator(self,
                                              make_me_team_moderator):
        assert is_valid_team_membership(make_me_team_moderator)
        assert make_me_team_moderator.isModerator

    def test_delete_membership(self, api, team, test_people):
        person = test_people["not_a_member"]
        membership = add_person_to_team_by_id(api, team, person)
        assert is_valid_team_membership(membership)
        delete_membership(api, membership)
        assert not membership_exists(api, membership)

    def test_list_team_memberships(self, api, team_with_members):
        team_memberships = get_team_membership_list(api, team_with_members)
        assert len(team_memberships) > 1
        assert are_valid_team_memberships(team_memberships)
