# -*- coding: utf-8 -*-

"""pytest Roles API wrapper tests and fixtures."""


import pytest

import ciscosparkapi


# Helper Functions

def get_list_of_roles(api, max=None):
    return api.roles.list(max=max)


def get_role_by_id(api, roleId):
    return api.roles.get(roleId)


def is_valid_role(obj):
    return isinstance(obj, ciscosparkapi.Role) and obj.id is not None


def are_valid_roles(iterable):
    return all([is_valid_role(obj) for obj in iterable])


# pytest Fixtures

@pytest.fixture(scope="session")
def roles_list(api):
    return list(get_list_of_roles(api))


@pytest.fixture(scope="session")
def roles_dict(roles_list):
    return {role.name: role for role in roles_list}


# Tests

class TestRolesAPI(object):
    """Test RolesAPI methods."""

    def test_list_roles(self, roles_list):
        assert are_valid_roles(roles_list)

    def test_list_roles_with_paging(self, api):
        paging_generator = get_list_of_roles(api, max=1)
        roles = list(paging_generator)
        assert roles > 1
        assert are_valid_roles(roles)

    def test_get_role_by_id(self, api, roles_list):
        assert len(roles_list) >= 1
        role_id = roles_list[0].id
        role = get_role_by_id(api, roleId=role_id)
        assert is_valid_role(role)
