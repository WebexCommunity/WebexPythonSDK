# -*- coding: utf-8 -*-
"""Webex Admin Audit Events API wrapper.

Copyright (c) 2016-2020 Cisco and/or its affiliates.

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


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from past.builtins import basestring

from webexteamssdk.generator_containers import generator_container
from webexteamssdk.restsession import RestSession
from webexteamssdk.utils import check_type, dict_from_items_with_values


API_ENDPOINT = 'adminAudit/events'
OBJECT_TYPE = 'admin_audit_event'


class AdminAuditEventsAPI(object):
    """Admin Audit Events API.

    Wraps the Webex Teams Admin Audit Events API and exposes the API as native
    Python methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new AdminAuditEventsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(AdminAuditEventsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, orgId, _from, to, actorId=None, max=100, offset=0,
             **request_parameters):
        """List Organizations.

        This method supports Webex Teams's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all audit events returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            orgId(basestring): List events in this organization, by ID.
            _from(basestring): List events which occurred after a specific
                date and time.
            to(basestring): List events which occurred before a specific date
                and time.
            actorId(basestring): List events performed by this person, by ID.
            max(int): Limit the maximum number of events in the response. The
                maximum value is 200.
            offset(int): Offset from the first result that you want to fetch.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the organizations returned by the Webex Teams query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.
        """
        check_type(orgId, basestring)
        check_type(_from, basestring)
        check_type(to, basestring)
        check_type(actorId, basestring, optional=True)
        check_type(max, int)
        check_type(offset, int)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
            _from=_from,
            to=to,
            actorId=actorId,
            max=max,
            offset=offset,
        )

        if _from:
            params["from"] = params.pop("_from")

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield AdminAuditEvent objects created from the returned JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)
