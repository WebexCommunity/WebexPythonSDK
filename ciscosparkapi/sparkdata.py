# -*- coding: utf-8 -*-
"""SparkData base-class; models Spark JSON objects as native Python objects.

The SparkData class models any JSON object passed to it as a string or Python
dictionary as a native Python object; providing attribute access using native
dot-syntax (`object.attribute`).

SparkData is intended to serve as a base-class, which provides inheritable
functionality, for concrete sub-classes that model specific Cisco Spark data
objects (rooms, messages, webhooks, etc.).  The SparkData base-class provides
attribute access to any additional JSON attributes received from the Cisco
Spark cloud, which haven't been implemented by the concrete sub-classes.  This
provides a measure of future-proofing when additional data attributes are added
to objects by the Cisco Spark cloud.

Example:
    >>> json_obj = '''{"created": "2012-06-15T20:36:48.914Z",
                       "displayName": "Chris Lunsford (chrlunsf)",
                       "id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mZjhlZTZmYi1h...",
                       "avatar": "https://1efa7a94ed216783e352-c6226652871...",
                       "emails": ["chrlunsf@cisco.com"]}'''
    >>> python_obj = SparkData(json_obj)
    >>> python_obj.displayName
    u'Chris Lunsford (chrlunsf)'
    >>> python_obj.created
    u'2012-06-15T20:36:48.914Z'

"""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
from past.builtins import basestring

import json as json_pkg

from collections import OrderedDict


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


def _json_dict(json):
    """Given a dictionary or JSON string; return a dictionary.

    Args:
        json(dict, str): Input JSON object.

    Returns:
        A Python dictionary with the contents of the JSON object.

    Raises:
        TypeError: If the input object is not a dictionary or string.

    """
    if isinstance(json, dict):
        return json
    elif isinstance(json, str):
        return json_pkg.loads(json, object_hook=OrderedDict)
    else:
        error = "'json' must be a dictionary or valid JSON string; " \
                "received: {!r}".format(json)
        raise TypeError(error)


class SparkData(object):
    """Model Spark JSON objects as native Python objects."""

    def __init__(self, json):
        """Init a new SparkData object from a dictionary or JSON string.

        Args:
            json(dict, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(SparkData, self).__init__()
        self._json_data = _json_dict(json)

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
            error = "'{}' object has no attribute " \
                    "'{}'".format(self.__class__.__name__, item)
            raise AttributeError(error)

    def __str__(self):
        """Return a human-readable string representation of this object."""
        class_str = self.__class__.__name__
        json_str = json_pkg.dumps(self._json_data, indent=2)
        return "{}:\n{}".format(class_str, json_str)

    def __repr__(self):
        """Return a string representing this object as valid Python expression.
        """
        class_str = self.__class__.__name__
        json_str = json_pkg.dumps(self._json_data, ensure_ascii=False)
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
        return json_pkg.dumps(self._json_data, **kwargs)
