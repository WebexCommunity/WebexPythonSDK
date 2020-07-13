# -*- coding: utf-8 -*-
"""webexteamssdk setup module."""


import os
from codecs import open

from setuptools import find_packages, setup

import versioneer


__copyright__ = "Copyright (c) 2016-2020 Cisco and/or its affiliates."
__license__ = "MIT"


PACKAGE_NAME = 'webexteamssdk'

PACKAGE_KEYWORDS = [
    'cisco',
    'webex',
    'teams',
    'spark',
    'python',
    'api',
    'sdk',
    'enterprise',
    'messaging',
]

PACKAGE_CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
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
    'Programming Language :: Python :: 3.7',
    'Topic :: Communications',
    'Topic :: Communications :: Chat'
]

INSTALLATION_REQUIREMENTS = [
    'future',
    'requests>=2.4.2',
    'requests-toolbelt',
    'PyJWT'
]


project_root = os.path.abspath(os.path.dirname(__file__))


# Get package metadata
metadata = {}
with open(os.path.join(project_root, PACKAGE_NAME, '_metadata.py')) as f:
    exec(f.read(), metadata)


# Get the long description from the project's README.rst file
with open(os.path.join(project_root, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=PACKAGE_NAME,

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description=metadata['__description__'],
    long_description=long_description,

    url=metadata['__url__'],
    download_url=metadata['__download_url__'],

    author=metadata['__author__'],
    author_email=metadata['__author_email__'],

    license=metadata['__license__'] + '; ' + metadata['__copyright__'],

    classifiers=PACKAGE_CLASSIFIERS,

    keywords=" ".join(PACKAGE_KEYWORDS),

    packages=find_packages(include=[PACKAGE_NAME, PACKAGE_NAME + '.*']),

    install_requires=INSTALLATION_REQUIREMENTS,
)
