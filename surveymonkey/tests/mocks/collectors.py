# -*- coding: utf-8 -*-

import random

from faker import Faker
from httmock import all_requests, response
from .utils import create_quota_headers

from .utils import BaseListMock
from surveymonkey.collectors.configs import is_email
from surveymonkey.constants import URL_COLLECTOR_CREATE, URL_COLLECTOR_SINGLE


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


class CollectorsListMock(BaseListMock):

    def __init__(self, total, survey_id, base_url=URL_COLLECTOR_CREATE):
        url = base_url.format(
            survey_id=survey_id
        )
        super(CollectorsListMock, self).__init__(total=total, base_url=url)

    def create_collectors(self, per_page, current_page, pages):
        collectors = []
        fake = Faker()
        remaining = self.calculate_number_remaining(per_page, current_page)

        if remaining > 0:
            remaining = remaining if remaining < per_page else per_page
            for x in range(0, remaining):
                id = fake.password(
                    length=8,
                    digits=True,
                    upper_case=True,
                    special_chars=False,
                    lower_case=False
                )
                data = {
                    "href": "{base_url}/{id}".format(base_url=URL_COLLECTOR_SINGLE, id=id),
                    "id": id,
                    "name": fake.catch_phrase()
                }
                collectors.append(data)

        return collectors

    @all_requests
    def list(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages = self.parse_url(url)

        links = self.get_links(per_page, current_page, pages)
        data = self.create_collectors(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "data": data,
            "links": links
        }

        return response(200, content, headers)
