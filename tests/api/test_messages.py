# -*- coding: utf-8 -*-
"""pytest Messages functions, fixtures and tests."""


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


import itertools

import pytest

import ciscosparkapi
from tests.conftest import TEST_FILE_URL
from tests.utils import create_string, download_file


# Helper Functions

def create_message(api, **message_attributes):
    return api.messages.create(**message_attributes)


def get_message_by_id(api, id):
    return api.messages.get(id)


def delete_message(api, message):
    api.messages.delete(message.id)


def delete_messages(api, iterable):
    for message in iterable:
        delete_message(api, message)


def list_messages(api, roomId, **query_parameters):
    return list(api.messages.list(roomId, **query_parameters))


def is_valid_message(obj):
    return isinstance(obj, ciscosparkapi.Message) and obj.id is not None


def are_valid_messages(iterable):
    return all([is_valid_message(obj) for obj in iterable])


def message_exists(api, message):
    try:
        api.messages.get(message.id)
    except ciscosparkapi.SparkApiError:
        return False
    else:
        return True


# pytest Fixtures

@pytest.fixture(scope="session")
def direct_message_by_email(api, test_people):
    person = test_people["member_added_by_email"]
    message = create_message(api, toPersonEmail=person.emails[0],
                             text=create_string("Message"))

    yield message

    delete_message(api, message)


@pytest.fixture(scope="session")
def direct_message_by_id(api, test_people):
    person = test_people["member_added_by_id"]
    message = create_message(api, toPersonId=person.id,
                             text=create_string("Message"))

    yield message

    delete_message(api, message)


@pytest.fixture(scope="session")
def send_group_room_message(api):
    messages = []

    def inner_function(roomId, **message_attributes):
        message = create_message(api, roomId=roomId, **message_attributes)
        messages.append(message)
        return message

    yield inner_function

    for message in messages:
        try:
            delete_message(api, message)
        except ciscosparkapi.SparkApiError as e:
            pass


@pytest.fixture(scope="session")
def group_room_text_message(group_room, send_group_room_message):
    text = create_string("Message")
    return send_group_room_message(group_room.id, text=text)


@pytest.fixture(scope="session")
def group_room_markdown_message(group_room, send_group_room_message, me,
                                group_room_member_added_by_email,
                                group_room_text_message):
    # Uses / depends on group_room_text_message to ensure this message is
    # created after group_room_text_message, so that we can be sure that a
    # message exists 'before' this one - used to test 'before' list filters.
    markdown = create_string("<@personEmail:{email}|{name}>, This is "
                             "**markdown** with a mention."
                             "".format(email=me.emails[0],
                                       name=me.displayName))
    return send_group_room_message(group_room.id, markdown=markdown)


@pytest.fixture(scope="session")
def group_room_file_by_URL_message(group_room, send_group_room_message):
    text = "File posted via URL"
    return send_group_room_message(group_room.id, text=text,
                                      files=[TEST_FILE_URL])


@pytest.fixture(scope="session")
def group_room_file_by_local_upload_message(api, group_room, local_file,
                                            send_group_room_message):
    text = "File posted via URL"
    return send_group_room_message(group_room.id, text=text,
                                   files=[local_file])


@pytest.fixture(scope="session")
def group_room_messages(api, group_room,
                        group_room_text_message,
                        group_room_markdown_message,
                        group_room_file_by_URL_message,
                        group_room_file_by_local_upload_message):
    return list(list_messages(api, group_room.id))


@pytest.fixture(scope="session")
def direct_messages(api, direct_message_by_email, direct_message_by_id):
    return [direct_message_by_email, direct_message_by_id]


# Tests

class TestMessagesAPI(object):
    """Test MessagesAPI methods."""

    def test_create_direct_messages_by_email(self, direct_message_by_email):
        assert is_valid_message(direct_message_by_email)

    def test_create_direct_messages_by_id(self, direct_message_by_id):
        assert is_valid_message(direct_message_by_id)

    def test_create_text_message(self, group_room_text_message):
        assert is_valid_message(group_room_text_message)

    def test_create_markdown_message(self, group_room_markdown_message):
        assert is_valid_message(group_room_markdown_message)

    def test_post_file_by_url(self, group_room_file_by_URL_message):
        assert is_valid_message(group_room_file_by_URL_message)

    def test_post_file_by_local_upload(self, group_room_file_by_local_upload_message):
        assert is_valid_message(group_room_file_by_local_upload_message)

    def test_get_message_by_id(self, api, group_room_text_message):
        message = get_message_by_id(api, group_room_text_message.id)
        assert is_valid_message(message)

    def test_delete_message(self, api, group_room, send_group_room_message):
        text = create_string("Message")
        message = create_message(api, roomId=group_room.id, text=text)
        assert is_valid_message(message)
        delete_message(api, message)
        assert not message_exists(api, message)

    def test_list_all_messages_in_room(self, group_room_messages):
        assert len(group_room_messages) >= 1
        assert are_valid_messages(group_room_messages)

    def test_list_messages_before(self, api, group_room,
                                  group_room_markdown_message):
        message_list = list_messages(api, group_room.id,
                                     before=group_room_markdown_message.created)
        assert len(message_list) >= 1
        assert are_valid_messages(message_list)

    def test_list_messages_before_message(self, api, group_room,
                                          group_room_markdown_message):
        message_list = list_messages(api, group_room.id,
                                     beforeMessage=group_room_markdown_message.id)
        assert len(message_list) >= 1
        assert are_valid_messages(message_list)

    def test_list_messages_with_paging(self, api, group_room,
                                       group_room_messages):
        page_size = 1
        pages = 3
        num_messages = pages * page_size
        assert len(group_room_messages) >= num_messages
        messages = list_messages(api, group_room.id, max=page_size)
        messages_list = list(itertools.islice(messages, num_messages))
        assert len(messages_list) == num_messages
        assert are_valid_messages(messages_list)

    def test_list_messages_mentioning_me(self, api, group_room,
                                         group_room_markdown_message):
        messages = list_messages(api, group_room.id, mentionedPeople="me")
        messages_list = list(messages)
        assert len(messages_list) >= 1
        assert are_valid_messages(messages_list)
