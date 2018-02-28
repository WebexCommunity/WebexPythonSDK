# -*- coding: utf-8 -*-
"""SparkData data model; models Spark JSON objects as native Python objects.

Classes:
    SparkData: Models Spark JSON objects as native Python objects.

The SparkData class models any JSON object passed to it as a string or Python
dictionary as a native Python object; providing attribute access using native
dot-syntax (`object.attribute`).

"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *
from collections import OrderedDict
import json

from past.builtins import basestring


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


def _json_dict(json_data):
    """Given a dictionary or JSON string; return a dictionary.

    Args:
        json_data(dict, str): Input JSON object.

    Returns:
        A Python dictionary with the contents of the JSON object.

    Raises:
        TypeError: If the input object is not a dictionary or string.

    """
    if isinstance(json_data, dict):
        return json_data
    elif isinstance(json_data, basestring):
        return json.loads(json_data, object_hook=OrderedDict)
    else:
        raise TypeError(
            "'json_data' must be a dictionary or valid JSON string; "
            "received: {!r}".format(json_data)
        )


class SparkData(object):
    """Model a Spark JSON object as a native Python object."""

    def __init__(self, json_data):
        """Init a new SparkData object from a dictionary or JSON string.

        Args:
            json_data(dict, basestring): Input JSON string or dictionary.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(SparkData, self).__init__()
        self._json_data = _json_dict(json_data)

    def __getattr__(self, item):
        """Provide native attribute access to the JSON object attributes.

        This method is called when attempting to access a object attribute that
        hasn't been defined for the object.  For example trying to access
        object.attribute1 when attribute1 hasn't been defined.

        SparkData.__getattr__() checks the original JSON object to see if the
        attribute exists, and if it does, it returns the attribute's value
        from the original JSON object.  This provides native access to all of
        the JSON object's attributes.

        Args:
            item(str): Name of the Attribute being accessed.

        Raises:
            AttributeError:  If the JSON object does not contain the attribute
                requested.

        """
        if item in list(self._json_data.keys()):
            item_data = self._json_data[item]
            if isinstance(item_data, dict):
                return SparkData(item_data)
            else:
                return item_data
        else:
            raise AttributeError(
                "'{}' object has no attribute '{}'"
                "".format(self.__class__.__name__, item)
            )

    def __str__(self):
        """A human-readable string representation of this object."""
        class_str = self.__class__.__name__
        json_str = json.dumps(self._json_data, indent=2)
        return "{}:\n{}".format(class_str, json_str)

    def __repr__(self):
        """A string representing this object as valid Python expression."""
        class_str = self.__class__.__name__
        json_str = json.dumps(self._json_data, ensure_ascii=False)
        return "{}({})".format(class_str, json_str)

    @property
    def json_data(self):
        """A copy of the Spark data object's JSON data (OrderedDict)."""
        return self._json_data.copy()

    def to_dict(self):
        """Convert the Spark data to a dictionary."""
        return dict(self._json_data)

    def to_json(self, **kwargs):
        """Convert the Spark data to JSON.

        Any keyword arguments provided are passed through the Python JSON
        encoder.

        """
        return json.dumps(self._json_data, **kwargs)
