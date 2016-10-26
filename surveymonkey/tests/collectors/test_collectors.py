#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from httmock import HTTMock
from expects import expect, have_keys, have_length

from ..utils import create_fake_connection
from .collector_matchers import be_email, be_weblink, be_new
from ..mocks.collectors import CollectorMock, CollectorsListMock

from surveymonkey.collectors import Collector, EmailConfig, WeblinkConfig


class TestCreateCollectors(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.API_KEY, self.connection = create_fake_connection()

    def setup_method(self, method):
        self.survey_id = random.randint(12345, 67890)

    def test_email_collector_created_with_no_optional_config_values(self):
        config = EmailConfig()
        collector = Collector(connection=self.connection, config=config)

        with HTTMock(CollectorMock(config).create):
            new_collector = collector.create(survey_id=self.survey_id)

        expect(new_collector).to(be_email)
        expect(new_collector).to(be_new)
        expect(new_collector).to(have_keys('id', 'name', 'url'))

    def test_weblink_collector_created_with_no_optional_config_values(self):
        config = WeblinkConfig()
        collector = Collector(connection=self.connection, config=config)

        with HTTMock(CollectorMock(config).create):
            new_collector = collector.create(survey_id=self.survey_id)

        expect(new_collector).to(be_weblink)
        expect(new_collector).to(be_new)
        expect(new_collector).to(have_keys('id', 'name', 'url'))

    def test_list_of_collectors_returned_for_valid_survey(self):
        collector = Collector(connection=self.connection)
        mock = CollectorsListMock(total=2, survey_id=self.survey_id)

        with HTTMock(mock.list):
            collector_list = collector.list(survey_id=self.survey_id)

        expect(collector_list).to(have_length(2))
        expect(collector_list[0]).to(have_keys('href', 'id', 'name'))
