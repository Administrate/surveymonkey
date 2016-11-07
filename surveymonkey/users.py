# -*- coding: utf-8 -*-
from __future__ import absolute_import

from surveymonkey.manager import BaseManager
from surveymonkey.constants import URL_USER_ME


class Users(BaseManager):

    def me(self):
        response = self.get(URL_USER_ME)
        return response
