import copy

def coalesce(l):
    l = list(l)
    idx = 0
    while idx < len(l) - 1:
        if l[idx].combinable_with(l[idx + 1]):
            if l[idx + 1].number is not None:
                l[idx].number += l[idx + 1].number
            del l[idx + 1]
        else:
            idx += 1
    return l

class Thingy(object):
    name = None
    tincture = None
    between = None

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
        for l in self.tincture.fielddescription():
            yield l
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

class Charge(Thingy):
    name = None
    number = None
    maintained = False

    def __init__(self, name, desc, category=False):
        self.name = name
        self.desc = desc
        self.category = category
        self.mods = []
        self.tags = []
        # Ones where we'r moore likely to conflict with something without
        self.iffy_tags = []
        self.seealso = []

    def combinable_with(self, other):
        return (other.name == self.name and other.maintained == self.maintained
                and self.tincture == other.tincture and self.mods == other.mods
                and self.tags == other.tags and self.between == other.between
                and self.iffy_tags == other.iffy_tags)
    
    def render(self):
        return """<circle cx="50" cy="50" r="50" fill="%s" /><text x="5" y="40" fill="grey">%s</text>""" % (self.tincture, self.name)

    def tree(self):
        yield "Charge: %s %s" % (self.tincture, self.name)

    def describe(self, as_mod=False):
        assert self.between is None, self.between
        if self.maintained:
            return
        tagbit = ''
        tags = list(self.tags)
        primtags = list(tags)
        tags += self.iffy_tags
        if self.tincture:
            tags = [self.tincture.tincture] + tags

        if self.number == 'seme':
            tags = ['seme'] + tags
        elif self.number in (None, 'the'):
            pass
        elif self.number < 10:
            tags = ['%s' % self.number] + tags
            if self.number < 4:
                primtags = ['%s' % self.number] + primtags
        else:
            tags = ['10 or more'] + tags

        if tags:
            tagbit = ':' + ':'.join(tags)
        yield "%s%s" % (self.desc, tagbit)
        if not as_mod:
            for c in self.seealso:
                yield "%s%s" % (c.desc, tagbit)
        if self.tincture:
            if 'primary' in self.tags and not as_mod:
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
    def __init__(self, tincture, csscolor=None, fielddesc=None):
        self.tincture = tincture
        self.css = csscolor
        self.fielddesc = fielddesc
        self.fieldextras = []
        self.chargeextras = []
        self.on_field = False

    def __str__(self):
        return self.css
    
    def add_treatment(self, treatment):
        from words import CHARGES
        if 'field treatment, %s' % treatment in CHARGES:
            a = copy.deepcopy(CHARGES['field treatment, %s' % treatment])
        else:
            a = copy.deepcopy(CHARGES['field treatment, seme, %s' % treatment])
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
        yield self.fielddesc
        for e in self.fieldextras:
            for d in e.describe():
                yield d

class Fieldless(Tincture):
    def __init__(self):
        Tincture.__init__(self, None)

    def fielddescription(self):
        return ()

class ComplexTincture(Tincture):
    def __init__(self, fieldcharge):
        Tincture.__init__(self, 'multicolor', fielddesc=fieldcharge.desc)
        self.fieldcharge = fieldcharge
        self.tcnt = 0
    
    def add_tincture(self, tincture):
        if self.tcnt == 0:
            self.fielddesc += ':' + tincture
        elif self.tcnt == 1:
            self.fielddesc += ':~and ' + tincture
        else:
            assert False, (self.fielddesc, self.tcnt, tincture)
        self.tcnt += 1
    
    def add_treatment(self, treatment):
        self.add_tincture('multicolor')
        return Tincture.add_treatment(self, treatment)

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
