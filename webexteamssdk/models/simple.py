# -*- coding: utf-8 -*-
"""Simple data model; models Webex Teams JSON objects as simple Python objects.

Classes:
    SimpleDataModel: Models Webex Teams JSON objects as simple Python objects.

The SimpleDataModel class models any JSON object passed to it as a string or
Python dictionary as a native Python object; providing attribute access using
native dot-syntax.

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


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import json
from builtins import *

from webexteamssdk.utils import json_dict


class SimpleDataModel(object):
    """Model a Webex Teams JSON object as a simple Python object."""

    def __init__(self, json_data):
        """Init a new SimpleDataModel object from a dictionary or JSON string.

        Args:
            json_data(dict, basestring): Input JSON string or dictionary.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(SimpleDataModel, self).__init__()
        for attribute, value in json_dict(json_data).items():
            setattr(self, attribute, value)

    def __str__(self):
        """A human-readable string representation of this object."""
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4)

    def __repr__(self):
        """A string representing this object as valid Python expression."""
        class_str = self.__class__.__name__
        json_str = json.dumps(self.__dict__, ensure_ascii=False)
        return "{}({})".format(class_str, repr(json_str))


def simple_data_factory(model, json_data):
    """Factory function for creating SimpleDataModel objects.

    Args:
        model(basestring): The data model to use when creating the data
            object (message, room, membership, etc.).
        json_data(basestring, dict): The JSON string or dictionary data with
            which to initialize the object.

    Returns:
        SimpleDataModel: The created SimpleDataModel object.

    Raises:
        TypeError: If the json_data parameter is not a JSON string or
            dictionary.

    """
    return SimpleDataModel(json_data)
