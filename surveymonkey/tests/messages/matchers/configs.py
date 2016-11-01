# -*- coding: utf-8 -*-

from expects.matchers import Matcher
from surveymonkey.messages.configs import is_invite


class BeInvite(Matcher):
    def _match(self, configuration):
        return is_invite(configuration.type), []


be_invite = BeInvite()

__all__ = ['be_invite']
