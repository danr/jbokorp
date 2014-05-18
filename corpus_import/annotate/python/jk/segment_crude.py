from bs4 import BeautifulSoup
from unidecode import unidecode
import sb.util as util
import re
import subprocess

def tokenise(cmd,txt):
    p = subprocess.Popen(cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    out = p.communicate(input=txt)[0]
    p.wait()
    return out, p.returncode

def segment_crude(in_file,out_file,cmd):

    if cmd == "segment":
        run_cmd = lambda txt : tokenise("cmafihe -t",txt)[0]
    elif cmd == "parse":
        def g(txt):
            parse, excode = tokenise("jbofihe -X",txt)
            if excode:
                return tokenise("cmafihe -X",txt)[0]
            else:
                return parse
        run_cmd = g

    soup = BeautifulSoup(open(in_file), "html.parser")

    for s in list(soup.strings):
        if len(s.strip()) > 0:
            txt = unidecode(s)
            txt_soup = BeautifulSoup(unidecode(run_cmd(txt)), "html.parser")
            s.replace_with(txt_soup)

    open(out_file,"w").write(unidecode(unicode(soup)))

if __name__ == '__main__':
    util.run.main(segment_crude)

