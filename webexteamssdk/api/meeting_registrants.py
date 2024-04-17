# -*- coding: utf-8 -*-
"""Webex MeetingRegistrants API wrapper.

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


API_ENDPOINT = "meetings/{meetingId}/registrants"
OBJECT_TYPE = "meetingRegistrant"


class MeetingRegistrantsAPI(object):
    """Webex MeetingRegistrants API.

    Wraps the Webex MeetingRegistrants API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new MeetingRegistrantsAPI object with the RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(MeetingRegistrantsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(
        self,
        meetingId,
        max=None,
        hostEmail=None,
        current=None,
        email=None,
        registrationTimeFrom=None,
        registrationTimeTo=None,
        headers=None,
        **request_parameters,
    ):
        """List meetingRegistrants.

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
            meetingId (basestring): Unique identifier for the meeting.
            max (int): Limit the maximum number of registrants in the response,
                up to 100.
            hostEmail (basestring): Email address for the meeting host.
            current (bool): Whether or not to retrieve only the current
                scheduled meeting of the meeting series, i.e. the meeting ready
                to join or start or the upcoming meeting of the meeting series.
            email (basestring): Registrant's email to filter registrants.
            registrationTimeFrom (basestring): The time registrants register a
                meeting starts from the specified date and time (inclusive) in
                any ISO 8601 compliant format.
            registrationTimeTo (basestring): The time registrants register a
                meeting before the specified date and time (exclusive) in any
                ISO 8601 compliant format.
            headers(dict): Additional headers to be passed.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the meetingRegistrants returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(meetingId, basestring)
        check_type(max, int, optional=True)
        check_type(hostEmail, basestring, optional=True)
        check_type(current, bool, optional=True)
        check_type(email, basestring, optional=True)
        check_type(registrationTimeFrom, basestring, optional=True)
        check_type(registrationTimeTo, basestring, optional=True)
        check_type(headers, dict, optional=True)

        headers = headers or {}

        params = dict_from_items_with_values(
            request_parameters,
            max=max,
            hostEmail=hostEmail,
            current=current,
            email=email,
            registrationTimeFrom=registrationTimeFrom,
            registrationTimeTo=registrationTimeTo,
        )

        # Add URL parameters to the API endpoint
        request_url = API_ENDPOINT.format(meetingId=meetingId)

        # API request - get items

        # Update headers
        for k, v in headers.items():
            self._session.headers[k] = v
        items = self._session.get_items(request_url, params=params)

        # Remove headers
        for k in headers.keys():
            del self._session.headers[k]

        # Yield membership objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def create(
        self,
        meetingId,
        firstName,
        lastName,
        email,
        sendEmail=None,
        jobTitle=None,
        address1=None,
        address2=None,
        city=None,
        state=None,
        zipCode=None,
        countryRegion=None,
        workPhone=None,
        fax=None,
        customizedQuestions=None,
        **request_parameters,
    ):
        """Create a meetingRegistrant.

        Args:
            meetingId (basestring): Unique identifier for the meeting.
            firstName (basestring): Registrant's first name.
            lastName (basestring): Registrant's last name.
            email (basestring): Registrant's email.
            sendEmail (bool): If true send email to the registrant.
            jobTitle (basestring): Registrant's job title.
            address1 (basestring): Registrant's first address line.
            address2 (basestring): Registrant's second address line.
            city (basestring): Registrant's city name.
            state (basestring): Registrant's state.
            zipCode (int): Registrant's postal code.
            countryRegion (basestring): Registrant's country or region.
            workPhone (basestring): Registrant's work phone number.
            fax (basestring): Registrant's FAX number.
            customizedQuestions (list): List of registrant's answers for
                customized questions,
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            MeetingRegistrant: A MeetingRegistrant object with the details of
                the created meetingRegistrant.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(meetingId, basestring)
        check_type(firstName, basestring)
        check_type(lastName, basestring)
        check_type(email, basestring)
        check_type(sendEmail, bool, optional=True)
        check_type(jobTitle, basestring, optional=True)
        check_type(address1, basestring, optional=True)
        check_type(address2, basestring, optional=True)
        check_type(city, basestring, optional=True)
        check_type(state, basestring, optional=True)
        check_type(zipCode, int, optional=True)
        check_type(countryRegion, basestring, optional=True)
        check_type(workPhone, basestring, optional=True)
        check_type(fax, basestring, optional=True)
        check_type(customizedQuestions, list, optional=True)

        post_data = dict_from_items_with_values(
            request_parameters,
            firstName=firstName,
            lastName=lastName,
            email=email,
            sendEmail=sendEmail,
            jobTitle=jobTitle,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zipCode=zipCode,
            countryRegion=countryRegion,
            workPhone=workPhone,
            fax=fax,
            customizedQuestions=customizedQuestions,
        )

        # Add URL parameters to the API endpoint
        request_url = API_ENDPOINT.format(meetingId=meetingId)

        # API request
        json_data = self._session.post(request_url, json=post_data)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, meetingId, meetingRegistrantId):
        """Get details for a meetingRegistrant, by ID.

        Args:
            meetingId (basestring): Unique identifier for the meeting.
            meetingRegistrantId(basestring): The meetingRegistrant ID.

        Returns:
            MeetingRegistrant: A MeetingRegistrant object with the details of
                the requested meetingRegistrant.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(meetingId, basestring)
        check_type(meetingRegistrantId, basestring)

        # Add URL parameters to the API endpoint
        request_url = API_ENDPOINT.format(meetingId=meetingId)

        # API request
        json_data = self._session.get(request_url + "/" + meetingRegistrantId)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, meetingId, meetingRegistrantId):
        """Delete a meetingRegistrant, by ID.

        Args:
            meetingId (basestring): Unique identifier for the meeting.
            meetingRegistrantId(basestring): The meetingRegistrant ID.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(meetingId, basestring)
        check_type(meetingRegistrantId, basestring)

        # Add URL parameters to the API endpoint
        request_url = API_ENDPOINT.format(meetingId=meetingId)

        # API request
        self._session.delete(request_url + "/" + meetingRegistrantId)
