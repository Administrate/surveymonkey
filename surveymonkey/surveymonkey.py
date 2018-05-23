# -*- coding: utf-8 -*-
from __future__ import absolute_import

import six


class SurveyMonkeyConnection(object):

    def __init__(self, access_token, access_url=None):
        self.ACCESS_TOKEN = access_token
        self.ACCESS_URL = access_url


class BaseConfig(object):
    def __init__(self, **kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def vars(self):
        return vars(self)
