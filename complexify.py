#!/usr/bin/python

import urllib

from parse import parse

if __name__ == '__main__':
    import sys
    p = parse(sys.argv[1])
    lst = list(p.describe())
    for l in lst:
        print l
    print 'self.assertEquals('
    print '    %s,' % repr(lst)
    print '    list(parse(%s).describe()))' % repr(sys.argv[1])
    url = 'http://oanda.sca.org/oanda_complex.cgi?'
    idx = 1
    for l in lst:
        url += 'w%d=1&m%d=armory+description&p%d=' % (idx, idx, idx)
        url += urllib.quote_plus(l)
        url += '&'
        idx += 1
    url += 'a=enabled'
    print url
