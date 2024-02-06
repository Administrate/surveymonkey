#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random

from expects import expect, have_keys, have_length, be_a
from httmock import HTTMock
from unittest.mock import patch

from surveymonkey.constants import URL_COLLECTOR_CREATE
from surveymonkey.collectors import Collector, EmailConfig, WeblinkConfig
from surveymonkey.tests.collectors.matchers.collector import be_email, be_weblink, be_new
from surveymonkey.tests.mocks.collectors import (CollectorMock, CollectorsListMock,
                                                 CollectorGetMock)
from surveymonkey.tests.utils import create_fake_connection


class TestCreateCollectors(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()

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

    @patch('surveymonkey.collectors.collectors.Collector.post')
    def test_collector_created_with_custom_name(self, mock_post):
        config = EmailConfig(name="This is a different name")
        collector = Collector(connection=self.connection, config=config)
        collector.create(1234)

        mock_post.assert_called_with(
            base_url=URL_COLLECTOR_CREATE,
            data={'name': 'This is a different name', 'type': 'email'},
            survey_id=1234
        )


class TestGetCollector(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()
        self.collector = Collector(connection=self.connection)
        self.collector_id = random.randint(1234, 56789)

    def test_single_collector_returned_for_id(self):
        mock = CollectorGetMock()

        with HTTMock(mock.by_id):
            collector = self.collector.by_id(collector_id=self.collector_id)

        expect(collector).to(be_a(dict))
        expect(collector).to(have_keys("id", "status", "type", "url"))
