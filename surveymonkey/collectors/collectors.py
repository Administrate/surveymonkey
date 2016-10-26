# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

from ..manager import BaseManager
from ..constants import URL_COLLECTOR_CREATE


class Collector(BaseManager):

    def __init__(self, connection, config=None):
        super(Collector, self).__init__(connection)
        self.config = config

    def build_url(self, url, *args, **kwargs):
        url = url.format(
            survey_id=kwargs.get("survey_id")
        )
        return super(Collector, self).build_url(url, *args, **kwargs)

    def create(self, survey_id):
        return self.post(
            base_url=URL_COLLECTOR_CREATE,
            data={"type": self.config.type},
            survey_id=survey_id
        )

    def list(self, survey_id):
        next_url = self.build_url(URL_COLLECTOR_CREATE, page=1, survey_id=survey_id)
        return self.get_list(next_url=next_url)
