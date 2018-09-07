# -*- coding: utf-8 -*-
"""WebexTeamsAPI Rooms API fixtures and tests.

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

def is_valid_room(obj):
    return isinstance(obj, webexteamssdk.Room) and obj.id is not None


def are_valid_rooms(iterable):
    return all([is_valid_room(obj) for obj in iterable])


# Fixtures

@pytest.fixture(scope="session")
def group_room(api):
    room = api.rooms.create(title=create_string("Group Room"))

    yield room

    api.rooms.delete(room.id)


@pytest.fixture(scope="session")
def direct_rooms(api, direct_messages):
    return [
        api.rooms.get(message.roomId)
        for message in direct_messages
    ]


@pytest.fixture(scope="session")
def team_room(api, team):
    team_room = api.rooms.create(
        title=create_string("Team Room"),
        teamId=team.id,
    )

    yield team_room

    api.rooms.delete(team_room.id)


@pytest.fixture(scope="session")
def list_of_rooms(api, group_room, direct_rooms, team_room):
    return list(api.rooms.list())


@pytest.fixture
def temp_room(api):
    room = api.rooms.create(title=create_string("Temp Room"))

    yield room

    try:
        api.rooms.delete(room.id)
    except webexteamssdk.ApiError:
        pass


@pytest.fixture
def add_rooms(api):
    rooms = []

    def inner(num_rooms):
        for i in range(num_rooms):
            rooms.append(api.rooms.create(create_string("Additional Room")))
        return rooms

    yield inner

    for room in rooms:
        try:
            api.rooms.delete(room.id)
        except webexteamssdk.ApiError:
            pass


# Tests

def test_list_all_rooms(list_of_rooms):
    assert len(list_of_rooms) > 0
    assert are_valid_rooms(list_of_rooms)


def test_list_rooms_with_paging(api, list_of_rooms, add_rooms):
    page_size = 1
    pages = 3
    num_rooms = pages * page_size
    if len(list_of_rooms) < num_rooms:
        add_rooms(num_rooms - len(list_of_rooms))
    rooms = api.rooms.list(max=page_size)
    rooms_list = list(itertools.islice(rooms, num_rooms))
    assert len(rooms_list) == num_rooms
    assert are_valid_rooms(rooms_list)


def test_list_group_rooms(api, group_room):
    group_rooms_list = list(api.rooms.list(type='group'))
    assert len(group_rooms_list) > 0
    assert are_valid_rooms(group_rooms_list)


def test_list_team_rooms(api, team, team_room):
    team_rooms_list = list(api.rooms.list(teamId=team.id))
    assert len(team_rooms_list) > 0
    assert are_valid_rooms(team_rooms_list)


def test_list_direct_rooms(api, direct_rooms):
    direct_rooms_list = list(api.rooms.list(type='direct'))
    assert len(direct_rooms_list) > 0
    assert are_valid_rooms(direct_rooms_list)


def test_create_group_room(group_room):
    assert is_valid_room(group_room)


def test_create_team_room(team_room):
    assert is_valid_room(team_room)


def test_get_room_details(api, group_room):
    room = api.rooms.get(group_room.id)
    assert is_valid_room(room)


def test_update_room_title(api, group_room):
    new_title = create_string("Updated Group Room")
    room = api.rooms.update(group_room.id, title=new_title)
    assert is_valid_room(room)
    assert room.title == new_title


def test_delete_room(api, temp_room):
    api.rooms.delete(temp_room.id)
