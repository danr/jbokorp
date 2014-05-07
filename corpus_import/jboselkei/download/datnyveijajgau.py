import xml.etree.ElementTree as ET
import HTMLParser
h = HTMLParser.HTMLParser()
# print h.unescape('&pound;682m')

def table_to_dict(tree):
    ret = {}
    for tbl in tree.iter("table"):
        d = {}
        for clmn in tbl.iter("column"):
            d[clmn.attrib['name']] = h.unescape(clmn.text)
        ret[d['id']] = d
    return ret

def file_to_dict(fname):
    return table_to_dict(ET.parse(fname).getroot())

users = file_to_dict('users.xml')
trans = file_to_dict('translations.xml')
posts = file_to_dict('posts.xml')

for i,d in trans.items():
    print d['entry']
    print users[d['authorid']]['name']
