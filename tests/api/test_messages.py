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
def direct_message_person_1(api, get_new_email_address):
    message = send_direct_message_to_email(api, get_new_email_address())
    yield message
    delete_message(api, message)


@pytest.fixture(scope="session")
def direct_message_person_2(api, get_new_email_address):
    message = send_direct_message_to_email(api, get_new_email_address())
    yield message
    delete_message(api, message)


@pytest.fixture(scope="session")
def direct_message_person_3(api, get_new_email_address):
    message = send_direct_message_to_email(api, get_new_email_address())
    yield message
    delete_message(api, message)


@pytest.fixture(scope="session")
def direct_message_person_4(api, get_new_email_address):
    message = send_direct_message_to_email(api, get_new_email_address())
    yield message
    delete_message(api, message)


@pytest.fixture(scope="session")
def direct_messages(direct_message_person_1, direct_message_person_2,
                    direct_message_person_3, direct_message_person_4):
    return [direct_message_person_1, direct_message_person_2,
            direct_message_person_3, direct_message_person_4]

@pytest.fixture(scope="session")
def send_direct_message(api):
    def inner_function(email_address, message=None):
        send_direct_message_to_email(api, email_address, message=message)
    return inner_function
