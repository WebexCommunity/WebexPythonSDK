# -*- coding: utf-8 -*-
"""Webex Teams Guest Issuer API wrapper.

Copyright (c) 2016-2020 Cisco and/or its affiliates.

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
    check_response_code
)
from ..response_codes import EXPECTED_RESPONSE_CODE


import jwt
import base64
import requests

API_ENDPOINT = "jwt"
OBJECT_TYPE = "guest_issuer_token"


class GuestIssuerAPI(object):
    """Webex Teams Guest Issuer API.

    Wraps the Webex Teams Guest Issuer API and exposes the API as native
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Initialize a new GuestIssuerAPI object with the provided RestSession

        Args:
            session(RestSession): The RESTful session object to be used for
            API calls to the Webex Teams service

        Raises:
            TypeError: If the parameter types are incorrect
        """
        check_type(session, RestSession)

        super(GuestIssuerAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    def create(self, sub, name, iss, exp, secret):
        """Create a new guest issuer using the provided issuer token.

        This function returns a guest issuer with an api access token.

        Args:
            sub(basestring): The subject of the token. This is your unique
                and public identifier for the guest user. This claim may
                contain only letters, numbers, and hyphens.
            name(basestring): The display name of the guest user. This will be
                the name shown in Webex Teams clients.
            iss(basestring): The issuer of the token. Use the Guest
                Issuer ID provided in My Webex Teams Apps.
            exp(basestring): The exp time of the token, as a UNIX
                timestamp in seconds. Use the lowest practical value for the
                use of the token. This is not the exp time for the guest
                user's session.
            secret(basestring): Use the secret Webex provided you when you
                created your Guest Issuer App. The secret will be used to sign
                the token request.

        Returns:
            GuestIssuerToken: A Guest Issuer token with a valid access token.

        Raises:
            TypeError: If the parameter types are incorrect
            ApiError: If the webex teams cloud returns an error.
        """
        check_type(sub, basestring)
        check_type(name, basestring)
        check_type(iss, basestring)
        check_type(exp, basestring)
        check_type(secret, basestring)

        payload = {
            "sub": sub,
            "name": name,
            "iss": iss,
            "exp": exp
        }

        key = base64.b64decode(secret)
        jwt_token = jwt.encode(payload, key, algorithm="HS256")

        headers = {
            "Authorization": "Bearer " + jwt_token.decode("utf-8")
        }

        json_data = self._session.post(
            API_ENDPOINT + "/" + "login",
            headers=headers
        )

        return self._object_factory(OBJECT_TYPE, json_data)
