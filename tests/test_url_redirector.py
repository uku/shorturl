#!/usr/bin/env python

from tornado.testing import AsyncHTTPTestCase
import main


class UrlRedirectorTest(AsyncHTTPTestCase):
    def get_app(self):
        return main.application

    # def test_homepage(self):
    #     response = self.fetch('/')
    #     self.assertIn('Unblock', response.body)

    # def test_redirect(self):
    #     response = self.fetch('/dns')
    #     self.assertIn('Unblock', response.body)

    def test_nonexist(self):
        response = self.fetch('/unit-test')
        self.assertEqual(404, response.code)
