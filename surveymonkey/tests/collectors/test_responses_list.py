#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pytest
from httmock import HTTMock
from expects import expect, have_keys, have_length

from ..utils import create_fake_connection
from .matchers.bulk import be_completed, be_partial, be_overquota, be_disqualified
from ..mocks.collectors import CollectorResponsesListMock

from surveymonkey.collectors import CollectorResponses


possible_statuses = [
    ('completed', 'completed', be_completed),
    ('partial', 'partial', be_partial),
    ('overquota', 'overquota', be_overquota),
    ('disqualified', 'disqualified', be_disqualified)
]


class TestFetchResponsesForSingleCollector(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()

    def setup_method(self, method):
        self.collector_id = random.randint(1234, 567890)
        self.collector = CollectorResponses(
            connection=self.connection,
            collector_ids=self.collector_id
        )

    def test_get_all_responses(self):
        mock = CollectorResponsesListMock(total=55, collector_ids=self.collector_id)
        with HTTMock(mock.list):
            responses_list = self.collector.responses()

        expect(responses_list).to(have_length(55))
        expect(responses_list[0]).to(have_keys('analyze_url', 'response_status', 'date_modified'))
        expect(responses_list[0]).to(have_keys('id', 'collector_id', 'recipient_id', 'survey_id'))

    @pytest.mark.parametrize("status,method_name,be_status", possible_statuses)
    def test_get_responses_by_status(self, status, method_name, be_status):
        mock = CollectorResponsesListMock(
            total=5,
            collector_ids=self.collector_id,
            status=status
        )

        with HTTMock(mock.list):
            responses_list = getattr(self.collector, method_name)()

        expect(responses_list).to(have_length(5))
        for response in responses_list:
            expect(response).to(be_status)


class TestFetchResponsesForMultipleCollectors(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()

    def setup_method(self, method):
        self.collector_ids = [
            str(random.randint(1234, 567890)) for i in range(3, random.randint(4, 10))
        ]
        self.collector = CollectorResponses(
            connection=self.connection,
            collector_ids=self.collector_ids,
            survey_id=random.randint(1234, 567890)
        )

    def test_get_all_responses(self):
        mock = CollectorResponsesListMock(total=5, collector_ids=self.collector_ids)
        with HTTMock(mock.list):
            responses_list = self.collector.responses()

        expect(responses_list).to(have_length(5))
        expect(responses_list[0]).to(have_keys('analyze_url', 'response_status', 'date_modified'))
        expect(responses_list[0]).to(have_keys('id', 'collector_id', 'recipient_id', 'survey_id'))

    def test_exception_raised_when_survey_id_not_supplied(self):
        mock = CollectorResponsesListMock(total=5, collector_ids=self.collector_ids)
        with HTTMock(mock.list):
            with pytest.raises(AttributeError):
                CollectorResponses(
                    connection=self.connection,
                    collector_ids=self.collector_ids
                )
                self.collector.responses()

    @pytest.mark.parametrize("status,method_name,be_status", possible_statuses)
    def test_get_responses_by_status(self, status, method_name, be_status):
        mock = CollectorResponsesListMock(
            total=5,
            collector_ids=self.collector_ids,
            status=status
        )

        with HTTMock(mock.list):
            responses_list = getattr(self.collector, method_name)()

        expect(responses_list).to(have_length(5))
        for response in responses_list:
            expect(response).to(be_status)
