# -*- coding: utf-8 -*-
"""Webex MeetingInvitees API wrapper.

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


API_ENDPOINT = "meetingInvitees"
OBJECT_TYPE = "meetingInvitee"


class MeetingInviteesAPI(object):
    """Webex MeetingInvitees API.

    Wraps the Webex MeetingInvitees API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new MeetingInviteesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(MeetingInviteesAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(
        self,
        meetingId,
        max=None,
        hostEmail=None,
        panelist=None,
        headers=None,
        **request_parameters,
    ):
        """List meetingInvitees.

        Use query parameters to filter the response.

        This method supports Webex Teams's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all memberships returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            meetingId (basestring): Unique id of the meeting for which invitees
                are requested.
            max (int): Limit the number of meeting invitees.
            hostEmail (basestring): Email address for the meeting host
                (requires admin scope).
            panelist (bool): Filter invitees or attendees based on their
                panelist status.
            headers(dict): Additional headers to be passed.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the meetingInvitees returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(meetingId, basestring)
        check_type(max, int, optional=True)
        check_type(hostEmail, basestring, optional=True)
        check_type(panelist, bool, optional=True)
        check_type(headers, dict, optional=True)

        headers = headers or {}

        params = dict_from_items_with_values(
            request_parameters,
            meetingId=meetingId,
            max=max,
            hostEmail=hostEmail,
            panelist=panelist,
        )

        # API request - get items

        # Update headers
        for k, v in headers.items():
            self._session.headers[k] = v
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Remove headers
        for k in headers.keys():
            del self._session.headers[k]

        # Yield membership objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def create(
        self,
        meetingId,
        email,
        displayName=None,
        coHost=None,
        hostEmail=None,
        sendEmail=None,
        panelist=None,
        **request_parameters,
    ):
        """Create a meetingInvitee.

        Args:
            meetingId (basestring): Unique id for the meeting that the invitee
                is part of.
            email (basestring): Email address for the meeting invitee.
            displayName (basestring): Display name of the meeting invitee.
            coHost (bool): CoHost status of the invitee.
            hostEmail (basestring): Email address for the meeting host
                (requires admin scope).
            sendEmail (bool): If true, send an e-mail to the invitee.
            panelist (bool): Flag to indicate if the invitee is panelist or
                not.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            MeetingInvitee: A MeetingInvitee object with the details of the
            created meetingInvitee.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(meetingId, basestring)
        check_type(email, basestring)
        check_type(displayName, basestring, optional=True)
        check_type(coHost, bool, optional=True)
        check_type(hostEmail, basestring, optional=True)
        check_type(sendEmail, bool, optional=True)
        check_type(panelist, bool, optional=True)

        post_data = dict_from_items_with_values(
            request_parameters,
            meetingId=meetingId,
            email=email,
            displayName=displayName,
            coHost=coHost,
            hostEmail=hostEmail,
            sendEmail=sendEmail,
            panelist=panelist,
        )

        # API request
        json_data = self._session.post(API_ENDPOINT, json=post_data)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, meetingInviteeId):
        """Get details for a meetingInvitee, by ID.

        Args:
            meetingInviteeId(basestring): The meetingInvitee ID.

        Returns:
            MeetingInvitee: A MeetingInvitee object with the details of the
            requested meetingInvitee.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(meetingInviteeId, basestring)

        # API request
        json_data = self._session.get(API_ENDPOINT + "/" + meetingInviteeId)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, meetingInviteeId):
        """Delete a meetingInvitee, by ID.

        Args:
            meetingInviteeId(basestring): The meetingInvitee ID.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(meetingInviteeId, basestring)

        # API request
        self._session.delete(API_ENDPOINT + "/" + meetingInviteeId)

    def update(
        self,
        meetingInviteeId,
        email,
        displayName=None,
        coHost=None,
        hostEmail=None,
        sendEmail=None,
        panelist=None,
        **request_parameters,
    ):
        """Update properties for a meetingInvitee, by ID.

        Args:
            meetingInviteeId(basestring): The meetingInvitee ID.
            email (basestring): Email address for the meeting invitee.
            displayName (basestring): Display name of the meeting invitee.
            coHost (bool): Cohost status of the invitee.
            hostEmail (basestring): Email address for the meeting host
                (requires admin scope).
            sendEmail (bool): If true, send an e-mail to the invitee.
            panelist (bool): Flag to indicate if the invitee is panelist or
                not.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            MeetingInvitee: A MeetingInvitee object with the updated Webex
            meetingInvitee details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(meetingInviteeId, basestring)
        check_type(email, basestring)
        check_type(displayName, basestring, optional=True)
        check_type(coHost, bool, optional=True)
        check_type(hostEmail, basestring, optional=True)
        check_type(sendEmail, bool, optional=True)
        check_type(panelist, bool, optional=True)

        put_data = dict_from_items_with_values(
            request_parameters,
            email=email,
            displayName=displayName,
            coHost=coHost,
            hostEmail=hostEmail,
            sendEmail=sendEmail,
            panelist=panelist,
        )

        # API request
        json_data = self._session.put(
            API_ENDPOINT + "/" + meetingInviteeId, json=put_data
        )

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def bulk(
        self, meetingId, hostEmail=None, items=None, **request_parameters
    ):
        """Bulk insert meeting invitees

        Args:
          meetingId(basestring): Id of the meeting the invitees should be added
            to.
          hostEmail(basestring): Email of the meeting host.
          items(list): List of invitees. Each invitee is a dict with email as
            the required key and displayName, coHost, sendEmail and panelist as
            optional properties.
          **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
          GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the meetingInvitees returned by the Webex query.

        Raises:
          TypeError: If the parameter types are incorrect.
          ApiError: If the Webex Teams cloud returns an error.
        """
        check_type(meetingId, basestring)
        check_type(hostEmail, basestring, optional=True)
        check_type(items, list, optional=True)

        post_data = dict_from_items_with_values(
            request_parameters,
            meetingId=meetingId,
            items=items,
            hostEmail=hostEmail,
        )

        # API request
        json_data = self._session.put(
            API_ENDPOINT + "/bulkInsert", json=post_data
        )

        # Return an object created from the response JSON data
        for itm in json_data["items"]:
            yield self._object_factory(OBJECT_TYPE, itm)
