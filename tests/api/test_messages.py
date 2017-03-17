# -*- coding: utf-8 -*-

"""pytest Messages functions, fixtures and tests."""


import pytest

import ciscosparkapi
from tests.utils import create_string


# Helper Functions

def send_direct_message_to_email(api, email, message=None):
    msg_text = message if message else create_string("Message")
    return api.messages.create(toPersonEmail=email, text=msg_text)


def delete_message(api, message):
    api.messages.delete(message.id)


def delete_messages(api, messages):
    for message in messages:
        delete_message(api, message)


# pytest Fixtures

@pytest.fixture(scope="session")
def direct_messages(api, additional_group_room_memberships, test_people):
    # Using additional_group_room_memberships to ensure some test_people
    # have been created
    direct_messages = []
    for person in test_people:
        message = send_direct_message_to_email(api, person.emails[0])
        direct_messages.append(message)

    yield direct_messages

    for message in direct_messages:
        delete_message(api, message)


@pytest.fixture(scope="session")
def send_direct_message(api):

    def inner_function(email_address, message=None):
        send_direct_message_to_email(api, email_address, message=message)

    return inner_function
