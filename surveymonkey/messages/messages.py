# -*- coding: utf-8 -*-

from ..manager import BaseManager
from ..constants import URL_MESSAGE_CREATE


class Message(BaseManager):

    def __init__(self, connection, collector, config=None):
        super(Message, self).__init__(connection)
        self.config = config
        self.collector_id = collector

    def build_url(self, url, *args, **kwargs):
        url = url.format(
            collector_id=self.collector_id
        )
        return super(Message, self).build_url(url, *args, **kwargs)

    def create(self):
        return self.post(
            base_url=URL_MESSAGE_CREATE,
            data={"type": self.config.type}
        )
