# -*- coding: utf-8 -*-
"""Webex Teams Access-Tokens API wrapper.

Copyright (c) 2016-2020 Cisco and/or its affiliates.

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


def set_if_not_none(property_name, property, export):
    if property is not None:
        export[property_name] = property.to_dict()


def check_type(obj, acceptable_types, optional=False, is_list=False):
    """Object is an instance of one of the acceptable types or None.

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
                "following types: {types}{none}; instead we received {o} "
                "which is a {o_type}.".format(
                    types=", ".join(
                        [repr(t.__name__) for t in acceptable_types]
                    ),
                    none="or None" if optional else "",
                    o=obj,
                    o_type=repr(type(obj).__name__)
                )
            )
            raise TypeError(error_message)

        for o in obj:
            if not isinstance(o, acceptable_types):
                error_message = (
                    "We were expecting to receive an object of one of the "
                    "following types: {types}{none}; but instead we received "
                    "{o} which is a {o_type}.".format(
                        types=", ".join(
                            [repr(t.__name__) for t in acceptable_types]
                        ),
                        none="or None" if optional else "",
                        o=o,
                        o_type=repr(type(o).__name__)
                    )
                )
                raise TypeError(error_message)
        return

    if isinstance(obj, acceptable_types):
        return
    else:
        error_message = (
            "We were expecting to receive an instance of one of the following "
            "types: {types}{none}; but instead we received {o} which is a "
            "{o_type}.".format(
                types=", ".join([repr(t.__name__) for t in acceptable_types]),
                none="or 'None'" if optional else "",
                o=obj,
                o_type=repr(type(obj).__name__)
            )
        )
        raise TypeError(error_message)
