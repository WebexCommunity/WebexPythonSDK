# Versioneer version control
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from exceptions import ciscosparkapiException, SparkApiError
from restsession import RestSession
from api.accesstokens import AccessToken, AccessTokensAPI
from api.people import Person, PeopleAPI
from api.rooms import Room, RoomsAPI
from api.memberships import Membership, MembershipsAPI
from api.messages import Message, MessagesAPI
from api.teams import Team, TeamsAPI
from api.teammemberships import TeamMembership, TeamMembershipsAPI
from api.webhooks import Webhook, WebhooksAPI


# Default base URL
DEFAULT_BASE_URL = 'https://api.ciscospark.com/v1/'


class CiscoSparkAPI(object):
    """Cisco Spark API wrapper class."""

    def __init__(self, access_token, base_url=DEFAULT_BASE_URL, timeout=None):
        # Process args
        assert isinstance(access_token, basestring)
        # Process kwargs
        session_args = {}
        if timeout:
            session_args['timeout'] = timeout

        # Create API session
        # All of the API calls associated with a CiscoSparkAPI object will
        # leverage a single RESTful 'session' connecting to the Cisco Spark
        # cloud.
        self.session = RestSession(access_token, base_url, **session_args)

        # Spark API wrappers
        self.access_tokens = AccessTokensAPI(self.base_url, timeout=timeout)
        self.people = PeopleAPI(self.session)
        self.rooms = RoomsAPI(self.session)
        self.memberships = MembershipsAPI(self.session)
        self.messages = MessagesAPI(self.session)
        self.teams = TeamsAPI(self.session)
        self.team_memberships = TeamMembershipsAPI(self.session)
        self.webhooks = WebhooksAPI(self.session)

    @property
    def access_token(self):
        return self.session.access_token

    @property
    def base_url(self):
        return self.session.base_url

    @property
    def timeout(self):
        return self.session.timeout
