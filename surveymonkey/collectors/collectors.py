# -*- coding: utf-8 -*-
from __future__ import absolute_import

from furl import furl
from surveymonkey.manager import BaseManager
from surveymonkey.constants import (URL_COLLECTOR_CREATE, URL_COLLECTOR_RESPONSES_BULK,
                                    URL_SURVEY_RESPONSES_BULK, URL_COLLECTOR_SINGLE)


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
            data=self.config.vars(),
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
        self.survey_id = survey_id
        self.url = URL_SURVEY_RESPONSES_BULK if self.is_multi else URL_COLLECTOR_RESPONSES_BULK

        if self.is_multi and not self.survey_id:
            raise AttributeError("Multiple collectors requested with no survey id")

    def build_url(self, url, *args, **kwargs):
        if self.is_multi:
            url = furl(url.format(survey_id=self.survey_id))
            url.args["collector_ids"] = ",".join(self.collector_ids)
            url = url.url
        else:
            url = url.format(collector_id=self.collector_ids)

        return super(CollectorResponsesBulk, self).build_url(url, *args, **kwargs)

    def responses(self):
        next_url = self.build_url(self.url, page=1)
        return self.get_list(next_url=next_url)

    def completed(self):
        url = self.build_url(self.url, page=1)
        next_url = "%s&status=completed" % url
        return self.get_list(next_url=next_url)

    def partial(self):
        url = self.build_url(self.url, page=1)
        next_url = "%s&status=partial" % url
        return self.get_list(next_url=next_url)

    def overquota(self):
        url = self.build_url(self.url, page=1)
        next_url = "%s&status=overquota" % url
        return self.get_list(next_url=next_url)

    def disqualified(self):
        url = self.build_url(self.url, page=1)
        next_url = "%s&status=disqualified" % url
        return self.get_list(next_url=next_url)
