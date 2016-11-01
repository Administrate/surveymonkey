# -*- coding: utf-8 -*-

import six


class BaseConfig(object):
    def __init__(self, **kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)


class InviteConfig(BaseConfig):
    def __init__(self, **kwargs):
        super(InviteConfig, self).__init__(**kwargs)
        self.type = "invite"


def is_invite(type):
    return type.lower() == "invite"
