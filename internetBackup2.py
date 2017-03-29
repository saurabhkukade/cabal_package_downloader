#!/usr/bin/python

import urllib2, re, sys

pkgName = sys.argv[1]

def cleanhtml(raw_html):
    cleanr =re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', raw_html)
    return cleantext
    
req = urllib2.Request("http://hackage.haskell.org/package/"+pkgName)
response = urllib2.urlopen(req)
page = response.read()
cleantext = cleanhtml(page)
for line in cleantext.split('\n'):
    print line
