"""Package helper functions."""


def utf8(string):
    """Return the 'string' as a UTF-8 unicode encoded string."""
    assert isinstance(string, basestring)
    if isinstance(string, unicode):
        return string
    elif isinstance(string, str):
        return unicode(string, encoding='utf-8')
