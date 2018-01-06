# -*- coding: utf-8 -*-
"""pytest Licenses API wrapper tests and fixtures."""


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


import pytest

import ciscosparkapi


# Helper Functions

def get_list_of_licenses(api, orgId=None, max=None):
    return api.licenses.list(orgId=orgId, max=max)


def get_license_by_id(api, licenseId):
    return api.licenses.get(licenseId)


def is_valid_license(obj):
    return isinstance(obj, ciscosparkapi.License) and obj.id is not None


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
