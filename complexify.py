import urllib

from parse import parse

if __name__ == '__main__':
    import sys
    p = parse(sys.argv[1])
    lst = list(p.describe())
    for l in lst:
        print l
    url = 'http://oanda.sca.org/oanda_complex.cgi?'
    idx = 1
    for l in lst:
        url += 'w%d=1&m%d=armory+description&p%d=' % (idx, idx, idx)
        url += urllib.quote_plus(l)
        url += '&'
        idx += 1
    print url[:-1]
