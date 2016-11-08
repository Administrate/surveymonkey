# -*- coding: utf-8 -*-
from __future__ import absolute_import

from httmock import all_requests, response
from surveymonkey.tests.mocks.utils import create_quota_headers


class QuotaMocks(object):

    @all_requests
    def within_daily_quota(self, url, request):
        headers = create_quota_headers()
        content = {
            'message': 'This is a mocked request which is within the daily quota.'
        }
        return response(200, content, headers)

    @all_requests
    def exceeds_daily_quota(self, url, request):
        headers = create_quota_headers(qpd=(10000, 10001))
        content = {
            'message': 'This is a mocked request which exceeds the daily quota.'
        }
        return response(200, content, headers)

    @all_requests
    def within_per_second_quota(self, url, request):
        headers = create_quota_headers()
        content = {
            'message': 'This is a mocked request which is within the per second quota.'
        }
        return response(200, content, headers)

    @all_requests
    def exceeds_per_second_quota(self, url, request):
        headers = create_quota_headers(qps=(8, 9))
        content = {
            'message': 'This is a mocked request which exceeds the per second quota.'
        }
        return response(200, content, headers)

    @all_requests
    def missing_quota_headers(self, url, request):
        content = {
            'message': 'This is a mocked request which does not have quota headers.'
        }
        return response(200, content)
