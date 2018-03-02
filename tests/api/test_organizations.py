# -*- coding: utf-8 -*-
"""pytest Organizations API wrapper tests and fixtures."""


import pytest

import ciscosparkapi


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


# Helper Functions

def get_list_of_organizations(api, max=None):
    return api.organizations.list(max=max)


def get_organization_by_id(api, orgId):
    return api.organizations.get(orgId)


def is_valid_organization(obj):
    return isinstance(obj, ciscosparkapi.Organization) and obj.id is not None

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
