# -*- coding: utf-8 -*-

import six


class BaseConfig(object):
    def __init__(self, **kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)


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
