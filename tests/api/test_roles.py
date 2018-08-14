# -*- coding: utf-8 -*-
"""pytest Roles API wrapper tests and fixtures.

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

def get_list_of_roles(api, max=None):
    return api.roles.list(max=max)


def get_role_by_id(api, roleId):
    return api.roles.get(roleId)


def is_valid_role(obj):
    return isinstance(obj, webexteamssdk.Role) and obj.id is not None


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
        assert len(roles) > 1
        assert are_valid_roles(roles)

    def test_get_role_by_id(self, api, roles_list):
        assert len(roles_list) >= 1
        role_id = roles_list[0].id
        role = get_role_by_id(api, roleId=role_id)
        assert is_valid_role(role)
