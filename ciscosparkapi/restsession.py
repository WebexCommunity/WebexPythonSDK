"""RestSession class for creating 'connections' to the Cisco Spark APIs."""


import urlparse
import requests
import exceptions


# Default api.ciscospark.com base URL
DEFAULT_API_URL = 'https://api.ciscospark.com/v1/'

# Cisco Spark cloud Expected Response Codes (HTTP Response Codes)
ERC = {'GET': 200,
       'POST': 200,
       'PUT': 200,
       'DELETE': 204}


def _validate_base_url(base_url):
    parsed_url = urlparse.urlparse(base_url)
    if parsed_url.scheme and parsed_url.netloc:
        return parsed_url.geturl()
    else:
        error_message = "base_url must contain a valid scheme (protocol " \
                        "specifier) and network location (hostname)"
        raise exceptions.CiscoSparkApiException(error_message)


def _raise_if_extra_kwargs(kwargs):
    if kwargs:
        raise TypeError("Unexpected **kwargs: %r" % kwargs)


def _check_response_code(response, erc):
    if response.status_code != erc:
        raise exceptions.CiscoSparkApiError(response.status_code,
                                            request=response.request,
                                            response=response)


def _extract_and_parse_json(response):
    return response.json()


class RestSession(object):
    def __init__(self, access_token, base_url=DEFAULT_API_URL, timeout=None):
        super(RestSession, self).__init__()
        self._base_url = _validate_base_url(base_url)
        self._access_token = access_token
        self._req_session = requests.session()
        self._timeout = None
        self.update_headers({'Authorization': 'Bearer ' + access_token})
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
        _raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.get(abs_url,
                                         params=params,
                                         timeout=timeout)
        # Process response
        _check_response_code(response, erc)
        return _extract_and_parse_json(response)

    def get_pages(self, url, params=None, **kwargs):
        # Process args
        assert isinstance(url, basestring)
        assert params is None or isinstance(params, dict)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['GET'])
        _raise_if_extra_kwargs(kwargs)
        # API request - get first page
        response = self._req_session.get(abs_url,
                                         params=params,
                                         timeout=timeout)
        while True:
            # Process response - Yield page's JSON data
            _check_response_code(response, erc)
            yield _extract_and_parse_json(response)
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
                raise exceptions.CiscoSparkApiException(error_message)

    def post(self, url, json_dict, **kwargs):
        # Process args
        assert isinstance(url, basestring)
        assert isinstance(json_dict, dict)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['POST'])
        _raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.post(abs_url,
                                          json=json_dict,
                                          timeout=timeout)
        # Process response
        _check_response_code(response, erc)
        return _extract_and_parse_json(response)

    def put(self, url, json_dict, **kwargs):
        # Process args
        assert isinstance(url, basestring)
        assert isinstance(json_dict, dict)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['PUT'])
        _raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.put(abs_url,
                                         json=json_dict,
                                         timeout=timeout)
        # Process response
        _check_response_code(response, erc)
        return _extract_and_parse_json(response)

    def delete(self, url, **kwargs):
        # Process args
        assert isinstance(url, basestring)
        abs_url = self.urljoin(url)
        # Process kwargs
        timeout = kwargs.pop('timeout', self.timeout)
        erc = kwargs.pop('erc', ERC['DELETE'])
        _raise_if_extra_kwargs(kwargs)
        # API request
        response = self._req_session.delete(abs_url, timeout=timeout)
        # Process response
        _check_response_code(response, erc)
