
class Thingy(object):
    tincture = None
    between = None

class Parent(Thingy):
    kid = None

class Field(Parent):
    BOXES_FOR_COUNT = {
        1: [(20,20,515,450)],
        2: [(20,20,255,450),(290,20,255,450)],
        3: [(20,20,255,255),(290,20,255,255),(155,295,255,255)]
        }

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
    mods = []

    def __init__(self,name):
        self.name = name
    
    def render(self):
        return """<circle cx="50" cy="50" r="50" fill="%s" /><text x="5" y="40" fill="grey">%s</text>""" % (self.tincture, self.name)

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

class Group(list,Thingy):
    pass

class Tincture(object):
    
    def __init__(self,csscolor):
        self.css = csscolor

    def __str__(self):
        return self.css
