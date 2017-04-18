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


class ResponseValidationMocks(object):

    @staticmethod
    def _valid_response_meta():
        return {
            "id": "12345",
            "collector_id": "12345",
            "survey_id": "12345",
            "analyze_url": "http://www.surveymonkey.com/analyze/browse/",
            "edit_url": "http://www.surveymonkey.com/r/",
            "href": "https://api.surveymonkey.net/v3/surveys/",
            "ip_address": "127.0.0.1",
            "response_status": "completed",
            "collection_mode": "default",
            "date_created": "2015-12-28T21:59:38+00:00",
            "date_modified": "2015-12-28T21:59:38+00:00",
        }

    @staticmethod
    def _valid_response_pages():
        return [{
            "id": "12345",
            "questions": [{
                "id": "12345",
                "answers": [{
                    "other_id": "12345",
                    "text": "This is my other text"
                }]
            }]
        }]

    def valid_response(self):
        response_obj = self._valid_response_meta()
        response_obj["pages"] = self._valid_response_pages()
        return response_obj

    @all_requests
    def invalid_json_content(self, url, request):
        headers = create_quota_headers()
        content = "{'message': ['this isn't valid': None]]"

        return response(200, content, headers)

    @all_requests
    def does_not_match_schema(self, url, request):
        headers = create_quota_headers()
        content = {
            "error": "Does not match schema"
        }

        return response(200, content, headers)

    @all_requests
    def invalid_analyze_url(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["analyze_url"] = "http://example.com"

        return response(200, content, headers)

    @all_requests
    def invalid_edit_url(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["edit_url"] = "http://example.com"

        return response(200, content, headers)

    @all_requests
    def invalid_href_url(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["href"] = "http://example.com"

        return response(200, content, headers)

    @all_requests
    def response_status_unknown(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        # Set our response status to an invalid value
        content["response_status"] = "unknown"

        return response(200, content, headers)

    @all_requests
    def remove_text_from_answer_type_other(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        del content["pages"][0]["questions"][0]["answers"][0]["text"]

        return response(200, content, headers)

    @all_requests
    def choice_col_row_answer(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["pages"][0]["questions"][0]["answers"][0] = {
            "col_id": "12345", "choice_id": "12345", "row_id": "12345"
        }

        return response(200, content, headers)

    @all_requests
    def choice_only_answer(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["pages"][0]["questions"][0]["answers"][0] = {"choice_id": "12345"}

        return response(200, content, headers)

    @all_requests
    def choice_row_answer(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["pages"][0]["questions"][0]["answers"][0] = {
            "row_id": "12345", "choice_id": "12345"
        }

        return response(200, content, headers)

    @all_requests
    def text_only_answer(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["pages"][0]["questions"][0]["answers"][0] = {"text": "This is some text"}

        return response(200, content, headers)

    @all_requests
    def text_and_row_answer(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["pages"][0]["questions"][0]["answers"][0] = {
            "text": "This is some text",
            "row_id": "12345"
        }

        return response(200, content, headers)

    @all_requests
    def text_and_content_type_answer(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["pages"][0]["questions"][0]["answers"][0] = {
            "text": "ui-previewer-demo.gif",
            "content_type": "image/gif"
        }

        return response(200, content, headers)

    @all_requests
    def answer_is_empty_dict(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["pages"][0]["questions"][0]["answers"][0] = {}

        return response(200, content, headers)

    @all_requests
    def answer_is_multiple(self, url, request):
        headers = create_quota_headers()
        content = self.valid_response()
        content["pages"][0]["questions"][0]["answers"].append({
            "text": "this is another answer"
        })

        return response(200, content, headers)
