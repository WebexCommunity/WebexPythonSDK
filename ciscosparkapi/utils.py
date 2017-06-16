# -*- coding: utf-8 -*-
"""Package helper functions and classes."""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *

from collections import namedtuple
import functools
import mimetypes
import os
import urllib.parse

from ciscosparkapi.exceptions import ciscosparkapiException, SparkApiError


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


# Cisco Spark cloud Expected Response Codes (HTTP Response Codes)
ERC = {
    'GET': 200,
    'POST': 200,
    'PUT': 200,
    'DELETE': 204
}


EncodableFile = namedtuple('EncodableFile',
                           ['file_name', 'file_object', 'content_type'])


def validate_base_url(base_url):
    """Verify that base_url specifies a protocol and network location."""
    parsed_url = urllib.parse.urlparse(base_url)
    if parsed_url.scheme and parsed_url.netloc:
        return parsed_url.geturl()
    else:
        error_message = "base_url must contain a valid scheme (protocol " \
                        "specifier) and network location (hostname)"
        raise ciscosparkapiException(error_message)


def is_web_url(string):
    """Check to see if string is an validly-formatted web url."""
    assert isinstance(string, str)
    parsed_url = urllib.parse.urlparse(string)
    return ((parsed_url.scheme.lower() == 'http' or
             parsed_url.scheme.lower() == 'https') and
            parsed_url.netloc)


def is_local_file(string):
    """Check to see if string is a valid local file path."""
    assert isinstance(string, str)
    return os.path.isfile(string)


def open_local_file(file_path):
    """Open the file and return an EncodableFile tuple."""
    assert isinstance(file_path, str)
    assert is_local_file(file_path)
    file_name = os.path.basename(file_path)
    file_object = open(file_path, 'rb')
    content_type = mimetypes.guess_type(file_name)[0] or 'text/plain'
    return EncodableFile(file_name=file_name,
                         file_object=file_object,
                         content_type=content_type)


def raise_if_extra_kwargs(kwargs):
    """Raise a TypeError if kwargs is not empty."""
    if kwargs:
        raise TypeError("Unexpected **kwargs: {!r}".format(kwargs))


def check_response_code(response, erc):
    """Check response code against the expected code; raise SparkApiError.

    Checks the requests.response.status_code against the provided expected
    response code (erc), and raises a SparkApiError if they do not match.

    Args:
        response(requests.response): The response object returned by a request
            using the requests package.
        erc(int): The expected response code (HTTP response code).

    Raises:
        SparkApiError: If the requests.response.status_code does not match the
            provided expected response code (erc).

     """
    if response.status_code != erc:
        raise SparkApiError(response.status_code,
                            request=response.request,
                            response=response)


def extract_and_parse_json(response):
    """Extract and parse the JSON data from an requests.response object.

    Args:
        response(requests.response): The response object returned by a request
            using the requests package.

    Returns:
        The parsed JSON data as the appropriate native Python data type.

    """
    return response.json()


class GeneratorContainer(object):
    """Container for storing a function call to a generator function.

    Return a fresh iterator every time __iter__() is called on the container
    object.

    Attributes:
        generator(func): The generator function.
        args(list): The arguments passed to the generator function.
        kwargs(dict): The keyword arguments passed to the generator function.

    """

    def __init__(self, generator, *args, **kwargs):
        """Init a new GeneratorContainer.

        Args:
            generator(func): The generator function.
            *args: The arguments passed to the generator function.
            **kwargs: The keyword arguments passed to the generator function.

        """
        self.generator = generator
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        """Return a fresh iterator."""
        return self.generator(*self.args, **self.kwargs)


def generator_container(generator):
    """Function Decorator: Containerize calls to a generator function.

    Args:
        generator(func): The generator function being containerized.

    Returns:
        func: A wrapper function that containerizes the calls to the generator.

    """

    @functools.wraps(generator)
    def generator_container_wrapper(*args, **kwargs):
        """Store a generator call in a container and return the container.

        Args:
            *args: The arguments passed to the generator function.
            **kwargs: The keyword arguments passed to the generator function.

        Returns:
            GeneratorContainer: A container wrapping the call to the generator.

        """
        return GeneratorContainer(generator, *args, **kwargs)

    return generator_container_wrapper
