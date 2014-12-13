#!/usr/bin/env python

from tornado.testing import AsyncHTTPTestCase
import main


class UrlRedirectorTest(AsyncHTTPTestCase):
    def get_app(self):
        return main.application

    def test_homepage(self):
        response = self.fetch('/')
        self.assertIn('Unblock', response.body)

    def test_redirect(self):
        response = self.fetch('/dns')
        self.assertIn('Unblock', response.body)

    def test_nonexist(self):
        response = self.fetch('/unit-test')
        self.assertEqual(404, response.code)

    def test_favicon_ico(self):
        response = self.fetch('/favicon.ico')
        self.assertEqual(404, response.code)

    def test_with_query(self):
        response = self.fetch('/httpbin?query-string=1')
        self.assertIn('"query-string": "1"', response.body)
