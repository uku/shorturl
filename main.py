#!/usr/bin/env python

import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
from raven.contrib.tornado import AsyncSentryClient, SentryMixin

from config import ANALYTICS_ID, HOMEPAGE_URL, SHORT_URL_MAPPING

from analytics import Analytics
analytics_client = Analytics(ANALYTICS_ID)


class ShortUrlHandler(SentryMixin, tornado.web.RequestHandler):
    def get(self):
        short = self.request.uri.lstrip('/')
        if len(short) == 0:
            self.redirect(HOMEPAGE_URL, permanent=True)
        else:
            if short in SHORT_URL_MAPPING:
                self.redirect(SHORT_URL_MAPPING[short], permanent=True)
            else:
                self.send_error(404)

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
