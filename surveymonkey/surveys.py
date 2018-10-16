# -*- coding: utf-8 -*-
from __future__ import absolute_import

from surveymonkey.manager import BaseManager
from surveymonkey.constants import URL_SURVEYS_LIST, URL_SURVEYS_DETAIL


class Surveys(BaseManager):

    def surveys(self, page=None, per_page=50, max_pages=100, folder_id=None):
        if page:
            response = self.get(
                base_url=URL_SURVEYS_LIST,
                page=page,
                per_page=per_page,
                folder_id=folder_id
            )
            self.verify_list_data(response)
            return response["data"]
        else:
            # If no page specified assume they want all surveys
            next_url = self.build_url(
                URL_SURVEYS_LIST,
                page=1,
                per_page=per_page,
                folder_id=folder_id
            )
            return self.get_list(next_url=next_url, max_pages=max_pages)

    def by_id(self, survey_id):
        url = URL_SURVEYS_DETAIL.format(survey_id=survey_id)
        return self.get(url)
