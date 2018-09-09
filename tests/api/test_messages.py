# -*- coding: utf-8 -*-
"""WebexTeamsAPI Messages API fixtures and tests.

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
from tests.environment import WEBEX_TEAMS_TEST_FILE_URL
from tests.utils import create_string


# Helper Functions

def is_valid_message(obj):
    return isinstance(obj, webexteamssdk.Message) and obj.id is not None


def are_valid_messages(iterable):
    return all([is_valid_message(obj) for obj in iterable])


# Fixtures

@pytest.fixture(scope="session")
def direct_message_by_email(api, test_people):
    person = test_people["member_added_by_email"]
    message = api.messages.create(
        toPersonEmail=person.emails[0],
        text=create_string("Message"),
    )

    yield message

    api.messages.delete(message.id)


@pytest.fixture(scope="session")
def direct_message_by_id(api, test_people):
    person = test_people["member_added_by_id"]
    message = api.messages.create(
        toPersonId=person.id,
        text=create_string("Message"),
    )

    yield message

    api.messages.delete(message.id)


@pytest.fixture(scope="session")
def send_group_room_message(api):
    messages = []

    def inner_function(room_id, **message_attributes):
        new_message = api.messages.create(roomId=room_id, **message_attributes)
        messages.append(new_message)
        return new_message

    yield inner_function

    for message in messages:
        try:
            api.messages.delete(message.id)
        except webexteamssdk.ApiError:
            pass


@pytest.fixture(scope="session")
def group_room_text_message(group_room, send_group_room_message):
    text = create_string("Message")
    return send_group_room_message(group_room.id, text=text)


@pytest.fixture(scope="session")
def group_room_markdown_message(group_room, send_group_room_message, me,
                                group_room_text_message):
    # Uses / depends-on group_room_text_message to ensure this message is
    # created after group_room_text_message, so that we can be sure that a
    # message exists 'before' this one - used to test 'before' list filters.
    markdown = create_string(
        "<@personId:{id}|{name}>, This is **markdown** with a mention."
        "".format(id=me.id, name=me.displayName)
    )
    return send_group_room_message(group_room.id, markdown=markdown)


@pytest.fixture(scope="session")
def group_room_message_with_file_by_url(group_room, send_group_room_message):
    text = "File posted via URL"
    return send_group_room_message(
        room_id=group_room.id,
        text=text,
        files=[WEBEX_TEAMS_TEST_FILE_URL]
    )


@pytest.fixture(scope="session")
def group_room_message_with_file_by_local_upload(api, group_room, local_file,
                                                 send_group_room_message):
    text = "File posted via URL"
    return send_group_room_message(
        room_id=group_room.id,
        text=text,
        files=[local_file],
    )


@pytest.fixture(scope="session")
def group_room_messages(api, group_room,
                        group_room_text_message,
                        group_room_markdown_message,
                        group_room_message_with_file_by_url,
                        group_room_message_with_file_by_local_upload):
    return list(api.messages.list(group_room.id))


@pytest.fixture(scope="session")
def direct_messages(api, direct_message_by_email, direct_message_by_id):
    return [direct_message_by_email, direct_message_by_id]


# Tests

def test_list_all_messages(group_room_messages):
    assert len(group_room_messages) >= 1
    assert are_valid_messages(group_room_messages)


def test_list_messages_with_paging(api, group_room, group_room_messages):
    page_size = 1
    pages = 3
    num_messages = pages * page_size
    assert len(group_room_messages) >= num_messages
    messages = api.messages.list(group_room.id, max=page_size)
    messages_list = list(itertools.islice(messages, num_messages))
    assert len(messages_list) == num_messages
    assert are_valid_messages(messages_list)


def test_list_messages_before_datetime(api, group_room,
                                       group_room_markdown_message):
    message_list = list(api.messages.list(
        roomId=group_room.id,
        before=str(group_room_markdown_message.created),
    ))
    assert len(message_list) >= 1
    assert are_valid_messages(message_list)


def test_list_messages_before_message_with_id(api, group_room,
                                              group_room_markdown_message):
    message_list = list(api.messages.list(
        roomId=group_room.id,
        beforeMessage=group_room_markdown_message.id,
    ))
    assert len(message_list) >= 1
    assert are_valid_messages(message_list)


def test_list_messages_mentioning_me(api, group_room,
                                     group_room_markdown_message):
    messages = api.messages.list(group_room.id, mentionedPeople="me")
    messages_list = list(messages)
    assert len(messages_list) >= 1
    assert are_valid_messages(messages_list)


def test_create_direct_messages_by_email(direct_message_by_email):
    assert is_valid_message(direct_message_by_email)


def test_create_direct_messages_by_id(direct_message_by_id):
    assert is_valid_message(direct_message_by_id)


def test_create_text_message(group_room_text_message):
    assert is_valid_message(group_room_text_message)


def test_create_markdown_message(group_room_markdown_message):
    assert is_valid_message(group_room_markdown_message)


def test_post_file_by_url(group_room_message_with_file_by_url):
    assert is_valid_message(group_room_message_with_file_by_url)


def test_post_file_by_local_upload(
        group_room_message_with_file_by_local_upload):
    assert is_valid_message(group_room_message_with_file_by_local_upload)


def test_get_message_by_id(api, group_room_text_message):
    message = api.messages.get(group_room_text_message.id)
    assert is_valid_message(message)


def test_delete_message(api, group_room, send_group_room_message):
    text = create_string("Message")
    message = api.messages.create(group_room.id, text=text)
    assert is_valid_message(message)
    api.messages.delete(message.id)
    with pytest.raises(webexteamssdk.ApiError):
        api.messages.get(message.id)
