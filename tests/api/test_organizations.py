# -*- coding: utf-8 -*-
"""WebexTeamsAPI Organizations API fixtures and tests.

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

import pytest

import webexteamssdk


# Helper Functions

def is_valid_organization(obj):
    return isinstance(obj, webexteamssdk.Organization) and obj.id is not None


def are_valid_organizations(iterable):
    return all([is_valid_organization(obj) for obj in iterable])


# Fixtures

@pytest.fixture(scope="session")
def organizations_list(api):
    return list(api.organizations.list())


# Tests

def test_list_organizations(organizations_list):
    assert are_valid_organizations(organizations_list)


def test_get_organization_by_id(api, organizations_list):
    assert len(organizations_list) >= 1
    organization_id = organizations_list[0].id
    organization = api.organizations.get(organization_id)
    assert is_valid_organization(organization)
