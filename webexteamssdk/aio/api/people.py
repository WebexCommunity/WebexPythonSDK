# -*- coding: utf-8 -*-
"""Webex Teams People API wrapper.

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

from webexteamssdk.generator_containers import generator_container
from webexteamssdk.aio.restsession import AsyncRestSession
from webexteamssdk.aio.utils import (
    check_type,
    dict_from_items_with_values,
)


API_ENDPOINT = "people"
OBJECT_TYPE = "person"


class AsyncPeopleAPI:
    """Webex Teams People API.

    Wraps the Webex Teams People API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session: AsyncRestSession, object_factory):
        """Initialize a new PeopleAPI object with the provided RestSession.

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

    @generator_container
    async def list(
        self,
        email=None,
        displayName=None,
        id=None,
        orgId=None,
        max=None,
        **request_parameters
    ):
        """List people

        This method supports Webex Teams's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all people returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            email(str): The e-mail address of the person to be found.
            displayName(str): The complete or beginning portion of
                the displayName to be searched.
            id(str): List people by ID. Accepts up to 85 person IDs
                separated by commas.
            orgId(str): The organization ID.
            max(int): Limit the maximum number of items returned from the Webex
                Teams service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the people returned by the Webex Teams query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(id, str, optional=True)
        check_type(email, str, optional=True)
        check_type(displayName, str, optional=True)
        check_type(orgId, str, optional=True)
        check_type(max, int, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            id=id,
            email=email,
            displayName=displayName,
            orgId=orgId,
            max=max,
        )

        # API request - get items
        items = await self._session.get_items(API_ENDPOINT, params=params)

        # Yield person objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    async def create(
        self,
        emails,
        displayName=None,
        firstName=None,
        lastName=None,
        avatar=None,
        orgId=None,
        roles=None,
        licenses=None,
        **request_parameters
    ):
        """Create a new user account for a given organization

        Only an admin can create a new user account.

        Args:
            emails(`list`): Email address(es) of the person (list of strings).
            displayName(str): Full name of the person.
            firstName(str): First name of the person.
            lastName(str): Last name of the person.
            avatar(str): URL to the person's avatar in PNG format.
            orgId(str): ID of the organization to which this
                person belongs.
            roles(`list`): Roles of the person (list of strings containing
                the role IDs to be assigned to the person).
            licenses(`list`): Licenses allocated to the person (list of
                strings - containing the license IDs to be allocated to the
                person).
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Person: A Person object with the details of the created person.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(emails, list)
        check_type(displayName, str, optional=True)
        check_type(firstName, str, optional=True)
        check_type(lastName, str, optional=True)
        check_type(avatar, str, optional=True)
        check_type(orgId, str, optional=True)
        check_type(roles, list, optional=True)
        check_type(licenses, list, optional=True)

        post_data = dict_from_items_with_values(
            request_parameters,
            emails=emails,
            displayName=displayName,
            firstName=firstName,
            lastName=lastName,
            avatar=avatar,
            orgId=orgId,
            roles=roles,
            licenses=licenses,
        )

        # API request
        json_data = await self._session.post(API_ENDPOINT, json=post_data)

        # Return a person object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)

    async def get(self, personId):
        """Get a person's details, by ID.

        Args:
            personId(str): The ID of the person to be retrieved.

        Returns:
            Person: A Person object with the details of the requested person.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(personId, str)

        # API request
        json_data = await self._session.get(API_ENDPOINT + "/" + personId)

        # Return a person object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)

    async def update(
        self,
        personId,
        emails=None,
        displayName=None,
        firstName=None,
        lastName=None,
        avatar=None,
        orgId=None,
        roles=None,
        licenses=None,
        **request_parameters
    ):
        """Update details for a person, by ID.

        Only an admin can update a person's details.

        Email addresses for a person cannot be changed via the Webex Teams API.

        Include all details for the person. This action expects all user
        details to be present in the request. A common approach is to first GET
        the person's details, make changes, then PUT both the changed and
        unchanged values.

        Args:
            personId(str): The person ID.
            emails(`list`): Email address(es) of the person (list of strings).
            displayName(str): Full name of the person.
            firstName(str): First name of the person.
            lastName(str): Last name of the person.
            avatar(str): URL to the person's avatar in PNG format.
            orgId(str): ID of the organization to which this
                person belongs.
            roles(`list`): Roles of the person (list of strings containing
                the role IDs to be assigned to the person).
            licenses(`list`): Licenses allocated to the person (list of
                strings - containing the license IDs to be allocated to the
                person).
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Person: A Person object with the updated details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(emails, list, optional=True)
        check_type(displayName, str, optional=True)
        check_type(firstName, str, optional=True)
        check_type(lastName, str, optional=True)
        check_type(avatar, str, optional=True)
        check_type(orgId, str, optional=True)
        check_type(roles, list, optional=True)
        check_type(licenses, list, optional=True)

        put_data = dict_from_items_with_values(
            request_parameters,
            emails=emails,
            displayName=displayName,
            firstName=firstName,
            lastName=lastName,
            avatar=avatar,
            orgId=orgId,
            roles=roles,
            licenses=licenses,
        )

        # API request
        json_data = await self._session.put(
            API_ENDPOINT + "/" + personId, json=put_data
        )

        # Return a person object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)

    async def delete(self, personId):
        """Remove a person from the system.

        Only an admin can remove a person.

        Args:
            personId(str): The ID of the person to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type(personId, str)

        # API request
        await self._session.delete(API_ENDPOINT + "/" + personId)

    async def me(self):
        """Get the details of the person accessing the API.

        Raises:
            ApiError: If the Webex Teams cloud returns an error.

        """
        # API request
        json_data = await self._session.get(API_ENDPOINT + "/me")

        # Return a person object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
