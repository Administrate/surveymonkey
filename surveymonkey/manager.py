# -*- coding: utf-8 -*-

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

    def parse_response(self, response):
        return response.json()

    def get(self, base_url):
        session = self.create_session()
        url = self.build_url(base_url)
        response = session.get(url)
        response_raises(response)
        return self.parse_response(response)
