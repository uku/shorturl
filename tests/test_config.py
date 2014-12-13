#!/usr/bin/env python

from tornado.testing import AsyncTestCase
import config


class TestConfigFile(AsyncTestCase):
    def test_duplciate_maps(self):
        mapping = config.SHORT_URL_MAPPING
        self.assertIn('httpbin', mapping['httpbin'])

    def test_homepage_url(self):
        self.assertIn('http', config.HOMEPAGE_URL)

    def test_analytics_id(self):
        self.assertIn('UA-', config.ANALYTICS_ID)
