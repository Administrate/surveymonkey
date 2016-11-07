# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

from httmock import urlmatch, response
from surveymonkey.tests.mocks.utils import create_quota_headers, BaseListMock

from surveymonkey.constants import URL_SURVEYS_LIST

from surveymonkey.tests.conftest import faker as faker_fixture
faker = faker_fixture()


class SurveyListMock(BaseListMock):

    def __init__(self, total=125, base_url=URL_SURVEYS_LIST):
        super(SurveyListMock, self).__init__(total=total, base_url=base_url)

    def create_surveys(self, per_page, current_page, pages):
        surveys = []
        fake = faker
        remaining = self.calculate_number_remaining(per_page, current_page)

        if remaining > 0:
            remaining = remaining if remaining < per_page else per_page
            for x in range(0, remaining):
                id = fake.password(
                    length=8,
                    digits=True,
                    upper_case=True,
                    special_chars=False,
                    lower_case=False
                )
                data = {
                    "href": "{base_url}/{id}".format(base_url=self.base_url, id=id),
                    "id": id,
                    "title": fake.catch_phrase()
                }
                surveys.append(data)

        return surveys

    @urlmatch(path="/v3/surveys")
    def surveys(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages = self.parse_url(url)

        links = self.get_links(per_page, current_page, pages)
        data = self.create_surveys(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "data": data,
            "links": links
        }

        return response(200, content, headers)
