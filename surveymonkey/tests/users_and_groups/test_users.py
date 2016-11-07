#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from httmock import HTTMock
from expects import expect, have_keys, equal

from surveymonkey.users import Users

from surveymonkey.tests.utils import create_fake_connection
from surveymonkey.tests.mocks.users import UsersResponseMocks


class TestSurveymonkeyUser(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()
        self.mocks = UsersResponseMocks()
        self.users = Users(self.connection)

    def test_successful_request_to_user_me_endpoint(self):
        with HTTMock(self.mocks.me):
            current_user = self.users.me()

            expect(current_user).to(have_keys('id', 'username', 'email'))
            expect(current_user["account_type"]).to(equal("enterprise_platinum"))
