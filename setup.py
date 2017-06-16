# -*- coding: utf-8 -*-
"""A setuptools based setup module."""


from codecs import open
from os import path
from setuptools import setup

import versioneer


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


# Get the long description from the README file
current_path = path.abspath(path.dirname(__file__))
with open(path.join(current_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ciscosparkapi',

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description='Simple, lightweight, scalable Python API wrapper for the '
                'Cisco Spark APIs',
    long_description=long_description,

    url='https://github.com/CiscoDevNet/ciscosparkapi',
    download_url="https://pypi.python.org/pypi/ciscosparkapi",

    author=__author__,
    author_email=__author_email__,

    license=__license__+"; "+__copyright__,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Education',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications',
        'Topic :: Communications :: Chat'
    ],

    keywords='cisco spark api enterprise messaging',

    packages=[
            'ciscosparkapi',
            'ciscosparkapi.api',
    ],

    install_requires=[
            'future',
            'requests>=2.4.2',
            'requests_toolbelt',
    ],
)
