#  -*- coding: utf-8 -*-
"""Main entry point."""


__author__ = "Jose Bogarín Solano"
__author_email__ = "jose@bogarin.co.cr"
__contributors__ = ["Chris Lunsford <chrlunsf@cisco.com>"]
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("pyramidSparkBot.views")
    return config.make_wsgi_app()
