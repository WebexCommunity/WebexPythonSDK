"""A setuptools based setup module."""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ciscosparkapi',

    version='0.1',

    description='Simple, lightweight and scalable Python API wrapper for the '
                'Cisco Spark APIs',
    long_description=long_description,

    url='https://github.com/CiscoDevNet/ciscosparkapi',

    author='Chris Lunsford',
    author_email='chrlunsf@cisco.com',

    license='MIT',

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
        'Topic :: Communications',
        'Topic :: Communications :: Chat'
    ],

    keywords='cisco spark api enterprise messaging',

    packages='ciscosparkapi',
    install_requires=['requests>=2.4.2'],
)
