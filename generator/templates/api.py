# -*- coding: utf-8 -*-
"""Webex {{ name }}s API wrapper.

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
)


API_ENDPOINT = "{{ endpoint }}"
OBJECT_TYPE = "{{ object_type }}"


class {{ name }}sAPI(object):
    """Webex {{ name }}s API.

    Wraps the Webex {{ name }}s API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new {{ name }}sAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex Teams service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super({{ name }}sAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory
    {% if "list" in methods %}
    @generator_container
    def list(self, {% for up in url_parameters -%}
                    {{ up['name'] }},
                   {% endfor -%}
                   {% for qp in query_parameters -%}
                    {{ qp['name'] }}{% if qp['optional'] %}=None{% endif %},
                   {% endfor -%}
            headers={},
             **request_parameters):

        """List {{ object_type }}s.

        Use query parameters to filter the response.

        This method supports Webex Teams's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all memberships returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Webex as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            {% for up in url_parameters -%}
            {{ up['name'] }} ({{ up['type']}}): {{ up['description']}}
            {% endfor -%}
            {% for qp in query_parameters -%}
            {{ qp['name'] }} ({{ qp['type']}}): {{ qp['description']}}
            {% endfor -%}
            headers(dict): Additional headers to be passed.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the {{ object_type }}s returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        {% for up in url_parameters -%}
        check_type({{ up['name'] }}, {{ up['type'] }})
        {% endfor -%}
        {% for qp in query_parameters -%}
        check_type({{ qp['name'] }}, {{ qp['type'] }}{% if qp['optional'] %}, optional=True{% endif %})
        {% endfor %}

        params = dict_from_items_with_values(
            request_parameters,
            {% for qp in query_parameters -%}
            {{ qp['name'] }}={{ qp['name'] }},
            {% endfor %}
        )
        {% for qp in query_parameters -%}
        {% if qp['requestName'] %}
        if {{ qp['name'] }}:
            params['{{qp['requestName']}}'] = params.pop("{{ qp['name'] }}")
        {% endif %}
        {%- endfor %}
        {%- if url_parameters %}
            {%- set ups = [] -%}
            {% for up in url_parameters|map(attribute='name') -%}
            {% set ups = ups.append( up+"="+up ) %}
            {%- endfor %}
        # Add URL parameters to the API endpoint
        request_url = API_ENDPOINT.format({{ ups|join(", ") }})
        {% else %}
        request_url = API_ENDPOINT
        {% endif %}
        # API request - get items

        # Update headers
        for k, v in headers.items():
            self._session.headers[k] = v
        items = self._session.get_items(request_url, params=params)

        # Remove headers
        for k, v in headers.items():
            del self._session.headers[k]

        # Yield membership objects created from the returned items JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)
    {% endif %}
    {% if "create" in methods %}
    def create(self, {% for up in url_parameters -%}
                      {{ up['name'] }},
                     {% endfor -%}
                     {% for cp in create_parameters -%}
                      {{ cp['name'] }}{% if cp['optional'] %}=None{% endif %},
                     {% endfor -%}

                    **request_parameters):
        """Create a {{ object_type }}.

        Args:
            {% for up in url_parameters -%}
            {{ up['name'] }} ({{ up['type']}}): {{ up['description']}}
            {% endfor -%}
            {% for cp in create_parameters -%}
            {{ cp['name'] }} ({{ cp['type'] }}): {{ cp['description'] }}
            {% endfor -%}
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            {{ name }}: A {{ name }} object with the details of the created
            {{ object_type }}.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        {% for up in url_parameters -%}
        check_type({{ up['name'] }}, {{ up['type'] }})
        {% endfor -%}
        {% for cp in create_parameters -%}
        check_type({{ cp['name'] }}, {{ cp['type'] }}{% if cp['optional'] %}, optional=True{% endif %})
        {% endfor %}
        post_data = dict_from_items_with_values(
            request_parameters,
            {% for cp in create_parameters -%}
            {{ cp['name'] }}={{ cp['name'] }},
            {% endfor %}
        )

        {% for cp in create_parameters -%}
        {% if cp['requestName'] %}
        if {{ cp['name'] }}:
            post_data['{{cp['requestName']}}'] = post_data.pop("{{ cp['name'] }}")
        {% endif %}
        {%- endfor %}
        {%- if url_parameters %}
            {%- set ups = [] -%}
            {% for up in url_parameters|map(attribute='name') -%}
            {% set ups = ups.append( up+"="+up ) %}
            {%- endfor %}
        # Add URL parameters to the API endpoint
        request_url = API_ENDPOINT.format({{ ups|join(", ") }})
        {% else %}
        request_url = API_ENDPOINT
        {% endif %}
        # API request
        json_data = self._session.post(request_url, json=post_data)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
    {% endif %}

    {% if "get" in methods %}
    def get(self, {% for up in url_parameters %}{{up['name']}}, {% endfor %}{{ object_type }}Id):
        """Get details for a {{ object_type }}, by ID.

        Args:
            {% for up in url_parameters -%}
            {{up['name']}} ({{ up['type']}}): {{ up['description']}}
            {% endfor -%}
            {{ object_type }}Id(basestring): The {{ object_type }} ID.

        Returns:
            {{ name }}: A {{ name }} object with the details of the requested
            {{ object_type }}.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        check_type({{ object_type }}Id, basestring)

        # Add URL parameters to the API endpoint
        request_url = API_ENDPOINT.format({{ ups|join(", ") }})
        {% else %}
        request_url = API_ENDPOINT
        {% endif %}
        # API request
        json_data = self._session.get(request_url + '/' + {{ object_type }}Id)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
    {% endif %}

    {% if "delete" in methods %}
    def delete(self, {% for up in url_parameters %}{{up['name']}}, {% endfor %}{{ object_type }}Id):
        """Delete a {{ object_type }}, by ID.

        Args:
            {% for up in url_parameters -%}
            {{up['name']}} ({{ up['type']}}): {{ up['description']}}
            {% endfor -%}
            {{ object_type }}Id(basestring): The {{ object_type }} ID.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
        {% for up in url_parameters -%}
        check_type({{ up['name'] }}, {{ up['type'] }})
        {% endfor -%}
        check_type({{ object_type }}Id, basestring)
        {%- if url_parameters %}
            {%- set ups = [] -%}
            {% for up in url_parameters|map(attribute='name') -%}
            {% set ups = ups.append( up+"="+up ) %}
            {%- endfor %}

        # Add URL parameters to the API endpoint
        request_url = API_ENDPOINT.format({{ ups|join(", ") }})
        {% else %}
        request_url = API_ENDPOINT
        {% endif %}
        # API request
        self._session.delete(request_url + '/' + {{ object_type }}Id)
    {% endif %}

    {% if "update" in methods %}
    def update(self, {{ object_type }}Id,
                     {% for up in update_parameters -%}
                     {{ up['name'] }}{% if up['optional'] %}=None{% endif %},
                     {% endfor -%}

                     **request_parameters):
        """Update properties for a {{ object_type }}, by ID.

        Args:
            {% for up in url_parameters -%}
            {{up['name']}} ({{ up['type']}}): {{ up['description']}}
            {% endfor -%}
            {{ object_type }}Id(basestring): The {{ object_type }} ID.
            {% for up in update_parameters -%}
            {{ up['name'] }} ({{ up['type']}}): {{ up['description']}}
            {% endfor -%}
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            {{ name }}: A {{ name }} object with the updated Webex
            {{ object_type }} details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type({{ object_type }}Id, basestring)
        {% for up in update_parameters -%}
        check_type({{ up['name'] }}, {{ up['type'] }}{% if up['optional'] %}, optional=True{% endif %})
        {% endfor %}
        put_data = dict_from_items_with_values(
            request_parameters,
            {% for up in update_parameters -%}
            {{ up['name'] }}={{ up['name'] }},
            {% endfor %}
        )
        {% for up in update_parameters -%}
        {% if up['requestName'] %}
        if {{ up['name'] }}:
            put_data['{{up['requestName']}}'] = put_data.pop("{{ up['name'] }}")
        {% endif %}
        {%- endfor %}
        {%- if url_parameters %}
            {%- set ups = [] -%}
            {% for up in url_parameters|map(attribute='name') -%}
            {% set ups = ups.append( up+"="+up ) %}
            {%- endfor %}
        # Add URL parameters to the API endpoint
        request_url = API_ENDPOINT.format({{ ups|join(", ") }})
        {% else %}
        request_url = API_ENDPOINT
        {% endif %}
        # API request
        json_data = self._session.put(request_url + '/' + {{ object_type }}Id,
                                      json=put_data)

        # Return a membership object created from the response JSON data
        return self._object_factory(OBJECT_TYPE, json_data)
    {% endif %}
    {% if additional_code %}
    {{ additional_code }}
    {% endif %}
