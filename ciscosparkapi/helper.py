"""Package helper functions and classes.

Functions:
    utf8: Returns the input string as a UTF-8 unicode encoded string.
    generator_container: Function decorator that containerizes calls to
        generator functions.

Classes:
    GeneratorContainer: Container for storing a function call to a generator
        function.

"""


import functools
import urlparse

from ciscosparkapi import ciscosparkapiException, SparkApiError


# Cisco Spark cloud Expected Response Codes (HTTP Response Codes)
ERC = {
    'GET': 200,
    'POST': 200,
    'PUT': 200,
    'DELETE': 204
}


def validate_base_url(base_url):
    """Verify that base_url specifies a protocol and network location."""
    parsed_url = urlparse.urlparse(base_url)
    if parsed_url.scheme and parsed_url.netloc:
        return parsed_url.geturl()
    else:
        error_message = "base_url must contain a valid scheme (protocol " \
                        "specifier) and network location (hostname)"
        raise ciscosparkapiException(error_message)


def raise_if_extra_kwargs(kwargs):
    """Raise a TypeError if kwargs is not empty."""
    if kwargs:
        raise TypeError("Unexpected **kwargs: %r" % kwargs)


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


def utf8(string):
    """Return the 'string' as a UTF-8 unicode encoded string.

    Ensure that 'string' is a unicode encoded string; converting if necessary.

    Args:
        string(unicode, str): The input string.

    Returns:
        unicode: The input string encoded as a unicode string.

    Raises:
        AssertionError: If the parameter types are incorrect.

    """
    assert isinstance(string, basestring)
    if isinstance(string, unicode):
        return string
    elif isinstance(string, str):
        return unicode(string, encoding='utf-8')


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
        """Inits a new GeneratorContainer.

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
