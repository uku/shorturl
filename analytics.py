#!/usr/bin/env python

import random
import urllib
import uuid
import tornado.httpclient


class Analytics:
    def __init__(self, tracking_id):
        assert tracking_id.startswith('UA-')
        self.tracking_id = tracking_id
        self.http_client = tornado.httpclient.AsyncHTTPClient()

    def report_pageview(self, uri,
                        referer=None, user_ip=None, user_agent=None):
        rand = str(random.randrange(1 << 128))
        rand_uuid = str(uuid.uuid4())  # random uuid

        payload_dict = {
            'v': '1',
            'z': rand,  # cache buster
            'cid': rand_uuid,  # treat every hit as an independent one
            'tid': self.tracking_id,
            'aip': '1',  # anonymize IP
            'dp': uri,
            'uip': '127.0.0.1'  # default
        }
        if referer:
            payload_dict['dr'] = referer
        if user_ip:
            payload_dict['uip'] = user_ip
        if user_agent:
            payload_dict['ua'] = user_agent
        payload = urllib.urlencode(payload_dict)

        request = tornado.httpclient.HTTPRequest(
            url='https://ssl.google-analytics.com/collect',
            method='POST',
            body=payload
        )
        self.http_client.fetch(request, raise_error=True)


def main():
    from config import ANALYTICS_ID

    analytics = Analytics(ANALYTICS_ID)
    analytics.report_pageview('/test')


if __name__ == '__main__':
    main()
