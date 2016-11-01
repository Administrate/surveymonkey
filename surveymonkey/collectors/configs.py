# -*- coding: utf-8 -*-

from surveymonkey.surveymonkey import BaseConfig


class EmailConfig(BaseConfig):
    def __init__(self, **kwargs):
        super(EmailConfig, self).__init__(**kwargs)
        self.type = "email"


class WeblinkConfig(BaseConfig):
    def __init__(self, **kwargs):
        super(WeblinkConfig, self).__init__(**kwargs)
        self.type = "weblink"


def is_email(type):
    return type.lower() == "email"


def is_weblink(type):
    return type.lower() == "weblink"
