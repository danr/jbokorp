# -*- coding: utf-8 -*-

import re
import sb.util as util
import cPickle as pickle

def compound_to_affixes(compound):
    """Split a compound word into affixes.

    Written by Dag Odenhall, code is in both dag/jbo and dag/vlasisku,
    He writes this credit:
        - Adam Lopresto, for the Perl code compound2affixes mimics.

    """
    c = r'[bcdfgjklmnprstvxz]'
    v = r'[aeiou]'
    cc = r'''(?:bl|br|
                cf|ck|cl|cm|cn|cp|cr|ct|
                dj|dr|dz|fl|fr|gl|gr|
                jb|jd|jg|jm|jv|kl|kr|
                ml|mr|pl|pr|
                sf|sk|sl|sm|sn|sp|sr|st|
                tc|tr|ts|vl|vr|xl|xr|
                zb|zd|zg|zm|zv)'''
    vv = r'(?:ai|ei|oi|au)'
    rafsi3v = r"(?:{cc}{v}|{c}{vv}|{c}{v}'{v})".format(**locals())
    rafsi3 = r'(?:{rafsi3v}|{c}{v}{c})'.format(**locals())
    rafsi4 = r'(?:{c}{v}{c}{c}|{cc}{v}{c})'.format(**locals())
    rafsi5 = r'{rafsi4}{v}'.format(**locals())

    for i in xrange(1, len(compound)/3+1):
        reg = r'(?:({rafsi3})[nry]??|({rafsi4})y)'.format(**locals()) * i
        reg2 = r'^{reg}({rafsi3v}|{rafsi5})$$'.format(**locals())
        matches = re.findall(reg2, compound, re.VERBOSE)
        if matches:
            return tuple(r for r in matches[0] if r)

    return tuple()


def make_rafsi(word, pos, out):
    WORD = util.read_annotation(word)
    POS = util.read_annotation(pos)
    OUT = {}

    for tokid in WORD:
        w = WORD[tokid]
        if POS[tokid] == "OTHER":
            rafsi = compound_to_affixes(w)
            OUT[tokid] = "|".join(rafsi)

    util.clear_annotation(out)
    util.write_annotation(out, OUT)


def make_longrafsi(rafsi, out, in_pickle):
    RAFSI = util.read_annotation(rafsi)
    OUT = {}
    rafsi_dict = pickle.load(open(in_pickle, 'rb'))

    for tokid in RAFSI:
        rafsi = RAFSI[tokid].split("|")
        if rafsi and rafsi[0]:
            OUT[tokid] = "|".join(rafsi_dict.get(r, 'UNDEF') for r in rafsi)

    util.clear_annotation(out)
    util.write_annotation(out, OUT)


def pickle_jbovlaste(jbovlaste_file, out_pickle):
    import xml.etree.ElementTree as ET
    root = ET.parse(jbovlaste_file).getroot()
    # rafsi_re = re.compile(r"proposed rafsi[: \-]*([a-z][a-z]'?[a-z])[.\- ]")
    rafsi_re = re.compile(r"-([a-z][a-z]'?[a-z])-")
    rd = {}
    erd = {}
    for valsi in root.iter('valsi'):
        ty = valsi.attrib['type']
        word = valsi.attrib['word']
        for rafsi in valsi.iter('rafsi'):
            rd[rafsi.text] = word
        if ty == 'gismu':
            rd[word[0:4]] = word
            rd[word] = word
        if ty == 'experimental gismu':
            erd[word[0:4]] = word
            erd[word] = word
        if 'gismu' in ty or 'cmavo' in ty:
            for note in valsi.iter('notes'):
                for m in re.findall(rafsi_re, note.text.lower()):
                    erd[m] = word

    for k in erd:
        if k in rd:
            print 'duplicate: ' + k
        else:
            rd[k] = erd[k]

    pickle.dump(rd, open(out_pickle, 'wb'))


######################################################################

if __name__ == '__main__':
    util.run.main(make_rafsi=make_rafsi,
                  make_longrafsi=make_longrafsi,
                  pickle_jbovlaste=pickle_jbovlaste)

