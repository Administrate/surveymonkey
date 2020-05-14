# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

from random import randint

from httmock import urlmatch, response
from surveymonkey.tests.mocks.utils import create_quota_headers, BaseListMock

from surveymonkey.constants import URL_FOLDERS_LIST

from surveymonkey.tests.conftest import faker


class FolderListMock(BaseListMock):

    def __init__(self, total=125, base_url=URL_FOLDERS_LIST):
        super(FolderListMock, self).__init__(total=total, base_url=base_url)

    def create_folders(self, per_page, current_page, pages):
        folders = []
        remaining = self.calculate_number_remaining(per_page, current_page)

        if remaining > 0:
            remaining = remaining if remaining < per_page else per_page
            for x in range(0, remaining):
                id = faker.password(
                    length=7,
                    digits=True,
                    upper_case=False,
                    special_chars=False,
                    lower_case=False
                )
                data = {
                    "href": "{base_url}/{id}".format(base_url=self.base_url, id=id),
                    "id": id,
                    "title": faker.catch_phrase(),
                    "num_surveys": randint(1, 9)
                }
                folders.append(data)

        return folders

    @urlmatch(path="/v3/survey_folders")
    def folders(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages = self.parse_url(url)

        links = self.get_links(per_page, current_page, pages)
        data = self.create_folders(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "data": data,
            "links": links
        }

        return response(200, content, headers)

    @urlmatch(path='/v3/survey_folders')
    def folders_no_data(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages = self.parse_url(url)

        links = self.get_links(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "links": links
        }

        return response(200, content, headers)

    @urlmatch(path='/v3/survey_folders')
    def folders_no_links(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages = self.parse_url(url)

        data = self.create_folders(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "data": data
        }

        return response(200, content, headers)
