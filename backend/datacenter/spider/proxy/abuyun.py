# -*- encoding:utf-8 -*-

import requests

def abuyunGet(targetUrl, headers={}):
    proxyHost = 'proxy.abuyun.com'
    proxyPort = '9010'

    proxyUser = 'H363M865K488A2GP'
    proxyPass = '8267463595761AF3'

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host" : proxyHost,
        "port" : proxyPort,
        "user" : proxyUser,
        "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }

    print proxyMeta
    resp = requests.get(targetUrl, headers=headers, proxies=proxies, timeout=10)

    return resp
