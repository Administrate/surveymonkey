# -*- coding: utf-8 -*-

import random
from datetime import datetime

from faker import Faker
from httmock import all_requests, response
from .utils import create_quota_headers

from surveymonkey.collectors.configs import is_email


class CollectorMock(object):

    def __init__(self, config):
        self.fake = Faker()
        self.config = {}
        self.id = "%s" % random.randint(12345, 67890)

        default_config = (
            ("status", "new"),
            ("redirect_url", "https://example.com"),
            ("thank_you_message", "Thank you for completing our survey!"),
            ("response_count", 0),
            ("closed_page_message", "This survey is currently closed."),
            ("href", "https://api.surveymonkey.net/v3/collectors/{id}".format(id=self.id)),
            ("close_date", None),
            ("display_survey_results", False),
            ("allow_multiple_responses", False),
            ("anonymous_type", "not_anonymous"),
            ("id", self.id),
            ("password_enabled", False),
            ("name", "New Collector"),
            ("date_modified", self.fake.iso8601(tzinfo=None)),
            ("url", None),
            ("edit_response_type", "until_complete"),
            ("sender_email", self.fake.safe_email()),
            ("date_created", self.fake.iso8601(tzinfo=None)),
            ("disqualification_message", "Thank you for completing our survey!"),
            ("type", "email" if is_email(config.type) else "weblink")
        )

        for key, value in default_config:
            self.config[key] = getattr(config, key) if hasattr(config, key) else value

    @all_requests
    def create(self, url, request):
        headers = create_quota_headers()
        content = self.config

        return response(200, content, headers)
