#!/usr/bin/python
# -*- coding: latin-1 -*-
 # -*- coding: ascii -*-
# -*- coding: iso-8859-15 -*-

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


import re
import htmlentitydefs

def convertentity(m):
    if m.group(1)=='#':
        try:
            return unichr(int(m.group(2)))
        except ValueError:
            return '&#%s;' % m.group(2)
        try:
            return htmlentitydefs.entitydefs[m.group(2)]
        except KeyError:
            return '&%s;' % m.group(2)

def converthtml(s):
    return re.sub(r'&(#?)(.+?);',convertentity,s)

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def removeHtmlTags(data):
    return remove_html_tags(data)
    return strip_tags(html)
    return converthtml(html)


if __name__ == "__main__":
    x1 = remove_html_tags(html)
    print x1
    sys.exit()


    x1 = strip_tags(html)
    print x1

    x2 =  converthtml(html)
    print x2
    x2.replace("&nbsp;", " ") ## Get rid of the remnants of cer