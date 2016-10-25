#!/usr/bin/env python
# -*- coding: utf-8 -*-

from faker import Factory
from surveymonkey.surveymonkey import SurveyMonkeyConnection


def create_fake_connection():
    fake = Factory.create()
    ACCESS_TOKEN = fake.password(
        length=50, special_chars=True, digits=True,
        upper_case=True, lower_case=True
    )
    API_KEY = fake.password(
        length=12, digits=True, special_chars=False,
        upper_case=True, lower_case=True
    )
    connection = SurveyMonkeyConnection(ACCESS_TOKEN, API_KEY)

    return ACCESS_TOKEN, API_KEY, connection
