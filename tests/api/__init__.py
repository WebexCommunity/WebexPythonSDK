# -*- coding: utf-8 -*-
"""WebexTeamsAPI fixtures and tests.

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

import os

import pytest

import webexteamssdk
from tests.environment import WEBEX_TEAMS_ACCESS_TOKEN
from webexteamssdk.api.access_tokens import AccessTokensAPI
from webexteamssdk.api.events import EventsAPI
from webexteamssdk.api.licenses import LicensesAPI
from webexteamssdk.api.memberships import MembershipsAPI
from webexteamssdk.api.messages import MessagesAPI
from webexteamssdk.api.organizations import OrganizationsAPI
from webexteamssdk.api.people import PeopleAPI
from webexteamssdk.api.roles import RolesAPI
from webexteamssdk.api.rooms import RoomsAPI
from webexteamssdk.api.team_memberships import TeamMembershipsAPI
from webexteamssdk.api.teams import TeamsAPI
from webexteamssdk.api.webhooks import WebhooksAPI
from webexteamssdk.config import (
    ACCESS_TOKEN_ENVIRONMENT_VARIABLE, DEFAULT_BASE_URL,
    DEFAULT_SINGLE_REQUEST_TIMEOUT, DEFAULT_WAIT_ON_RATE_LIMIT,
)


# Fixtures

@pytest.fixture(scope="session")
def access_token():
    return WEBEX_TEAMS_ACCESS_TOKEN


@pytest.fixture
def unset_access_token(access_token):
    del os.environ[ACCESS_TOKEN_ENVIRONMENT_VARIABLE]
    yield None
    os.environ[ACCESS_TOKEN_ENVIRONMENT_VARIABLE] = access_token


@pytest.fixture(scope="session")
def api():
    return webexteamssdk.WebexTeamsAPI()


# Tests

# Test creating WebexTeamsAPI objects

@pytest.mark.usefixtures("unset_access_token")
def test_create_without_an_access_token():
    with pytest.raises(webexteamssdk.AccessTokenError):
        webexteamssdk.WebexTeamsAPI()


def test_create_with_access_token_environment_variable():
    connection_object = webexteamssdk.WebexTeamsAPI()
    assert isinstance(connection_object, webexteamssdk.WebexTeamsAPI)


@pytest.mark.usefixtures("unset_access_token")
def test_create_with_access_token_argument(access_token):
    connection_object = webexteamssdk.WebexTeamsAPI(
        access_token=access_token
    )
    assert isinstance(connection_object, webexteamssdk.WebexTeamsAPI)


def test_default_base_url():
    connection_object = webexteamssdk.WebexTeamsAPI()
    assert connection_object.base_url == DEFAULT_BASE_URL


def test_custom_base_url():
    custom_url = "https://custom.domain.com/v1/"
    connection_object = webexteamssdk.WebexTeamsAPI(base_url=custom_url)
    assert connection_object.base_url == custom_url


def test_default_single_request_timeout():
    connection_object = webexteamssdk.WebexTeamsAPI()
    assert connection_object.single_request_timeout == \
        DEFAULT_SINGLE_REQUEST_TIMEOUT


def test_custom_single_request_timeout():
    custom_timeout = 10
    connection_object = webexteamssdk.WebexTeamsAPI(
        single_request_timeout=custom_timeout
    )
    assert connection_object.single_request_timeout == custom_timeout


def test_default_wait_on_rate_limit():
    connection_object = webexteamssdk.WebexTeamsAPI()
    assert connection_object.wait_on_rate_limit == \
        DEFAULT_WAIT_ON_RATE_LIMIT


def test_non_default_wait_on_rate_limit():
    connection_object = webexteamssdk.WebexTeamsAPI(
        wait_on_rate_limit=not DEFAULT_WAIT_ON_RATE_LIMIT
    )
    assert connection_object.wait_on_rate_limit != \
        DEFAULT_WAIT_ON_RATE_LIMIT


# Test creation of component API objects

def test_access_tokens_api_object_creation(api):
    assert isinstance(api.access_tokens, AccessTokensAPI)


def test_events_api_object_creation(api):
    assert isinstance(api.events, EventsAPI)


def test_licenses_api_object_creation(api):
    assert isinstance(api.licenses, LicensesAPI)


def test_memberships_api_object_creation(api):
    assert isinstance(api.memberships, MembershipsAPI)


def test_messages_api_object_creation(api):
    assert isinstance(api.messages, MessagesAPI)


def test_organizations_api_object_creation(api):
    assert isinstance(api.organizations, OrganizationsAPI)


def test_people_api_object_creation(api):
    assert isinstance(api.people, PeopleAPI)


def test_roles_api_object_creation(api):
    assert isinstance(api.roles, RolesAPI)


def test_rooms_api_object_creation(api):
    assert isinstance(api.rooms, RoomsAPI)


def test_team_memberships_api_object_creation(api):
    assert isinstance(api.team_memberships, TeamMembershipsAPI)


def test_teams_api_object_creation(api):
    assert isinstance(api.teams, TeamsAPI)


def test_webhooks_api_object_creation(api):
    assert isinstance(api.webhooks, WebhooksAPI)
