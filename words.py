import copy

from structs import Tincture, Charge, Bend, Chief

TINCTURES = {
    'azure': Tincture('azure', 'blue', 'AZ'),
    'sable': Tincture('sable', 'black', 'SA'),
    'purpure': Tincture('purpure', 'purple', 'PU'),
    'gules': Tincture('gules', 'red', 'GU'),
    'vert': Tincture('vert', 'green', 'VE'),
    'argent': Tincture('argent', 'white', 'AR'),
    'or': Tincture('or', 'gold', 'OR'),
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

CHARGES = {}

ORDINARIES = {
    'bend': Bend()
    }

LOCATIONS = {'base', 'chief'}

PERIPHERALS = {
    'chief': Chief()
    }

PUNCT = frozenset((',','.'))

BETWEEN = frozenset(('between',))

DETAILS = {'slipped', 'leaved', 'bellied', 'breathing flames',
           'couped', 
           # ???
           'counterchanged'}

DEFAULT_CHARGE = Charge('?', '?')

ALIASES = {'cross, as charge': 'cross',
           'mullet': 'mullet, charged',
           'bird, whole': 'bird'}
ALSOS = {'flower, few petals'}
CATEGORIES = {}

def loadwords():
    with open('my.cat') as mydotcat:
        for l in mydotcat:
            l = l.strip()
            if l.startswith('|'):
                if l.startswith('|tincture:') and '=' not in l:
                    tag, tinct = l.split(':')
                    if '<' in tinct:
                        tinct, rest = tinct.split('<', 1)
                    if tinct not in TINCTURES:
                        TINCTURES[tinct] = Tincture(tinct)
                else:
                    continue
            elif '|' in l:
                name, desc = l.split('|')

                cat = None
                if ', ' in name:
                    cat, typ = name.rsplit(', ', 1)
                    if typ not in CHARGES:
                        CHARGES[typ] = Charge(typ, desc, category=cat)
                    else:
                        if CHARGES[typ] is None or CHARGES[typ].category != typ:
                            CHARGES[typ] = None
                            
                    if cat not in CATEGORIES:
                        CATEGORIES[cat] = [Charge(name, desc, category=cat)]
                    else:
                        CATEGORIES[cat].append(Charge(name, desc, category=cat))
                CHARGES[name] = Charge(name, desc, category=cat)
                if name in ALIASES:
                    CHARGES[ALIASES[name]] = Charge(name, desc, category=cat)

            elif ' - see ' in l:
                name, see = l.split(' - see ')
                if see.startswith('also '):
                    see = see[len('also '):]
                    also = True
                else:
                    also = name in ALSOS
                seenames = see.split(' and ')
                sees = []
                for n in seenames:
                    if n in CATEGORIES and n not in CHARGES:
                        sees += CATEGORIES[n]
                        assert None not in sees, (sees, n)
                    else:
                        assert n in CHARGES, n
                        sees.append(CHARGES[n])
                        assert None not in sees, (sees, n)
                if also:
                    assert name in CHARGES, name
                else:
                    assert (name not in CHARGES or CHARGES[name] is None 
                            or CHARGES[name].category), name
                    first = sees.pop(0)
                    CHARGES[name] = copy.deepcopy(first)
                for s in sees:
                    CHARGES[name].seealso.append(s)
            else:
                assert False, l
