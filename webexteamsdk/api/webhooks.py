# -*- coding: utf-8 -*-
"""Cisco Spark Webhooks API."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from past.builtins import basestring

from ..generator_containers import generator_container
from ..restsession import RestSession
from ..utils import (
    check_type,
    dict_from_items_with_values,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


API_ENDPOINT = 'webhooks'
OBJECT_TYPE = 'webhook'


class WebhooksAPI(object):
    """Cisco Spark Webhooks API.

    Wraps the Cisco Spark Webhooks API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
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
        self._object_factory = object_factory

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
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield webhook objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

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
        json_data = self._session.post(API_ENDPOINT, json=post_data)

        # Return a webhook object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

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
        json_data = self._session.get(API_ENDPOINT + '/' + webhookId)

        # Return a webhook object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

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
        json_data = self._session.put(API_ENDPOINT + '/' + webhookId,
                                      json=put_data)

        # Return a webhook object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

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
        self._session.delete(API_ENDPOINT + '/' + webhookId)
