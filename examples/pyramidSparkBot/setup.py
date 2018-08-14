#  -*- coding: utf-8 -*-
"""A simple bot script, built on Pyramid using Cornice"""

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
    name='pyramidSparkBot',
    version=0.1,
    description='Pyramid Spark Bot application',
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
                    main=pyramidSparkBot:main
                    """,
    paster_plugins=['pyramid']
)
