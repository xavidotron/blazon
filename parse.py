import copy, urllib
import re

from structs import Field, Group, ComplexTincture, MultiTincture
from words import *

class BlazonException(Exception):
    def __init__(self, text, word=None, dym=[], options=[], blist=[]):
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

def get_prev(x, offset=0):
    retl = x.lastb[-2 - offset:-offset if offset else None]
    for i in xrange(len(retl)):
        if retl[i] in (',',) or retl[i] in WITHS:
            del retl[:i+1]
            break
    return ' '.join(retl)

def proc(x, b, orig_b, blist):
    if b in CHARGES and CHARGES[b] is not None:
        if CHARGES[b].number is not None:
            if x.number is not None:
                raise BlazonException(
                    "Explicit number for charge '%s' with an implicit "
                    "number: %s vs %s" % (b, x.number, CHARGES[b].number))
            assert not x.multiplier, x.multiplier
            x.number = CHARGES[b].number
        if x.number is None and x.was == 'with' and x.lastcharge[-1].number > 1:
            # This is something like "two plates charged with triskelions".
            x.number = x.lastcharge[-1].number
        if (x.number is None and x.was == 'charge of' 
            and x.lastcharge[-1].name in OF_CHARGES):
            x.number = (x.lastcharge[-1].number 
                        * OF_CHARGES[x.lastcharge[-1].name])
        if x.number is None:
            if x.maintained:
                pass
            elif (x.was not in ('charge', 'charge of') 
                  or not x.unspecified[-1].blazon):
                lb = get_prev(x)
                raise BlazonException("No number/a/an for a charge: %s" % b,
                                      lb + ' ' + orig_b if lb else orig_b, 
                                      blist=blist)
            elif x.unspecified[-1].name != CHARGES[b].name:
                if x.was == 'charge':
                    glued = '%s %s' % (x.unspecified[-1].blazon, orig_b)
                else:
                    glued = '%s of %s' % (x.unspecified[-1].blazon, orig_b)
                if x.unspecified[-1].adj:
                    glued = x.unspecified[-1].adj + ' ' + glued
                raise BlazonException(
                    "I don't know if '%s' means '%s' or '%s' (or both)!"
                    % (glued,
                       x.unspecified[-1].name, CHARGES[b].name),
                    glued, options=[x.unspecified[-1].name, CHARGES[b].name],
                    blist=blist)
        if x.betweenness is not None:
            if x.number <= 1 and len(x.betweenness) == 0 and (not blist or 'and' not in blist):
                raise BlazonException(
                    "You can't be between only one thing! (%s)"
                    % b)
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
        if c.name in PERIPHERALS:
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
            c.tincture = copy.deepcopy(TINCTURES[IMPLIED_TINCTURES[b]])
            if (x.was == 'of number' 
                or (x.unspecified and
                    x.unspecified[-1].category == 'arrangement')):
                assert len(x.unspecified) == 1
                for u in x.unspecified:
                    u.tincture = c.tincture
                x.unspecified = []
            else:
                if x.unspecified:
                    raise BlazonException(
                        "Unspecified charges (%s) followed by something "
                        "with an implied tincture (%s)!"
                        % (', '.join(c.name for c in x.unspecified), b))
        else:
            x.unspecified.append(c)
        x.lastcharge.append(c)
        x.multi = None
        x.number = None
        c.adj = x.adj
        x.adj = None
        x.nextmods = []
        x.was = 'charge'
    elif b in BETWEEN:
        if x.lastcharge:
            if x.on.kid is None:
                raise BlazonException("Between with nothing before it!")
            x.primary = False
            x.betweenness = x.on.kid.between = Group()
        x.lastcharge = []
    else:
        return False
    return True

PLURALS = [
    ('ves', 'f'),
    ('ies', 'y'),
    ('es', ''),
    ('s', ''),
]

def depluralize(chargename):
    if chargename not in CHARGES:
        for suf, repl in PLURALS:
            if chargename.endswith(suf):
                poss = chargename[:-len(suf)] + repl
                if poss in CHARGES:
                    return poss
        if ' ' in chargename:
            first, rest = chargename.split(' ', 1)
            for suf, repl in PLURALS:
                if first.endswith(suf):
                    poss = first[:-len(suf)] + repl + ' ' + rest
                    if poss in CHARGES:
                        return poss
    return chargename

def clear_fielddivision(x):
    if x.fielddivision:
        # Done describing a complex tincture
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

def unknown(typ, word, blist=[], prev=None):
    dym = []
    if prev:
        wd = prev + ' ' + word
    else:
        wd = word
    if PWL:
        if PWL.check(word):
            raise BlazonException("'%s' is not a %s expected here!"
                                  % (word, typ), wd, blist=blist)
        else:
            sugg = suggest(word)
            if sugg:
                dym.append("Did you mean: %s" % (', '.join(sugg)))
    raise BlazonException("Unknown %s: %s" % (typ, word), wd, dym,
                          blist=blist)

def dont_understand(w1, w2, blist=[]):
    dym = []
    if PWL:
        if not PWL.check(w1):
            dym.append("Should '%s' be: %s?" % (w1, ', '.join(suggest(w1))))
        if not PWL.check(w2):
            dym.append("Should '%s' be: %s?" % (w2, ', '.join(suggest(w2))))
    if w2 in ('.', ','):
        raise BlazonException("I don't understand '%s' here!" % w1,
                              w1, dym, blist=blist)
    else:
        raise BlazonException("I don't understand '%s %s' here!"
                              % (w1, w2), '%s %s' % (w1, w2), dym, blist=blist)

def check_no_adj(x, b, blist=[], prev=None):
    #print 'cna', prev
    if x.adj:
        unknown("charge", x.adj, blist=[b] + blist, prev=prev)

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
    blaz = re.sub(r'inscription \"[^"]+\"', 'inscription', blaz)
    blist = blaz.split()
    
    x = stor()
            
    x.field = Field()
    x.unspecified = [x.field]
    x.on = x.field
    x.onstack = [None,x.field]
    x.number = None
    x.multiplier = None
    x.betweenness = None
    x.mod = None
    x.adj = None
    x.arrangement = None
    x.fielddivision = []
    x.multi = None
    x.lastcharge = []
    x.lasttincture = None
    x.maintained = False
    x.primary = True
    x.commadeprim = False
    x.commamult = None
    x.numdeprim = False
    x.was = None
    x.nextmods = []
    x.lastb = []

    b = None
    while len(blist) > 0:
        if b:
            x.lastb.append(b)
        b = pop_blist(blist)
        #print b, [x.unspecified[-1].category if x.unspecified else None]
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
                raise BlazonException("Unknown location '%s'!" % b, 'in '+b)
            x.mod = None
            continue

        if x.number is None and b in SEMYS:
            blist = ['of', SEMYS[b]] + blist
            b = 'semy'
        #print "!", x.lastcharge, b
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
                x.lastcharge[-1].mods.append(chg)
                chg.number = x.lastcharge[-1].number
                chg.tags = x.lastcharge[-1].tags
            else:
                x.arrangement = chg
            x.unspecified.append(chg)
            x.lastcharge.append(chg)
            x.multi = None
            continue
        elif (x.lastcharge or x.adj) and b in ORIENTATIONS:
            if x.lastcharge:
                x.lastcharge[-1].tags.append(ORIENTATIONS[b])
            else:
                unknown("charge", x.adj)
            x.was = 'orientation'
            continue
        elif x.was == 'field division' and x.fielddivision and b in LINES:
            if x.fielddivision[-1].fielddesc:
                x.fielddivision[-1].fielddesc += ':' + LINES[b]
            continue
        elif x.lastcharge and b in LINES:
            x.lastcharge[-1].tags.append(LINES[b])
            continue
        elif (x.lastcharge 
              and x.lastcharge[-1].category in ('monster', 'beast', 'bird',
                                                'reptile', 'monster, sea')
              and 'arrangement, creature, %s' % b in CHARGES):
            x.lastcharge[-1].mods.append(
                CHARGES['arrangement, creature, %s' % b])
            continue
        elif (x.lastcharge
              and x.lastcharge[-1].category
              and (x.lastcharge[-1].category.startswith('head, ')
                   or x.lastcharge[-1].category == 'head')
              and 'arrangement, head, %s' % b in CHARGES):
            x.lastcharge[-1].mods.append(
                CHARGES['arrangement, head, %s' % b])
            continue
        elif b in POSTURES or b in BIRD_POSTURES or b in FISH_POSTURES:
            check_no_adj(x, b)
            if not x.lastcharge:
                raise BlazonException("Posture '%s' with no charge to modify!"
                                      % b, b)
            orig_lastcharge = x.lastcharge[-1]
            POST_MISC = (
                    'amphibian', 'ship', 'bow', 'axe', 'escarbuncle')
            BIRD_MISC = ('wing',)
            while (x.lastcharge
                   and x.lastcharge[-1].category not in (
                    'monster', 'beast', 'human', 'reptile', 'bird',
                    'monster, sea', 'fish', 'flower', 'head, beast')
                   and x.lastcharge[-1].name not in POST_MISC
                   and x.lastcharge[-1].name not in BIRD_MISC):
                x.lastcharge.pop()
            if not x.lastcharge:
                raise BlazonException("%s is a posture, but a '%s' is not an appropriate creature!" % (b, orig_lastcharge.name), orig_lastcharge.blazon+' '+b)
            if ((x.lastcharge[-1].category in ('monster', 'beast', 'human',
                                               'reptile',
                                               'monster, sea',
                                               'flower', 'head, beast')
                 or x.lastcharge[-1].name in POST_MISC)
                and b in POSTURES):
                x.lastcharge[-1].add_posture(POSTURES[b])
                continue
            elif ((x.lastcharge[-1].category in ('bird', 'monster')
                   or x.lastcharge[-1].name in BIRD_MISC)
                  and b in BIRD_POSTURES):
                x.lastcharge[-1].add_posture(BIRD_POSTURES[b])
                continue
            elif (x.lastcharge[-1].category in ('monster, sea', 'fish') 
                  and b in FISH_POSTURES):
                x.lastcharge[-1].add_posture(FISH_POSTURES[b])
                continue
            else:
                raise BlazonException("%s is a posture, but a '%s' is a %s, not an appropriate creature!" % (b, x.lastcharge[-1].name, x.lastcharge[-1].category or x.lastcharge[-1].name), b)
        elif (x.lastcharge
              and x.lastcharge[-1].name == 'cross, as charge'
              and b in CROSS_FAMILIES):
            x.lastcharge[-1].tags.append(CROSS_FAMILIES[b])
            # Possibly clear an extraneous 'of'.
            x.mod = None
            continue
        elif ('field division, %s' % b in CHARGES or b in VAIRYS
              or (b in CHARGES
                  and CHARGES[b].name.startswith('field division,'))
              or b in ('parted',)):
            #print 'field division', b
            check_no_adj(x, b)
            if b in ('parted',):
                if blist[0].endswith('wise'):
                    del blist[0]
                charge = None
            elif b in VAIRYS:
                charge = copy.deepcopy(CHARGES['field treatment, %s' % b])
            elif 'field division, %s' % b in CHARGES:
                charge = CHARGES['field division, %s' % b]
            else:
                charge = CHARGES[b]
            if not x.fielddivision:
                if x.unspecified:
                    if charge:
                        x.lasttincture = ComplexTincture(charge)
                    else:
                        x.lasttincture = MultiTincture([])
                    if isinstance(x.unspecified[0], Field):
                        x.lasttincture.on_field = True
                    for u in x.unspecified:
                        u.tincture = x.lasttincture
                    x.unspecified = []
                else:
                    x.lasttincture.complicate(charge)
            else:
                x.lasttincture = ComplexTincture(charge)
                if b in VAIRYS:
                    x.lasttincture.fieldextras.append(charge)
            if x.fielddivision:
                x.fielddivision[-1].add_tincture(x.lasttincture)
            x.fielddivision.append(x.lasttincture)
            x.was = 'field division'
            continue
        else:
            assert x.mod in (None, 'of') or x.mod in WITHS or x.mod in ATOPS, x.mod

        if b in NUMBERS:
            #print 'NUMBER', b, x.mod
            if x.number is not None:
                if x.adj == 'sets' and x.mod == 'of':
                    x.number *= NUMBERS[b]
                    x.adj = None
                    x.mod = None
                    continue
                else:
                    check_no_adj(x, b)
                    raise BlazonException(
                        "Multiple numbers without a charge between: %s and %s" 
                        % (x.number, b), b, blist=blist)
            if x.numdeprim:
                x.primary = False
            elif x.commadeprim:
                x.numdeprim = True
            # A "cross of five golpes" is basically an other cross and
            # five golpes
            if (x.mod == 'of'
                and (not x.lastcharge
                     or x.lastcharge[-1].name not in ('cross, as charge'))):
                num = NUMBERS[b]
                if (blist[0] == 'greater' and blist[1] == 'and'
                    and blist[3] == 'lesser'):
                    num += NUMBERS[blist[2]]
                    blist = blist[4:]
                if num >= 9:
                    num = '9 or more'
                if x.lastcharge and blist[0] in ('rays', 'points'):
                    x.lastcharge[-1].tags.append('of %s' % num)
                    blist.pop(0)
                elif x.fielddivision:
                    pass
                else:
                    lb = get_prev(x)
                    raise BlazonException("Weird use of 'of %s'!" % b, 
                                          lb + ' ' + b,
                                          blist=blist)
                    
                x.mod = None
                x.was = 'number'
            else:
                assert x.mod in (None, 'of') or x.mod in WITHS or x.mod in ATOPS, x.mod
                x.number = NUMBERS[b]
                if x.multiplier:
                    x.number *= x.multiplier
                    x.multiplier = None
                if x.mod == 'of':
                    x.was = 'of number'
                else:
                    x.was = 'number'
            continue

        if b in TINCTURES:
            #print 'TINCTURE', b, x.unspecified, x.was
            t = copy.deepcopy(TINCTURES[b])
            check_no_adj(x, b, blist=blist, prev=get_prev(x, 1))
            if not x.unspecified:
                if x.was in ('field treatment', 'counterchange'):
                    continue
                old_was = x.was
                x.was = 'tincture'
                if old_was in ('detail',):
                    continue
                elif x.fielddivision:
                    x.fielddivision[-1].add_tincture(t)
                    if x.fielddivision[-1].on_field:
                        t.on_field = True
                    x.lasttincture = t
                    if old_was == 'and' and len(x.fielddivision) > 1:
                        #print 'popping at', b
                        x.fielddivision.pop()
                    continue
                elif x.multi is not None:
                    x.lasttincture = t
                    if isinstance(x.multi.tincture, MultiTincture):
                        x.multi.tincture.add_tincture(t)
                    else:
                        x.multi.tincture = MultiTincture([x.multi.tincture, t])
                    continue
                elif (x.lastcharge and x.lastcharge[-1].number == 2
                      and not isinstance(x.lastcharge[-1].tincture, 
                                         MultiTincture)):
                    x.lasttincture = t
                    x.lastcharge[-1].tincture = MultiTincture([
                        x.lastcharge[-1].tincture, t])
                    continue
                elif x.lastcharge and x.lastcharge[-1].number == 3:
                    x.lasttincture = t
                    if isinstance(x.lastcharge[-1].tincture, MultiTincture):
                        if len(x.lastcharge[-1].tincture.tincts) >= 3:
                            raise BlazonException(
                                "Too many tinctures for 3 things! (at %s)"
                                % b)
                        x.lastcharge[-1].tincture.add_tincture(t)
                    else:
                        x.lastcharge[-1].tincture = MultiTincture([
                                x.lastcharge[-1].tincture, t])
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
                check_no_adj(x, b)
                if x.was in ('detail',):
                    continue
                elif x.wasi in ('field treatment',):
                    raise BlazonException("Weird counterchange!")
                else:
                    raise BlazonException(
                        "Counterchange without anything to color: %s" % b)
            if True: #x.primary is not False:
                if not x.field.tincture:
                    raise BlazonException("Counterchange without a field!")
                if x.primary is True and not x.field.tincture.is_complex():
                    raise BlazonException(
                        "Counterchange over a simple field!")
                unspec = [u for u in x.unspecified if not u.maintained]
                if len(unspec) == 1:
                    # Do this even if unspec[0].number != 1; that's how
                    # oanda does it.
                    unspec[0].tincture = MultiTincture([])
            x.lasttincture = None
            x.unspecified = []
            x.was = 'counterchange'
            continue
        #print ':', b, x.number, x.unspecified
        if (('field treatment, %s' % b in CHARGES 
             or 'field treatment, seme, %s' % b in CHARGES
             or b.startswith('crusilly'))
            and b not in ('roundels',) and b not in VAIRYS):
            assert x.lasttincture is not None
            chgs = x.lasttincture.add_treatment(b)
            #print 'TREATMENT', chgs, 'added to', x.lasttincture.fielddesc
            x.unspecified += chgs
            x.was = 'field treatment'
            #clear_fielddivision(x)
            continue
        elif b in ('semy', 'orle', 'annulet') and blist[0] == 'of':
            blist.pop(0)
            #print 'SEMY'
            if blist[0] in NUMBERS:
                num = NUMBERS[blist.pop(0)]
            else:
                num = 'seme'
            charge = depluralize(pop_blist(blist))
            while charge in DETAIL_ADJ:
                charge = depluralize(pop_blist(blist))
            if charge not in CHARGES:
                raise BlazonException("Semy of unknown charge: '%s'" % charge,
                                      charge, blist=blist)
            chg = copy.deepcopy(CHARGES[charge])
            chg.number = num
            if x.lasttincture is None:
                if (blist[0] == 'counterchanged'
                    or (blist[0] == 'all' and blist[1] == 'counterchanged')):
                    assert len(x.unspecified) == 1, x.unspecified
                    x.lasttincture = MultiTincture([])
                    x.unspecified[-1].tincture = x.lasttincture
                    x.unspecified = []
                else:
                    raise BlazonException(
                        "'%s of %s' without a tincture to modify!"
                        % (b, charge))
            x.lasttincture.add_extra(chg)
            if b == 'orle':
                arr = copy.deepcopy(CHARGES['arrangement, in orle'])
                chg.mods.append(arr)
                x.unspecified.append(arr)
            elif b == 'annulet':
                arr = copy.deepcopy(CHARGES['arrangement, in annulo'])
                chg.mods.append(arr)
                x.unspecified.append(arr)
            if charge in IMPLIED_TINCTURES:
                assert not x.unspecified, x.unspecified
                chg.tincture = copy.deepcopy(
                    TINCTURES[IMPLIED_TINCTURES[charge]])
            else:
                x.unspecified.append(chg)
            x.lastcharge.append(chg)
            x.multi = None
            x.was = 'tincture'
            #print 'SEMY LT', x.lasttincture, x.lasttincture.on_field
            if x.lasttincture.on_field:
                ft = copy.deepcopy(CHARGES['field treatment, seme, other'])
                x.unspecified.append(ft)
                x.lasttincture.add_extra(ft)
                chg.tags.append('seme on field')
            x.lastb.append(b)
            b = charge
            continue
        #print '!', b
        if b == 'the':
            assert not x.multiplier, x.multiplier
            x.number = 'the'
            x.was = 'number'
            continue
        elif b in ANDS:
            if x.primary is None:
                x.primary = True
            if x.was not in ('field treatment', 'counterchange'):
                x.was = 'and'
            continue
        elif b in SUSTAININGS:
            x.primary = False
            x.was = 'sustaining'
            continue
        elif b == ',':
            if x.commadeprim:
                x.primary = False
            if x.commamult:
                assert not x.multiplier, x.multiplier
                assert not x.number, x.number
                x.multiplier = x.commamult
                x.commamult = None
            #if x.on is not None:
            #    assert x.on.kid is not None,"Excess punctuation!"
            assert x.betweenness is None or len(x.betweenness) > 0, "Unfilled between!"
            #x.on = x.onstack.pop()
            x.betweenness = None
            if x.was not in ('field treatment',):
                x.was = 'comma'
            continue
        elif x.number is None and b in MAJOR_DETAILS:
            check_no_adj(x, b)
            x.on.kid.append(copy.deepcopy(CHARGES[MAJOR_DETAILS[b]]))
            x.was = 'detail'
            continue
        elif b in DETAILS:
            check_no_adj(x, b)
            if x.was not in ('field division',):
                x.was = 'detail'
            continue
        elif b in DEPRIM:
            check_no_adj(x, b)
            if x.was not in ('field division',):
                x.was = 'detail'
            x.primary = False
            continue
        elif b in ARRANGEMENTS:
            #print 'ARRANGEMENT'
            check_no_adj(x, b)
            x.was = 'arrangement'
            continue
        elif x.number is not None and b in CHARGE_ADJ:
            #print 'CHARGE_ADJ'
            check_no_adj(x, b, prev=get_prev(x, 1))
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
        elif b in ('in',) and blist[0] == 'its' and blist[1] not in ALL_WORDS:
            # e.g., "in its beak"
            del blist[:2]
            x.was = 'detail'
            continue
        elif (b in ('in',) and blist[0] == 'its' and blist[1] in LOCATIONS
              and (blist[2] not in ALL_WORDS or blist[2] in CHARGES)):
            # e.g., "in its sinister paw"
            del blist[:3]
            x.was = 'detail'
            continue
        elif b == 'with' and blist[0] == 'its' and (
            blist[1] in CHARGES or blist[1] not in ALL_WORDS):
            # e.g., enfiling "with its tail" or sustaining "with its talons"
            del blist[:2]
            continue
        elif b in CHARGES and blist[0] == 'to' and blist[1] in LOCATIONS:
            # e.g., a belt "buckle to base"
            del blist[:2]
            x.was = 'detail'
            continue

        if b not in ('of',):
            clear_fielddivision(x)

        if x.number is None and b in IMPLIED_NUMBER:
            assert not x.multiplier, x.multiplier
            x.number = IMPLIED_NUMBER[b]

        res = proc(x, depluralize(b), b, blist)
        #print res, depluralize(b)
        if not res and b.startswith('demi-'):
            res = proc(x, depluralize(b[len('demi-'):]), b, blist)
            if res:
                chg = x.unspecified[-1]
                if chg.category not in ('monster', 'beast', 'bird'):
                    raise BlazonException("Unexpected demi- charge: "+b, b)
                demi = copy.deepcopy(CHARGES['%s, demi' % chg.category])
                demi.number = chg.number
                chg.mods.append(demi)
                x.unspecified.append(demi)
                x.multi = None
        if res:
            x.mod = None
        else:
            if x.lastcharge and x.lastcharge[-1].name == 'symbol':
                x.was = 'symbol'
                pass
            elif x.number is not None and x.adj != 'sets':
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
                    #print 'adj', b
                    x.adj = b
                x.was = 'adjective'
            elif b in ('overall',):
                x.primary = False
            elif b in WITHS:
                # Could still be a primary if this is:
                # Sable, in base a wombat Or.
                # or
                # Vert, within an annulet an acorn argent.
                if x.lastcharge and x.primary:
                    x.primary = None # Not primary until 'and'
                x.mod = b
                if WITHS[b] is not None:
                    assert not x.multiplier, x.multiplier
                    x.number = WITHS[b]
                x.was = 'with'
            elif (b == 'charged' and blist[0] == 'on' and blist[1] == 'the'
                  and blist[3] == 'with'
                  and (blist[2] in CHARGES or blist[2] not in ALL_WORDS)):
                # charged on the cuff/head/shoulder with
                del blist[:4]
                if x.primary:
                    x.primary = None # Not primary until 'and'
                x.mod = 'charged with'
                x.was = 'with'
            elif b == 'each of' and x.was == 'with':
                if blist[0] not in NUMBERS:
                    raise BlazonException(
                        "'each of' followed by '%s', not a number!" % blist[0],
                        b, blist=blist)
                x.commamult = NUMBERS[blist[0]]
            elif b == 'each':
                b2 = pop_blist(blist)
                if b2 in WITHS and blist[0] in ('a', 'an'):
                    del blist[0]
                    if x.primary:
                        x.primary = None # Not primary until 'and'
                    assert not x.multiplier, x.multiplier
                    x.number = x.lastcharge[-1].number
                    x.mod = 'charged with'
                    x.was = 'with'
                elif b2 == depluralize(x.lastcharge[-1].name):
                    b3 = pop_blist(blist)
                    if b3 not in WITHS or blist[0] not in ('a', 'an'):
                        dont_understand('%s %s' % (b, b2), b3, blist)
                    del blist[0]
                    if x.primary:
                        x.primary = None # Not primary until 'and'
                    assert not x.multiplier, x.multiplier
                    x.number = x.lastcharge[-1].number
                    x.mod = 'charged with'
                    x.was = 'with'
                else:
                    dont_understand(b, b2, blist)
            elif b in ATOPS or b in ('issuant', 'elongated'):
                if x.was in ('charge', 'detail'):
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
                if x.primary:
                    x.primary = None
                if MAINTAININGS[b] is not None:
                    assert not x.multiplier, x.multiplier
                    x.number = MAINTAININGS[b]
                x.was = 'maintaining'
            elif b == '.':
                x.was = 'period'
                pass
            elif b in ('to',):
                dont_understand(b, blist[0], blist[1:])
            elif (b.endswith('ed') and x.was == 'tincture'
                  and blist[0] in TINCTURES):
                # X sable vested azure
                del blist[0]
            elif x.was == 'charge of':
                unknown("'charge of' phrase",
                        "%s of %s" % (x.lastcharge[-1].blazon, b),
                        blist)
            else:
                unknown("noncharge word after '%s'" % x.was, b, blist,
                        prev=get_prev(x))

    #assert x.betweenness is None, x.betweenness
    assert not x.fielddivision, x.fielddivision

    if x.field.tincture is None:
        raise BlazonException("No tincture for field!")

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
