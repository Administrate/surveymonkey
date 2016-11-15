#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
import pytest
from httmock import HTTMock
from expects import expect, have_key, equal

from surveymonkey.webhooks import Webhook
from surveymonkey.webhooks.constants import COMPLETED, DISQUALIFIED, UPDATED, SURVEY, COLLECTOR

from surveymonkey.tests.mocks.webhooks import WebhookMock
from surveymonkey.tests.utils import create_fake_connection


def create_random_number_of_object_ids():
    return [str(random.randint(1234, 567890)) for x in range(1, random.randint(3, 12))]


single_object_list = [
    (COMPLETED, SURVEY, "create_for_survey", str(random.randint(1234, 567890))),
    (DISQUALIFIED, SURVEY, "create_for_survey", str(random.randint(1234, 567890))),
    (UPDATED, SURVEY, "create_for_survey", str(random.randint(1234, 567890))),
    (COMPLETED, COLLECTOR, "create_for_collector", str(random.randint(1234, 567890))),
    (DISQUALIFIED, COLLECTOR, "create_for_collector", str(random.randint(1234, 567890))),
    (UPDATED, COLLECTOR, "create_for_collector", str(random.randint(1234, 567890)))
]


multiple_object_list = [
    (COMPLETED, SURVEY, "create_for_survey", create_random_number_of_object_ids()),
    (DISQUALIFIED, SURVEY, "create_for_survey", create_random_number_of_object_ids()),
    (UPDATED, SURVEY, "create_for_survey", create_random_number_of_object_ids()),
    (COMPLETED, COLLECTOR, "create_for_collector", create_random_number_of_object_ids()),
    (DISQUALIFIED, COLLECTOR, "create_for_collector", create_random_number_of_object_ids()),
    (UPDATED, COLLECTOR, "create_for_collector", create_random_number_of_object_ids())
]


class TestCreateWebhooks(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()

    def setup_method(self, method):
        pass

    @pytest.mark.parametrize("event_type,object_type,method,object_ids", single_object_list)
    def test_webhook_create_for_single_object(self, event_type, object_type, method, object_ids):
        mock = WebhookMock(
            event_type=event_type,
            object_type=object_type,
            object_ids=[object_ids],
            subscription_url="https://example.com"
        )

        with HTTMock(mock.create):
            webhook = Webhook(self.connection)
            response = getattr(webhook, method)(
                event_type=event_type,
                object_ids=object_ids,
                subscription_url="https://example.com"
            )

        expect(response).to(have_key('event_type', event_type))
        expect(response["object_ids"]).to(equal([object_ids]))

    @pytest.mark.parametrize("event_type,object_type,method,object_ids", multiple_object_list)
    def test_webhook_create_for_multiple_objects(self, event_type, object_type, method, object_ids):  # noqa:E501
        mock = WebhookMock(
            event_type=event_type,
            object_type=object_type,
            object_ids=object_ids,
            subscription_url="https://example.com"
        )

        with HTTMock(mock.create):
            webhook = Webhook(self.connection)
            response = getattr(webhook, method)(
                event_type=event_type,
                object_ids=object_ids,
                subscription_url="https://example.com"
            )

        expect(response).to(have_key('event_type', event_type))
        expect(response["object_ids"]).to(equal(object_ids))
