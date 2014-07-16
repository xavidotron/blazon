import copy, urllib

from structs import Field, Group, ComplexTincture, MultiTincture
from words import *

class BlazonException(Exception):
    def __init__(self, text, word=None):
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
        Exception.__init__(self, text)

class stor(object):
    pass

def proc(x, b, next):
    if b in CHARGES:
        #print 'CHARGE', b
        if x.number is None:
            assert x.was_charge_word,("No number/a/an for a charge:", b,
                                      x.unspecified)
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
        x.number = None
        x.adj = None
        x.nextmods = []
        x.was_charge_word = True
    elif b in BETWEEN:
        assert x.on.kid is not None,"Between with nothing before it!"
        x.primary = False
        x.betweenness = x.on.kid.between = Group()
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
        if (depluralize(poss) in CHARGES
            or poss in DETAILS or poss in ARRANGEMENTS 
            or poss in ORIENTATIONS or poss in POSTURES or poss in BIRD_POSTURES
            or poss in NUMBERS
            or poss in ANDS
            or poss in WITHINS
            or poss in CHARGED_WITHS
            or poss in DETAIL_ADJ):
            del blist[:ln]
            return poss
    return b

def parse(blaz):
    loadwords()

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
            else:
                assert b in LOCATIONS, b
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
            continue
        elif (x.lastcharge or x.adj) and b in ORIENTATIONS:
            if x.lastcharge:
                x.lastcharge.tags.append(ORIENTATIONS[b])
            else:
                raise BlazonException("Unknown charge: %s" % x.adj, x.adj)
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
              and x.lastcharge.category in ('monster', 'beast', 'human')
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
            x.fielddivision.append(
                ComplexTincture(CHARGES['field division, %s' % b]))
            x.lasttincture = x.fielddivision[-1]
            if not x.fdunspec:
                x.fdunspec = x.unspecified
                x.unspecified = []
            if isinstance(x.fdunspec[0], Field):
                x.lasttincture.on_field = True
            continue
        elif x.mod in ('issuant', 'elongated'):
            if b in ('from', 'to'):
                continue
            elif b in ('a', 'an'):
                x.mod = None
            else:
                assert b in LOCATIONS, b
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
                assert num in xrange(1,10), num
                x.lastcharge.tags.append('of %d' % num)
                x.mod = None
                if blist[0] in ('rays', 'points'):
                    blist.pop(0)
            else:
                assert x.mod in (None, 'on') or x.mod in WITHINS or x.mod in CHARGED_WITHS, x.mod
                x.number = NUMBERS[b]
            continue

        if b in TINCTURES:
            if not x.unspecified and x.fielddivision:
                assert b in TINCTURES, b
                for fd in x.fielddivision:
                    fd.add_tincture(b)
                continue
            if len(x.unspecified) == 0:
                if x.adj:
                    raise BlazonException("Unknown charge: %s" % x.adj, x.adj)
                    x.number = None
                    continue
                elif x.was_detail or x.was_field_treatment:
                    continue
                else:
                    raise BlazonException(
                        "Tincture without anything to color: %s" % b)
            t = copy.deepcopy(TINCTURES[b])
            if isinstance(x.unspecified[0], Field):
                t.on_field = True
            x.lasttincture = t
            if len(x.unspecified) == 1 and x.unspecified[0].category == 'field treatment':
                x.was_field_treatment = True
            else:
                for s in x.unspecified:
                    s.tincture = t
            x.unspecified = []
            x.was_detail = False
            x.was_charge_word = False
            continue
        elif b == 'counterchanged':
            if len(x.unspecified) == 0:
                if x.adj:
                    raise BlazonException("Unknown charge: %s" % x.adj, x.adj)
                    x.number = None
                    continue
                elif x.was_detail or x.was_field_treatment:
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
        x.was_field_treatment = True
        #print ':'
        if ('field treatment, %s' % b in CHARGES 
            or 'field treatment, seme, %s' % b in CHARGES):
            assert x.lasttincture is not None
            chgs = x.lasttincture.add_treatment(b)
            #print 'TREATMENT', chgs
            x.unspecified += chgs
            x.was_charge_word = False
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
            x.lasttincture.add_extra(chg)
            x.was_charge_word = False
            if x.lasttincture.on_field:
                ft = copy.deepcopy(CHARGES['field treatment, seme, other'])
                x.unspecified.append(ft)
                x.lasttincture.add_extra(ft)
                chg.tags.append('seme on field')
            continue

        if b == 'the':
            x.number = 'the'
            x.was_charge_word = False
            continue
        elif b in ANDS:
            if x.primary is None:
                x.primary = True
            x.was_charge_word = False
            continue
        elif b == 'sustaining':
            x.primary = False
            x.was_charge_word = False
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
            continue
        elif b in DETAILS:
            x.was_detail = True
            x.was_charge_word = False
            x.primary = None  # Not primary until "and"
            continue
        elif b in ARRANGEMENTS:
            #print 'ARRANGEMENT'
            x.was_charge_word = False
            continue
        elif x.number is not None and b in CHARGE_ADJ:
            #print 'CHARGE_ADJ'
            adj = copy.deepcopy(CHARGES[CHARGE_ADJ[b]])
            x.unspecified.append(adj)
            x.nextmods.append(adj)
            x.was_charge_word = False
            continue

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
                    raise BlazonException("I don't understand '%s %s' here!"
                                          % (x.adj, b))
                if b not in DETAIL_ADJ:
                    x.adj = b
                x.was_charge_word = False
            elif b in ('in',) or b in WITHINS or b in CHARGED_WITHS:
                x.primary = False
                x.mod = b
                x.was_charge_word = False
            elif b in ('on', 'issuant', 'elongated'):
                if x.was_charge_word:
                    x.primary = False
                else:
                    x.commadeprim = True
                x.mod = b
                x.was_charge_word = False
            elif b == 'of':
                x.mod = b
                if x.was_charge_word:
                    x.was_charge_word = b
            elif b == 'maintaining':
                x.maintained = True
                x.primary = None
                x.was_charge_word = False
            elif x.mod == 'of':
                x.was_charge_word = False
                pass
            elif b == '.':
                x.was_charge_word = False
                pass
            else:
                if x.unspecified and x.unspecified[-1].name == 'symbol':
                    x.was_charge_word = False
                    pass
                else:
                    if b in BIRD_POSTURES:
                        raise BlazonException("%s is a bird posture, but a '%s' is not a bird!" % (b, x.lastcharge.name), b)
                    elif b in ('to',):
                        raise BlazonException("I don't understand '%s %s' in this context!" % (b, blist[0]), "%s %s" % (b, blist[0]))
                    else:
                        raise BlazonException("Unknown noncharge word %s!" % b, b)

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
