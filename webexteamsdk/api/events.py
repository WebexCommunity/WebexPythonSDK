# -*- coding: utf-8 -*-
"""Cisco Spark Events API."""


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


API_ENDPOINT = 'events'
OBJECT_TYPE = 'event'


class EventsAPI(object):
    """Cisco Spark Events API.

    Wraps the Cisco Spark Events API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new EventsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession, may_be_none=False)

        super(EventsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, resource=None, type=None, actorId=None, _from=None, to=None,
             max=None, **request_parameters):
        """List events.

        List events in your organization. Several query parameters are
        available to filter the response.

        Note: `from` is a keyword in Python and may not be used as a variable
        name, so we had to use `_from` instead.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all events returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            resource(basestring): Limit results to a specific resource type.
                Possible values: "messages", "memberships".
            type(basestring): Limit results to a specific event type. Possible
                values: "created", "updated", "deleted".
            actorId(basestring): Limit results to events performed by this
                person, by ID.
            _from(basestring): Limit results to events which occurred after a
                date and time, in ISO8601 format (yyyy-MM-dd'T'HH:mm:ss.SSSZ).
            to(basestring): Limit results to events which occurred before a
                date and time, in ISO8601 format (yyyy-MM-dd'T'HH:mm:ss.SSSZ).
            max(int): Limit the maximum number of items returned from the Spark
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
                yields the events returned by the Cisco Spark query.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(resource, basestring)
        check_type(type, basestring)
        check_type(actorId, basestring)
        check_type(_from, basestring)
        check_type(to, basestring)
        check_type(max, int)

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
            eventId(basestring): The ID of the event to be retrieved.

        Returns:
            Event: A event object with the details of the requested room.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(eventId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get(API_ENDPOINT + '/' + eventId)

        # Return a room object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
