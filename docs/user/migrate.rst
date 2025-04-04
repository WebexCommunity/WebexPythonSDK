.. _Migrate:

.. currentmodule:: webexpythonsdk

=========
Migration
=========

This *should* 🤞 be easy!

The transition from `webexteamssdk` to `webexpythonsdk` is not entirely a "drop-in replacement" due to substantial changes in class structures and functionalities. This guide aims to clarify these changes and offer solutions to ease the migration process.

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



**Doing a quick search-and-replace in your codebase will help when migrating.**

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

Key Changes For Adaptive Cards
------------------------------

Module and Class Changes
~~~~~~~~~~~~~~~~~~~~~~~~

The following table outlines the changes in module and class names:

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Old Module/Class
     - New Module/Class
     - Example Usage
   * - `webexteamssdk.models.cards.components.TextBlock`
     - `webexpythonsdk.models.cards.card_elements.TextBlock`
     - `TextBlock(color=Colors.light)`
   * - `webexteamssdk.models.cards.container.ColumnSet`
     - `webexpythonsdk.models.cards.containers.ColumnSet`
     - `ColumnSet(columns=[Column()])`
   * - `webexteamssdk.models.cards.components.Image`
     - `webexpythonsdk.models.cards.card_elements.Image`
     - `Image(url="https://example.com/image.jpg")`
   * - `webexteamssdk.models.cards.components.Choice`
     - `webexpythonsdk.models.cards.inputs.Choice`
     - `Choice(title="Option", value="option")`
   * - `webexteamssdk.models.cards.options.BlockElementHeight`
     - `webexpythonsdk.models.cards.options.BlockElementHeight`
     - `BlockElementHeight(height="stretch")`
   * - New Imports
     - `webexpythonsdk.models.cards.actions.OpenUrl`, `Submit`, `ShowCard`
     - `OpenUrl(url="https://example.com")`
   * - New Imports
     - `webexpythonsdk.models.cards.types.BackgroundImage`
     - `BackgroundImage(url="https://example.com/image.jpg")`

Enums and Case Sensitivity
~~~~~~~~~~~~~~~~~~~~~~~~~~

Attributes now require specific enums for values, which are case-sensitive. For example:

- **Previous**: `TextBlock.color = "Light"`
- **New**: `TextBlock.color = Colors.light`

Refer to the `Adaptive Cards TextBlock documentation <https://adaptivecards.io/explorer/TextBlock.html>`_ for valid enum values.

Compatibility Solutions
-----------------------

Wrapper Classes
~~~~~~~~~~~~~~~

To facilitate backward compatibility, consider using the following wrapper classes:

.. code-block:: python

   # Example wrapper for components.py
   from webexpythonsdk.models.cards.card_elements import TextBlock, Image
   from webexpythonsdk.models.cards.containers import Column, Fact

   # Example wrapper for container.py
   from webexpythonsdk.models.cards.containers import Container, ColumnSet, FactSet

Module Flag for Compatibility
-----------------------------

A module flag can be introduced to bypass the `validate_input` function where backward compatibility is needed. Ensure this flag is set before executing legacy code.

.. code-block:: python

   # Example usage
   webexpythonsdk.enable_backward_compatibility(True)

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