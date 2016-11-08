# -*- coding: utf-8 -*-
from __future__ import absolute_import

from surveymonkey.manager import BaseManager
from surveymonkey.constants import (URL_COLLECTOR_CREATE, URL_COLLECTOR_RESPONSES,
                                    URL_COLLECTOR_SINGLE)


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

    def by_id(self, collector_id):
        url = URL_COLLECTOR_SINGLE.format(collector_id=collector_id)
        return self.get(url)


class CollectorResponsesBulk(BaseManager):

    def __init__(self, connection, collector_ids, survey_id=None):
        super(CollectorResponsesBulk, self).__init__(connection)
        self.is_multi = isinstance(collector_ids, list)
        self.collector_ids = collector_ids
        self.url = URL_COLLECTOR_RESPONSES

    def build_url(self, url, *args, **kwargs):
        if self.is_multi:
            url = url.format(collector_id=kwargs.pop("collector_id"))
        else:
            url = url.format(collector_id=self.collector_ids)

        status = kwargs.get("status", None)
        url = "%s&status=%s" % (url, status) if status else url

        return super(CollectorResponsesBulk, self).build_url(url, *args, **kwargs)

    def responses(self, status=None):
        if self.is_multi:
            response = []
            for collector_id in self.collector_ids:
                data = self.get_list(
                    next_url=self.url,
                    page=1,
                    collector_id=collector_id,
                    status=status
                )
                response = response + data
        else:
            response = self.get_list(next_url=self.url, page=1, status=status)

        return response

    def completed(self):
        return self.responses(status="completed")

    def partial(self):
        return self.responses(status="partial")

    def overquota(self):
        return self.responses(status="overquota")

    def disqualified(self):
        return self.responses(status="disqualified")
