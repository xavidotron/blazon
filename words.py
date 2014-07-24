# -*- coding: utf-8 -*-

import os, codecs
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
    }

WITHINS = {
    'within',
    'all within',
    'within and conjoined to',
    }

CHARGED_WITHS = {
    'charged with',
    'charged on the head with',
}

ATOPS = {
    'atop',
    'fastened to',
    'hanging from',
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
    'each arm charged with a': 4,  # for crosses
    'each arm charged with an': 4,  # for crosses
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

MAJOR_DETAILS = {'winged': 'winged object'}

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
    }
BIRD_TYPES = {}

FISH_POSTURES = {}
FISH_POSTURE_ALIASES = {}

POSTURES = {}
POSTURE_ALIASES = {'rampant': ['segreant', 'salient', 'clymant'],
                   'passant': ['courant']}

CROSS_FAMILIES = {}
CROSS_ALIASES = {
    'crosslet': ['of saint julian'],
    'doubled': ['russian orthodox'],
    'flory': ['patonce'],
    'other cross': ['of saint brigid', 'canterbury'],
    }

DEFAULT_CHARGE = Charge('?', '?')

#SYMBOLS = {'elder futhark'}

ALIASES = {}
MULTI = {
    'annulet of ivy': ['annulet', 'plant, vine'],
    'bow and arrow': ['bow', 'arrow'],
    'elm hurst': ['tree, multiple', 'tree, rounded shape'],
    'holly sprig': ['holly', 'sprig'],
    'triskelion of legs': ['triskelion', 'leg, human*3'],
    'triskelion of armored legs': ['triskelion', 'leg, human*3'],
    'wreath of thorns': ['wreath', 'thorn'],
}
ALSOS = {'flower, few petals'}
CATEGORIES = {}

EXPLICIT_CATEGORIES = {'human figure': 'human'}

IMPLIED_NUMBER = {
    'flames': 1,
    'flaunches': 2,
    }
IMPLIED_TINCTURES = {'bezant': 'or',
                     'plate': 'argent',
                     'hurt': 'azure',
                     'torteau': 'gules',
                     'pellet': 'sable',
                     'pomme': 'vert',
                     'golpe': 'purpure'}

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

CHARGE_ADJ = {'winged': 'monster, winged'}

DETAIL_ADJ = {
    'empty',
    'bottom-whorl',
    'elder futhark',
    'brunette',
    'caucasian',
    }

BLACKLIST = {'throughout'}

# These we want to treat as words for purposes of spellchecking, but we only
# understand them in certain manually-coded contexts.
MISC_WORDS = {'of', 'on', 'to', 'her', 'his', 'its', 'at', 'with'}

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

    with codecs.open(os.path.join(os.path.dirname(__file__), 'aliases.txt'),
              encoding='utf-8') as fil:
        for l in fil:
            if l.strip() and not l.startswith('#'):
                k, v = l.strip().split(': ')
                if k in ALIASES:
                    ALIASES[k].append(v)
                else:
                    ALIASES[k] = [v]

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

                assert desc not in DESC_TO_CHARGE, desc
                DESC_TO_CHARGE[desc] = charge
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
        for a in MULTI[w][1:]:
            if '*' in a:
                a, multiplier = a.split('*')
                charge = copy.deepcopy(CHARGES[a])
                charge.multiplier = int(multiplier)
            else:
                charge = CHARGES[a]
            CHARGES[w].seealso.append(charge)

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

    ALL_WORDS.update(CHARGES, DETAILS, ARRANGEMENTS, ORIENTATIONS, POSTURES,
                     BIRD_POSTURES, NUMBERS, ANDS, SUSTAININGS, MAINTAININGS,
                     WITHINS, CROSS_FAMILIES,
                     CHARGED_WITHS, ATOPS,
                     DETAIL_ADJ, COUNTERCHANGEDS,
                     MISC_WORDS)

    LOADED = True
