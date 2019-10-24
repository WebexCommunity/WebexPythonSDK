# -*- coding: utf-8 -*-
"""Webex Teams Attachment Actions API wrapper.

Copyright (c) 2016-2019 Cisco and/or its affiliates.

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

from ..restsession import RestSession
from ..utils import (
    check_type,
    dict_from_items_with_values,
)


API_ENDPOINT = 'attachment/actions'
OBJECT_TYPE = 'attachment_action'


class AttachmentActionsAPI(object):
    """Webex Teams Attachment Actions API.

    Wraps the Webex Teams Attachment Actions API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new AttachmentActionsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession, may_be_none=False)

        super(AttachmentActionsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    def create(self, actionType=None, messageId=None, inputs=None, **request_parameters):
        """Create a new attachment action.

        Args:
            actionType(basestring): The type of action to perform.
            messageId(basestring): The ID of the message which contains the attachment.
            inputs(basestring): The attachment action's inputs.

        Returns:
            Message: A AttachmentAction object with the details of the created Attachment Action.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.
            ValueError: If the files parameter is a list of length > 1, or if
                the string in the list (the only element in the list) does not
                contain a valid URL or path to a local file.

        """
        check_type(actionType, basestring, may_be_none=False)
        check_type(messageId, basestring, may_be_none=False)
        check_type(inputs, dict, may_be_none=False)

        post_data = dict_from_items_with_values(
            request_parameters,
            type=actionType,
            messageId=messageId,
            inputs=inputs,
        )

        json_data = self._session.post(API_ENDPOINT, json=post_data)

        # Return a AttachmentAction object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    def get(self, actionId):
        """Get Attachment Action Details

        Args:
            actionId(basestring): The ID of the Attachment Action to be retrieved.

        Returns:
            Action: A Attachment Action object with the details of the requested Attachment Action.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(actionId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get(API_ENDPOINT + '/' + actionId)

        # Return a Attachment Action object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
