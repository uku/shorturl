#!/usr/bin/env python

from tornado.testing import AsyncTestCase
import analytics
from config import ANALYTICS_ID


class AnalyticsTest(AsyncTestCase):
    def test_report_pageview(self):
        ga = analytics.Analytics(ANALYTICS_ID)
        code = ga.report_pageview('/unit-test')
        self.assertEqual(code, 200)
