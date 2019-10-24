# -*- coding: utf-8 -*-
"""WebexTeamsAPI Messages API fixtures and tests.

Copyright (c) 2016-2019 Cisco and/or its affiliates.

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

def is_valid_attachment_action(obj):
    return isinstance(obj, webexteamssdk.AttachmentAction) \
        and obj.id is not None


# Fixtures

@pytest.fixture(scope="session")
def attachment_action_create(api, test_people):
    person = test_people["member_added_by_email"]
    message = api.messages.create(
        toPersonEmail=person.emails[0],
        text=create_string("Message"),
        attachments=[{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": ("http://adaptivecards.io/schemas/"
                            "adaptive-card.json"),
                "type": "AdaptiveCard",
                "version": "1.0",
                "body": [{
                    "type": "ColumnSet",
                    "columns": [{
                        "type": "Column",
                        "width": 2,
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Tell us about your problem",
                                "weight": "bolder",
                                "size": "medium"
                            },
                            {
                                "type": "TextBlock",
                                "text": "Your name",
                                "wrap": True
                            },
                            {
                                "type": "Input.Text",
                                "id": "Name",
                                "placeholder": "John Andersen"
                            },
                            {
                                "type": "TextBlock",
                                "text": "Your email",
                                "wrap": True
                            },
                            {
                                "type": "Input.Text",
                                "id": "Email",
                                "placeholder": "john.andersen@example.com",
                                "style": "email"
                            },
                        ]
                    }]
                }],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit"
                    }
                ]
            }
        }]
    )
    attachment_action = api.attachment_actions.create(
        type="submit", messageId=message.id,
        inputs={"Name": "test_name", "Email": "test_email"}
    )
    yield attachment_action

    api.messages.delete(message.id)

# Tests


def test_attachment_actions_create(attachment_action_create):
    assert is_valid_attachment_action(attachment_action_create)


def test_attachment_actions_get(api, attachment_action_create):
    attachment_action = api.attachment_actions.get(attachment_action_create.id)
    assert is_valid_attachment_action(attachment_action)
