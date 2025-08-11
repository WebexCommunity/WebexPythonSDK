.. _Contributing:

============
Contributing
============

*webexpythonsdk* is a community development project.  Feedback, thoughts, ideas, and code contributions are most welcome!


How to contribute Feedback, Issues, Thoughts and Ideas
=======================================================

Please use the `issues`_ page to report issues or post ideas for enhancement.


Interested in Contributing Code?
================================


Common Developer Tasks
----------------------

See the project's `Makefile` targets for a list of common developer tasks, which you can run by simply running `make <target>` from the repository root directory.


Notes on the Test Suite
-----------------------

To test all the API endpoints, the account that you use for testing must be an *admin* and *compliance officer* user for your Webex Organization.  Additionally, you should know that that the testing process creates some test people, rooms, messages, teams, and etc. as part of executing the test suite.

We strongly recommend *NOT* running the test suite using your personal Webex account (not that you can't; it's just that you probably don't want it cluttering your account with all these test artifacts).

Webex now offers a free developer sandbox organization that you can use for testing purposes.  You can request the sandbox at https://developer.webex.com/docs/developer-sandbox-guide. Once you have your sandbox organization, you can create a test account with *admin* and *compliance officer* privileges via [Webex Control Hub](https://admin.webex.com) and use that account for testing. (Be sure to login to Control Hub with the new admin so that the roles are assigned properly to the Webex token.)

If you cannot create a test account with *admin* privileges or configure your environment to run the test suite locally, you may always submit your code via a pull request.  We will test your code before merging and releasing the changes.


Contributing Code
-----------------

1. Check for open `issues`_ or create a new *issue* for the item you want to work on and make sure to comment and let us know that you are working on it.

2. Fork a copy of the `repository`_ and clone your forked repository to your development environment.

3. Create a Python virtual environment and install the project dependencies.

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate

4. Use the ``setup`` target to install the project dependencies and setup your environment for development.

   .. code-block:: bash

      make setup

5. Install the SDK in Editable Mode.

   .. code-block:: bash

      pip install -e

5. Add your code to your forked repository.

   If you are creating some new feature or functionality (excellent!), please also write tests to verify that your code works as expected.

6. Please format your code and make sure your code passes the linter.

   .. code-block:: bash

      make format
      make lint

7. If you running the test suite locally, ensure your code passes all of the default tests.  Use the ``test`` target and ensure all tests execute successfully.

   .. code-block:: bash

      make tests

8. Commit your changes.

9. Submit a `pull request`_.


Running the Test Suite Locally
------------------------------

To run the test suite locally, you must configure the following environment variables in your development environment:

* ``WEBEX_ACCESS_TOKEN`` - Your test account's Webex access token.

* ``WEBEX_TEST_DOMAIN`` - The test suite creates some users as part of the testing process. The test suite uses this domain name as the e-mail suffix of for the user's e-mail addresses.
To ensure that the developer passes all tests, the developer should use the domain name of the sandbox organization that they have created.

* ``WEBEX_TEST_ID_START`` - The test suite uses this integer as the starting number for creating test user accounts (example: "test42@domain.com").

* ``WEBEX_TEST_FILE_URL`` - Configure this environment variable with a URL referencing a file that can be downloaded and posted to Webex as part of the testing process.

*Example:*

.. code-block:: bash

   #!/usr/bin/env bash
   export WEBEX_ACCESS_TOKEN="<test account's access token>"
   export WEBEX_TEST_DOMAIN="domain.com"
   export WEBEX_TEST_ID_START=42
   export WEBEX_TEST_FILE_URL="https://www.webex.com/content/dam/wbx/us/images/navigation/CiscoWebex-Logo_white.png"

If you are updating or testing the guest issuer functionality, you will also need to configure the following environment variables:

* ``WEBEX_GUEST_ISSUER_ID`` - The issuer ID for the guest issuer account.
* ``WEBEX_GUEST_ISSUER_SECRET`` - The issuer secret for the guest issuer account.


Ensure your code passes all of the default tests.  Run ``make test`` and ensure all tests execute successfully.


.. _script: https://github.com/WebexCommunity/WebexPythonSDK/tree/master/script
.. _issues: https://github.com/WebexCommunity/WebexPythonSDK/issues
.. _repository: https://github.com/WebexCommunity/WebexPythonSDK
.. _test: https://github.com/WebexCommunity/WebexPythonSDK/tree/master/tests
.. _pull request: https://github.com/WebexCommunity/WebexPythonSDK/pulls
