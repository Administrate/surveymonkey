# -*- coding: utf-8 -*-
from __future__ import absolute_import

import six
from furl import furl

from surveymonkey.constants import API_VERSION


class SurveyMonkeyConnection(object):

    def __init__(self, access_token, access_url=None):
        self.access_token = access_token
        self.access_url = self._add_api_version_to_url(access_url) if access_url else None

    @staticmethod
    def _add_api_version_to_url(url):
        url = furl(url)
        if not url.path or url.path == '/':
            url.join(API_VERSION)
        return url.url.rstrip('/')


class BaseConfig(object):
    def __init__(self, **kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def vars(self):
        return vars(self)
