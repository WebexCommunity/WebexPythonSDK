# -*- coding: utf-8 -*-
"""WebexTeamsAPI Memberships API fixtures and tests.

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

def is_valid_membership(membership):
    return isinstance(membership, webexteamssdk.Membership) \
        and membership.id is not None


def are_valid_memberships(iterable):
    are_valid = (is_valid_membership(item) for item in iterable)
    return all(are_valid)


# Fixtures

@pytest.fixture(scope="session")
def my_memberships(api, group_room, team_room, direct_rooms):
    return list(api.memberships.list())


@pytest.fixture(scope="session")
def my_group_room_membership(api, group_room, me):
    memberships = list(
        api.memberships.list(roomId=group_room.id, personId=me.id)
    )
    assert len(memberships) == 1
    return memberships[0]


@pytest.fixture(scope="session")
def group_room_moderator(api, my_group_room_membership):
    if my_group_room_membership.isModerator:
        return True
    else:
        updated_membership = api.memberships.update(
            membershipId=my_group_room_membership.id,
            isModerator=True,
        )

        if updated_membership.isModerator:
            return True

    pytest.fail("Unable to make test account a Room Moderator")


@pytest.fixture(scope="session")
def membership_person_added_by_email(api, group_room, test_people,
                                     group_room_moderator):
    person = test_people["member_added_by_email"]
    membership = api.memberships.create(
        roomId=group_room.id,
        personEmail=person.emails[0],
    )

    yield membership

    api.memberships.delete(membership.id)


@pytest.fixture(scope="session")
def membership_person_added_by_id(api, group_room, test_people,
                                  group_room_moderator):
    person = test_people["member_added_by_id"]
    membership = api.memberships.create(
        roomId=group_room.id,
        personId=person.id,
    )

    yield membership

    api.memberships.delete(membership.id)


@pytest.fixture(scope="session")
def membership_moderator_added_by_email(api, group_room, test_people,
                                        group_room_moderator):
    person = test_people["moderator_added_by_email"]
    membership = api.memberships.create(
        roomId=group_room.id,
        personEmail=person.emails[0],
        isModerator=True,
    )

    yield membership

    api.memberships.delete(membership.id)


@pytest.fixture(scope="session")
def membership_moderator_added_by_id(api, group_room, test_people,
                                     group_room_moderator):
    person = test_people["moderator_added_by_id"]
    membership = api.memberships.create(
        roomId=group_room.id,
        personId=person.id,
        isModerator=True,
    )

    yield membership

    api.memberships.delete(membership.id)


@pytest.fixture(scope="session")
def additional_group_room_memberships(membership_person_added_by_email,
                                      membership_person_added_by_id,
                                      membership_moderator_added_by_email,
                                      membership_moderator_added_by_id):
    return [
        membership_person_added_by_email,
        membership_person_added_by_id,
        membership_moderator_added_by_email,
        membership_moderator_added_by_id
    ]


@pytest.fixture(scope="session")
def group_room_with_members(group_room, additional_group_room_memberships):
    return group_room


# Tests

def test_list_memberships(my_memberships):
    assert len(my_memberships) >= 3
    assert are_valid_memberships(my_memberships)


def test_list_memberships_with_paging(api, add_rooms, my_memberships):
    page_size = 1
    pages = 3
    num_memberships = pages * page_size
    if len(my_memberships) < num_memberships:
        add_rooms(num_memberships - len(my_memberships))
    memberships = api.memberships.list(max=page_size)
    memberships_list = list(itertools.islice(memberships, num_memberships))
    assert len(memberships_list) == num_memberships
    assert are_valid_memberships(memberships_list)


def test_filter_room_memberships_by_person_email(api, test_people,
                                                 group_room_with_members):
    person = test_people["member_added_by_email"]
    memberships = list(api.memberships.list(
        roomId=group_room_with_members.id,
        personEmail=person.emails[0],
    ))
    assert len(memberships) == 1
    membership = memberships[0]
    assert is_valid_membership(membership)
    assert membership.roomId == group_room_with_members.id


def test_filter_room_memberships_by_person_id(api, test_people,
                                              group_room_with_members):
    person = test_people["member_added_by_id"]
    memberships = list(api.memberships.list(
        roomId=group_room_with_members.id,
        personId=person.id,
    ))
    assert len(memberships) == 1
    membership = memberships[0]
    assert is_valid_membership(membership)
    assert membership.roomId == group_room_with_members.id


def test_list_room_memberships(api, group_room_with_members):
    memberships = list(api.memberships.list(group_room_with_members.id))
    assert len(memberships) > 1
    assert are_valid_memberships(memberships)


def test_create_membership_by_email(membership_person_added_by_email):
    assert is_valid_membership(membership_person_added_by_email)


def test_create_membership_by_person_id(membership_person_added_by_id):
    assert is_valid_membership(membership_person_added_by_id)


def test_create_moderator_by_email(membership_moderator_added_by_email):
    assert is_valid_membership(membership_moderator_added_by_email)


def test_create_moderator_by_person_id(membership_moderator_added_by_id):
    assert is_valid_membership(membership_moderator_added_by_id)


def test_get_membership_details(api, membership_person_added_by_id):
    membership_id = membership_person_added_by_id.id
    details = api.memberships.get(membership_id)
    assert is_valid_membership(details)


def test_update_membership_make_moderator(api, membership_person_added_by_id):
    assert not membership_person_added_by_id.isModerator
    updated_membership = api.memberships.update(
        membershipId=membership_person_added_by_id.id,
        isModerator=True,
    )
    assert is_valid_membership(updated_membership)
    assert updated_membership.isModerator


def test_delete_membership(api, group_room, test_people):
    person = test_people["not_a_member"]
    membership = api.memberships.create(group_room.id, personId=person.id)
    assert is_valid_membership(membership)
    api.memberships.delete(membership.id)
