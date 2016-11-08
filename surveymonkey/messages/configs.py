# -*- coding: utf-8 -*-

from surveymonkey.surveymonkey import BaseConfig


class InviteConfig(BaseConfig):
    def __init__(self, **kwargs):
        super(InviteConfig, self).__init__(**kwargs)
        self.type = "invite"


class ReminderConfig(BaseConfig):
    def __init__(self, **kwargs):
        super(ReminderConfig, self).__init__(**kwargs)
        self.type = "reminder"


def is_invite(type):
    return type.lower() == "invite"


def is_reminder(type):
    return type.lower() == "reminder"
