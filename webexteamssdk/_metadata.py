# -*- coding: utf-8 -*-
"""Package metadata.

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

__title__ = 'webexteamssdk'
__description__ = 'Community-developed Python SDK for the Webex Teams APIs'
__url__ = 'https://github.com/CiscoDevNet/webexteamssdk'
__download_url__ = 'https://pypi.python.org/pypi/webexteamssdk'
__author__ = 'Chris Lunsford'
__author_email__ = 'chrlunsf@cisco.com'
__copyright__ = "Copyright (c) 2016-2020 Cisco and/or its affiliates."
__license__ = "MIT"


# Only import the ._version module and compute the version when this module is
# imported.
if __name__ == "webexteamssdk._metadata":
    from ._version import get_versions
    __version__ = get_versions()['version']
    del get_versions
