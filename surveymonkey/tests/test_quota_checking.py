#!/usr/bin/env python
# -*- coding: utf-8 -*-

from httmock import HTTMock
from expects import expect, have_keys, be_false, be_true, be_none

from surveymonkey.manager import BaseManager
from .utils import create_fake_connection
from .mocks.quota import QuotaMocks


class TestQuotaChecking(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()
        self.mocks = QuotaMocks()

    def setup_method(self, method):
        self.manager = BaseManager(self.connection)

    def test_daily_quota_headers_available_when_sending_a_head_request(self):
        with HTTMock(self.mocks.within_daily_quota):
            headers = self.manager.head('mocked://')

        expect(headers).to(have_keys('X-Plan-Quota-Allotted', 'X-Plan-Quota-Current'))

    def test_manager_correctly_updated_when_daily_quota_is_not_exceeded(self):
        with HTTMock(self.mocks.within_daily_quota):
            self.manager.head('mocked://')

        expect(self.manager.daily_quota_exceeded).to(be_false)
        expect(self.manager.quota_exceeded).to(be_false)

    def test_per_second_quota_headers_available_when_sending_a_head_request(self):
        with HTTMock(self.mocks.within_per_second_quota):
            headers = self.manager.head('mocked://')

        expect(headers).to(have_keys('X-Plan-QPS-Allotted', 'X-Plan-QPS-Current'))

    def test_manager_correctly_updated_when_per_second_quota_is_not_exceeded(self):
        with HTTMock(self.mocks.within_per_second_quota):
            self.manager.head('mocked://')

        expect(self.manager.per_second_quota_exceeded).to(be_false)
        expect(self.manager.quota_exceeded).to(be_false)

    def test_manager_correctly_updated_when_daily_quota_is_exceeded(self):
        with HTTMock(self.mocks.exceeds_daily_quota):
            self.manager.head('mocked://')

        expect(self.manager.daily_quota_exceeded).to(be_true)
        expect(self.manager.quota_exceeded).to(be_true)

    def test_manager_correctly_updated_when_per_second_quota_is_exceeded(self):
        with HTTMock(self.mocks.exceeds_per_second_quota):
            self.manager.head('mocked://')

        expect(self.manager.per_second_quota_exceeded).to(be_true)
        expect(self.manager.quota_exceeded).to(be_true)

    def test_manager_does_not_die_when_quota_headers_are_not_set(self):
        with HTTMock(self.mocks.missing_quota_headers):
            self.manager.head('mocked://')

        expect(self.manager.quota_exceeded).to(be_none)
