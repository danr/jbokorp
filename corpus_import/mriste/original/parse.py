import email.parser
import re

import sb.util

from sb.islojban import is_lojban

from_re = re.compile("^From ")

if __name__ == "__main__":
    content = open('lojban-9402').read()
    chunk = []
    count = 0
    for l in content.split("\n"):
        if from_re.match(l) and len(chunk) > 0:
            # the content in chunk is now a mail
            mail = email.message_from_string("\n".join(chunk))
            print count
            print mail.get('Date','')
            print mail.get('From','')
            print mail.get('Subject','')

            for x in mail.get_payload().split("\n\n"):
                if is_lojban(x):
                    print x

            chunk = []
            count += 1
        else:
            chunk.append(l)
            
    # test = email.message_from_file(open('lojban-9402'))

