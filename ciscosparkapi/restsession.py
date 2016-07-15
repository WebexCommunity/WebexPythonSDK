"""RestSession class for creating 'connections' to the Cisco Spark APIs."""

import urlparse
import requests
import exception


GET_EXPECTED_RESPONSE_CODE = 200
POST_EXPECTED_RESPONSE_CODE = 200
PUT_EXPECTED_RESPONSE_CODE = 200
DELETE_EXPECTED_RESPONSE_CODE = 204


def _validate_base_url(base_url):
    parsed_url = urlparse.urlparse(base_url)
    if parsed_url.scheme and parsed_url.netloc:
        return parsed_url.geturl()
    else:
        error_message = "base_url must contain a valid scheme (protocol " \
                        "specifier) and network location (hostname)"
        raise exception.CiscoSparkApiException(error_message)


def _check_response(response, expected_response_code):
    if response.status_code != expected_response_code:
        raise exception.CiscoSparkApiError(response.status_code,
                                           request=response.request,
                                           response=response)


def _extract_and_parse_json(response):
    return response.json()


class RestSession(object):
    def __init__(self, base_url, access_token, timeout=None):
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

    def get(self, url, **kwargs):
        timeout = kwargs.pop('timeout', self.timeout)
        expected_response_code = kwargs.pop('expected_response_code',
                                            GET_EXPECTED_RESPONSE_CODE)
        if kwargs:
            raise TypeError(' Unexpected **kwargs: %r' % kwargs)
        # API request
        response = self._req_session.get(self.urljoin(url), timeout=timeout)
        # Process response
        _check_response(response, expected_response_code)
        return _extract_and_parse_json(response)

    def get_pages(self, url, **kwargs):
        timeout = kwargs.pop('timeout', self.timeout)
        expected_response_code = kwargs.pop('expected_response_code',
                                            GET_EXPECTED_RESPONSE_CODE)
        if kwargs:
            raise TypeError(' Unexpected **kwargs: %r' % kwargs)
        # API request - get first page
        response = self._req_session.get(self.urljoin(url), timeout=timeout)
        _check_response(response, expected_response_code)
        json_dict = _extract_and_parse_json(response)
        while True:
            # Yield response content
            yield json_dict
            # Get next page
            if response.links.get('next'):
                next_url = response.links.get('next').get('url')
                # API request - get next page
                response = self._req_session.get(next_url, timeout=timeout)
                _check_response(response, expected_response_code)
                json_dict = _extract_and_parse_json(response)
            else:
                raise StopIteration

    def get_items(self, url, **kwargs):
        pages = self.get_pages(url, **kwargs)
        for json_dict in pages:
            assert isinstance(json_dict, dict)
            items = json_dict.get(u'items')
            if items:
                for item in items:
                    yield item
            else:
                error_message = "'items' object not found in JSON data: %r" \
                                % json_dict
                raise exception.CiscoSparkApiException(error_message)

    def post(self, url, json_dict, **kwargs):
        timeout = kwargs.pop('timeout', self.timeout)
        expected_response_code = kwargs.pop('expected_response_code',
                                            POST_EXPECTED_RESPONSE_CODE)
        if kwargs:
            raise TypeError(' Unexpected **kwargs: %r' % kwargs)
        # API request
        response = self._req_session.post(self.urljoin(url),
                                          json=json_dict,
                                          timeout=timeout)
        _check_response(response, expected_response_code)
        return _extract_and_parse_json(response)

    def put(self, url, json_dict, **kwargs):
        timeout = kwargs.pop('timeout', self.timeout)
        expected_response_code = kwargs.pop('expected_response_code',
                                            PUT_EXPECTED_RESPONSE_CODE)
        if kwargs:
            raise TypeError(' Unexpected **kwargs: %r' % kwargs)
        # API request
        response = self._req_session.put(self.urljoin(url),
                                         json=json_dict,
                                         timeout=timeout)
        _check_response(response, expected_response_code)
        return _extract_and_parse_json(response)

    def delete(self, url, **kwargs):
        timeout = kwargs.pop('timeout', self.timeout)
        expected_response_code = kwargs.pop('expected_response_code',
                                            DELETE_EXPECTED_RESPONSE_CODE)
        if kwargs:
            raise TypeError(' Unexpected **kwargs: %r' % kwargs)
        # API request
        response = self._req_session.delete(self.urljoin(url), timeout=timeout)
        _check_response(response, expected_response_code)
