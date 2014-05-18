import lxml.etree as ET
import csv
import sys

# Get links
links = {}
with open('links.csv', 'rb') as csvfile:
    rdr = csv.reader(csvfile, delimiter='\t', quotechar=None)
    for row in rdr:
        links[row[0]] = links.get(row[0],[]) + [row[1]]

jbosent = {}
# First pass: find lojban sentences
with open('sentences_detailed.csv', 'rb') as csvfile:
    rdr = csv.reader(csvfile, delimiter='\t', quotechar=None)
    for row in rdr:
        if row[1] == 'jbo':
            jbosent[row[0]] = dict(
                id_num = row[0],
                sent =   row[2],
                author = row[3],
                date =   row[4]
                )

# Second pass: find their english translations
with open('sentences_detailed.csv', 'rb') as csvfile:
    rdr = csv.reader(csvfile, delimiter='\t', quotechar=None)
    for row in rdr:
        if row[1] == 'eng': 
            for link_id in links.get(row[0],[]): 
                if link_id in jbosent:
                    jbosent[link_id]['eng'] = row[2]

root = ET.Element('text')

for _,d in jbosent.items():
    try:
        date=d['date'].split(" ")[0]
        time=d['date'].split(" ")[1]
    except:
        date=''
        time=''

    try:
        msg = ET.SubElement(root, 'msg',
            tatoebaid=d['id_num'],
            author=d['author'],
            source=d.get('eng',''),
            date=date,
            time=time)
        msg.text = unicode(d['sent'])
        x = '' + ET.tostring(msg, pretty_print = True) + ''
    except:
        # print "msg= error:", sys.exc_info()[0]
        # print d
        pass

print ET.tostring(root, pretty_print = True)

