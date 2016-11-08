# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random

from httmock import all_requests, response
from surveymonkey.tests.utils import weighted_choice
from surveymonkey.tests.mocks.utils import create_quota_headers, BaseListMock

from surveymonkey.collectors.configs import is_email
from surveymonkey.constants import (API_URL, BASE_URL, URL_COLLECTOR_CREATE, URL_COLLECTOR_SINGLE,
                                    URL_COLLECTOR_RESPONSES)
from surveymonkey.responses.constants import COMPLETED, PARTIAL, OVERQUOTA, DISQUALIFIED

from surveymonkey.tests.conftest import faker as faker_fixture
faker = faker_fixture()


class CollectorMock(object):

    def __init__(self, config):
        self.fake = faker
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
        self.fake = faker
        url = base_url.format(
            survey_id=survey_id
        )
        super(CollectorsListMock, self).__init__(total=total, base_url=url)

    def create_item(self):
        id = self.fake.password(
            length=8,
            digits=True,
            upper_case=True,
            special_chars=False,
            lower_case=False
        )
        return {
            "href": "{base_url}/{id}".format(base_url=URL_COLLECTOR_SINGLE, id=id),
            "id": id,
            "name": self.fake.catch_phrase()
        }

    @all_requests
    def list(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages = self.parse_url(url)

        links = self.get_links(per_page, current_page, pages)
        data = self.create_items(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "data": data,
            "links": links
        }

        return response(200, content, headers)


class CollectorResponsesBulkListMock(BaseListMock):

    def __init__(self, total, status=None, config={}):
        self.collector_id = random.randint(1234, 567890)
        self.status = status
        self.config = config
        self.survey_id = random.randint(1234, 567890)
        self.fake = faker
        base_url = URL_COLLECTOR_RESPONSES.format(collector_id=self.collector_id)

        super(CollectorResponsesBulkListMock, self).__init__(total=total, base_url=base_url)

    def get_status(self):
        if self.status:
            return self.status

        return weighted_choice(
            [(COMPLETED, 20), (PARTIAL, 70), (OVERQUOTA, 5), (DISQUALIFIED, 5)]
        )

    def create_item(self):
        response_id = random.randint(123456, 34567890)
        uid = self.fake.password(
            length=20,
            digits=True,
            upper_case=True,
            special_chars=False,
            lower_case=False
        )

        href = "{api_url}/surveys/{survey_id}/responses/{response_id}".format(
            api_url=API_URL,
            survey_id=self.survey_id,
            response_id=response_id
        )
        analyze_url = "{base_url}/analyze/browse/{uid}?respondent_id={response_id}".format(
            base_url=BASE_URL,
            uid=uid,
            response_id=response_id
        )
        edit_url = "{base_url}/r/?sm={uid}".format(
            base_url=BASE_URL,
            uid=uid
        )

        return {
            "total_time": 12,
            "href": href,
            "custom_variables": self.config.get("custom_variables", {}),
            "ip_address": "87.246.78.46",
            "id": response_id,
            "logic_path": {},
            "date_modified": self.fake.iso8601(tzinfo=None),
            "response_status": self.get_status(),
            "custom_value": self.config.get("custom_value", ""),
            "analyze_url": analyze_url,
            "pages": [],
            "page_path": [],
            "recipient_id": "",
            "collector_id": self.collector_id,
            "date_created": self.fake.iso8601(tzinfo=None),
            "survey_id": self.survey_id,
            "collection_mode": "default",
            "edit_url": edit_url,
            "metadata": self.config.get("metadata", {})
        }

    @all_requests
    def bulk(self, url, request):
        headers = create_quota_headers()
        per_page, current_page, pages = self.parse_url(url)

        links = self.get_links(per_page, current_page, pages)
        data = self.create_items(per_page, current_page, pages)

        content = {
            "per_page": per_page,
            "total": self.total,
            "page": current_page,
            "data": data,
            "links": links
        }

        return response(200, content, headers)


class CollectorGetMock(object):

    def __init__(self, collector_id=random.randint(1234, 567890), type="weblink"):
        self.fake = faker
        self.collector_id = collector_id
        self.type = type

    @all_requests
    def by_id(self, url, request):
        headers = create_quota_headers()
        content = {
          "status": "open",
          "id": self.collector_id,
          "type": self.type,
          "name": "My Collector",
          "thank_you_message": "Thank you for taking my survey.",
          "disqualification_message": "Thank you for taking my survey.",
          "close_date": self.fake.iso8601(tzinfo=None),
          "closed_page_message": "This survey is currently closed.",
          "redirect_url": "https://www.surveymonkey.com",
          "display_survey_results": False,
          "edit_response_type": "until_complete",
          "anonymous_type": "not_anonymous",
          "allow_multiple_responses": False,
          "date_modified": self.fake.iso8601(tzinfo=None),
          "url": "https://www.surveymonkey.com/r/2Q3RXZB",
          "date_created": "2015-10-06T12:56:55+00:00",
          "sender_email": None,
          "password_enabled": False,
          "href": "{base_url}/{id}".format(base_url=URL_COLLECTOR_SINGLE, id=self.collector_id)
        }

        return response(200, content, headers)
