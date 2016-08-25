"""SparkData base-class; models Spark JSON objects as native Python objects.

The SparkData class models any JSON object passed to it as a string or Python
dictionary as a native Python object; providing attribute access access using
native object.attribute syntax.

SparkData is intended to serve as a base-class, which provides inheritable
functionality, for concrete sub-classes that model specific Cisco Spark data
objects (rooms, messages, webhooks, etc.).  The SparkData base-class provides
attribute access to any additonal JSON attributes received from the Cisco Spark
cloud, which haven't been implemented by the concrete sub-classes.  This
provides a measure of future-proofing when additional data attributes are added
to objects by the Cisco Spark cloud.

Example:
    >>> json_obj = '{"created": "2012-06-15T20:36:48.914Z", "displayName": "Chris Lunsford (chrlunsf)", "id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mZjhlZTZmYi1hZmVmLTRhNGQtOTJiMS1kNmIyMTZiNTg5NDk", "avatar": "https://1efa7a94ed216783e352-c62266528714497a17239ececf39e9e2.ssl.cf1.rackcdn.com/V1~ba1ecf557a7e0b7cc3081998df965aad~cNFKqEjAQ5aQkyt_l1zsCQ==~1600", "emails": ["chrlunsf@cisco.com"]}'
    >>> python_obj = SparkData(json_obj)
    >>> python_obj.displayName
    u'Chris Lunsford (chrlunsf)'
    >>> python_obj.created
    u'2012-06-15T20:36:48.914Z'

"""


import json as json_pkg


def _json_dict(json):
    """Given a JSON dictionary or string; return a dictionary.

    Args:
        json(dict, unicode, str): Input JSON object.

    Returns:
        A Python dictionary with the contents of the JSON object.

    Raises:
        TypeError: If the input object is not a dictionary or string.

    """
    if isinstance(json, dict):
        return json
    elif isinstance(json, basestring):
        return json_pkg.loads(json)
    else:
        error = "'json' must be a dictionary or string; " \
                "received: %r" % json
        raise TypeError(error)


class SparkData(object):
    """Model Spark JSON objects as native Python objects."""

    def __init__(self, json):
        """Inits a new SparkData object from a JSON dictionary or string.

        Args:
            json(dict, unicode, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(SparkData, self).__init__()
        self._json = _json_dict(json)

    def __getattr__(self, item):
        """Provide native attribute access to the JSON object's attributes.

        This method is called when attempting to access a object attribute that
        hasn't been defined for the object.  For example trying to access
        object.attribute1 when attribute1 hasn't been defined.

        SparkData.__getattr__() checks the original JSON object to see if the
        attribute exists, and if it does, it returns the attribute's value
        from the original JSON object.  This provides native access to all of
        the JSON object's attributes.

        Args:
            item(unicode, str): Name of the Attribute being accessed.

        Raises:
            AttributeError:  If the JSON object does not contain the attribute
                requested.

        """
        if item in self._json.keys():
            item_data = self._json[item]
            if isinstance(item_data, dict):
                return SparkData(item_data)
            else:
                return item_data
        else:
            error = "'%s' object has no attribute '%s'" % \
                    (self.__class__.__name__, item)
            raise AttributeError(error)

    def __str__(self):
        """Return a human-readable string representation of this object."""
        class_str = self.__class__.__name__
        json_str = json_pkg.dumps(self._json, indent=2)
        return "%s:\n%s" % (class_str, json_str)

    def __repr__(self):
        """Return a string representing this object as valid Python expression.
        """
        class_str = self.__class__.__name__
        json_str = json_pkg.dumps(self._json, ensure_ascii=False)
        return "%s(%r)" % (class_str, json_str)
