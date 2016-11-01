#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from expects import expect, have_key
from httmock import HTTMock

from surveymonkey.messages import Message, InviteConfig
from surveymonkey.tests.messages.matchers.messages import be_sent, be_invite
from ..mocks.messages import MessagesMock
from ..utils import create_fake_connection


class TestCreateMessages(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.API_KEY, self.connection = create_fake_connection()
        self.collector_id = random.randint(1234, 567890)

    def setup_method(self, method):
        pass

    def test_invite_created(self):
        config = InviteConfig()
        message = Message(connection=self.connection, collector=self.collector_id, config=config)

        with HTTMock(MessagesMock(config).create):
            invite = message.create()

        expect(invite).to_not(be_sent)
        expect(invite).to(be_invite)
        expect(invite).to(have_key("id"))
