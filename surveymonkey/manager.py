# -*- coding: utf-8 -*-

from datetime import datetime
import requests

from .exceptions import response_raises


class BaseManager(object):

    def __init__(self, connection):
        self.connection = connection

    def create_session(self):
        session = requests.Session()
        session.headers.update({
            "Authorization": "Bearer %s" % self.connection.ACCESS_TOKEN,
            "Content-Type": "application/json"
        })

        return session

    def build_url(self, url):
        return "{url}?api_key={api_key}".format(
            url=url,
            api_key=self.connection.API_KEY
        )

    def set_quotas(self, response):
        self.quotas = {}
        if "X-Plan-QPS-Allotted" in response.headers:
            self.quotas["QPS Allotted"] = response.headers["X-Plan-QPS-Allotted"]
        if "X-Plan-QPS-Current" in response.headers:
            self.quotas["QPS Current"] = response.headers["X-Plan-QPS-Current"]
        if "X-Plan-Quota-Allotted" in response.headers:
            self.quotas["Quota Allotted"] = response.headers["X-Plan-Quota-Allotted"]
        if "X-Plan-Quota-Current" in response.headers:
            self.quotas["Quota Current"] = response.headers["X-Plan-Quota-Current"]
        if "X-Plan-Quota-Reset" in response.headers:
            self.quotas["Quota Reset"] = datetime.strptime(
                response.headers["X-Plan-Quota-Reset"], "%A, %B %d, %Y %I:%M:%S %p %Z"
            )

        if "Quota Current" and "Quota Allotted" in self.quotas:
            self.daily_quota_exceeded = (
                self.quotas["Quota Current"] > self.quotas["Quota Allotted"]
            )
        else:
            self.daily_quota_exceeded = None

        if "QPS Current" and "QPS Allotted" in self.quotas:
            self.per_second_quota_exceeded = (
                self.quotas["QPS Current"] > self.quotas["QPS Allotted"]
            )
        else:
            self.per_second_quota_exceeded = None

        self.quota_exceeded = (self.daily_quota_exceeded or self.per_second_quota_exceeded)

    def parse_response(self, response):
        return response.json()

    def make_request(self, base_url, method="GET"):
        self.create_session()
        url = self.build_url(base_url)
        return requests.request(method, url)

    def get(self, base_url):
        response = self.make_request(base_url)
        self.set_quotas(response)
        response_raises(response)
        return self.parse_response(response)

    def head(self, base_url):
        response = self.make_request(base_url, 'HEAD')
        self.set_quotas(response)
        response_raises(response)
        return response.headers
