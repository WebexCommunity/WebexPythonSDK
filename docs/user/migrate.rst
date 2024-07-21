.. _Migrate:

.. currentmodule:: webexpythonsdk

=========
Migration
=========

This *should* 🤞 be easy!

``webexpythonsdk`` is designed to be a drop-in replacement for the ``webexteamssdk`` package. The SDK interface and data objects are largely unchanged with only a few minor name changes.

Major changes that you should be aware of:

* The package name has changed from ``webexteamssdk`` to ``webexpythonsdk``
* ``webexpythonsdk`` drops support for Python v2, and supports Python 3.10+
* The primary API object has changed from ``WebexTeamsAPI`` to ``WebexAPI``



---------------
Migration Guide
---------------

TL;DR: Update the package dependency, environment variables, imports, and primary API object.

The following table summarizes the name changes that need to be made to migrate from
``webexteamssdk`` to ``webexpythonsdk``:

+------------------------------+------------------------+-----------------------------------+
| Old Name                     | New Name               | Description                       |
+==============================+========================+===================================+
| ``webexteamssdk``            | ``webexpythonsdk``     | Package name                      |
+------------------------------+------------------------+-----------------------------------+
| ``WebexTeamsAPI``            | ``WebexAPI``           | Primary API object                |
+------------------------------+------------------------+-----------------------------------+
| ``WEBEX_TEAMS_ACCESS_TOKEN`` | ``WEBEX_ACCESS_TOKEN`` | Access token environment variable |
+------------------------------+------------------------+-----------------------------------+

*Note:* The old ``WEBEX_TEAMS_ACCESS_TOKEN`` environment variable should continue to work with the new package; however, you will receive a deprecation warning. It is recommended to update the environment variable name to ``WEBEX_ACCESS_TOKEN``.

**Doing a quick search-and-replace in your codebase should be all you need to do to migrate.**

Detailed Steps
--------------

1.  Update Package

    Ensure you update the package in your project's dependencies:

    .. code-block:: bash

        pip uninstall webexteamssdk
        pip install webexpythonsdk


2.  Update Environment Variables

    If you are using the ``WEBEX_TEAMS_ACCESS_TOKEN`` environment variable, you will need to update it to ``WEBEX_ACCESS_TOKEN``.

3.  Codebase Changes

    **Imports:** Replace all imports from ``webexteamssdk`` to ``webexpythonsdk``.

    **Primary API Object:** Replace all instances of ``WebexTeamsAPI`` with ``WebexAPI``.

----------------
For Contributors
----------------

Project changes that you should be aware of:

- Tooling changes:
    - Using GitHub Actions for CI/CD
    - Using `poetry`_ for packaging and dependency management
    - Using `poetry-dynamic-versioning`_ for version management
    - Using `ruff`_ for linting and code formatting
    - Using `make`_ to automate common tasks
- The test suite environment variable names have changed:

    +-------------------------------------+-------------------------------+
    | Old Environment Variable            | New Environment Variable      |
    +=====================================+===============================+
    | ``WEBEX_TEAMS_ACCESS_TOKEN``        | ``WEBEX_ACCESS_TOKEN``        |
    +-------------------------------------+-------------------------------+
    | ``WEBEX_TEAMS_TEST_DOMAIN``         | ``WEBEX_TEST_DOMAIN``         |
    +-------------------------------------+-------------------------------+
    | ``WEBEX_TEAMS_TEST_ID_START``       | ``WEBEX_TEST_ID_START``       |
    +-------------------------------------+-------------------------------+
    | ``WEBEX_TEAMS_TEST_FILE_URL``       | ``WEBEX_TEST_FILE_URL``       |
    +-------------------------------------+-------------------------------+
    | ``WEBEX_TEAMS_GUEST_ISSUER_ID``     | ``WEBEX_GUEST_ISSUER_ID``     |
    +-------------------------------------+-------------------------------+
    | ``WEBEX_TEAMS_GUEST_ISSUER_SECRET`` | ``WEBEX_GUEST_ISSUER_SECRET`` |
    +-------------------------------------+-------------------------------+


*Copyright (c) 2016-2024 Cisco and/or its affiliates.*


.. _Webex: https://www.webex.com/products/teams/index.html
.. _developer.webex.com: https://developer.webex.com/
.. _issues: https://github.com/WebexCommunity/WebexPythonSDK/issues
.. _poetry: https://python-poetry.org/
.. _poetry-dynamic-versioning: https://github.com/mtkennerly/poetry-dynamic-versioning
.. _ruff: https://docs.astral.sh/ruff/
.. _make: https://www.gnu.org/software/make/