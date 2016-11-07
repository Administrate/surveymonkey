# -*- coding: utf-8 -*-
from __future__ import absolute_import

import six

from surveymonkey.manager import BaseManager
from surveymonkey.webhooks.constants import SURVEY
from surveymonkey.constants import URL_WEBHOOKS


class Webhook(BaseManager):

    def create_for_survey(self, event_type, object_ids, subscription_url):
        object_ids = [object_ids] if isinstance(object_ids, six.string_types) else object_ids

        return self.post(
            base_url=URL_WEBHOOKS,
            data={
                "event_type": event_type,
                "object_type": SURVEY,
                "object_ids": object_ids,
                "subscription_url": subscription_url
            }
        )
