#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects import expect, equal, be_a
from surveymonkey.surveymonkey import BaseConfig


class TestBaseConfig(object):

    def test_base_config_accepts_arbitrary_values(self):
        config = BaseConfig(
            company="Administrate"
        )

        expect(config.company).to(equal("Administrate"))

    def test_base_config_var_returns_valid_dict_of_all_vars(self):
        custom_vars = {
            "company": "Administrate",
            "location": "Edinburgh"
        }
        config = BaseConfig(**custom_vars)
        config_vars = config.vars()

        expect(config_vars).to(be_a(dict))
        expect(config_vars).to(equal(custom_vars))
