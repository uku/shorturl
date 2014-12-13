#!/usr/bin/env python

from tornado.testing import AsyncTestCase
import analytics
from config import ANALYTICS_ID


class AnalyticsTest(AsyncTestCase):
    def test_report_pageview(self):
        ga = analytics.Analytics(ANALYTICS_ID)
        code = ga.report_pageview('/unit-test')
        self.assertEqual(code, 200)

    def test_report_pageview_extra_info(self):
        ga = analytics.Analytics(ANALYTICS_ID)
        code = ga.report_pageview('/unit-test', '/', '127.0.0.1', 'Test-Agent')
        self.assertEqual(code, 200)
