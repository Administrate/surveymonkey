# -*- coding: utf-8 -*-

import json
import random
from faker import Faker
from httmock import urlmatch


class UsersResponseMocks(object):

    def __init__(self):
        self.fake = Faker()

    @urlmatch(path="/v3/users/me")
    def me(self, url, request):
        return {
            "status_code": 200,
            "content": json.dumps({
                "id": str(random.randint(1, 9000)),
                "username": self.fake.user_name(),
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "language": "en",
                "email": self.fake.safe_email(),
                "account_type": "enterprise_platinum",
                "date_created": self.fake.iso8601(tzinfo=None),
                "date_last_login": self.fake.iso8601(tzinfo=None)
            })
        }
