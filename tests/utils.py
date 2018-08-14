# -*- coding: utf-8 -*-
"""Test utilities, helper functions, and classes.

Copyright (c) 2016-2018 Cisco and/or its affiliates.

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

import datetime
import os

import requests

from tests.environment import (
    WEBEX_TEAMS_TEST_STRING_PREFIX, WEBEX_TEAMS_TEST_STRING_TEMPLATE,
)


def create_string(item):
    """Create strings for tests."""
    return WEBEX_TEAMS_TEST_STRING_TEMPLATE.substitute(
        prefix=WEBEX_TEAMS_TEST_STRING_PREFIX,
        item=item,
        datetime=str(datetime.datetime.now())
    )


def download_file(url, local_directory, local_filename=None):
    """Download a file from a remote URL to a local directory."""
    # http://stackoverflow.com/questions/16694907/
    # how-to-download-large-file-in-python-with-requests-py
    local_filename = local_filename if local_filename \
        else url.split('/')[-1]
    local_path = os.path.normpath(os.path.join(
        local_directory, local_filename,
    ))
    response = requests.get(url, stream=True)
    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_path
