from structs import Field, Group
from words import (TINCTURES, NUMBERS, CHARGES, DEFAULT_CHARGE, 
                   ORDINARIES, PERIPHERALS,
                   PUNCT,
                   BETWEEN)

class stor(object):
    pass

def parse(blaz):
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

    while len(blist) > 0:
        b = blist.pop(0)
        def proc(x,b):
            if b in TINCTURES:
                assert len(x.unspecified) > 0,"Tincture without anything to color!"
                for s in x.unspecified:
                    s.tincture = TINCTURES[b]
                x.unspecified = []
            elif b in NUMBERS:
                assert x.number is None,"Multiple numbers without a charge between!"
                x.number = NUMBERS[b]
            elif b in CHARGES:
                assert x.number is not None,"No number/a/an for a charge!"
                if x.betweenness is not None:
                    assert x.number > 1,"You can't be between only one thing!"
                    g = x.betweenness
                elif x.on.kid is None:
                    g = x.on.kid = Group()
                else:
                    assert isinstance(on.kid, Group)
                    g = x.on.kid
                for lcv in xrange(x.number):
                    c = CHARGES[b]()
                    g.append(c)
                    x.unspecified.append(c)
                x.number = None
            elif b in ORDINARIES:
                assert x.number is not None,"No number/a/an for an ordinary!"
                assert x.number == 1,"Too many ordinaries!"
                x.number = None
                o = ORDINARIES[b]()
                assert x.on.kid is None
                x.on.kid = o
                x.unspecified.append(o)
            elif b in PERIPHERALS:
                assert x.number is not None,"No number/a/an for an peripheral!"
                assert x.number == 1,"Too many peripherals!"
                x.number = None
                p = PERIPHERALS[b]()
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
        
        res = proc(x,b)
        if not res and b[-1] == 's':
            res = proc(x,b[:-1])
        if not res and b[-2:-1] == 'es':
            res = proc(x,b[:-2])
        if not res:
            if x.number is not None:
                if x.on.kid is None:
                    x.on.kid = Group()
                else:
                    assert isinstance(x.on.kid, Group)
                for lcv in xrange(x.number):
                    c = DEFAULT_CHARGE()
                    x.on.kid.append(c)
                    x.unspecified.append(c)
                x.number = None
            else:
                assert False,"Unknown noncharge word %s!"%b
    return x.field

if __name__ == '__main__':
    import sys
    p = parse(sys.argv[1])
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
