# -*- coding: utf-8 -*
from __future__ import absolute_import

from expects.matchers import Matcher


class BeAfter(Matcher):
    def __init__(self, start_date):
        self._start_date = start_date

    def _match(self, subject):
        return self._start_date < subject, []

    def __repr__(self):
        return 'be after {start}'.format(start=self._start_date)


be_after = BeAfter
