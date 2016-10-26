# -*- coding: utf-8 -*-
from __future__ import division

from six.moves.urllib.parse import parse_qs

import math
from datetime import datetime
from random import randint

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

        links = dict()
        links["self"] = "{base_url}?page={page}&per_page={per_page}".format(
            base_url=self.base_url,
            page=current_page,
            per_page=per_page
        )

        if last_page > 1:
            if current_page != last_page:
                links["last"] = "{base_url}?page={current_page}&per_page={per_page}".format(
                    base_url=self.base_url,
                    current_page=current_page,
                    per_page=per_page
                )
                if current_page < last_page:
                    links["next"] = "{base_url}?page={next_page}&per_page={per_page}".format(
                        base_url=self.base_url,
                        next_page=current_page + 1,
                        per_page=per_page
                    )
            if current_page != 1:
                links["first"] = "{base_url}?page=1&per_page={per_page}".format(
                    base_url=self.base_url,
                    per_page=per_page
                )
                links["prev"] = "{base_url}?page={prev_page}&per_page={per_page}".format(
                    base_url=self.base_url,
                    prev_page=current_page - 1,
                    per_page=per_page
                )

        return links

    def calculate_number_remaining(self, per_page, current_page):
        if current_page == 1:
            return self.total
        else:
            total_done = (current_page - 1) * per_page
            total_remaining = self.total - total_done
            return 0 if total_remaining <= 0 else total_remaining

    def parse_url(self, url):
        qs = dict(parse_qs(url.query))

        per_page = int(qs.get("per_page", ['50'])[0])
        current_page = int(qs.get("page", ['1'])[0])
        pages = math.ceil(self.total / per_page)

        return per_page, current_page, pages
