#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from faker import Faker


@pytest.fixture(scope="module")
def faker():
    return Faker()
