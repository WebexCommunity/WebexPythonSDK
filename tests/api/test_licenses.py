# -*- coding: utf-8 -*-
"""pytest Licenses API wrapper tests and fixtures.

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

def get_list_of_licenses(api, orgId=None, max=None):
    return api.licenses.list(orgId=orgId, max=max)


def get_license_by_id(api, licenseId):
    return api.licenses.get(licenseId)


def is_valid_license(obj):
    return isinstance(obj, webexteamssdk.License) and obj.id is not None


def are_valid_licenses(iterable):
    return all([is_valid_license(obj) for obj in iterable])


# pytest Fixtures

@pytest.fixture(scope="session")
def licenses_list(api):
    return list(get_list_of_licenses(api))


@pytest.fixture(scope="session")
def licenses_dict(licenses_list):
    return {lic.name: lic for lic in licenses_list}


# Tests

class TestLicensesAPI(object):
    """Test LicensesAPI methods."""

    def test_list_licenses(self, licenses_list):
        assert are_valid_licenses(licenses_list)

    def test_list_licenses_with_paging(self, api):
        paging_generator = get_list_of_licenses(api, max=1)
        licenses = list(paging_generator)
        assert len(licenses) > 1
        assert are_valid_licenses(licenses)

    def test_get_licenses_for_organization(self, api, me):
        licenses = list(get_list_of_licenses(api, orgId=me.orgId))
        assert are_valid_licenses(licenses)

    def test_get_license_by_id(self, api, licenses_list):
        assert len(licenses_list) >= 1
        license_id = licenses_list[0].id
        license = get_license_by_id(api, licenseId=license_id)
        assert is_valid_license(license)
