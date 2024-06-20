"""Webex Meetings API wrapper.

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


API_ENDPOINT = "meetings"
OBJECT_TYPE = "meeting"


class MeetingsAPI(object):
    """Webex Meetings API.

    Wraps the Webex Meetings API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new MeetingsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(MeetingsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(
        self,
        meetingNumber=None,
        webLink=None,
        roomId=None,
        meetingType=None,
        state=None,
        scheduledType=None,
        participantEmail=None,
        current=None,
        from_=None,
        to=None,
        max=None,
        hostEmail=None,
        siteUrl=None,
        integrationTag=None,
        headers=None,
        **request_parameters,
    ):
        """List meetings.

        Use query parameters to filter the response.

        This method supports Webex's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all memberships returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            meetingNumber (str): Meeting number for the meeting objects
                being requested.
            webLink (str): URL encoded link to information page.
            roomId (str): Associated teams space room ID.
            meetingType (str): Type of the meeting (meetingSeries,
                scheduledMeeting, meeting).
            state (str):
            scheduledType (str): Schedule type of this meeting (meeting,
                webinar, personalRoomMeeting).
            participantEmail (str): E-Mail of a meeting participant.
            current (bool): Flag to retrieve the current scheduled meeting of a
                series.
            from_ (str): Start date and time in ISO 8601 format.
            to (str): To date and time in ISO 8601 format.
            max (int): Limit the number of meetings in response.
            hostEmail (str): Email address for the meeting host (Needs
                admin-level scope).
            siteUrl (str): URL of the webex site.
            integrationTag (str): External tag set by integrations.
            headers(dict): Additional headers to be passed.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the meetings returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(meetingNumber, str, optional=True)
        check_type(webLink, str, optional=True)
        check_type(roomId, str, optional=True)
        check_type(meetingType, str, optional=True)
        check_type(state, str, optional=True)
        check_type(scheduledType, str, optional=True)
        check_type(participantEmail, str, optional=True)
        check_type(current, bool, optional=True)
        check_type(from_, str, optional=True)
        check_type(to, str, optional=True)
        check_type(max, int, optional=True)
        check_type(hostEmail, str, optional=True)
        check_type(siteUrl, str, optional=True)
        check_type(integrationTag, str, optional=True)
        check_type(headers, dict, optional=True)

        headers = headers if headers is not None else {}

        params = dict_from_items_with_values(
            request_parameters,
            meetingNumber=meetingNumber,
            webLink=webLink,
            roomId=roomId,
            meetingType=meetingType,
            state=state,
            scheduledType=scheduledType,
            participantEmail=participantEmail,
            current=current,
            from_=from_,
            to=to,
            max=max,
            hostEmail=hostEmail,
            siteUrl=siteUrl,
            integrationTag=integrationTag,
        )

        if from_:
            params["from"] = params.pop("from_")

        request_url = API_ENDPOINT

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
        title,
        start,
        end,
        templateId=None,
        agenda=None,
        password=None,
        timezone=None,
        recurrence=None,
        enabledAutoRecordMeeting=None,
        allowAnyUserToBeCoHost=None,
        enabledJoinBeforeHost=None,
        enableConnectAudioBeforeHost=None,
        joinBeforeHostMinutes=None,
        excludePassword=None,
        publicMeeting=None,
        reminderTime=None,
        unlockedMeetingJoinSecurity=None,
        sessionTypeId=None,
        scheduledType=None,
        enabledWebcastView=None,
        panelistPassword=None,
        enableAutomaticLock=None,
        automaticLockMinutes=None,
        allowFirstUserToBeCoHost=None,
        allowAuthenticatedDevices=None,
        invitees=None,
        sendEmail=None,
        hostEmail=None,
        siteUrl=None,
        meetingOptions=None,
        registration=None,
        integrationTags=None,
        simultaneousInterpretation=None,
        enabledBreakoutSessions=None,
        breakoutSessions=None,
        **request_parameters,
    ):
        """Create a meeting.

        Args:
            title (str): Title of the meeting.
            start (str): Start time of the meeting in ISO 8601.
            end (str): End time of the meeting in ISO 8601.
            templateId (str): Unique identifier for meeting template.
            agenda (str): Meeting agenda (Maximum 1300 characters).
            password (str): Password of the meeting.
            timezone (str): Time zone of start and end property in
                IANA time zone database format.
            recurrence (str): Meeting recurrence according to RFC 2445.
            enabledAutoRecordMeeting (bool): Whether or not meeting is
                recorded automatically.
            allowAnyUserToBeCoHost (bool): Allow any attendee with host
                account on site to become cohost.
            enabledJoinBeforeHost (bool): Allow attendees to join before the
                host.
            enableConnectAudioBeforeHost (bool): Allow attendees to connect
                audio before the host joins.
            joinBeforeHostMinutes (int): Number of minutes attendees can join
                before the start time.
            excludePassword (bool): Exclude meeting password from meeting
                invite emails.
            publicMeeting (bool): Allow meeting to be listed on public
                calendar.
            reminderTime (int): Number of minutes before start time a reminder
                is send to the host.
            unlockedMeetingJoinSecurity (str): Join settings for
                uninvited people.
            sessionTypeId (str): Unique identifier for a meeting
                session type.
            scheduledType (str): Type of meeting (regular, webinar,
                meeting in personal room).
            enabledWebcastView (bool): Whether or not webcast view is enabled.
            panelistPassword (str): Password for panelists of a
                webinar meeting.
            enableAutomaticLock (bool): Whether or not to automatically lock
                the meeting after start.
            automaticLockMinutes (int): Number of minutes for the meeting to
                be automatically locked.
            allowFirstUserToBeCoHost (bool): Allow the first joiner with host
                account on the meeting site to be cohost.
            allowAuthenticatedDevices (bool): Whether or not to allow
                authenticated video devices in the meeting's organization to
                start or join the meeting.
            invitees (list): List of invitee objects.
            sendEmail (bool): Send an invite e-mail.
            hostEmail (str): Email address of the meeting host.
            siteUrl (str): Site URL for the meeting.
            meetingOptions (dict): Options for this meeting.
            registration (dict): Meeting registration information.
            integrationTags (list): List of external keys created by
                integrations.
            simultaneousInterpretation (dict): Simultaneous interpretation
                information for the meeting.
            enabledBreakoutSessions (bool): Flag to enable breakout sessions
                in this meeting.
            breakoutSessions (list): List of breakout sessions.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Meeting: A Meeting object with the details of the created meeting.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(title, str)
        check_type(start, str)
        check_type(end, str)
        check_type(templateId, str, optional=True)
        check_type(agenda, str, optional=True)
        check_type(password, str, optional=True)
        check_type(timezone, str, optional=True)
        check_type(recurrence, str, optional=True)
        check_type(enabledAutoRecordMeeting, bool, optional=True)
        check_type(allowAnyUserToBeCoHost, bool, optional=True)
        check_type(enabledJoinBeforeHost, bool, optional=True)
        check_type(enableConnectAudioBeforeHost, bool, optional=True)
        check_type(joinBeforeHostMinutes, int, optional=True)
        check_type(excludePassword, bool, optional=True)
        check_type(publicMeeting, bool, optional=True)
        check_type(reminderTime, int, optional=True)
        check_type(unlockedMeetingJoinSecurity, str, optional=True)
        check_type(sessionTypeId, str, optional=True)
        check_type(scheduledType, str, optional=True)
        check_type(enabledWebcastView, bool, optional=True)
        check_type(panelistPassword, str, optional=True)
        check_type(enableAutomaticLock, bool, optional=True)
        check_type(automaticLockMinutes, int, optional=True)
        check_type(allowFirstUserToBeCoHost, bool, optional=True)
        check_type(allowAuthenticatedDevices, bool, optional=True)
        check_type(invitees, list, optional=True)
        check_type(sendEmail, bool, optional=True)
        check_type(hostEmail, str, optional=True)
        check_type(siteUrl, str, optional=True)
        check_type(meetingOptions, dict, optional=True)
        check_type(registration, dict, optional=True)
        check_type(integrationTags, list, optional=True)
        check_type(simultaneousInterpretation, dict, optional=True)
        check_type(enabledBreakoutSessions, bool, optional=True)
        check_type(breakoutSessions, list, optional=True)

        post_data = dict_from_items_with_values(
            request_parameters,
            title=title,
            start=start,
            end=end,
            templateId=templateId,
            agenda=agenda,
            password=password,
            timezone=timezone,
            recurrence=recurrence,
            enabledAutoRecordMeeting=enabledAutoRecordMeeting,
            allowAnyUserToBeCoHost=allowAnyUserToBeCoHost,
            enabledJoinBeforeHost=enabledJoinBeforeHost,
            enableConnectAudioBeforeHost=enableConnectAudioBeforeHost,
            joinBeforeHostMinutes=joinBeforeHostMinutes,
            excludePassword=excludePassword,
            publicMeeting=publicMeeting,
            reminderTime=reminderTime,
            unlockedMeetingJoinSecurity=unlockedMeetingJoinSecurity,
            sessionTypeId=sessionTypeId,
            scheduledType=scheduledType,
            enabledWebcastView=enabledWebcastView,
            panelistPassword=panelistPassword,
            enableAutomaticLock=enableAutomaticLock,
            automaticLockMinutes=automaticLockMinutes,
            allowFirstUserToBeCoHost=allowFirstUserToBeCoHost,
            allowAuthenticatedDevices=allowAuthenticatedDevices,
            invitees=invitees,
            sendEmail=sendEmail,
            hostEmail=hostEmail,
            siteUrl=siteUrl,
            meetingOptions=meetingOptions,
            registration=registration,
            integrationTags=integrationTags,
            simultaneousInterpretation=simultaneousInterpretation,
            enabledBreakoutSessions=enabledBreakoutSessions,
            breakoutSessions=breakoutSessions,
        )

        request_url = API_ENDPOINT

        # API request
        json_data = self._session.post(request_url, json=post_data)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, meetingId):
        """Get details for a meeting, by ID.

        Args:
            meetingId(str): The meeting ID.

        Returns:
            Meeting: A Meeting object with the details of the requested
            meeting.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(meetingId, str)
        request_url = API_ENDPOINT

        # API request
        json_data = self._session.get(request_url + "/" + meetingId)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, meetingId):
        """Delete a meeting, by ID.

        Args:
            meetingId(str): The meeting ID.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(meetingId, str)
        request_url = API_ENDPOINT

        # API request
        self._session.delete(request_url + "/" + meetingId)

    def update(
        self,
        meetingId,
        title,
        password,
        start,
        end,
        agenda=None,
        timezone=None,
        recurrence=None,
        enabledAutoRecordMeeting=None,
        allowAnyUserToBeCoHost=None,
        enabledJoinBeforeHost=None,
        enableConnectAudioBeforeHost=None,
        joinBeforeHostMinutes=None,
        excludePassword=None,
        publicMeeting=None,
        reminderTime=None,
        unlockedMeetingJoinSecurity=None,
        sessionTypeId=None,
        scheduledType=None,
        enabledWebcastView=None,
        panelistPassword=None,
        enableAutomaticLock=None,
        automaticLockMinutes=None,
        allowFirstUserToBeCoHost=None,
        allowAuthenticatedDevices=None,
        sendEmail=None,
        hostEmail=None,
        siteUrl=None,
        meetingOptions=None,
        integrationTags=None,
        enabledBreakoutSessions=None,
        **request_parameters,
    ):
        """Update properties for a meeting, by ID.

        Args:
            meetingId(str): The meeting ID.
            title (str): Title of the meeting.
            password (str): Password of the meeting.
            start (str): Start time of the meeting in ISO 8601.
            end (str): End time of the meeting in ISO 8601.
            agenda (str): Meeting agenda (Maximum 1300 characters).
            timezone (str): Time zone of start and end property in IANA
                time zone database format.
            recurrence (str): Meeting recurrence according to RFC 2445.
            enabledAutoRecordMeeting (bool): Whether or not meeting is recorded
                automatically.
            allowAnyUserToBeCoHost (bool): Allow any attendee with host account
                on site to become cohost.
            enabledJoinBeforeHost (bool): Allow attendees to join before the
                host.
            enableConnectAudioBeforeHost (bool): Allow attendees to connect
                audio before the host joins.
            joinBeforeHostMinutes (int): Number of minutes attendees can join
                before the start time.
            excludePassword (bool): Exclude meeting password from meeting
                invite emails.
            publicMeeting (bool): Allow meeting to be listed on public
                calendar.
            reminderTime (int): Number of minutes before start time a reminder
                is send to the host.
            unlockedMeetingJoinSecurity (str): Join settings for
                uninvited people.
            sessionTypeId (str): Unique identifier for a meeting session
                type.
            scheduledType (str): Type of meeting (regular, webinar,
                meeting in personal room).
            enabledWebcastView (bool): Whether or not webcast view is enabled.
            panelistPassword (str): Password for panelists of a webinar
                meeting.
            enableAutomaticLock (bool): Whether or not to automatically lock
                the meeting after start.
            automaticLockMinutes (int): Number of minutes for the meeting to be
                automatically locked.
            allowFirstUserToBeCoHost (bool): Allow the first joiner with host
                account on the meeting site to be cohost.
            allowAuthenticatedDevices (bool): Whether or not to allow
                authenticated video devices in the meeting's organization to
                start or join the meeting.
            sendEmail (bool): Send an invite e-mail.
            hostEmail (str): Email address of the meeting host.
            siteUrl (str): Site URL for the meeting.
            meetingOptions (dict): Options for this meeting.
            integrationTags (list): List of external keys created by
                integrations.
            enabledBreakoutSessions (bool): Flag to enable breakout sessions in
                this meeting.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Meeting: A Meeting object with the updated Webex
            meeting details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(meetingId, str)
        check_type(title, str)
        check_type(password, str)
        check_type(start, str)
        check_type(end, str)
        check_type(agenda, str, optional=True)
        check_type(timezone, str, optional=True)
        check_type(recurrence, str, optional=True)
        check_type(enabledAutoRecordMeeting, bool, optional=True)
        check_type(allowAnyUserToBeCoHost, bool, optional=True)
        check_type(enabledJoinBeforeHost, bool, optional=True)
        check_type(enableConnectAudioBeforeHost, bool, optional=True)
        check_type(joinBeforeHostMinutes, int, optional=True)
        check_type(excludePassword, bool, optional=True)
        check_type(publicMeeting, bool, optional=True)
        check_type(reminderTime, int, optional=True)
        check_type(unlockedMeetingJoinSecurity, str, optional=True)
        check_type(sessionTypeId, str, optional=True)
        check_type(scheduledType, str, optional=True)
        check_type(enabledWebcastView, bool, optional=True)
        check_type(panelistPassword, str, optional=True)
        check_type(enableAutomaticLock, bool, optional=True)
        check_type(automaticLockMinutes, int, optional=True)
        check_type(allowFirstUserToBeCoHost, bool, optional=True)
        check_type(allowAuthenticatedDevices, bool, optional=True)
        check_type(sendEmail, bool, optional=True)
        check_type(hostEmail, str, optional=True)
        check_type(siteUrl, str, optional=True)
        check_type(meetingOptions, dict, optional=True)
        check_type(integrationTags, list, optional=True)
        check_type(enabledBreakoutSessions, bool, optional=True)

        put_data = dict_from_items_with_values(
            request_parameters,
            title=title,
            password=password,
            start=start,
            end=end,
            agenda=agenda,
            timezone=timezone,
            recurrence=recurrence,
            enabledAutoRecordMeeting=enabledAutoRecordMeeting,
            allowAnyUserToBeCoHost=allowAnyUserToBeCoHost,
            enabledJoinBeforeHost=enabledJoinBeforeHost,
            enableConnectAudioBeforeHost=enableConnectAudioBeforeHost,
            joinBeforeHostMinutes=joinBeforeHostMinutes,
            excludePassword=excludePassword,
            publicMeeting=publicMeeting,
            reminderTime=reminderTime,
            unlockedMeetingJoinSecurity=unlockedMeetingJoinSecurity,
            sessionTypeId=sessionTypeId,
            scheduledType=scheduledType,
            enabledWebcastView=enabledWebcastView,
            panelistPassword=panelistPassword,
            enableAutomaticLock=enableAutomaticLock,
            automaticLockMinutes=automaticLockMinutes,
            allowFirstUserToBeCoHost=allowFirstUserToBeCoHost,
            allowAuthenticatedDevices=allowAuthenticatedDevices,
            sendEmail=sendEmail,
            hostEmail=hostEmail,
            siteUrl=siteUrl,
            meetingOptions=meetingOptions,
            integrationTags=integrationTags,
            enabledBreakoutSessions=enabledBreakoutSessions,
        )

        request_url = API_ENDPOINT

        # API request
        json_data = self._session.put(
            request_url + "/" + meetingId, json=put_data
        )

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
