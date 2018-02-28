# -*- coding: utf-8 -*-
"""Cisco Spark Messages API."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from past.builtins import basestring
from requests_toolbelt import MultipartEncoder

from ..generator_containers import generator_container
from ..restsession import RestSession
from ..utils import (
    check_type, dict_from_items_with_values, is_local_file, is_web_url,
    open_local_file,
)


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


API_ENDPOINT = 'messages'
OBJECT_TYPE = 'message'


class MessagesAPI(object):
    """Cisco Spark Messages API.

    Wraps the Cisco Spark Messages API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new MessagesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession, may_be_none=False)
        super(MessagesAPI, self).__init__()
        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(self, roomId, mentionedPeople=None, before=None,
             beforeMessage=None, max=None, **request_parameters):
        """Lists messages in a room.

        Each message will include content attachments if present.

        The list API sorts the messages in descending order by creation date.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all messages returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            roomId(basestring): List messages for a room, by ID.
            mentionedPeople(basestring): List messages where the caller is
                mentioned by specifying "me" or the caller `personId`.
            before(basestring): List messages sent before a date and time, in
                ISO8601 format.
            beforeMessage(basestring): List messages sent before a message,
                by ID.
            max(int): Limit the maximum number of items returned from the Spark
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
                yields the messages returned by the Cisco Spark query.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(roomId, basestring, may_be_none=False)
        check_type(mentionedPeople, basestring)
        check_type(before, basestring)
        check_type(beforeMessage, basestring)
        check_type(max, int)

        params = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
            mentionedPeople=mentionedPeople,
            before=before,
            beforeMessage=beforeMessage,
            max=max,
        )

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield message objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def create(self, roomId=None, toPersonId=None, toPersonEmail=None,
               text=None, markdown=None, files=None, **request_parameters):
        """Post a message, and optionally a attachment, to a room.

        The files parameter is a list, which accepts multiple values to allow
        for future expansion, but currently only one file may be included with
        the message.

        Args:
            roomId(basestring): The room ID.
            toPersonId(basestring): The ID of the recipient when sending a
                private 1:1 message.
            toPersonEmail(basestring): The email address of the recipient when
                sending a private 1:1 message.
            text(basestring): The message, in plain text. If `markdown` is
                specified this parameter may be optionally used to provide
                alternate text for UI clients that do not support rich text.
            markdown(basestring): The message, in markdown format.
            files(list): A list of public URL(s) or local path(s) to files to
                be posted into the room. Only one file is allowed per message.
                Uploaded files are automatically converted into a format that
                all Spark clients can render.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Message: A Message object with the details of the created message.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.
            ValueError: If the files parameter is a list of length > 1, or if
                the string in the list (the only element in the list) does not
                contain a valid URL or path to a local file.

        """
        check_type(roomId, basestring)
        check_type(toPersonId, basestring)
        check_type(toPersonEmail, basestring)
        check_type(text, basestring)
        check_type(markdown, basestring)
        check_type(files, list)
        if files:
            if len(files) != 1:
                raise ValueError("The length of the `files` list is greater "
                                 "than one (1). The files parameter is a "
                                 "list, which accepts multiple values to "
                                 "allow for future expansion, but currently "
                                 "only one file may be included with the "
                                 "message.")
            check_type(files[0], basestring)

        post_data = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
            toPersonId=toPersonId,
            toPersonEmail=toPersonEmail,
            text=text,
            markdown=markdown,
            files=files,
        )

        # API request
        if not files or is_web_url(files[0]):
            # Standard JSON post
            json_data = self._session.post(API_ENDPOINT, json=post_data)

        elif is_local_file(files[0]):
            # Multipart MIME post
            try:
                post_data['files'] = open_local_file(files[0])
                multipart_data = MultipartEncoder(post_data)
                headers = {'Content-type': multipart_data.content_type}
                json_data = self._session.post(API_ENDPOINT,
                                               headers=headers,
                                               data=multipart_data)
            finally:
                post_data['files'].file_object.close()

        else:
            raise ValueError("The `files` parameter does not contain a vaild "
                             "URL or path to a local file.")

        # Return a message object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, messageId):
        """Get the details of a message, by ID.

        Args:
            messageId(basestring): The ID of the message to be retrieved.

        Returns:
            Message: A Message object with the details of the requested
                message.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(messageId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get(API_ENDPOINT + '/' + messageId)

        # Return a message object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, messageId):
        """Delete a message.

        Args:
            messageId(basestring): The ID of the message to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(messageId, basestring, may_be_none=False)

        # API request
        self._session.delete(API_ENDPOINT + '/' + messageId)
