#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects import expect, equal
from surveymonkey.surveymonkey import BaseConfig


class TestBaseConfig(object):

    def test_base_config_accepts_arbitrary_values(self):
        config = BaseConfig(
            company="Administrate"
        )

        expect(config.company).to(equal("Administrate"))
