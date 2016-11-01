# -*- coding: utf-8 -*-

import six


class SurveyMonkeyConnection(object):

    def __init__(self, access_token):
        self.ACCESS_TOKEN = access_token


class BaseConfig(object):
    def __init__(self, **kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)
