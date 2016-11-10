# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects.matchers import Matcher
from surveymonkey.messages.configs import is_invite, is_reminder


class BeInvite(Matcher):
    def _match(self, response):
        return is_invite(response["type"]), []


class BeReminder(Matcher):
    def _match(self, response):
        return is_reminder(response["type"]), []


class BeSent(Matcher):
    def _match(self, response):
        return "status" in response and response["status"] == "sent", []


be_invite = BeInvite()
be_reminder = BeReminder()
be_sent = BeSent()

__all__ = ['be_invite', 'be_reminder', 'be_sent']
