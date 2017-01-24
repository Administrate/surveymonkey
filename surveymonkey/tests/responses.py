#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random

import requests
import pytest
from httmock import HTTMock
from expects import expect, have_keys, be_a

from surveymonkey.responses import Response
from surveymonkey.exceptions import SurveyMonkeyBadResponse
from surveymonkey.tests.mocks.responses import ResponseGetMock, ResponseValidationMocks
from surveymonkey.tests.utils import create_fake_connection


class TestGetResponse(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()
        self.response = Response(connection=self.connection)
        self.survey_id = random.randint(1234, 56789)
        self.response_id = random.randint(1234, 56789)
        self.mock = ResponseGetMock(self.survey_id, self.response_id)

    def test_get_single_response_by_id(self):
        with HTTMock(self.mock.by_id):
            response = self.response.by_id(
                survey_id=self.survey_id,
                response_id=self.response_id
            )

        expect(response).to(be_a(dict))
        expect(response).to(have_keys('id', 'response_status', 'pages'))


class TestResponseSchemaValidation(object):

    def setup_class(self):
        self.mocks = ResponseValidationMocks()

    def test_malformed_json_raises_bad_response(self):
        with HTTMock(self.mocks.invalid_json_content):
            response = requests.get('mocked://')
            with pytest.raises(SurveyMonkeyBadResponse):
                Response.verify_response_json(response)

    def test_json_which_doesnt_match_schema_raises_bad_response(self):
        with HTTMock(self.mocks.does_not_match_schema):
            response = requests.get('mocked://')
            with pytest.raises(SurveyMonkeyBadResponse):
                Response.verify_response_json(response)

    def test_invalid_analyze_url_raises_bad_response(self):
        with HTTMock(self.mocks.invalid_analyze_url):
            response = requests.get('mocked://')
            with pytest.raises(SurveyMonkeyBadResponse):
                Response.verify_response_json(response)

    def test_invalid_edit_url_raises_bad_response(self):
        with HTTMock(self.mocks.invalid_edit_url):
            response = requests.get('mocked://')
            with pytest.raises(SurveyMonkeyBadResponse):
                Response.verify_response_json(response)

    def test_invalid_href_url_raises_bad_response(self):
        with HTTMock(self.mocks.invalid_href_url):
            response = requests.get('mocked://')
            with pytest.raises(SurveyMonkeyBadResponse):
                Response.verify_response_json(response)

    def test_response_status_has_invalid_value(self):
        with HTTMock(self.mocks.response_status_unknown):
            response = requests.get('mocked://')
            with pytest.raises(SurveyMonkeyBadResponse):
                Response.verify_response_json(response)

    def test_other_answer_does_not_have_text(self):
        with HTTMock(self.mocks.remove_text_from_answer_type_other):
            response = requests.get('mocked://')
            with pytest.raises(SurveyMonkeyBadResponse):
                Response.verify_response_json(response)

    def test_choice_col_row_is_valid_answer_combination(self):
        with HTTMock(self.mocks.choice_col_row_answer):
            response = requests.get('mocked://')
            Response.verify_response_json(response)

    def test_just_choice_is_valid_answer(self):
        with HTTMock(self.mocks.choice_only_answer):
            response = requests.get('mocked://')
            Response.verify_response_json(response)

    def test_choice_and_row_is_valid_answer_combination(self):
        with HTTMock(self.mocks.choice_row_answer):
            response = requests.get('mocked://')
            Response.verify_response_json(response)

    def test_just_test_is_valid_answer(self):
        with HTTMock(self.mocks.text_only_answer):
            response = requests.get('mocked://')
            Response.verify_response_json(response)

    def test_text_and_row_is_valid_answer(self):
        with HTTMock(self.mocks.text_and_row_answer):
            response = requests.get('mocked://')
            Response.verify_response_json(response)

    def test_text_and_content_type_is_valid_answer(self):
        with HTTMock(self.mocks.text_and_content_type_answer):
            response = requests.get('mocked://')
            Response.verify_response_json(response)

    def test_answer_can_be_empty_dict(self):
        with HTTMock(self.mocks.answer_is_empty_dict):
            response = requests.get('mocked://')
            Response.verify_response_json(response)

    def test_answers_can_be_multiple(self):
        with HTTMock(self.mocks.answer_is_multiple):
            response = requests.get('mocked://')
            Response.verify_response_json(response)
