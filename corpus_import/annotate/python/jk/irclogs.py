from xml.sax.saxutils import escape
import lxml.etree as ET
import sb.util as util
import re
import subprocess
from unidecode import unidecode

matchers = []

# ircname = r"/\A[a-z_\-\[\]\\^{}|`][a-z0-9_\-\[\]\\^{}|`]*\z/i"
ircname = r"\S*"

# Broca: oi le dei velsku
matchers.append(re.compile(r"^\s?(?P<nick>" + ircname + r"): (?P<msg>.*)$"))

# <Broca> go'i
matchers.append(re.compile(r"^<\s?(?P<nick>" + ircname + r")> (?P<msg>.*)$"))

# 01 Aug 2003 02:10:18
pretty_full_date = r"(?P<day>\d{2}) (?P<pretty_month>\S{3}) (?P<year>\d{4}) (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})"

# 01 Aug 2003 02:10
pretty_mini_date = r"(?P<day>\d{2}) (?P<pretty_month>\S{3}) (?P<year>\d{4}) (?P<hour>\d{2}):(?P<min>\d{2})"

# 2014-03-28 12:13:11 PDT/-0700
digit_date = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2}) ...\/....."

# [19:39]
brack_time = r"\[(?P<hour>\d{2}):(?P<min>\d{2})\]"

# 01 Aug 2003 02:10:18 <carbon> la'o gy. gyrations gy.
matchers.append(re.compile(r"^" + pretty_full_date + r" <\s?(?P<nick>" + ircname + r")> (?P<msg>.*)$"))

# 20 Sep 2010 15:22 < jaupre> no.
matchers.append(re.compile(r"^" + pretty_mini_date + r" <\s?(?P<nick>" + ircname + r")> (?P<msg>.*)$"))

# 20 Jan 2010 07:21:58  * codrus na'e co'e cusku da poi ve vimcu de noi vo'a jinvi fi ra
# 11 Jun 2008 20:46:50 * durka cu slilu lo stedu
matchers.append(re.compile(r"^" + pretty_full_date + r" \s?\* (?P<msg> (?P<nick>" + ircname + r") .*)$"))

# 23 Sep 2010 16:09  * rlpowell terpa
matchers.append(re.compile(r"^" + pretty_mini_date + r" \s?\* (?P<msg> (?P<nick>" + ircname + r") .*)$"))


# 2014-03-28 12:13:11 PDT/-0700 <danr> .u'i
matchers.append(re.compile(r"^" + digit_date + r" <\s?(?P<nick>" + ircname + r")> (?P<msg>.*)$"))

# 2014-03-26 13:49:13 PDT/-0700 * durka42 cu nitcu lo nu cliva
matchers.append(re.compile(r"^" + digit_date + r" \s?\* (?P<msg> (?P<nick>" + ircname + r") .*)$"))

# [19:39] <Broca> coi zinks
matchers.append(re.compile(r"^" + brack_time + r" \s?\* (?P<msg> (?P<nick>" + ircname + r") .*)$"))

# [22:06] *** bancus sezgletu
matchers.append(re.compile(r"^" + brack_time + r" \s?\*\*\* \s?(?P<msg> (?P<nick>" + ircname + r") .*)$"))

# 19 Jan 2010 20:01:06 -!- vesna [i=4d7c290c@gateway/web/freenode/x-xprmfgfzgrnhorgn] has joined #lojban
matchers.append(re.compile(r"^" + pretty_full_date + r" -!-"))
matchers.append(re.compile(r"^" + pretty_mini_date + r" -!-"))

months = dict(zip(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],range(1,13)))

MSGS_PER_FILE = 10000

written = {}
store   = {}
items   = {}

def banned(nick):
    return nick == "livla" or nick == "mensi"

def add_msg(d):
    year = d.get('year', "undef")
    if not year in store:
        store[year] = ET.Element('text')
    root = store[year]
    try:
        msg = ET.SubElement(root, 'msg',
            date=d.get('date',''),
            time=d.get('time',''),
            nick=d['nick'])
        msg.text = unicode(unidecode(d['msg']))
        items[year] = items.get(year, 0) + 1
    except:
        # print "failed to add ", d['msg'], " to ", year
        pass

def write_cycle(limit=MSGS_PER_FILE):
    kill = []
    for year, amt in items.iteritems():
        if amt > limit:
            written[year] = written.get(year, -1) + 1
            fname = "irc" + year + "-" + str(written[year]) + ".wip"
            with open(fname, "w") as f:
                f.write(ET.tostring(store[year], pretty_print = True))
            print "wrote", fname
            kill.append(year)
    for year in kill:
        items.pop(year, None)
        store.pop(year, None)

def parse_irc(in_file):

    for l in open(in_file).readlines():
        for m in matchers:
            d = m.match(l)
            if d is not None:
                d = d.groupdict()
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

                    add_msg(d)
                    write_cycle()
    write_cycle(0)

if __name__ == '__main__':
    util.run.main(parse_irc)

