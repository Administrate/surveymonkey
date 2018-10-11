# -*- coding: utf-8 -*-
from __future__ import absolute_import

from surveymonkey.manager import BaseManager
from surveymonkey.constants import URL_FOLDERS_LIST


class Folders(BaseManager):

    def folders(self, page=None, per_page=50, max_pages=100):
        if page:
            return self._get_page_of_folders(page, per_page)
        else:
            return self._get_all_folders(per_page, max_pages)

    def _get_all_folders(self, per_page, max_pages):
        next_url = self.build_url(URL_FOLDERS_LIST, page=1, per_page=per_page)
        return self.get_list(next_url=next_url, max_pages=max_pages)

    def _get_page_of_folders(self, page, per_page):
        response = self.get(base_url=URL_FOLDERS_LIST, page=page, per_page=per_page)
        self.verify_list_data(response)
        return response["data"]
