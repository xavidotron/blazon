from structs import Field
from words import COLORS, NUMBERS, CHARGES, DEFAULT_CHARGE

def parse(blaz):
    blist = blaz.lower().replace(',',' ,').replace('.',' .').split()
    
    field = Field()
    stack = [field]
    on = field
    number = None

    while len(blist) > 0:
        b = blist.pop(0)
        if b in COLORS:
            assert len(stack) > 0,"Color without anything to color!"
            for s in stack:
                s.color = COLORS[b]
                on.kids.append(s)
            stack = []
        elif b in NUMBERS:
            assert number is None,"Multiple numbers without a charge between!"
            number = NUMBERS[b]
        elif b in CHARGES:
            assert number is not None,"No number/a/an for a charge!"
            for lcv in xrange(number):
                stack.append(CHARGES[b])
            number = None
        elif b == ',':
            pass
        elif b == '.':
            assert len(blist) == 0,"Period in the middle of a blazon!"
        else:
            if number is not None:
                stack.append(DEFAULT_CHARGE)
            else:
                assert False,"Unknown noncharge word %s!"%b
    return field

if __name__ == '__main__':
    import sys
    p = parse(sys.argv[1])
    print "OK"
