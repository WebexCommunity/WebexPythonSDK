# -*- coding: utf-8 -*-
"""webexteamssdk/__init__.py Fixtures & Tests"""


import os

import pytest

import webexteamssdk
import webexteamssdk.api
import webexteamssdk.config

__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


# pytest Fixtures

@pytest.fixture(scope="session")
def access_token():
    return os.environ.get(
        webexteamssdk.config.ACCESS_TOKEN_ENVIRONMENT_VARIABLE)


@pytest.fixture
def unset_access_token(access_token):
    del os.environ[webexteamssdk.config.ACCESS_TOKEN_ENVIRONMENT_VARIABLE]
    yield None
    os.environ[webexteamssdk.config.ACCESS_TOKEN_ENVIRONMENT_VARIABLE] = access_token


@pytest.fixture(scope="session")
def api():
    return webexteamssdk.api.WebexTeamsAPI()


# CiscoSparkAPI Tests

class TestCiscoSparkAPI:
    """Test the CiscoSparkAPI package-level code."""

    # Test creating CiscoSparkAPI objects

    @pytest.mark.usefixtures("unset_access_token")
    def test_creating_a_new_webexteamssdk_object_without_an_access_token(self):
        with pytest.raises(webexteamssdk.webexteamssdkException):
            webexteamssdk.api.WebexTeamsAPI()

    @pytest.mark.usefixtures("unset_access_token")
    def test_creating_a_new_webexteamssdk_object_via_access_token_argument(self, access_token):
        connection_object = webexteamssdk.api.WebexTeamsAPI(access_token=access_token)
        assert isinstance(connection_object, webexteamssdk.api.WebexTeamsAPI)

    def test_creating_a_new_webexteamssdk_object_via_environment_varable(self):
        connection_object = webexteamssdk.api.WebexTeamsAPI()
        assert isinstance(connection_object, webexteamssdk.api.WebexTeamsAPI)

    def test_default_base_url(self):
        connection_object = webexteamssdk.api.WebexTeamsAPI()
        assert connection_object.base_url == webexteamssdk.config.DEFAULT_BASE_URL

    def test_custom_base_url(self):
        custom_url = "https://spark.cmlccie.com/v1/"
        connection_object = webexteamssdk.api.WebexTeamsAPI(base_url=custom_url)
        assert connection_object.base_url == custom_url

    def test_default_timeout(self):
        connection_object = webexteamssdk.api.WebexTeamsAPI()
        assert connection_object.timeout == \
               webexteamssdk.config.DEFAULT_SINGLE_REQUEST_TIMEOUT

    def test_custom_timeout(self):
        custom_timeout = 10
        connection_object = webexteamssdk.api.WebexTeamsAPI(timeout=custom_timeout)
        assert connection_object.timeout == custom_timeout

    def test_default_single_request_timeout(self):
        connection_object = webexteamssdk.api.WebexTeamsAPI()
        assert connection_object.single_request_timeout == \
               webexteamssdk.config.DEFAULT_SINGLE_REQUEST_TIMEOUT

    def test_custom_single_request_timeout(self):
        custom_timeout = 10
        connection_object = webexteamssdk.api.WebexTeamsAPI(
                single_request_timeout=custom_timeout
        )
        assert connection_object.single_request_timeout == custom_timeout

    def test_default_wait_on_rate_limit(self):
        connection_object = webexteamssdk.api.WebexTeamsAPI()
        assert connection_object.wait_on_rate_limit == \
               webexteamssdk.config.DEFAULT_WAIT_ON_RATE_LIMIT

    def test_non_default_wait_on_rate_limit(self):
        connection_object = webexteamssdk.api.WebexTeamsAPI(
                wait_on_rate_limit=not webexteamssdk.config.DEFAULT_WAIT_ON_RATE_LIMIT
        )
        assert connection_object.wait_on_rate_limit != \
               webexteamssdk.config.DEFAULT_WAIT_ON_RATE_LIMIT

    # Test creation of component API objects

    def test_people_api_object_creation(self, api):
        assert isinstance(api.people, webexteamssdk._PeopleAPI)

    def test_rooms_api_object_creation(self, api):
        assert isinstance(api.rooms, webexteamssdk._RoomsAPI)

    def test_memberships_api_object_creation(self, api):
        assert isinstance(api.memberships, webexteamssdk._MembershipsAPI)

    def test_messages_api_object_creation(self, api):
        assert isinstance(api.messages, webexteamssdk._MessagesAPI)

    def test_teams_api_object_creation(self, api):
        assert isinstance(api.teams, webexteamssdk._TeamsAPI)

    def test_team_memberships_api_object_creation(self, api):
        assert isinstance(api.team_memberships, webexteamssdk._TeamMembershipsAPI)

    def test_webhooks_api_object_creation(self, api):
        assert isinstance(api.webhooks, webexteamssdk._WebhooksAPI)

    def test_access_tokens_api_object_creation(self, api):
        assert isinstance(api.access_tokens, webexteamssdk._AccessTokensAPI)
