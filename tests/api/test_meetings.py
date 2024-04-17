# -*- coding: utf-8 -*-
"""WebexTeamsAPI Meetings API fixtures and tests.

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

import pytest
import datetime

import webexteamssdk

from tests.utils import create_string

# Helper Functions


def is_valid_meeting(obj):
    return isinstance(obj, webexteamssdk.Meeting) and obj.id is not None


def get_start_end_time():
    now = datetime.datetime.now()
    start = (now + datetime.timedelta(days=1)).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )  # tomorrow same time
    end = (now + datetime.timedelta(days=1, hours=1)).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )  # tomorrow 1 hour later
    return {"start": start, "end": end}


# Fixtures


@pytest.fixture(scope="session")
def meeting(api):
    meeting = api.meetings.create(
        title=create_string("Meeting"), **get_start_end_time()
    )

    yield meeting

    try:
        api.meetings.delete(meeting.id)
    except webexteamssdk.ApiError:
        pass


@pytest.fixture(scope="session")
def webinar(api):
    webinar = api.meetings.create(
        title=create_string("Webinar"),
        scheduledType="webinar",
        **get_start_end_time(),
    )

    yield webinar

    try:
        api.meetings.delete(webinar.id)
    except webexteamssdk.ApiError:
        pass


# Tests


def test_create_meeting(meeting):
    assert is_valid_meeting(meeting)


def test_create_webinar(webinar):
    assert is_valid_meeting(webinar)
    assert webinar.scheduledType == "webinar"


def test_get_meeting(api, meeting, webinar):
    assert is_valid_meeting(api.meetings.get(meeting.id))
    assert (
        is_valid_meeting(api.meetings.get(webinar.id))
        and api.meetings.get(webinar.id).scheduledType == "webinar"
    )


def test_list_meetings(api, meeting, webinar):
    meetings_list = list(api.meetings.list())
    assert len(meetings_list) > 0
    all_ids = [item.id for item in meetings_list]
    assert meeting.id in all_ids
    assert webinar.id in all_ids


def test_update_meeting_title(api, meeting):
    new_title = create_string("Updates Meeting")
    updated_meeting = api.meetings.update(
        meeting.id,
        title=new_title,
        password=meeting.password,
        start=meeting.start,
        end=meeting.end,
    )
    assert is_valid_meeting(updated_meeting)
    assert updated_meeting.title == new_title


def test_delete_meeting(api, meeting):
    api.meetings.delete(meeting.id)
