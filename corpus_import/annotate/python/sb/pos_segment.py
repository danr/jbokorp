# -*- coding: utf-8 -*-

import re
import util
import cPickle as pickle
try:
    import crf # for CRF++ models
except:
    pass


def pos_segment(text, element, pos, delimiter, out):
    """

    We will need
        token.n
    as the first argument

    pos = selma'o

    element could be like sentence or paragraph

    """
    document = [(k,txt) for k , txt in util.read_annotation_iteritems(text)]
    delims = delimiter.split('|')
    POS = util.read_annotation(pos)
    OUT = {}

    start = document[0][0]
    prev = start


    for k, _txt in document:
        if POS[k] in delims:
            startW = start.split(':')[1].split('-')[0]
            prevW = prev.split(':')[1].split('-')[1]
            edge = util.mkEdge(element, (startW, prevW))
            start = k
            OUT[edge] = None
        prev = k

    startW = start.split(':')[1].split('-')[0]
    prevW = prev.split(':')[1].split('-')[1]
    edge = util.mkEdge(element, (startW, prevW))
    OUT[edge] = None

    util.clear_annotation(out)

    util.write_annotation(out, OUT)




######################################################################

if __name__ == '__main__':
    util.run.main(pos_segment = pos_segment)
