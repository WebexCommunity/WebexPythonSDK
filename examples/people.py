#!/usr/bin/env python
#  -*- coding: utf-8 -*-
""" Script to demonstrate the use of ciscosparkapi for the people API

The package natively retrieves your Spark access token from the
SPARK_ACCESS_TOKEN environment variable.  You must have this environment
variable set to run this script.

"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *


__author__ = "Jose Bogarín Solano"
__author_email__ = "jose@bogarin.co.cr"
__contributors__ = ["Chris Lunsford <chrlunsf@cisco.com>"]
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


from ciscosparkapi import CiscoSparkAPI


api = CiscoSparkAPI()                           # Create a CiscoSparkAPI connection object; uses your SPARK_ACCESS_TOKEN environment variable


# Get my user information
print("Get my information ...")
me = api.people.me()
print(me)


# Get my user information using my id
print("Get my information but using id ...")
me_by_id = api.people.get(me.id)
print(me_by_id)


# Get my user information using id
print("Get the list of people I know...")
people = api.people.list(displayName="Jose")    # Creates a generator container (iterable) that lists the people I know
for person in people:
    print(person.displayName)                   # Return the displayName of every person found
