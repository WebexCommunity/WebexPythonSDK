# -*- coding: utf-8 -*-
"""Cisco Spark Webhooks API wrapper.

Classes:
    Webhook: Models a Spark 'webhook' JSON object as a native Python object.
    WebhooksAPI: Wraps the Cisco Spark Webhooks API and exposes the API as
        native Python methods that return native Python objects.

"""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
from past.builtins import basestring

from ..api.memberships import Membership
from ..api.messages import Message
from ..api.rooms import Room
from ..restsession import RestSession
from ..sparkdata import SparkData
from ..utils import (
    check_type,
    dict_from_items_with_values,
    generator_container,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


class Webhook(SparkData):
    """Model a Spark 'webhook' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Webhook data object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Webhook, self).__init__(json)

    @property
    def id(self):
        """Webhook ID."""
        return self._json_data.get('id')

    @property
    def name(self):
        """A user-friendly name for this webhook."""
        return self._json_data.get('name')

    @property
    def targetUrl(self):
        """The URL that receives POST requests for each event."""
        return self._json_data.get('targetUrl')

    @property
    def resource(self):
        """The resource type for the webhook."""
        return self._json_data.get('resource')

    @property
    def event(self):
        """The event type for the webhook."""
        return self._json_data.get('event')

    @property
    def filter(self):
        """The filter that defines the webhook scope."""
        return self._json_data.get('filter')

    @property
    def secret(self):
        """Secret used to generate payload signature."""
        return self._json_data.get('secret')

    @property
    def orgId(self):
        """The ID of the organization that owns the webhook."""
        return self._json_data.get('orgId')

    @property
    def createdBy(self):
        """The ID of the person that added the webhook."""
        return self._json_data.get('createdBy')

    @property
    def appId(self):
        """Identifies the application that added the webhook."""
        return self._json_data.get('appId')

    @property
    def ownedBy(self):
        """Indicates if the webhook is owned by the `org` or the `creator`.

        Webhooks owned by the creator can only receive events that are
        accessible to the creator of the webhook. Those owned by the
        organization will receive events that are visible to anyone in the
        organization.

        """
        return self._json_data.get('ownedBy')

    @property
    def status(self):
        """Indicates if the webhook is active.

        A webhook that cannot reach your URL is disabled.

        """
        return self._json_data.get('status')

    @property
    def created(self):
        """Creation date and time in ISO8601 format."""
        return self._json_data.get('created')


class WebhookEvent(SparkData):
    """Model a Spark webhook event JSON object as a native Python object."""

    def __init__(self, json):
        """Init a WebhookEvent data object from a JSON dictionary or string.

        Args:
            json(dict, basestring): Input dictionary or JSON string.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(WebhookEvent, self).__init__(json)

        self._data = None

    @property
    def id(self):
        """Webhook ID."""
        return self._json_data.get('id')

    @property
    def name(self):
        """A user-friendly name for this webhook."""
        return self._json_data.get('name')

    @property
    def resource(self):
        """The resource type for the webhook."""
        return self._json_data.get('resource')

    @property
    def event(self):
        """The event type for the webhook."""
        return self._json_data.get('event')

    @property
    def filter(self):
        """The filter that defines the webhook scope."""
        return self._json_data.get('filter')

    @property
    def orgId(self):
        """The ID of the organization that owns the webhook."""
        return self._json_data.get('orgId')

    @property
    def createdBy(self):
        """The ID of the person that added the webhook."""
        return self._json_data.get('createdBy')

    @property
    def appId(self):
        """Identifies the application that added the webhook."""
        return self._json_data.get('appId')

    @property
    def ownedBy(self):
        """Indicates if the webhook is owned by the `org` or the `creator`.

        Webhooks owned by the creator can only receive events that are
        accessible to the creator of the webhook. Those owned by the
        organization will receive events that are visible to anyone in the
        organization.

        """
        return self._json_data.get('ownedBy')

    @property
    def status(self):
        """Indicates if the webhook is active.

        A webhook that cannot reach your URL is disabled.

        """
        return self._json_data.get('status')

    @property
    def actorId(self):
        """The ID of the person that caused the webhook to be sent."""
        return self._json_data.get('actorId')

    @property
    def data(self):
        """The data for the resource that triggered the webhook.

        For example, if you registered a webhook that triggers when messages
        are created (i.e. posted into a room) then the data property will
        contain the JSON representation for a message resource.

        Note:  That not all of the details of the resource are included in the
        data object.  For example, the contents of a message are not included.
        You would need to request the details for the message using the message
        'id' (which is in the data object) and the
        `CiscoSparkAPI.messages.get()` method.

        """
        if self._data is None and self._json_data.get('data'):
            if self.resource == "memberships":
                self._data = Membership(self._json_data.get('data'))

            elif self.resource == "messages":
                self._data = Message(self._json_data.get('data'))

            elif self.resource == "rooms":
                self._data = Room(self._json_data.get('data'))

            else:
                self._data = SparkData(self._json_data.get('data'))

        return self._data


class WebhooksAPI(object):
    """Cisco Spark Webhooks API wrapper.

    Wraps the Cisco Spark Webhooks API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session):
        """Initialize a new WebhooksAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(WebhooksAPI, self).__init__()

        self._session = session

    @generator_container
    def list(self, max=None, **request_parameters):
        """List all of the authenticated user's webhooks.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all webhooks returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            max(int): Limit the maximum number of items returned from the Spark
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
                yields the webhooks returned by the Cisco Spark query.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(max, int)

        params = dict_from_items_with_values(
            request_parameters,
            max=max,
        )

        # API request - get items
        items = self._session.get_items('webhooks', params=params)

        # Yield Webhook objects created from the returned items JSON objects
        for item in items:
            yield Webhook(item)

    def create(self, name, targetUrl, resource, event,
               filter=None, secret=None, **request_parameters):
        """Create a webhook.

        Args:
            name(basestring): A user-friendly name for this webhook.
            targetUrl(basestring): The URL that receives POST requests for
                each event.
            resource(basestring): The resource type for the webhook.
            event(basestring): The event type for the webhook.
            filter(basestring): The filter that defines the webhook scope.
            secret(basestring): The secret used to generate payload signature.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Webhook: A Webhook object with the details of the created webhook.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(name, basestring, may_be_none=False)
        check_type(targetUrl, basestring, may_be_none=False)
        check_type(resource, basestring, may_be_none=False)
        check_type(event, basestring, may_be_none=False)
        check_type(filter, basestring)
        check_type(secret, basestring)

        post_data = dict_from_items_with_values(
            request_parameters,
            name=name,
            targetUrl=targetUrl,
            resource=resource,
            event=event,
            filter=filter,
            secret=secret,
        )

        # API request
        json_data = self._session.post('webhooks', json=post_data)

        # Return a Webhook object created from the response JSON data
        return Webhook(json_data)

    def get(self, webhookId):
        """Get the details of a webhook, by ID.

        Args:
            webhookId(basestring): The ID of the webhook to be retrieved.

        Returns:
            Webhook: A Webhook object with the details of the requested
                webhook.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(webhookId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get('webhooks/' + webhookId)

        # Return a Webhook object created from the response JSON data
        return Webhook(json_data)

    def update(self, webhookId, name=None, targetUrl=None,
               **request_parameters):
        """Update a webhook, by ID.

        Args:
            webhookId(basestring): The webhook ID.
            name(basestring): A user-friendly name for this webhook.
            targetUrl(basestring): The URL that receives POST requests for
                each event.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Webhook: A Webhook object with the updated Spark webhook details.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(webhookId, basestring, may_be_none=False)
        check_type(name, basestring)
        check_type(targetUrl, basestring)

        put_data = dict_from_items_with_values(
            request_parameters,
            name=name,
            targetUrl=targetUrl,
        )

        # API request
        json_data = self._session.put('webhooks/' + webhookId, json=put_data)

        # Return a Webhook object created from the response JSON data
        return Webhook(json_data)

    def delete(self, webhookId):
        """Delete a webhook, by ID.

        Args:
            webhookId(basestring): The ID of the webhook to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(webhookId, basestring, may_be_none=False)

        # API request
        self._session.delete('webhooks/' + webhookId)
