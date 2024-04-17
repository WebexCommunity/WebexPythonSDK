# -*- coding: utf-8 -*-
"""WebexTeamsAPI Recordings API fixtures and tests.

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
import os
from datetime import timedelta, timezone

import pytest

import webexteamssdk

to_datetime = webexteamssdk.WebexTeamsDateTime.now(tz=timezone.utc)
from_datetime = to_datetime - timedelta(days=364)


# Helper Functions
def is_valid_recording(obj):
    return isinstance(obj, webexteamssdk.Recording) and obj.id is not None


def are_valid_recording(iterable):
    return all([is_valid_recording(obj) for obj in iterable])


# Fixtures
@pytest.fixture(scope="session")
def list_recordings(api):
    return list(
        api.recordings.list(_from=str(from_datetime), to=str(to_datetime))
    )


@pytest.fixture(scope="session")
def recording_id(api, list_recordings):
    assert list_recordings > 0
    return list_recordings[0].id


# Tests
# We cannot create recordings programmatically, so we cannot automate testing
# of the Recordings API - we can only manually test the API after manually
# creating recordings.


@pytest.mark.manual
def test_recording_list(list_recordings):
    assert len(list_recordings) > 0
    assert are_valid_recording(list_recordings)


@pytest.mark.manual
def test_recording_detail(recording_id):
    assert is_valid_recording(recording_id)


@pytest.mark.manual
def test_delete_recording(api, recording_id):
    api.recordings.delete(recording_id)
