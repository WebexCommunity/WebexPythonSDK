# -*- coding: utf-8 -*-
"""Python API wrapper for the Cisco Spark APIs."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *
import logging
import os

from past.builtins import basestring

from .api.access_tokens import AccessTokensAPI as _AccessTokensAPI
from .api.licenses import LicensesAPI as _LicensesAPI
from .api.memberships import MembershipsAPI as _MembershipsAPI
from .api.messages import MessagesAPI as _MessagesAPI
from .api.organizations import OrganizationsAPI as _OrganizationsAPI
from .api.people import PeopleAPI as _PeopleAPI
from .api.roles import RolesAPI as _RolesAPI
from .api.rooms import RoomsAPI as _RoomsAPI
from .api.team_memberships import TeamMembershipsAPI as _TeamMembershipsAPI
from .api.teams import TeamsAPI as _TeamsAPI
from .api.webhooks import WebhooksAPI as _WebhooksAPI
from .exceptions import (
    SparkApiError, SparkRateLimitError, SparkRateLimitWarning,
    ciscosparkapiException,
)
from .models import (
    AccessToken, License, Membership, Message, Organization, Person, Role,
    Room, Team, TeamMembership, Webhook, WebhookEvent, sparkdata_factory,
)
from .restsession import (
    DEFAULT_SINGLE_REQUEST_TIMEOUT,
    DEFAULT_WAIT_ON_RATE_LIMIT,
    RestSession as _RestSession,
)
from .utils import check_type


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


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

    :CiscoSparkAPI: :class:`people <_PeopleAPI>`

                    :class:`rooms <_RoomsAPI>`

                    :class:`memberships <_MembershipsAPI>`

                    :class:`messages <_MessagesAPI>`

                    :class:`teams <_TeamsAPI>`

                    :class:`team_memberships <_TeamMembershipsAPI>`

                    :class:`webhooks <_WebhooksAPI>`

                    :class:`organizations <_OrganizationsAPI>`

                    :class:`licenses <_LicensesAPI>`

                    :class:`roles <_RolesAPI>`

                    :class:`access_tokens <_AccessTokensAPI>`

    """

    def __init__(self, access_token=None, base_url=DEFAULT_BASE_URL,
                 timeout=None,
                 single_request_timeout=DEFAULT_SINGLE_REQUEST_TIMEOUT,
                 wait_on_rate_limit=DEFAULT_WAIT_ON_RATE_LIMIT,
                 object_factory=sparkdata_factory):
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
            object_factory(callable): The factory function to use to create
                Python objects from the returned Cisco Spark JSON data objects.

        Returns:
            CiscoSparkAPI: A new CiscoSparkAPI object.

        Raises:
            TypeError: If the parameter types are incorrect.
            ciscosparkapiException: If an access token is not provided via the
                access_token argument or SPARK_ACCESS_TOKEN environment
                variable.

        """
        check_type(access_token, basestring)
        check_type(base_url, basestring)
        check_type(single_request_timeout, int)
        check_type(wait_on_rate_limit, bool)

        env_access_token = os.environ.get(ACCESS_TOKEN_ENVIRONMENT_VARIABLE)
        access_token = access_token or env_access_token
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
        self.people = _PeopleAPI(self._session, object_factory)
        self.rooms = _RoomsAPI(self._session, object_factory)
        self.memberships = _MembershipsAPI(self._session, object_factory)
        self.messages = _MessagesAPI(self._session, object_factory)
        self.teams = _TeamsAPI(self._session, object_factory)
        self.team_memberships = _TeamMembershipsAPI(
            self._session, object_factory
        )
        self.webhooks = _WebhooksAPI(self._session, object_factory)
        self.organizations = _OrganizationsAPI(self._session, object_factory)
        self.licenses = _LicensesAPI(self._session, object_factory)
        self.roles = _RolesAPI(self._session, object_factory)
        self.access_tokens = _AccessTokensAPI(
            self.base_url, object_factory, timeout=single_request_timeout
        )

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
