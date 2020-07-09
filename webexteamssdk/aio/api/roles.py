# -*- coding: utf-8 -*-
"""Webex Teams Roles API wrapper.

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
)


API_ENDPOINT = "roles"
OBJECT_TYPE = "role"


class AsyncRolesAPI:
    """Webex Teams Roles API.

    Wraps the Webex Teams Roles API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session: AsyncRestSession, object_factory):
        """Initialize a new RolesAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, AsyncRestSession)

        super().__init__()

        self._session = session
        self._object_factory = object_factory

    @async_generator_container
    async def list(self, **request_parameters):
        """List all roles.

        Args:
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the roles returned by the Webex Teams query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=request_parameters)

        # Yield role objects created from the returned JSON objects
        async for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    async def get(self, roleId):
        """Get the details of a Role, by ID.

        Args:
            roleId(str): The ID of the Role to be retrieved.

        Returns:
            Role: A Role object with the details of the requested Role.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(roleId, str)

        # API request
        json_data = await self._session.get(API_ENDPOINT + "/" + roleId)

        # Return a role object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)
