# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects.matchers import Matcher
from surveymonkey.messages.configs import is_invite, is_reminder


class BeInvite(Matcher):
    def _match(self, configuration):
        return is_invite(configuration.type), []


class BeReminder(Matcher):
    def _match(self, configuration):
        return is_reminder(configuration.type), []


be_invite = BeInvite()
be_reminder = BeReminder()

__all__ = ['be_invite', 'be_reminder']
