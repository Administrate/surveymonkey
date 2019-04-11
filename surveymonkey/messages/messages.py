# -*- coding: utf-8 -*-
from __future__ import absolute_import

import six
from surveymonkey.manager import BaseManager
from surveymonkey.constants import (URL_MESSAGE_CREATE, URL_MESSAGE_RECIPIENT_ADD_BULK,
                                    URL_MESSAGE_SEND)


class Message(BaseManager):

    def __init__(self, connection, collector_id, message_id=None, config=None):
        super(Message, self).__init__(connection)
        self.config = config
        self.collector_id = collector_id
        self.message_id = message_id

    def create(self):
        url = URL_MESSAGE_CREATE.format(
            collector_id=self.collector_id
        )
        response = self.post(
            base_url=url,
            data=self.config.vars()
        )
        self.message_id = response["id"]
        return response

    @staticmethod
    def validate_recipient(recipient, custom_field_mapping, extra_field_mapping):
        custom_field_keys = list(custom_field_mapping.values()) if custom_field_mapping else []
        extra_field_keys = list(extra_field_mapping.values()) if extra_field_mapping else []
        for key in ['email'] + custom_field_keys + extra_field_keys:
            if key in recipient:
                if not recipient[key]:
                    raise ValueError
            else:
                raise KeyError

    @staticmethod
    def add_custom_fields(contact, recipient, custom_field_mapping):
        if custom_field_mapping:
            contact['custom_fields'] = {
                field_number: str(recipient[field_key]) for field_number, field_key in six.iteritems(custom_field_mapping)  # noqa:E501
            }

    @staticmethod
    def add_extra_fields(contact, recipient, extra_field_mapping):
        if extra_field_mapping:
            contact['extra_fields'] = {
                field_name: str(recipient[field_key]) for field_name, field_key in six.iteritems(extra_field_mapping)  # noqa:E501
            }

    def recipients(self, recipients_list, custom_field_mapping=None, extra_field_mapping=None):
        contacts = []

        if not self.message_id:
            raise AttributeError

        print("\ntest message\n")

        for recipient in recipients_list:
            self.validate_recipient(recipient, custom_field_mapping, extra_field_mapping)
            contact = {'email': recipient["email"]}
            self.add_custom_fields(contact, recipient, custom_field_mapping)
            self.add_extra_fields(contact, recipient, extra_field_mapping)
            contacts.append(contact)

        url = URL_MESSAGE_RECIPIENT_ADD_BULK.format(
            collector_id=self.collector_id,
            message_id=self.message_id
        )

        return self.post(
            base_url=url,
            data={'contacts': contacts}
        )

    def send(self, scheduled_date=None):
        if not self.message_id:
            raise AttributeError

        if scheduled_date:
            scheduled_date_string = scheduled_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")
            data = {"scheduled_date": scheduled_date_string}
        else:
            data = {}

        url = URL_MESSAGE_SEND.format(
            collector_id=self.collector_id,
            message_id=self.message_id
        )

        return self.post(base_url=url, data=data)
