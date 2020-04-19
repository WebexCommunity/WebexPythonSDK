# -*- coding: utf-8 -*-
"""Webex Teams Guest Issuer API wrapper.

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

from webexteamssdk.aio.generator_containers import async_generator_container

from webexteamssdk.aio.restsession import AsyncRestSession
from webexteamssdk.aio.utils import (
    check_type,
    dict_from_items_with_values,
    async_check_response_code,
)
from webexteamssdk.response_codes import EXPECTED_RESPONSE_CODE


import jwt
import base64
import requests

API_ENDPOINT = "jwt"
OBJECT_TYPE = "guest_issuer_token"


class AsyncGuestIssuerAPI:
    """Webex Teams Guest Issuer API.

    Wraps the Webex Teams Guest Issuer API and exposes the API as native
    methods that return native Python objects.

    """

    def __init__(self, session: AsyncRestSession, object_factory):
        """Initialize a new GuestIssuerAPI object with the provided RestSession

        Args:
            session(RestSession): The RESTful session object to be used for
            API calls to the Webex Teams service

        Raises:
            TypeError: If the parameter types are incorrect
        """
        check_type(session, AsyncRestSession)

        super().__init__()

        self._session = session
        self._object_factory = object_factory

    async def create(self, subject, displayName, issuerToken, expiration, secret):
        """Create a new guest issuer using the provided issuer token.

        This function returns a guest issuer with an api access token.

        Args:
            subject(str): Unique and public identifier
            displayName(str): Display Name of the guest user
            issuerToken(str): Issuer token from developer hub
            expiration(str): Expiration time as a unix timestamp
            secret(str): The secret used to sign your guest issuers

        Returns:
            GuestIssuerToken: A Guest Issuer with a valid access token.

        Raises:
            TypeError: If the parameter types are incorrect
            ApiError: If the webex teams cloud returns an error.
        """
        check_type(subject, str, optional=True)
        check_type(displayName, str, optional=True)
        check_type(issuerToken, str, optional=True)
        check_type(expiration, str, optional=True)
        check_type(secret, str, optional=True)

        payload = {
            "sub": subject,
            "name": displayName,
            "iss": issuerToken,
            "exp": expiration,
        }

        key = base64.b64decode(secret)
        jwt_token = jwt.encode(payload, key, algorithm="HS256")

        url = self._session.base_url + API_ENDPOINT + "/" + "login"
        headers = {"Authorization": "Bearer " + jwt_token.decode("utf-8")}
        response = requests.post(url, headers=headers)
        async_check_response_code(response, EXPECTED_RESPONSE_CODE["GET"])

        return self._object_factory(OBJECT_TYPE, response.json())
