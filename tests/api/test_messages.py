# -*- coding: utf-8 -*-

"""pytest Messages functions, fixtures and tests."""


import pytest

import ciscosparkapi
from tests.utils import create_string


# Helper Functions




# pytest Fixtures

@pytest.fixture(scope="session")
def direct_messages(api, email_addresses):
    msg_text = create_string("Message")
    messages = []
    for email in email_addresses:
        messages.append(api.messages.create(toPersonEmail=email,
                                            text=msg_text))
    yield messages
    delete_messages(api, messages)


def delete_messages(api, messages):
    for message in messages:
        api.messages.delete(message.id)
