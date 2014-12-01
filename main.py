#!/usr/bin/env python

import os
import tornado.ioloop
import tornado.web
import tornado.httpserver

# from tornado.web.RequestHandler import redirect
from tornado.web import RedirectHandler


class ShortUrlHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


application = tornado.web.Application([
    (r"/", RedirectHandler, dict(url=HOMEPAGE_URL)),
    (r"/.*", ShortUrlHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_port = int(os.environ.get("PORT", 5000))
    http_server.bind(http_port)
    http_server.start()
    tornado.ioloop.IOLoop.instance().start()
