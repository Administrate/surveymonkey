#!/usr/bin/env python
# -*- coding: utf-8 -*-

from httmock import HTTMock
from expects import expect, end_with, have_keys, have_length

from surveymonkey.surveys import Surveys

from ..utils import create_fake_connection
from ..mocks.surveys import SurveyListMock


class TestSurveyList(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.API_KEY, self.connection = create_fake_connection()

    def setup_method(self, method):
        self.mocks = SurveyListMock(total=125)
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
