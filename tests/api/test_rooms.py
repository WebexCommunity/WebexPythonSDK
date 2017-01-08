# -*- coding: utf-8 -*-

"""pytest Rooms functions, fixtures and tests."""


import pytest

import ciscosparkapi
from tests.utils import create_string


NUM_MULTIPLE_ROOMS = 10


# Helper Functions

def create_room(api, title):
    return api.rooms.create(title)


def create_team_room(api, team, room_title):
    return api.rooms.create(room_title, teamId=team.id)


def delete_room(api, room):
    api.rooms.delete(room.id)


# pytest Fixtures

@pytest.fixture(scope="session")
def direct_rooms(api, direct_messages):
    return [api.rooms.get(message.roomId) for message in direct_messages]


@pytest.fixture(scope="session")
def group_room(api):
    room = create_room(api, create_string("Room"))
    yield room
    delete_room(api, room)


@pytest.fixture(scope="session")
def team_room(api, team):
    team_room =  create_team_room(api, team, create_string("Team Room"))
    yield team_room
    delete_room(api, team_room)


@pytest.fixture(scope="session")
def ten_group_rooms(api):
    rooms =  [create_room(api, create_string("Room")) for i in range(10)]
    yield rooms
    for room in rooms:
        delete_room(api, room)


@pytest.fixture
def temp_group_room(api):
    room =  create_room(api, create_string("Room"))
    yield room
    delete_room(api, room)


# Room Tests

class TestRoomsAPI(object):
    """Test RoomsAPI methods."""

    @pytest.mark.usefixtures("group_room")
    def test_list_all_rooms(self, api):
        rooms_list = list(api.rooms.list())
        assert len(rooms_list) > 0

    @pytest.mark.usefixtures("ten_group_rooms")
    def test_list_all_rooms_with_paging(self, api):
        rooms_list = list(api.rooms.list(max=5))
        assert len(rooms_list) >= 10

    @pytest.mark.usefixtures("group_room")
    def test_list_group_rooms(self, api):
        group_rooms_list = list(api.rooms.list(type='group'))
        assert len(group_rooms_list) > 0

    @pytest.mark.usefixtures("direct_rooms")
    def test_list_direct_rooms(self, api):
        direct_rooms_list = list(api.rooms.list(type='direct'))
        assert len(direct_rooms_list) > 0

    @pytest.mark.usefixtures("team_room")
    def test_list_team_rooms(self, api, team):
        team_rooms_list = list(api.rooms.list(teamId=team.id))
        assert len(team_rooms_list) > 0

    def test_create_room(self, group_room):
        assert isinstance(group_room, ciscosparkapi.Room) \
               and group_room.id is not None
