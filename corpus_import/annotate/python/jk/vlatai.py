# -*- coding: utf-8 -*-

import re
import sb.util as util
import cPickle as pickle

from subprocess import Popen, PIPE

def vlatai(word, pos, out):
    WORD = util.read_annotation(word)
    POS = util.read_annotation(pos)

    inp = []
    tokids = []

    for tokid in WORD:
        inp.append(WORD[tokid].replace('.',''))
        tokids.append(tokid)

    p = Popen('vlatai', stdin=PIPE, stdout=PIPE, stderr=PIPE)
    lines, err = p.communicate(input='\n'.join(inp))
    p.wait()

    OUT = {}
    for tokid, line in zip(tokids, lines.split('\n')):
        v = line.split(':')[1].strip().split()[0]
        if v == 'cmavo(s)':
            v = 'cmavo'
        OUT[tokid] = v

    util.clear_annotation(out)
    util.write_annotation(out, OUT)


def experimental(word, tai, out, in_pickle):
    WORD = util.read_annotation(word)
    TAI = util.read_annotation(tai)
    catni = pickle.load(open(in_pickle, 'rb'))
    OUT = {}

    for tokid in WORD:
        if TAI[tokid] in ['cmavo','gismu']:
            OUT[tokid] = str(WORD[tokid].replace('.','') not in catni)
        else:
            OUT[tokid] = "UNDEF"

    util.clear_annotation(out)
    util.write_annotation(out, OUT)



def pickle_jbovlaste(jbovlaste_file, out_pickle):
    import xml.etree.ElementTree as ET
    root = ET.parse(jbovlaste_file).getroot()
    catni = {}
    for valsi in root.iter('valsi'):
        ty = valsi.attrib['type']
        word = valsi.attrib['word']
        if ty in ['gismu','cmavo']:
            catni[word] = True

    pickle.dump(catni, open(out_pickle, 'wb'))


######################################################################

if __name__ == '__main__':
    util.run.main(vlatai=vlatai, experimental=experimental, pickle_jbovlaste=pickle_jbovlaste)

