# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects.matchers import Matcher


class BeEmail(Matcher):
    def _match(self, response):
        return response["type"] == "email", []


class BeWeblink(Matcher):
    def _match(self, response):
        return response["type"] == "weblink", []


class BeOpen(Matcher):
    def _match(self, response):
        return response["status"] == "open", []


class BeClosed(Matcher):
    def _match(self, response):
        return response["status"] == "closed", []


class BeNew(Matcher):
    def _match(self, response):
        return response["status"] == "new", []


be_email = BeEmail()
be_weblink = BeWeblink()
be_open = BeOpen()
be_closed = BeClosed()
be_new = BeNew()

__all__ = ['be_email', 'be_weblink', 'be_open', 'be_closed', 'be_new']
