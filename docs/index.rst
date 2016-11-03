=============
ciscosparkapi
=============

-------------------------------------------------------------------------
Simple, lightweight, scalable Python API wrapper for the Cisco Spark APIs
-------------------------------------------------------------------------

Welcome to the docs!  ciscosparkapi is a *community developed* Pythonic
wrapping of the Cisco Spark APIs.  We represent all of the API components using
native Python tools.

* Authentication, session headers, and connection info --> Wrapped in a
  'connection object'
* API Calls --> Wrapped in native method (function) calls hierarchically
  structured underneath the 'connection object'
* Returned Spark Data Objects --> Wrapped and represented as native Python
  objects
* Returned Lists of Objects --> Wrapped and represented as iterable sequences
  yielding native Python objects

This makes working with the Cisco Spark APIs in Python a native and natural
experience.  You can easily interact with the Cisco Spark APIs in an
interactive Python session, quickly create some throw-away code that helps you
get something done in Spark, or you can leverage the API wrapper to cleanly add
Spark functionality to your project without having to write boilerplate code
for working with the Spark APIs.

*ciscosparkapi helps you get things done faster.*  We'll take care of the API
semantics, and you can focus on writing your code.

**What is Cisco Spark?**

    "Cisco Spark is where all your work lives.  Bring your teams together in a
     place that makes it easy to keep people and work connected."

Check out the official `Cisco Spark`_ website for more details and to create a
free account!

**Looking for the official Cisco Spark API docs?**

You can find them at `Spark for Developers`_ website.


User Docs
=========

.. toctree::
    :maxdepth: 2

    user/intro
    user/tutorial
    user/api


Developer Docs
==============

Full developer docs are *coming soon*.  For now, please see the contribution_
instructions on the ciscosparkapi_ GitHub page to get started.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


*Copyright (c) 2016 Cisco Systems, Inc.*


.. _Cisco Spark: https://www.ciscospark.com/
.. _Spark for Developers: https://developer.ciscospark.com/
.. _contribution: https://github.com/CiscoDevNet/ciscosparkapi#contribution
.. _ciscosparkapi: https://github.com/CiscoDevNet/ciscosparkapi
