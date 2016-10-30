from bs4 import BeautifulSoup
from unidecode import unidecode
import sb.util as util
import re
import subprocess
from collections import defaultdict
import json


def call_tool(cmd,txt):
    p = subprocess.Popen(cmd.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    out, err = p.communicate(input=txt.encode('ascii',errors='ignore'))
    p.wait()
    return out, p.returncode


import xml.etree.ElementTree as ET


def on_text(in_file, out_file, handle):
    xml = ET.parse(in_file)
    root = xml.getroot()

    ks = []

    for elem in root.iter():
        if elem.text:
            def k(elem):
                r = handle(elem.text)
                if isinstance(r, basestring):
                    elem.text = r
                else:
                    elem.text = ''
                    elem.append(r)
            ks.append((k, elem))

    for k, elem in ks:
        k(elem)

    xml.write(out_file, encoding='utf-8')


clean_re = re.compile(r"[^a-zA-Z0-9' \n\t]+")
def rm_junk(s):
    return re.sub(clean_re, '', s).lower()


# BUG: splits up zoi-quotes, too
def vlatai_text(doc):
    out, exc = call_tool('vlatai', '\n'.join(rm_junk(doc).split()))
    return ' '.join(w
                    for line in out.strip().split('\n')
                    if line
                    for w in line.split(':')[2].strip().split())


def jbofihe_text(doc):
    p = ET.Element('p')
    # BUG: splits at "zo i" and "i" inside lu...li'u
    for sent in re.compile(r' (?=i )').split(doc):
        # print sent
        out, exc = call_tool('jbofihe -X', rm_junk(sent))
        # print out
        if exc == 0:
            p.append(jbofihe_process_output(out))
        else:
            s = ET.SubElement(p, 's')
            s.attrib['grammar'] = "none"
            for w in sent.split():
                word = ET.SubElement(s, 'word')
                word.text = w
    return p


def jbofihe(in_file, out_file):
    on_text(in_file, out_file, jbofihe_text)


def vlatai(in_file, out_file):
    on_text(in_file, out_file, vlatai_text)


def selbriplaces(ds):
    out = []
    for d in ds:
        out.append(d['selbriplace'].rstrip('t'))
    return '|'.join(out)


def jbofihe_process_output(doc):
    args = []
    newinfo = []
    newargs = []
    i = 0
    s = ET.Element('s')
    s.attrib['grammar'] = 'jbofihe'
    for line in doc.split('\n'):
        try:
            d = json.loads(line)
            if d['type'] == 'info':
                newinfo.append(d['info'])
            elif d['type'] == 'argbegin':
                del d['type']
                newargs.append(d)
            elif d['type'] == 'argend':
                args.pop()
        except ValueError:
            for w in quicksplit(line.replace('_',' ')):
                w = w.strip()
                if w:
                    word = ET.SubElement(s, 'word')
                    word.text = w
                    if newinfo:
                        word.attrib['info'] = '|'.join(newinfo)
                        newinfo = []
                    word.attrib['dephead'] = str((args + [(None,)])[0][0])
                    word.attrib['ref'] = str(i)
                    word.attrib['deprel'] = selbriplaces(map(lambda arg: arg[1], args[0:1]))
                    word.attrib['tags'] = selbriplaces(newargs)
                    for n in newargs:
                        args.append((i, n))
                    newargs=[]
                    i+=1
    return s


c='bcdfgjklmnprstvxz'
cc=[a+b for a in c for b in c]+[a+'y'+b for a in c for b in c]


def has_cc(w):
    for x in cc:
        if x in w:
            return True
    return False


def split_at_c(w):
    out = []
    temp = ""
    for s in re.split('(['+c+'])',w):
        if s == '':
            continue
        elif s in c:
            temp += s
        else:
            yield temp + s
            temp = ""


# does not work with zoi-quotes
# used to break apart things like uinai that jbofihe insists on grouping
def quicksplit(ws):
    for w in ws.split():
        if has_cc(w):
            yield w
        elif w.strip()[-1:] in c:
            yield w # cmevla
        else:
            for cmavo in split_at_c(w):
                yield cmavo

if __name__ == '__main__':
    util.run.main(vlatai=vlatai, jbofihe=jbofihe)


