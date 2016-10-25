# -*- coding: utf-8 -*-

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
