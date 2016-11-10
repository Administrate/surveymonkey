#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects import expect, equal, have_property

from surveymonkey.messages import InviteConfig, ReminderConfig
from surveymonkey.tests.messages.matchers.configs import be_invite, be_reminder


class TestMessageConfigs(object):

    def test_type_is_invite_when_using_the_invite_configurator(self):
        configuration = InviteConfig()
        expect(configuration).to(be_invite)

    def test_type_is_reminder_when_using_the_reminder_configurator(self):
        configuration = ReminderConfig()
        expect(configuration).to(be_reminder)

    def test_reminder_has_correct_recipient_status(self):
        config = ReminderConfig()
        expect(config).to(have_property("recipient_status"))

    def test_config_accepts_extra_values(self):
        config = InviteConfig(subject="My Test Message")
        expect(config.subject).to(equal("My Test Message"))
