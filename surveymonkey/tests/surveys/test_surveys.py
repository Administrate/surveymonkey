#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
from furl import furl

from httmock import HTTMock
from expects import expect, have_keys, have_key, be_a, equal

from surveymonkey.surveys import Surveys
from surveymonkey.tests.matchers import be_url
from surveymonkey.tests.mocks.surveys import SurveyGetMock
from surveymonkey.tests.utils import create_fake_connection


class TestGetSurvey(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()
        self.survey = Surveys(connection=self.connection)
        self.survey_id = random.randint(1234, 56789)
        self.mock = SurveyGetMock()

    def test_get_single_survey_by_id(self):
        with HTTMock(self.mock.by_id):
            survey = self.survey.by_id(survey_id=self.survey_id)

        expect(survey).to(be_a(dict))
        expect(survey).to(have_keys('id', 'title', 'analyze_url'))

    def test_valid_analyze_url_returned(self):
        with HTTMock(self.mock.by_id):
            survey = self.survey.by_id(survey_id=self.survey_id)

        expect(survey).to(be_a(dict))
        expect(survey).to(have_key('analyze_url'))

        analyze_url = furl(survey["analyze_url"])

        expect(survey["analyze_url"]).to(be_url)
        expect(analyze_url.path.segments[0]).to(equal("analyze"))
