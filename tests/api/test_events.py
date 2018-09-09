# -*- coding: utf-8 -*-
"""WebexTeamsAPI Events API fixtures and tests.

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


# Helper Functions

def is_valid_event(obj):
    return isinstance(obj, webexteamssdk.Event) and obj.id is not None


def are_valid_events(iterable):
    return all([is_valid_event(obj) for obj in iterable])


# Fixtures

@pytest.fixture(scope="session")
def events(api, group_room_messages, direct_messages):
    five_events = list(api.events.list()[:5])
    assert len(five_events) == 5
    return five_events


# Tests

def test_list_events(api, events):
    assert are_valid_events(events)


def test_list_message_events(api, events):
    message_events = list(api.events.list(resource="messages")[:5])
    assert are_valid_events(message_events)
    assert all([event.resource == "messages" for event in message_events])


def test_list_membership_events(api, events):
    membership_events = list(api.events.list(resource="memberships")[:5])
    assert are_valid_events(membership_events)
    assert all(
        [event.resource == "memberships" for event in membership_events]
    )


def test_list_events_by_type(api, events):
    created_events = list(api.events.list(type="created")[:5])
    assert are_valid_events(created_events)
    assert all([event.type == "created" for event in created_events])


def test_list_events_by_actor_id(api, events):
    actor_id = events[0].actorId
    actor_events = list(api.events.list(actorId=actor_id)[:5])
    assert are_valid_events(actor_events)
    assert all([event.actorId == actor_id for event in actor_events])


def test_list_events_from(api, events):
    datetime_string = str(min(event.created for event in events))
    from_events = list(api.events.list(_from=datetime_string)[:5])
    assert are_valid_events(from_events)


def test_list_events_to(api, events):
    datetime_string = str(max(event.created for event in events))
    to_events = list(api.events.list(to=datetime_string)[:5])
    assert are_valid_events(to_events)


def test_list_events_with_paging(api, events):
    page_size = 1
    pages = 3
    num_events = pages * page_size
    assert len(events) >= num_events
    events_gen = api.events.list(max=page_size)
    events_list = list(itertools.islice(events_gen, num_events))
    assert len(events_list) == num_events
    assert are_valid_events(events_list)


def test_get_event_by_id(api, events):
    event_id = events[0].id
    event = api.events.get(event_id)
    assert is_valid_event(event)
