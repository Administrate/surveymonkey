# -*- coding: utf-8 -*-

import random

from faker import Faker
from httmock import all_requests, response
from .utils import create_quota_headers

from surveymonkey.constants import API_URL


class MessagesMock(object):

    def __init__(self, config):
        self.fake = Faker()
        self.config = {}
        self.id = "%s" % random.randint(12345, 67890)

        default_config = (
            ("status", "not_sent"),
            ("body", "<html>...</html>"),
            ("recipient_status", None),
            ("is_branding_enabled", True),
            ("href", "This survey is currently closed."),
            ("href", "{base}/collectors/{collector_id}/messages/{id}".format(
                base=API_URL,
                collector_id=random.randint(1234, 567890),
                id=self.id
            )),
            ("is_scheduled", False),
            ("scheduled_date", None),
            ("date_created", self.fake.iso8601(tzinfo=None)),
            ("type", "invite"),
            ("id", self.id),
            ("subject", "We want your opinion"),
            ("name", "New Collector"),
        )

        for key, value in default_config:
            self.config[key] = getattr(config, key) if hasattr(config, key) else value

    @all_requests
    def create(self, url, request):
        headers = create_quota_headers()
        content = self.config
        return response(200, content, headers)
