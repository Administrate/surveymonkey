#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from httmock import HTTMock
from expects import expect, have_keys

from ..utils import create_fake_connection
from .collector_matchers import be_email, be_weblink, be_new
from ..mocks.collectors import CollectorMock

from surveymonkey.collectors import Collector, EmailConfig, WeblinkConfig


class TestCreateCollectors(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.API_KEY, self.connection = create_fake_connection()

    def setup_method(self, method):
        pass

    def test_email_collector_created_with_no_optional_config_values(self):
        config = EmailConfig()
        collector = Collector(connection=self.connection, config=config)

        with HTTMock(CollectorMock(config).create):
            new_collector = collector.create(survey_id=random.randint(12345, 67890))

        expect(new_collector).to(be_email)
        expect(new_collector).to(be_new)
        expect(new_collector).to(have_keys('id', 'name', 'url'))

    def test_weblink_collector_created_with_no_optional_config_values(self):
        config = WeblinkConfig()
        collector = Collector(connection=self.connection, config=config)

        with HTTMock(CollectorMock(config).create):
            new_collector = collector.create(survey_id=random.randint(12345, 67890))

        expect(new_collector).to(be_weblink)
        expect(new_collector).to(be_new)
        expect(new_collector).to(have_keys('id', 'name', 'url'))
