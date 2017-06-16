# -*- coding: utf-8 -*-
"""Cisco Spark Messages-API wrapper classes.

Classes:
    Message: Models a Spark 'message' JSON object as a native Python object.
    MessagesAPI: Wrappers the Cisco Spark Messages-API and exposes the API
        calls as Python method calls that return native Python objects.

"""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *

from requests_toolbelt import MultipartEncoder

from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData
from ciscosparkapi.utils import (
    generator_container,
    is_web_url,
    is_local_file,
    open_local_file,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


class Message(SparkData):
    """Model a Spark 'message' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Message data object from a JSON dictionary or string.

        Args:
            json(dict, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Message, self).__init__(json)

    @property
    def id(self):
        return self._json['id']

    @property
    def roomId(self):
        return self._json['roomId']

    @property
    def roomType(self):
        return self._json['roomType']

    @property
    def toPersonId(self):
        """Optional attribute; returns None if not present."""
        return self._json.get('toPersonId')

    @property
    def toPersonEmail(self):
        """Optional attribute; returns None if not present."""
        return self._json.get('toPersonEmail')

    @property
    def text(self):
        """Optional attribute; returns None if not present."""
        return self._json.get('text')

    @property
    def markdown(self):
        """Optional attribute; returns None if not present."""
        return self._json.get('markdown')

    @property
    def files(self):
        """Optional attribute; returns None if not present."""
        return self._json.get('files')

    @property
    def personId(self):
        return self._json['personId']

    @property
    def personEmail(self):
        return self._json['personEmail']

    @property
    def created(self):
        return self._json['created']

    @property
    def mentionedPeople(self):
        """Optional attribute; returns None if not present."""
        return self._json.get('mentionedPeople')


class MessagesAPI(object):
    """Cisco Spark Messages-API wrapper class.

    Wrappers the Cisco Spark Messages-API and exposes the API calls as Python
    method calls that return native Python objects.

    """

    def __init__(self, session):
        """Init a new MessagesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(session, RestSession)
        super(MessagesAPI, self).__init__()
        self._session = session

    @generator_container
    def list(self, roomId, mentionedPeople=None, before=None,
             beforeMessage=None, max=None):
        """List all messages in a room.

        If present, includes the associated media content attachment for each
        message.  The list sorts the messages in descending order by creation
        date.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yield all messages returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            roomId(str): List messages for the room with roomId.
            mentionedPeople(str): List messages for a person, by
                personId or me.
            before(str): List messages sent before a date and time,
                in ISO8601 format
            beforeMessage(str): List messages sent before a message,
                by message ID
            max(int): Limit the maximum number of messages returned from the
                Spark service per request.

        Returns:
            GeneratorContainer: When iterated, the GeneratorContainer, yields
                the messages returned by the Cisco Spark query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(roomId, str)
        assert mentionedPeople is None or isinstance(mentionedPeople, list)
        assert before is None or isinstance(before, str)
        assert beforeMessage is None or isinstance(beforeMessage, str)
        assert max is None or isinstance(max, int)
        params = {}
        params['roomId'] = roomId
        if mentionedPeople:
            params['mentionedPeople'] = mentionedPeople
        if before:
            params['before'] = before
        if beforeMessage:
            params['beforeMessage'] = beforeMessage
        if max:
            params['max'] = max
        # API request - get items
        items = self._session.get_items('messages', params=params)
        # Yield Message objects created from the returned items JSON objects
        for item in items:
            yield Message(item)

    def create(self, roomId=None, toPersonId=None, toPersonEmail=None,
               text=None, markdown=None, files=None):
        """Posts a message to a room.

        Posts a message, and optionally, a media content attachment, to a room.

        You must specify either a roomId, toPersonId or toPersonEmail when
        posting a message, and you must supply some message content (text,
        markdown, files).

        Args:
            roomId(str): The room ID.
            toPersonId(str): The ID of the recipient when sending a
                private 1:1 message.
            toPersonEmail(str): The email address of the recipient
                when sending a private 1:1 message.
            text(str): The message, in plain text. If markdown is
                specified this parameter may be optionally used to provide
                alternate text forUI clients that do not support rich text.
            markdown(str): The message, in markdown format.
            files(list): A list containing local paths or URL references for
                the message attachment(s).  The files attribute currently only
                takes a list containing one (1) filename or URL as an input.
                This is a Spark API limitation that may be lifted at a later
                date.

        Returns:
            Message: With the details of the created message.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If the required arguments are not
                specified.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert roomId is None or isinstance(roomId, str)
        assert toPersonId is None or isinstance(toPersonId, str)
        assert toPersonEmail is None or isinstance(toPersonEmail, str)
        assert text is None or isinstance(text, str)
        assert markdown is None or isinstance(markdown, str)
        assert files is None or isinstance(files, list)
        post_data = {}
        # Where is message to be posted?
        if roomId:
            post_data['roomId'] = roomId
        elif toPersonId:
            post_data['toPersonId'] = toPersonId
        elif toPersonEmail:
            post_data['toPersonEmail'] = toPersonEmail
        else:
            error_message = "You must specify a roomId, toPersonId, or " \
                            "toPersonEmail to which you want to post a new " \
                            "message."
            raise ciscosparkapiException(error_message)
        # Ensure some message 'content' is provided.
        if not text and not markdown and not files:
            error_message = "You must supply some message content (text, " \
                            "markdown, files) when posting a message."
            raise ciscosparkapiException(error_message)
        # Process the content.
        if text:
            post_data['text'] = text
        if markdown:
            post_data['markdown'] = markdown
        upload_local_file = False
        if files:
            if len(files) > 1:
                error_message = "The files attribute currently only takes a " \
                                "list containing one (1) filename or URL as " \
                                "an input.  This is a Spark API limitation " \
                                "that may be lifted at a later date."
                raise ciscosparkapiException(error_message)
            if is_web_url(files[0]):
                post_data['files'] = files
            elif is_local_file(files[0]):
                upload_local_file = True
                post_data['files'] = open_local_file(files[0])
            else:
                error_message = "The provided files argument does not " \
                                "contain a valid URL or local file path."
                raise ciscosparkapiException(error_message)
        # API request
        if upload_local_file:
            try:
                multipart_data = MultipartEncoder(post_data)
                headers = {'Content-type': multipart_data.content_type}
                json_obj = self._session.post('messages',
                                              data=multipart_data,
                                              headers=headers)
            finally:
                post_data['files'].file_object.close()
        else:
            json_obj = self._session.post('messages', json=post_data)
        # Return a Message object created from the response JSON data
        return Message(json_obj)

    def get(self, messageId):
        """Get the details of a message, by ID.

        Args:
            messageId(str): The messageId of the message.

        Returns:
            Message: With the details of the requested message.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(messageId, str)
        # API request
        json_obj = self._session.get('messages/' + messageId)
        # Return a Message object created from the response JSON data
        return Message(json_obj)

    def delete(self, messageId):
        """Delete a message.

        Args:
            messageId(str): The messageId of the message to be
                deleted.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(messageId, str)
        # API request
        self._session.delete('messages/' + messageId)
