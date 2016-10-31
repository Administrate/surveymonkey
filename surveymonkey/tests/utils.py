#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
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


def weighted_choice(choices):
    return random.choice(choices)[0]
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
