# -*- coding: utf-8 -*-
"""Simple data model; models Spark JSON objects as simple Python objects.

Classes:
    SimpleDataModel: Models Spark JSON objects as simple Python objects.

The SimpleDataModel class models any JSON object passed to it as a string or
Python dictionary as a native Python object; providing attribute access using
native dot-syntax.

"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *
import json

from ..utils import json_dict


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


class SimpleDataModel(object):
    """Model a Spark JSON object as a simple Python object."""

    def __init__(self, json_data):
        """Init a new SparkData object from a dictionary or JSON string.

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
