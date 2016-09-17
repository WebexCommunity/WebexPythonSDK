"""Cisco Spark Messages-API wrapper classes.

Classes:
    Message: Models a Spark 'message' JSON object as a native Python object.
    MessagesAPI: Wrappers the Cisco Spark Messages-API and exposes the API
        calls as Python method calls that return native Python objects.

"""


from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.helper import utf8, generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData


class Message(SparkData):
    """Model a Spark 'message' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Message data object from a JSON dictionary or string.

        Args:
            json(dict, unicode, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Message, self).__init__(json)

    @property
    def id(self):
        return self._json[u'id']

    @property
    def roomId(self):
        return self._json[u'roomId']

    @property
    def roomType(self):
        return self._json[u'roomType']

    @property
    def toPersonId(self):
        """Optional attribute; returns None if not present."""
        return self._json.get(u'toPersonId')

    @property
    def toPersonEmail(self):
        """Optional attribute; returns None if not present."""
        return self._json.get(u'toPersonEmail')

    @property
    def text(self):
        """Optional attribute; returns None if not present."""
        return self._json.get(u'text')

    @property
    def markdown(self):
        """Optional attribute; returns None if not present."""
        return self._json.get(u'markdown')


    @property
    def files(self):
        """Optional attribute; returns None if not present."""
        return self._json.get(u'files')


    @property
    def personId(self):
        return self._json[u'personId']


    @property
    def personEmail(self):
        return self._json[u'personEmail']


    @property
    def created(self):
        return self._json[u'created']

    @property
    def mentionedPeople(self):
        """Optional attribute; returns None if not present."""
        return self._json.get(u'mentionedPeople')


class MessagesAPI(object):
    """Cisco Spark Messages-API wrapper class.

    Wrappers the Cisco Spark Messages-API and exposes the API calls as Python
    method calls that return native Python objects.

    Attributes:
        session(RestSession): The RESTful session object to be used for API
            calls to the Cisco Spark service.

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
        self.session = session

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
            roomId(unicode, str): List messages for the room with roomId.
            mentionedPeople(unicode, str): List messages for a person, by
                personId or me.
            before(unicode, str): List messages sent before a date and time,
                in ISO8601 format
            beforeMessage(unicode, str): List messages sent before a message,
                by message ID
            max(int): Limit the maximum number of messages returned from the
                Spark service per request.

        Yields:
            Message: The the next message from the Cisco Spark query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(roomId, basestring)
        assert mentionedPeople is None or \
               isinstance(mentionedPeople, basestring)
        assert before is None or isinstance(before, basestring)
        assert beforeMessage is None or isinstance(beforeMessage, basestring)
        assert max is None or isinstance(max, int)
        params = {}
        params[u'roomId'] = utf8(roomId)
        if mentionedPeople:
            params[u'mentionedPeople'] = utf8(mentionedPeople)
        if before:
            params[u'before'] = utf8(before)
        if beforeMessage:
            params[u'beforeMessage'] = utf8(beforeMessage)
        if max:
            params[u'max'] = max
        # API request - get items
        items = self.session.get_items('messages', params=params)
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
            roomId(unicode, str): The room ID.
            toPersonId(unicode, str): The ID of the recipient when sending a
                private 1:1 message.
            toPersonEmail(unicode, str): The email address of the recipient
                when sending a private 1:1 message.
            text(unicode, str): The message, in plain text. If markdown is
                speficied this parameter may be optionally used to provide
                alternate text forUI clients that do not support rich text.
            markdown(unicode, str): The message, in markdown format.
            files(list): A list of URL references for the message attachments.

        Returns:
            Message: With the details of the created message.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If the required arguments are not
                specified.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert roomId is None or isinstance(roomId, basestring)
        assert toPersonId is None or isinstance(toPersonId, basestring)
        assert toPersonEmail is None or isinstance(toPersonEmail, basestring)
        assert text is None or isinstance(text, basestring)
        assert markdown is None or isinstance(markdown, basestring)
        assert files is None or isinstance(files, list)
        post_data = {}
        if roomId:
            post_data[u'roomId'] = utf8(roomId)
        elif toPersonId:
            post_data[u'toPersonId'] = utf8(toPersonId)
        elif toPersonEmail:
            post_data[u'toPersonEmail'] = utf8(toPersonEmail)
        else:
            error_message = "You must specify a roomId, toPersonId, or " \
                            "toPersonEmail to which you want to post a new " \
                            "message."
            raise ciscosparkapiException(error_message)
        if not text and not markdown and not files:
            error_message = "You must supply some message content (text, " \
                            "markdown, files) when posting a message."
            raise ciscosparkapiException(error_message)
        if text:
            post_data[u'text'] = utf8(text)
        if markdown:
            post_data[u'markdown'] = utf8(markdown)
        if files:
            files = map(utf8, files)
            post_data[u'files'] = files
        # API request
        json_obj = self.session.post('messages', json=post_data)
        # Return a Message object created from the response JSON data
        return Message(json_obj)

    def get(self, messageId):
        """Get the details of a message, by ID.

        Args:
            messageId(unicode, str): The messageId of the message.

        Returns:
            Message: With the details of the requested message.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(messageId, basestring)
        # API request
        json_obj = self.session.get('messages/'+messageId)
        # Return a Message object created from the response JSON data
        return Message(json_obj)

    def delete(self, messageId):
        """Delete a message.

        Args:
            messageId(unicode, str): The messageId of the message to be
                deleted.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(messageId, basestring)
        # API request
        self.session.delete('messages/'+messageId)
