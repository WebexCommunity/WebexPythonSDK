.. _Contributing:

============
Contributing
============

*webexpythonsdk* is a community development project.  Feedback, thoughts, ideas, and code contributions are most welcome!


How to contribute Feedback, Issues, Thoughts and Ideas
=======================================================

Please use the `issues`_ page to report issues or post ideas for enhancement.

Join our `Webex Python SDK - Python Community Contributors <https://eurl.io/#BJ0A8gfOQ>`_ Webex space to join the conversation with other contributors to this project.



Interested in Contributing Code?
================================


Developer Scripts
-----------------

We have created some scripts to automate everyday actions needed when working on the project.  Please see the `script`_ directory, and it's README for more information.


Notes on the Test Suite
-----------------------

To test all the API endpoints, the account that you use for testing must be an *admin* user for your Webex Organization.  Additionally, you should know that that the testing process creates some test people, rooms, messages, teams, and etc. as part of executing the test suite. We strongly recommend *NOT* running the test suite using your personal Webex account (not that you can't; it's just that you probably don't want it cluttering your account with all these test artifacts).

If you cannot create a test account with *admin* privileges or configure your environment to run the test suite locally, you may always submit your code via a pull request.  We will test your code before merging and releasing the changes.


Contributing Code
-----------------

1. Check for open `issues`_ or create a new *issue* for the item you want to work on and make sure to comment and let us know that you are working on it.

2. Fork a copy of the `repository`_ and clone your forked repository to your development environment.

3. Run ``script/setup`` to install the development dependencies and setup your environment.

4. Configure the following environment variables in your development environment:

   * ``WEBEX_ACCESS_TOKEN`` - Your test account's Webex access token.

5. Add your code to your forked repository.

   If you are creating some new feature or functionality (excellent!), please also write a `test`_ to verify that your code works as expected.

6. We follow `PEP8`_ reasonably strictly for this project.  Please make sure your code passes the linter.

   Run ``script/test lint`` or simply run ``flake8`` from the project root.

7. Commit your changes.

8. Submit a `pull request`_.


Running the Test Suite Locally
------------------------------

Configure the following environment variables in your development environment:

* ``WEBEX_ACCESS_TOKEN`` - Your test account's Webex access token.

* ``WEBEX_TEST_DOMAIN`` - The test suite creates some users as part of the testing process. The test suite uses this domain name as the e-mail suffix of for the user's e-mail addresses.

* ``WEBEX_TEST_ID_START`` - The test suite uses this integer as the starting number for creating test user accounts (example: "test42@domain.com").

* ``WEBEX_TEST_FILE_URL`` - Configure this environment variable with a URL referencing a file that can be downloaded and posted to Webex as part of the testing process.

*Example:*

.. code-block:: bash

   #!/usr/bin/env bash
   export WEBEX_ACCESS_TOKEN="<test account's access token>"
   export WEBEX_TEST_DOMAIN="domain.com"
   export WEBEX_TEST_ID_START=42
   export WEBEX_TEST_FILE_URL="https://www.webex.com/content/dam/wbx/us/images/navigation/CiscoWebex-Logo_white.png"

Ensure your code passes all of the default tests.  Run ``script/test`` and ensure all tests execute successfully.


.. _script: https://github.com/WebexCommunity/WebexPythonSDK/tree/master/script
.. _issues: https://github.com/WebexCommunity/WebexPythonSDK/issues
.. _repository: https://github.com/WebexCommunity/WebexPythonSDK
.. _test: https://github.com/WebexCommunity/WebexPythonSDK/tree/master/tests
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _pull request: https://github.com/WebexCommunity/WebexPythonSDK/pulls
