
import sb.util as util
import os
import re
import subprocess

from unidecode import unidecode

def call(cmd,txt):
    """Call a subprocess"""
    p = subprocess.Popen(cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    out = p.communicate(input=txt)[0]
    p.wait()
    return out, p.returncode

dot    = re.compile(r"\.")
good   = re.compile(r"cmavo\(s\)|lujvo|gismu")
cmevla = re.compile(r"cmene")
quote  = re.compile(r"la'o|zoi")
quotew = re.compile(r"zo'oi|la'oi|me'oi")
upper  = re.compile(r"contains invalid uppercase")

def is_lojban(s):
    """
    Does this string seem to be in lojban? 
    
    Morphology checked by vlatai, uses the same alogrithm as for the irc logs.
    """
    words = [dot.sub("",unidecode(w)) for w in s.split()]
    out, _ = call("/home/dan/code/jbofihe/vlatai","\n".join(words))

    total_count  = len(out.split('\n')) - 1

    good_count   = len(good.findall(out))
    cmevla_count = len(cmevla.findall(out))
    quote_count  = len(quote.findall(out))
    quotew_count = len(quotew.findall(out))
    upper_count  = len(upper.findall(out))

    total_count -= quote_count * 3
    total_count -= quotew_count

    if total_count > 0:
        score = (good_count + cmevla_count * 0.4) / total_count
    else: 
        score = 0

    needed = 0.8

    if total_count == 0:
        return False
    elif total_count == 1 and upper_count == 1:
        return False
    elif total_count == 2:
        needed = 0.6
    elif total_count == 3:
        needed = 0.66
    
    return score > needed

    print
    print "Result:", score > needed
    print unidecode(s)
    print
    print good_count, cmevla_count, quote_count, quotew_count, total_count
    print score, needed
    print
    print out
    print


if __name__ == '__main__':
    util.run.main(is_lojban = is_lojban)

