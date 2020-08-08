#!/usr/bin/python

import unittest

from parse import parse

class TestCases(unittest.TestCase):
    
    def test_one(self):
        self.assertEquals(
            ['ARM:primary:1',
             'ARM:primary:argent',
             'ARM:primary:embowed',
             'HORN AND ATTIRES:1:or'], 
            list(parse(u"(Fieldless) An arm embowed argent sustaining a stag's attire Or.").describe()))
        self.assertEquals(
            ['CRAC:primary:1',
             'CRAC:primary:or',
             'CRAC:primary:plain cross',
             'FDL:1:sable'], 
            list(parse(u'(Fieldless) On a cross couped Or, a fleur-de-lys sable').describe()))
        self.assertEquals(
            ['AR', 
             'DOG:primary:1', 
             'DOG:primary:sable', 
             'DOG:primary:courant', 
             'ESCALLOP:3:gules'], 
            list(parse(u'Argent, a greyhound courant sable between three escallops gules.').describe()))
        self.assertEquals(
            ['AR',
             'SPINDLE:primary:1',
             'SPINDLE:primary:purpure',
             '?TOOL-SEWING AND WEAVING:1:purpure:primary',
             'CHIEF:1:purpure',
             'POLE-AXE:1:argent'], 
            list(parse(u'Argent, an empty bottom-whorl drop spindle and on a chief purpure a glaive argent.').describe()))
        self.assertEquals(
            ['AZ',
             'CRAC:primary:1',
             'CRAC:primary:or',
             'CRAC:primary:moline',
             'CHIEF:1:or',
             'BIRD:3:azure:volant to dexter',
             '?BIRD9DEMI:3:azure:volant to dexter'], 
            list(parse(u'Azure, a cross moline and on a chief Or three martlets volant azure').describe()))
        self.assertEquals(
            ['OR',
             'FIELD TREATMENT-SEME (CRUSILLY):sable',
             '?CRAC:sable',
             'CROSS:primary:1',
             'CROSS:primary:gules',
             'BIRD:1:or:eagle:displayed',
             '?BIRD9DEMI:1:or:eagle:displayed'], 
            list(parse(u'Or, crusilly sable, on a cross throughout gules, an eagle displayed Or.\n\n').describe()))
        self.assertEquals(
            ['OR',
             'ARROW:primary:2',
             'ARROW:primary:vert',
             'INSA:2:vert:primary',
             'JEWELS AND JEWELRY:1:gules',
             '?CROWN:1:gules'], 
            list(parse(u'Or, two arrows in saltire vert within a rosary gules.\n').describe()))
        self.assertEquals(
            ['PB:purpure:~and sable',
             'HEADDOG:primary:1',
             'HEADDOG:primary:argent',
             'FLOWER-IRIS AND ORCHID:primary:1',
             'FLOWER-IRIS AND ORCHID:primary:argent',
             'FLOWER-IRIS AND ORCHID:primary:bendwise'], 
            list(parse(u"Per bend purpure and sable, a wolf's head erased and an iris bendwise slipped and leaved argent").describe()))
        self.assertEquals(
            ['PCI:sable:~and purpure',
             'CASTLE:primary:1',
             'CASTLE:primary:or',
             '?BEACON AND BRAZIER:1:or:primary',
             'INPALE:or',
             'LW:primary:1',
             'LW:primary:or'], 
            list(parse(u'Per chevron inverted sable and purpure, in pale a lighthouse and a laurel wreath Or\n').describe()))
        self.assertEquals(
            ['PU',
             'CASTLE:primary:1',
             'CASTLE:primary:or',
             '?BEACON AND BRAZIER:1:or:primary'], 
            list(parse(u'Purpure, a lighthouse Or').describe()))
        self.assertEquals(
            ['PU',
             'HEADDOG:primary:1',
             'HEADDOG:primary:argent',
             'FLOWER-IRIS AND ORCHID:1:argent:maintained'], 
            list(parse(u"Purpure, a wolf's head erased maintaining an iris slipped and leaved argent").describe()))
        self.assertEquals(
            ['MONSTER-SPHINX:primary:1',
             'MONSTER-SPHINX:primary:or',
             'MONSTER-SPHINX:primary:couchant'], 
            list(parse(u'(Fieldless) An Egyptian sphinx couchant Or.').describe()))
        self.assertEquals(
            ['AZ',
             'BEAST-BEAR:primary:1',
             'BEAST-BEAR:primary:or',
             'BEAST-BEAR:primary:rampant',
             'KNOT AND ROPE:3:or'], 
            list(parse(u'Azure, a bear rampant and in chief three quatrefoil knots Or.').describe()))
        self.assertEquals(
            ['AZ',
             'DOG:primary:1',
             'DOG:primary:argent',
             'DOG:primary:sejant',
             'CHIEF:1:argent',
             'LETTERS,RUNES AND SYMBOLS:azure'], 
            list(parse(u'Azure, a wolf sejant erect and on a chief argent the Elder Futhark runes laguz, dagaz, jera, ansuz, laguz, teiwaz, and jera azure.').describe()))
        self.assertEquals(
            ['FIELD DIV.-BARRY:or:~and azure',
             'CHIEF:1:gules:indented',
             'CAT:3:or'], 
            list(parse(u'Barry Or and azure, on a chief indented gules three lions queue-forchy Or.').describe()))
        self.assertEquals(
            ['ER',
             'PEN:primary:1',
             'PEN:primary:purpure',
             'PEN:primary:bendwise sinister'], 
            list(parse(u'Ermine, a quill pen bendwise sinister purpure.\n').describe()))
        self.assertEquals(
            ['GU',
             'FDL:primary:3',
             'FDL:primary:or',
             'ARRANGEMENT-IN BEND:or',
             'BORDURE:1:or:embattled'], 
            list(parse(u'Gules, in bend three fleurs-de-lis within a bordure embattled Or.\n').describe()))
        self.assertEquals(
            ['GYRONNY:argent:~and gules',
             'CUP:primary:1',
             'CUP:primary:purpure',
             'BEAST-WEASEL AND OTTER:1:sable',
             'BEAST9DEMI:1:sable'], 
            list(parse(u'Gyronny argent and gules, issuant from a mug purpure a demi-weasel sable.\n\n').describe()))
        self.assertEquals(
            ['PB:azure:~and argent', 
             'ROSE:primary:1', 
             'ROSE:primary:argent', 
             'DOG:primary:1', 
             'DOG:primary:courant', 
             'DOG:primary:bendwise', 
             'CHIEF:1:argent', 
             'BIRD:3:sable', 
             '?BIRD9DEMI:3:sable'], 
            list(parse(u'Per bend azure and argent, a rose argent and a fox courant bendwise proper, on a chief argent three martlets sable').describe()))
        self.assertEquals(
            ['FIELD TREATMENT-VAIRY',
             'PALL*7:primary:1',
             'PALL*7:primary:gules'], 
            list(parse(u'Vair, a pall inverted gules\n').describe()))
        self.assertEquals(
            ['VT',
             'ARROW:primary:2',
             'ARROW:primary:or',
             'INSA:2:or:primary',
             'CHIEF:1:or',
             'LEAF:3:vert'], 
            list(parse(u'Vert, two arrows in saltire and on a chief Or, three poplar leaves vert.\n\n').describe()))
        self.assertEquals(
            ['BIRD:primary:1',
             'BIRD:primary:multicolor',
             'BIRD:primary:volant to dexter',
             '?BIRD9DEMI:1:multicolor:primary:volant to dexter'],
            list(parse(u'(Fieldless) A swallow volant per fess azure and argent\n\n').describe()))
        self.assertEquals(
            ['AR',
             'FESS:primary:2',
             'FESS:primary:azure',
             'FESS:primary:wavy',
             'ROUNDEL:1:sable',
             'CRESCENT:2:sable'],
            list(parse(u'Argent, two bars wavy azure and in chief a roundel between an increscent and a decrescent sable\n\n').describe()))

        self.assertEquals(
            ['HEART:primary:1',
             'HEART:primary:gules',
             '?LEAF:1:gules:primary', 
             'WINGED OBJECT'],
            list(parse(u'(Fieldless) A heart gules winged argent\n\n').describe()))

        self.assertEquals(
            ['VT',
             'BEAST-BULL AND BISON:primary:1',
             'BEAST-BULL AND BISON:primary:argent',
             'BEAST-BULL AND BISON:primary:courant',
             'MONSTER9WINGED:argent:courant',
             'BASE:1:or'],
            list(parse(u'Vert, a winged bull courant wings elevated and addorsed argent and a base Or').describe()))

        self.assertEquals(
            ['STAR:primary:1',
             'STAR:primary:argent',
             'STAR:primary:of 5',
             'STAR:primary:estoile'],
            list(parse(u'(Fieldless) An estoile of five rays argent\n\n').describe()))

        self.assertEquals(
            [u'PB:sable:~and argent',
             'BEND:primary:1',
             'BEND:primary:azure',
             '?FIELD DIV.-BENDY:1:azure:primary',
             'CRAMPET:3:argent',
             'MONSTER-PHOENIX:2:multicolor'],
            list(parse(u'Per bend sable and argent, on a bend azure between two phoenixes counterchanged, three crampets argent').describe()))

        self.assertEquals(
            ['AR',
             'BEAST-MOUSE AND RAT:primary:1',
             'BEAST-MOUSE AND RAT:primary:passant',
             'BORDURE:1:purpure'],
            list(parse(u'Argent, a brown mouse passant proper and a bordure purpure\n').describe()))
        
        self.assertEquals(
            [u'QLY:sable:~and multicolor',
             'FIELD TREATMENT-VAIRY',
             'CASTLE:primary:3',
             'CASTLE:primary:or',
             'CASTLE:primary:palewise',
             'ARRANGEMENT-IN BEND:or'],
            list(parse(u'Quarterly sable and vairy sable, argent, gules and Or, in bend three towers palewise Or\n\n').describe()))

        self.assertEquals(
            ['OR',
             'BEND:primary:1',
             'BEND:primary:azure',
             'BEND:primary:cotised',
             '?FIELD DIV.-BENDY:1:azure:primary:cotised',
             'FDL:1:or:palewise',
             'ROSE:2:or',
             'CHIEF:1:gules',
             'CAT:1:or:passant'],
            list(parse(u'Or, on a bend cotised azure a fleur-de-lys palewise between two cinquefoils Or and on a chief gules a lion passant guardant Or\n\n').describe()))

        self.assertEquals(
            ['AZ',
             'PLANT-WHEAT:seme:or:seme on field',
             'FIELD TREATMENT-SEME (9OTHER):or',
             'PALE:primary:1',
             'PALE:primary:or',
             '?FIELD DIV.-PALY:1:or:primary',
             'SWORD:1:azure'],
            list(parse(u'Azure semy of ears of wheat, on a pale Or a sword azure').describe()))

        self.assertEquals(
            [u'PBS:sable:~and argent',
             'STAR:primary:1',
             'STAR:primary:or',
             'STAR:primary:mullet',
             '?CALTRAP:1:or:primary',
             'HAMMER:primary:2',
             '?HAMMER:2:primary',
             'INSA:2:primary'],
            list(parse(u"Per bend sinister sable and argent, a spur rowel Or and two smith's hammers in saltire proper.").describe()))

        self.assertEquals(
            ['AR',
             'MONSTER-PHOENIX:primary:1',
             'MONSTER-PHOENIX:primary:gules',
             'FIRE AND FLAME:1',
             'BORDURE:1:gules',
             'ROUNDEL:seme:or'],
            list(parse(u'Argent, a phoenix gules rising from flames proper and a bordure gules semy of bezants').describe()))

        self.assertEquals(
            ['VT',
             'CAULDRON AND COOKING POT:primary:1',
             'CAULDRON AND COOKING POT:primary:or',
             'FIRE AND FLAME:1:or',
             'CHIEF:1:or',
             'FORK AND SPOON:2:vert',
             'INSA:2:vert'],
            list(parse(u'Vert, a cauldron issuant from a flame and on a chief Or two ladles in saltire vert\n\n').describe()))

        self.assertEquals(
            [u'QLY:sable:~and or',
             'BEND:primary:1',
             'BEND:primary:argent',
             '?FIELD DIV.-BENDY:1:argent:primary',
             'DOG:2:sable:rampant to sinister',
             'PAW PRINT:5:sable'],
            list(parse(u'Quarterly sable and Or, on a bend argent between two wolves rampant contourney five paw prints sable.\n\n').describe()))

        self.assertEquals(
            [u'PFESS:azure:~and or',
             'MONSTER-SEA LION:primary:1',
             'MACE AND MORNINGSTAR:1:maintained'],
            list(parse(u'Per fess azure and Or, a sea lion maintaining a spiked mace counterchanged\n\n').describe()))

        self.assertEquals(
            [u'PC:vert:~and argent',
             'FLOWER-TRUMPET SHAPE:primary:2',
             'REPTILE-TURTLE:primary:1',
             'REPTILE-TURTLE:primary:statant',
             'LOZENGE:1:or',
             '?MASCLE AND RUSTRE:1:or',
             '?FIELD DIV.-VETU:1:or',
             '?FIELD DIV.-LOZENGY OR FUSILY:1:or',
             'HARP:1:sable',
             'LEG AND FOOT-MONSTER:1:vert:fesswise',
             '?CLAW:1:vert:fesswise'],
            list(parse(u"Per chevron vert and argent, two lilies and a turtle statant counterchanged, and for augmentation in fess point on a lozenge Or, a harp sable sustained by a dragon's jamb fesswise vert.\n\n").describe()))

        self.assertEquals(
            [u'GYRONNY:sable:~and vert',
             'DRAGON:primary:1',
             'DRAGON:primary:argent',
             'DRAGON:primary:rampant',
             'SWORD:1:or:maintained'],
            list(parse(u'Gyronny of eight, sable and vert a wyvern rampant argent langued gules, maintaining in dexter claw a sword erect Or.').describe()))

        self.assertEquals(
            [u'PPALE:azure:~and or',
             'EYE:seme:argent:seme on field',
             'FIELD TREATMENT-SEME (9OTHER):argent',
             'HAND AND GAUNTLET:primary:1',
             'HAND AND GAUNTLET:primary:multicolor'],
            list(parse(u'Per pale azure semy of eyes argent orbed sable and Or, a sinister hand counter-changed.\n').describe()))

        self.assertEquals(
            ['OR',
             'STAR:primary:1',
             'STAR:primary:sable',
             'STAR:primary:of 9 or more',
             'STAR:primary:mullet',
             '?CALTRAP:1:sable:primary:of 9 or more',
             'BORDURE:1:sable'],
            list(parse(u'Or, a mullet of five greater and five lesser points within a bordure sable.\n\n').describe()))

        self.assertEquals(
            ['AR',
             'HAMMER:primary:1',
             'HAMMER:primary:sable',
             'CRESCENT:2:sable',
             'ARRANGEMENT-IN BEND:sable'],
            list(parse(u"Argent, a Thor's hammer between in bend two increscents sable.").describe()))

        self.assertEquals(
            [u'PBS:argent:~and gules',
             'HUMAN FIGURE:primary:1',
             '?HUMAN FIGURE:1:primary',
             'ROSE:primary:3',
             'ROSE:primary:argent'],
            list(parse(u'Per bend sinister argent and gules, a brunette Caucasian maiden proper vested azure and three roses argent.').describe()))

        self.assertEquals(
            ['OR',
             'TOOL9OTHER:primary:1',
             'TOOL9OTHER:primary:sable',
             'TOOL9OTHER:primary:bendwise sinister',
             '?ANVIL:1:sable:primary:bendwise sinister',
             'FOODSTUFF:3:or',
             'ARM:1:embowed',
             'CHIEF:1:gules:rayonny'],
            list(parse(u"Or, a baker's peel bendwise sinister sable charged with three loaves of bread Or sustained by an arm embowed issuant from sinister proper vested sable, a chief rayonny gules.").describe()))

        self.assertEquals(
            ['TOOL9OTHER:primary:1',
             'TOOL9OTHER:primary:sable',
             '?ANVIL:1:sable:primary',
             'INPALE:sable',
             'FOODSTUFF:3:argent',
             'GARB:1:sable'],
            list(parse(u"(Fieldless) In pale a baker's peel sable charged with three loaves of bread argent issuant palewise from a garb sable.").describe()))

        self.assertEquals(
            ['GU',
             'HEAD-BEAST,RAM AND GOAT:primary:2',
             'HEAD-BEAST,RAM AND GOAT:primary:argent',
             'HEAD-BEAST,RAM AND GOAT:primary:fesswise',
             'ARRANGEMENT-IN FESS:argent',
             'ARRANGEMENT9HEAD,RESPECTANT',
             'STAR:2:or:mullet',
             '?CALTRAP:2:or',
             '?STAR:2:or',
             'INPALE:or'],
            list(parse(u"Gules, in fess two lamb's heads fesswise respectant erased conjoined at the forehead argent between in pale two mullets Or.").describe()))

        self.assertEquals(
            [u'FIELD DIV.-VETU:ploye:argent:~and azure',
             'REPTILE-SNAKE:primary:2',
             'REPTILE-SNAKE:primary:sable',
             'ARRANGEMENT9BEAST&MONSTER,RESPECTANT'],
            list(parse(u'Argent v\xeatu ploy\xe9 azure, two serpents erect respectant entwined sable.').describe()))

        self.assertEquals(
            [u'PPALE:gules:~and or',
             'BELL:primary:2',
             'BELL:primary:argent',
             'INPALE:argent'],
            list(parse(u"Per pale gules and Or, in dexter in pale two hawk's bells argent.").describe()))

        self.assertEquals(
            [u'PC:azure:~and gules',
             'CHEVRON:primary:1',
             'CHEVRON:primary:or',
             'HEAD-MONSTER,DRAGON:1:argent'],
            list(parse(u"Per chevron azure and gules, a chevron Or and overall a dragon's head cabossed argent.").describe()))

        self.assertEquals(
            [u'PBS:nebuly:or:~and azure',
             'HARP:primary:2',
             'HARP:primary:multicolor'],
            list(parse(u'Per bend sinister nebuly Or and azure, two harps counterchanged.').describe()))

        self.assertEquals(
            [u'PPALE:purpure:~and argent',
             'CHEVRON:primary:1',
             'PAW PRINT:4',
             'CRAC:1:doubled'],
            list(parse(u'Per pale purpure and argent, on a chevron four pawprints and in base a Russian Orthodox cross, all counterchanged').describe()))

        self.assertEquals(
            [u'PPALE:argent:~and azure',
             'DOG:primary:2',
             'DOG:primary:multicolor',
             'COMBAT'],
            list(parse(u'Per pale argent and azure, two wolves combattant counterchanged sable and argent.').describe()))

        self.assertEquals(
            [u'PC:or:~and vert',
             'ROUNDEL:primary:2',
             'ROUNDEL:primary:vert',
             'TRISKELION:2:or',
             '?LEG AND FOOT-HUMAN:6:or',
             'SEAWOLF:primary:1',
             'SEAWOLF:primary:argent',
             'SEAWOLF:primary:naiant to dexter',
             'MONSTER9WINGED:argent:naiant to dexter'],
            list(parse(u'Per chevron Or and vert, two pommes each charged with a triskelion of armored legs Or and a winged sea-fox naiant argent.').describe()))

        self.assertEquals(
            [u'PPALE:argent:~and sable',
             'ROUNDEL:primary:4',
             'ROUNDEL:primary:multicolor',
             'CHIEF:1:vert:engrailed',
             'BELL:3:argent'],
            list(parse(u"Per pale argent and sable, four\n  roundels counterchanged two and two and on a chief engrailed vert\n  three hawk's bells argent.\n").describe()))

        self.assertEquals(
            [u'PFESS:azure:~and multicolor',
             'FESS:primary:1',
             'FESS:primary:argent',
             '?FIELD DIV.-BARRY:1:argent:primary',
             'DICE:2:azure'],
            list(parse(u'Per fess azure and checky argent and\n  azure, on a fess argent two dice azure marked argent.').describe()))

        self.assertEquals(
            [u'PB:multicolor:~and argent',
             'BEND:primary:1',
             'BEND:primary:vert',
             '?FIELD DIV.-BENDY:1:vert:primary',
             'FEATHER AND QUILL:1:sable:bendwise',
             '?PEN:1:sable:bendwise',
             '?FIELD TREATMENT-PLUMMETTY:1:sable:bendwise'],
            list(parse(u'Per bend lozengy argent and sable and\n  argent, a bend vert and in base a feather bendwise sable.').describe()))

        self.assertEquals(
            [u'FIELD DIV.-LOZENGY OR FUSILY:argent:~and gules',
             'CRAC:primary:1',
             'CRAC:primary:sable',
             'CRAC:primary:other cross',
             'CHIEF:1:sable',
             'FIRE AND FLAME:2:argent'],
            list(parse(u'Lozengy argent and gules, a cross of Saint Brigid and on a chief sable two flames argent.').describe()))

        self.assertEquals(
            ['CRAC:primary:1',
             'CRAC:primary:argent',
             'CRAC:primary:other cross',
             'ERMINE SPOT:4:sable',
             '?FIELD TREATMENT-SEME (ERMINED):4:sable'],
            list(parse(u'(Fieldless) A cross of Canterbury argent each arm charged with an ermine spot head to center sable.\n').describe()))

        self.assertEquals(
            ['SA',
             'ROUNDEL:seme:argent:seme on field',
             'ARRANGEMENT-IN ORLE:argent',
             'FIELD TREATMENT-SEME (9OTHER):argent',
             'HEADDOG:primary:1',
             'HEADDOG:primary:argent'],
            list(parse(u"Sable, a wolf's head erased contourny within an orle of roundels argent.").describe()))

        self.assertEquals(
            ['FISH8OTHER:primary:1',
             'FISH8OTHER:primary:argent',
             'FISH8OTHER:primary:naiant to dexter',
             'FISH8OTHER:primary:embowed',
             'MONSTER9WINGED:argent:naiant to dexter',
             'ARRANGEMENT-IN ANNULO:1:argent:primary:naiant to dexter:embowed',
             'HORN AND ATTIRES:1:argent:maintained'],
            list(parse(u"(Fieldless) A bat-winged fish attired of a stag's antlers naiant embowed in annulo argent.").describe()))

        self.assertEquals(
            ['PPALE:fur:~and fur',
             'FIELD TREATMENT-SEME (ERMINED):multicolor',
             'BIRD:primary:2',
             'BIRD:primary:multicolor',
             'BIRD:primary:owl',
             '?BIRD9DEMI:2:multicolor:owl:primary',
             'ARRANGEMENT9BEAST&MONSTER,RESPECTANT'],
            list(parse(u'Per pale azure ermined argent and argent ermined azure, two owls respectant counterchanged argent and azure.').describe()))

        self.assertEquals(
            ['AR',
             u'CROSS:primary:1',
             u'CROSS:primary:azure',
             u'CROSS:primary:complex line',
             'KNOT AND ROPE:1:or'],
            list(parse(u'Argent, on a cross nowy azure a trefoil knot Or.').describe()))

        self.assertEquals(
            ['CRAC:primary:1',
             'CRAC:primary:purpure',
             'ROUNDEL:primary:5',
             'ROUNDEL:primary:purpure'],
            list(parse(u'(Fieldless) A cross of five golpes.').describe()))

        self.assertEquals(
            ['GU',
             'ARROW:primary:1',
             'ARROW:primary:argent',
             'HEAD-BIRD:2:argent',
             'ARRANGEMENT9HEAD,RESPECTANT'],
            list(parse(u"Gules, an arrow inverted between two bird's heads couped respectant argent.").describe()))

        self.assertEquals(
            ['QLY:azure:~and gules',
             'BIRD:primary:1',
             'BIRD:primary:argent',
             'BIRD:primary:owl',
             '?BIRD9DEMI:1:argent:owl:primary',
             'WREATH,OTHER:1:argent',
             '?FLOWER-MULTI-PETALED:seme:argent'],
            list(parse(u'Quarterly azure and gules, an owl within a wreath of daisies argent.').describe()))

        self.assertEquals(
            ['SA',
             'ROUNDEL:primary:1',
             'ROUNDEL:primary:argent',
             'CRAC:1:azure:formy',
             'BORDURE:1:multicolor'],
            list(parse(u'Sable, on a plate a Latin cross formy azure, a bordure parted bordurewise indented azure and argent.').describe()))

        self.assertEquals(
            ['AR',
             'AMPHIBIAN-FROG:primary:1',
             'AMPHIBIAN-FROG:primary:vert',
             'AMPHIBIAN-FROG:primary:affronte',
             'HEART:1:gules',
             '?LEAF:1:gules',
             'ARRANGEMENT-IN ANNULO:1:sable',
             'LETTERS,RUNES AND SYMBOLS:sable'],
            list(parse(u'Argent, a toad sejant affronty vert, spotted and crowned Or, charged with a heart gules fimbriated Or within in annulo the inscription "Before you meet the handsome prince you have to kiss a lot of toads" sable.').describe()))

        self.assertEquals(
            ['BEAST-BOAR:primary:1',
             'BEAST-BOAR:primary:or',
             'BEAST-BOAR:primary:passant',
             'JEWELS AND JEWELRY:1:gules'],
            list(parse(u'(Fieldless) A boar passant Or charged on the shoulder with a hexagonal gemstone gules.').describe()))

        self.assertEquals(
            ['PC:argent:~and sable',
             'TREE9BRANCH:primary:4',
             'TREE9BRANCH:primary:vert',
             'INSA:4:vert:primary',
             'SWORD:primary:1',
             'SWORD:primary:argent'],
            list(parse(u'Per chevron throughout argent and sable, between two pairs of branches in saltire vert, a sword inverted argent.').describe()))

        self.assertEquals(
            ['PC:azure:~and argent',
             'FDL:primary:2',
             'INSECT-BUTTERFLY AND MOTH:primary:1',
             'BORDURE:1:multicolor',
             'GOUTE:seme:multicolor'],
            list(parse(u'Per chevron azure and argent, two fleurs-de-lys and a butterfly counterchanged, a bordure goutty all counterchanged argent and gules.').describe()))

        self.assertEquals(
            ['PB:or:~and sable',
             'GOUTE:primary:1',
             'GOUTE:primary:multicolor'],
            list(parse(u'Per bend Or and sable, a goutte counterchanged.').describe()))

        self.assertEquals(
            ['GU',
             'CALIPER AND COMPASS:primary:1',
             'CALIPER AND COMPASS:primary:argent',
             '?TOOL9OTHER:1:argent:primary',
             'CRESCENT:3:argent',
             'STAR:3:sable:of 6:mullet',
             '?CALTRAP:3:sable:of 6',
             '?STAR:3:sable:of 6'],
            list(parse(u'Gules, a pair of calipers and in chief three crescents argent each crescent charged with a mullet of six points sable.').describe()))

        self.assertEquals(
            ['FIELD DIV.-PER PALL',
             'TRISKELION:primary:3',
             'TRISKELION:primary:multicolor'],
            list(parse(u'Per pall vert, Or, and argent, three triskeles argent, purpure, and azure.\n').describe()))

        self.assertEquals(
            ['OR',
             'BIRD:primary:1',
             'BIRD:primary:sable',
             '?BIRD9DEMI:1:sable:primary',
             'BASE:1:vert:enarched',
             'BORDURE:1:sable:nebuly'],
            list(parse(u'Or, a hen sable and a mount vert, a bordure nebuly sable.').describe()))

        self.assertEquals(
            ['GATE AND DOOR:primary:1',
             'GATE AND DOOR:primary:multicolor',
             'HEAD-BEAST,CAT AND LION:1:multicolor'],
            list(parse(u"(Fieldless) On a chainless portcullis per pale argent and sable a lion's head cabossed counterchanged.").describe()))

        self.assertEquals(
            ['SA',
             'EYE:primary:1',
             'EYE:primary:or',
             'ARROW:1:or:bendwise sinister',
             'CHIEF:1:or',
             'ANNULET:6:sable',
             '?TORSE:6:sable',
             'ROUNDEL:3:sable'],
            list(parse(u'Sable, an eye Or, irised sable, transfixed by an arrow bendwise sinister and on a chief Or within each of three sets of two concentric annulets, a roundel sable.').describe()))

        self.assertEquals(
            ['PPALE:gules:~and sable',
             'BIRD:primary:1',
             'BIRD:primary:argent',
             'BIRD:primary:raven',
             'BIRD:primary:displayed',
             '?BIRD9DEMI:1:argent:raven:primary:displayed',
             'ROUNDEL:2:argent',
             'INPALE:argent',
             'TRISKELION:2'],
            list(parse(u'Per pale gules and sable, a raven displayed argent between in pale two plates charged with triskelions of spirals.').describe()))

        self.assertEquals(
            ['AZ',
             'REPTILE-SNAKE:primary:3',
             'REPTILE-SNAKE:primary:or',
             'KNOT AND ROPE:primary:1',
             'KNOT AND ROPE:primary:or'],
            list(parse(u'Azure, three snakes nowed in a trefoil knot Or.').describe()))

        self.assertEquals(
            ['PBS:purpure:~and vert',
             'BS:primary:1',
             'BS:primary:or',
             '?FIELD DIV.-BENDY*3:1:or:primary',
             'HEAD-MONSTER,UNICORN:1:argent',
             'STAR:3:or:mullet',
             '?CALTRAP:3:or',
             '?STAR:3:or'],
            list(parse(u"Per bend sinister purpure and vert, a bend sinister Or between a unicorn's head erased argent and 3 mullets Or").describe()))

        self.assertEquals(
            ['VT',
             'FESS:primary:1',
             'FESS:primary:multicolor',
             '?FIELD DIV.-BARRY:1:multicolor:primary',
             'FLEAM:1',
             'CHESS PIECE:1'],
            list(parse(u'Vert, on a fess per pale azure and Or, a fleam and a chessrook counterchanged.').describe()))

        self.assertEquals(
            ['VT',
             'BEAST-DEER AND STAG:primary:1',
             'BEAST-DEER AND STAG:primary:or',
             'BEAST-DEER AND STAG:primary:passant to sinister',
             'BEAST9DEMI:1:or:passant to sinister'],
            list(parse(u'Vert, a demi-stag passant to sinister reguardant Or.\n').describe()))

        self.assertEquals(
            ['AZ',
             'FLOWER-CUP SHAPE:primary:1',
             'FLOWER-CUP SHAPE:primary:argent',
             'STAR:5:argent',
             'ARRANGEMENT-IN CHEVRON:5:argent',
             'ORLE AND TRESSURE:1:argent'],
            list(parse(u'Azure, a lotus blossom in profile beneath five compass stars in chevron, an orle argent.').describe()))

        self.assertEquals(
            ['AR',
             'FESS:primary:1',
             'FESS:primary:sable',
             '?FIELD DIV.-BARRY:1:sable:primary',
             'CRESCENT:3:gules',
             'MONSTER-ENFIELD:1:gules'],
            list(parse(u'Argent, surmounting a fess sable between three crescents an enfield gules.').describe()))

        self.assertEquals(
            ['VT',
             'TRISKELION:primary:1',
             'TRISKELION:primary:or',
             'HEADDOG:primary:3',
             'HEADDOG:primary:or'],
            list(parse(u"Vert, a triskelion of wolves' heads Or.\n").describe()))

        self.assertEquals(
            ['AZ',
             'LETTERS,RUNES AND SYMBOLS:seme:argent:seme on field',
             'FIELD TREATMENT-SEME (9OTHER):argent',
             'BEAST-RABBIT:primary:1',
             'BEAST-RABBIT:primary:argent',
             'BEAST-RABBIT:primary:rampant',
             'HOURGLASS:1:argent:maintained'],
            list(parse(u'Azure semy of Greek letters pi, a rabbit rampant maintaining an hourglass argent.\n').describe()))

        self.assertEquals(
            ['FIELD DIV.-PER PALL',
             'BEAST-HORSE:seme:or:seme on field:passant',
             'FIELD TREATMENT-SEME (9OTHER):or'],
            list(parse(u'Per pall gules, azure and vert, semy of horses passant Or').describe()))

        self.assertEquals(
            ['SA',
             'FIRE AND FLAME:primary:1',
             '?FIRE AND FLAME:1:primary',
             'REPTILE-SNAKE:1:argent',
             'ARRANGEMENT-IN ANNULO:1:argent',
             'STAR:1:argent:of 8:mullet',
             '?CALTRAP:1:argent:of 8',
             '?STAR:1:argent:of 8',
             'BORDURE:1:argent'],
            list(parse(u'Sable, on a flame proper a serpent in annulo with head to base argent surrounding a mullet of eight points pierced argent within a bordure argent').describe()))

        self.assertEquals(
            ['GU',
             'HEAD-BEAST,RABBIT:primary:1',
             'HEAD-BEAST,RABBIT:primary:argent',
             'HEAD-JESSANT-DE-LYS:primary:or',
             '?HEAD-JESSANT-DE-LYS:primary'],
            list(parse(u"Gules, a rabbit's head argent jessant-de-lys Or.\n\n").describe()))
        
        self.assertEquals(
            ['OR',
             'LW:primary:1',
             'LW:primary:vert'],
            list(parse(u'Or, a Laurel wreath vert.\n').describe()))
        
        self.assertEquals(
            ['AR',
             'FESS:primary:1',
             'FESS:primary:gules',
             '?FIELD DIV.-BARRY:1:gules:primary',
             'BEAST-HORSE:3:gules:rampant'],
            list(parse(u'Argent, a fess and three stallions rampant gules.').describe()))

        self.assertEquals(
            ['AR',
             'CAT:seme:vert:seme on field',
             'FIELD TREATMENT-SEME (9OTHER):vert'],
            list(parse(u'Argent, seme of lions vert.\n').describe()))

        self.assertEquals(
            ['FIELD DIV.-CHECKY:or:~and sable',
             'FIELD DIV.-BENDY:or:~and sable'],
            list(parse(u'Checky and bendy Or and sable.').describe()))

        self.assertEquals(
            ['FIELD DIV.-CHECKY:or:~and sable',
             'FIELD DIV.-BENDY:or:~and sable'],
            list(parse(u'Checky of nine and bendy Or and sable.').describe()))

        self.assertEquals(
            ['FIELD DIV.-CHECKY:multicolor:~and vert'],
            list(parse(u'Checky bendy Or and sable and vert.').describe()))

        self.assertEquals(
            ['OR', 'WELL:primary:1', 'WELL:primary:vert',
             '?ARCHITECTURE:1:vert:primary'],
            list(parse(u'Or, a well vert.').describe()))

        self.assertEquals(
            ['OR',
             'STAR:primary:1',
             'STAR:primary:vert',
             'STAR:primary:sun'],
            list(parse(u'Or, a sun vert.').describe()))
        self.assertEquals(
            ['OR',
             'STAR:primary:1',
             'STAR:primary:vert',
             'STAR:primary:estoile'],
            list(parse(u'Or, an estoile vert.').describe()))
        self.assertEquals(
            ['OR',
             'STAR:primary:1',
             'STAR:primary:vert',
             'STAR:primary:mullet',
             '?CALTRAP:1:vert:primary'],
            list(parse(u'Or, a mullet vert.').describe()))
        self.assertEquals(
            ['FIELD TREATMENT-POTENTY:argent:~and sable',
             'PALL:primary:1',
             'PALL:primary:gules'],
            list(parse(u'Potenty argent and sable, a pall gules').describe()))

        self.assertEquals(
            ['VT',
             'CHEVRON*7:primary:1',
             'CHEVRON*7:primary:azure',
             'SPINDLE:2:argent',
             '?TOOL-SEWING AND WEAVING:2:argent',
             'ROUNDEL-DEMI:3:argent'],
            list(parse(u'Vert, on a chevron inverted azure fimbriated Or two drop spindles and in base three demi-roundel two and one argent').describe()))

if __name__ == "__main__":
    unittest.main()
