# -*- coding: utf-8 -*-
from __future__ import absolute_import

from surveymonkey.surveymonkey import BaseConfig


class InviteConfig(BaseConfig):
    def __init__(self, **kwargs):
        super(InviteConfig, self).__init__(**kwargs)
        self.type = "invite"


def is_invite(type):
    return type.lower() == "invite"
