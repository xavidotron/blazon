import copy, urllib

from structs import Field, Group, ComplexTincture, MultiTincture
from words import *

class BlazonException(Exception):
    def __init__(self, text, word=None, dym=[], options=[], blist=None):
        self.text = text
        if word:
            self.word = word
            url = 'http://oanda.sca.org/oanda_bp.cgi?p=%s&a=enabled' % urllib.quote_plus(word.encode('iso-8859-1'))
            self.url = url
            self.linktext = ("Search the Blazon Pattern Search Form for '%s'"
                             % word)
            text += '\n' + url
        else:
            self.word = None
            self.url = None
            self.linktext = None
        self.dym = dym
        self.options = options
        self.blist = blist
        Exception.__init__(self, text)

class stor(object):
    pass

def proc(x, b, orig_b, blist):
    if b in CHARGES and CHARGES[b] is not None:
        #print 'CHARGE', b
        if x.number is None:
            if x.maintained:
                pass
            elif x.was not in ('charge', 'charge of'):
                raise BlazonException("No number/a/an for a charge: %s" % b)
            elif x.unspecified[-1].name != CHARGES[b].name:
                if x.was == 'charge':
                    glued = '%s %s' % (x.unspecified[-1].blazon, orig_b)
                else:
                    glued = '%s of %s' % (x.unspecified[-1].blazon, orig_b)
                raise BlazonException(
                    "I don't know if a '%s' is a %s or a %s (or both)!"
                    % (glued,
                       x.unspecified[-1].name, CHARGES[b].name),
                    glued, options=[x.unspecified[-1].name, CHARGES[b].name],
                    blist=blist)
        if x.betweenness is not None:
            assert x.number > 1 or len(x.betweenness) > 0 or (blist and blist[0] == 'and'),"You can't be between only one thing!"
            g = x.betweenness
        elif x.on.kid is None:
            g = x.on.kid = Group()
        else:
            assert isinstance(x.on.kid, Group)
            g = x.on.kid
        c = copy.deepcopy(CHARGES[b])
        c.blazon = orig_b
        g.append(c)
        c.number = x.number
        if b in PERIPHERALS:
            x.primary = False
        elif x.primary:
            assert not x.maintained
            assert 'primary' not in c.tags, c.tags
            c.tags.append('primary')
        if c.name == 'cross, as charge' and x.adj in CROSS_FAMILIES:
            c.tags.append(CROSS_FAMILIES[x.adj])
        if x.arrangement is not None:
            c.mods.append(x.arrangement)
            x.arrangement = None
        if x.maintained:
            c.maintained = True
            x.maintained = False
        if x.nextmods:
            c.mods += x.nextmods
        if b in IMPLIED_TINCTURES:
            assert not x.unspecified, x.unspecified
            c.tincture = copy.deepcopy(TINCTURES[IMPLIED_TINCTURES[b]])
        else:
            x.unspecified.append(c)
            x.lastcharge = c
        x.multi = None
        x.number = None
        x.adj = None
        x.nextmods = []
        x.was = 'charge'
    elif b in BETWEEN:
        assert x.on.kid is not None,"Between with nothing before it!"
        x.primary = False
        x.betweenness = x.on.kid.between = Group()
        x.lastcharge = None
    else:
        return False
    return True

PLURAL_MAP = {
    'ies': 'y',
    'ves': 'f',
}

def depluralize(chargename):
    if chargename not in CHARGES:
        if chargename.endswith('s') and chargename[:-1] in CHARGES:
            return chargename[:-1]
        if chargename.endswith('es') and chargename[:-2] in CHARGES:
            return chargename[:-2]
        for suf in PLURAL_MAP:
            if chargename.endswith(suf):
                poss = chargename[:-len(suf)] + PLURAL_MAP[suf]
                if poss in CHARGES:
                    return poss
    return chargename

def clear_fielddivision(x):
    if x.fielddivision:
        # Done describing a complex tincture
        if x.fdunspec is not None:
            assert len(x.fdunspec) > 0
            for s in x.fdunspec:
                #if len(x.fielddivision) == 1:
                s.tincture = x.fielddivision[0]
                #else:
                #    s.tincture = MultiTincture(x.fielddivision)
        x.fdunspec = None
        x.fielddivision = []

def pop_blist(blist):
    b = blist.pop(0)
    
    for ln in xrange(5, 0, -1):
        poss = ' '.join([b]+blist[:ln])
        if depluralize(poss) in CHARGES or poss in ALL_WORDS:
            del blist[:ln]
            return poss
    return b

def suggest(word):
    ret = PWL.suggest(word)
    return ret

def unknown(typ, word, blist=None):
    dym = []
    if PWL:
        if PWL.check(word):
            raise BlazonException("'%s' is not a %s expected here!"
                                  % (word, typ), word, blist=blist)
        else:
            sugg = suggest(word)
            if sugg:
                dym.append("Did you mean: %s" % (', '.join(sugg)))
    raise BlazonException("Unknown %s: %s" % (typ, word), word, dym,
                          blist=blist)

def dont_understand(w1, w2, blist=None):
    dym = []
    if PWL:
        if not PWL.check(w1):
            dym.append("Should '%s' be: %s?" % (w1, ', '.join(suggest(w1))))
        if not PWL.check(w2):
            dym.append("Should '%s' be: %s?" % (w2, ', '.join(suggest(w2))))
    raise BlazonException("I don't understand '%s %s' here!"
                          % (w1, w2), '%s %s' % (w1, w2), dym, blist=blist)

def check_no_adj(x):
    if x.adj:
        unknown("charge", x.adj)

def parse(blaz):
    global PWL
    loadwords()

    try:
        from enchant import PyPWL
    except ImportError:
        PWL = None
    else:
        PWL = PyPWL()
        for word in ALL_WORDS:
            PWL.add(word)

    assert isinstance(blaz, unicode), repr(blaz)

    blaz = blaz.lower().strip()
    if not blaz.endswith('.'):
        blaz += '.'
    for p in (',', '.'):
        blaz = blaz.replace(p,' '+p)
    blist = blaz.split()
    
    x = stor()
            
    x.field = Field()
    x.unspecified = [x.field]
    x.on = x.field
    x.onstack = [None,x.field]
    x.number = None
    x.betweenness = None
    x.mod = None
    x.adj = None
    x.arrangement = None
    x.fielddivision = []
    x.fdunspec = None
    x.multi = None
    x.lastcharge = None
    x.lasttincture = None
    x.maintained = False
    x.primary = True
    x.commadeprim = False
    x.numdeprim = False
    x.was = None
    x.nextmods = []

    while len(blist) > 0:
        b = pop_blist(blist)
        print b, [x.unspecified[-1].category if x.unspecified else None]
        if x.mod == 'in':
            if b in ('her', 'his', 'its'):
                raise BlazonException(
                    "Unknown modifier 'in %s %s'" % (b, blist[0]),
                    'in %s %s' % (b, blist[0]))
            elif b in ('dexter', 'sinister'):
                # You can say "in dexter a wombat" or
                # "in dexter chief a wombat".
                if blist[0] in CHARGES:
                    # We don't care about details like 'in dexter claw'
                    del blist[0]
                    x.mod = None
                elif blist[0] not in LOCATIONS:
                    x.mod = None
                continue
            elif b not in LOCATIONS:
                raise BlazonException("Unknown location '%s'!" % b, b)
            x.mod = None
            continue

        if b in SEMYS:
            blist = ['of', SEMYS[b]] + blist
            b = 'semy'

        if x.mod in ('issuant', 'elongated'):
            if b in ('from', 'to', 'palewise', 'fesswise'):
                continue
            elif b in ('a', 'an'):
                x.mod = None
            else:
                if b not in LOCATIONS:
                    unknown('location', b, blist)
                x.mod = None
                continue
        elif 'arrangement, %s' % b in CHARGES:
            chg = CHARGES['arrangement, %s' % b]
            if x.lastcharge:
                x.lastcharge.mods.append(chg)
                chg.number = x.lastcharge.number
                chg.tags = x.lastcharge.tags
            else:
                x.arrangement = chg
            x.unspecified.append(chg)
            x.lastcharge = chg
            x.multi = None
            continue
        elif (x.lastcharge or x.adj) and b in ORIENTATIONS:
            if x.lastcharge:
                x.lastcharge.tags.append(ORIENTATIONS[b])
            else:
                unknown("charge", x.adj)
            continue
        elif x.lastcharge and b in LINES:
            x.lastcharge.tags.append(LINES[b])
            continue
        elif x.fielddivision and b in LINES:
            x.fielddivision[-1].fielddesc += ':' + LINES[b]
            continue
        elif (x.lastcharge 
              and x.lastcharge.category in ('monster', 'beast', 'bird',
                                            'reptile')
              and 'arrangement, creature, %s' % b in CHARGES):
            x.lastcharge.mods.append(
                CHARGES['arrangement, creature, %s' % b])
            continue
        elif (x.lastcharge
              and x.lastcharge.category
              and x.lastcharge.category.startswith('head, ')
              and 'arrangement, head, %s' % b in CHARGES):
            x.lastcharge.mods.append(
                CHARGES['arrangement, head, %s' % b])
            continue
        elif (x.lastcharge
              and (x.lastcharge.category in ('monster', 'beast', 'human',
                                             'reptile')
                   or x.lastcharge.name in ('amphibian',))
              and b in POSTURES):
            x.lastcharge.tags.append(POSTURES[b])
            continue
        elif (x.lastcharge
              and x.lastcharge.category in ('bird', 'monster')
              and b in BIRD_POSTURES):
            x.lastcharge.tags.append(BIRD_POSTURES[b])
            continue
        elif (x.lastcharge
              and x.lastcharge.category in ('monster, sea', 'fish') 
              and b in FISH_POSTURES):
            x.lastcharge.tags.append(FISH_POSTURES[b])
            continue
        elif (x.lastcharge
              and x.lastcharge.name == 'cross, as charge'
              and b in CROSS_FAMILIES):
            x.lastcharge.tags.append(CROSS_FAMILIES[b])
            continue
        elif 'field division, %s' % b in CHARGES:
            #print 'field division', b
            check_no_adj(x)
            charge = CHARGES['field division, %s' % b]
            if not x.fdunspec:
                if x.unspecified:
                    x.fdunspec = x.unspecified
                    x.unspecified = []
                    x.lasttincture = ComplexTincture(charge)
                else:
                    x.lasttincture.complicate(charge)
            else:
                x.lasttincture = ComplexTincture(charge)
            if x.fielddivision:
                if not x.fielddivision[-1].add_tincture('multicolor'):
                    raise BlazonException("Trying to add a division (%s) to a full field division." % (b))
            x.fielddivision.append(x.lasttincture)
            if x.fdunspec and isinstance(x.fdunspec[0], Field):
                x.lasttincture.on_field = True
            continue
        else:
            assert x.mod in (None, 'of', 'on') or x.mod in WITHINS or x.mod in CHARGED_WITHS, x.mod

        if b in NUMBERS:
            #print 'NUMBER', b, x.mod
            if x.number is not None:
                if x.adj == 'sets' and x.mod == 'of':
                    x.number *= NUMBERS[b]
                    continue
                else:
                    raise BlazonException("Multiple numbers without a charge between: %s and %s" % (x.number, b))
            if x.numdeprim:
                x.primary = False
            elif x.commadeprim:
                x.numdeprim = True
            if x.mod == 'of':
                num = NUMBERS[b]
                if (blist[0] == 'greater' and blist[1] == 'and'
                    and blist[3] == 'lesser'):
                    num += NUMBERS[blist[2]]
                    blist = blist[4:]
                if num >= 9:
                    num = '9 or more'
                if x.lastcharge is not None:
                    x.lastcharge.tags.append('of %s' % num)
                elif x.fielddivision:
                    pass
                else:
                    raise BlazonException("Weird use of 'of %s'!" % num)
                    
                x.mod = None
                if blist[0] in ('rays', 'points'):
                    blist.pop(0)
            else:
                assert x.mod in (None, 'on') or x.mod in WITHINS or x.mod in CHARGED_WITHS, x.mod
                x.number = NUMBERS[b]
            continue

        if b in TINCTURES:
            t = copy.deepcopy(TINCTURES[b])
            check_no_adj(x)
            if not x.unspecified:
                if x.was in ('field treatment', 'counterchange'):
                    continue
                old_was = x.was
                x.was = 'tincture'
                if old_was in ('detail',):
                    continue
                elif x.fielddivision:
                    while not x.fielddivision[-1].add_tincture(b):
                        x.fielddivision.pop()
                        if not x.fielddivision:
                            raise BlazonExceptions("Too many tinctures for a field division, don't know what to do with '%s'!" % b)
                    continue
                elif x.multi is not None:
                    x.lasttincture = t
                    if isinstance(x.multi.tincture, MultiTincture):
                        assert x.multi.tincture.add_tincture(t)
                    else:
                        x.multi.tincture = MultiTincture([x.multi.tincture, t])
                    continue
                elif (x.lastcharge and x.lastcharge.number == 2
                      and not isinstance(x.lastcharge.tincture, MultiTincture)):
                    x.lasttincture = t
                    x.lastcharge.tincture = MultiTincture([
                        x.lastcharge.tincture, t])
                    continue
                else:
                    raise BlazonException(
                        "Tincture without anything to color: %s" % (b))
            if isinstance(x.unspecified[0], Field):
                t.on_field = True
            x.lasttincture = t
            if len(x.unspecified) == 1 and x.unspecified[0].category == 'field treatment':
                x.was = 'field treatment'
            else:
                for s in x.unspecified:
                    s.tincture = t
                x.was = 'tincture'
            if len(x.unspecified) == 1 and x.unspecified[0].name in MULTIPLE_TINCTURES:
                x.multi = x.unspecified[0]
            else:
                x.multi = None
            x.unspecified = []
            continue
        elif b in COUNTERCHANGEDS:
            if len(x.unspecified) == 0:
                check_no_adj(x)
                if x.was in ('detail', 'field treatment'):
                    raise BlazonException("Weird counterchange!")
                    continue
                else:
                    raise BlazonException(
                        "Counterchange without anything to color: %s" % b)
            if x.primary is not False:
                if not x.field.tincture.is_complex():
                    raise BlazonException(
                        "Counterchange over a simple field!")
                unspec = [u for u in x.unspecified if not u.maintained]
                if len(unspec) == 1:
                    # Do this even if unspec[0].number != 1; that's how
                    # oanda does it.
                    unspec[0].tincture = Tincture('multicolor')
            x.lasttincture = None
            x.unspecified = []
            x.was = 'counterchange'
            continue
        #print ':', b, x.number
        if ('field treatment, %s' % b in CHARGES 
            or ('field treatment, seme, %s' % b in CHARGES 
                and b != 'roundels')):
            assert x.lasttincture is not None
            chgs = x.lasttincture.add_treatment(b)
            #print 'TREATMENT', chgs
            x.unspecified += chgs
            x.was = 'field treatment'
            clear_fielddivision(x)
            continue
        elif b == 'semy':
            assert blist.pop(0) == 'of'
            #print 'SEMY'
            charge = depluralize(pop_blist(blist))
            assert charge in CHARGES, charge
            chg = copy.deepcopy(CHARGES[charge])
            chg.number = 'seme'
            if charge in IMPLIED_TINCTURES:
                assert not x.unspecified, x.unspecified
                chg.tincture = copy.deepcopy(
                    TINCTURES[IMPLIED_TINCTURES[charge]])
            else:
                x.unspecified.append(chg)
                x.lastcharge = chg
            x.multi = None
            x.lasttincture.add_extra(chg)
            x.was = 'tincture'
            if x.lasttincture.on_field:
                ft = copy.deepcopy(CHARGES['field treatment, seme, other'])
                x.unspecified.append(ft)
                x.lasttincture.add_extra(ft)
                chg.tags.append('seme on field')
            continue

        if b == 'the':
            x.number = 'the'
            x.was = 'number'
            continue
        elif b in ANDS:
            if x.primary is None:
                x.primary = True
            if x.was not in ('field treatment',):
                x.was = 'and'
            continue
        elif b in SUSTAININGS:
            x.primary = False
            x.was = 'sustaining'
            continue
        elif b == ',':
            if x.commadeprim:
                x.primary = False
            #if x.on is not None:
            #    assert x.on.kid is not None,"Excess punctuation!"
            assert x.betweenness is None or len(x.betweenness) > 0, "Unfilled between!"
            #x.on = x.onstack.pop()
            x.betweenness = None
            if x.was not in ('field treatment',):
                x.was = 'comma'
            continue
        elif x.number is None and b in MAJOR_DETAILS:
            x.on.kid.append(copy.deepcopy(CHARGES[MAJOR_DETAILS[b]]))
            x.was = 'detail'
            continue
        elif b in DETAILS:
            x.was = 'detail'
            x.primary = None  # Not primary until "and"
            continue
        elif b in ARRANGEMENTS:
            #print 'ARRANGEMENT'
            x.was = 'arrangement'
            continue
        elif x.number is not None and b in CHARGE_ADJ:
            #print 'CHARGE_ADJ'
            adj = copy.deepcopy(CHARGES[CHARGE_ADJ[b]])
            x.unspecified.append(adj)
            x.nextmods.append(adj)
            x.was = 'adjective'
            continue
        elif b == 'at' and blist[0] == 'the':
            # e.g., "conjoined at the bells"
            if not blist[1].endswith('s') and blist[1] in ALL_WORDS:
                raise BlazonException("I don't understand 'at the %s'!"
                                      % (blist[1]), 'at the %s' % blist[1])
            del blist[:2]
            continue
        elif b == 'at' and blist[0] in LOCATIONS:
            # e.g., "conjoined at base"
            del blist[0]
            continue
        elif b in ATOPS and blist[0] == 'its' and blist[1] not in ALL_WORDS:
            # e.g., "atop its back"
            del blist[:2]
            x.was = 'detail'
            continue
        elif b == 'with' and blist[0] == 'its' and blist[1] in CHARGES:
            # e.g., "enfiling with its tail"
            del blist[:2]
            continue

        if b not in ('of',):
            clear_fielddivision(x)

        if x.number is None and b in IMPLIED_NUMBER:
            x.number = IMPLIED_NUMBER[b]

        res = proc(x, depluralize(b), b, blist)
        #print res, depluralize(b)
        if not res and b.startswith('demi-'):
            res = proc(x, depluralize(b[len('demi-'):]), b, blist)
            if res:
                chg = x.unspecified[-1]
                assert chg.category in ('monster', 'beast', 'bird'), chg
                demi = copy.deepcopy(CHARGES['%s, demi' % chg.category])
                demi.number = chg.number
                chg.mods.append(demi)
                x.unspecified.append(demi)
                x.lastcharge = demi
                x.multi = None
        if res:
            x.mod = None
        else:
            if x.number is not None and x.adj != 'sets':
                #if x.on.kid is None:
                #    x.on.kid = Group()
                #else:
                #    assert isinstance(x.on.kid, Group)
                #for lcv in xrange(x.number):
                #    c = copy.copy(DEFAULT_CHARGE)
                #    x.on.kid.append(c)
                #    x.unspecified.append(c)
                #x.number = None
                if x.adj is not None:
                    dont_understand(x.adj, b, blist)
                if b not in DETAIL_ADJ:
                    x.adj = b
                x.was = 'adjective'
            elif b in ('overall',):
                x.primary = False
            elif b in ('in',) or b in WITHINS or b in CHARGED_WITHS:
                # Could still be a primary if this is:
                # Sable, in base a wombat Or.
                # or
                # Vert, within an annulet an acorn argent.
                if x.lastcharge:
                    x.primary = False
                x.mod = b
                x.was = 'in'
            elif b in ('on', 'issuant', 'elongated'):
                if x.was == 'charge':
                    x.primary = False
                else:
                    x.commadeprim = True
                x.mod = b
                x.was = 'on'
            elif b == 'of':
                x.mod = b
                if x.was == 'charge':
                    x.was = 'charge of'
                else:
                    x.was = 'of'
            elif b in MAINTAININGS:
                x.maintained = True
                x.primary = None
                x.was = 'maintaining'
            elif b == '.':
                x.was = 'period'
                pass
            else:
                if x.unspecified and x.unspecified[-1].name == 'symbol':
                    x.was = 'symbol'
                    pass
                else:
                    if (b in POSTURES or b in BIRD_POSTURES 
                        or b in FISH_POSTURES):
                        raise BlazonException("%s is a posture, but a '%s' is not an appropriate creature!" % (b, x.lastcharge.name), b)
                    elif b in ('to',):
                        dont_understand(b, blist[0], blist[1:])
                    elif (b.endswith('ed') and x.was == 'tincture'
                          and blist[0] in TINCTURES):
                        # X sable vested azure
                        del blist[0]
                    else:
                        unknown("noncharge word after a %s" % x.was, b, blist)

    #assert x.betweenness is None, x.betweenness
    assert not x.fielddivision, x.fielddivision

    return x.field

if __name__ == '__main__':
    import sys
    p = parse(sys.argv[1])
    for l in p.tree():
        print l

def render():
    print """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
              "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 100 100" version="1.1">
  <desc>
  </desc>"""
    print p.render()
    print "</svg>"
