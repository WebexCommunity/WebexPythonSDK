# -*- coding: utf-8 -*-
"""pytest Messages functions, fixtures and tests."""


import itertools

import pytest

import ciscosparkapi


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


# Helper Functions

def is_valid_event(obj):
    return isinstance(obj, ciscosparkapi.Event) and obj.id is not None


def are_valid_events(iterable):
    return all([is_valid_event(obj) for obj in iterable])


# pytest Fixtures
@pytest.fixture(scope="session")
def events(api, group_room_messages, direct_messages):
    five_events = list(api.events.list()[:5])
    assert len(five_events) == 5
    return five_events


# Tests

class TestEventsAPI(object):
    """Test EventsAPI methods."""

    def test_list_events(self, api, events):
        assert are_valid_events(events)

    def test_list_message_events(self, api, events):
        message_events = list(api.events.list(resource="messages")[:5])
        assert are_valid_events(message_events)
        assert all([event.resource == "messages" for event in message_events])

    def test_list_membership_events(self, api, events):
        membership_events = list(api.events.list(resource="memberships")[:5])
        assert are_valid_events(membership_events)
        assert all(
            [event.resource == "memberships" for event in membership_events]
        )

    def test_list_events_by_type(self, api, events):
        created_events = list(api.events.list(type="created")[:5])
        assert are_valid_events(created_events)
        assert all([event.type == "created" for event in created_events])

    def test_list_events_by_actor_id(selfs, api, events):
        actor_id = events[0].actorId
        actor_events = list(api.events.list(actorId=actor_id)[:5])
        assert are_valid_events(actor_events)
        assert all([event.actorId == actor_id for event in actor_events])

    def test_list_events_from(selfs, api, events):
        datetime_string = min(event.created for event in events)
        from_events = list(api.events.list(_from=datetime_string)[:5])
        assert are_valid_events(from_events)

    def test_list_events_to(selfs, api, events):
        datetime_string = max(event.created for event in events)
        to_events = list(api.events.list(to=datetime_string)[:5])
        assert are_valid_events(to_events)

    def test_list_events_with_paging(self, api, events):
        page_size = 1
        pages = 3
        num_events = pages * page_size
        assert len(events) >= num_events
        events_gen = api.events.list(max=page_size)
        events_list = list(itertools.islice(events_gen, num_events))
        assert len(events_list) == num_events
        assert are_valid_events(events_list)

    def test_get_event_by_id(self, api, events):
        event_id = events[0].id
        event = api.events.get(event_id)
        assert is_valid_event(event)
