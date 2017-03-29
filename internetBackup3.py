#!/usr/bin/python

import urllib2, re, sys
import requests
from requests.exceptions import HTTPError

pkgName = sys.argv[1]

def cleanHtml(raw_html):
    clean = re.compile('<.*?>')
    cleanText = re.sub(clean,'', raw_html)
    return cleanText

try:
    url = "http://hackage.haskell.org/package/"+pkgName
    req = urllib2.Request(url)
    handle = urllib2.urlopen(req)
    page = handle.read()
    cleanText = cleanHtml(page)
    for line in cleanText.split('\n'):
            print line
except urllib2.HTTPError, e:
    if e.code == 404:
        print "Not Found"
