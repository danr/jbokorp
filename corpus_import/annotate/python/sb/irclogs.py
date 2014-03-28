import util
import re
import subprocess

name = []
datename_digit = []
datename_string = []
timename = []
junk = []

# ircname = r"/\A[a-z_\-\[\]\\^{}|`][a-z0-9_\-\[\]\\^{}|`]*\z/i"
ircname = r"\S*"

# Broca: oi le dei velsku
name.append(re.compile(r"^\s?(" + ircname + r"): (.*)$"))

# <Broca> go'i
name.append(re.compile(r"^<\s?(" + ircname + r")> (.*)$"))

# 01 Aug 2003 02:10:18 <carbon> la'o gy. gyrations gy.
datename_string.append(re.compile(r"^(\d{2}) (\S{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) <\s?(" + ircname + r")> (.*)$"))

# 20 Jan 2010 07:21:58  * codrus na'e co'e cusku da poi ve vimcu de noi vo'a jinvi fi ra
# 11 Jun 2008 20:46:50 * durka cu slilu lo stedu
datename_string.append(re.compile(r"^(\d{2}) (\S{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) \s?\* ((" + ircname + r") .*)$"))

# 20 Sep 2010 15:22 < jaupre> no.
datename_string.append(re.compile(r"^(\d{2}) (\S{3}) (\d{4}) (\d{2}):(\d{2}) <\s?(" + ircname + r")> (.*)$"))
# TODO: no seconds!

# 23 Sep 2010 16:09  * rlpowell terpa
datename_string.append(re.compile(r"^(\d{2}) (\S{3}) (\d{4}) (\d{2}):(\d{2}) \s?\* ((" + ircname + r") .*)$"))
# TODO: no seconds!

# 2014-03-28 12:13:11 PDT/-0700 <danr> .u'i
datename_digit.append(re.compile(r"^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}) ...\/..... <\s?(" + ircname + r")> (.*)$"))

# 2014-03-26 13:49:13 PDT/-0700 * durka42 cu nitcu lo nu cliva
datename_digit.append(re.compile(r"^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}) ...\/..... \s?\* ((" + ircname + r") .*)$"))

# [19:39] <Broca> coi zinks
timename.append(re.compile(r"^\[(\d{2}):(\d{2})\] \s?(<" + ircname +r">) (.*)$"))

# [22:06] *** bancus sezgletu
timename.append(re.compile(r"^\[(\d{2}):(\d{2})\] ... \s?((" + ircname +r") .*)$"))

# 19 Jan 2010 20:01:06 -!- vesna [i=4d7c290c@gateway/web/freenode/x-xprmfgfzgrnhorgn] has joined #lojban
junk.append(re.compile(r"^(\d{2}) (\S{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) -!-"))
junk.append(re.compile(r"^(\d{2}) (\S{3}) (\d{4}) (\d{2}):(\d{2}) -!-"))

matchers = sum([name,datename_digit,datename_string,timename,junk],[])

def segment_crude(in_file,out_file):

    with open(in_file) as f:
        lines = f.readlines()
        f.close()

    for l in lines:
        match = False
        for m in matchers:
            if m.search(l):
                match = True
        if not match:
            print l

    # with open(out_file,'w') as f:
    #     f.write(''.join(out))
    #     f.close()

if __name__ == '__main__':
    util.run.main(segment_crude)



