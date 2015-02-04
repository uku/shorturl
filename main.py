#!/usr/bin/env python

import os
# import urlparse
import tornado.ioloop
import tornado.web
import tornado.httpserver
from raven.contrib.tornado import AsyncSentryClient, SentryMixin

from config import ANALYTICS_ID, HOMEPAGE_URL, \
    SHORT_URL_MAPPING, IGNORED_SHORT_URLS

from analytics import Analytics
analytics_client = Analytics(ANALYTICS_ID)


def construct_long_url(base_url, request_uri, short):
    extra_part = request_uri[len(short) + 1:]
    if len(extra_part) > 0:
        if base_url[-1] == '/' and extra_part[0] == '/':
            long_url = base_url + extra_part[1:]
        else:
            long_url = base_url + extra_part
    else:
        long_url = base_url

    return long_url


class ShortUrlHandler(SentryMixin, tornado.web.RequestHandler):
    def get(self):
        path_sections = self.request.path.split('/')
        if len(path_sections) > 1:
            short = path_sections[1]
        else:
            short = ''

        if len(short) == 0:
            self.redirect(HOMEPAGE_URL, permanent=True)

        elif short in SHORT_URL_MAPPING:
            long_url = construct_long_url(SHORT_URL_MAPPING[short],
                                          self.request.uri, short)
            self.redirect(long_url, permanent=True)

        else:
            self.send_error(404)
            if SENTRY_DSN is not None and short not in IGNORED_SHORT_URLS:
                # self.captureMessage('Unmapped URL: ' + self.request.uri)
                pass

        if short not in IGNORED_SHORT_URLS:
            analytics_client.report_pageview(
                uri=self.request.uri,
                referer=self.request.headers.get('Referer'),
                user_ip=self.request.remote_ip,
                user_agent=self.request.headers.get('User-Agent')
            )

    head = get


application = tornado.web.Application([
    (r"/.*", ShortUrlHandler),
])
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN is not None:
    application.sentry_client = AsyncSentryClient(SENTRY_DSN)


if __name__ == "__main__":
    http_port = int(os.environ.get("PORT", 8888))
    application.listen(http_port)
    tornado.ioloop.IOLoop.instance().start()
