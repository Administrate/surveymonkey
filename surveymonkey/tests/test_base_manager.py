#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pytest

from httmock import HTTMock
from expects import expect, have_key, have_keys, equal, be_a, contain
from unittest.mock import MagicMock

from surveymonkey.manager import BaseManager
from surveymonkey.constants import URL_USER_ME, API_URL
from surveymonkey.exceptions import SurveyMonkeyBadResponse

from surveymonkey.tests.utils import create_fake_connection
from surveymonkey.tests.mocks.users import UsersResponseMocks


class TestBaseManager(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()
        self.manager = BaseManager(self.connection)
        self.session = self.manager.create_session()

    def test_session_content_type_is_json(self):
        expect(self.session.headers).to(have_key('Content-Type'))
        expect(self.session.headers['Content-Type']).to(equal('application/json'))

    def test_session_contains_authorization_bearer_token(self):
        expect(self.session.headers).to(have_key('Authorization'))
        expect(self.session.headers['Authorization']).to(equal("Bearer %s" % self.ACCESS_TOKEN))

    def test_parse_response_returns_a_dict_with_correct_keys(self):
        with HTTMock(UsersResponseMocks().me):
            response = self.session.get(API_URL + URL_USER_ME)
            data = self.manager.parse_response(response)

            expect(data).to(have_keys('id', 'username', 'email'))
            expect(data["id"]).to(be_a(str))  # IDs from SurveyMonkey are strings

    def test_parse_response_raises_exception_on_malformed_response(self):
        with pytest.raises(SurveyMonkeyBadResponse) as e:
            BaseManager.parse_response('{This is malformed: [[[JSON]]}')

        expect(str(e.value)).to(contain("JSON"))

    def test_daily_quota_exceeded_is_none_if_quota_current_header_is_missing(self):
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-Quota-Current"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.daily_quota_exceeded).to(equal(None))

    def test_daily_quota_exceeded_is_none_if_quota_allotted_header_is_missing(self):
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-Quota-Allotted"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.daily_quota_exceeded).to(equal(None))

    def test_daily_quota_exceeded_is_true_if_quota_current_exceeds_quota_allotted(self):
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-Quota-Current"] = 1001
        response.headers["X-Plan-Quota-Allotted"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.daily_quota_exceeded).to(equal(True))

    def test_daily_quota_exceeded_is_false_if_quota_current_is_less_than_quota_allotted(self):
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-Quota-Current"] = 999
        response.headers["X-Plan-Quota-Allotted"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.daily_quota_exceeded).to(equal(False))

    def test_per_second_quota_exceeded_is_none_if_qps_current_header_is_missing(self):
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-QPS-Current"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.daily_quota_exceeded).to(equal(None))

    def test_per_second_quota_exceeded_is_none_if_qps_allotted_header_is_missing(self):
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-QPS-Allotted"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.per_second_quota_exceeded).to(equal(None))

    def test_per_second_quota_exceeded_is_true_if_qps_current_exceeds_qps_allotted(self):
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-QPS-Current"] = 1001
        response.headers["X-Plan-QPS-Allotted"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.per_second_quota_exceeded).to(equal(True))

    def test_per_second_quota_exceeded_is_false_if_qps_current_is_less_than_qps_allotted(self):
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-QPS-Current"] = 999
        response.headers["X-Plan-QPS-Allotted"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.per_second_quota_exceeded).to(equal(False))

    def test_quota_exceeded_is_true_if_daily_quota_exceeded_is_true_and_per_second_quota_exceeded_is_false(self):  # noqa:E501
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-Quota-Current"] = 1001
        response.headers["X-Plan-Quota-Allotted"] = 1000
        response.headers["X-Plan-QPS-Current"] = 999
        response.headers["X-Plan-QPS-Allotted"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.quota_exceeded).to(equal(True))

    def test_quota_exceeded_is_true_if_daily_quota_exceeded_is_false_and_per_second_quota_exceeded_is_true(self):  # noqa:E501
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-Quota-Current"] = 999
        response.headers["X-Plan-Quota-Allotted"] = 1000
        response.headers["X-Plan-QPS-Current"] = 1001
        response.headers["X-Plan-QPS-Allotted"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.quota_exceeded).to(equal(True))

    def test_quota_exceeded_is_false_if_daily_quota_exceeded_is_false_and_per_second_quota_exceeded_is_false(self):  # noqa:E501
        response = MagicMock()
        response.headers = {}
        response.headers["X-Plan-Quota-Current"] = 999
        response.headers["X-Plan-Quota-Allotted"] = 1000
        response.headers["X-Plan-QPS-Current"] = 999
        response.headers["X-Plan-QPS-Allotted"] = 1000

        self.manager.set_quotas(response)
        expect(self.manager.quota_exceeded).to(equal(False))

    def test_access_url_overrides_api_url_when_provided(self):
        connection = MagicMock(
            connection=self.connection,
            access_url="http://overridden.com"
        )
        manager = BaseManager(connection)

        overriden_url = manager.build_url(URL_USER_ME)
        expect(overriden_url).to(equal("http://overridden.com" + URL_USER_ME))

    def test_add_base_url_handles_pre_formatted_urls(self):
        connection = MagicMock(
            connection=self.connection,
            access_url="http://overridden.com"
        )
        manager = BaseManager(connection)
        formatted_overridden_url = "http://overridden.com" + URL_USER_ME
        formatted_default_url = API_URL + URL_USER_ME

        overriden_url = manager.build_url(formatted_overridden_url)
        default_url = manager.build_url(formatted_default_url)
        expect(overriden_url).to(equal(formatted_overridden_url))
        expect(default_url).to(equal(formatted_default_url))
