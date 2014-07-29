# -*- coding: utf-8 -*-

import os, codecs
import copy

from structs import Tincture, Fieldless, Charge

TINCTURES = {
    '(fieldless)': Fieldless(),
}
TINCTURE_ALIASES = {
    'azure': ['de larmes'],
    'sable': ['de poix'],
    'purpure': ['de vin'],
    'gules': ['de sangue'],
    'vert': ["d'huile"],
    'argent': ["d'eau"],
    'or': ["d'or"],
    'counterermine': ['counter-ermine'],
    }

FURS = {
    'ermined',
}

COUNTERCHANGEDS = {
    'counterchanged',
    'counter-changed',
    }

ANDS = {
    'and',
    'and for augmentation',
    'conjoined with',
    'conjoined in pale with',
    'conjoined to',
    'enfiling',
    'between the head and tail',
}

SUSTAININGS = {
    'sustaining',
    'sustained by',
}

MAINTAININGS = {
    'maintaining',
    'maintaining between them',
    'maintaining on the outer swirl',
    'gorged of',
    'perched upon',
    'distilling',
    'attired of',
    'grasping',
    'sinister forepaw resting on a maintained',
    }

# "Charged withs" or "withins".
# Value is implied number, if any.
WITHS = {
    'in': None,
    'within': None,
    'all within': None,
    'within and conjoined to': None,
    # charged withs
    'charged with': None,
    'each arm charged with a': 4,  # for crosses
    'each arm charged with an': 4,  # for crosses
    'decorated with': None,
}

ATOPS = {
    'atop',
    'fastened to',
    'hanging from',
    'on',  # Can also be used in other ways.
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
    'two pairs of': 4,
    }

CHARGES = {}
DESC_TO_CHARGE = {}

LOCATIONS = {
    'base',
    'chief',
    'dexter',
    'sinister',
    'dexter chief',
    'sinister chief',
    'canton',
    }
ARRANGEMENTS = {
    'one and two', 'two and one',
    'two and two',
    'two , two and two',
    'two , two , and two',
}
ORIENTATIONS = {}

PERIPHERALS = {'chief', 'base', 'bordure', 'orle', 'gore', 'flaunch', 'fillet'}

BETWEEN = frozenset(('between',))

MAJOR_DETAILS = {
    'winged': 'winged object',
    }

DETAILS = set()
CONTOURNYS = {
    'contourny',
    'contourney',
    'countourny',
}
DETAILS.update(CONTOURNYS)

LINES = {'grady': 'indented',
         u'ployé': 'ploye',
         'doubly-enarched': 'enarched',
         'endorsed': 'cotised'}

BIRD_POSTURES = {}
BIRD_POSTURE_ALIASES = {
    'rising': 'rousant',
    'volant': 'volant guardant',
    'other bird posture': 'volant in chevron addorsed',
    }
BIRD_TYPES = {}

FISH_POSTURES = {}
FISH_POSTURE_ALIASES = {
    'hauriant': 'haurient',
    }

POSTURES = {}
POSTURE_ALIASES = {
    'rampant': ['segreant', 'salient', 'clymant'],
    'passant': ['courant'],
    'affronte': ['affronty', 'sejant affronty'],
    }

CROSS_FAMILIES = {}
CROSS_ALIASES = {
    'crosslet': ['of saint julian'],
    'doubled': ['russian orthodox'],
    'flory': ['patonce'],
    'other cross': ['of saint brigid', 'canterbury'],
    }

DEFAULT_CHARGE = Charge('?', '?')

#SYMBOLS = {'elder futhark'}

ALSOS = {'flower, few petals'}
CATEGORIES = {}

EXPLICIT_CATEGORIES = {'human figure': 'human'}

IMPLIED_NUMBER = {
    'flames': 1,
    'flaunches': 2,
    }
IMPLIED_TINCTURES = {
    'bezant': 'or',
    'plate': 'argent',
    'hurt': 'azure',
    'torteau': 'gules',
    'pellet': 'sable',
    'pomme': 'vert',
    'golpe': 'purpure',
    }

MULTIPLE_TINCTURES = {
    'flower, rose',  # for double rose
}

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

# vairy is a field treatment that's written like a field division
VAIRYS = {
    'vairy',
    'counter-vairy',
}

CHARGE_ADJ = {
    'winged': 'monster, winged',
    'bat-winged': 'monster, winged'
    }

DETAIL_ADJ = {
    'empty',
    'bottom-whorl',
    'elder futhark',
    'lower case',
    'brunette',
    'caucasian',
    }

BLACKLIST = {
    'throughout',
    'cross of',
    'fish', # From head, fish
    'enflamed', # Can be a line, but usually isn't.
    }

# These we want to treat as words for purposes of spellchecking, but we only
# understand them in certain manually-coded contexts.
MISC_WORDS = {'of', 'on', 'to', 'her', 'his', 'its', 'at', 'with',
              'in', 'the'}

ALL_WORDS = set()

LOADED = False

def loadwords():
    global LOADED
    if LOADED:
        return
    
    with codecs.open(os.path.join(os.path.dirname(__file__), 'details.txt'),
              encoding='utf-8') as fil:
        for l in fil:
            if l.strip() and not l.startswith('#'):
                DETAILS.add(l.strip())

    with open(os.path.join(os.path.dirname(__file__), 'my.cat')) as mydotcat:
        for l in mydotcat:
            l = l.strip()
            if l.startswith('|'):
                if l.startswith('|tincture:') and '=' not in l:
                    typ, tinct = l.split(':')
                    if '<' in tinct:
                        tinct, rest = tinct.split('<', 1)
                    if tinct not in TINCTURES and tinct != 'brown':
                        TINCTURES[tinct] = Tincture(tinct)
                        if tinct in TINCTURE_ALIASES:
                            for a in TINCTURE_ALIASES[tinct]:
                                TINCTURES[a] = Tincture(tinct)
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
                elif l.startswith('|fish_posture:'):
                    typ, post = l.split(':')
                    if '<' in post:
                        post, rest = post.split('<', 1)
                    name = post
                    if name.startswith('fish '):
                        name = name[len('fish '):]
                    names = [name]
                    for a in FISH_POSTURE_ALIASES:
                        if name.startswith(a):
                            names.append(FISH_POSTURE_ALIASES[a] 
                                         + name[len(a):])
                    for n in list(names):
                        if n.endswith(' to dexter'):
                            names.append(n[:-len(' to dexter')])
                    
                    for n in names:
                        FISH_POSTURES[n] = post
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
                        for c in CONTOURNYS:
                            names.append(stem + ' ' + c)
                    else:
                        names.append(name + ' guardant')

                    for n in names:
                        POSTURES[n] = post
                elif l.startswith('|cross_family:'):
                    typ, fam = l.split(':')
                    CROSS_FAMILIES[fam] = fam
                    if fam in CROSS_ALIASES:
                        for a in CROSS_ALIASES[fam]:
                            CROSS_FAMILIES[a] = fam
                elif l.startswith('|orientation:'):
                    typ, orient = l.split(':')
                    if '<' in orient:
                        orient, rest = orient.split('<', 1)
                    ORIENTATIONS[orient] = orient
                elif l.startswith('|line:'):
                    typ, ln = l.split(':')
                    if '<' in ln:
                        ln, rest = ln.split('<', 1)
                    if ln not in BLACKLIST:
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

                assert desc not in DESC_TO_CHARGE, desc
                DESC_TO_CHARGE[desc] = charge
            elif ' - see ' in l:
                name, see = l.split(' - see ')
                name = name.lower()
                if name in BLACKLIST:
                    continue
                if see.startswith('also '):
                    see = see[len('also '):]
                    also = True
                else:
                    also = name in ALSOS
                seenames = see.split(' and ')
                sees = []
                for n in seenames:
                    # We don't handle sees referring to a see later in the
                    # alphabet; so sees referring to other sees need correction.
                    CORRECTIONS = {
                        'fish, lobster': 'arthropod, lobster',
                        'peripheral on ly': 'peripheral only',
                        'bird': 'bird, whole',
                        'sun': 'sun, whole',
                        'roundel': 'roundel, whole',
                        }
                    if n in CORRECTIONS:
                        n = CORRECTIONS[n]
                    if n in CATEGORIES and n not in CHARGES:
                        sees += CATEGORIES[n]
                        assert None not in sees, (sees, n)
                    else:
                        if n not in CHARGES:
                            assert ', ' in n, n
                            most, lastbit = n.rsplit(', ', 1)
                            chargemod = copy.deepcopy(CHARGES[most])
                            if lastbit == 'seme':
                                chargemod.number = 'seme'
                            elif lastbit in LINES and most in PERIPHERALS:
                                chargemod.tags.append(LINES[lastbit])
                            elif lastbit == 'charged':
                                chargemod.tags.append('charged')
                            else:
                                assert most == 'cross, as charge', n
                                assert lastbit in CROSS_FAMILIES, n
                                chargemod.tags.append(CROSS_FAMILIES[lastbit])
                            sees.append(chargemod)
                        else:
                            assert CHARGES[n] is not None, n
                            sees.append(CHARGES[n])
                        assert None not in sees, (sees, n)
                if also:
                    assert name in CHARGES, name
                else:
                    assert (name not in CHARGES or CHARGES[name] is None 
                            #or CHARGES[name].name == sees[0].name
                            or CHARGES[name].category), (name, CHARGES[name], sees[0])
                    first = sees.pop(0)
                    CHARGES[name] = copy.deepcopy(first)
                    # Copying the seealso of just the first is weird
                    CHARGES[name].seealso = []
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
    
    with codecs.open(os.path.join(os.path.dirname(__file__), 'aliases.txt'),
              encoding='utf-8') as fil:
        for l in fil:
            if l.strip() and not l.startswith('#'):
                k, val = l.strip().split(': ')
                assert (k not in CHARGES or CHARGES[k] is None
                        or CHARGES[k].name == val), (k, val, CHARGES[k].name)
                charges = []
                for v in val.split(' & '):
                    if '*' in v:
                        v, multiplier = v.split('*')
                    else:
                        multiplier = None
                    tags = v.split(':')
                    v = tags.pop(0)
                    assert v in CHARGES, v
                    chg = copy.deepcopy(CHARGES[v])
                    for t in tags:
                        if t == 'seme' or t.isdigit():
                            chg.number = t
                        else:
                            chg.tags.append(t)
                    if multiplier:
                        chg.multiplier = int(multiplier)
                    charges.append(chg)
                CHARGES[k] = charges[0]
                for a in charges[1:]:
                    CHARGES[k].seealso.append(a)

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

    ALL_WORDS.update(TINCTURES,
                     CHARGES, DETAILS, ARRANGEMENTS, ORIENTATIONS, POSTURES,
                     BIRD_POSTURES, NUMBERS, ANDS, SUSTAININGS, MAINTAININGS,
                     WITHS, CROSS_FAMILIES, ATOPS,
                     DETAIL_ADJ, COUNTERCHANGEDS,
                     MISC_WORDS)

    LOADED = True
