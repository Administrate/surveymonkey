#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six

from faker import Factory
from httmock import HTTMock
from expects import expect, have_key, have_keys, equal, start_with, end_with, be_a

from surveymonkey.surveymonkey import SurveyMonkeyConnection
from surveymonkey.manager import BaseManager
from surveymonkey.constants import URL_USER_ME

from .mocks.users import UsersResponseMocks


class TestBaseManager(object):

    def setup_class(self):
        self.fake = Factory.create()
        self.ACCESS_TOKEN = self.fake.password(
            length=50, special_chars=True, digits=True,
            upper_case=True, lower_case=True
        )
        self.API_KEY = self.fake.password(
            length=12, digits=True,
            upper_case=True, lower_case=True
        )
        self.connection = SurveyMonkeyConnection(self.ACCESS_TOKEN, self.API_KEY)
        self.manager = BaseManager(self.connection)
        self.session = self.manager.create_session()

    def test_session_content_type_is_json(self):
        expect(self.session.headers).to(have_key('Content-Type'))
        expect(self.session.headers['Content-Type']).to(equal('application/json'))

    def test_session_contains_authorization_bearer_token(self):
        expect(self.session.headers).to(have_key('Authorization'))
        expect(self.session.headers['Authorization']).to(equal("Bearer %s" % self.ACCESS_TOKEN))

    def test_build_url_appends_our_api_key(self):
        built_url = self.manager.build_url(URL_USER_ME)

        expect(built_url).to(start_with(URL_USER_ME))
        expect(built_url).to(end_with(self.API_KEY))

    def test_parse_response_returns_a_dict_with_correct_keys(self):
        with HTTMock(UsersResponseMocks().me):
            response = self.session.get(URL_USER_ME)
            data = self.manager.parse_response(response)

            expect(data).to(have_keys('id', 'username', 'email'))
            expect(data["id"]).to(be_a(six.text_type))  # IDs from SurveyMonkey are strings not ints
