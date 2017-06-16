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

import os

from ciscosparkapi.exceptions import ciscosparkapiException, SparkApiError
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.api.people import Person, PeopleAPI
from ciscosparkapi.api.rooms import Room, RoomsAPI
from ciscosparkapi.api.memberships import Membership, MembershipsAPI
from ciscosparkapi.api.messages import Message, MessagesAPI
from ciscosparkapi.api.teams import Team, TeamsAPI
from ciscosparkapi.api.teammemberships import (
    TeamMembership,
    TeamMembershipsAPI
)
from ciscosparkapi.api.webhooks import Webhook, WebhooksAPI
from ciscosparkapi.api.organizations import Organization, OrganizationsAPI
from ciscosparkapi.api.licenses import License, LicensesAPI
from ciscosparkapi.api.roles import Role, RolesAPI
from ciscosparkapi.api.accesstokens import AccessToken, AccessTokensAPI


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


# Versioneer version control
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


DEFAULT_BASE_URL = 'https://api.ciscospark.com/v1/'
DEFAULT_TIMEOUT = 60
ACCESS_TOKEN_ENVIRONMENT_VARIABLE = 'SPARK_ACCESS_TOKEN'


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
                 timeout=DEFAULT_TIMEOUT):
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
            access_token(str): The access token to be used for API
                calls to the Cisco Spark service.  Defaults to checking for a
                SPARK_ACCESS_TOKEN environment variable.
            base_url(str): The base URL to be prefixed to the
                individual API endpoint suffixes.
                Defaults to ciscosparkapi.DEFAULT_BASE_URL.
            timeout(int): Timeout (in seconds) for RESTful HTTP requests.
                Defaults to ciscosparkapi.DEFAULT_TIMEOUT.

        Returns:
            CiscoSparkAPI: A new CiscoSparkAPI object.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If an access token is not provided via the
                access_token argument or SPARK_ACCESS_TOKEN environment
                variable.

        """
        # Process args
        assert access_token is None or isinstance(access_token, basestring)
        assert isinstance(base_url, str)
        assert isinstance(timeout, int)
        spark_access_token = os.environ.get(ACCESS_TOKEN_ENVIRONMENT_VARIABLE)
        access_token = access_token if access_token else spark_access_token
        if not access_token:
            error_message = "You must provide an Spark access token to " \
                            "interact with the Cisco Spark APIs, either via " \
                            "a SPARK_ACCESS_TOKEN environment variable " \
                            "or via the access_token argument."
            raise ciscosparkapiException(error_message)
        session_args = {u'timeout': timeout}

        # Create the API session
        # All of the API calls associated with a CiscoSparkAPI object will
        # leverage a single RESTful 'session' connecting to the Cisco Spark
        # cloud.
        self._session = RestSession(access_token, base_url, **session_args)

        # Spark API wrappers
        self.people = PeopleAPI(self._session)
        self.rooms = RoomsAPI(self._session)
        self.memberships = MembershipsAPI(self._session)
        self.messages = MessagesAPI(self._session)
        self.teams = TeamsAPI(self._session)
        self.team_memberships = TeamMembershipsAPI(self._session)
        self.webhooks = WebhooksAPI(self._session)
        self.organizations = OrganizationsAPI(self._session)
        self.licenses = LicensesAPI(self._session)
        self.roles = RolesAPI(self._session)
        self.access_tokens = AccessTokensAPI(self.base_url, timeout=timeout)

    @property
    def access_token(self):
        return self._session.access_token

    @property
    def base_url(self):
        return self._session.base_url

    @property
    def timeout(self):
        return self._session.timeout
