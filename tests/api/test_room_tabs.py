# -*- coding: utf-8 -*-
"""WebexTeamsAPI Rooms API fixtures and tests.

Copyright (c) 2016-2024 Cisco and/or its affiliates.

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
import os

import pytest

import webexteamssdk
from tests.utils import create_string

WEBEX_TEAMS_TEST_FILE_URL = os.environ.get("WEBEX_TEAMS_TEST_FILE_URL")

if not WEBEX_TEAMS_TEST_FILE_URL:
    pytest.skip(
        "WEBEX_TEAMS_TEST_FILE_URL environment variable is not set.",
        allow_module_level=True,
    )


# Helper Functions


def is_valid_room_tab(obj):
    return isinstance(obj, webexteamssdk.RoomTab) and obj.id is not None


def are_valid_room_tabs(iterable):
    return all([is_valid_room_tab(obj) for obj in iterable])


# Fixtures
@pytest.fixture(scope="session")
def room_tab(api, group_room):
    room_tab = api.room_tabs.create(
        roomId=group_room.id,
        contentUrl=WEBEX_TEAMS_TEST_FILE_URL,
        displayName=create_string("RoomTab"),
    )

    yield room_tab

    api.room_tabs.delete(room_tab.id)


@pytest.fixture()
def temp_room_tab(api, group_room):
    temp_room_tab = api.room_tabs.create(
        roomId=group_room.id,
        contentUrl=WEBEX_TEAMS_TEST_FILE_URL,
        displayName=create_string("RoomTab"),
    )

    yield temp_room_tab

    try:
        api.room_tabs.delete(temp_room_tab.id)
    except webexteamssdk.ApiError:
        pass


# Tests


def test_list_all_room_tabs(api, group_room, room_tab):
    all_room_tabs = list(api.room_tabs.list(roomId=group_room.id))
    assert len(all_room_tabs) > 0
    assert are_valid_room_tabs(all_room_tabs)


def test_create_room_tab(room_tab):
    assert is_valid_room_tab(room_tab)


def test_get_room_tab(api, room_tab):
    assert is_valid_room_tab(api.room_tabs.get(room_tab.id))


def test_update_room_tab(api, group_room, room_tab):
    new_display_name = create_string("RoomTab")
    updated_room_tab = api.room_tabs.update(
        roomTabId=room_tab.id,
        roomId=group_room.id,
        contentUrl=room_tab.contentUrl,
        displayName=new_display_name,
    )
    assert is_valid_room_tab(updated_room_tab)
    assert updated_room_tab.displayName == new_display_name


def test_delete_room_tab(api, temp_room_tab):
    api.room_tabs.delete(temp_room_tab.id)
