# -*- coding: utf-8 -*-
"""WebexTeamsAPI Team Memberships API fixtures and tests.

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


# Helper Functions

def is_valid_team_membership(membership):
    return isinstance(membership, webexteamssdk.TeamMembership) \
        and membership.id is not None


def are_valid_team_memberships(iterable):
    are_valid = (is_valid_team_membership(item) for item in iterable)
    return all(are_valid)


# Fixtures

@pytest.fixture(scope="session")
def my_team_membership(api, me, team):
    team_memberships = api.team_memberships.list(team.id)
    for membership in team_memberships:
        if membership.personId == me.id:
            return membership


@pytest.fixture(scope="session")
def team_moderator(api, my_team_membership):
    if my_team_membership.isModerator:
        return True
    else:
        updated_membership = api.team_memberships.update(
            my_team_membership.id,
            isModerator=True,
        )

        if updated_membership.isModerator:
            return True

    pytest.fail("Unable to make test account a Team Moderator")


@pytest.fixture(scope="session")
def team_member_added_by_email(api, team, test_people, team_moderator):
    person = test_people["member_added_by_email"]
    membership = api.team_memberships.create(
        teamId=team.id,
        personEmail=person.emails[0],
    )

    yield membership

    api.team_memberships.delete(membership.id)


@pytest.fixture(scope="session")
def team_member_added_by_id(api, team, test_people, team_moderator):
    person = test_people["member_added_by_id"]
    membership = api.team_memberships.create(
        teamId=team.id,
        personId=person.id,
    )

    yield membership

    api.team_memberships.delete(membership.id)


@pytest.fixture(scope="session")
def team_moderator_added_by_email(api, team, test_people, team_moderator):
    person = test_people["moderator_added_by_email"]
    membership = api.team_memberships.create(
        teamId=team.id,
        personEmail=person.emails[0],
        isModerator=True,
    )

    yield membership

    api.team_memberships.delete(membership.id)


@pytest.fixture(scope="session")
def team_moderator_added_by_id(api, team, test_people, team_moderator):
    person = test_people["moderator_added_by_id"]
    membership = api.team_memberships.create(
        teamId=team.id,
        personId=person.id,
        isModerator=True,
    )

    yield membership

    api.team_memberships.delete(membership.id)


@pytest.fixture(scope="session")
def additional_team_memberships(team_member_added_by_email,
                                team_member_added_by_id,
                                team_moderator_added_by_email,
                                team_moderator_added_by_id):
    return [
        team_member_added_by_email,
        team_member_added_by_id,
        team_moderator_added_by_email,
        team_moderator_added_by_id
    ]


@pytest.fixture(scope="session")
def team_with_members(team, additional_team_memberships):
    return team


# Tests

def test_list_team_memberships(api, team_with_members):
    team_memberships = list(api.team_memberships.list(team_with_members.id))
    assert len(team_memberships) > 1
    assert are_valid_team_memberships(team_memberships)


@pytest.mark.usefixtures("additional_team_memberships")
def test_list_team_memberships_with_paging(api, team):
    page_size = 1
    pages = 3
    num_memberships = pages * page_size
    memberships = api.team_memberships.list(team.id, max=page_size)
    memberships_list = list(itertools.islice(memberships, num_memberships))
    assert len(memberships_list) == num_memberships
    assert are_valid_team_memberships(memberships_list)


def test_create_team_membership_by_email(team_member_added_by_email):
    assert is_valid_team_membership(team_member_added_by_email)


def test_create_team_membership_by_person_id(team_member_added_by_id):
    assert is_valid_team_membership(team_member_added_by_id)


def test_create_team_moderator_by_email(team_moderator_added_by_email):
    assert is_valid_team_membership(team_moderator_added_by_email)


def test_create_team_moderator_by_person_id(team_moderator_added_by_id):
    assert is_valid_team_membership(team_moderator_added_by_id)


def test_get_team_membership_details(api, my_team_membership):
    membership = api.team_memberships.get(my_team_membership.id)
    assert is_valid_team_membership(membership)


def test_update_membership_make_moderator(api, team_member_added_by_id):
    updated_membership = api.team_memberships.update(
        membershipId=team_member_added_by_id.id,
        isModerator=True,
    )
    assert updated_membership.isModerator


def test_delete_membership(api, team, test_people):
    person = test_people["not_a_member"]
    membership = api.team_memberships.create(team.id, personId=person.id)
    assert is_valid_team_membership(membership)
    api.team_memberships.delete(membership.id)
