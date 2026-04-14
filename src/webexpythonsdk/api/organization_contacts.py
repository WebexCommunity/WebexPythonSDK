"""Webex Organization Contacts API wrapper.

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

from ..generator_containers import generator_container
from ..exceptions import MalformedResponse
from ..restsession import RestSession
from ..utils import (
    check_type,
    dict_from_items_with_values,
    extract_and_parse_json,
)


API_ENDPOINT = "contacts/organizations"
OBJECT_TYPE = "organization_contact"
DEFAULT_CONTACT_TYPE = "CUSTOM"
DEFAULT_SCHEMAS = "urn:cisco:codev:identity:contact:core:1.0"
UPDATE_MUTABLE_FIELDS = {
    "emails",
    "phoneNumbers",
    "extension",
    "firstName",
    "lastName",
    "avatar",
    "department",
    "manager",
    "managerId",
    "title",
    "addresses",
    "customAttributes",
    "displayName",
}


class OrganizationContactsAPI(object):
    """Webex Organization Contacts API.

    Wraps the Webex Organization Contacts API and exposes the API as native
    Python methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new OrganizationContactsAPI object with RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(OrganizationContactsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    @staticmethod
    def _base_endpoint(orgId):
        """Build base endpoint for organization contacts."""
        return "{}/{}/contacts".format(API_ENDPOINT, orgId)

    @staticmethod
    def _yield_result_items(pages):
        """Yield contact items from paged responses."""
        # The organization contacts endpoints return "result" as top-level
        # list key. For empty results, the API may omit "result" and return
        # only metadata (for example: start/limit/total).
        for json_page in pages:
            assert isinstance(json_page, dict)
            items = json_page.get("result")
            if items is None:
                if json_page.get("total") == 0:
                    continue
                error_message = (
                    "'result' key not found in JSON data: {!r}".format(
                        json_page
                    )
                )
                raise MalformedResponse(error_message)

            for item in items:
                yield item

    def _search_pages(self, endpoint, params=None):
        """Yield pages for org contacts search endpoints.

        Organization Contacts pagination is driven by ``start``, ``limit``,
        and ``total`` fields in the response body, not by RFC5988 Link
        headers.
        """
        check_type(endpoint, str)
        check_type(params, dict, optional=True)

        params = (params or {}).copy()

        while True:
            json_page = self._session.get(endpoint, params=params)
            assert isinstance(json_page, dict)
            yield json_page

            total = json_page.get("total")
            start = json_page.get("start")
            limit = json_page.get("limit")

            if not all(isinstance(v, int) for v in [total, start, limit]):
                break
            if total <= 0 or limit <= 0:
                break

            next_start = start + limit
            if next_start >= total or next_start <= start:
                break

            params["start"] = next_start

    @generator_container
    def list(
        self,
        orgId,
        keyword=None,
        source=None,
        limit=None,
        groupIds=None,
        **request_parameters,
    ):
        """List all contacts for a given organization.

        Args:
            orgId(str): List contacts for this organization, by ID.
            keyword(str): List contacts with a keyword.
            source(str): List contacts with source.
            limit(int): Limit the maximum number of contacts in the response.
            groupIds(`list`): Filter contacts based on groups.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the contacts returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(orgId, str)
        check_type(keyword, str, optional=True)
        check_type(source, str, optional=True)
        check_type(limit, int, optional=True)
        check_type(groupIds, list, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            keyword=keyword,
            source=source,
            limit=limit,
        )
        if groupIds:
            params["groupIds"] = ",".join(groupIds)

        # API request - get pages from /search endpoint
        pages = self._search_pages(
            self._base_endpoint(orgId) + "/search",
            params=params,
        )

        for item in self._yield_result_items(pages):
            yield self._object_factory(OBJECT_TYPE, item)

    @generator_container
    def search(
        self,
        orgId,
        keyword=None,
        source=None,
        limit=None,
        groupIds=None,
        email=None,
        displayName=None,
        id=None,
        max=None,  # Backwards-compat alias for `limit`.
        **request_parameters,
    ):
        """Search contacts.

        For most users, either the ``email`` or ``displayName`` parameter is
        required. Admin users can omit these fields and list all contacts in
        their organization.

        This method uses ``start``/``limit``/``total`` response fields to
        provide pagination support.

        Args:
            orgId(str): List contacts for this organization, by ID.
            keyword(str): List contacts with a keyword.
            source(str): List contacts with source.
            limit(int): Limit the maximum number of contacts in the response.
            groupIds(`list`): Filter contacts based on groups.
            email(str): The e-mail address of the contact to be found.
            displayName(str): The complete or beginning portion of the
                displayName to be searched.
            id(str): List contacts by ID. Accepts up to 85 contact IDs
                separated by commas.
            max(int): Backwards-compat alias for `limit`.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields contacts returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(orgId, str)
        check_type(keyword, str, optional=True)
        check_type(source, str, optional=True)
        check_type(limit, int, optional=True)
        check_type(groupIds, list, optional=True)
        check_type(id, str, optional=True)
        check_type(email, str, optional=True)
        check_type(displayName, str, optional=True)
        check_type(max, int, optional=True)

        # Backwards compatibility with older People-like parameters.
        if keyword is None:
            keyword = email or displayName or id
        if limit is None:
            limit = max

        params = dict_from_items_with_values(
            request_parameters,
            keyword=keyword,
            source=source,
            limit=limit,
        )
        if groupIds:
            params["groupIds"] = ",".join(groupIds)

        # API request - get pages
        pages = self._search_pages(
            self._base_endpoint(orgId) + "/search", params=params
        )

        for item in self._yield_result_items(pages):
            yield self._object_factory(OBJECT_TYPE, item)

    def get(self, orgId, contactId):
        """Get a contact's details, by ID.

        Args:
            orgId(str): The organization ID.
            contactId(str): The ID of the contact to be retrieved.

        Returns:
            OrganizationContact: Contact details as an object.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(orgId, str)
        check_type(contactId, str)

        # API request
        json_data = self._session.get(
            self._base_endpoint(orgId) + "/" + contactId
        )

        # Return a contact object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)

    def create(
        self,
        orgId,
        emails,
        contactType=DEFAULT_CONTACT_TYPE,
        schemas=DEFAULT_SCHEMAS,
        phoneNumbers=None,
        extension=None,
        firstName=None,
        lastName=None,
        avatar=None,
        department=None,
        manager=None,
        managerId=None,
        title=None,
        addresses=None,
        customAttributes=None,
        displayName=None,
        **request_parameters,
    ):
        """Create a contact.

        Args:
            orgId(str): ID of the organization to which this contact belongs.
            emails(`list`): Email address(es) of the contact.
            contactType(str): Type of contact, e.g. ``CUSTOM`` or ``CLOUD``.
            schemas(str): Contact schema identifier.
            phoneNumbers(`list`): Phone numbers for the contact.
            extension(str): Calling extension for the contact.
            firstName(str): First name of the contact.
            lastName(str): Last name of the contact.
            avatar(str): URL to the contact avatar in PNG format.
            department(str): The business department the contact belongs to.
            manager(str): A manager identifier.
            managerId(str): Person ID of the manager.
            title(str): The contact's title.
            addresses(`list`): Contact addresses.
            customAttributes(`list`): Contact custom attributes.
            displayName(str): Full name of the contact.
            **request_parameters: Additional request parameters.

        Returns:
            OrganizationContact: The created organization contact.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(orgId, str)
        check_type(emails, list)
        check_type(contactType, str, optional=True)
        check_type(schemas, str, optional=True)
        check_type(phoneNumbers, list, optional=True)
        check_type(extension, str, optional=True)
        check_type(firstName, str, optional=True)
        check_type(lastName, str, optional=True)
        check_type(avatar, str, optional=True)
        check_type(department, str, optional=True)
        check_type(manager, str, optional=True)
        check_type(managerId, str, optional=True)
        check_type(title, str, optional=True)
        check_type(addresses, list, optional=True)
        check_type(customAttributes, list, optional=True)
        check_type(displayName, str, optional=True)

        post_data = dict_from_items_with_values(
            request_parameters,
            emails=emails,
            contactType=contactType or DEFAULT_CONTACT_TYPE,
            schemas=schemas or DEFAULT_SCHEMAS,
            phoneNumbers=phoneNumbers,
            extension=extension,
            firstName=firstName,
            lastName=lastName,
            avatar=avatar,
            department=department,
            manager=manager,
            managerId=managerId,
            title=title,
            addresses=addresses,
            customAttributes=customAttributes,
            displayName=displayName,
        )

        # API request
        json_data = self._session.post(
            self._base_endpoint(orgId), json=post_data, erc=201
        )

        # Return a contact object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)

    def update(
        self,
        orgId,
        contactId,
        emails=None,
        schemas=None,
        phoneNumbers=None,
        extension=None,
        firstName=None,
        lastName=None,
        avatar=None,
        department=None,
        manager=None,
        managerId=None,
        title=None,
        addresses=None,
        customAttributes=None,
        displayName=None,
        **request_parameters,
    ):
        """Update details for a contact.

        Args:
            orgId(str): ID of the organization to which this contact belongs.
            contactId(str): Unique ID for the contact.
            emails(`list`): Email address(es) of the contact.
            schemas(str): Contact schema identifier.
            phoneNumbers(`list`): Phone numbers for the contact.
            extension(str): Calling extension for the contact.
            firstName(str): First name of the contact.
            lastName(str): Last name of the contact.
            avatar(str): URL to the contact avatar in PNG format.
            department(str): The business department the contact belongs to.
            manager(str): A manager identifier.
            managerId(str): Person ID of the manager.
            title(str): The contact's title.
            addresses(`list`): Contact addresses.
            customAttributes(`list`): Contact custom attributes.
            displayName(str): Full name of the contact.
            **request_parameters: Additional request parameters.

        Returns:
            OrganizationContact: The updated organization contact.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(orgId, str)
        check_type(contactId, str)
        check_type(emails, list, optional=True)
        check_type(schemas, str, optional=True)
        check_type(phoneNumbers, list, optional=True)
        check_type(extension, str, optional=True)
        check_type(firstName, str, optional=True)
        check_type(lastName, str, optional=True)
        check_type(avatar, str, optional=True)
        check_type(department, str, optional=True)
        check_type(manager, str, optional=True)
        check_type(managerId, str, optional=True)
        check_type(title, str, optional=True)
        check_type(addresses, list, optional=True)
        check_type(customAttributes, list, optional=True)
        check_type(displayName, str, optional=True)

        # Filter out read-only/unsupported fields (for example: contactType,
        # schemas, created, lastModified) from user-provided kwargs.
        filtered_request_parameters = {
            key: value
            for key, value in request_parameters.items()
            if key in UPDATE_MUTABLE_FIELDS
        }

        if not schemas:
            schemas = DEFAULT_SCHEMAS

        put_data = dict_from_items_with_values(
            filtered_request_parameters,
            emails=emails,
            schemas=schemas,
            phoneNumbers=phoneNumbers,
            extension=extension,
            firstName=firstName,
            lastName=lastName,
            avatar=avatar,
            department=department,
            manager=manager,
            managerId=managerId,
            title=title,
            addresses=addresses,
            customAttributes=customAttributes,
            displayName=displayName,
        )

        print("PUT data: {}".format(put_data))

        # API request (PATCH)
        response = self._session.request(
            "PATCH",
            self._base_endpoint(orgId) + "/" + contactId,
            erc=200,
            json=put_data,
        )
        json_data = extract_and_parse_json(response)

        # Return a contact object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)

    def delete(self, orgId, contactId):
        """Delete a contact.

        Args:
            orgId(str): The organization ID.
            contactId(str): The ID of the contact to be deleted.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(orgId, str)
        check_type(contactId, str)

        # API request
        self._session.delete(self._base_endpoint(orgId) + "/" + contactId)
