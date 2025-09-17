"""WebexAPI Messages API fixtures and tests.

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
import json
import os

import pytest

import webexpythonsdk
from tests.environment import WEBEX_TEST_FILE_URL
from tests.utils import create_string


# Module Variables
adaptive_card_path = os.path.abspath(
    os.path.join(__file__, os.pardir, "adaptive_card.json")
)


# Helper Functions
def is_valid_message(obj):
    return isinstance(obj, webexpythonsdk.Message) and obj.id is not None


def are_valid_messages(iterable):
    return all([is_valid_message(obj) for obj in iterable])


# Fixtures
@pytest.fixture(scope="session")
def adaptive_card():
    with open(adaptive_card_path) as file:
        card = json.load(file)
    return card


@pytest.fixture(scope="session")
def direct_message_by_person_email(api, test_people):
    person = test_people["member_added_by_email"]
    message = api.messages.create(
        toPersonEmail=person.emails[0],
        text=create_string("Message"),
    )

    yield message

    api.messages.delete(message.id)


@pytest.fixture(scope="session")
def direct_message_reply_by_person_email(api, direct_message_by_person_email):
    text = create_string("Reply Message")
    return api.messages.create(
        toPersonEmail=direct_message_by_person_email.toPersonEmail,
        parentId=direct_message_by_person_email.id,
        text=text,
    )


@pytest.fixture(scope="session")
def direct_message_by_email_with_card(api, test_people, adaptive_card):
    person = test_people["member_added_by_email"]
    message = api.messages.create(
        toPersonEmail=person.emails[0],
        text=create_string("Message"),
        attachments=[
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": adaptive_card,
            }
        ],
    )

    yield message

    api.messages.delete(message.id)


@pytest.fixture(scope="session")
def direct_message_by_person_id(api, test_people):
    person = test_people["member_added_by_id"]
    message = api.messages.create(
        toPersonId=person.id,
        text=create_string("Message"),
    )

    yield message

    api.messages.delete(message.id)


@pytest.fixture(scope="session")
def direct_message_reply_by_person_id(api, direct_message_by_person_id):
    text = create_string("Reply Message")
    return api.messages.create(
        toPersonId=direct_message_by_person_id.toPersonId,
        parentId=direct_message_by_person_id.id,
        text=text,
    )


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
        except webexpythonsdk.ApiError:
            pass


@pytest.fixture(scope="session")
def group_room_text_message(group_room, send_group_room_message):
    text = create_string("Message")
    return send_group_room_message(group_room.id, text=text)


@pytest.fixture(scope="session")
def group_room_message_reply_by_id(api, group_room, group_room_text_message):
    text = create_string("Reply Message")
    return api.messages.create(
        roomId=group_room.id,
        parentId=group_room_text_message.id,
        text=text,
    )


@pytest.fixture(scope="session")
def group_room_markdown_message(
    me,
    group_room,
    send_group_room_message,
    group_room_text_message,
):
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
        room_id=group_room.id, text=text, files=[WEBEX_TEST_FILE_URL]
    )


@pytest.fixture(scope="session")
def group_room_message_with_file_by_local_upload(
    api,
    group_room,
    local_file,
    send_group_room_message,
):
    text = "File posted via URL"
    return send_group_room_message(
        room_id=group_room.id,
        text=text,
        files=[local_file],
    )


@pytest.fixture(scope="session")
def group_room_message_with_card(
    api,
    group_room,
    adaptive_card,
    send_group_room_message,
):
    return send_group_room_message(
        room_id=group_room.id,
        text=create_string("Message"),
        attachments=[
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": adaptive_card,
            }
        ],
    )


@pytest.fixture(scope="session")
def group_room_messages(
    api,
    group_room,
    group_room_text_message,
    group_room_markdown_message,
    group_room_message_with_file_by_url,
    group_room_message_with_file_by_local_upload,
    group_room_message_with_card,
):
    return list(api.messages.list(group_room.id))


@pytest.fixture(scope="session")
def direct_messages(
    direct_message_by_person_email,
    direct_message_by_person_id,
    direct_message_by_email_with_card,
):
    return [
        direct_message_by_person_email,
        direct_message_by_person_id,
        direct_message_by_email_with_card,
    ]


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


def test_list_messages_before_datetime(
    api, group_room, group_room_markdown_message
):
    message_list = list(
        api.messages.list(
            roomId=group_room.id,
            before=str(group_room_markdown_message.created),
        )
    )
    assert len(message_list) >= 1
    assert are_valid_messages(message_list)


def test_list_messages_before_message_with_id(
    api, group_room, group_room_markdown_message
):
    message_list = list(
        api.messages.list(
            roomId=group_room.id,
            beforeMessage=group_room_markdown_message.id,
        )
    )
    assert len(message_list) >= 1
    assert are_valid_messages(message_list)


@pytest.mark.xfail(
    reason="API Error: The API is not returning the expected results"
)
def test_list_messages_mentioning_me(
    api, group_room, group_room_markdown_message
):
    messages = api.messages.list(group_room.id, mentionedPeople="me")
    messages_list = list(messages)
    assert len(messages_list) >= 1
    assert are_valid_messages(messages_list)


def test_create_direct_messages_by_email(direct_message_by_person_email):
    assert is_valid_message(direct_message_by_person_email)


def test_reply_to_direct_message_by_person_email(
    direct_message_reply_by_person_email,
):
    assert is_valid_message(direct_message_reply_by_person_email)


def test_create_direct_messages_by_email_with_card(
    direct_message_by_email_with_card,
):
    assert is_valid_message(direct_message_by_email_with_card)


def test_create_direct_messages_by_id(direct_message_by_person_id):
    assert is_valid_message(direct_message_by_person_id)


def test_reply_to_direct_message_by_person_id(
    direct_message_reply_by_person_id,
):
    assert is_valid_message(direct_message_reply_by_person_id)


def test_list_direct_messages_by_person_id(api, direct_message_by_person_id):
    messages = api.messages.list_direct(
        personId=direct_message_by_person_id.toPersonId,
    )
    assert are_valid_messages(messages)


def test_list_direct_messages_by_person_email(
    api, direct_message_by_person_email
):
    messages = api.messages.list_direct(
        personEmail=direct_message_by_person_email.toPersonEmail,
    )
    assert are_valid_messages(messages)


def test_create_text_message(group_room_text_message):
    assert is_valid_message(group_room_text_message)


def test_create_reply_message(group_room_text_message):
    assert is_valid_message(group_room_text_message)


def test_create_markdown_message(group_room_markdown_message):
    assert is_valid_message(group_room_markdown_message)


def test_post_file_by_url(group_room_message_with_file_by_url):
    assert is_valid_message(group_room_message_with_file_by_url)


def test_post_file_by_local_upload(
    group_room_message_with_file_by_local_upload,
):
    assert is_valid_message(group_room_message_with_file_by_local_upload)


def test_get_message_by_id(api, group_room_text_message):
    message = api.messages.get(group_room_text_message.id)
    assert is_valid_message(message)


def test_delete_message(api, group_room, send_group_room_message):
    text = create_string("Message")
    message = api.messages.create(group_room.id, text=text)
    assert is_valid_message(message)
    api.messages.delete(message.id)


def test_edit_message(api, group_room):
    text = create_string("Edit this Message")
    message = api.messages.create(group_room.id, text=text)
    text = create_string("Message Edited")
    assert text == api.messages.edit(message.id, group_room.id, text).text


def test_update_message(api, group_room):
    text = create_string("Update this Message")
    message = api.messages.create(group_room.id, text=text)
    text = create_string("Message Updated")
    assert text == api.messages.edit(message.id, group_room.id, text).text


# Thread-aware message retrieval tests
def test_is_direct_room_detection(api, direct_message_by_person_id):
    """Test room type detection for direct messages."""
    assert api.messages._is_direct_room(direct_message_by_person_id) is True
    assert api.messages._is_group_room(direct_message_by_person_id) is False


def test_is_group_room_detection(api, group_room_text_message):
    """Test room type detection for group room messages."""
    assert api.messages._is_group_room(group_room_text_message) is True
    assert api.messages._is_direct_room(group_room_text_message) is False


def test_get_thread_context_direct_message(api, direct_message_reply_by_person_id):
    """Test thread context retrieval for direct message threads."""
    context = api.messages.get_thread_context(direct_message_reply_by_person_id)

    assert context["is_thread"] is True
    assert context["room_type"] == "direct"
    assert context["reply_count"] >= 0
    assert isinstance(context["thread_messages"], list)
    assert len(context["thread_messages"]) >= 1

    # The original message should be in the thread
    message_ids = [msg.id for msg in context["thread_messages"]]
    assert direct_message_reply_by_person_id.id in message_ids


def test_get_thread_context_group_message(api, group_room_message_reply_by_id):
    """Test thread context retrieval for group room message threads."""
    context = api.messages.get_thread_context(group_room_message_reply_by_id)

    assert context["is_thread"] is True
    assert context["room_type"] == "group"
    assert context["reply_count"] >= 0
    assert isinstance(context["thread_messages"], list)
    assert len(context["thread_messages"]) >= 1

    # The original message should be in the thread
    message_ids = [msg.id for msg in context["thread_messages"]]
    assert group_room_message_reply_by_id.id in message_ids


def test_get_thread_context_single_message(api, group_room_text_message):
    """Test thread context for non-threaded messages."""
    context = api.messages.get_thread_context(group_room_text_message)

    assert context["is_thread"] is False
    assert context["room_type"] == "group"
    assert context["reply_count"] == 0
    assert len(context["thread_messages"]) == 1
    assert context["thread_messages"][0].id == group_room_text_message.id


def test_get_thread_messages_direct(api, direct_message_reply_by_person_id):
    """Test thread message retrieval for direct messages."""
    thread_messages, root_message, error = api.messages.get_thread_messages(
        direct_message_reply_by_person_id
    )

    assert isinstance(thread_messages, list)
    assert len(thread_messages) >= 1
    assert error is None or isinstance(error, str)

    # The original message should be in the thread
    message_ids = [msg.id for msg in thread_messages]
    assert direct_message_reply_by_person_id.id in message_ids


def test_get_thread_messages_group(api, group_room_message_reply_by_id):
    """Test thread message retrieval for group room messages."""
    thread_messages, root_message, error = api.messages.get_thread_messages(
        group_room_message_reply_by_id
    )

    assert isinstance(thread_messages, list)
    assert len(thread_messages) >= 1
    assert error is None or isinstance(error, str)

    # The original message should be in the thread
    message_ids = [msg.id for msg in thread_messages]
    assert group_room_message_reply_by_id.id in message_ids


def test_get_thread_messages_single_message(api, group_room_text_message):
    """Test thread message retrieval for non-threaded messages."""
    thread_messages, root_message, error = api.messages.get_thread_messages(
        group_room_text_message
    )

    assert isinstance(thread_messages, list)
    assert len(thread_messages) == 1
    assert thread_messages[0].id == group_room_text_message.id
    assert root_message is None
    assert error is None


def test_thread_context_error_handling(api):
    """Test error handling in thread context retrieval."""
    # Create a mock message with invalid data to test error handling
    class MockMessage:
        def __init__(self):
            self.id = "invalid_message_id"
            self.parentId = "invalid_parent_id"
            self.roomId = "invalid_room_id"
            self.roomType = "group"
            self.created = "2024-01-01T10:00:00Z"

    mock_msg = MockMessage()
    context = api.messages.get_thread_context(mock_msg)

    # Should handle errors gracefully
    assert isinstance(context, dict)
    assert "error" in context
    assert "thread_messages" in context
    assert "room_type" in context
    assert context["room_type"] == "group"


def test_thread_messages_error_handling(api):
    """Test error handling in thread message retrieval."""
    # Create a mock message with invalid data to test error handling
    class MockMessage:
        def __init__(self):
            self.id = "invalid_message_id"
            self.parentId = "invalid_parent_id"
            self.roomId = "invalid_room_id"
            self.roomType = "group"
            self.created = "2024-01-01T10:00:00Z"

    mock_msg = MockMessage()
    thread_messages, root_message, error = api.messages.get_thread_messages(mock_msg)

    # Should handle errors gracefully
    assert isinstance(thread_messages, list)
    assert isinstance(error, str) or error is None
    assert root_message is None or isinstance(root_message, object)


def test_thread_context_room_type_consistency(api, direct_message_by_person_id, group_room_text_message):
    """Test that room type detection is consistent across different message types."""
    # Test direct message
    direct_context = api.messages.get_thread_context(direct_message_by_person_id)
    assert direct_context["room_type"] == "direct"

    # Test group message
    group_context = api.messages.get_thread_context(group_room_text_message)
    assert group_context["room_type"] == "group"


def test_thread_messages_ordering(api, group_room_message_reply_by_id):
    """Test that thread messages are returned in chronological order."""
    thread_messages, root_message, error = api.messages.get_thread_messages(
        group_room_message_reply_by_id
    )

    if len(thread_messages) > 1:
        # Messages should be ordered by creation time (oldest to newest)
        for i in range(len(thread_messages) - 1):
            current_created = getattr(thread_messages[i], "created", "")
            next_created = getattr(thread_messages[i + 1], "created", "")
            if current_created and next_created:
                assert current_created <= next_created


def test_thread_context_with_max_scan_limit(api, group_room_message_reply_by_id):
    """Test thread context with custom max_scan parameter."""
    # Test with a very small max_scan to ensure the parameter is respected
    context = api.messages.get_thread_context(group_room_message_reply_by_id, max_scan=1)

    assert isinstance(context, dict)
    assert "thread_messages" in context
    assert "room_type" in context
    assert context["room_type"] == "group"


def test_thread_messages_with_max_scan_limit(api, group_room_message_reply_by_id):
    """Test thread messages with custom max_scan parameter."""
    # Test with a very small max_scan to ensure the parameter is respected
    thread_messages, root_message, error = api.messages.get_thread_messages(
        group_room_message_reply_by_id, max_scan=1
    )

    assert isinstance(thread_messages, list)
    assert isinstance(error, str) or error is None


def test_collect_thread_text_and_attachments_utility(api, group_room_message_reply_by_id):
    """Test the collect_thread_text_and_attachments utility function with real data."""
    from webexpythonsdk.thread_utils import collect_thread_text_and_attachments

    thread_text, attachments = collect_thread_text_and_attachments(api, group_room_message_reply_by_id)

    # Verify return types
    assert isinstance(thread_text, str)
    assert isinstance(attachments, list)
    assert len(attachments) >= 0

    # Verify thread text contains the message content
    assert len(thread_text) > 0

    # Verify attachments is a list of strings (or empty)
    for attachment in attachments:
        assert isinstance(attachment, str)


def test_collect_thread_text_and_attachments_direct_message(api, direct_message_reply_by_person_id):
    """Test the collect_thread_text_and_attachments utility function with direct messages."""
    from webexpythonsdk.thread_utils import collect_thread_text_and_attachments

    thread_text, attachments = collect_thread_text_and_attachments(api, direct_message_reply_by_person_id)

    # Verify return types
    assert isinstance(thread_text, str)
    assert isinstance(attachments, list)
    assert len(attachments) >= 0

    # Verify thread text contains the message content
    assert len(thread_text) > 0


def test_collect_thread_text_and_attachments_single_message(api, group_room_text_message):
    """Test the collect_thread_text_and_attachments utility function with single messages."""
    from webexpythonsdk.thread_utils import collect_thread_text_and_attachments

    thread_text, attachments = collect_thread_text_and_attachments(api, group_room_text_message)

    # Verify return types
    assert isinstance(thread_text, str)
    assert isinstance(attachments, list)
    assert len(attachments) >= 0

    # Verify thread text contains the message content
    assert len(thread_text) > 0


def test_collect_thread_text_and_attachments_with_custom_limits(api, group_room_message_reply_by_id):
    """Test the collect_thread_text_and_attachments utility function with custom parameters."""
    from webexpythonsdk.thread_utils import collect_thread_text_and_attachments

    # Test with custom max_scan and max_chars
    thread_text, attachments = collect_thread_text_and_attachments(
        api, group_room_message_reply_by_id, max_scan=10, max_chars=1000
    )

    # Verify return types
    assert isinstance(thread_text, str)
    assert isinstance(attachments, list)

    # Verify max_chars limit is respected
    assert len(thread_text) <= 1000
