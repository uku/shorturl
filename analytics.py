#!/usr/bin/env python

import random
import uuid

# cannot use tornado.httpclient.AsyncHTTPClient (see http://git.io/EUDgzw)
import requests


class Analytics:
    def __init__(self, tracking_id):
        assert tracking_id.startswith('UA-')
        self.tracking_id = tracking_id

    def report_pageview(self, uri,
                        referer=None, user_ip=None, user_agent=None):
        rand = str(random.randrange(1 << 128))
        rand_uuid = str(uuid.uuid4())  # random uuid

        payload = {
            'v': '1',
            'z': rand,  # cache buster
            'cid': rand_uuid,  # treat every hit as an independent one
            'tid': self.tracking_id,
            'aip': '1',  # anonymize IP
            'dp': uri,
            'uip': '127.0.0.1'  # default
        }
        if referer:
            payload['dr'] = referer
        if user_ip:
            payload['uip'] = user_ip
        if user_agent:
            payload['ua'] = user_agent

        requests.post('https://ssl.google-analytics.com/collect', data=payload)


def main():
    from config import ANALYTICS_ID

    analytics = Analytics(ANALYTICS_ID)
    analytics.report_pageview('/test')


if __name__ == '__main__':
    main()
