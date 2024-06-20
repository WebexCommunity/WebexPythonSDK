"""Webex Recordings API wrapper.

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

from webexpythonsdk.generator_containers import generator_container

from webexpythonsdk.utils import check_type, dict_from_items_with_values

from webexpythonsdk.restsession import RestSession

API_ENDPOINT = "recordings"
OBJECT_TYPE = "recording"


class RecordingsAPI(object):
    """Webex Recordings API.

    Wraps the Webex Recordings API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new RecordingsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)
        super(RecordingsAPI, self).__init__()
        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(
        self,
        max=None,
        _from=None,
        to=None,
        meetingId=None,
        hostEmail=None,
        siteUrl=None,
        integrationTag=None,
        topic=None,
        format=None,
        serviceType=None,
        **request_parameters,
    ):
        """Lists recordings.

        You can specify a date range, a parent meeting ID and the maximum
        number of recordings to return.

        Only recordings of meetings hosted by or shared with the authenticated
        user will be listed. The list returned is sorted in descending order by
        the date and time that the recordings were created.

        This method supports Webex's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all recordings returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            max(int): Limit the maximum number of items returned from the Webex
                service per request.
            _from(str): List recordings which occurred after a specific
                date and time.
            to(str): List recordings which occurred before a specific
                date and time.
            meetingId(str): List recordings filtered by ID.
            hostEmail(str): Email address of meeting host.
            siteUrl(str): URL of the Webex site which the API lists
                recordings from.
            integrationTag(str): External key of the parent meeting
                created by an integration application.
            topic(str): Recording's topic (case-insensitive).
            format(str): Recording's format; if specified, it should be
                either "MP4" or "ARF".
            serviceType(str): Recording's service type; if specified, it
                should be either of:
                    MeetingCenter,
                    EventCenter,
                    SupportCenter,
                    TrainingCenter
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the recordings returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.
        """
        check_type(max, int, optional=True)
        check_type(_from, str, optional=True)
        check_type(to, str, optional=True)
        check_type(meetingId, str, optional=True)
        check_type(hostEmail, str, optional=True)
        check_type(siteUrl, str, optional=True)
        check_type(integrationTag, str)
        check_type(topic, str, optional=True)
        check_type(format, str, optional=True)
        check_type(serviceType, str, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            max_recordings=max,
            _from=_from,
            to=to,
            meetingId=meetingId,
            hostEmail=hostEmail,
            siteUrl=siteUrl,
            integrationTag=integrationTag,
            topic=topic,
            format=format,
            serviceType=serviceType,
        )

        items = self._session.get_items(API_ENDPOINT, params=params)

        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def get(self, recordingId, siteUrl=None, hostEmail=None):
        """Get the details of a recording, by ID.

        Args:
            recordingId(str): The ID of the recording to be retrieved.
            siteUrl(str): URL of the Webex site which the API gets
                recordings from.
            hostEmail(str): Email address of meeting host.

        Returns:
            Recording: A Recording object with the details of the requested
            recording.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(recordingId, str)
        check_type(siteUrl, str, optional=True)
        check_type(hostEmail, str, optional=True)

        params = dict_from_items_with_values(
            siteUrl=siteUrl, hostEmail=hostEmail
        )

        json_data = self._session.get(
            API_ENDPOINT + "/" + recordingId, params=params
        )

        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, recordingId, siteUrl=None, hostEmail=None):
        """Delete a recording.

        Args:
            recordingId(str): The ID of the recording to be deleted.
            siteUrl(str): URL of the Webex site which the API deletes
                recording from.
            hostEmail(str): Email address of meeting host.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(recordingId, str)
        check_type(siteUrl, str, optional=True)
        check_type(hostEmail, str, optional=True)

        params = dict_from_items_with_values(
            siteUrl=siteUrl, hostEmail=hostEmail
        )

        self._session.get(API_ENDPOINT + "/" + recordingId, params=params)
