# -*- coding: utf-8 -*-

"""pytest Licenses functions, fixtures and tests."""


import pytest

import ciscosparkapi


# Helper Functions

def list_organizations(api, max=None):
    return list(api.organizations.list(max=max))


def get_organization_by_id(api, orgId):
    return api.organizations.get(orgId)


def is_valid_organization(obj):
    return isinstance(obj, ciscosparkapi.Organization) and obj.id is not None

def are_valid_organizations(iterable):
    return all([is_valid_organization(obj) for obj in iterable])


# pytest Fixtures

@pytest.fixture(scope="session")
def organizations_list(api):
    return list_organizations(api)


# Tests

class TestOrganizationsAPI(object):
    """Test OrganizationsAPI methods."""

    def test_list_organizations(self, organizations_list):
        assert are_valid_organizations(organizations_list)

    def test_get_organization_by_id(self, api, organizations_list):
        assert len(organizations_list) >= 1
        org_id = organizations_list[0].id
        org = get_organization_by_id(api, orgId=org_id)
        assert is_valid_organization(org)
