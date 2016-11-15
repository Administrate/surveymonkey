# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

import random
from httmock import all_requests, response
from surveymonkey.tests.mocks.utils import create_quota_headers

from surveymonkey.tests.conftest import faker as faker_fixture
faker = faker_fixture()


class ResponseGetMock(object):

    def __init__(self, survey_id=random.randint(1234, 567890), response_id=random.randint(1234, 567890)):  # noqa:E501
        self.fake = faker
        self.survey_id = survey_id
        self.response_id = response_id

    @all_requests
    def by_id(self, url, request):
        headers = create_quota_headers()
        content = {
            "total_time": 144,
            "ip_address": "192.168.4.16",
            "recipient_id": "",
            "id": "5007154402",
            "logic_path": {},
            "metadata": {},
            "date_modified": "2015-12-28T21:59:38+00:00",
            "response_status": "completed",
            "custom_variables": {
                "custvar_1": "one",
                "custvar_2": "two"
            },
            "custom_value": "custom identifier for the response",
            "edit_url": "https://www.surveymonkey.com/r/",
            "analyze_url": "https://www.surveymonkey.com/analyze/browse/",
            "page_path": [],
            "pages": [{
                "id": "103332310",
                "questions": [{
                    "answers": [{
                        "choice_id": "3057839051"
                    }],
                    "id": "319352786"
                }]
            }],
            "collector_id": "50253690",
            "date_created": "2015-12-28T21:57:14+00:00",
            "survey_id": "105724755",
            "collection_mode": "default"
        }
        return response(200, content, headers)
