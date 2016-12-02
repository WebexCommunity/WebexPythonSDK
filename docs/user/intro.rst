.. _Introduction:

============
Introduction
============

ciscosparkapi is a *community developed* Pythonic wrapping of the Cisco Spark
APIs.

*What do we mean by a 'Python wrapping' of the APIs?*

===============================  ==============================================
Cisco Spark API                  ciscosparkapi Package
===============================  ==============================================
Authentication, URLs, & headers  Wrapped in a simple :class:`CiscoSparkAPI`
                                 "connection object"
-------------------------------  ----------------------------------------------
API Endpoints & Calls            Wrapped and represented as native method /
                                 function calls hierarchically structured
                                 underneath the :class:`CiscoSparkAPI`
                                 "connection object"
-------------------------------  ----------------------------------------------
Returned Spark Data Objects      Wrapped and represented as native Python
                                 objects
-------------------------------  ----------------------------------------------
Returned Lists of Objects        Wrapped and represented as iterable sequences
                                 that yield the native Spark Data Objects
===============================  ==============================================

The idea is to enable you to work with the Cisco Spark APIs using native Python
objects and tools, such that you can focus on your code and not have to write
boiler-plate code to handle the API mechanics.

Head over to the :ref:`Quickstart` page to get started.

.. _License:

MIT License
-----------

ciscosparkapi is currently licensed under the `MIT Open Source License`_, and
distributed as a source distribution (no binaries) via :ref:`PyPI <Install>`,
and the complete :ref:`Source Code` is available on GitHub.

ciscosparkapi License
---------------------

.. include:: ../../LICENSE


.. _MIT Open Source License: https://opensource.org/licenses/MIT

*Copyright (c) 2016 Cisco Systems, Inc.*
