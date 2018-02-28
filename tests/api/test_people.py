# -*- coding: utf-8 -*-
"""pytest People functions, fixtures and tests."""


import itertools

import pytest

import ciscosparkapi


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


# Helper Functions

def is_valid_person(obj):
    return isinstance(obj, ciscosparkapi.Person) and obj.id is not None


def are_valid_people(iterable):
    return all([is_valid_person(obj) for obj in iterable])


def get_person_by_id(api, id):
    return api.people.get(id)


def list_people(api, **search_attribute):
    return list(api.people.list(**search_attribute))


def get_person_by_email(api, email):
    list_of_people = list_people(api, email=email)
    if list_of_people:
        # If found, there should only be one Spark account associated with an
        # single e-mail address.
        assert len(list_of_people) == 1
        return list_of_people[0]
    else:
        return None


def create_person(api, emails, **person_attributes):
    return api.people.create(emails, **person_attributes)


def update_person(api, person, **person_attributes):
    # Get a copy of the person's current attributes
    new_attributes = person.json_data

    # Merge in attribute updates
    for attribute, value in person_attributes.items():
        new_attributes[attribute] = value

    return api.people.update(person.id, **new_attributes)


def delete_person(api, person):
    api.people.delete(person.id)


# pytest Fixtures

@pytest.fixture(scope="session")
def me(api):
    return api.people.me()

@pytest.fixture(scope="session")
def get_new_test_person(api, get_new_email_address, me, licenses_dict):

    def inner_function():
        person_email = get_new_email_address()
        person = get_person_by_email(api, person_email)
        if person:
            return person
        else:
            person = create_person(api,
                                   emails=[person_email],
                                   displayName="ciscosparkapi",
                                   firstName="ciscosparkapi",
                                   lastName="ciscosparkapi",
                                   orgId=me.orgId,
                                   licenses=[licenses_dict["Messaging"].id],
                                   )
            assert is_valid_person(person)
            return person

    return inner_function


class PeopleManager(object):
    """Creates, tracks and manages test accounts 'people' used by the tests."""

    def __init__(self, api, get_new_test_person):
        super(PeopleManager, self).__init__()
        self._api = api
        self._get_new_test_person = get_new_test_person
        self.test_people = {}

    def __getitem__(self, item):
        if self.test_people.get(item):
            return self.test_people[item]
        else:
            new_test_person = self._get_new_test_person()
            self.test_people[item] = new_test_person
            return new_test_person

    @property
    def list(self):
        return self.test_people.values()

    def len(self):
        return len(self.list)

    def __iter__(self):
        return iter(self.list)

    def __del__(self):
        # TODO: Enable test account clean-up.
        # Licensed privileges aren't taking effect for accounts that have
        # just been created and this is causing some tests to fail.
        # I am temporarily disabling test account clean-up to enable the
        # accounts (with their privileges) to persist.  It would be good to
        # find a way around this.

        # for person in self.test_people.values():
        #     delete_person(self._api, person)
        pass


@pytest.fixture(scope="session")
def test_people(api, get_new_test_person):
    test_people = PeopleManager(api, get_new_test_person)
    yield test_people
    del test_people


@pytest.fixture()
def temp_person(api, get_new_test_person):
    person = get_new_test_person()
    yield person
    delete_person(api, person)


@pytest.fixture()
def people_in_group_room(api, group_room_memberships):
    return [get_person_by_id(api, membership.personId)
            for membership in group_room_memberships]


# Tests

class TestPeopleAPI(object):
    """Test PeopleAPI methods."""

    def test_create_person(self, test_people):
        person = test_people["not_a_member"]
        assert is_valid_person(person)

    def test_update_person(self, api, temp_person):
        update_attributes = {
            "displayName": temp_person.displayName + " Updated",
            "firstName": temp_person.firstName + " Updated",
            "lastName": temp_person.lastName + " Updated",
        }
        updated_person = update_person(api, temp_person, **update_attributes)
        assert is_valid_person(updated_person)
        for attribute, value in update_attributes.items():
            assert getattr(updated_person, attribute) == value

    def test_get_my_details(self, me):
        assert is_valid_person(me)

    def test_get_person_details(self, api, test_people):
        person_id = test_people["not_a_member"].id
        person = get_person_by_id(api, person_id)
        assert is_valid_person(person)

    def test_list_people_by_email(self, api, test_people):
        email = test_people["not_a_member"].emails[0]
        list_of_people = list_people(api, email=email)
        assert len(list_of_people) >= 1
        assert are_valid_people(list_of_people)

    def test_list_people_by_display_name(self, api, test_people):
        display_name = test_people["not_a_member"].displayName
        list_of_people = list_people(api, displayName=display_name)
        assert len(list_of_people) >= 1
        assert are_valid_people(list_of_people)

    def test_list_people_by_id(self, api, test_people):
        id = test_people["not_a_member"].id
        list_of_people = list_people(api, id=id)
        assert len(list_of_people) >= 1
        assert are_valid_people(list_of_people)

    def test_list_people_with_paging(self, api, test_people,
                                     additional_group_room_memberships):
        page_size = 1
        pages = 3
        num_people = pages * page_size
        assert test_people.len() >= num_people
        display_name = test_people["not_a_member"].displayName
        people = api.people.list(displayName=display_name, max=page_size)
        people_list = list(itertools.islice(people, num_people))
        assert len(people_list) == num_people
        assert are_valid_people(people_list)
