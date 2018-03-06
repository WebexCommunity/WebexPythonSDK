# -*- coding: utf-8 -*-
"""ciscosparkapi exception classes."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *
import sys
import textwrap

from past.builtins import basestring
import requests

from .response_codes import SPARK_RESPONSE_CODES


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


# Helper functions
def sanitize(header_tuple):
    """Sanitize request headers.

    Remove Spark authentication token.

    """
    header, value = header_tuple

    if (header.lower().strip() == "Authorization".lower().strip()
            and "Bearer".lower().strip() in value.lower().strip()):
        return header, "Bearer <redacted>"

    else:
        return header_tuple


def to_unicode(string):
    """Convert a string (bytes, str or unicode) to unicode."""
    assert isinstance(string, basestring)
    if sys.version_info[0] >= 3:
        if isinstance(string, bytes):
            return string.decode('utf-8')
        else:
            return string
    else:
        if isinstance(string, str):
            return string.decode('utf-8')
        else:
            return string


def response_to_string(response):
    """Render a response object as a human readable string."""
    assert isinstance(response, requests.Response)
    request = response.request

    section_header = "{title:-^79}"

    # Prepare request components
    req = textwrap.fill("{} {}".format(request.method, request.url),
                        width=79,
                        subsequent_indent=' ' * (len(request.method) + 1))
    req_headers = [
        textwrap.fill("{}: {}".format(*sanitize(header)),
                      width=79,
                      subsequent_indent=' ' * 4)
        for header in request.headers.items()
    ]
    req_body = (textwrap.fill(to_unicode(request.body), width=79)
                if request.body else "")

    # Prepare response components
    resp = textwrap.fill("{} {}".format(response.status_code,
                                        response.reason
                                        if response.reason else ""),
                         width=79,
                         subsequent_indent=' ' * (len(request.method) + 1))
    resp_headers = [
        textwrap.fill("{}: {}".format(*header), width=79,
                      subsequent_indent=' ' * 4)
        for header in response.headers.items()
    ]
    resp_body = textwrap.fill(response.text, width=79) if response.text else ""

    # Return the combined string
    return "\n".join([
        section_header.format(title="Request"),
        req,
        "\n".join(req_headers),
        "",
        req_body,
        "",
        section_header.format(title="Response"),
        resp,
        "\n".join(resp_headers),
        "",
        resp_body,
    ])


class ciscosparkapiException(Exception):
    """Base class for all ciscosparkapi package exceptions."""
    pass


class SparkApiError(ciscosparkapiException):
    """Errors returned by requests to the Cisco Spark cloud APIs."""

    def __init__(self, response):
        assert isinstance(response, requests.Response)

        # Extended exception data attributes
        self.request = response.request
        """The :class:`requests.PreparedRequest` of the API call."""

        self.response = response
        """The :class:`requests.Response` object returned from the API call."""

        # Error message
        response_code = response.status_code
        response_reason = " " + response.reason if response.reason else ""
        description = SPARK_RESPONSE_CODES.get(response_code,
                                               "Unknown Response Code")
        detail = response_to_string(response)

        super(SparkApiError, self).__init__("Response Code [{}]{} - {}\n{}"
                                            "".format(response_code,
                                                      response_reason,
                                                      description,
                                                      detail))


class SparkRateLimitError(SparkApiError):
    """Cisco Spark Rate-Limit exceeded Error."""

    def __init__(self, response):
        super(SparkRateLimitError, self).__init__(response)

        # Extended exception data attributes
        self.retry_after = max(1, int(response.headers.get('Retry-After', 15)))
        """The `Retry-After` time period (in seconds) provided by Cisco Spark.

        Defaults to 15 seconds if the response `Retry-After` header isn't
        present in the response headers, and defaults to a minimum wait time of
        1 second if Spark returns a `Retry-After` header of 0 seconds.

        """


class SparkRateLimitWarning(UserWarning):
    """Cisco Spark rate-limit exceeded warning; the request will be retried."""

    def __init__(self, response):
        super(SparkRateLimitWarning, self).__init__()
        self.retry_after = max(1, int(response.headers.get('Retry-After', 15)))
        """The `Retry-After` time period (in seconds) provided by Cisco Spark.

        Defaults to 15 seconds if the response `Retry-After` header isn't
        present in the response headers, and defaults to a minimum wait time of
        1 second if Spark returns a `Retry-After` header of 0 seconds.

        """

    def __str__(self):
        """Spark rate-limit exceeded warning message."""
        return "Rate-limit response received; the request will " \
               "automatically be retried in {0} seconds." \
               "".format(self.retry_after)
