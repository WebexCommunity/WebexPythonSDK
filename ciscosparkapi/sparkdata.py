"""SparkData base-class; represents Spark JSON as native Python objects."""


import json as json_pkg


def _json_dict(json):
    if isinstance(json, dict):
        return json
    elif isinstance(json, basestring):
        return json_pkg.loads(json)
    else:
        error = "'json' must be a dictionary or string; " \
                "received: %r" % json
        raise TypeError(error)


class SparkData(object):
    """Represents Spark JSON as native Python objects."""

    def __init__(self, json):
        super(SparkData, self).__init__()
        self._json = _json_dict(json)

    def __getattr__(self, item):
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
        class_str = self.__class__.__name__
        json_str = json_pkg.dumps(self._json, indent=2)
        return "%s:\n%s" % (class_str, json_str)

    def __repr__(self):
        class_str = self.__class__.__name__
        json_str = json_pkg.dumps(self._json, ensure_ascii=False)
        return "%s(%r)" % (class_str, json_str)
