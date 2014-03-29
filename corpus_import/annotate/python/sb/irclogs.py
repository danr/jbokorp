from xml.sax.saxutils import escape
import util
import re
import subprocess

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

INFINITY = 987654321
MSGS_PER_FILE = 10000

def parse_irc(in_file, out_prefix):

    with open(in_file) as g:
        lines = g.readlines()
        g.close()

    printed = INFINITY;
    num = 0

    f = None

    for l in lines:
        for m in matchers:
            d = m.match(l)
            if d is not None:
                d = d.groupdict()
                if d.get('msg'):

                    if d.get('pretty_month'):
                        d['month'] = "%02d" % months[d['pretty_month']]

                    y, m, day = d.get('year'), d.get('month'), d.get('day')

                    date = None
                    if y and m and day:
                        date = y + "-" + m + "-" + day

                    if not d.get('sec'):
                        d['sec'] = "00"

                    hh, mm, ss = d.get('hour'), d.get('min'), d.get('sec')

                    time = None
                    if hh and mm and ss:
                        time = hh + ":" + mm + ":" + ss

                    out = "<msg "
                    if date:
                        out += 'date="' + date + '" '

                    if time:
                        out += 'time="' + time + '" '

                    out += 'nick="' + d["nick"] + '">'

                    if printed > MSGS_PER_FILE:
                        printed = 0
                        if f is not None:
                            f.write("</text>\n")
                            f.close()
                        f = open(out_prefix + str(num) + ".xml",'w')
                        f.write("<text>\n")
                        num += 1
                    else:
                        printed += 1

                    f.write(out + "\n")
                    f.write(escape(d["msg"]) + "\n")
                    f.write("</msg>\n")

    if f is not None:
        f.write("</text>\n")
        f.close()

if __name__ == '__main__':
    util.run.main(parse_irc)



