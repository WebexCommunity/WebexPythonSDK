# -*- coding: utf-8 -*-

"""pytest People functions, fixtures and tests."""


import pytest

import ciscosparkapi


# Helper Functions

def is_valid_person(obj):
    return isinstance(obj, ciscosparkapi.Person) and obj.id is not None


def are_valid_people(iterable):
    return all([is_valid_person(obj) for obj in iterable])


def get_person_by_id(api, id):
    return api.people.get(id)


def get_person_by_email(api, email):
    list_of_people = list(api.people.list(email=email))
    if list_of_people:
        # If found, there should only be one Spark account associated with an
        # single e-mail address.
        assert len(list_of_people) == 1
        return list_of_people[0]
    else:
        return None


def create_person(api, emails, **person_attributes):
    return api.people.create(emails, **person_attributes)


def delete_person(api, person):
    api.people.delete(person.id)


def get_new_test_person(api, get_new_email_address, licenses_dict):
    person_email = get_new_email_address()
    person = get_person_by_email(api, person_email)
    if person:
        return person
    else:
        emails = [person_email]
        display_name = "ciscosparkapi"
        first_name = "ciscosparkapi"
        last_name = "ciscosparkapi"
        licenses = [licenses_dict["Messaging"].id]
        person = create_person(api, emails,
                               displayName=display_name,
                               firstName=first_name,
                               lastName=last_name,
                               licenses=licenses)
        assert is_valid_person(person)
        return person


# Helper Classes

class TestPeople(object):
    """Creates, tracks and manages test accounts 'people' used by the tests."""

    def __init__(self, api, get_new_email_address, licenses_dict):
        super(object, TestPeople).__init__()
        self._api = api
        self._get_new_email_address = get_new_email_address
        self._licenses_dict = licenses_dict
        self.test_people = {}

    def __getitem__(self, item):
        if self.test_people.get(item):
            return self.test_people[item]
        else:
            new_test_person = get_new_test_person(self._api,
                                                  self._get_new_email_address,
                                                  self._licenses_dict)
            self.test_people[item] = new_test_person
            return new_test_person

    def list(self):
        return self.test_people.values()

    def __iter__(self):
        return iter(self.list())

    def __del__(self):
        for person in self.test_people.values():
            delete_person(self._api, person)
        super(object, TestPeople).__del__()


# pytest Fixtures

@pytest.fixture(scope="session")
def me(api):
    return api.people.me()


@pytest.fixture(scope="session")
def test_people(api, get_new_email_address, licenses_dict):
    test_people = TestPeople()
    yield test_people
    del(test_people)


@pytest.fixture()
def temp_person(api, get_new_email_address, licenses_dict):
    person =  get_new_test_person(api, get_new_email_address, licenses_dict)
    yield person
    delete_person(api, person)


@pytest.fixture()
def people_in_group_room(api, group_room_memberships):
    return [get_person_by_id(api, membership.personId)
            for membership in group_room_memberships]
