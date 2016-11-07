#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
from faker import Factory
from surveymonkey.surveymonkey import SurveyMonkeyConnection


def create_fake_connection():
    fake = Factory.create()
    ACCESS_TOKEN = fake.password(
        length=50, special_chars=True, digits=True,
        upper_case=True, lower_case=True
    )
    connection = SurveyMonkeyConnection(ACCESS_TOKEN)

    return ACCESS_TOKEN, connection


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
