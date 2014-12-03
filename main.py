#!/usr/bin/env python

import os
import tornado.ioloop
import tornado.web
import tornado.httpserver

from tornado.web.RequestHandler import request, redirect, send_error
from config import HOMEPAGE_URL, SHORT_URL_MAPPING


class ShortUrlHandler(tornado.web.RequestHandler):
    def get(self):
        uri = request.uri.lstrip('/')
        if len(uri) == 0:
            redirect(HOMEPAGE_URL, permanent=True)
        else:
            if uri in SHORT_URL_MAPPING:
                redirect(SHORT_URL_MAPPING[uri], permanent=True)
            else:
                send_error(404)


application = tornado.web.Application([
    (r"/.*", ShortUrlHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_port = int(os.environ.get("PORT", 5000))
    http_server.bind(http_port)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()
