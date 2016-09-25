#!/usr/bin/env python
#  -*- coding: utf-8 -*-
""" Script to demostrate the use of ciscosparkapi for the people API

The package natively retrieves your Spark access token from the
SPARK_ACCESS_TOKEN environment variable.  You must have this environment
variable set to run this script.

"""


from __future__ import print_function
from ciscosparkapi import CiscoSparkAPI


api = CiscoSparkAPI()    # Create a CiscoSparkAPI connection object; uses your SPARK_ACCESS_TOKEN


# Get my user information
print("Get my information ...")
me = api.people.me()
print(me)

# Get my user information using id
print("Get my information but using id ...")
me_by_id = api.people.get(me.id)
print(me_by_id)

# Get my user information using id
print("Get the list of people I know ...")
people = api.people.list(displayName="Jose") # Creates a generator container (iterable) that lists the people I know
for person in people:
    print(person.displayName) # Return the displayName of every person found
