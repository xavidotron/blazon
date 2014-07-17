#!/usr/bin/python

import urllib

from parse import parse

def url_for(lst):
    url = 'http://oanda.sca.org/oanda_complex.cgi?'
    idx = 1
    for l in lst:
        url += 'w%d=1&m%d=armory+description&p%d=' % (idx, idx, idx)
        url += urllib.quote_plus(l)
        url += '&'
        idx += 1
    url += 'a=enabled'
    return url

if __name__ == '__main__':
    import sys
    blaz = unicode(sys.argv[1], 'utf-8')
    p = parse(blaz)
    lst = list(p.describe())
    for l in lst:
        print l
    print '        self.assertEquals('
    print '            %s,' % repr(lst).replace(', ', ',\n             ')
    print '            list(parse(%s).describe()))' % repr(blaz)
    print url_for(lst)
