#!/usr/bin/env python

import os
import urlparse
import tornado.ioloop
import tornado.web
import tornado.httpserver
from raven.contrib.tornado import AsyncSentryClient, SentryMixin

from config import ANALYTICS_ID, HOMEPAGE_URL, SHORT_URL_MAPPING

from analytics import Analytics
analytics_client = Analytics(ANALYTICS_ID)


class ShortUrlHandler(SentryMixin, tornado.web.RequestHandler):
    def get(self):
        short = self.request.path.lstrip('/')
        if len(short) == 0:
            self.redirect(HOMEPAGE_URL, permanent=True)
        elif short in ('favicon.ico', 'robots.txt',
                       'sitemap.xml', 'unit-test'):
            self.send_error(404)
        elif short in SHORT_URL_MAPPING:
            long_url = SHORT_URL_MAPPING[short]
            # http://stackoverflow.com/a/9538343/1766096
            if len(self.request.query) > 0:
                if urlparse.urlparse(long_url)[4]:
                    long_url += '&' + self.request.query
                else:
                    long_url += '?' + self.request.query
            self.redirect(long_url, permanent=True)
        else:
            self.send_error(404)
            self.captureMessage('Unmapped URL: ' + self.request.uri)

        analytics_client.report_pageview(
            uri=self.request.uri,
            referer=self.request.headers.get('Referer'),
            user_ip=self.request.remote_ip,
            user_agent=self.request.headers.get('User-Agent')
        )


application = tornado.web.Application([
    (r"/.*", ShortUrlHandler),
])
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN is not None:
    application.sentry_client = AsyncSentryClient(SENTRY_DSN)


def main():
    http_server = tornado.httpserver.HTTPServer(application)
    http_port = int(os.environ.get("PORT", 8888))
    http_server.bind(http_port)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
