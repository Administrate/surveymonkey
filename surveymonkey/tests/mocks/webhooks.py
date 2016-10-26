# -*- coding: utf-8 -*-

import random
from faker import Faker
from httmock import urlmatch, response
from .utils import create_quota_headers

from surveymonkey.constants import URL_WEBHOOKS


class WebhookMock(object):

    def __init__(self, event_type, object_type, object_ids, subscription_url):
        self.event_type = event_type
        self.object_type = object_type
        self.object_ids = object_ids
        self.subscription_url = subscription_url
        self.fake = Faker()

    @urlmatch(path="/v3/webhooks")
    def create(self, url, request):
        id = str(random.randint(1, 9000))
        headers = create_quota_headers()
        content = {
            "id": id,
            "name": self.fake.catch_phrase(),
            "event_type": self.event_type,
            "object_ids": self.object_ids,
            "subscription_url": self.subscription_url,
            "href": "{base_url}/{id}".format(base_url=URL_WEBHOOKS, id=id)
        }

        return response(200, content, headers)
