#!/usr/bin/python

import unittest

from parse import parse

class TestCases(unittest.TestCase):
    
    def test_one(self):
        self.assertEquals(
            ['ARM:1:argent:primary:embowed', 'ARM:1:primary:embowed', 'HORN AND ATTIRES:1:or'], 
            list(parse(u"(Fieldless) An arm embowed argent sustaining a stag's attire Or.").describe()))
        self.assertEquals(
            ['CRAC:1:or:primary', 'CRAC:1:primary', 'FDL:1:sable'], 
            list(parse(u'(Fieldless) On a cross couped Or, a fleur-de-lys sable').describe()))
        self.assertEquals(
            ['AR', 'DOG:1:sable:primary:passant', 'DOG:1:primary:passant', 'ESCALLOP:3:gules'], 
            list(parse(u'Argent, a greyhound courant sable between three escallops gules.').describe()))
        self.assertEquals(
            ['AR', 'SPINDLE:1:purpure:primary', 'TOOL-SEWING AND WEAVING:1:purpure:primary', 'SPINDLE:1:primary', 'CHIEF:1:purpure', 'POLE-AXE:1:argent'], 
            list(parse(u'Argent, an empty bottom-whorl drop spindle and on a chief purpure a glaive argent.').describe()))
        self.assertEquals(
            ['AZ', 'CRAC:1:or:primary:moline', 'CRAC:1:primary:moline', 'CHIEF:1:or', 'BIRD:3:azure:volant to dexter', 'BIRD9DEMI:3:azure:volant to dexter'], 
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
            ['ER', 'FEATHER AND QUILL:1:purpure:primary:bendwise sinister', 'PEN:1:purpure:primary:bendwise sinister', 'FEATHER AND QUILL:1:primary:bendwise sinister'], 
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

        #self.assertEquals(
        #    [u'PB:sable:~and argent', 'BEND:1:azure:primary', 'FIELD DIV.-BENDY:1:azure:primary', 'BEND:1:primary', 'CRAMPET:3:argent', 'MONSTER-PHOENIX:2'],
        #    list(parse(u'Per bend sable and argent, on a bend azure between two phoenixes counterchanged, three crampets argent').describe()))

        self.assertEquals(
            ['AR', 'BEAST-MOUSE AND RAT:1:proper:primary:passant', 'BEAST-MOUSE AND RAT:1:primary:passant', 'BORDURE:1:purpure'],
            list(parse(u'Argent, a brown mouse passant proper and a bordure purpure\n').describe()))
        
        self.assertEquals(
            [u'QLY:sable:~and multicolor', 'FIELD TREATMENT-VAIRY', 'CASTLE:3:or:primary:palewise', 'CASTLE:3:primary:palewise', 'ARRANGEMENT-IN BEND:or'],
            list(parse(u'Quarterly sable and vairy sable, argent, gules and Or, in bend three towers palewise Or\n\n').describe()))

        self.assertEquals(
            ['OR', 'BEND:1:azure:primary:cotised', 'FIELD DIV.-BENDY:1:azure:primary:cotised', 'BEND:1:primary:cotised', 'FDL:1:or:palewise', 'ROSE:2:or', 'CHIEF:1:gules', 'CAT:1:or:passant'],
            list(parse(u'Or, on a bend cotised azure a fleur-de-lys palewise between two cinquefoils Or and on a chief gules a lion passant guardant Or\n\n').describe()))

        self.assertEquals(
            ['AZ', 'PLANT-WHEAT:seme:or:seme on field', 'FIELD TREATMENT-SEME (9OTHER):or', 'PALE:1:or:primary', 'FIELD DIV.-PALY:1:or:primary', 'PALE:1:primary', 'SWORD:1:azure'],
            list(parse(u'Azure semy of ears of wheat, on a pale Or a sword azure').describe()))

        self.assertEquals(
            [u'PBS:sable:~and argent', 'STAR:1:or:primary', 'CALTRAP:1:or:primary', 'ESTOILE:1:or:primary', 'SUN-DEMI:1:or:primary', 'SUN:1:or:primary', 'STAR:1:primary', 'HAMMER:2:proper:primary', 'HAMMER:2:primary', 'INSA:2:proper:primary'],
            list(parse(u"Per bend sinister sable and argent, a spur rowel Or and two smith's hammers in saltire proper.").describe()))

        self.assertEquals(
            ['AR', 'MONSTER-PHOENIX:1:gules:primary', 'MONSTER-PHOENIX:1:primary', 'FIRE AND FLAME:1:proper', 'BORDURE:1:gules', 'ROUNDEL:seme:or'],
            list(parse(u'Argent, a phoenix gules rising from flames proper and a bordure gules semy of bezants').describe()))

        self.assertEquals(
            ['VT', 'CAULDRON AND COOKING POT:1:or:primary', 'CAULDRON AND COOKING POT:1:primary', 'FIRE AND FLAME:1:or', 'CHIEF:1:or', 'FORK AND SPOON:2:vert', 'INSA:2:vert'],
            list(parse(u'Vert, a cauldron issuant from a flame and on a chief Or two ladles in saltire vert\n\n').describe()))

        self.assertEquals(
            [u'QLY:sable:~and or', 'BEND:1:argent:primary', 'FIELD DIV.-BENDY:1:argent:primary', 'BEND:1:primary', 'DOG:2:sable:rampant', 'PAW PRINT:5 or more:sable'],
            list(parse(u'Quarterly sable and Or, on a bend argent between two wolves rampant contourney five paw prints sable.\n\n').describe()))

if __name__ == "__main__":
    unittest.main()
