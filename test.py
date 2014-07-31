#!/usr/bin/python

import unittest

from parse import parse

class TestCases(unittest.TestCase):
    
    def test_one(self):
        self.assertEquals(
            ['ARM:1:argent:primary:embowed', 'ARM:1:primary:embowed', 'HORN AND ATTIRES:1:or'], 
            list(parse(u"(Fieldless) An arm embowed argent sustaining a stag's attire Or.").describe()))
        self.assertEquals(
            ['CRAC:1:or:plain cross:primary',
             'CRAC:1:plain cross:primary',
             'FDL:1:sable'], 
            list(parse(u'(Fieldless) On a cross couped Or, a fleur-de-lys sable').describe()))
        self.assertEquals(
            ['AR', 'DOG:1:sable:primary:passant', 'DOG:1:primary:passant', 'ESCALLOP:3:gules'], 
            list(parse(u'Argent, a greyhound courant sable between three escallops gules.').describe()))
        self.assertEquals(
            ['AR', 'SPINDLE:1:purpure:primary', 'TOOL-SEWING AND WEAVING:1:purpure:primary', 'SPINDLE:1:primary', 'CHIEF:1:purpure', 'POLE-AXE:1:argent'], 
            list(parse(u'Argent, an empty bottom-whorl drop spindle and on a chief purpure a glaive argent.').describe()))
        self.assertEquals(
            ['AZ',
             'CRAC:1:or:moline:primary',
             'CRAC:1:moline:primary',
             'CHIEF:1:or',
             'BIRD:3:azure:volant to dexter',
             'BIRD9DEMI:3:azure:volant to dexter'], 
            list(parse(u'Azure, a cross moline and on a chief Or three martlets volant azure').describe()))
        self.assertEquals(
            ['OR', 'FIELD TREATMENT-SEME (CRUSILLY):sable', 'CRAC:sable', 'CROSS:1:gules:primary', 'CROSS:1:primary', 'BIRD:1:or:displayed:eagle', 'BIRD9DEMI:1:or:displayed:eagle'], 
            list(parse(u'Or, crusilly sable, on a cross throughout gules, an eagle displayed Or.\n\n').describe()))
        self.assertEquals(
            ['OR', 'ARROW:2:vert:primary', 'ARROW:2:primary', 'INSA:2:vert:primary', 'JEWELS AND JEWELRY:1:gules', 'CROWN:1:gules'], 
            list(parse(u'Or, two arrows in saltire vert within a rosary gules.\n').describe()))
        self.assertEquals(
            ['PB:purpure:~and sable', 'HEADDOG:1:argent:primary', 'HEADDOG:1:primary', 'FLOWER-IRIS AND ORCHID:1:argent:primary:bendwise', 'FLOWER-IRIS AND ORCHID:1:primary:bendwise'], 
            list(parse(u"Per bend purpure and sable, a wolf's head erased and an iris bendwise slipped and leaved argent").describe()))
        self.assertEquals(
            ['PCI:sable:~and purpure', 'CASTLE:1:or:primary', 'BEACON AND BRAZIER:1:or:primary', 'CASTLE:1:primary', 'INPALE:or', 'LW:1:or:primary', 'LW:1:primary'], 
            list(parse(u'Per chevron inverted sable and purpure, in pale a lighthouse and a laurel wreath Or\n').describe()))
        self.assertEquals(
            ['PU', 'CASTLE:1:or:primary', 'BEACON AND BRAZIER:1:or:primary', 'CASTLE:1:primary'], 
            list(parse(u'Purpure, a lighthouse Or').describe()))
        self.assertEquals(
            ['PU', 'HEADDOG:1:argent:primary', 'HEADDOG:1:primary'], 
            list(parse(u"Purpure, a wolf's head erased maintaining an iris slipped and leaved argent").describe()))
        self.assertEquals(
            ['MONSTER-SPHINX:1:or:primary:couchant', 'MONSTER-SPHINX:1:primary:couchant'], 
            list(parse(u'(Fieldless) An Egyptian sphinx couchant Or.').describe()))
        self.assertEquals(
            ['AZ', 'BEAST-BEAR:1:or:primary:rampant', 'BEAST-BEAR:1:primary:rampant', 'KNOT AND ROPE:3:or'], 
            list(parse(u'Azure, a bear rampant and in chief three quatrefoil knots Or.').describe()))
        self.assertEquals(
            ['AZ', 'DOG:1:argent:primary:sejant', 'DOG:1:primary:sejant', 'CHIEF:1:argent', 'LETTERS,RUNES AND SYMBOLS:azure'], 
            list(parse(u'Azure, a wolf sejant erect and on a chief argent the Elder Futhark runes laguz, dagaz, jera, ansuz, laguz, teiwaz, and jera azure.').describe()))
        self.assertEquals(
            ['FIELD DIV.-BARRY:or:~and azure', 'CHIEF:1:gules:indented', 'CAT:3:or'], 
            list(parse(u'Barry Or and azure, on a chief indented gules three lions queue-forchy Or.').describe()))
        self.assertEquals(
            ['ER',
             'PEN:1:purpure:primary:bendwise sinister',
             'PEN:1:primary:bendwise sinister'], 
            list(parse(u'Ermine, a quill pen bendwise sinister purpure.\n').describe()))
        self.assertEquals(
            ['GU', 'FDL:3:or:primary', 'FDL:3:primary', 'ARRANGEMENT-IN BEND:or', 'BORDURE:1:or:embattled'], 
            list(parse(u'Gules, in bend three fleurs-de-lis within a bordure embattled Or.\n').describe()))
        self.assertEquals(
            ['GYRONNY:argent:~and gules', 'CUP:1:purpure:primary', 'CUP:1:primary', 'BEAST-WEASEL AND OTTER:1:sable', 'BEAST9DEMI:1:sable'], 
            list(parse(u'Gyronny argent and gules, issuant from a mug purpure a demi-weasel sable.\n\n').describe()))
        self.assertEquals(
            ['PB:azure:~and argent', 'ROSE:1:argent:primary', 'ROSE:1:primary', 'DOG:1:proper:primary:passant:bendwise', 'DOG:1:primary:passant:bendwise', 'CHIEF:1:argent', 'BIRD:3:sable', 'BIRD9DEMI:3:sable'], 
            list(parse(u'Per bend azure and argent, a rose argent and a fox courant bendwise proper, on a chief argent three martlets sable').describe()))
        self.assertEquals(
            ['FIELD TREATMENT-VAIRY', 'PALL*7:1:gules:primary', 'PALL*7:1:primary'], 
            list(parse(u'Vair, a pall inverted gules\n').describe()))
        self.assertEquals(
            ['VT', 'ARROW:2:or:primary', 'ARROW:2:primary', 'INSA:2:or:primary', 'CHIEF:1:or', 'LEAF:3:vert'], 
            list(parse(u'Vert, two arrows in saltire and on a chief Or, three poplar leaves vert.\n\n').describe()))
        self.assertEquals(
            ['BIRD:1:multicolor:primary:volant to dexter', 'BIRD9DEMI:1:multicolor:primary:volant to dexter', 'BIRD:1:primary:volant to dexter'],
            list(parse(u'(Fieldless) A swallow volant per fess azure and argent\n\n').describe()))
        self.assertEquals(
            ['AR', 'FESS:2:azure:primary:wavy', 'FESS:2:primary:wavy', 'ROUNDEL:1:sable', 'CRESCENT:2:sable'],
            list(parse(u'Argent, two bars wavy azure and in chief a roundel between an increscent and a decrescent sable\n\n').describe()))

        self.assertEquals(
            ['HEART:1:gules:primary', 'LEAF:1:gules:primary', 
             'HEART:1:primary', 'WINGED OBJECT'],
            list(parse(u'(Fieldless) A heart gules winged argent\n\n').describe()))

        self.assertEquals(
            ['VT', 'BEAST-BULL AND BISON:1:argent:primary:passant', 'BEAST-BULL AND BISON:1:primary:passant', 'MONSTER9WINGED:argent', 'BASE:1:or'],
            list(parse(u'Vert, a winged bull courant wings elevated and addorsed argent and a base Or').describe()))

        self.assertEquals(
            ['ESTOILE:1:argent:primary:of 5', 'STAR:1:argent:primary:of 5', 'ESCARB:1:argent:primary:of 5', 'ESTOILE:1:primary:of 5'],
            list(parse(u'(Fieldless) An estoile of five rays argent\n\n').describe()))

        self.assertEquals(
            [u'PB:sable:~and argent', 'BEND:1:azure:primary', 'FIELD DIV.-BENDY:1:azure:primary', 'BEND:1:primary', 'CRAMPET:3:argent', 'MONSTER-PHOENIX:2'],
            list(parse(u'Per bend sable and argent, on a bend azure between two phoenixes counterchanged, three crampets argent').describe()))

        self.assertEquals(
            ['AR', 'BEAST-MOUSE AND RAT:1:proper:primary:passant', 'BEAST-MOUSE AND RAT:1:primary:passant', 'BORDURE:1:purpure'],
            list(parse(u'Argent, a brown mouse passant proper and a bordure purpure\n').describe()))
        
        self.assertEquals(
            [u'QLY:sable:~and multicolor', 'FIELD TREATMENT-VAIRY', 'CASTLE:3:or:primary:palewise', 'CASTLE:3:primary:palewise', 'ARRANGEMENT-IN BEND:or'],
            list(parse(u'Quarterly sable and vairy sable, argent, gules and Or, in bend three towers palewise Or\n\n').describe()))

        self.assertEquals(
            ['OR',
             'BEND:1:azure:primary:cotised',
             'FIELD DIV.-BENDY:1:azure:primary:cotised',
             'BEND:1:primary:cotised',
             'FDL:1:or:palewise',
             'FOIL-5:2:or',
             'ROSE:2:or',
             'CHIEF:1:gules',
             'CAT:1:or:passant'],
            list(parse(u'Or, on a bend cotised azure a fleur-de-lys palewise between two cinquefoils Or and on a chief gules a lion passant guardant Or\n\n').describe()))

        self.assertEquals(
            ['AZ', 'PLANT-WHEAT:seme:or:seme on field', 'FIELD TREATMENT-SEME (9OTHER):or', 'PALE:1:or:primary', 'FIELD DIV.-PALY:1:or:primary', 'PALE:1:primary', 'SWORD:1:azure'],
            list(parse(u'Azure semy of ears of wheat, on a pale Or a sword azure').describe()))

        self.assertEquals(
            [u'PBS:sable:~and argent',
             'STAR:1:or:primary',
             'CALTRAP:1:or:primary',
             'ESTOILE:1:or:primary',
             'SUN:1:or:primary',
             'STAR:1:primary',
             'HAMMER:2:proper:primary',
             'HAMMER:2:primary',
             'INSA:2:proper:primary'],
            list(parse(u"Per bend sinister sable and argent, a spur rowel Or and two smith's hammers in saltire proper.").describe()))

        self.assertEquals(
            ['AR', 'MONSTER-PHOENIX:1:gules:primary', 'MONSTER-PHOENIX:1:primary', 'FIRE AND FLAME:1:proper', 'BORDURE:1:gules', 'ROUNDEL:seme:or'],
            list(parse(u'Argent, a phoenix gules rising from flames proper and a bordure gules semy of bezants').describe()))

        self.assertEquals(
            ['VT', 'CAULDRON AND COOKING POT:1:or:primary', 'CAULDRON AND COOKING POT:1:primary', 'FIRE AND FLAME:1:or', 'CHIEF:1:or', 'FORK AND SPOON:2:vert', 'INSA:2:vert'],
            list(parse(u'Vert, a cauldron issuant from a flame and on a chief Or two ladles in saltire vert\n\n').describe()))

        self.assertEquals(
            [u'QLY:sable:~and or',
             'BEND:1:argent:primary',
             'FIELD DIV.-BENDY:1:argent:primary',
             'BEND:1:primary',
             'DOG:2:sable:rampant to sinister',
             'PAW PRINT:5:sable'],
            list(parse(u'Quarterly sable and Or, on a bend argent between two wolves rampant contourney five paw prints sable.\n\n').describe()))

        self.assertEquals(
            [u'PFESS:azure:~and or', 'MONSTER-SEA LION:1:multicolor:primary', 'MONSTER-SEA LION:1:primary'],
            list(parse(u'Per fess azure and Or, a sea lion maintaining a spiked mace counterchanged\n\n').describe()))

        self.assertEquals(
            [u'PC:vert:~and argent',
             'FLOWER-TRUMPET SHAPE:2:primary',
             'REPTILE-TURTLE:1:primary:statant',
             'LOZENGE:1:or',
             'MASCLE AND RUSTRE:1:or',
             'FIELD DIV.-VETU:1:or',
             'FIELD DIV.-LOZENGY OR FUSILY:1:or',
             'HARP:1:sable',
             'LEG AND FOOT-MONSTER:1:vert:fesswise',
             'CLAW:1:vert:fesswise'],
            list(parse(u"Per chevron vert and argent, two lilies and a turtle statant counterchanged, and for augmentation in fess point on a lozenge Or, a harp sable sustained by a dragon's jamb fesswise vert.\n\n").describe()))

        self.assertEquals(
            [u'GYRONNY:sable:~and vert',
             'DRAGON:1:argent:primary:rampant',
             'DRAGON:1:primary:rampant'],
            list(parse(u'Gyronny of eight, sable and vert a wyvern rampant argent langued gules, maintaining in dexter claw a sword erect Or.').describe()))

        self.assertEquals(
            [u'PPALE:azure:~and or',
             'EYE:seme:argent:seme on field',
             'FIELD TREATMENT-SEME (9OTHER):argent',
             'HAND AND GAUNTLET:1:multicolor:primary',
             'HAND AND GAUNTLET:1:primary'],
            list(parse(u'Per pale azure semy of eyes argent orbed sable and Or, a sinister hand counter-changed.\n').describe()))

        self.assertEquals(
            ['OR',
             'STAR:1:sable:primary:of 9 or more',
             'CALTRAP:1:sable:primary:of 9 or more',
             'ESTOILE:1:sable:primary:of 9 or more',
             'SUN:1:sable:primary:of 9 or more',
             'STAR:1:primary:of 9 or more',
             'BORDURE:1:sable'],
            list(parse(u'Or, a mullet of five greater and five lesser points within a bordure sable.\n\n').describe()))

        self.assertEquals(
            ['AR',
             'HAMMER:1:sable:primary',
             'HAMMER:1:primary',
             'CRESCENT:2:sable',
             'ARRANGEMENT-IN BEND:sable'],
            list(parse(u"Argent, a Thor's hammer between in bend two increscents sable.").describe()))

        self.assertEquals(
            [u'PBS:argent:~and gules',
             'HUMAN FIGURE:1:proper:primary',
             'HUMAN FIGURE:1:primary',
             'ROSE:3:argent:primary',
             'ROSE:3:primary'],
            list(parse(u'Per bend sinister argent and gules, a brunette Caucasian maiden proper vested azure and three roses argent.').describe()))

        self.assertEquals(
            ['OR',
             'TOOL9OTHER:1:sable:primary:bendwise sinister',
             'ANVIL:1:sable:primary:bendwise sinister',
             'TOOL9OTHER:1:primary:bendwise sinister',
             'FOODSTUFF:3:or',
             'ARM:1:proper:embowed',
             'CHIEF:1:gules:rayonny'],
            list(parse(u"Or, a baker's peel bendwise sinister sable charged with three loaves of bread Or sustained by an arm embowed issuant from sinister proper vested sable, a chief rayonny gules.").describe()))

        self.assertEquals(
            ['TOOL9OTHER:1:sable:primary',
             'ANVIL:1:sable:primary',
             'TOOL9OTHER:1:primary',
             'INPALE:sable',
             'FOODSTUFF:3:argent',
             'GARB:1:sable'],
            list(parse(u"(Fieldless) In pale a baker's peel sable charged with three loaves of bread argent issuant palewise from a garb sable.").describe()))

        self.assertEquals(
            ['GU',
             'HEAD-BEAST,RAM AND GOAT:2:argent:primary:fesswise',
             'HEAD-BEAST,RAM AND GOAT:2:primary:fesswise',
             'ARRANGEMENT-IN FESS:argent',
             'ARRANGEMENT9HEAD,RESPECTANT',
             'STAR:2:or',
             'CALTRAP:2:or',
             'ESTOILE:2:or',
             'SUN:2:or',
             'INPALE:or'],
            list(parse(u"Gules, in fess two lamb's heads fesswise respectant erased conjoined at the forehead argent between in pale two mullets Or.").describe()))

        self.assertEquals(
            [u'FIELD DIV.-VETU:ploye:argent:~and azure',
             'REPTILE-SNAKE:2:sable:primary',
             'REPTILE-SNAKE:2:primary',
             'ARRANGEMENT9BEAST&MONSTER,RESPECTANT'],
            list(parse(u'Argent v\xeatu ploy\xe9 azure, two serpents erect respectant entwined sable.').describe()))

        self.assertEquals(
            [u'PPALE:gules:~and or',
             'BELL:2:argent:primary',
             'BELL:2:primary',
             'INPALE:argent'],
            list(parse(u"Per pale gules and Or, in dexter in pale two hawk's bells argent.").describe()))

        self.assertEquals(
            [u'PC:azure:~and gules',
             'CHEVRON:1:or:primary',
             'CHEVRON:1:primary',
             'HEAD-MONSTER,DRAGON:1:argent'],
            list(parse(u"Per chevron azure and gules, a chevron Or and overall a dragon's head cabossed argent.").describe()))

        self.assertEquals(
            [u'PBS:nebuly:or:~and azure',
             'HARP:2:multicolor:primary',
             'HARP:2:primary'],
            list(parse(u'Per bend sinister nebuly Or and azure, two harps counterchanged.').describe()))

        self.assertEquals(
            [u'PPALE:purpure:~and argent',
             'CHEVRON:1:primary',
             'PAW PRINT:4',
             'CRAC:1:doubled'],
            list(parse(u'Per pale purpure and argent, on a chevron four pawprints and in base a Russian Orthodox cross, all counterchanged').describe()))

        self.assertEquals(
            [u'PPALE:argent:~and azure',
             'DOG:2:multicolor:primary',
             'DOG:2:primary',
             'COMBAT'],
            list(parse(u'Per pale argent and azure, two wolves combattant counterchanged sable and argent.').describe()))

        self.assertEquals(
            [u'PC:or:~and vert',
             'ROUNDEL:2:vert:primary',
             'ROUNDEL:2:primary',
             'TRISKELION:2:or',
             'LEG AND FOOT-HUMAN:6:or',
             'SEAWOLF:1:argent:primary:naiant to dexter',
             'SEAWOLF:1:primary:naiant to dexter',
             'MONSTER9WINGED:argent'],
            list(parse(u'Per chevron Or and vert, two pommes each charged with a triskelion of armored legs Or and a winged sea-fox naiant argent.').describe()))

        self.assertEquals(
            [u'PPALE:argent:~and sable',
             'ROUNDEL:4:multicolor:primary',
             'ROUNDEL:primary',
             'CHIEF:1:vert:engrailed',
             'BELL:3:argent'],
            list(parse(u"Per pale argent and sable, four\n  roundels counterchanged two and two and on a chief engrailed vert\n  three hawk's bells argent.\n").describe()))

        self.assertEquals(
            [u'PFESS:azure:~and multicolor',
             'FESS:1:argent:primary',
             'FIELD DIV.-BARRY:1:argent:primary',
             'FESS:1:primary',
             'DICE:2:azure'],
            list(parse(u'Per fess azure and checky argent and\n  azure, on a fess argent two dice azure marked argent.').describe()))

        self.assertEquals(
            [u'PB:multicolor:~and argent',
             'BEND:1:vert:primary',
             'FIELD DIV.-BENDY:1:vert:primary',
             'BEND:1:primary',
             'FEATHER AND QUILL:1:sable:bendwise',
             'PEN:1:sable:bendwise',
             'FIELD TREATMENT-PLUMMETTY:1:sable:bendwise'],
            list(parse(u'Per bend lozengy argent and sable and\n  argent, a bend vert and in base a feather bendwise sable.').describe()))

        self.assertEquals(
            [u'FIELD DIV.-LOZENGY OR FUSILY:argent:~and gules',
             'CRAC:1:sable:other cross:primary',
             'CRAC:1:other cross:primary',
             'CHIEF:1:sable',
             'FIRE AND FLAME:2:argent'],
            list(parse(u'Lozengy argent and gules, a cross of Saint Brigid and on a chief sable two flames argent.').describe()))

        self.assertEquals(
            ['CRAC:1:argent:other cross:primary',
             'CRAC:1:other cross:primary',
             'ERMINE SPOT:4:sable',
             'FIELD TREATMENT-SEME (ERMINED):4:sable'],
            list(parse(u'(Fieldless) A cross of Canterbury argent each arm charged with an ermine spot head to center sable.\n').describe()))

        self.assertEquals(
            ['SA',
             'ROUNDEL:seme:argent:seme on field',
             'ARRANGEMENT-IN ORLE:argent',
             'FIELD TREATMENT-SEME (9OTHER):argent',
             'HEADDOG:1:argent:primary',
             'HEADDOG:1:primary'],
            list(parse(u"Sable, a wolf's head erased contourny within an orle of roundels argent.").describe()))

        self.assertEquals(
            ['FISH8OTHER:1:argent:primary:naiant to dexter:embowed',
             'FISH8OTHER:1:primary:naiant to dexter:embowed',
             'MONSTER9WINGED:argent',
             'ARRANGEMENT-IN ANNULO:1:argent:primary:naiant to dexter:embowed'],
            list(parse(u"(Fieldless) A bat-winged fish attired of a stag's antlers naiant embowed in annulo argent.").describe()))

        self.assertEquals(
            ['PPALE:fur:~and fur',
             'FIELD TREATMENT-SEME (ERMINED):multicolor',
             'BIRD:2:multicolor:primary:owl',
             'BIRD9DEMI:2:multicolor:primary:owl',
             'BIRD:2:primary',
             'ARRANGEMENT9BEAST&MONSTER,RESPECTANT'],
            list(parse(u'Per pale azure ermined argent and argent ermined azure, two owls respectant counterchanged argent and azure.').describe()))

        self.assertEquals(
            ['AR',
             u'CROSS:1:azure:complex line:primary',
             u'CROSS:1:complex line:primary',
             'KNOT AND ROPE:1:or'],
            list(parse(u'Argent, on a cross nowy azure a trefoil knot Or.').describe()))

        self.assertEquals(
            ['CRAC:1:purpure:primary',
             'CRAC:1:primary',
             'ROUNDEL:5:purpure:primary',
             'ROUNDEL:primary'],
            list(parse(u'(Fieldless) A cross of five golpes.').describe()))

        self.assertEquals(
            ['GU',
             'ARROW:1:argent:primary',
             'ARROW:1:primary',
             'HEAD-BIRD:2:argent',
             'ARRANGEMENT9HEAD,RESPECTANT'],
            list(parse(u"Gules, an arrow inverted between two bird's heads couped respectant argent.").describe()))

        self.assertEquals(
            ['QLY:azure:~and gules',
             'BIRD:1:argent:primary:owl',
             'BIRD9DEMI:1:argent:primary:owl',
             'BIRD:1:primary',
             'WREATH,OTHER:1:argent',
             'FLOWER-MULTI-PETALED:seme:argent'],
            list(parse(u'Quarterly azure and gules, an owl within a wreath of daisies argent.').describe()))

        self.assertEquals(
            ['SA',
             'ROUNDEL:1:argent:primary',
             'ROUNDEL:1:primary',
             'CRAC:1:azure:formy',
             'BORDURE:1:multicolor'],
            list(parse(u'Sable, on a plate a Latin cross formy azure, a bordure parted bordurewise indented azure and argent.').describe()))

        self.assertEquals(
            ['AR',
             'AMPHIBIAN-FROG:1:vert:primary:affronte',
             'AMPHIBIAN-FROG:1:primary:affronte',
             'HEART:1:gules',
             'LEAF:1:gules',
             'ARRANGEMENT-IN ANNULO:1:sable',
             'LETTERS,RUNES AND SYMBOLS:sable'],
            list(parse(u'Argent, a toad sejant affronty vert, spotted and crowned Or, charged with a heart gules fimbriated Or within in annulo the inscription "Before you meet the handsome prince you have to kiss a lot of toads" sable.').describe()))

        self.assertEquals(
            ['BEAST-BOAR:1:or:primary:passant',
             'BEAST-BOAR:1:primary:passant',
             'JEWELS AND JEWELRY:1:gules'],
            list(parse(u'(Fieldless) A boar passant Or charged on the shoulder with a hexagonal gemstone gules.').describe()))

        self.assertEquals(
            ['PC:argent:~and sable',
             'TREE9BRANCH:4:vert:primary',
             'TREE9BRANCH:primary',
             'INSA:4:vert:primary',
             'SWORD:1:argent:primary',
             'SWORD:1:primary'],
            list(parse(u'Per chevron throughout argent and sable, between two pairs of branches in saltire vert, a sword inverted argent.').describe()))

        self.assertEquals(
            ['PC:azure:~and argent',
             'FDL:2:primary',
             'INSECT-BUTTERFLY AND MOTH:1:primary',
             'BORDURE:1:multicolor',
             'GOUTE:seme:multicolor'],
            list(parse(u'Per chevron azure and argent, two fleurs-de-lys and a butterfly counterchanged, a bordure goutty all counterchanged argent and gules.').describe()))

        self.assertEquals(
            ['PB:or:~and sable',
             'GOUTE:1:multicolor:primary',
             'GOUTE:1:primary'],
            list(parse(u'Per bend Or and sable, a goutte counterchanged.').describe()))

        self.assertEquals(
            ['GU',
             'CALIPER AND COMPASS:1:argent:primary',
             'TOOL9OTHER:1:argent:primary',
             'CALIPER AND COMPASS:1:primary',
             'CRESCENT:3:argent',
             'STAR:3:sable:of 6',
             'CALTRAP:3:sable:of 6',
             'ESTOILE:3:sable:of 6',
             'SUN:3:sable:of 6'],
            list(parse(u'Gules, a pair of calipers and in chief three crescents argent each crescent charged with a mullet of six points sable.').describe()))

if __name__ == "__main__":
    unittest.main()
