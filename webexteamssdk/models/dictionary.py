# -*- coding: utf-8 -*-
"""Webex Teams data models.

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

from webexteamssdk.utils import json_dict


def dict_data_factory(model, json_data):
    """Factory function for creating SimpleDataModel objects.

    Args:
        model(basestring): The data model to use when creating the data
            object (message, room, membership, etc.).
        json_data(basestring, dict): The JSON string or dictionary data with
            which to initialize the object.

    Returns:
        OrderedDict: An ordered dictionary with the contents of the Webex Teams
         JSON object.

    Raises:
        TypeError: If the json_data parameter is not a JSON string or
            dictionary.

    """
    return json_dict(json_data)
