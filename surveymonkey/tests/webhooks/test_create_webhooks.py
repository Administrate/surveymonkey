#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
import pytest
from httmock import HTTMock
from expects import expect, have_key, equal

from surveymonkey.webhooks import Webhook
from surveymonkey.webhooks.constants import COMPLETED, DISQUALIFIED, UPDATED, SURVEY

from surveymonkey.tests.mocks.webhooks import WebhookMock
from surveymonkey.tests.utils import create_fake_connection


def create_random_number_of_object_ids():
    return [str(random.randint(1234, 567890)) for x in range(1, random.randint(3, 12))]

single_survey_list = [
    (COMPLETED, SURVEY, str(random.randint(1234, 567890))),
    (DISQUALIFIED, SURVEY, str(random.randint(1234, 567890))),
    (UPDATED, SURVEY, str(random.randint(1234, 567890)))
]


multiple_survey_list = [
    (COMPLETED, SURVEY, create_random_number_of_object_ids()),
    (DISQUALIFIED, SURVEY, create_random_number_of_object_ids()),
    (UPDATED, SURVEY, create_random_number_of_object_ids())
]


class TestCreateWebhooks(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()

    def setup_method(self, method):
        pass

    @pytest.mark.parametrize("event_type,object_type,object_ids", single_survey_list)
    def test_webhook_create_responses_for_single_survey(self, event_type, object_type, object_ids):
        mock = WebhookMock(
            event_type=event_type,
            object_type=object_type,
            object_ids=[object_ids],
            subscription_url="https://example.com"
        )

        with HTTMock(mock.create):
            webhook = Webhook(self.connection)
            response = webhook.create_for_survey(
                event_type=event_type,
                object_ids=object_ids,
                subscription_url="https://example.com"
            )

        expect(response).to(have_key('event_type', event_type))
        expect(response["object_ids"]).to(equal([object_ids]))

    @pytest.mark.parametrize("event_type,object_type,object_ids", multiple_survey_list)
    def test_webhook_create_responses_for_multiple_surveys(self, event_type, object_type, object_ids):  # noqa:E501
        mock = WebhookMock(
            event_type=event_type,
            object_type=object_type,
            object_ids=object_ids,
            subscription_url="https://example.com"
        )

        with HTTMock(mock.create):
            webhook = Webhook(self.connection)
            response = webhook.create_for_survey(
                event_type=event_type,
                object_ids=object_ids,
                subscription_url="https://example.com"
            )

        expect(response).to(have_key('event_type', event_type))
        expect(response["object_ids"]).to(equal(object_ids))
