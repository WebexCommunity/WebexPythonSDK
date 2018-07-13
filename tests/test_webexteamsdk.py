# -*- coding: utf-8 -*-
"""webexteamsdk/__init__.py Fixtures & Tests"""


import os

import pytest

import webexteamsdk
import webexteamsdk.api
import webexteamsdk.config

__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


# pytest Fixtures

@pytest.fixture(scope="session")
def access_token():
    return os.environ.get(
        webexteamsdk.config.ACCESS_TOKEN_ENVIRONMENT_VARIABLE)


@pytest.fixture
def unset_access_token(access_token):
    del os.environ[webexteamsdk.config.ACCESS_TOKEN_ENVIRONMENT_VARIABLE]
    yield None
    os.environ[webexteamsdk.config.ACCESS_TOKEN_ENVIRONMENT_VARIABLE] = access_token


@pytest.fixture(scope="session")
def api():
    return webexteamsdk.api.WebexTeamsAPI()


# CiscoSparkAPI Tests

class TestCiscoSparkAPI:
    """Test the CiscoSparkAPI package-level code."""

    # Test creating CiscoSparkAPI objects

    @pytest.mark.usefixtures("unset_access_token")
    def test_creating_a_new_webexteamsdk_object_without_an_access_token(self):
        with pytest.raises(webexteamsdk.webexteamsdkException):
            webexteamsdk.api.WebexTeamsAPI()

    @pytest.mark.usefixtures("unset_access_token")
    def test_creating_a_new_webexteamsdk_object_via_access_token_argument(self, access_token):
        connection_object = webexteamsdk.api.WebexTeamsAPI(access_token=access_token)
        assert isinstance(connection_object, webexteamsdk.api.WebexTeamsAPI)

    def test_creating_a_new_webexteamsdk_object_via_environment_varable(self):
        connection_object = webexteamsdk.api.WebexTeamsAPI()
        assert isinstance(connection_object, webexteamsdk.api.WebexTeamsAPI)

    def test_default_base_url(self):
        connection_object = webexteamsdk.api.WebexTeamsAPI()
        assert connection_object.base_url == webexteamsdk.config.DEFAULT_BASE_URL

    def test_custom_base_url(self):
        custom_url = "https://spark.cmlccie.com/v1/"
        connection_object = webexteamsdk.api.WebexTeamsAPI(base_url=custom_url)
        assert connection_object.base_url == custom_url

    def test_default_timeout(self):
        connection_object = webexteamsdk.api.WebexTeamsAPI()
        assert connection_object.timeout == \
               webexteamsdk.config.DEFAULT_SINGLE_REQUEST_TIMEOUT

    def test_custom_timeout(self):
        custom_timeout = 10
        connection_object = webexteamsdk.api.WebexTeamsAPI(timeout=custom_timeout)
        assert connection_object.timeout == custom_timeout

    def test_default_single_request_timeout(self):
        connection_object = webexteamsdk.api.WebexTeamsAPI()
        assert connection_object.single_request_timeout == \
               webexteamsdk.config.DEFAULT_SINGLE_REQUEST_TIMEOUT

    def test_custom_single_request_timeout(self):
        custom_timeout = 10
        connection_object = webexteamsdk.api.WebexTeamsAPI(
                single_request_timeout=custom_timeout
        )
        assert connection_object.single_request_timeout == custom_timeout

    def test_default_wait_on_rate_limit(self):
        connection_object = webexteamsdk.api.WebexTeamsAPI()
        assert connection_object.wait_on_rate_limit == \
               webexteamsdk.config.DEFAULT_WAIT_ON_RATE_LIMIT

    def test_non_default_wait_on_rate_limit(self):
        connection_object = webexteamsdk.api.WebexTeamsAPI(
                wait_on_rate_limit=not webexteamsdk.config.DEFAULT_WAIT_ON_RATE_LIMIT
        )
        assert connection_object.wait_on_rate_limit != \
               webexteamsdk.config.DEFAULT_WAIT_ON_RATE_LIMIT

    # Test creation of component API objects

    def test_people_api_object_creation(self, api):
        assert isinstance(api.people, webexteamsdk._PeopleAPI)

    def test_rooms_api_object_creation(self, api):
        assert isinstance(api.rooms, webexteamsdk._RoomsAPI)

    def test_memberships_api_object_creation(self, api):
        assert isinstance(api.memberships, webexteamsdk._MembershipsAPI)

    def test_messages_api_object_creation(self, api):
        assert isinstance(api.messages, webexteamsdk._MessagesAPI)

    def test_teams_api_object_creation(self, api):
        assert isinstance(api.teams, webexteamsdk._TeamsAPI)

    def test_team_memberships_api_object_creation(self, api):
        assert isinstance(api.team_memberships, webexteamsdk._TeamMembershipsAPI)

    def test_webhooks_api_object_creation(self, api):
        assert isinstance(api.webhooks, webexteamsdk._WebhooksAPI)

    def test_access_tokens_api_object_creation(self, api):
        assert isinstance(api.access_tokens, webexteamsdk._AccessTokensAPI)
