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


def get_new_test_person(api, get_new_email_address, licenses_dict):
    person_email = get_new_email_address()
    person = get_person_by_email(api, person_email)
    if person:
        return person
    else:
        emails = [person_email]
        display_name = person_email
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


# pytest Fixtures

@pytest.fixture(scope="session")
def me(api):
    return api.people.me()


@pytest.fixture(scope="session")
def person_1(api, get_new_email_address, licenses_dict):
    return get_new_test_person(api, get_new_email_address, licenses_dict)


@pytest.fixture(scope="session")
def person_2(api, get_new_email_address, licenses_dict):
    return get_new_test_person(api, get_new_email_address, licenses_dict)


@pytest.fixture(scope="session")
def person_3(api, get_new_email_address, licenses_dict):
    return get_new_test_person(api, get_new_email_address, licenses_dict)


@pytest.fixture(scope="session")
def person_4(api, get_new_email_address, licenses_dict):
    return get_new_test_person(api, get_new_email_address, licenses_dict)


@pytest.fixture()
def temp_person(api, get_new_email_address, licenses_dict):
    return get_new_test_person(api, get_new_email_address, licenses_dict)


@pytest.fixture(scope="session")
def people_in_group_room(api, group_room_memberships):
    return [get_person_by_id(api, membership.personId)
            for membership in group_room_memberships]

