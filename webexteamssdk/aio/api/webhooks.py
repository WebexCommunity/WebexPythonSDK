# -*- coding: utf-8 -*-
"""Webex Teams Webhooks API wrapper.

Copyright (c) 2016-2019 Cisco and/or its affiliates.

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


from webexteamssdk.generator_containers import generator_container
from webexteamssdk.aio.restsession import AsyncRestSession
from webexteamssdk.aio.utils import (
    check_type,
    dict_from_items_with_values,
)


API_ENDPOINT = "webhooks"
OBJECT_TYPE = "webhook"


class AsyncWebhooksAPI:
    """Webex Teams Webhooks API.

    Wraps the Webex Teams Webhooks API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session: AsyncRestSession, object_factory):
        """Initialize a new WebhooksAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, AsyncRestSession)

        super().__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    async def list(self, max=None, **request_parameters):
        """List all of the authenticated user's webhooks.

        This method supports Webex Teams's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all webhooks returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            max(int): Limit the maximum number of items returned from the Webex
                Teams service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the webhooks returned by the Webex Teams query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(max, int, optional=True)

        params = dict_from_items_with_values(request_parameters, max=max,)

        # API request - get items
        items = await self._session.get_items(API_ENDPOINT, params=params)

        # Yield webhook objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    async def create(
        self,
        name,
        targetUrl,
        resource,
        event,
        filter=None,
        secret=None,
        **request_parameters
    ):
        """Create a webhook.

        Args:
            name(str): A user-friendly name for this webhook.
            targetUrl(str): The URL that receives POST requests for
                each event.
            resource(str): The resource type for the webhook.
            event(str): The event type for the webhook.
            filter(str): The filter that defines the webhook scope.
            secret(str): The secret used to generate payload signature.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Webhook: A Webhook object with the details of the created webhook.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(name, str)
        check_type(targetUrl, str)
        check_type(resource, str)
        check_type(event, str)
        check_type(filter, str, optional=True)
        check_type(secret, str, optional=True)

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
        json_data = await self._session.post(API_ENDPOINT, json=post_data)

        # Return a webhook object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    async def get(self, webhookId):
        """Get the details of a webhook, by ID.

        Args:
            webhookId(str): The ID of the webhook to be retrieved.

        Returns:
            Webhook: A Webhook object with the details of the requested
            webhook.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(webhookId, str)

        # API request
        json_data = await self._session.get(API_ENDPOINT + "/" + webhookId)

        # Return a webhook object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    async def update(self, webhookId, name=None, targetUrl=None, **request_parameters):
        """Update a webhook, by ID.

        Args:
            webhookId(str): The webhook ID.
            name(str): A user-friendly name for this webhook.
            targetUrl(str): The URL that receives POST requests for
                each event.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Webhook: A Webhook object with the updated Webex Teams webhook
                details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(webhookId, str)
        check_type(name, str, optional=True)
        check_type(targetUrl, str, optional=True)

        put_data = dict_from_items_with_values(
            request_parameters, name=name, targetUrl=targetUrl,
        )

        # API request
        json_data = await self._session.put(
            API_ENDPOINT + "/" + webhookId, json=put_data
        )

        # Return a webhook object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    async def delete(self, webhookId):
        """Delete a webhook, by ID.

        Args:
            webhookId(str): The ID of the webhook to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(webhookId, str)

        # API request
        await self._session.delete(API_ENDPOINT + "/" + webhookId)
