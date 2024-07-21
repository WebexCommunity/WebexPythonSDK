"""Webex Meetings data model.

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


class MeetingBasicPropertiesMixin(object):
    """Meeting basic properties."""

    @property
    def id(self):
        """Unique identifier for the meeting."""
        return self._json_data.get("id")

    @property
    def meetingNumber(self):
        """Meeting number (of series, scheduled meeting, or instance)."""
        return self._json_data.get("meetingNumber")

    @property
    def title(self):
        """Title of the meeting."""
        return self._json_data.get("title")

    @property
    def agenda(self):
        """Meeting agenda (Maximum 1300 characters)."""
        return self._json_data.get("agenda")

    @property
    def password(self):
        """Password of the meeting."""
        return self._json_data.get("password")

    @property
    def phoneAndVideoSystemPassword(self):
        """Eight (8) digit numeric password to join via phone/device."""
        return self._json_data.get("phoneAndVideoSystemPassword")

    @property
    def meetingType(self):
        """Type of meeting.

        Values: `meetingSeries`, `scheduledMeeting`, `meeting`
        """
        return self._json_data.get("meetingType")

    @property
    def state(self):
        """Meeting state.

        Values: `active`, `scheduled`, `ready`, `lobby`, `inProgress`, `ended`,
            `missed`, `expired`
        """
        return self._json_data.get("state")

    @property
    def timezone(self):
        """Time zone.

        Time zone of start and end property in IANA time zone database format.
        """
        return self._json_data.get("timezone")

    @property
    def start(self):
        """Start time of the meeting in ISO 8601."""
        return self._json_data.get("start")

    @property
    def end(self):
        """End time of the meeting in ISO 8601."""
        return self._json_data.get("end")

    @property
    def recurrence(self):
        """Meeting recurrence according to RFC 2445"""
        return self._json_data.get("recurrence")

    @property
    def hostUserId(self):
        """Unique id of the meeting host."""
        return self._json_data.get("hostUserId")

    @property
    def hostDisplayName(self):
        """Display name for the meeting host"""
        return self._json_data.get("hostDisplayName")

    @property
    def hostEmail(self):
        """Email address of the meeting host"""
        return self._json_data.get("hostEmail")

    @property
    def hostKey(self):
        """Key for joining the meeting as host"""
        return self._json_data.get("hostKey")

    @property
    def siteUrl(self):
        """Site URL for the meeting"""
        return self._json_data.get("siteUrl")

    @property
    def webLink(self):
        """Link to a meeting information page that launches the client"""
        return self._json_data.get("webLink")

    @property
    def registerLink(self):
        """Link to a page where attendees can register for the webinar.

        Only applies for webinars.
        """
        return self._json_data.get("registerLink")

    @property
    def sipAddress(self):
        """SIP address for callback from a video system"""
        return self._json_data.get("sipAddress")

    @property
    def dialInIpAddress(self):
        """IP address for callback from video system."""
        return self._json_data.get("dialInIpAddress")

    @property
    def roomId(self):
        """Room ID of the associated webex space. Only in space meetings."""
        return self._json_data.get("roomId")

    @property
    def enabledAutoRecordMeeting(self):
        """Whether or not meeting is recorded automatically."""
        return self._json_data.get("enabledAutoRecordMeeting")

    @property
    def allowAnyUserToBeCoHost(self):
        """Allow any attendee with host account on site to become cohost"""
        return self._json_data.get("allowAnyUserToBeCoHost")

    @property
    def enabledJoinBeforeHost(self):
        """Allow attendees to join before the host."""
        return self._json_data.get("enabledJoinBeforeHost")

    @property
    def enableConnectAudioBeforeHost(self):
        """Allow attendees to connect audio before the host joins."""
        return self._json_data.get("enableConnectAudioBeforeHost")

    @property
    def joinBeforeHostMinutes(self):
        """Number of minutes attendees can join before the start time."""
        return self._json_data.get("joinBeforeHostMinutes")

    @property
    def excludePassword(self):
        """Exclude meeting password from meeting invite emails."""
        return self._json_data.get("excludePassword")

    @property
    def publicMeeting(self):
        """Allow meeting to be listed on public calendar"""
        return self._json_data.get("publicMeeting")

    @property
    def reminderTime(self):
        """Number of minutes before start time to send reminder to the host."""
        return self._json_data.get("reminderTime")

    @property
    def unlockedMeetingJoinSecurity(self):
        """Join settings for uninvited people."""
        return self._json_data.get("unlockedMeetingJoinSecurity")

    @property
    def sessionTypeId(self):
        """Unique identifier for a meeting session type."""
        return self._json_data.get("sessionTypeId")

    @property
    def scheduledType(self):
        """Type of meeting (regular, webinar, meeting in personal room)."""
        return self._json_data.get("scheduledType")

    @property
    def enabledWebcastView(self):
        """Whether or not webcast view is enabled."""
        return self._json_data.get("enabledWebcastView")

    @property
    def panelistPassword(self):
        """Password for panelists of a webinar meeting."""
        return self._json_data.get("panelistPassword")

    @property
    def phoneAndVideoSystemPanelistPassword(self):
        """Eight (8) digit numeric panelist password for phone/device usage."""
        return self._json_data.get("phoneAndVideoSystemPanelistPassword")

    @property
    def enableAutomaticLock(self):
        """Whether or not to automatically lock the meeting after start."""
        return self._json_data.get("enableAutomaticLock")

    @property
    def automaticLockMinutes(self):
        """Number of minutes for the meeting to be automatically locked."""
        return self._json_data.get("automaticLockMinutes")

    @property
    def allowFirstUserToBeCoHost(self):
        """Allow first organization member to join to cohost the meeting.

        Allow the first joiner with host account on the meeting site to be
        cohost.
        """
        return self._json_data.get("allowFirstUserToBeCoHost")

    @property
    def allowAuthenticatedDevices(self):
        """Allow authenticated video devices to start or join the meeting.

        Whether or not to allow authenticated video devices in the meeting's
        organization to start or join the meeting.
        """
        return self._json_data.get("allowAuthenticatedDevices")

    @property
    def telephony(self):
        """Telephony information used to join the meeting from a phone.

        Information for callbacks from a meeting to phone or for joining via
        phone.
        """
        return self._json_data.get("telephony")

    @property
    def meetingOptions(self):
        """Options for this meeting."""
        return self._json_data.get("meetingOptions")

    @property
    def registration(self):
        """Meeting registration information."""
        return self._json_data.get("registration")

    @property
    def integrationTags(self):
        """List of external keys created by integrations."""
        return self._json_data.get("integrationTags")

    @property
    def simultaneousInterpretation(self):
        """Simultaneous interpretation information for the meeting."""
        return self._json_data.get("simultaneousInterpretation")
