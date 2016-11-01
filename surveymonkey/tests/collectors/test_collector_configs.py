#!/usr/bin/env python
# -*- coding: utf-8 -*-

from expects import expect
from faker import Factory

from surveymonkey.collectors import EmailConfig, WeblinkConfig
from surveymonkey.tests.collectors.matchers.config import be_email, be_weblink


class TestCollectorsConfiguration(object):

    def setup_class(self):
        self.fake = Factory.create()

    def test_type_is_email_when_using_the_email_configurator(self):
        configuration = EmailConfig(
            name=self.fake.catch_phrase(),
            sender_email=self.fake.email()
        )

        expect(configuration).to(be_email)

    def test_type_is_weblink_when_using_the_weblink_configurator(self):
        configuration = WeblinkConfig(
            name=self.fake.catch_phrase(),
            sender_email=self.fake.email()
        )

        expect(configuration).to(be_weblink)
