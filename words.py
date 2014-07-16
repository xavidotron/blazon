# -*- coding: utf-8 -*-

import copy

from structs import Tincture, Fieldless, Charge

TINCTURES = {
    'azure': Tincture('azure', 'blue', 'AZ'),
    'sable': Tincture('sable', 'black', 'SA'),
    'purpure': Tincture('purpure', 'purple', 'PU'),
    'gules': Tincture('gules', 'red', 'GU'),
    'vert': Tincture('vert', 'green', 'VT'),
    'argent': Tincture('argent', 'white', 'AR'),
    'or': Tincture('or', 'gold', 'OR'),
    '(fieldless)': Fieldless(),
    }

ANDS = {
    'and',
    'conjoined with',
    'conjoined in pale with'
}

CHARGED_WITHS = {
    'charged with',
    'charged on the head with',
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
    'ten': 10,
    'a sheaf of': 3,
    }

CHARGES = {}

LOCATIONS = {'base', 'chief'}
ARRANGEMENTS = {
    'one and two', 'two and one',
    'two , two and two',
}
ORIENTATIONS = {}

PERIPHERALS = {'chief', 'base', 'bordure', 'orle', 'gore'}

BETWEEN = frozenset(('between',))

MAJOR_DETAILS = {'winged': 'winged object'}

DETAILS = {'slipped', 'leaved', 'bellied', 'breathing flames', 'fructed', 
           'barbed', 'seeded',
           'collared',
           'vented',
           'wings displayed', 'wings elevated', 'wings addorsed', 
           'wings elevated and addorsed',
           'paw upraised',
           'inverted',
           'affronty', 'regardant', 'reguardant',
           'gowned',
           'eradicated',
           'fimbriated',
           'queue-forchy', 'fitchy',
           'couped', 'erased',
           'erect',
           'nowed in', 'nowed',
           'fretted with',
           'rising from',
           'throughout', 'reversed',
           'transfixed by',
           'in her vanity', 'in its piety', 'in her plentitude',
           'crined'}

LINES = {'grady': 'indented',
         u'ployé': 'ploye'}

BIRD_POSTURES = {}
BIRD_POSTURE_ALIASES = {
    'rising': 'rousant',
    'volant': 'volant guardant',
    }
BIRD_TYPES = {}

POSTURES = {}
POSTURE_ALIASES = {'rampant': ['segreant'],
                   'passant': ['courant', 'passant guardant']}

CROSS_FAMILIES = {}

DEFAULT_CHARGE = Charge('?', '?')

#SYMBOLS = {'elder futhark'}

ALIASES = {
    'bird, whole': ['bird'],
    'caltrap': ['caltrop'],
    'charge treatment, seme, crusily': ['charge treatment, seme, crusilly'],
    'cross, as charge': ['cross'],
    'cross, throughout': ['cross throughout'],
    'field treatment, seme, crusily': ['field treatment, seme, crusilly'],
    'field treatment, vairy': ['field treatment, vair'],
    'fleur de lys': ['fleurs-de-lis', 'fleur-de-lys', 'fleurs-de-lys'],
    'gate': ['torii gate'],
    'jewelry': ['rosary'],
    'knot': ['quatrefoil knot'],
    'monster, sea, other': ['sea-stag'],
    'mullet': ['mullet, charged', 'spur rowel'],
    'paw print': ['pawprint'],
    'plant, heather': ['sprig of heather'],
    'plant, wheat': ['ears of wheat', 'ear of wheat'],
    'quill': ['quill pen'],
    'roundel, whole': ['roundel'],
    'sun, whole': ['sun, whole, charged'],
    'tree, rounded shape': ['tree'], # This is the default tree.
    'wreath, not laurel': ['wreath'],
}
MULTI = {
    'bow and arrow': ['bow', 'arrow'],
    'holly sprig': ['holly', 'sprig'],
    'wreath of thorns': ['wreath', 'thorn'],
    'elm hurst': ['tree, multiple', 'tree, rounded shape'],
}
ALSOS = {'flower, few petals'}
CATEGORIES = {}

EXPLICIT_CATEGORIES = {'human figure': 'human'}

IMPLIED_NUMBER = {'flames': 1}
IMPLIED_TINCTURES = {'bezant': 'or',
                     'plate': 'argent',
                     'hurt': 'azure',
                     'torteau': 'gules',
                     'pellet': 'sable',
                     'pomme': 'vert',
                     'golpe': 'purpure'}

SEMYS = {
    'billety': 'billet',
    'billetty': 'billet',
    'bezanty': 'bezant',
    'crescenty': 'crescent',
    'crusily': 'cross',
    'delphy': 'delf',
    'escallopy': 'escallop',
    'estencely': 'spark',
    'estoilly': 'estoile',
    'fleury': 'fleur de lys',
    'goutty': 'goute',
}

CHARGE_ADJ = {'winged': 'monster, winged'}

BLACKLIST = {'throughout'}

LOADED = False

def loadwords():
    global LOADED
    if LOADED:
        return
    with open('my.cat') as mydotcat:
        for l in mydotcat:
            l = l.strip()
            if l.startswith('|'):
                if l.startswith('|tincture:') and '=' not in l:
                    typ, tinct = l.split(':')
                    if '<' in tinct:
                        tinct, rest = tinct.split('<', 1)
                    if tinct not in TINCTURES and tinct != 'brown':
                        TINCTURES[tinct] = Tincture(tinct)
                elif l.startswith('|bird_type:'):
                    typ, post = l.split(':')
                    if '<' in post:
                        post, rest = post.split('<', 1)
                    if post.endswith(' shaped'):
                        key = post[:-len(' shaped')]
                    else:
                        key = post
                    BIRD_TYPES[key] = post
                elif l.startswith('|bird_posture:'):
                    typ, post = l.split(':')
                    if '<' in post:
                        post, rest = post.split('<', 1)
                    name = post
                    if name.startswith('bird '):
                        name = name[len('bird '):]
                    names = [name]
                    for a in BIRD_POSTURE_ALIASES:
                        if name.startswith(a):
                            names.append(BIRD_POSTURE_ALIASES[a] 
                                         + name[len(a):])
                    for n in list(names):
                        if n.endswith(' to dexter'):
                            names.append(n[:-len(' to dexter')])
                    
                    for n in names:
                        BIRD_POSTURES[n] = post
                elif l.startswith('|posture:'):
                    typ, post = l.split(':')
                    if '<' in post:
                        post, rest = post.split('<', 1)
                    name = post
                    names = [name]
                    for a in POSTURE_ALIASES:
                        if name.startswith(a):
                            for v in POSTURE_ALIASES[a]:
                                names.append(v + name[len(a):])
                    if name.endswith(' to sinister'):
                        stem = name[:-len(' to sinister')]
                        names.append(stem + ' contourney')
                        names.append(stem + ' contourny')

                    for n in names:
                        POSTURES[n] = post
                elif l.startswith('|cross_family:'):
                    typ, fam = l.split(':')
                    CROSS_FAMILIES[fam] = fam
                elif l.startswith('|orientation:'):
                    typ, orient = l.split(':')
                    if '<' in orient:
                        orient, rest = orient.split('<', 1)
                    ORIENTATIONS[orient] = orient
                elif l.startswith('|line:'):
                    typ, ln = l.split(':')
                    if '<' in ln:
                        ln, rest = ln.split('<', 1)
                    LINES[ln] = ln
                else:
                    continue
            elif '|' in l:
                name, desc = l.split('|')

                cat = None
                if ', ' in name:
                    cat, typ = name.rsplit(', ', 1)
                    charge = Charge(name, desc, category=cat)
                    if typ in BLACKLIST:
                        pass
                    elif typ not in CHARGES:
                        CHARGES[typ] = charge
                    else:
                        if CHARGES[typ] is None or CHARGES[typ].category != typ:
                            CHARGES[typ] = None
                            
                    if cat not in CATEGORIES:
                        CATEGORIES[cat] = [charge]
                    else:
                        CATEGORIES[cat].append(charge)
                elif name in EXPLICIT_CATEGORIES:
                    charge = Charge(name, desc, 
                                    category=EXPLICIT_CATEGORIES[name])
                else:
                    charge = Charge(name, desc)
                CHARGES[name] = charge
                if name in ALIASES:
                    for alt in ALIASES[name]: 
                        CHARGES[alt] = charge

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
                    # Copying the seealso of just the first is weird
                    CHARGES[name].seealso = []
                    if name in ALIASES:
                        for alt in ALIASES[name]:
                            CHARGES[alt] = CHARGES[name]
                if 'bird, whole' in seenames and name in BIRD_TYPES:
                    CHARGES[name].iffy_tags.append(BIRD_TYPES[name])
                for s in sees:
                    CHARGES[name].seealso.append(s)
                if ', ' in name:
                    cat, typ = name.rsplit(', ', 1)
                    if cat == 'tree':
                        CHARGES['%s leaf' % typ] = CHARGES['leaf']
                        CHARGES['%s leaves' % typ] = CHARGES['leaves']
            else:
                assert False, l
    
    for w in MULTI:
        assert w not in CHARGES
        CHARGES[w] = copy.deepcopy(CHARGES[MULTI[w][0]])
        CHARGES[w].seealso += [CHARGES[a] for a in MULTI[w][1:]]

    for n in TINCTURES:
        tinct = TINCTURES[n]
        if tinct.fielddesc is None:
            key = "%s field" % tinct.tincture
            if key in CHARGES:
                tinct.fielddesc = CHARGES[key].desc
            else:
                ftkey = 'field treatment, %s' % tinct.tincture
                if ftkey in CHARGES:
                    tinct.fielddesc = CHARGES[ftkey].desc
    
    LOADED = True
