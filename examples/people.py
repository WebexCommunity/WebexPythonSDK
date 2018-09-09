#!/usr/bin/env python
#  -*- coding: utf-8 -*-
""" Script to demonstrate the use of webexteamssdk for the people API

The package natively retrieves your Webex Teams access token from the
WEBEX_TEAMS_ACCESS_TOKEN environment variable.  You must have this environment
variable set to run this script.

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

from webexteamssdk import WebexTeamsAPI


# Create a WebexTeamsAPI connection object; uses your WEBEX_TEAMS_ACCESS_TOKEN
# environment variable
api = WebexTeamsAPI()


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
# Creates a generator container (iterable) that lists the people I know
people = api.people.list(displayName="Jose")
# Return the displayName of every person found
for person in people:
    print(person.displayName)
