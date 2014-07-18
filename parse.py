import copy, urllib

from structs import Field, Group, ComplexTincture, MultiTincture
from words import *

class BlazonException(Exception):
    def __init__(self, text, word=None, dym=[]):
        self.text = text
        if word:
            url = 'http://oanda.sca.org/oanda_bp.cgi?p=%s&a=enabled' % urllib.quote_plus(word)
            self.url = url
            self.linktext = ("Search the Blazon Pattern Search Form for '%s'"
                             % word)
            text += '\n' + url
        else:
            self.url = None
            self.linktext = None
        self.dym = dym
        Exception.__init__(self, text)

class stor(object):
    pass

def proc(x, b, next):
    if b in CHARGES and CHARGES[b] is not None:
        #print 'CHARGE', b
        if x.number is None:
            if not x.was_charge_word:
                raise BlazonException("No number/a/an for a charge: %s" % b)
            if x.unspecified[-1].name != CHARGES[b].name:
                if x.was_charge_word is True:
                    glued = '%s %s' % (x.unspecified[-1].blazon, b)
                else:
                    glued = '%s %s %s' % (x.unspecified[-1].blazon, 
                                          x.was_charge_word, b)
                raise BlazonException(
                    "I don't know if a '%s' is a %s or a %s (or both)!"
                    % (glued,
                       x.unspecified[-1].name, CHARGES[b].name),
                    glued)
        if x.betweenness is not None:
            assert x.number > 1 or len(x.betweenness) > 0 or next == 'and',"You can't be between only one thing!"
            g = x.betweenness
        elif x.on.kid is None:
            g = x.on.kid = Group()
        else:
            assert isinstance(x.on.kid, Group)
            g = x.on.kid
        c = copy.deepcopy(CHARGES[b])
        c.blazon = b
        g.append(c)
        c.number = x.number
        if b in PERIPHERALS:
            x.primary = False
        elif x.primary:
            assert not x.maintained
            assert 'primary' not in c.tags, c.tags
            c.tags.append('primary')
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
        x.was_charge_word = True
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
        assert len(x.fdunspec) > 0
        for s in x.fdunspec:
            if len(x.fielddivision) == 1:
                s.tincture = x.fielddivision[0]
            else:
                s.tincture = MultiTincture(x.fielddivision)
        x.fdunspec = []
        x.fielddivision = []

def pop_blist(blist):
    b = blist.pop(0)
    
    for ln in xrange(4, 0, -1):
        poss = ' '.join([b]+blist[:ln])
        if depluralize(poss) in CHARGES or poss in ALL_WORDS:
            del blist[:ln]
            return poss
    return b

def suggest(word):
    ret = PWL.suggest(word)
    return ret

def unknown(typ, word):
    dym = []
    if PWL:
        if PWL.check(word):
            raise BlazonException("'%s' is not a %s expected here!"
                                  % (word, typ), word)
        else:
            sugg = suggest(word)
            if sugg:
                dym.append("Did you mean: %s" % (', '.join(sugg)))
    raise BlazonException("Unknown %s: %s" % (typ, word), word, dym)

def dont_understand(w1, w2):
    dym = []
    if PWL:
        if not PWL.check(w1):
            dym.append("Should '%s' be: %s?" % (w1, ', '.join(suggest(w1))))
        if not PWL.check(w2):
            dym.append("Should '%s' be: %s?" % (w2, ', '.join(suggest(w2))))
    raise BlazonException("I don't understand '%s %s' here!"
                          % (w1, w2), '%s %s' % (w1, w2), dym)

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
    x.was_detail = False
    x.was_field_treatment = False
    x.was_charge_word = False
    x.nextmods = []

    while len(blist) > 0:
        b = pop_blist(blist)
        #print b, [x.unspecified[-1].category if x.unspecified else None]
        if x.mod == 'in':
            if b in ('her', 'his', 'its'):
                raise BlazonException(
                    "Unknown modifier 'in %s %s'" % (b, blist[0]),
                    'in %s %s' % (b, blist[0]))
            elif b in ('dexter', 'sinister'):
                continue
            elif b in CHARGES:
                # We don't care about details like 'in dexter claw'
                pass
            elif b not in LOCATIONS:
                raise BlazonException("Unknown location '%s'!" % b, b)
            x.mod = None
            continue

        if b in SEMYS:
            blist = ['of', SEMYS[b]] + blist
            b = 'semy'
        
        if 'arrangement, %s' % b in CHARGES:
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
              and x.lastcharge.category in ('monster', 'beast', 'bird')
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
              and x.lastcharge.category in ('monster', 'beast', 'human',
                                            'reptile')
              and b in POSTURES):
            x.lastcharge.tags.append(POSTURES[b])
            continue
        elif (x.lastcharge
              and x.lastcharge.category in ('bird', 'monster')
              and b in BIRD_POSTURES):
            x.lastcharge.tags.append(BIRD_POSTURES[b])
            continue
        elif (x.lastcharge
              and x.lastcharge.name == 'cross, as charge'
              and b in CROSS_FAMILIES):
            x.lastcharge.tags.append(CROSS_FAMILIES[b])
            continue
        elif 'field division, %s' % b in CHARGES:
            check_no_adj(x)
            x.fielddivision.append(
                ComplexTincture(CHARGES['field division, %s' % b]))
            x.lasttincture = x.fielddivision[-1]
            if not x.fdunspec:
                x.fdunspec = x.unspecified
                x.unspecified = []
            if x.fdunspec and isinstance(x.fdunspec[0], Field):
                x.lasttincture.on_field = True
            continue
        elif x.mod in ('issuant', 'elongated'):
            if b in ('from', 'to'):
                continue
            elif b in ('a', 'an'):
                x.mod = None
            else:
                if b not in LOCATIONS:
                    unknown('location', b)
                x.mod = None
                continue
        else:
            assert x.mod in (None, 'of', 'on') or x.mod in WITHINS or x.mod in CHARGED_WITHS, x.mod

        if b in NUMBERS:
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
            if not x.unspecified:
                check_no_adj(x)
                #assert False, (x.was_detail, x.was_field_treatment)
                if x.was_detail or x.was_field_treatment:
                    continue
                elif x.fielddivision:
                    for fd in x.fielddivision:
                        fd.add_tincture(b)
                    continue
                elif x.multi is not None:
                    x.lasttincture = t
                    if isinstance(x.multi.tincture, MultiTincture):
                        x.multi.tincture.add_tincture(t)
                    else:
                        x.multi.tincture = MultiTincture([x.multi.tincture, t])
                    continue
                else:
                    raise BlazonException(
                        "Tincture without anything to color: %s" % b)
            if isinstance(x.unspecified[0], Field):
                t.on_field = True
            x.lasttincture = t
            if len(x.unspecified) == 1 and x.unspecified[0].category == 'field treatment':
                x.was_field_treatment = True
            else:
                for s in x.unspecified:
                    s.tincture = t
            if len(x.unspecified) == 1 and x.unspecified[0].name in MULTIPLE_TINCTURES:
                x.multi = x.unspecified[0]
            else:
                x.multi = None
            x.unspecified = []
            x.was_detail = False
            x.was_charge_word = False
            continue
        elif b in COUNTERCHANGEDS:
            if len(x.unspecified) == 0:
                check_no_adj(x)
                if x.was_detail or x.was_field_treatment:
                    raise BlazonException("Weird counterchange!")
                    continue
                else:
                    raise BlazonException(
                        "Counterchange without anything to color: %s" % b)
            if x.primary is not False:
                if not isinstance(x.field.tincture, ComplexTincture):
                    raise BlazonException(
                        "Counterchange over a simple field!")
                unspec = [u for u in x.unspecified if not u.maintained]
                if len(unspec) == 1:
                    unspec[0].tincture = Tincture('multicolor')
            x.lasttincture = None
            x.unspecified = []
            x.was_detail = False
            x.was_charge_word = False
            continue
        x.was_detail = False
        #print ':', b
        if ('field treatment, %s' % b in CHARGES 
            or 'field treatment, seme, %s' % b in CHARGES):
            assert x.lasttincture is not None
            chgs = x.lasttincture.add_treatment(b)
            #print 'TREATMENT', chgs
            x.unspecified += chgs
            x.was_charge_word = False
            x.was_field_treatment = True
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
            x.was_charge_word = False
            x.was_field_treatment = False
            if x.lasttincture.on_field:
                ft = copy.deepcopy(CHARGES['field treatment, seme, other'])
                x.unspecified.append(ft)
                x.lasttincture.add_extra(ft)
                chg.tags.append('seme on field')
            continue

        if b == 'the':
            x.number = 'the'
            x.was_charge_word = False
            x.was_field_treatment = False
            continue
        elif b in ANDS:
            if x.primary is None:
                x.primary = True
            x.was_charge_word = False
            continue
        elif b in SUSTAININGS:
            x.primary = False
            x.was_charge_word = False
            x.was_field_treatment = False
            continue
        elif b == ',':
            if x.commadeprim:
                x.primary = False
            #if x.on is not None:
            #    assert x.on.kid is not None,"Excess punctuation!"
            assert x.betweenness is None or len(x.betweenness) > 0, "Unfilled between!"
            #x.on = x.onstack.pop()
            x.betweenness = None
            x.was_charge_word = False
            continue
        elif x.number is None and b in MAJOR_DETAILS:
            x.on.kid.append(copy.deepcopy(CHARGES[MAJOR_DETAILS[b]]))
            x.was_detail = True
            x.was_charge_word = False
            x.was_field_treatment = False
            continue
        elif b in DETAILS:
            x.was_detail = True
            x.was_charge_word = False
            x.was_field_treatment = False
            x.primary = None  # Not primary until "and"
            continue
        elif b in ARRANGEMENTS:
            #print 'ARRANGEMENT'
            x.was_charge_word = False
            x.was_field_treatment = False
            continue
        elif x.number is not None and b in CHARGE_ADJ:
            #print 'CHARGE_ADJ'
            adj = copy.deepcopy(CHARGES[CHARGE_ADJ[b]])
            x.unspecified.append(adj)
            x.nextmods.append(adj)
            x.was_charge_word = False
            x.was_field_treatment = False
            continue
        elif b == 'at' and blist[0] == 'the' and blist[1].endswith('s'):
            del blist[:2]
            continue

        if b not in ('of',):
            clear_fielddivision(x)

        if x.number is None and b in IMPLIED_NUMBER:
            x.number = IMPLIED_NUMBER[b]

        next = blist[0] if blist else None
        res = proc(x, depluralize(b), next)
        #print res, depluralize(b)
        if not res and b.startswith('demi-'):
            res = proc(x, depluralize(b[len('demi-'):]), next)
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
                    dont_understand(x.adj, b)
                if b not in DETAIL_ADJ:
                    x.adj = b
                x.was_charge_word = False
                x.was_field_treatment = False
            elif b in ('in',) or b in WITHINS or b in CHARGED_WITHS:
                x.primary = False
                x.mod = b
                x.was_charge_word = False
                x.was_field_treatment = False
            elif b in ('on', 'issuant', 'elongated'):
                if x.was_charge_word:
                    x.primary = False
                else:
                    x.commadeprim = True
                x.mod = b
                x.was_charge_word = False
                x.was_field_treatment = False
            elif b == 'of':
                x.mod = b
                if x.was_charge_word:
                    x.was_charge_word = b
                x.was_field_treatment = False
            elif b in MAINTAININGS:
                x.maintained = True
                x.primary = None
                x.was_charge_word = False
                x.was_field_treatment = False
            elif x.mod == 'of':
                x.was_charge_word = False
                x.was_field_treatment = False
                pass
            elif b == '.':
                x.was_charge_word = False
                x.was_field_treatment = False
                pass
            else:
                if x.unspecified and x.unspecified[-1].name == 'symbol':
                    x.was_charge_word = False
                    x.was_field_treatment = False
                    pass
                else:
                    if b in POSTURES:
                        raise BlazonException("%s is a posture, but a '%s' is not an appropriate creature!" % (b, x.lastcharge.name), b)
                    elif b in BIRD_POSTURES:
                        raise BlazonException("%s is a bird posture, but a '%s' is not a bird!" % (b, x.lastcharge.name), b)
                    elif b in ('to',):
                        dont_understand(b, blist[0])
                    else:
                        unknown("noncharge word", b)

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
