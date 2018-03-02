# -*- coding: utf-8 -*-
"""pytest Rooms functions, fixtures and tests."""


import itertools

import pytest

import ciscosparkapi
from tests.utils import create_string


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


# Helper Functions

def create_room(api, title):
    return api.rooms.create(title)


def create_team_room(api, team, room_title):
    return api.rooms.create(room_title, teamId=team.id)


def delete_room(api, room):
    try:
        api.rooms.delete(room.id)
    except ciscosparkapi.SparkApiError as e:
        if e.response.status_code == 404:
            # Room doesn't exist
            pass
        else:
            raise


def is_valid_room(obj):
    return isinstance(obj, ciscosparkapi.Room) and obj.id is not None


def are_valid_rooms(iterable):
    return all([is_valid_room(obj) for obj in iterable])


def room_exists(api, room):
    try:
        api.rooms.get(room.id)
    except ciscosparkapi.SparkApiError:
        return False
    else:
        return True


# pytest Fixtures

@pytest.fixture(scope="session")
def group_room(api):
    room = create_room(api, create_string("Room"))
    yield room
    delete_room(api, room)


@pytest.fixture(scope="session")
def direct_rooms(api, direct_messages):
    return [api.rooms.get(message.roomId) for message in direct_messages]


@pytest.fixture(scope="session")
def team_room(api, team):
    team_room = create_team_room(api, team, create_string("Team Room"))
    yield team_room
    delete_room(api, team_room)


@pytest.fixture(scope="session")
def rooms_list(api, group_room, direct_rooms, team_room):
    return list(api.rooms.list())


@pytest.fixture
def temp_group_room(api):
    room = create_room(api, create_string("Room"))
    yield room
    if room_exists(api, room):
        delete_room(api, room)


@pytest.fixture
def add_rooms(api):
    rooms = []

    def inner(num_rooms):
        for i in range(num_rooms):
            rooms.append(create_room(api, create_string("Additional Room")))
        return rooms

    yield inner

    for room in rooms:
        delete_room(api, room)


# Tests

class TestRoomsAPI(object):
    """Test RoomsAPI methods."""

    def test_create_group_room(self, group_room):
        assert is_valid_room(group_room)

    def test_create_team_room(self, team_room):
        assert is_valid_room(team_room)

    def test_get_room_details(self, api, group_room):
        room = api.rooms.get(group_room.id)
        assert is_valid_room(room)

    def test_update_room_title(self, api, group_room):
        new_title = create_string("Updated Room")
        room = api.rooms.update(group_room.id, title=new_title)
        assert is_valid_room(room)
        assert room.title == new_title

    def test_delete_room(self, api, temp_group_room):
        # The delete method should complete without raising an exception
        api.rooms.delete(temp_group_room.id)
        # Spark API endpoints aren't updating fast enough, deleted teams are
        # still showing as existing via the `get` the API endpoint
        # assert not room_exists(api, temp_group_room)

    def test_list_group_rooms(self, api, group_room):
        group_rooms_list = list(api.rooms.list(type='group'))
        assert len(group_rooms_list) > 0
        assert are_valid_rooms(group_rooms_list)

    def test_list_team_rooms(self, api, team, team_room):
        team_rooms_list = list(api.rooms.list(teamId=team.id))
        assert len(team_rooms_list) > 0
        assert are_valid_rooms(team_rooms_list)

    def test_list_direct_rooms(self, api, direct_rooms):
        direct_rooms_list = list(api.rooms.list(type='direct'))
        assert len(direct_rooms_list) > 0
        assert are_valid_rooms(direct_rooms_list)

    def test_list_all_rooms(self, rooms_list):
        assert len(rooms_list) > 0
        assert are_valid_rooms(rooms_list)

    def test_list_rooms_with_paging(self, api, rooms_list, add_rooms):
        page_size = 1
        pages = 3
        num_rooms = pages * page_size
        if len(rooms_list) < num_rooms:
            add_rooms(num_rooms - len(rooms_list))
        rooms = api.rooms.list(max=page_size)
        rooms_list = list(itertools.islice(rooms, num_rooms))
        assert len(rooms_list) == num_rooms
        assert are_valid_rooms(rooms_list)
