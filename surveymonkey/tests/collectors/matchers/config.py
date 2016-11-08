# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects.matchers import Matcher
from surveymonkey.collectors.configs import is_email, is_weblink


class BeEmail(Matcher):
    def _match(self, configuration):
        return is_email(configuration.type), []


class BeWeblink(Matcher):
    def _match(self, configuration):
        return is_weblink(configuration.type), []


be_email = BeEmail()
be_weblink = BeWeblink()

__all__ = ['be_email', 'be_weblink']
