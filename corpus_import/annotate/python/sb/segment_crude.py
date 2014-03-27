import xml.etree.ElementTree as ET
import util
import re
import subprocess

xml_line = re.compile(r"^\s*<.*>\s*$")

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
        run_cmd = lambda txt : tokenise("/home/dan/code/jbofihe/cmafihe -t",txt)[0]
    elif cmd == "parse":
        def g(txt):
            parse, excode = tokenise("/home/dan/code/jbofihe/jbofihe -X",txt)
            if excode:
                return tokenise("/home/dan/code/jbofihe/cmafihe -X",txt)[0]
            else:
                return parse
        run_cmd = g

    with open(in_file) as f:
        lines = f.readlines()
        f.close()

    chunks = []
    last_xml = True
    out = []

    for l in lines:
        if xml_line.search(l):
            # is an xml line
            if not last_xml:
                out.append(run_cmd(' '.join(chunks)))
                chunks = []
            out.append(l)
            last_xml = True
        else:
            chunks.append(l)
            last_xml = False

    if len(chunks) > 0:
        out.append(run_cmd(' '.join(chunks)))

    # print ''.join(out)

    with open(out_file,'w') as f:
        f.write(''.join(out))
        f.close()

if __name__ == '__main__':
    util.run.main(segment_crude)



