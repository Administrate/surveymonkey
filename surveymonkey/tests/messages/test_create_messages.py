#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pytest

from faker import Faker
from expects import expect, have_key, have_length, be_above_or_equal
from httmock import HTTMock

from surveymonkey.messages import Message, InviteConfig
from surveymonkey.tests.messages.matchers.messages import be_sent, be_invite
from ..mocks.messages import MessagesMock, MessagesRecipientsMock
from ..utils import create_fake_connection


class TestCreateMessages(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()
        self.collector_id = random.randint(1234, 567890)

    def setup_method(self, method):
        pass

    def test_invite_created(self):
        config = InviteConfig()
        message = Message(
            connection=self.connection,
            collector_id=self.collector_id,
            config=config
        )

        with HTTMock(MessagesMock(config).create):
            invite = message.create()

        expect(invite).to_not(be_sent)
        expect(invite).to(be_invite)
        expect(invite).to(have_key("id"))


class RecipientLists(object):

    def __init__(self):
        self.fake = Faker()

    def valid(self):
        return [
            [{'name': self.fake.name(), 'email': self.fake.safe_email()}],
            [
                {
                    'name': self.fake.name(),
                    'email': self.fake.safe_email()
                } for x in range(1, random.randint(3, 10))
            ]
        ]

    def _invalidate_recipient_list(self, key, invalid_values):
        recipients = self.valid()
        random.shuffle(invalid_values)
        recipients[0][0][key] = invalid_values[0]
        recipients[1][0][key] = invalid_values[1]
        random.shuffle(recipients[1])
        return recipients

    def missing_email_value(self):
        return self._invalidate_recipient_list(
            "email",
            [None, ""]
        )

    def missing_name_value(self):
        return self._invalidate_recipient_list(
            "name",
            [None, ""]
        )

    def _delete_key(self, key):
        recipients = self.valid()
        recipients[0][0].pop(key)
        recipients[1][0].pop(key)
        random.shuffle(recipients[1])
        return recipients

    def missing_email_key(self):
        return self._delete_key("email")

    def missing_name_key(self):
        return self._delete_key("name")

recipient_lists = RecipientLists()


class TestAddRecipients(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()
        self.config = InviteConfig()
        self.collector_id = random.randint(1234, 567890)
        self.message_id = random.randint(1234, 567890)
        self.mock = MessagesRecipientsMock()

    @pytest.mark.parametrize("recipients", recipient_lists.valid())
    def test_add_recipients_to_existing_message(self, recipients):
        message = Message(
            connection=self.connection,
            collector_id=self.collector_id,
            message_id=self.message_id,
        )

        with HTTMock(self.mock.recipient_add):
            response = message.recipients(recipients)

        expect(response["succeeded"]).to(have_length(be_above_or_equal(1)))

    @pytest.mark.parametrize("recipients", recipient_lists.valid())
    def test_create_new_message_and_add_a_recipients(self, recipients):
        message = Message(
            connection=self.connection,
            collector_id=self.collector_id,
            config=self.config
        )

        with HTTMock(MessagesMock(self.config).create):
            message.create()

        with HTTMock(self.mock.recipient_add):
            response = message.recipients(recipients)

        expect(response["succeeded"]).to(have_length(be_above_or_equal(1)))

    @pytest.mark.parametrize("recipients", recipient_lists.valid())
    def test_exception_raised_when_no_message_id_is_provided_and_message_is_not_newly_created(self, recipients):  # noqa:E501
        message = Message(
            connection=self.connection,
            collector_id=self.collector_id,
        )

        with HTTMock(self.mock.recipient_add):
            with pytest.raises(AttributeError):
                message.recipients(recipients)

    @pytest.mark.parametrize("recipients", recipient_lists.missing_email_value())
    def test_exception_raised_when_recipient_has_empty_email(self, recipients):
        message = Message(
            connection=self.connection,
            collector_id=self.collector_id,
            message_id=self.message_id,
        )

        with HTTMock(self.mock.recipient_add):
            with pytest.raises(ValueError):
                message.recipients(recipients)

    @pytest.mark.parametrize("recipients", recipient_lists.missing_name_value())
    def test_exception_raised_when_recipient_has_empty_name(self, recipients):
        message = Message(
            connection=self.connection,
            collector_id=self.collector_id,
            message_id=self.message_id,
        )

        with HTTMock(self.mock.recipient_add):
            with pytest.raises(ValueError):
                message.recipients(recipients)

    @pytest.mark.parametrize("recipients", recipient_lists.missing_name_key())
    def test_exception_raised_when_recipient_dictionary_is_missing_name_key(self, recipients):
        message = Message(
            connection=self.connection,
            collector_id=self.collector_id,
            message_id=self.message_id,
        )

        with HTTMock(self.mock.recipient_add):
            with pytest.raises(KeyError):
                message.recipients(recipients)

    @pytest.mark.parametrize("recipients", recipient_lists.missing_email_key())
    def test_exception_raised_when_recipient_dictionary_is_missing_email_key(self, recipients):
        message = Message(
            connection=self.connection,
            collector_id=self.collector_id,
            message_id=self.message_id,
        )

        with HTTMock(self.mock.recipient_add):
            with pytest.raises(KeyError):
                message.recipients(recipients)
