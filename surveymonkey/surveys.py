# -*- coding: utf-8 -*-

from .manager import BaseManager
from .constants import URL_SURVEYS_LIST


class Surveys(BaseManager):

    def surveys(self, page=None, per_page=50, max_pages=100):
        if page:
            return self.get(base_url=URL_SURVEYS_LIST, page=page, per_page=per_page)["data"]
        else:
            # If no page specified assume they want all surveys
            next_url = self.build_url(URL_SURVEYS_LIST, page=1, per_page=per_page)
            return self.get_list(next_url=next_url, max_pages=max_pages)
