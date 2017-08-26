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
from past.builtins import basestring

import json

import requests

from collections import OrderedDict

from ciscosparkapi.responsecodes import SPARK_RESPONSE_CODES


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


class ciscosparkapiException(Exception):
    """Base class for all ciscosparkapi package exceptions."""

    def __init__(self, *error_message_args, **error_data):
        super(ciscosparkapiException, self).__init__()

        self.error_message_args = error_message_args
        self.error_data = OrderedDict(error_data)

    @property
    def error_message(self):
        """The error message created from the error message arguments."""
        if not self.error_message_args:
            return ""
        elif len(self.error_message_args) == 1:
            return str(self.error_message_args[0])
        elif len(self.error_message_args) > 1 \
                and isinstance(self.error_message_args[0], basestring):
            return self.error_message_args[0] % self.error_message_args[1:]
        else:
            return "; ".join(self.error_message_args)

    def __repr__(self):
        """String representation of the exception."""
        arg_list = self.error_message_args
        kwarg_list = [str(key) + "=" + repr(value)
                      for key, value in self.error_data.items()]
        arg_string = ", ".join(arg_list + kwarg_list)

        return self.__class__.__name__ + "(" + arg_string + ")"

    def __str__(self):
        """Human readable string representation of the exception."""
        return self.error_message + '\n' + \
            json.dumps(self.error_data, indent=4)


class SparkApiError(ciscosparkapiException):
    """Errors returned by requests to the Cisco Spark cloud APIs."""

    def __init__(self, response):
        assert isinstance(response, requests.Response)

        super(SparkApiError, self).__init__()

        # Convenience data attributes
        self.request = response.request
        self.response = response
        self.response_code = response.status_code
        self.response_text = SPARK_RESPONSE_CODES.get(self.response_code,
                                                      "Unknown Response Code")

        # Error message and parameters
        self.error_message_args = [
            "Response Code [%s] - %s",
            self.response_code,
            self.response_text
        ]

        # Error Data
        self.error_data["response_code"] = self.response_code
        self.error_data["description"] = self.response_text
        if response.text:
            try:
                response_data = json.loads(response.text,
                                           object_pairs_hook=OrderedDict)
            except ValueError:
                self.error_data["response_body"] = response.text
            else:
                self.error_data["response_body"] = response_data


class SparkRateLimitError(SparkApiError):
    """Cisco Spark Rate-Limit exceeded Error."""

    def __init__(self, response):
        assert isinstance(response, requests.Response)

        super(SparkRateLimitError, self).__init__(response)

        retry_after = response.headers.get('Retry-After')
        if retry_after:
            # Convenience data attributes
            self.retry_after = float(retry_after)

            # Error Data
            self.error_data["retry_after"] = self.retry_after
