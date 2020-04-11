# -*- coding: utf-8 -*-
"""Webex Teams Access-Tokens API wrapper.

Copyright (c) 2016-2019 Cisco and/or its affiliates.

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

def check_type(obj, acceptable_types, is_list=False, may_be_none=False):
    """Object is an instance of one of the acceptable types or None.

    Args:
        obj: The object to be inspected.
        acceptable_types: A type or tuple of acceptable types.
        is_list(bool): Whether or not we expect a list of objects of acceptable
            type
        may_be_none(bool): Whether or not the object may be None.

    Raises:
        TypeError: If the object is None and may_be_none=False, or if the
            object is not an instance of one of the acceptable types.

    """
    error_message = None
    if not isinstance(acceptable_types, tuple):
        acceptable_types = (acceptable_types,)

    if may_be_none and obj is None:
        pass
    elif is_list:
        # Check that all objects in that list are of the required type
        if not isinstance(obj, list):
            error_message = (
                "We were expecting to receive a list of one of the following "
                "types: {types}{none}; but instead we received {o} which is a "
                "{o_type}.".format(
                    types=", ".join([repr(t.__name__) for t in acceptable_types]),
                    none="or 'None'" if may_be_none else "",
                    o=obj,
                    o_type=repr(type(obj).__name__)
                )
            )
        else:
            for o in obj:
                if not isinstance(o, acceptable_types):
                    error_message = (
                        "We were expecting to receive an instance of one of the following "
                        "types: {types}{none}; but instead we received {o} which is a "
                        "{o_type}.".format(
                            types=", ".join([repr(t.__name__) for t in acceptable_types]),
                            none="or 'None'" if may_be_none else "",
                            o=o,
                            o_type=repr(type(o).__name__)
                        )
                    )
    elif isinstance(obj, acceptable_types):
        pass
    else:
        # Object is something else.
        error_message = (
            "We were expecting to receive an instance of one of the following "
            "types: {types}{none}; but instead we received {o} which is a "
            "{o_type}.".format(
                types=", ".join([repr(t.__name__) for t in acceptable_types]),
                none="or 'None'" if may_be_none else "",
                o=obj,
                o_type=repr(type(obj).__name__)
            )
        )
    if error_message is not None:
        raise TypeError(error_message)
