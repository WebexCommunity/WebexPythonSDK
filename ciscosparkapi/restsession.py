"""RestSession class for creating 'connections' to the Cisco Spark APIs."""

import urlparse

import requests

from .exceptions import ciscosparkapiException
from .helper import ERC, validate_base_url, \
    raise_if_extra_kwargs, check_response_code, extract_and_parse_json


class RestSession(object):
    def __init__(self, access_token, base_url, timeout=None):
        super(RestSession, self).__init__()
        self._base_url = validate_base_url(base_url)
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
        return urlparse.urljoin(self.base_url, suffix_url)

    def get(self, url, params=None, **kwargs):
        # Process args
        assert isinstance(url, basestring)
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
        assert isinstance(url, basestring)
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
            if items:
                for item in items:
                    yield item
            else:
                error_message = "'items' object not found in JSON data: %r" \
                                % json_page
                raise ciscosparkapiException(error_message)

    def post(self, url, json, **kwargs):
        # Process args
        assert isinstance(url, basestring)
        assert isinstance(json, dict)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['POST'])
        raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.post(abs_url, json=json, timeout=timeout)
        # Process response
        check_response_code(response, erc)
        return extract_and_parse_json(response)

    def put(self, url, json, **kwargs):
        # Process args
        assert isinstance(url, basestring)
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
        assert isinstance(url, basestring)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['DELETE'])
        raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.delete(abs_url, timeout=timeout)
        # Process response
        check_response_code(response, erc)
