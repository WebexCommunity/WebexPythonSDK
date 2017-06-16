# -*- coding: utf-8 -*-
"""ciscosparkapi exception classes."""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


SPARK_RESPONSE_CODES = {
    200: "OK",
    204: "Member deleted.",
    400: "The request was invalid or cannot be otherwise served. An "
         "accompanying error message will explain further.",
    401: "Authentication credentials were missing or incorrect.",
    403: "The request is understood, but it has been refused or access is not "
         "allowed.",
    404: "The URI requested is invalid or the resource requested, such as a "
         "user, does not exist. Also returned when the requested format is "
         "not supported by the requested method.",
    409: "The request could not be processed because it conflicts with some "
         "established rule of the system. For example, a person may not be "
         "added to a room more than once.",
    500: "Something went wrong on the server.",
    503: "Server is overloaded with requests. Try again later."
}


class ciscosparkapiException(Exception):
    """Base class for all ciscosparkapi package exceptions."""

    def __init__(self, *args, **kwargs):
        super(ciscosparkapiException, self).__init__(*args, **kwargs)


class SparkApiError(ciscosparkapiException):
    """Errors returned by requests to the Cisco Spark cloud APIs."""

    def __init__(self, response_code, request=None, response=None):
        assert isinstance(response_code, int)
        self.response_code = response_code
        self.request = request
        self.response = response
        response_text = SPARK_RESPONSE_CODES.get(response_code)
        if response_text:
            self.response_text = response_text
            error_message = "Response Code [{!s}] - {}".format(response_code,
                                                               response_text)
        else:
            error_message = "Response Code [{!s}] - " \
                            "Unknown Response Code".format(response_code)
        super(SparkApiError, self).__init__(error_message)
