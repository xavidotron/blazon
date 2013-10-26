import copy

from structs import Field, Group, ComplexTincture
from words import *

class stor(object):
    pass

def proc(x,b):
    if b in TINCTURES:
        if x.fielddivision:
            assert b in TINCTURES, b
            x.fielddivision.add_tincture(b)
            return True
        assert len(x.unspecified) > 0,("Tincture without anything to color:", b)
        t = copy.deepcopy(TINCTURES[b])
        for s in x.unspecified:
            s.tincture = t
        x.lasttincture = t
        x.unspecified = []
        return True
    elif b == 'and':
        return True

    if x.fielddivision and b not in PUNCT:
        # Done describing a complex tincture
        assert len(x.unspecified) > 0
        for s in x.unspecified:
            s.tincture = x.fielddivision
        x.unspecified = []
        x.fielddivision = None

    if b in NUMBERS:
        assert x.number is None,"Multiple numbers without a charge between!"
        x.number = NUMBERS[b]
    elif b in CHARGES:
        assert x.number is not None,("No number/a/an for a charge:", b,
                                     x.unspecified)
        if x.betweenness is not None:
            assert x.number > 1,"You can't be between only one thing!"
            g = x.betweenness
        elif x.on.kid is None:
            g = x.on.kid = Group()
        else:
            assert isinstance(x.on.kid, Group)
            g = x.on.kid
        c = copy.copy(CHARGES[b])
        g.append(c)
        c.number = x.number
        if x.arrangement is not None:
            c.mods.append(x.arrangement)
            x.arrangement = None
        x.unspecified.append(c)
        x.number = None
    elif b in ORDINARIES:
        assert x.number is not None,"No number/a/an for an ordinary!"
        assert x.number == 1,"Too many ordinaries!"
        x.number = None
        o = copy.copy(ORDINARIES[b])
        assert x.on.kid is None
        x.on.kid = o
        x.unspecified.append(o)
    elif b in PERIPHERALS:
        assert x.number is not None,"No number/a/an for an peripheral!"
        assert x.number == 1,"Too many peripherals!"
        x.number = None
        p = copy.copy(PERIPHERALS[b])
        p.outside = x.on.kid
        x.on.kid = p
        x.unspecified.append(p)
    elif b in PUNCT:
        #if x.on is not None:
        #    assert x.on.kid is not None,"Excess punctuation!"
        assert x.betweenness is None or len(x.betweenness) > 0, "Unfilled between!"
        #x.on = x.onstack.pop()
        x.betweenness = None
    elif b in BETWEEN:
        assert x.on.kid is not None,"Between with nothing before it!"
        x.betweenness = x.on.kid.between = Group()
    else:
        return False
    return True

def parse(blaz):
    loadwords()

    blaz = blaz.lower()
    for p in PUNCT:
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
    x.fielddivision = None
    x.lasttincture = None

    while len(blist) > 0:
        b = blist.pop(0)

        for ln in xrange(3, 0, -1):
            poss = ' '.join([b]+blist[:ln])
            if (poss in CHARGES or (poss.endswith('s') and poss[:-1] in CHARGES)
                or (poss.endswith('es') and poss[:-2] in CHARGES)
                or poss in DETAILS):
                b = poss
                blist = blist[ln:]
                break

        if x.mod == 'in':
            if 'arrangement, in %s' % b in CHARGES:
                x.mod = None
                x.arrangement = CHARGES['arrangement, in %s' % b]
                continue
            else:
                assert b in LOCATIONS, b
                x.mod = None
                continue
        elif (x.unspecified 
              and x.unspecified[-1].category in ('monster', 'beast')
              and 'arrangement, creature, %s' % b in CHARGES):
            x.unspecified[-1].mods.append(
                CHARGES['arrangement, creature, %s' % b])
            continue
        elif (x.unspecified
              and x.unspecified[-1].category
              and x.unspecified[-1].category.startswith('head, ')
              and 'arrangement, head, %s' % b in CHARGES):
            x.unspecified[-1].mods.append(
                CHARGES['arrangement, head, %s' % b])
            continue
        elif 'field division, %s' % b in CHARGES:
            x.fielddivision = ComplexTincture(CHARGES['field division, %s' % b])
            x.lasttincture = x.fielddivision
            continue
        elif x.mod in ('issuant', 'elongated'):
            if b in ('from', 'to'):
                continue
            else:
                assert b in LOCATIONS, b
                x.mod = None
                continue
        else:
            assert x.mod in (None, 'of'), x.mod

        if 'field treatment, %s' % b in CHARGES:
            assert x.lasttincture is not None
            x.lasttincture.add_treatment(b)
            continue
        
        res = proc(x,b)
        if not res and x.adj is not None:
            res = proc(x, x.adj + ' ' + b)
            assert res, (x.adj, b)
            x.adj = None
        if not res and b[-1] == 's':
            res = proc(x,b[:-1])
        if not res and b[-2:-1] == 'es':
            res = proc(x,b[:-2])
        if res:
            x.mod = None
        else:
            if x.number is not None:
                #if x.on.kid is None:
                #    x.on.kid = Group()
                #else:
                #    assert isinstance(x.on.kid, Group)
                #for lcv in xrange(x.number):
                #    c = copy.copy(DEFAULT_CHARGE)
                #    x.on.kid.append(c)
                #    x.unspecified.append(c)
                #x.number = None
                x.adj = b
            elif b in ('in', 'within', 'of', 'issuant', 'elongated'):
                x.mod = b
            elif b in DETAILS:
                pass
            elif x.mod == 'of':
                pass
            else:
                assert False,"Unknown noncharge word %s!"%b
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
