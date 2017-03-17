# -*- coding: utf-8 -*-

"""pytest Memberships functions, fixtures and tests."""


import itertools

import pytest

import ciscosparkapi


# Helper Functions

def add_person_to_room_by_email(api, room, person, isModerator=False):
    return api.memberships.create(room.id,
                                  personEmail=person.emails[0],
                                  isModerator=isModerator)


def add_person_to_room_by_id(api, room, person, isModerator=False):
    return api.memberships.create(room.id,
                                  personId=person.id,
                                  isModerator=isModerator)


def add_people_to_room_by_email(api, room, people):
    return [add_person_to_room_by_email(api, room, person)
            for person in people]


def add_people_to_room_by_id(api, room, people):
    return [add_person_to_room_by_id(api, room, person)
            for person in people]


def get_room_membership_list(api, room, **kwargs):
    return list(api.memberships.list(roomId=room.id, **kwargs))


def get_membership_by_id(api, id):
    return api.memberships.get(id)


def make_moderator(api, membership):
    return api.memberships.update(membership.id, isModerator=True)


def delete_membership(api, membership):
    api.memberships.delete(membership.id)


def empty_room(api, me, room):
    """Remove all memberships from a room (except the caller's membership)."""
    memberships = api.memberships.list(room.id)
    for membership in memberships:
        if membership.personId != me.id:
            delete_membership(api, membership)


def is_valid_membership(membership):
    return isinstance(membership, ciscosparkapi.Membership) \
           and membership.id is not None


def are_valid_memberships(iterable):
    are_valid = (is_valid_membership(item) for item in iterable)
    return all(are_valid)


def membership_exists(api, membership):
    try:
        get_membership_by_id(api, membership.id)
    except ciscosparkapi.SparkApiError:
        return False
    else:
        return True


# pytest Fixtures

@pytest.fixture(scope="session")
def authenticated_users_memberships(api):
    return list(api.memberships.list())


@pytest.fixture(scope="session")
def my_group_room_membership(api, me, group_room):
    memberships = get_room_membership_list(api, group_room, personId=me.id)
    assert len(memberships) == 1
    membership = memberships[0]
    return membership


@pytest.fixture(scope="session")
def make_me_group_room_moderator(api, my_group_room_membership):
    return make_moderator(api, my_group_room_membership)


@pytest.fixture(scope="session")
def person_1_group_room_membership(api, make_me_group_room_moderator,
                                   group_room, person_1):
    # Used by test_create_membership_by_email()
    membership = add_person_to_room_by_email(api, group_room, person_1)
    yield membership
    delete_membership(api, membership)


@pytest.fixture(scope="session")
def person_2_group_room_membership(api, make_me_group_room_moderator,
                                   group_room, person_2):
    # Used by test_create_membership_by_person_id()
    membership = add_person_to_room_by_id(api, group_room, person_2)
    yield membership
    delete_membership(api, membership)


@pytest.fixture(scope="session")
def person_3_group_room_membership(api, make_me_group_room_moderator,
                                   group_room, person_3):
    # Used by test_create_moderator_by_email()
    membership = add_person_to_room_by_email(api, group_room, person_3,
                                             isModerator=True)
    yield membership
    delete_membership(api, membership)


@pytest.fixture(scope="session")
def person_4_group_room_membership(api, make_me_group_room_moderator,
                                   group_room, person_4):
    # Used by test_create_moderator_by_person_id()
    membership = add_person_to_room_by_id(api, group_room, person_4,
                                          isModerator=True)
    yield membership
    delete_membership(api, membership)


@pytest.fixture(scope="session")
def additional_group_room_memberships(person_1_group_room_membership,
                                      person_2_group_room_membership,
                                      person_3_group_room_membership,
                                      person_4_group_room_membership):
    return [person_1_group_room_membership,
            person_2_group_room_membership,
            person_3_group_room_membership,
            person_4_group_room_membership]


@pytest.fixture(scope="session")
def group_room_with_members(group_room, additional_group_room_memberships):
    return group_room


# Tests

class TestMembershipsAPI(object):
    """Test MembershipsAPI methods."""

    def test_list_user_memberships(self, group_room, team_room, direct_rooms,
                                   authenticated_users_memberships):
        assert len(authenticated_users_memberships) >= 3
        assert are_valid_memberships(authenticated_users_memberships)

    def test_list_user_memberships_with_paging(self, api, add_rooms,
                                               authenticated_users_memberships,
                                               group_room, team_room,
                                               direct_rooms):
        page_size = 2
        pages = 3
        num_memberships = pages * page_size
        if len(authenticated_users_memberships) < num_memberships:
            add_rooms(num_memberships - len(authenticated_users_memberships))
        memberships = api.memberships.list(max=page_size)
        memberships_list = list(itertools.islice(memberships, num_memberships))
        assert len(memberships_list) == num_memberships
        assert are_valid_memberships(memberships_list)

    def test_list_room_memberships(self, api, group_room_with_members):
        memberships = get_room_membership_list(api, group_room_with_members)
        assert len(memberships) > 1
        assert are_valid_memberships(memberships)

    def test_filter_room_memberships_by_personEmail(self, api, person_1,
                                                    group_room_with_members):
        memberships = get_room_membership_list(api, group_room_with_members,
                                               personEmail=person_1.emails[0])
        assert len(memberships) == 1
        membership = memberships[0]
        assert is_valid_membership(membership)
        assert membership.roomId == group_room_with_members.id

    def test_filter_room_memberships_by_personId(self, api, person_1,
                                                 group_room_with_members):
        memberships = get_room_membership_list(api, group_room_with_members,
                                               personId=person_1.id)
        assert len(memberships) == 1
        membership = memberships[0]
        assert is_valid_membership(membership)
        assert membership.roomId == group_room_with_members.id

    def test_create_membership_by_email(self, person_1_group_room_membership):
        assert is_valid_membership(person_1_group_room_membership)

    def test_create_membership_by_person_id(self,
                                            person_2_group_room_membership):
        assert is_valid_membership(person_2_group_room_membership)

    def test_create_moderator_by_email(self, person_3_group_room_membership):
        assert is_valid_membership(person_3_group_room_membership)

    def test_create_moderator_by_person_id(self,
                                           person_4_group_room_membership):
        assert is_valid_membership(person_4_group_room_membership)

    def test_get_membership_details(self, api, my_group_room_membership):
        membership = get_membership_by_id(api, my_group_room_membership.id)
        assert is_valid_membership(membership)

    def test_update_membership_make_moderator(self,
                                              make_me_group_room_moderator):
        assert is_valid_membership(make_me_group_room_moderator)
        assert make_me_group_room_moderator.isModerator

    def test_delete_membership(self, api, group_room, temp_person):
        membership = add_person_to_room_by_id(api, group_room, temp_person)
        assert is_valid_membership(membership)
        delete_membership(api, membership)
        assert not membership_exists(api, membership)
