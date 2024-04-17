# -*- coding: utf-8 -*-
"""WebexTeamsAPI MeetingRegistrants API fixtures and tests.

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


def is_valid_registrant(obj):
    return (
        isinstance(obj, webexteamssdk.MeetingRegistrant) and obj.id is not None
    )


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
        registration={
            "autoAcceptRequest": True,
            "requireFirstName": True,
            "requireLastName": True,
            "requireEmail": True,
        },
        **get_start_end_time(),
    )

    yield webinar

    try:
        api.meetings.delete(webinar.id)
    except webexteamssdk.ApiError:
        pass


@pytest.fixture(scope="session")
def registrant(api, webinar):
    registrant = api.meeting_registrants.create(
        webinar.id,
        firstName=create_string("FirstName"),
        lastName=create_string("LastName"),
        email="someone@example.com",
    )

    yield registrant

    try:
        api.meeting_registrants.delete(webinar.id, registrant.id)
    except webexteamssdk.ApiError:
        pass


# Tests


def test_register_for_meeting(api, meeting):
    # it is expected that registration does not work for a plain meeting
    with pytest.raises(webexteamssdk.ApiError) as ex_info:
        api.meeting_registrants.create(
            meeting.id,
            firstName=create_string("FirstName"),
            lastName=create_string("LastName"),
            email="someone@example.com",
        )
    assert ex_info.value.status_code == 400
    assert (
        ex_info.value.response.json()["errors"][0]["description"]
        == "Registration is not supported for this meeting series."
    )


def test_register_for_webinar(api, registrant):
    assert is_valid_registrant(registrant)


def test_get_registrant(api, webinar, registrant):
    assert is_valid_registrant(
        api.meeting_registrants.get(webinar.id, registrant.id)
    )


def test_list_registrants(api, webinar, registrant):
    registrants_list = list(api.meeting_registrants.list(webinar.id))
    assert len(registrants_list) > 0
    assert registrant.id in [item.id for item in registrants_list]


def test_unregister(api, webinar, registrant):
    api.meeting_registrants.delete(webinar.id, registrant.id)
