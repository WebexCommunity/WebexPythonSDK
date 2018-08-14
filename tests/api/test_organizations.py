# -*- coding: utf-8 -*-
"""pytest Organizations API wrapper tests and fixtures.

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

def get_list_of_organizations(api, max=None):
    return api.organizations.list(max=max)


def get_organization_by_id(api, orgId):
    return api.organizations.get(orgId)


def is_valid_organization(obj):
    return isinstance(obj, webexteamssdk.Organization) and obj.id is not None

def are_valid_organizations(iterable):
    return all([is_valid_organization(obj) for obj in iterable])


# pytest Fixtures

@pytest.fixture(scope="session")
def organizations_list(api):
    return list(get_list_of_organizations(api))


# Tests

class TestOrganizationsAPI(object):
    """Test OrganizationsAPI methods."""

    def test_list_organizations(self, organizations_list):
        assert are_valid_organizations(organizations_list)

    def test_get_organization_by_id(self, api, organizations_list):
        assert len(organizations_list) >= 1
        organization_id = organizations_list[0].id
        organization = get_organization_by_id(api, orgId=organization_id)
        assert is_valid_organization(organization)
