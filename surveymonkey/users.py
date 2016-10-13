# -*- coding: utf-8 -*-

from .manager import BaseManager
from .constants import URL_USER_ME


class Users(BaseManager):

    def me(self):
        response = self.get(URL_USER_ME)
        return response
