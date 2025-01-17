"""Webex Adaptive Card - Utilities Model.

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

from enum import Enum
from typing import Any, Type
from urllib.parse import urlparse


def check_type(
    obj: object,
    acceptable_types: Any,
    optional: bool = False,
    is_list: bool = False,
):
    """
    Object is an instance of one of the acceptable types or None.

    Args:
        obj: The object to be inspected.
        acceptable_types: A type or tuple of acceptable types.
        optional(bool): Whether or not the object may be None.
        is_list(bool): Whether or not we expect a list of objects of acceptable
            type.

    Raises:
        TypeError: If the object is None and optional=False, or if the
            object is not an instance of one of the acceptable types.
    """
    if not isinstance(acceptable_types, tuple):
        acceptable_types = (acceptable_types,)

    if optional and obj is None:
        return

    if is_list:
        # Check that all objects the list are of the required type(s)
        if not isinstance(obj, list):
            error_message = (
                "We were expecting to receive a list of objects of the "
                "following types: "
                f"{', '.join([repr(t.__name__) for t in acceptable_types])}"
                f"{' or None' if optional else ''}; instead we received "
                f"{obj} which is a {repr(type(obj).__name__)}."
            )
            raise TypeError(error_message)

        for o in obj:
            if not isinstance(o, acceptable_types):
                error_message = (
                    "We were expecting to receive an object of one of the "
                    "following types: "
                    f"{', '.join(repr(t.__name__) for t in acceptable_types)}"
                    f"{' or None' if optional else ''}; instead we "
                    f"received {o} which is a {repr(type(o).__name__)}."
                )
                raise TypeError(error_message)
        return

    if isinstance(obj, acceptable_types):
        return
    else:
        error_message = (
            "We were expecting to receive an instance of one of the following "
            f"types: {', '.join(repr(t.__name__) for t in acceptable_types)}"
            f"{' or None' if optional else ''}; but instead we received "
            f"{obj} which is a {repr(type(obj).__name__)}."
        )

        raise TypeError(error_message)


def validate_input(
    input_value: Any,
    allowed_values: Any,
    optional: bool = False,
):
    """
    Validate if the input value is in the tuple of allowed values.

    Args:
        input_value: The value to be validated.
        allowed_values (str | tuple | Enum): A string, a tuple of allowed
            values, or an Enum subclass.
        optional (bool): Whether or not the object may be None.

    Raises:
        ValueError: If the value is not in the allowed values.
        TypeError: If allowed_values is neither a string, a tuple, nor an Enum
            subclass.
    """
    # Return if the argument is optional and if the input is None
    if optional and input_value is None:
        return

    # If allowed_values is an Enum subclass, get its members' values as a tuple
    if isinstance(allowed_values, type) and issubclass(allowed_values, Enum):
        expected_values = tuple(
            f"{item.__class__.__name__}.{item.name}" for item in allowed_values
        )
        allowed_values = tuple(item.value for item in allowed_values)

    # Convert a single string to a tuple of one string
    if isinstance(allowed_values, str):
        allowed_values = (allowed_values,)
        expected_values = allowed_values

    # Ensure allowed_values is a tuple
    if not isinstance(allowed_values, tuple):
        raise TypeError(
            "allowed_values must be a string, a tuple, or an Enum subclass."
        )

    # Determine the value to check based on its type
    value_to_check = (
        input_value.value if isinstance(input_value, Enum) else input_value
    )

    # Check if the value is in the tuple of allowed values
    if value_to_check not in allowed_values:
        raise ValueError(
            f"Invalid value: '{input_value}'. "
            f"Must be one of '{expected_values}'."
        )

    return


def validate_dict_str(
    input_value: Any,
    key_type: Type,
    value_type: Type,
    optional: bool = False,
):
    """
    Validate that the input is a dictionary and that all keys and values in the
    dictionary are of the specified types.

    Args:
        input_value (Any): The input to validate.
        key_type (Type): The expected type for the dictionary keys.
        value_type (Type): The expected type for the dictionary values.
        optional(bool): Whether or not the object may be None.

    Raises:
        TypeError: If the input is not a dictionary or any key or value in the
            dictionary does not match the specified types, with details about
            the non-conforming elements.
    """
    if optional and input_value is None:
        return

    if not isinstance(input_value, dict):
        raise TypeError(f"'{input_value}' is not of type 'dict'")

    errors = []

    for key, value in input_value.items():
        if not isinstance(key, key_type):
            errors.append(
                f"Key '{key}' of type '{type(key).__name__}' "
                f"is not of type '{key_type.__name__}'."
            )
        if not isinstance(value, value_type):
            errors.append(
                f"Value '{value}' of type '{type(value).__name__}' "
                f"is not of type '{value_type.__name__}'."
            )

    if errors:
        raise TypeError("\n".join(errors))

    return


class URIException(Exception):
    """
    Custom exception for invalid URIs.
    """


def validate_uri(
    uri: Any,
    optional=False,
):
    """
    Validate the given URI and raise an exception if it is invalid.

    Args:
        uri (str): The URI to validate.
        optional(bool): Whether or not the object may be None.

    Raises:
        TypeError: If the input is not a string.
        URIException: If the URI is invalid.
    """
    if optional and uri is None:
        return

    if not isinstance(uri, str):
        raise TypeError(f"'{uri}' is not of type 'str'")

    # First validate using urlparse
    parsed_uri = urlparse(uri)

    # Check if the URI has a scheme
    if not parsed_uri.scheme:
        raise URIException("Invalid URI: Missing scheme")

    # Check if the URI has a heir-part location if scheme isn't "data"
    if parsed_uri.scheme != "data" and not parsed_uri.netloc:
        raise URIException("Invalid URI: Missing heir part location")

    # Return if every check is passed
    return
