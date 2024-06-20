"""Webex Events API wrapper.

Copyright (c) 2016-2024 Cisco and/or its affiliates.

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

from ..generator_containers import generator_container
from ..restsession import RestSession
from ..utils import (
    check_type,
    dict_from_items_with_values,
)


API_ENDPOINT = "events"
OBJECT_TYPE = "event"


class EventsAPI(object):
    """Webex Events API.

    Wraps the Webex Events API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new EventsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(EventsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(
        self,
        resource=None,
        type=None,
        actorId=None,
        _from=None,
        to=None,
        max=None,
        **request_parameters,
    ):
        """List events.

        List events in your organization. Several query parameters are
        available to filter the response.

        Note: `from` is a keyword in Python and may not be used as a variable
        name, so we had to use `_from` instead.

        This method supports Webex's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all events returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Wevex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            resource(str): Limit results to a specific resource type.
                Possible values: "messages", "memberships".
            type(str): Limit results to a specific event type. Possible
                values: "created", "updated", "deleted".
            actorId(str): Limit results to events performed by this
                person, by ID.
            _from(str): Limit results to events which occurred after a
                date and time, in ISO8601 format (yyyy-MM-dd'T'HH:mm:ss.SSSZ).
            to(str): Limit results to events which occurred before a
                date and time, in ISO8601 format (yyyy-MM-dd'T'HH:mm:ss.SSSZ).
            max(int): Limit the maximum number of items returned from the Webex
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the events returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(resource, str, optional=True)
        check_type(type, str, optional=True)
        check_type(actorId, str, optional=True)
        check_type(_from, str, optional=True)
        check_type(to, str, optional=True)
        check_type(max, int, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            resource=resource,
            type=type,
            actorId=actorId,
            _from=_from,
            to=to,
            max=max,
        )

        if _from:
            params["from"] = params.pop("_from")

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield event objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def get(self, eventId):
        """Get the details for an event, by event ID.

        Args:
            eventId(str): The ID of the event to be retrieved.

        Returns:
            Event: A event object with the details of the requested room.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(eventId, str)

        # API request
        json_data = self._session.get(API_ENDPOINT + "/" + eventId)

        # Return a room object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
