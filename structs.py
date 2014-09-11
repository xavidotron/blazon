import copy

DOUBLE_PRIMARIES = True

def coalesce(l):
    l = list(l)
    idx = 0
    while idx < len(l) - 1:
        comb = l[idx].combine_with(l[idx + 1])
        if comb is not None:
            del l[idx:idx + 2]
            l.insert(idx, comb)
        else:
            idx += 1
    return l

class Thingy(object):
    name = None
    tincture = None
    between = None

    # Return None or a combined thing.
    def combine_with(self, other):
        return None

class Parent(Thingy):
    kid = None
    category = None

class Field(Parent):
    BOXES_FOR_COUNT = {
        1: [(20,20,515,450)],
        2: [(20,20,255,450),(290,20,255,450)],
        3: [(20,20,255,255),(290,20,255,255),(155,295,255,255)]
        }

    def tree(self):
        yield "Field: %s" % self.tincture
        for l in self.kid.tree():
            yield "  " + l
    
    def describe(self):
        assert self.tincture is not None
        for l in self.tincture.fielddescription():
            yield l
        if self.kid is not None:
            for l in self.kid.describe():
                yield l

    def render(self):
        assert self.between is None
        # Draw a colored shield, then put our kids on it
        ret = """<svg height="100" width="100" viewBox="0 0 561 640"
      preserveAspectRatio="xMidYMid meet">
    <path stroke="black" stroke-width="1" fill="%s"
        d="M 0.00,319.00
           C 7.00,482.00 140.00,580.00 279.00,639.00
             418.00,580.00 553.00,482.00 560.00,320.00
             560.00,320.00 560.00,0.00 560.00,0.00
             560.00,0.00 0.00,0.00 0.00,0.00
             0.00,0.00 0.00,319.00 0.00,319.00 Z" />""" % (self.tincture)
        if isinstance(self.kid,Group):
            bxs = self.BOXES_FOR_COUNT[len(self.kid)]
            for lcv in xrange(len(self.kid)):
                ret += """<svg x="%d" y="%d" width="%d" height="%d"
      viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">""" % bxs[lcv]
                ret += self.kid[lcv].render()
                ret += """</svg>"""
        else:
            ret += """<svg x="0" y="0" width="561" height="640"
      viewBox="0 0 100 100" preserveAspectRatio="xMidYMin">"""
            ret += self.kid.render()
            ret += """</svg>"""
        ret += """</svg>""" 
        return ret

def numtag_for(num):
    if num == 'seme':
        return 'seme'
    elif num in (None, 'the'):
        return None
    elif num < 10:
        return '%d' % num
    else:
        return '10 or more'

class Charge(Thingy):
    name = None
    number = None
    maintained = False
    multiplier = None
    blazon = None
    adj = None

    def __init__(self, name, desc, category=False):
        self.name = name
        self.desc = desc
        self.category = category
        self.mods = []
        self.tags = []
        self.seealso = []

    def combine_with(self, other):
        if (other.name == self.name and other.maintained == self.maintained
            and self.mods == other.mods
            and self.tags == other.tags and self.between == other.between):
            ret = copy.deepcopy(self)
            if other.number is not None:
                ret.number += other.number
            if self.tincture != other.tincture:
                ret.tincture = MultiTincture([self.tincture, other.tincture])
            return ret
        else:
            return None
    
    def render(self):
        return """<circle cx="50" cy="50" r="50" fill="%s" /><text x="5" y="40" fill="grey">%s</text>""" % (self.tincture, self.name)

    def tree(self):
        yield "Charge: %s %s" % (self.tincture, self.name)

    def describe(self, as_mod=False):
        from words import PRIMTAGS_WHITELIST

        assert self.between is None, self.between
        if self.maintained:
            return
        tags = list(self.tags)
        primtags = [t for t in tags if t in PRIMTAGS_WHITELIST]
        if self.tincture:
            tags = [self.tincture.tincture] + tags

        numtag = numtag_for(self.number)
        if self.number and self.number != 'the':
            if self.number < 4:
                primtags = ['%d' % self.number] + primtags
            else:
                primtags = ['4 or more'] + primtags

        tagbit = ''
        if tags:
            tagbit = ':' + ':'.join(tags)
        numtagbit = ''
        if numtag:
            numtagbit = ':' + numtag
        yield "%s%s%s" % (self.desc, numtagbit, tagbit)
        if not as_mod:
            for c in self.seealso:
                if c.number:
                    yield "%s:%s%s" % (c.desc, numtag_for(c.number), tagbit)
                elif c.multiplier and numtagbit:
                    yield "%s:%s%s" % (c.desc,
                                       numtag_for(self.number * c.multiplier),
                                       tagbit)
                else:
                    yield "%s%s%s" % (c.desc, numtagbit, tagbit)
        if self.tincture:
            if 'primary' in self.tags and not as_mod and DOUBLE_PRIMARIES:
                # Add an additonal instance, without the tincture, for 
                # sig diffness
                yield "%s:%s" % (self.desc, ':'.join(primtags))
            for c in self.tincture.chargeextras:
                for d in c.describe():
                    yield d
        for c in self.mods:
            for d in c.describe(as_mod=True):
                assert isinstance(d, basestring), d
                yield d

    def add_posture(self, posture):
        self.tags.append(posture)
        for c in self.mods:
            c.tags.append(posture)

    def __repr__(self):
        return 'Charge:'+repr((self.name, self.desc, self.category))

class Ordinary(Parent):
    arounds = []

class Bend(Ordinary):

    BOXES_FOR_BETWEEN = {
        2: [(55,5,40,40),(10,55,40,40)],
        3: [(40,3,30,30),(65,27,30,30),(10,55,30,30)]
        }

    def render(self):
        ret = """<line x1="0" y1="0" x2="100" y2="100" stroke-width="20" stroke="%s"/>""" % self.tincture
        if self.between:
            bxs = self.BOXES_FOR_BETWEEN[len(self.between)]
            for lcv in xrange(len(self.between)):
                ret += """<svg x="%d" y="%d" width="%d" height="%d"
      viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">""" % bxs[lcv]
                ret += self.between[lcv].render()
                ret += """</svg>"""
        return ret

class Peripheral(Parent):
    outside = None

class Chief(Peripheral):

    BOXES_FOR_COUNT = {
        1: [(5,35,70,70)],
        2: [(5,35,40,40),(55,35,40,40)],
        3: [(5,32,30,30),(55,32,30,30),(30,67,30,30)]
        }

    def render(self):
        ret = """<line x1="0" y1="15" x2="100" y2="15" stroke-width="30" stroke="%s"/>""" % self.tincture
        if self.outside:
            if isinstance(self.outside,Group):
                bxs = self.BOXES_FOR_COUNT[len(self.outside)]
                for lcv in xrange(len(self.outside)):
                    ret += """<svg x="%d" y="%d" width="%d" height="%d"
          viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">""" % bxs[lcv]
                    ret += self.outside[lcv].render()
                    ret += """</svg>"""
            else:
                ret += """<svg x="0" y="30" width="100" height="100" 
      viewBox="0 0 100 100" preserveAspectRatio="xMidYMin">"""
                ret += self.outside.render()
                ret += """</svg>"""
    
        return ret

class Group(list, Thingy):
    def tree(self):
        for i in self:
            for l in i.tree():
                yield l

    def describe(self):
        l = coalesce(self)
        for i in l:
            for l in i.describe():
                yield l
        if self.between:
            for i in coalesce(self.between):
                for l in i.describe():
                    yield l

class Tincture(object):
    def __init__(self, tincture, fielddesc=None):
        self.tincture = tincture
        self.fielddesc = fielddesc
        self.fieldextras = []
        self.chargeextras = []
        self.on_field = False
        self.fieldcharge = None
        self.fdtincts = None

    def __str__(self):
        return self.tincture
    
    def add_treatment(self, treatment):
        from words import CHARGES, FURS
        if self.is_complex():
            self.fdtincts[-1].add_treatment(treatment)
            return
        if treatment in FURS:
            self.tincture = 'fur'
        else:
            self.tincture = 'multicolor'
        if 'field treatment, %s' % treatment in CHARGES:
            a = copy.deepcopy(CHARGES['field treatment, %s' % treatment])
        elif 'field treatment, seme, %s' % treatment in CHARGES:
            a = copy.deepcopy(CHARGES['field treatment, seme, %s' % treatment])
        else:
            a = copy.deepcopy(CHARGES[treatment])
        self.fieldextras.append(a)
        if 'charge treatment, %s' % treatment in CHARGES:
            b = copy.deepcopy(CHARGES['charge treatment, %s' % treatment])
        elif 'charge treatment, seme, %s' % treatment in CHARGES:
            b = copy.deepcopy(CHARGES['charge treatment, seme, %s' % treatment])
        else:
            b = None
        if b is not None:
            self.chargeextras.append(b)
            l = [a, b]
        else:
            l = [a]
        return l

    def add_extra(self, extra):
        self.fieldextras.append(extra)
        self.chargeextras.append(extra)

    def fielddescription(self):
        fd = self.fielddesc
        if self.fdtincts:
            fd += ':' + self.fdtincts[0].tincture
            if len(self.fdtincts) > 1:
                fd += ':~and ' + self.fdtincts[1].tincture
        yield fd
        for e in self.fieldextras:
            for d in e.describe():
                yield d
        if self.fdtincts:
            fdextras = []
            for fdt in self.fdtincts:
                fdextras += fdt.fieldextras
            for e in coalesce(fdextras):
                for d in e.describe():
                    yield d

    def complicate(self, fieldcharge):
        self.fielddesc = fieldcharge.desc
        self.fieldcharge = fieldcharge
        self.fdtincts = []
        if self.tincture != 'multicolor':
            from words import TINCTURES
            self.add_tincture(copy.deepcopy(TINCTURES[self.tincture]))
            self.tincture = 'multicolor'

    def is_complex(self):
        return self.fieldcharge is not None

    def add_tincture(self, tincture):
        #print 'a_t', tincture
        assert self.is_complex()
        assert self.fdtincts is not None
        assert isinstance(tincture, Tincture), tincture
        if len(self.fdtincts) < 2:
            self.fdtincts.append(tincture)
        else:
            self.fdtincts = [Tincture('multicolor'), Tincture('multicolor')]

class Fieldless(Tincture):
    def __init__(self):
        Tincture.__init__(self, None)

    def fielddescription(self):
        return ()

def ComplexTincture(fieldcharge):
    ret = Tincture('multicolor')
    ret.complicate(fieldcharge)
    return ret

class MultiTincture(Tincture):
    def __init__(self, tincts):
        Tincture.__init__(self, 'multicolor')
        self.tincts = tincts

    def fielddescription(self):
        for t in self.tincts:
            for d in t.fielddescription():
                yield d
    
    def add_tincture(self, tincture):
        self.tincts.append(tincture)
