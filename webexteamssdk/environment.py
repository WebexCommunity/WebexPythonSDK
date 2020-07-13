# -*- coding: utf-8 -*-
"""Package environment variables.

Copyright (c) 2016-2020 Cisco and/or its affiliates.

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


import os
import warnings

from .config import (
    ACCESS_TOKEN_ENVIRONMENT_VARIABLE,
    LEGACY_ACCESS_TOKEN_ENVIRONMENT_VARIABLES,
)


# Helper Functions
def _get_access_token():
    """Attempt to get the access token from the environment.

    Try using the current and legacy environment variables. If the access token
    is found in a legacy environment variable, raise a deprecation warning.

    Returns:
        The access token found in the environment (str), or None.
    """
    access_token = os.environ.get(ACCESS_TOKEN_ENVIRONMENT_VARIABLE)
    if access_token:
        return access_token

    else:
        for access_token_variable in LEGACY_ACCESS_TOKEN_ENVIRONMENT_VARIABLES:
            access_token = os.environ.get(access_token_variable)
            if access_token:
                env_var_deprecation_warning = PendingDeprecationWarning(
                    "Use of the `{legacy}` environment variable will be "
                    "deprecated in the future.  Please update your "
                    "environment(s) to use the new `{new}` environment "
                    "variable.".format(
                        legacy=access_token,
                        new=ACCESS_TOKEN_ENVIRONMENT_VARIABLE,
                    )
                )
                warnings.warn(env_var_deprecation_warning)
                return access_token


# Package Environment Variables
WEBEX_TEAMS_ACCESS_TOKEN = _get_access_token()
