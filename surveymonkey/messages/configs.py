# -*- coding: utf-8 -*-
from __future__ import absolute_import

from surveymonkey.surveymonkey import BaseConfig


class InviteConfig(BaseConfig):
    def __init__(self, **kwargs):
        super(InviteConfig, self).__init__(**kwargs)
        self.type = "invite"


class ReminderConfig(BaseConfig):
    def __init__(self, **kwargs):
        super(ReminderConfig, self).__init__(**kwargs)
        self.type = "reminder"
        self.recipient_status = "has_not_responded"


def is_invite(type):
    return type.lower() == "invite"


def is_reminder(type):
    return type.lower() == "reminder"
