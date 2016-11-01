#!/usr/bin/env python
# -*- coding: utf-8 -*-

from expects import expect

from surveymonkey.messages import InviteConfig
from surveymonkey.tests.messages.matchers.configs import be_invite


class TestMessageConfigs(object):

    def test_type_is_invite_when_using_the_invite_configurator(self):
        configuration = InviteConfig()
        expect(configuration).to(be_invite)
