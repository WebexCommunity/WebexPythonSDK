# -*- coding: utf-8 -*-
"""WebexTeamsAPI Messages API fixtures and tests.

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

import json
import os

import pytest

import webexteamssdk
from tests.utils import create_string


# Module Variables
attachment_actions_card_path = os.path.abspath(
    os.path.join(__file__, os.pardir, "attachment_actions_card.json")
)


# Helper Functions
def is_valid_attachment_action(obj):
    return (
        isinstance(obj, webexteamssdk.AttachmentAction) and obj.id is not None
    )


# Fixtures
@pytest.fixture(scope="session")
def attachment_actions_card():
    with open(attachment_actions_card_path) as file:
        card = json.load(file)
    return card


@pytest.fixture(scope="session")
def attachment_action_create(api, test_people, attachment_actions_card):
    person = test_people["member_added_by_email"]
    message = api.messages.create(
        toPersonEmail=person.emails[0],
        text=create_string("Message"),
        attachments=[
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": attachment_actions_card,
            }
        ],
    )
    attachment_action = api.attachment_actions.create(
        type="submit",
        messageId=message.id,
        inputs={
            "Name": person.displayName,
            "Email": person.emails[0],
        },
    )

    yield attachment_action

    api.messages.delete(message.id)


# Tests
def test_attachment_actions_create(attachment_action_create):
    assert is_valid_attachment_action(attachment_action_create)


def test_attachment_actions_get(api, attachment_action_create):
    attachment_action = api.attachment_actions.get(attachment_action_create.id)
    assert is_valid_attachment_action(attachment_action)
