#!/usr/bin/env python

from tornado.testing import AsyncTestCase
import config


class TestConfigFile(AsyncTestCase):
    def test_duplciate_maps(self):
        mapping = config.SHORT_URL_MAPPING
        keys = set(mapping.keys())
        vals = set(mapping.values())
        self.assertEqual(len(keys), len(vals))

    def test_homepage_url(self):
        self.assertIn('http', config.HOMEPAGE_URL)

    def test_analytics_id(self):
        self.assertIn('UA-', config.ANALYTICS_ID)
