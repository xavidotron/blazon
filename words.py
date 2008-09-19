from structs import Tincture, Charge, Bend, Chief

TINCTURES = {
    'azure': Tincture('blue'),
    'sable': Tincture('black'),
    'purpure': Tincture('purple'),
    'gules': Tincture('red'),
    'vert': Tincture('green'),
    'argent': Tincture('white'),
    'or': Tincture('gold')
    }

NUMBERS = {
    'a': 1,
    'an': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10
    }

CHARGES = {
    'eagle': lambda:Charge('eagle'),
    'lion': lambda:Charge('lion'),
    'mullet': lambda:Charge('mullet'),
    'sword': lambda:Charge('sword')
    }

ORDINARIES = {
    'bend': lambda:Bend()
    }

PERIPHERALS = {
    'chief': lambda:Chief()
    }

PUNCT = frozenset((',','.'))

BETWEEN = frozenset(('between',))

DEFAULT_CHARGE = lambda:Charge('?')
