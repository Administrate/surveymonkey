# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

import math
from datetime import datetime
from random import randint

from furl import furl
from delorean import Delorean


def create_quota_headers(qpd=None, qps=None, reset=datetime.now()):
    qpd_allotted, qpd_current = qpd if qpd else (10000, randint(1, 9000))
    qps_allotted, qps_current = qps if qps else (8, randint(1, 5))

    reset = Delorean(datetime=reset,  timezone='UTC').datetime

    return {
        'X-Plan-QPS-Allotted': qps_allotted,
        'X-Plan-QPS-Current': qps_current,
        'X-Plan-Quota-Allotted': qpd_allotted,
        'X-Plan-Quota-Current': qpd_current,
        'X-Plan-Quota-Reset': reset.strftime("%A, %B %d, %Y %I:%M:%S %p %Z")
    }


class BaseListMock(object):

    def __init__(self, total=125, base_url=None):
        self.total = total
        self.base_url = base_url

    def get_links(self, per_page, current_page, pages):
        last_page = pages

        def _clean_base_url(url):  # Prevent duplicate qs params
            return furl(url).remove(['per_page', 'current_page', 'pages']).copy()

        links = dict()
        links["self"] = _clean_base_url(self.base_url).add({
            "per_page": per_page,
            "page": current_page
        }).url

        if last_page > 1:
            if current_page != last_page:
                links["last"] = _clean_base_url(self.base_url).add({
                    "per_page": per_page,
                    "page": current_page
                }).url

                if current_page < last_page:
                    links["next"] = _clean_base_url(self.base_url).add({
                        "per_page": per_page,
                        "page": current_page + 1
                    }).url
            if current_page != 1:
                links["first"] = _clean_base_url(self.base_url).add({
                    "per_page": per_page,
                    "page": 1
                }).url
                links["prev"] = _clean_base_url(self.base_url).add({
                    "per_page": per_page,
                    "page": current_page - 1
                }).url

        return links

    def calculate_number_remaining(self, per_page, current_page):
        if current_page == 1:
            return self.total
        else:
            total_done = (current_page - 1) * per_page
            total_remaining = self.total - total_done
            return 0 if total_remaining <= 0 else total_remaining

    def parse_url(self, url):
        url = furl(url.geturl())
        per_page = int(url.args.get("per_page", 50))
        current_page = int(url.args.get("page", 1))
        pages = math.ceil(self.total / per_page)
        return per_page, current_page, pages

    def create_item(self):
        raise NotImplementedError("Implemented in subclass")

    def create_items(self, per_page, current_page, pages):
        items = []
        remaining = self.calculate_number_remaining(per_page, current_page)

        if remaining > 0:
            remaining = remaining if remaining < per_page else per_page
            for x in range(0, remaining):
                item = self.create_item()
                items.append(item)

        return items
