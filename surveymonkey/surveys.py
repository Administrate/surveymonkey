# -*- coding: utf-8 -*-

from .manager import BaseManager
from .constants import URL_SURVEYS_LIST


class Surveys(BaseManager):

    def surveys(self, page=None, per_page=50, max_depth=100):
        if page:
            return self.get(base_url=URL_SURVEYS_LIST, page=page, per_page=per_page)["data"]
        else:
            # If no page specified assume they want all surveys
            guard = 0
            surveys = []
            next = self.build_url(URL_SURVEYS_LIST, page=1, per_page=per_page)

            while guard < max_depth and next:
                guard += 1
                response = self.get(base_url=next)
                surveys = surveys + response["data"]
                next = response["links"]["next"] if "next" in response["links"] else False

            return surveys
