#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

import ciscosparkapi


class TestPackage:
    """Test the ciscosparkapi package-level code."""

    def test_creating_a_new_ciscosparkapi_object_without_an_access_token_raises_an_exception(self):
        at = os.environ.get(ciscosparkapi.ACCESS_TOKEN_ENVIRONMENT_VARIABLE)
        del os.environ[ciscosparkapi.ACCESS_TOKEN_ENVIRONMENT_VARIABLE]

        with pytest.raises(ciscosparkapi.ciscosparkapiException):
            connection_object = ciscosparkapi.CiscoSparkAPI()

        os.environ[ciscosparkapi.ACCESS_TOKEN_ENVIRONMENT_VARIABLE] = at

    def test_creating_a_new_ciscosparkapi_object_via_access_token_argument(self):
        at = os.environ.get(ciscosparkapi.ACCESS_TOKEN_ENVIRONMENT_VARIABLE)
        del os.environ[ciscosparkapi.ACCESS_TOKEN_ENVIRONMENT_VARIABLE]

        connection_object = ciscosparkapi.CiscoSparkAPI(access_token=at)
        assert connection_object

        os.environ[ciscosparkapi.ACCESS_TOKEN_ENVIRONMENT_VARIABLE] = at

    def test_creating_a_new_ciscosparkapi_object_via_environment_varable(self):
        connection_object = ciscosparkapi.CiscoSparkAPI()
        assert connection_object
