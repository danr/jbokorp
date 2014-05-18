import email.parser
import re

from datetime import datetime

import dateutil.parser 

import util

from xml.sax.saxutils import escape, quoteattr

from sb.islojban import is_lojban

from_re = re.compile("^From ")

# Dates are of lots of forms:
# Fri, 2 Apr 1993 16:40:37 BST 
# Wed, 06 Jun 90 11:44:24 -0700
# 6 Nov 90 00:02:21 EST (Tue)

months = dict(zip(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],range(1,13)))

def parse(fname):
    content = open(fname).read()
    chunk = []
    for l in content.split("\n"):
        if from_re.match(l) and len(chunk) > 0:
            # the content in chunk is now a mail
            mail = email.message_from_string("\n".join(chunk))

            # for k,v in mail.items():
            #     print k,v

            dt = mail.get('Date','')
            if dt == "":
                mid = mail.get('Message-Id','')
                if mid[1:3] == "19":
                    dt = mid[1:9]
                else:
                    dt = mid[1:7]
            # print "dt:", dt
            
            date = None
            try:
                date = dateutil.parser.parse(dt)
            except ValueError:
                try:
                    date = dateutil.parser.parse(dt[:-8])
                except ValueError:
                    pass
                    # print "Cannot parse", dt

            if date is not None and dt != "":
                if date.year < 2014: 
                    date = date.strftime("%Y-%m-%d")
                else:
                    date = ""
            else:
                date = ""

            # print "date:", date
            # print

            header_printed = False

            try:
                paragraphs = mail.get_payload().split("\n\n")
            except:
                paragraphs = []

            for x in paragraphs:
                if is_lojban(x):

                    if not header_printed:
                        header_printed = True
                        def lk(x):
                            return quoteattr(mail.get(x,''))
                        print "<msg date=%s author=%s subject=%s>" % (quoteattr(date),lk('From'),lk('Subject'))

                    print "<chunk>"
                    print escape(x)
                    print "</chunk>"

            if header_printed:
                print "</msg>"

            chunk = []

        else:
            chunk.append(l)

if __name__ == "__main__":
    util.run.main(parse) 
