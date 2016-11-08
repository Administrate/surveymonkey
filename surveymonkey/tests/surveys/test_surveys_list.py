#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pytest
from httmock import HTTMock
from expects import expect, end_with, have_keys, have_length, contain

from surveymonkey.surveys import Surveys
from surveymonkey.exceptions import SurveyMonkeyBadResponse

from surveymonkey.tests.utils import create_fake_connection
from surveymonkey.tests.mocks.surveys import SurveyListMock


survey_mocks = SurveyListMock(total=125)
malformed_response_mocks = [
    (survey_mocks.surveys_no_data),
    (survey_mocks.surveys_no_links),
]


class TestSurveyList(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()

    def setup_method(self, method):
        self.mocks = survey_mocks
        self.surveys = Surveys(self.connection)

    def test_get_first_page_of_surveys(self):
        with HTTMock(self.mocks.surveys):
            survey_list = self.surveys.surveys(page=1)

        expect(survey_list).to(have_length(50))
        expect(survey_list[0]).to(have_keys('href', 'id', 'title'))

    def test_get_big_list_of_all_surveys(self):
        with HTTMock(self.mocks.surveys):
            survey_big_list = self.surveys.surveys()

        expect(survey_big_list).to(have_length(125))

        for survey in survey_big_list:
            expect(survey).to(have_keys('href', 'id', 'title'))
            expect(survey["href"]).to(end_with(survey['id']))

    def test_get_survey_list_by_valid_page_number(self):
        with HTTMock(self.mocks.surveys):
            survey_list = self.surveys.surveys(per_page=10, page=3)

        expect(survey_list).to(have_length(10))
        expect(survey_list[0]).to(have_keys('href', 'id', 'title'))

    @pytest.mark.parametrize("mock", malformed_response_mocks)
    def test_surveymonkey_malformed_responses(self, mock):
        with HTTMock(mock):
            with pytest.raises(SurveyMonkeyBadResponse) as e:
                self.surveys.surveys()

            expect(str(e.value)).to(contain("Missing keys"))
