# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects.matchers import Matcher
from surveymonkey.responses.constants import COMPLETED, PARTIAL, OVERQUOTA, DISQUALIFIED


class BeCompleted(Matcher):
    def _match(self, response):
        return response["response_status"] == COMPLETED, []


class BePartial(Matcher):
    def _match(self, response):
        return response["response_status"] == PARTIAL, []


class BeOverquota(Matcher):
    def _match(self, response):
        return response["response_status"] == OVERQUOTA, []


class BeDisqualified(Matcher):
    def _match(self, response):
        return response["response_status"] == DISQUALIFIED, []


be_completed = BeCompleted()
be_partial = BePartial()
be_overquota = BeOverquota()
be_disqualified = BeDisqualified()

__all__ = ['be_completed', 'be_partial', 'be_overquota', 'be_disqualified']
