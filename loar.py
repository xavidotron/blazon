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

def prompt_n(letter, pattern, word, blist):
    global idx
    from parse import PLURALS
    from words import (TINCTURES, SMALL_WORDS, ALL_WORDS, NUMBERS, CHARGES, 
                       COUNTERCHANGEDS)
    idx = 0
    opts = {}
    def opt(wd):
        global idx
        if wd in ALL_WORDS or wd.split()[-1] in SMALL_WORDS:
            return False
        if (' ' in wd and wd.split(' ', 1)[0] in NUMBERS 
            and wd.split(' ', 1)[-1] in CHARGES):
            return False
        itag = str(idx) if idx else ''
        print letter + itag + '.', pattern % wd
        opts[letter + itag] = (letter, wd)
        idx += 1
        return True
    def opt_pl(wd):
        if opt(wd):
            for suf, repl in PLURALS:
                if (wd.endswith(suf)
                    and (wd[:-len(suf)] + repl in ALL_WORDS
                         or wd.split()[-1][:-len(suf)] + repl in ALL_WORDS)):
                    opt(wd[:-len(suf)] + repl)
                    break
            else:
                if wd not in ALL_WORDS:
                    for suf, repl in PLURALS:
                        if wd.endswith(suf):
                            opt(wd[:-len(suf)] + repl)

            if ' ' not in wd:
                return
            for suf, repl in PLURALS:
                if wd.split(' ')[0].endswith(suf):
                    first, rest = wd.split(' ', 1)
                    if (first[:-len(suf)] + repl in ALL_WORDS 
                        or first[:-len(suf)] + repl + ' ' + rest in ALL_WORDS):
                        opt(first[:-len(suf)] + repl + ' ' + rest)
                        break
            else:
                if wd.split(' ')[0] not in ALL_WORDS:
                    for suf, repl in PLURALS:
                        if wd.split(' ')[0].endswith(suf):
                            first, rest = wd.split(None, 1)
                            opt(first[:-len(suf)] + repl + ' ' + rest)
    opt_pl(word)
    if ' ' in word:
        parts = word.split(' ')
        parts = parts + blist
    else:
        parts = [word] + blist
    if len(parts) > 1:
        for i in xrange(len(word.split(' '))):
            if i == 0:
                pref = ''
            else:
                pref = str(i)
            limit = 3
            n = 0
            while (n < limit and i + n < len(parts)
                   and parts[i + n] not in TINCTURES
                   and parts[i + n] not in COUNTERCHANGEDS
                   and parts[i + n] not in (',', '.')):
                w = ' '.join(parts[i:i+n+1])
                if w != word:
                    opt_pl(w)
                if parts[i + n] in SMALL_WORDS or parts[i + n] in NUMBERS:
                    limit += 1
                n += 1
    return opts

def prompt_for_edit(e):
    from words import CHARGES
    word = e.word
    options = e.options
    print
    if e.dym:
        for d in e.dym:
            print d
        print

    if word in CHARGES:
        print '("%s" is already a charge.)' % word

    opts = {}
    if options:
        for i in xrange(len(options)):
            print '%s. Treat "%s" as an alias for "%s".' % (i+1, word,
                                                            options[i])
            opts[str(i+1)] = (str(i+1), word)
        if len(options) == 2:
            print 'b. both'
            opts['b'] = ('b', word)
    opts.update(
        prompt_n('a', 'Treat "%s" as an alias for a charge.', word, e.blist))
    opts.update(
        prompt_n('d', 'Treat "%s" as detail.', word, e.blist))
    print 'x. quit'
    action = raw_input("Action: ")
    if action not in opts:
        sys.exit(1)
    action, word = opts[action]
    if action == 'a':
        import words
        charge = None
        while True:
            charge = raw_input("Specify charge that '%s' is an alias of: "
                               % word)
            for c in charge.split(' & '):
                c = c.split(':', 1)[0]
                if (c not in words.CHARGES
                    and c not in words.DESC_TO_CHARGE):
                    print "%s is not a charge!" % c
                    break
            else:
                break
        names = []
        for c in charge.split(' & '):
            if ':' in c:
                c, t = c.split(':', 1)
                tags = t.split(':')
            else:
                tags = []
            if c in words.DESC_TO_CHARGE:
                n = words.DESC_TO_CHARGE[c].name
                tags += words.DESC_TO_CHARGE[c].tags
            else:
                n = words.CHARGES[c].name
                tags += words.CHARGES[c].tags
            if tags:
                n += ':' + ':'.join(tags)
            names.append(n)
        add_entry('aliases', '%s: %s' % (word, ' & '.join(names)))
    elif action == 'd':
        add_entry('details', word)
    elif action.isdigit():
        i = int(action) - 1
        add_entry('aliases', '%s: %s' % (word, options[i]))
    elif action == 'b':
        assert len(options) == 2
        add_entry('aliases', '%s: %s & %s' % (word, options[0], options[1]))
    else:
        assert False, action
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
            print
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
