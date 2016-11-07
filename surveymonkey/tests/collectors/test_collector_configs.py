#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects import expect

from surveymonkey.collectors import EmailConfig, WeblinkConfig
from surveymonkey.tests.collectors.matchers.config import be_email, be_weblink


class TestCollectorsConfiguration(object):

    def test_type_is_email_when_using_the_email_configurator(self, faker):
        configuration = EmailConfig(
            name=faker.catch_phrase(),
            sender_email=faker.email()
        )

        expect(configuration).to(be_email)

    def test_type_is_weblink_when_using_the_weblink_configurator(self, faker):
        configuration = WeblinkConfig(
            name=faker.catch_phrase(),
            sender_email=faker.email()
        )

        expect(configuration).to(be_weblink)
