# -*- coding: utf-8 -*-
from __future__ import absolute_import

from surveymonkey.manager import BaseManager
from surveymonkey.constants import URL_RESPONSE_DETAIL


class Response(BaseManager):

    def by_id(self, survey_id, response_id):
        url = URL_RESPONSE_DETAIL.format(survey_id=survey_id, response_id=response_id)
        return self.get(url)
