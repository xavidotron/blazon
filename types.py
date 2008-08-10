
class Thingy(object):
    color = None

class Parent(Thingy):
    kids = []

class Field(Parent):
    pass

class Charge(Thingy):
    name = None
    mods = []

class Color(object):
    pass
