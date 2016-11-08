# -*- coding: utf-8 -*-

from ..manager import BaseManager
from ..constants import URL_MESSAGE_CREATE, URL_MESSAGE_RECIPIENT_ADD_BULK, URL_MESSAGE_SEND


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
            data={"type": self.config.type}
        )
        self.message_id = response["id"]
        return response

    def validate_recipient(self, recipient):
        if "email" and "name" in recipient:
            if not recipient["email"] or not recipient["name"]:
                raise ValueError
        else:
            raise KeyError

    def recipients(self, recipients_list):
        contacts = []

        if not self.message_id:
            raise AttributeError

        for recipient in recipients_list:
            self.validate_recipient(recipient)

            contacts.append({
                "email": recipient["email"],
                "custom_fields": {
                    "1": recipient["name"]
                }
            })

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
