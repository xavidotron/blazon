#!/usr/bin/python

import os, sys, codecs
import re

def blazons_from(fname):
    encoding_pat = re.compile(r'<td>([^<>]+)</td><td>[^<>]+</td><td>[^<>]+</td><td>([^<>]+)')
    encodings = {}
    with codecs.open('data_symbols.html', encoding='utf-8') as fil:
        for l in fil:
            m = encoding_pat.search(l)
            if m:
                encodings[m.group(1)] = m.group(2)

    daud_pat = re.compile(r'\{([^}]+)\}')

    with open(fname) as fil:
        build = []
        for l in fil:
            if l.startswith('  ') and not l.startswith('   '):
                build.append(l.strip())
            elif build:
                entry = ' '.join(build)
                parts = entry.split('. ')
                if len(parts) > 2:
                    blaz = unicode(parts[2])
                    blaz = daud_pat.sub(lambda m: encodings[m.group(1)], blaz)
                    yield blaz
                build = []

def add_entry(typ, entry):
    with codecs.open('%s.txt' % typ, 'a', encoding='utf-8') as fil:
        print 'Adding "%s" to the %s list.' % (entry, typ)
        fil.write(entry + '\n')

def prompt_for_edit(e):
    word = e.word
    options = e.options
    print
    if e.dym:
        for d in e.dym:
            print d
        print
    print 'a. Treat "%s" as an alias for a charge.' % word
    print 'd. Treat "%s" as detail.' % word
    if e.blist:
        print 'd2. Treat "%s %s" as detail.' % (word, e.blist[0])
        if len(e.blist) > 1:
            print 'd3. Treat "%s %s %s" as detail.' % (word, e.blist[0], 
                                                       e.blist[1])
    if options:
        for i in xrange(len(options)):
            print '%s. %s' % (i+1, options[i])
        if len(options) == 2:
            print 'b. both'
    print 'x. quit'
    action = raw_input("Action: ")
    if action.startswith('a'):
        import words
        charge = None
        while not charge or charge not in words.CHARGES:
            if charge:
                print "%s is not a charge!" % charge
            charge = raw_input("Specify charge: ")
        add_entry('aliases', '%s: %s' % (words.CHARGES[charge].name, word))
    elif action.startswith('d'):
        entry = word
        if len(action) > 1:
            entry += ' ' + ' '.join(e.blist[:int(action[1:]) - 1])
        add_entry('details', entry)
    elif action.isdigit():
        i = int(action) - 1
        add_entry('aliases', '%s: %s' % (options[i], word))
    elif action == 'b':
        assert False
    else:
        sys.exit(1)
    os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == '__main__':
    import traceback
    from parse import parse, BlazonException
    from complexify import url_for

    verbose = False

    for b in blazons_from(sys.argv[1]):
        try:
            lst = list(parse(b).describe())
        except BlazonException, e:
            print b
            if e.word:
                traceback.print_exc()
                prompt_for_edit(e)
                print
            else:
                raise
        else:
            if verbose:
                print lst
                print url_for(lst)
                print