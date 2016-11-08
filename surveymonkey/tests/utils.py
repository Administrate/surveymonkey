#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
from faker import Factory
from surveymonkey.surveymonkey import SurveyMonkeyConnection


def create_fake_connection():
    fake = Factory.create()
    access_token = fake.password(
        length=50, special_chars=True, digits=True,
        upper_case=True, lower_case=True
    )
    connection = SurveyMonkeyConnection(access_token)

    return access_token, connection


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
