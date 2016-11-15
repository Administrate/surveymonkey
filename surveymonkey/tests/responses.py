#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random

from httmock import HTTMock
from expects import expect, have_keys, be_a

from surveymonkey.responses import Response
from surveymonkey.tests.mocks.responses import ResponseGetMock
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
