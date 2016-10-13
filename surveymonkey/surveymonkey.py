# -*- coding: utf-8 -*-


class SurveyMonkeyConnection(object):

    def __init__(self, access_token, api_key):
        self.ACCESS_TOKEN = access_token
        self.API_KEY = api_key
