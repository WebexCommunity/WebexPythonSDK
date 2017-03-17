# -*- coding: utf-8 -*-

"""pytest People functions, fixtures and tests."""


import itertools

import pytest

import ciscosparkapi
from tests.conftest import TEST_FILE_URL


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
    return api.people.update(person.id, **person_attributes)


def delete_person(api, person):
    # Temporarily disabling test account deletion to workon account
    # capabilities issues.
    # TODO: Enable test account clean-up.
    # api.people.delete(person.id)
    pass


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
        super(TestPeople, self).__init__()
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

    @property
    def list(self):
        return self.test_people.values()

    def len(self):
        return len(self.list)

    def __iter__(self):
        return iter(self.list)

    def __del__(self):
        for person in self.test_people.values():
            delete_person(self._api, person)
            pass


# pytest Fixtures

@pytest.fixture(scope="session")
def me(api):
    return api.people.me()


@pytest.fixture(scope="session")
def test_people(api, get_new_email_address, licenses_dict):
    test_people = TestPeople(api, get_new_email_address, licenses_dict)
    yield test_people
    del test_people


@pytest.fixture()
def temp_person(api, get_new_email_address, licenses_dict):
    person = get_new_test_person(api, get_new_email_address, licenses_dict)
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

    # TODO: Investigate update person API not working
    # def test_update_person(self, api, temp_person, roles_dict, licenses_dict,
    #                        get_new_email_address):
    #     # Note:  Not testing updating orgId
    #     updated_attributes = {
    #         "emails": [get_new_email_address()],
    #         "displayName": temp_person.displayName + " Updated",
    #         "firstName": temp_person.firstName + " Updated",
    #         "lastName": temp_person.lastName + " Updated",
    #         "avatar": TEST_FILE_URL,
    #         "roles": [roles_dict["Read-only administrator"].id],
    #         "licenses": [licenses_dict["Messaging"].id,
    #                      licenses_dict["Meeting 25 party"].id],
    #     }
    #     updated_person = update_person(api, temp_person, **updated_attributes)
    #     assert is_valid_person(updated_person)
    #     for attribute, value in updated_attributes:
    #         assert getattr(updated_person, attribute, default=None) == value

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
