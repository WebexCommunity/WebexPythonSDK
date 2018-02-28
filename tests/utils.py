# -*- coding: utf-8 -*-
"""Tests helper functions and classes."""


import datetime
import os
import string

import requests


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


STRING_PREFIX = "ciscosparkapi py.test"
STRING_TEMPLATE = string.Template("$prefix $item [$datetime]")


# Helper Functions

def create_string(item):
    """Create strings for tests; prefixed-timestamped strings."""
    return STRING_TEMPLATE.substitute(prefix=STRING_PREFIX,
                                      item=item,
                                      datetime=str(datetime.datetime.now()))


def download_file(url, local_directory, local_filename=None):
    """Download a file from a remote URL to a local directory."""
    # http://stackoverflow.com/questions/16694907/
    # how-to-download-large-file-in-python-with-requests-py
    local_filename = local_filename if local_filename \
        else url.split('/')[-1]
    local_path = os.path.normpath(os.path.join(local_directory,
                                               local_filename))
    response = requests.get(url, stream=True)
    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_path
