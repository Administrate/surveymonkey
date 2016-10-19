# -*- coding: utf-8 -*-
from __future__ import division

from six.moves.urllib.parse import parse_qs

import math
from faker import Factory
from httmock import urlmatch, response
from .utils import create_quota_headers

from surveymonkey.constants import URL_SURVEYS_LIST


class SurveyListMock(object):

    def __init__(self, total=125, base_url=URL_SURVEYS_LIST):
        self.total = total
        self.base_url = base_url

    def get_links(self, per_page, current_page, pages):
        last_page = pages

        links = dict()
        links["self"] = "{base_url}?page={page}&per_page={per_page}".format(
            base_url=self.base_url,
            page=current_page,
            per_page=per_page
        )

        if last_page > 1:
            if current_page != last_page:
                links["last"] = "{base_url}?page={current_page}&per_page={per_page}".format(
                    base_url=self.base_url,
                    current_page=current_page,
                    per_page=per_page
                )
                if current_page < last_page:
                    links["next"] = "{base_url}?page={next_page}&per_page={per_page}".format(
                        base_url=self.base_url,
                        next_page=current_page + 1,
                        per_page=per_page
                    )
            if current_page != 1:
                links["first"] = "{base_url}?page=1&per_page={per_page}".format(
                    base_url=self.base_url,
                    per_page=per_page
                )
                links["prev"] = "{base_url}?page={prev_page}&per_page={per_page}".format(
                    base_url=self.base_url,
                    prev_page=current_page - 1,
                    per_page=per_page
                )

        return links

    def calculate_number_of_surveys_remaining(self, per_page, current_page):
        if current_page == 1:
            return self.total
        else:
            total_done = (current_page - 1) * per_page
            total_remaining = self.total - total_done
            return 0 if total_remaining <= 0 else total_remaining

    def create_surveys(self, per_page, current_page, pages):
        surveys = []
        fake = Factory.create()
        remaining = self.calculate_number_of_surveys_remaining(per_page, current_page)

        if remaining > 0:
            remaining = remaining if remaining < per_page else per_page
            for x in range(0, remaining):
                id = fake.password(length=8, digits=True)
                data = {
                    "href": "{base_url}/{id}".format(base_url=self.base_url, id=id),
                    "id": id,
                    "title": fake.catch_phrase()
                }
                surveys.append(data)

        return surveys

    def parse_url(self, url):
        qs = dict(parse_qs(url.query))

        per_page = int(qs.get("per_page", ['50'])[0])
        current_page = int(qs.get("page", ['1'])[0])
        pages = math.ceil(self.total / per_page)

        return per_page, current_page, pages

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
