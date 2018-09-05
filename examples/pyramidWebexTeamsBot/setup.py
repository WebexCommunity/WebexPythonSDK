#  -*- coding: utf-8 -*-
"""A simple bot script, built on Pyramid using Cornice.

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

__author__ = "Jose Bogarín Solano"
__author_email__ = "jose@bogarin.co.cr"
__contributors__ = ["Chris Lunsford <chrlunsf@cisco.com>"]
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(
    name='pyramidWebexTeamsBot',
    version=0.1,
    description='Pyramid Webex Teams Bot application',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
    keywords="web services",
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cornice',
        'waitress',
        'webexteamssdk'
    ],
    entry_points="""[paste.app_factory]
                    main=pyramidWebexTeamsBot:main
                    """,
    paster_plugins=['pyramid']
)
