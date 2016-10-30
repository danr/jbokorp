from xml.sax.saxutils import escape
import lxml.etree as ET
import sb.util as util
import re
import subprocess
from unidecode import unidecode
import codecs

from collections import Counter

matchers = []

def pat(r):
    matchers.append(re.compile(r"^" + r + r"$"))

# ircname = r"/\A[a-z_\-\[\]\\^{}|`][a-z0-9_\-\[\]\\^{}|`]*\z/i"
ircname = r"\S*"

# Broca: oi le dei velsku
pat(r"\s?(?P<nick>" + ircname + r"): (?P<msg>.*)")

# <Broca> go'i
pat(r"<\s?(?P<nick>" + ircname + r")> (?P<msg>.*)")

# 01 Aug 2003 02:10:18
pretty_full_date = r"(?P<day>\d{2}) (?P<pretty_month>\S{3}) (?P<year>\d{4}) (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})"

# 01 Aug 2003 02:10
pretty_mini_date = r"(?P<day>\d{2}) (?P<pretty_month>\S{3}) (?P<year>\d{4}) (?P<hour>\d{2}):(?P<min>\d{2})"

# 2014-03-28 12:13:11 PDT/-0700
digit_date = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2}) ...\/....."

# 19:39
hhmm_time = r"(?P<hour>\d{2}):(?P<min>\d{2})"

# [19:39]
brack_time = r"\[" + hhmm_time + r"\]"

# 01 Aug 2003 02:10:18 <carbon> la'o gy. gyrations gy.
pat(pretty_full_date + r" <\s?(?P<nick>" + ircname + r")> (?P<msg>.*)")

# 20 Sep 2010 15:22 < jaupre> no.
pat(pretty_mini_date + r" <\s?(?P<nick>" + ircname + r")> (?P<msg>.*)")

# 20 Jan 2010 07:21:58  * codrus na'e co'e cusku da poi ve vimcu de noi vo'a jinvi fi ra
# 11 Jun 2008 20:46:50 * durka cu slilu lo stedu
pat(pretty_full_date + r" \s?\* (?P<msg>(?P<nick>" + ircname + r") .*)")

# 23 Sep 2010 16:09  * rlpowell terpa
pat(pretty_mini_date + r" \s?\* (?P<msg>(?P<nick>" + ircname + r") .*)")

relayed_name = r"[^>]+"

# 2016-10-27 05:33:35 PDT/-0700 <^^^^> > "<03gleki> i za'a so'e lo jbopre ca'o drani be na ku pilno lo cnima'o"
pat(digit_date + r" <\s?(?P<relay>" + ircname + r")> > \"<.[0-9][0-9]..(?P<nick>" + relayed_name + r").> (?P<msg>.*)\"")

# 2016-10-22 02:43:40 PDT/-0700 <mensi1> 13ilmen: cu'u la'o gy.la_aLEKsolas.gy.: doi te frica be lo cmavo bei lo rafsi ko sezgle ga'i (╯°□°)つ ======> | 2016-10-22T02:20:59.478Z
pat(digit_date + r" <\s?(?P<relay>" + ircname + r")> [0-9][0-9](?P<nick>" + relayed_name + r"): (?P<msg>.*)")

# 2016-10-19 08:57:38 PDT/-0700 <^^^^> <03Kleo Kapaj>: .i mi ba lo nu mi mulgau lo ckule djedi ku vau kei ku jungau do
# 2016-10-29 16:42:59 PDT/-0700 <^^^^> <06selckiku>: .i .au bu'o zo cladaxi cu jbocme lo mensi
pat(digit_date + r" <\s?(?P<relay>" + ircname + r")> <[0-9][0-9](?P<nick>" + relayed_name + r")>: (?P<msg>.*)")

# 2016-09-28 03:48:03 PDT/-0700 <o`> <07aksilys> .i lo cmene tanbargu skarai zvati
pat(digit_date + r" <\s?(?P<relay>" + ircname + r")> <.[0-9][0-9](?P<nick>" + relayed_name + r").>:? (?P<msg>.*)")

# 2016-02-01 07:07:00 PST/-0800 <iii> <nejni_marji>: .i xu jbonunsla ca
pat(digit_date + r" <\s?(?P<relay>" + ircname + r")> <(?P<nick>" + relayed_name + r")>:? (?P<msg>.*)")

# 2014-03-28 12:13:11 PDT/-0700 <danr> .u'i
pat(digit_date + r" <\s?(?P<nick>" + ircname + r")> (?P<msg>.*)")

# 2014-03-26 13:49:13 PDT/-0700 * durka42 cu nitcu lo nu cliva
pat(digit_date + r" \s?\* (?P<msg>(?P<nick>" + ircname + r") .*)")

# [19:39] <Broca> coi zinks
pat(brack_time + r" <(?P<nick>" + ircname + r")> (?P<msg>.*)")

# 09:11 < cliva> go'i
pat(hhmm_time + r" <\s?(?P<nick>" + ircname + r")> (?P<msg>.*)")

# 14:59  * Ilmen ca'o tinju'i lo .albumza'o
pat(hhmm_time + r" \s?\* (?P<msg>(?P<nick>" + ircname + r") .*)")

# [22:06] *** bancus sezgletu
pat(brack_time + r" \s?\*\*\* \s?(?P<msg>(?P<nick>" + ircname + r") .*)")

# 19 Jan 2010 20:01:06 -!- vesna [i=4d7c290c@gateway/web/freenode/x-xprmfgfzgrnhorgn] has joined #lojban

months = dict(zip(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],range(1,13)))

def parse_irc(in_file):
    LIMIT = 10000
    roots = {}
    files = Counter()
    docs  = Counter()

    def write_root(year, root):
        fname = "irc" + year + "-" + str(files[year]) + ".wip"
        ET.ElementTree(root).write(fname, encoding='utf-8')
        print "wrote", fname
        root.clear()
        del roots[year]
        files[year] += 1
        docs[year] = 0

    for year, attach in messages(in_file):
        if year not in roots:
            roots[year] = ET.Element('text')

        root = roots[year]
        attach(root)
        docs[year] += 1

        if docs[year] > LIMIT:
            write_root(year, root)

    for year, root in list(roots.iteritems()):
        write_root(year, root)


def messages(in_file):
    for l in codecs.open(in_file, encoding="utf-8", errors='ignore').readlines():
        for m in matchers:
            d = m.match(l)
            if d is not None:
                m = handle_match(d.groupdict())
                if m:
                    yield m
                break
        else:
            # print(l.encode('utf-8'))
            # print 'no match!'
            pass


def banned(nick):
    return nick in ["livla","mensi","zbagamumble","||","||1","^^^^","o`","o`1","xx","nuzba"]


def handle_match(d):
    if d.get('msg') and not banned(d["nick"]):
        if d.get('pretty_month'):
            d['month'] = "%02d" % months[d['pretty_month']]

        y, m, day = d.get('year'), d.get('month'), d.get('day')

        if y and m and day:
            d['date'] = y + "-" + m + "-" + day

        if not d.get('sec'):
            d['sec'] = "00"

        hh, mm, ss = d.get('hour'), d.get('min'), d.get('sec')

        if hh and mm and ss:
            d['time'] = hh + ":" + mm + ":" + ss

        # print(d.encode('utf-8'))
        return make_message(d)

clean_re = re.compile(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\u10000-\u10FFFF]+')
def clean(s):
    return re.sub(clean_re, '', s)

def make_message(d):
    year = d.get('year', "undef")

    try:
        def attach(root):
            msg = ET.SubElement(root, 'msg',
                date=d.get('date',''),
                time=d.get('time',''),
                relay=d.get('relay',''),
                nick=clean(d['nick']))
            msg.text = clean(d['msg'])
        return year, attach
    except Exception as e:
        print e
        print "failed to add ", d['msg'].encode('utf-8'), " to ", year

if __name__ == '__main__':
    util.run.main(parse_irc)

