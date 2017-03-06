# -*- coding: utf-8 -*-

"""pytest Memberships functions, fixtures and tests."""


import pytest

import ciscosparkapi


# Helper Functions

def add_people_to_room(api, room, emails):
    for email in emails:
        api.memberships.create(room.id, personEmail=email)


def empty_room(api, me, room):
    """Remove all memberships from a room (except the caller's membership)."""
    memberships = api.memberships.list(room.id)
    for membership in memberships:
        if membership.personId != me.id:
            api.memberships.delete(membership.id)


# pytest Fixtures

@pytest.fixture(scope="session")
def group_room_with_members(api, me, group_room, email_addresses):
    add_people_to_room(api, group_room, email_addresses)
    yield group_room
    empty_room(api, me, group_room)


@pytest.fixture(scope="session")
def team_room_with_members(api, me, team_room, email_addresses):
    add_people_to_room(api, team_room, email_addresses)
    yield team_room
    empty_room(api, me, team_room)


@pytest.fixture
def temp_group_room_with_members(api, me, temp_group_room, email_addresses):
    add_people_to_room(api, temp_group_room, email_addresses)
    yield temp_group_room
    empty_room(api, me, temp_group_room)

