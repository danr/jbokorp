# import xml.etree.ElementTree as ET
import lxml.etree as ET
import HTMLParser
import re

amp = re.compile(r"\\&")
h = HTMLParser.HTMLParser()

# print h.unescape('&pound;682m')

def table_to_dict(tree):
    ret = {}
    for tbl in tree.iter("table"):
        d = {}
        for clmn in tbl.iter("column"):
            t = clmn.text
            if t:
                o = "" + t
                t = amp.sub("&",t)
                t = h.unescape(h.unescape(t))
                # if o != t:
                #     print "####"
                #     print o
                #     print "===="
                #     print t
                #     print "^^^^"
            d[clmn.attrib['name']] = t
        ret[d['id']] = d
    return ret

def file_to_dict(fname):
    return table_to_dict(ET.parse(fname).getroot())

users = file_to_dict('users.xml')
trans = file_to_dict('translations.xml')
posts = file_to_dict('posts.xml')

msgs = ET.Element('text')

for i,d in trans.items():
    # print "########"
    # print i
    # print d['entry']
    if d['entry']:
        msg = ET.SubElement(msgs, 'msg', 
            id=i,
            author=users[d['authorid']]['name'],
            difficulty=posts[d['postid']]['difficulty'],
            sourceauthor=users[posts[d['postid']]['authorid']]['name'],
            sourceid=d['postid'],
            source=posts[d['postid']]['entry'] or '',
            sourcelang=posts[d['postid']]['language'],
            sourcecomment=posts[d['postid']]['comment'] or '',
            comment=d['comment'] or '',
            date=d['date'].split(" ")[0],
            time=d['date'].split(" ")[1],
            value=d['value'],
            reviews=d['reviews'])
        msg.text = d['entry']

print ET.tostring(msgs, pretty_print = True)

