# -*- coding: utf-8 -*-
"""Webex Teams API wrappers.

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

from past.types import basestring

from webexteamssdk.config import (
    DEFAULT_BASE_URL, DEFAULT_SINGLE_REQUEST_TIMEOUT,
    DEFAULT_WAIT_ON_RATE_LIMIT,
)
from webexteamssdk.environment import WEBEX_TEAMS_ACCESS_TOKEN
from webexteamssdk.exceptions import AccessTokenError
from webexteamssdk.models.immutable import immutable_data_factory
from webexteamssdk.restsession import RestSession
from webexteamssdk.utils import check_type
from .access_tokens import AccessTokensAPI
from .events import EventsAPI
from .licenses import LicensesAPI
from .memberships import MembershipsAPI
from .messages import MessagesAPI
from .organizations import OrganizationsAPI
from .people import PeopleAPI
from .roles import RolesAPI
from .rooms import RoomsAPI
from .team_memberships import TeamMembershipsAPI
from .teams import TeamsAPI
from .webhooks import WebhooksAPI


class WebexTeamsAPI(object):
    """Webex Teams API wrapper.

    Creates a 'session' for all API calls through a created WebexTeamsAPI
    object.  The 'session' handles authentication, provides the needed headers,
    and checks all responses for error conditions.

    WebexTeamsAPI wraps all of the individual Webex Teams APIs and represents
    them in a simple hierarchical structure.
    """

    def __init__(self, access_token=None, base_url=DEFAULT_BASE_URL,
                 single_request_timeout=DEFAULT_SINGLE_REQUEST_TIMEOUT,
                 wait_on_rate_limit=DEFAULT_WAIT_ON_RATE_LIMIT,
                 object_factory=immutable_data_factory):
        """Create a new WebexTeamsAPI object.

        An access token must be used when interacting with the Webex Teams API.
        This package supports two methods for you to provide that access token:

          1. You may manually specify the access token via the `access_token`
             argument, when creating a new WebexTeamsAPI object.

          2. If an access_token argument is not supplied, the package checks
             for a WEBEX_TEAMS_ACCESS_TOKEN environment variable.

        An AccessTokenError is raised if an access token is not provided
        via one of these two methods.

        Args:
            access_token(basestring): The access token to be used for API
                calls to the Webex Teams service.  Defaults to checking for a
                WEBEX_TEAMS_ACCESS_TOKEN environment variable.
            base_url(basestring): The base URL to be prefixed to the
                individual API endpoint suffixes.
                Defaults to webexteamssdk.DEFAULT_BASE_URL.
            single_request_timeout(int): Timeout (in seconds) for RESTful HTTP
                requests. Defaults to
                webexteamssdk.config.DEFAULT_SINGLE_REQUEST_TIMEOUT.
            wait_on_rate_limit(bool): Enables or disables automatic rate-limit
                handling. Defaults to
                webexteamssdk.config.DEFAULT_WAIT_ON_RATE_LIMIT.
            object_factory(callable): The factory function to use to create
                Python objects from the returned Webex Teams JSON data objects.

        Returns:
            WebexTeamsAPI: A new WebexTeamsAPI object.

        Raises:
            TypeError: If the parameter types are incorrect.
            AccessTokenError: If an access token is not provided via the
                access_token argument or an environment variable.

        """
        check_type(access_token, basestring)
        check_type(base_url, basestring)
        check_type(single_request_timeout, int)
        check_type(wait_on_rate_limit, bool)

        access_token = access_token or WEBEX_TEAMS_ACCESS_TOKEN
        if not access_token:
            raise AccessTokenError(
                "You must provide a Webex Teams access token to interact with "
                "the Webex Teams APIs, either via a WEBEX_TEAMS_ACCESS_TOKEN "
                "environment variable or via the access_token argument."
            )

        # Create the API session
        # All of the API calls associated with a WebexTeamsAPI object will
        # leverage a single RESTful 'session' connecting to the Webex Teams
        # cloud.
        self._session = RestSession(
            access_token=access_token,
            base_url=base_url,
            single_request_timeout=single_request_timeout,
            wait_on_rate_limit=wait_on_rate_limit
        )

        # API wrappers
        self.people = PeopleAPI(self._session, object_factory)
        self.rooms = RoomsAPI(self._session, object_factory)
        self.memberships = MembershipsAPI(self._session, object_factory)
        self.messages = MessagesAPI(self._session, object_factory)
        self.teams = TeamsAPI(self._session, object_factory)
        self.team_memberships = TeamMembershipsAPI(
            self._session, object_factory
        )
        self.webhooks = WebhooksAPI(self._session, object_factory)
        self.organizations = OrganizationsAPI(self._session, object_factory)
        self.licenses = LicensesAPI(self._session, object_factory)
        self.roles = RolesAPI(self._session, object_factory)
        self.access_tokens = AccessTokensAPI(
            self.base_url, object_factory,
            single_request_timeout=single_request_timeout
        )
        self.events = EventsAPI(self._session, object_factory)

    @property
    def access_token(self):
        """The access token used for API calls to the Webex Teams service."""
        return self._session.access_token

    @property
    def base_url(self):
        """The base URL prefixed to the individual API endpoint suffixes."""
        return self._session.base_url

    @property
    def single_request_timeout(self):
        """Timeout (in seconds) for an single HTTP request."""
        return self._session.single_request_timeout

    @property
    def wait_on_rate_limit(self):
        """Automatic rate-limit handling enabled / disabled."""
        return self._session.wait_on_rate_limit
