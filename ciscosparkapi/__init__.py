# -*- coding: utf-8 -*-
"""Python API wrapper for the Cisco Spark APIs."""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
from past.builtins import basestring

import logging
import os

from .api.people import Person
from .api.rooms import Room
from .api.memberships import Membership
from .api.messages import Message
from .api.teams import Team
from .api.team_memberships import TeamMembership
from .api.webhooks import Webhook, WebhookEvent
from .api.organizations import Organization
from .api.licenses import License
from .api.roles import Role
from .api.access_tokens import AccessToken

from .api.people import PeopleAPI as _PeopleAPI
from .api.rooms import RoomsAPI as _RoomsAPI
from .api.memberships import MembershipsAPI as _MembershipsAPI
from .api.messages import MessagesAPI as _MessagesAPI
from .api.teams import TeamsAPI as _TeamsAPI
from .api.team_memberships import TeamMembershipsAPI as _TeamMembershipsAPI
from .api.webhooks import WebhooksAPI as _WebhooksAPI
from .api.organizations import OrganizationsAPI as _OrganizationsAPI
from .api.licenses import LicensesAPI as _LicensesAPI
from .api.roles import RolesAPI as _RolesAPI
from .api.access_tokens import AccessTokensAPI as _AccessTokensAPI

from .exceptions import (
    ciscosparkapiException,
    SparkApiError,
    SparkRateLimitError,
)

from .restsession import (
    DEFAULT_SINGLE_REQUEST_TIMEOUT,
    DEFAULT_WAIT_ON_RATE_LIMIT,
    RestSession as _RestSession,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"
__all__ = [
    "CiscoSparkAPI", "ciscosparkapiException", "SparkApiError",
    "SparkRateLimitError", "Person", "Room", "Membership", "Message", "Team",
    "TeamMembership", "Webhook", "WebhookEvent", "Organization", "License",
    "Role", "AccessToken"
]


# Versioneer version control
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


# Package Constants
DEFAULT_BASE_URL = 'https://api.ciscospark.com/v1/'
ACCESS_TOKEN_ENVIRONMENT_VARIABLE = 'SPARK_ACCESS_TOKEN'


# Initialize Package Logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# Main Package Interface
class CiscoSparkAPI(object):
    """Cisco Spark API wrapper.

    Creates a 'session' for all API calls through a created CiscoSparkAPI
    object.  The 'session' handles authentication, provides the needed headers,
    and checks all responses for error conditions.

    CiscoSparkAPI wraps all of the individual Cisco Spark APIs and represents
    them in a simple hierarchical structure.

    :CiscoSparkAPI: :class:`people <PeopleAPI>`

                    :class:`rooms <RoomsAPI>`

                    :class:`memberships <MembershipsAPI>`

                    :class:`messages <MessagesAPI>`

                    :class:`teams <TeamsAPI>`

                    :class:`team_memberships <TeamMembershipsAPI>`

                    :class:`webhooks <WebhooksAPI>`

                    :class:`organizations <OrganizationsAPI>`

                    :class:`licenses <LicensesAPI>`

                    :class:`roles <RolesAPI>`

                    :class:`access_tokens <AccessTokensAPI>`

    """

    def __init__(self, access_token=None, base_url=DEFAULT_BASE_URL,
                 timeout=None,
                 single_request_timeout=DEFAULT_SINGLE_REQUEST_TIMEOUT,
                 wait_on_rate_limit=DEFAULT_WAIT_ON_RATE_LIMIT):
        """Create a new CiscoSparkAPI object.

        An access token must be used when interacting with the Cisco Spark API.
        This package supports two methods for you to provide that access token:

          1. You may manually specify the access token via the access_token
             argument, when creating a new CiscoSparkAPI object.

          2. If an access_token argument is not supplied, the package checks
             for a SPARK_ACCESS_TOKEN environment variable.

        A ciscosparkapiException is raised if an access token is not provided
        via one of these two methods.

        Args:
            access_token(basestring): The access token to be used for API
                calls to the Cisco Spark service.  Defaults to checking for a
                SPARK_ACCESS_TOKEN environment variable.
            base_url(basestring): The base URL to be prefixed to the
                individual API endpoint suffixes.
                Defaults to ciscosparkapi.DEFAULT_BASE_URL.
            timeout(int): [deprecated] Timeout (in seconds) for RESTful HTTP
                requests. Defaults to ciscosparkapi.DEFAULT_TIMEOUT.
            single_request_timeout(int): Timeout (in seconds) for RESTful HTTP
                requests. Defaults to
                ciscosparkapi.DEFAULT_SINGLE_REQUEST_TIMEOUT.
            wait_on_rate_limit(bool): Enables or disables automatic rate-limit
                handling. Defaults to ciscosparkapi.DEFAULT_WAIT_ON_RATE_LIMIT.

        Returns:
            CiscoSparkAPI: A new CiscoSparkAPI object.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If an access token is not provided via the
                access_token argument or SPARK_ACCESS_TOKEN environment
                variable.

        """
        assert access_token is None or isinstance(access_token, basestring)
        env_access_token = os.environ.get(ACCESS_TOKEN_ENVIRONMENT_VARIABLE)
        access_token = access_token if access_token else env_access_token
        if not access_token:
            error_message = "You must provide an Spark access token to " \
                            "interact with the Cisco Spark APIs, either via " \
                            "a SPARK_ACCESS_TOKEN environment variable " \
                            "or via the access_token argument."
            raise ciscosparkapiException(error_message)

        # Create the API session
        # All of the API calls associated with a CiscoSparkAPI object will
        # leverage a single RESTful 'session' connecting to the Cisco Spark
        # cloud.
        self._session = _RestSession(
            access_token,
            base_url,
            timeout=timeout,
            single_request_timeout=single_request_timeout,
            wait_on_rate_limit=wait_on_rate_limit
        )

        # Spark API wrappers
        self.people = _PeopleAPI(self._session)
        self.rooms = _RoomsAPI(self._session)
        self.memberships = _MembershipsAPI(self._session)
        self.messages = _MessagesAPI(self._session)
        self.teams = _TeamsAPI(self._session)
        self.team_memberships = _TeamMembershipsAPI(self._session)
        self.webhooks = _WebhooksAPI(self._session)
        self.organizations = _OrganizationsAPI(self._session)
        self.licenses = _LicensesAPI(self._session)
        self.roles = _RolesAPI(self._session)
        self.access_tokens = _AccessTokensAPI(self.base_url, timeout=timeout)

    @property
    def access_token(self):
        """The access token used for API calls to the Cisco Spark service."""
        return self._session.access_token

    @property
    def base_url(self):
        """The base URL prefixed to the individual API endpoint suffixes."""
        return self._session.base_url

    @property
    def timeout(self):
        """[deprecated] Timeout (in seconds) for RESTful HTTP requests."""
        return self._session.timeout

    @property
    def single_request_timeout(self):
        """Timeout (in seconds) for an single HTTP request."""
        return self._session.single_request_timeout

    @property
    def wait_on_rate_limit(self):
        """Automatic rate-limit handling enabled / disabled."""
        return self._session.wait_on_rate_limit
