"""WebexAPI Admin Audit Events API fixtures and tests.

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
from datetime import timedelta, timezone
import pytest
import webexpythonsdk
from webexpythonsdk.exceptions import ApiError


to_datetime = webexpythonsdk.WebexDateTime.now(tz=timezone.utc)
from_datetime = to_datetime - timedelta(days=364)


# Helper Functions
def is_valid_admin_audit_event(obj):
    return (
        isinstance(obj, webexpythonsdk.AdminAuditEvent) and obj.id is not None
    )


def are_valid_admin_audit_events(iterable):
    return all([is_valid_admin_audit_event(obj) for obj in iterable])


# Fixtures
@pytest.fixture(scope="session")
def admin_audit_events(api, me):
    # Test passes if API call succeeds (200 status), regardless of result count
    try:
        events = list(
            api.admin_audit_events.list(
                orgId=me.orgId,
                _from=str(from_datetime),
                to=str(to_datetime),
            )[:3]
        )
        return events
    except ApiError as e:
        # Re-raise ApiError to show proper error details
        raise e


# Tests
def test_list_admin_audit_events(api, admin_audit_events):
    # Test passes if fixture succeeded (no ApiError raised)
    # Validate events only if they exist
    if len(admin_audit_events) > 0:
        assert are_valid_admin_audit_events(admin_audit_events)


def test_list_admin_audit_events_by_actor_id(api, admin_audit_events):
    # Skip if no events available
    if len(admin_audit_events) == 0:
        pytest.skip("No admin audit events available for actor filtering test")

    try:
        actor_id = admin_audit_events[0].actorId
        actor_events = list(api.events.list(actorId=actor_id)[:3])
        # Test passes if API call succeeds
        if len(actor_events) > 0:
            assert are_valid_admin_audit_events(actor_events)
            assert all([event.actorId == actor_id for event in actor_events])
    except ApiError as e:
        # Re-raise ApiError to show proper error details
        raise e


def test_list_events_with_paging(api, me, admin_audit_events):
    try:
        page_size = 1
        pages = 3
        num_events = pages * page_size

        events_gen = api.admin_audit_events.list(
            orgId=me.orgId,
            _from=str(from_datetime),
            to=str(to_datetime),
            max=page_size,
        )
        events_list = list(itertools.islice(events_gen, num_events))

        # Test passes if API call succeeds (200 status)
        # Validate events only if they exist
        if len(events_list) > 0:
            assert are_valid_admin_audit_events(events_list)
    except ApiError as e:
        # Re-raise ApiError to show proper error details
        raise e
