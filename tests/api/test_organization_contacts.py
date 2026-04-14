"""WebexAPI Organization Contacts API fixtures and tests.

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

import pytest

import webexpythonsdk


# Helper Functions
def get_contact_by_email(api, org_id, email):
    list_of_contacts = list(
        api.organization_contacts.search(org_id, email=email)
    )
    if list_of_contacts:
        assert len(list_of_contacts) == 1
        return list_of_contacts[0]
    else:
        return None


def update_contact(api, contact, **contact_attributes):
    # Get a copy of the contact's current attributes
    new_attributes = contact.json_data

    # Merge in attribute updates
    for attribute, value in contact_attributes.items():
        new_attributes[attribute] = value

    return api.organization_contacts.update(
        contact.orgId, contact.id, **new_attributes
    )


def delete_contact(api, contact):
    """Delete a contact and swallow any API error."""
    try:
        api.organization_contacts.delete(contact.orgId, contact.id)
    except webexpythonsdk.ApiError:
        pass


def is_valid_organization_contact(obj):
    return (
        isinstance(obj, webexpythonsdk.OrganizationContact)
        and obj.id is not None
    )


def are_valid_organization_contacts(iterable):
    return all([is_valid_organization_contact(obj) for obj in iterable])


# Fixtures
@pytest.fixture(scope="session")
def get_test_contact(api, get_new_email_address, me):
    def inner_function():
        contact_email = get_new_email_address()
        contact = get_contact_by_email(api, me.orgId, contact_email)
        if contact:
            return contact
        else:
            contact = api.organization_contacts.create(
                me.orgId,
                emails=[contact_email],
                displayName="webexpythonsdk",
                firstName="webexpythonsdk",
                lastName="webexpythonsdk",
            )
            return contact

    return inner_function


class OrganizationContactsManager(object):
    """Creates, tracks and manages test contacts used by the tests."""

    def __init__(self, api, get_test_contact):
        super(OrganizationContactsManager, self).__init__()
        self._api = api
        self._get_new_test_contact = get_test_contact
        self.test_contacts = {}

    def __getitem__(self, item):
        if self.test_contacts.get(item):
            return self.test_contacts[item]
        else:
            new_test_contact = self._get_new_test_contact()
            self.test_contacts[item] = new_test_contact
            return new_test_contact

    @property
    def list(self):
        return self.test_contacts.values()

    def len(self):
        return len(self.list)

    def __iter__(self):
        return iter(self.list)

    def __del__(self):
        for contact in self.test_contacts.values():
            delete_contact(self._api, contact)


@pytest.fixture(scope="session")
def test_organization_contacts(api, get_test_contact):
    test_contacts = OrganizationContactsManager(api, get_test_contact)

    yield test_contacts

    del test_contacts


@pytest.fixture()
def temp_contact(api, get_random_email_address, me):
    # Get an e-mail address not currently used on Webex
    contact_email = None
    contact = True
    while contact:
        contact_email = get_random_email_address()
        contact = get_contact_by_email(api, me.orgId, contact_email)

    # Create the contact
    contact = api.organization_contacts.create(
        me.orgId,
        emails=[contact_email],
        displayName="webexpythonsdk",
        firstName="webexpythonsdk",
        lastName="webexpythonsdk",
    )

    yield contact

    try:
        api.organization_contacts.delete(me.orgId, contact.id)
    except webexpythonsdk.ApiError:
        pass


# Tests
def test_list_organization_contacts(api, me, test_organization_contacts):
    # Ensure we have at least one contact
    _ = test_organization_contacts["test_contact"]

    list_of_contacts = list(api.organization_contacts.list(me.orgId))
    assert len(list_of_contacts) >= 1
    assert are_valid_organization_contacts(list_of_contacts)


def test_search_organization_contacts_by_email(
    api, me, test_organization_contacts
):
    email = test_organization_contacts["not_a_member"].emails[0]
    list_of_contacts = list(
        api.organization_contacts.search(me.orgId, email=email)
    )
    assert len(list_of_contacts) >= 1
    assert are_valid_organization_contacts(list_of_contacts)


def test_search_organization_contacts_by_display_name(
    api, me, test_organization_contacts
):
    display_name = test_organization_contacts["not_a_member"].displayName
    list_of_contacts = list(
        api.organization_contacts.search(me.orgId, displayName=display_name)
    )
    assert len(list_of_contacts) >= 1
    assert are_valid_organization_contacts(list_of_contacts)


def test_search_organization_contacts_by_id(
    api, me, test_organization_contacts
):
    contact_id = test_organization_contacts["not_a_member"].id
    list_of_contacts = list(
        api.organization_contacts.search(me.orgId, id=contact_id)
    )
    assert len(list_of_contacts) == 1
    assert are_valid_organization_contacts(list_of_contacts)


def test_search_organization_contacts_with_paging(
    api, me, test_organization_contacts
):
    page_size = 1
    pages = 3
    num_contacts = pages * page_size

    for i in range(num_contacts):
        _ = test_organization_contacts[f"contact_{i}"]

    contacts = api.organization_contacts.search(me.orgId, max=page_size)
    contacts_list = list(itertools.islice(contacts, num_contacts))

    assert len(contacts_list) == num_contacts
    assert are_valid_organization_contacts(contacts_list)


def test_create_organization_contact(test_organization_contacts):
    contact = test_organization_contacts["not_a_member"]
    assert is_valid_organization_contact(contact)


def test_get_organization_contact_details(api, me, test_organization_contacts):
    contact_id = test_organization_contacts["not_a_member"].id
    contact = api.organization_contacts.get(me.orgId, contact_id)
    assert is_valid_organization_contact(contact)


def test_update_organization_contact(api, temp_contact):
    update_attributes = {
        "displayName": temp_contact.displayName + " Updated",
        "firstName": temp_contact.firstName + " Updated",
        "lastName": temp_contact.lastName + " Updated",
    }
    updated_contact = update_contact(api, temp_contact, **update_attributes)
    assert is_valid_organization_contact(updated_contact)
    for attribute, value in update_attributes.items():
        assert getattr(updated_contact, attribute) == value


def test_delete_organization_contact(api, temp_contact):
    api.organization_contacts.delete(temp_contact.orgId, temp_contact.id)
