# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random

from httmock import all_requests, response
from surveymonkey.tests.mocks.utils import create_quota_headers
from surveymonkey.constants import API_URL

from surveymonkey.tests.conftest import faker


class MessagesMock(object):

    def __init__(self, config):
        self.config = {}
        self.id = "%s" % random.randint(12345, 67890)

        default_config = (
            ("status", "not_sent"),
            ("body", "<html>...</html>"),
            ("recipient_status", None),
            ("is_branding_enabled", True),
            ("href", "This survey is currently closed."),
            ("href", "{base}/collectors/{collector_id}/messages/{id}".format(
                base=API_URL,
                collector_id=random.randint(1234, 567890),
                id=self.id
            )),
            ("is_scheduled", False),
            ("scheduled_date", None),
            ("date_created", faker.iso8601(tzinfo=None)),
            ("type", "invite"),
            ("id", self.id),
            ("subject", "We want your opinion"),
            ("name", "New Collector"),
        )

        for key, value in default_config:
            self.config[key] = getattr(config, key) if hasattr(config, key) else value

    @all_requests
    def create(self, url, request):
        headers = create_quota_headers()
        content = self.config
        return response(200, content, headers)


class MessagesRecipientsMock(object):

    @all_requests
    def recipient_add(self, url, request):
        headers = create_quota_headers()

        content = {
            "succeeded": [{
                "id": str(random.randint(1234, 567890)),
                "email": faker.safe_email(),
                "href": "https://api.surveymonkey.net/v3/collectors/1234/recipients/1234"
            }],
            "invalids": [],
            "existing": [],
            "bounced": [],
            "opted_out": [],
            "duplicate": []
        }

        return response(200, content, headers)


class MessagesSendMock(object):

    @all_requests
    def send(self, url, request):
        headers = create_quota_headers()

        content = {
          "is_scheduled": True,
          "scheduled_date": faker.iso8601(tzinfo=None),
          "body": "<html>...</html>",
          "subject": "We want your opinion",
          "recipients": [
              str(random.randint(12345, 67890)) for x in range(2, random.randint(5, 20))
          ],
          "recipient_status": None,
          "type": "invite"
        }

        return response(200, content, headers)
