# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

import random
from httmock import urlmatch, response
from surveymonkey.tests.mocks.utils import create_quota_headers, BaseListMock

from surveymonkey.constants import URL_SURVEYS_LIST

from surveymonkey.tests.conftest import faker


class SurveyListMock(BaseListMock):

    def __init__(self, total=125, base_url=URL_SURVEYS_LIST):
        super(SurveyListMock, self).__init__(total=total, base_url=base_url)

    def create_surveys(self, per_page, current_page, pages):
        surveys = []
        remaining = self.calculate_number_remaining(per_page, current_page)

        if remaining > 0:
            remaining = remaining if remaining < per_page else per_page
            for x in range(0, remaining):
                id = faker.password(
                    length=8,
                    digits=True,
                    upper_case=True,
                    special_chars=False,
                    lower_case=False
                )
                data = {
                    "href": "{base_url}/{id}".format(base_url=self.base_url, id=id),
                    "id": id,
                    "title": faker.catch_phrase()
                }
                surveys.append(data)

        return surveys

    @urlmatch(path="/v3/surveys")
    def surveys(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages, folder_id = self.parse_url_with_folder(url)

        links = self.get_links(per_page, current_page, pages, folder_id)
        data = self.create_surveys(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "data": data,
            "links": links
        }

        return response(200, content, headers)

    @urlmatch(path='/v3/surveys')
    def surveys_no_data(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages, folder_id = self.parse_url_with_folder(url)

        links = self.get_links(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "links": links
        }

        return response(200, content, headers)

    @urlmatch(path='/v3/surveys')
    def surveys_no_links(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages, folder_id = self.parse_url_with_folder(url)

        data = self.create_surveys(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "data": data
        }

        return response(200, content, headers)


class SurveyGetMock(object):

    def __init__(self, survey_id=random.randint(1234, 567890)):
        self.survey_id = survey_id

    @urlmatch(path='/v3/surveys')
    def by_id(self, url, request):
        headers = create_quota_headers()
        content = {
            "title": faker.catch_phrase(),
            "nickname": "",
            "custom_variables": {
                "name": "label"
            },
            "language": "en",
            "question_count": random.randint(1, 20),
            "page_count": random.randint(1, 20),
            "date_created": faker.iso8601(tzinfo=None),
            "date_modified": faker.iso8601(tzinfo=None),
            "id": self.survey_id,
            "pages": [{
              "questions": [{}]
            }],
            "buttons_text": {
                "done_button": "Done",
                "prev_button": "Prev",
                "exit_button": "Exit",
                "next_button": "Next"
            },
            "preview": "https://www.surveymonkey.com/r/Preview/",
            "edit_url": "https://www.surveymonkey.com/create/",
            "collect_url": "https://www.surveymonkey.com/collect/list",
            "analyze_url": "http://www.surveymonkey.com/analyze/3bOmrM5mtfgBEcubFSDvR_2FbJ_2BrGx0E4aEBPKvsYFo9E_3D",  # noqa:E501
            "summary_url": "https://www.surveymonkey.com/summary/"
        }

        return response(200, content, headers)
