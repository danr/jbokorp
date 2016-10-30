# -*- coding: utf-8 -*-

import re
import sb.util as util
import cPickle as pickle


def pos(word, out, in_pickle):
    WORD = util.read_annotation(word)
    OUT = {}
    pos = pickle.load(open(in_pickle, 'rb'))

    for tokid in WORD:
        OUT[tokid] = pos.get(WORD[tokid],'OTHER').rstrip('0123456789*abcdefghijklmnopqrstuvwxyz')

    util.clear_annotation(out)
    util.write_annotation(out, OUT)


def pickle_jbovlaste(jbovlaste_file, out_pickle):
    import xml.etree.ElementTree as ET
    root = ET.parse(jbovlaste_file).getroot()
    pos = {}
    for valsi in root.iter('valsi'):
        w = valsi.attrib['word']
        t = valsi.attrib['type']
        for selmaho in valsi.iter('selmaho'):
            pos[w] = selmaho.text

    pickle.dump(pos, open(out_pickle, 'wb'))


######################################################################

if __name__ == '__main__':
    util.run.main(pos,
                  pickle_jbovlaste=pickle_jbovlaste)

