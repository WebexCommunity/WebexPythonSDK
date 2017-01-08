# -*- coding: utf-8 -*-

"""Tests helper functions and classes."""


import datetime
import string


STRING_PREFIX = "ciscosparkapi py.test"
STRING_TEMPLATE = string.Template("$prefix $item [$datetime]")


# Helper Functions

def create_string(item):
    return STRING_TEMPLATE.substitute(prefix=STRING_PREFIX,
                                      item=item,
                                      datetime=str(datetime.datetime.now()))
