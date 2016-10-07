# -*- coding: utf-8 -*-
"""RestSession class for creating 'connections' to the Cisco Spark APIs."""


from future import standard_library
standard_library.install_aliases()
from builtins import object
from six import string_types

import urllib.parse

import requests

from .exceptions import ciscosparkapiException
from .helper import ERC, validate_base_url, \
    raise_if_extra_kwargs, check_response_code, extract_and_parse_json


def _fix_next_url(next_url):
    """Remove max=null parameter from URL.

    Patch for Cisco Spark Defect: 'next' URL returned in the Link headers of
    the responses contain an errant 'max=null' parameter, which  causes the
    next request (to this URL) to fail if the URL is requested as-is.

    This patch parses the next_url to remove the max=null parameter.

    Args:
        next_url(string_types): The 'next' URL to be parsed and cleaned.

    Returns:
        str: The clean URL to be used for the 'next' request.

    Raises:
        AssertionError: If the parameter types are incorrect.
        ciscosparkapiException: If 'next_url' does not contain a valid API
            endpoint URL (scheme, netloc and path).

    """
    assert isinstance(next_url, string_types)
    next_url = str(next_url)
    parsed_url = urllib.parse.urlparse(next_url)
    if not parsed_url.scheme or not parsed_url.netloc or not parsed_url.path:
        error_message = "'next_url' must be a valid API endpoint URL, " \
                        "minimally containing a scheme, netloc and path."
        raise ciscosparkapiException(error_message)
    if parsed_url.query:
        query_list = parsed_url.query.split('&')
        if 'max=null' in query_list:
            query_list.remove('max=null')
        new_query = '&'.join(query_list)
        parsed_url = list(parsed_url)
        parsed_url[4] = new_query
    return urllib.parse.urlunparse(parsed_url)


class RestSession(object):
    def __init__(self, access_token, base_url, timeout=None):
        super(RestSession, self).__init__()
        self._base_url = str(validate_base_url(base_url))
        self._access_token = access_token
        self._req_session = requests.session()
        self._timeout = None
        self.update_headers({'Authorization': 'Bearer ' + access_token,
                             'Content-type': 'application/json;charset=utf-8'})
        self.timeout = timeout

    @property
    def base_url(self):
        return self._base_url

    @property
    def access_token(self):
        return self._access_token

    @property
    def headers(self):
        return self._req_session.headers.copy()

    def update_headers(self, headers):
        assert isinstance(headers, dict)
        self._req_session.headers.update(headers)

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        assert value is None or value > 0
        self._timeout = value

    def urljoin(self, suffix_url):
        return urllib.parse.urljoin(str(self.base_url), str(suffix_url))

    def get(self, url, params=None, **kwargs):
        # Process args
        assert isinstance(url, string_types)
        assert params is None or isinstance(params, dict)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['GET'])
        raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.get(abs_url, params=params,
                                         timeout=timeout)
        # Process response
        check_response_code(response, erc)
        return extract_and_parse_json(response)

    def get_pages(self, url, params=None, **kwargs):
        # Process args
        assert isinstance(url, string_types)
        assert params is None or isinstance(params, dict)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['GET'])
        raise_if_extra_kwargs(kwargs)
        # API request - get first page
        response = self._req_session.get(abs_url, params=params,
                                         timeout=timeout)
        while True:
            # Process response - Yield page's JSON data
            check_response_code(response, erc)
            yield extract_and_parse_json(response)
            # Get next page
            if response.links.get('next'):
                next_url = response.links.get('next').get('url')
                # Patch for Cisco Spark 'max=null' in next URL bug.
                next_url = _fix_next_url(next_url)
                # API request - get next page
                response = self._req_session.get(next_url, timeout=timeout)
            else:
                raise StopIteration

    def get_items(self, url, params=None, **kwargs):
        # Get iterator for pages of JSON data
        pages = self.get_pages(url, params=params, **kwargs)
        # Process pages
        for json_page in pages:
            # Process each page of JSON data yielding the individual JSON
            # objects contained within the top level 'items' array
            assert isinstance(json_page, dict)
            items = json_page.get(u'items')
            if items is None:
                error_message = "'items' object not found in JSON data: " \
                                "{!r}".format(json_page)
                raise ciscosparkapiException(error_message)
            else:
                for item in items:
                    yield item

    def post(self, url, json=None, data=None, headers=None, **kwargs):
        # Process args
        assert isinstance(url, string_types)
        abs_url = self.urljoin(url)
        # Process listed kwargs
        request_args = {}
        assert json is None or isinstance(json, dict)
        assert headers is None or isinstance(headers, dict)
        if json and data:
            raise TypeError("You must provide either a json or data argument, "
                            "not both.")
        elif json:
            request_args['json'] = json
        elif data:
            request_args['data'] = data
        elif not json and not data:
            raise TypeError("You must provide either a json or data argument.")
        if headers:
            request_args['headers'] = headers
        # Process unlisted kwargs
        request_args['timeout'] = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['POST'])
        raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.post(abs_url, **request_args)
        # Process response
        check_response_code(response, erc)
        return extract_and_parse_json(response)

    def put(self, url, json, **kwargs):
        # Process args
        assert isinstance(url, string_types)
        assert isinstance(json, dict)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['PUT'])
        raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.put(abs_url, json=json, timeout=timeout)
        # Process response
        check_response_code(response, erc)
        return extract_and_parse_json(response)

    def delete(self, url, **kwargs):
        # Process args
        assert isinstance(url, string_types)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['DELETE'])
        raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.delete(abs_url, timeout=timeout)
        # Process response
        check_response_code(response, erc)
