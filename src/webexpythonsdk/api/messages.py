"""Webex Messages API wrapper.

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

from requests_toolbelt import MultipartEncoder

from webexpythonsdk.models.cards import AdaptiveCard
from ..generator_containers import generator_container
from ..restsession import RestSession
from ..utils import (
    check_type,
    dict_from_items_with_values,
    is_local_file,
    is_web_url,
    make_attachment,
    open_local_file,
)


API_ENDPOINT = "messages"
OBJECT_TYPE = "message"


class MessagesAPI(object):
    """Webex Messages API.

    Wraps the Webex Messages API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new MessagesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)
        super(MessagesAPI, self).__init__()
        self._session = session
        self._object_factory = object_factory

    @generator_container
    def list(
        self,
        roomId,
        parentId=None,
        mentionedPeople=None,
        before=None,
        beforeMessage=None,
        max=50,
        **request_parameters,
    ):
        """Lists messages in a room.

        Each message will include content attachments if present.

        The list API sorts the messages in descending order by creation date.

        This method supports Webex's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all messages returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            roomId(str): List messages for a room, by ID.
            parentId(str): List messages with a parent, by ID.
            mentionedPeople(str): List messages where the caller is
                mentioned by specifying "me" or the caller `personId`.
            before(str): List messages sent before a date and time, in
                ISO8601 format.
            beforeMessage(str): List messages sent before a message,
                by ID.
            max(int): Limit the maximum number of items returned from the Webex
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the messages returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(roomId, str)
        check_type(parentId, str, optional=True)
        check_type(mentionedPeople, str, optional=True)
        check_type(before, str, optional=True)
        check_type(beforeMessage, str, optional=True)
        check_type(max, int, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
            parentId=parentId,
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

    @generator_container
    def list_direct(
        self,
        personId=None,
        personEmail=None,
        parentId=None,
        **request_parameters,
    ):
        """List all messages in a 1:1 (direct) room.

        Use the `personId` or `personEmail` query parameter to specify the
        room.

        The list API sorts the messages in descending order by creation date.

        This method supports Webex's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all messages returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            personId(str): List messages in a 1:1 room, by person ID.
            personEmail(str): List messages in a 1:1 room, by person
                email.
            parentId(str): List messages with a parent, by ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the messages returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(personId, str, optional=True)
        check_type(personEmail, str, optional=True)
        check_type(parentId, str, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            personId=personId,
            personEmail=personEmail,
            parentId=parentId,
        )

        # API request - get items
        items = self._session.get_items(
            API_ENDPOINT + "/direct",
            params=params,
        )

        # Yield message objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def create(
        self,
        roomId=None,
        parentId=None,
        toPersonId=None,
        toPersonEmail=None,
        text=None,
        markdown=None,
        files=None,
        attachments=None,
        **request_parameters,
    ):
        """Post a message to a room.

        The files parameter is a list, which accepts multiple values to allow
        for future expansion, but currently only one file may be included with
        the message.

        Args:
            roomId(str): The room ID.
            toPersonId(str): The ID of the recipient when sending a
                private 1:1 message.
            toPersonEmail(str): The email address of the recipient when
                sending a private 1:1 message.
            text(str): The message, in plain text. If `markdown` is
                specified this parameter may be optionally used to provide
                alternate text for UI clients that do not support rich text.
            markdown(str): The message, in markdown format.
            files(list): A list of public URL(s) or local path(s) to files to
                be posted into the room. Only one file is allowed per message.
            attachments(list): Content attachments to attach to the message.
                See the Cards Guide for more information.
            parentId(str): The parent message to reply to. This will
                start or reply to a thread.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Message: A Message object with the details of the created message.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.
            ValueError: If the files parameter is a list of length > 1, or if
                the string in the list (the only element in the list) does not
                contain a valid URL or path to a local file.

        """
        check_type(roomId, str, optional=True)
        check_type(toPersonId, str, optional=True)
        check_type(toPersonEmail, str, optional=True)
        check_type(text, str, optional=True)
        check_type(markdown, str, optional=True)
        check_type(files, list, optional=True)
        check_type(attachments, list, optional=True)
        check_type(parentId, str, optional=True)

        if files:
            if len(files) > 1:
                raise ValueError(
                    "The `files` parameter should be a list with "
                    "exactly one (1) item. The files parameter "
                    "is a list, which accepts multiple values to "
                    "allow for future expansion, but currently "
                    "only one file may be included with the "
                    "message."
                )
            check_type(files[0], str)
        else:
            files = None

        # Process and serialize attachments
        if attachments:
            for item, attachment in enumerate(attachments):
                check_type(attachment, (dict, AdaptiveCard))

                if isinstance(attachment, AdaptiveCard):
                    attachments[item] = make_attachment(attachment)

        post_data = dict_from_items_with_values(
            request_parameters,
            roomId=roomId,
            toPersonId=toPersonId,
            toPersonEmail=toPersonEmail,
            text=text,
            markdown=markdown,
            files=files,
            attachments=attachments,
            parentId=parentId,
        )

        # API request
        if not files or is_web_url(files[0]):
            # Standard JSON post
            json_data = self._session.post(API_ENDPOINT, json=post_data)

        elif is_local_file(files[0]):
            # Multipart MIME post
            try:
                post_data["files"] = open_local_file(files[0])
                multipart_data = MultipartEncoder(post_data)
                headers = {"Content-type": multipart_data.content_type}
                json_data = self._session.post(
                    API_ENDPOINT, headers=headers, data=multipart_data
                )
            finally:
                post_data["files"].file_object.close()

        else:
            raise ValueError(
                "The `files` parameter does not contain a vaild "
                "URL or path to a local file."
            )

        # Return a message object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, messageId):
        """Get the details of a message, by ID.

        Args:
            messageId(str): The ID of the message to be retrieved.

        Returns:
            Message: A Message object with the details of the requested
            message.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(messageId, str)

        # API request
        json_data = self._session.get(API_ENDPOINT + "/" + messageId)

        # Return a message object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, messageId):
        """Delete a message.

        Args:
            messageId(str): The ID of the message to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(messageId, str)

        # API request
        self._session.delete(API_ENDPOINT + "/" + messageId)

    def update(self, messageId=None, roomId=None, text=None, markdown=None):
        """Update (edit) a message.

        Args:
            messageId(str): The ID of the message to be edit.
            roomId(str): The room ID.
            text(str): The message, in plain text. If `markdown` is
                specified this parameter may be optionally used to provide
                alternate text for UI clients that do not support rich text.
            markdown(str): The message, in markdown format.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(messageId, str)
        check_type(roomId, str, optional=True)
        check_type(text, str, optional=True)
        check_type(markdown, str, optional=True)

        put_data = dict_from_items_with_values(
            roomId=roomId,
            text=text,
            markdown=markdown,
        )

        # API request
        json_data = self._session.put(
            API_ENDPOINT + "/" + messageId, json=put_data
        )

        # Return a message object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    # Add edit() as an alias to the update() method for backward compatibility
    edit = update

    def _is_direct_room(self, message):
        """Determine if a message is from a direct (1:1) room.

        Args:
            message: Message object with roomType property

        Returns:
            bool: True if the message is from a direct room, False otherwise
        """
        if hasattr(message, "roomType"):
            return message.roomType == "direct"
        return False

    def _is_group_room(self, message):
        """Determine if a message is from a group room (space).

        Args:
            message: Message object with roomType property

        Returns:
            bool: True if the message is from a group room, False otherwise
        """
        if hasattr(message, "roomType"):
            return message.roomType == "group"
        return False

    def get_thread_messages(self, message, max_scan=500):
        """Retrieve all messages in a thread, including the root message.

        This method provides a robust way to collect thread messages that works
        for both 1:1 conversations and spaces, handling the different permission
        models and API limitations.

        Args:
            message: The message object to get the thread for
            max_scan (int): Maximum number of messages to scan when searching for parent

        Returns:
            tuple: (thread_messages, root_message, error_message)
                - thread_messages: List of all messages in the thread (oldest to newest)
                - root_message: The root message of the thread (or None if not found)
                - error_message: Error description if any issues occurred
        """
        thread_messages = []
        root_message = None
        error_message = None

        parent_id = getattr(message, "parentId", None)
        room_id = getattr(message, "roomId", None)

        if not parent_id or not room_id:
            # Not a threaded message, return just this message
            return [message], None, None

        try:
            # Strategy 1: Try to get the parent message directly
            try:
                root_message = self.get(parent_id)
                thread_messages.append(root_message)
            except Exception:
                # Direct retrieval failed, try alternative strategies
                if self._is_direct_room(message):
                    # For direct rooms, try list_direct with parentId
                    try:
                        direct_messages = list(
                            self.list_direct(
                                personId=getattr(message, "toPersonId", None),
                                personEmail=getattr(
                                    message, "toPersonEmail", None
                                ),
                                parentId=parent_id,
                                max=100,
                            )
                        )
                        if direct_messages:
                            root_message = direct_messages[0]
                            thread_messages.extend(direct_messages)
                    except Exception:
                        pass
                else:
                    # For group rooms, try scanning recent messages
                    try:
                        scanned = 0
                        for msg in self.list(roomId=room_id, max=100):
                            scanned += 1
                            if getattr(msg, "id", None) == parent_id:
                                root_message = msg
                                thread_messages.append(msg)
                                break
                            if scanned >= max_scan:
                                break
                    except Exception:
                        pass

                if not root_message:
                    error_message = f"Could not retrieve parent message {parent_id}. Bot may have joined after thread started or lacks permission."

            # Strategy 2: Get all replies in the thread
            try:
                if self._is_direct_room(message):
                    # For direct rooms, use list_direct
                    replies = list(
                        self.list_direct(
                            personId=getattr(message, "toPersonId", None),
                            personEmail=getattr(
                                message, "toPersonEmail", None
                            ),
                            parentId=parent_id,
                            max=100,
                        )
                    )
                else:
                    # For group rooms, use list
                    replies = list(
                        self.list(roomId=room_id, parentId=parent_id, max=100)
                    )

                # Add replies to thread messages, avoiding duplicates
                existing_ids = {
                    getattr(m, "id", None) for m in thread_messages
                }
                for reply in replies:
                    reply_id = getattr(reply, "id", None)
                    if reply_id and reply_id not in existing_ids:
                        thread_messages.append(reply)
                        existing_ids.add(reply_id)

            except Exception as e:
                if not error_message:
                    error_message = (
                        f"Could not retrieve thread replies: {str(e)}"
                    )

            # Strategy 3: Ensure the original message is included
            original_id = getattr(message, "id", None)
            if original_id and not any(
                getattr(m, "id", None) == original_id for m in thread_messages
            ):
                thread_messages.append(message)

            # Sort messages by creation time (oldest to newest)
            thread_messages.sort(key=lambda m: getattr(m, "created", ""))

        except Exception as e:
            error_message = f"Unexpected error retrieving thread: {str(e)}"

        return thread_messages, root_message, error_message

    def get_thread_context(self, message, max_scan=500):
        """Get thread context including root message and all replies.

        This is a convenience method that returns a structured result with
        thread information, making it easy to work with thread data.

        Args:
            message: The message object to get thread context for
            max_scan (int): Maximum number of messages to scan when searching for parent

        Returns:
            dict: Dictionary containing:
                - "thread_messages": List of all messages in thread (oldest to newest)
                - "root_message": The root message of the thread
                - "reply_count": Number of replies in the thread
                - "is_thread": Boolean indicating if this is a threaded conversation
                - "error": Error message if any issues occurred
                - "room_type": Type of room (direct/group)
        """
        thread_messages, root_message, error = self.get_thread_messages(
            message, max_scan
        )

        return {
            "thread_messages": thread_messages,
            "root_message": root_message,
            "reply_count": len(thread_messages) - 1 if root_message else 0,
            "is_thread": getattr(message, "parentId", None) is not None,
            "error": error,
            "room_type": getattr(message, "roomType", "unknown"),
        }
