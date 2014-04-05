ANNOUNCE: Beta-version of a new Lojban corpus search system

ju'i jbopli

I have made a new Lojban corpus searching system.  The idea is to enhance the study of the usage and development of the language.  The search tool supports, apart from searching for a single word, also searching for selma'o, place structures of bridi, seltau, date, irc nick, and more. 

Good old jbofi'e has attempted to parse all sentences, and its terbri information is extracted from successful parses. When the parse fails, cmafi'e is used for word segmentation and selma'o-tagging.

The system is kindly hosted by durka at:

https://www.alexburka.com/~danr

Here are some examples of what you can do with the extended search:
(Please be patient when clicking the links, it takes a little while to render the pages.)

Searching for usages of traji3:
https://www.alexburka.com/~danr/#?stats_reduce=word&cqp=%5Btags%20_%3D%20%22traji3%22%5D&search_tab=1&within=sentence&hpp=100&search=cqp

Please note that you can click on the words in the search results to get more information in the right-hand side sidebar.

Searching for self-greetings, COI + mi:
https://www.alexburka.com/~danr/#?cqp=%5Bpos%20%3D%20%22COI%22%5D%20%5Bword%20%3D%20%22mi%22%5D&stats_reduce=word&search_tab=1&within=sentence&search=cqp

Searching for irc messages authored by Robin:
https://www.alexburka.com/~danr/#?stats_reduce=word&cqp=%5B_.text_nick%20%3D%20%22rlpowell%22%20%26%20lbound(sentence)%5D&search_tab=1&within=sentence&search=cqp&page=855

Usages of pi'o as terminal rafsi (or zi'evla):
https://www.alexburka.com/~danr/#?stats_reduce=word&cqp=%5Bword%20%26%3D%20%22pi'o%22%20%26%20pos%20%3D%20%22BRIVLA%22%5D&search_tab=1&within=sentence&search=cqp

Examples of statistics:

Statistics of lo + BRIVLA:
https://www.alexburka.com/~danr/#?cqp=%5Bword%20%3D%20%22lo%22%5D%20%5Bpos%20%3D%20%22BRIVLA%22%5D&stats_reduce=word&search_tab=1&within=sentence&search=cqp&result_tab=1

The most common seltau (the info is set to "end with q"):
https://www.alexburka.com/~danr/#?cqp=%5Btrans%20%26%3D%20%22q%22%5D&search_tab=1&within=sentence&page=0&search=cqp&stats_reduce=word&result_tab=1

Popular selbri in gadri (info ends with n):
https://www.alexburka.com/~danr/#?cqp=%5Btrans%20%26%3D%20%22n%22%5D&search_tab=1&within=sentence&page=0&search=cqp&result_tab=1

There is also a comparison mode, which requires you to save to searches, by pressing the down arrow next to the search button. Then you can search for statistically significant differences between them. Try yourself by comparing used words without vs with only the irc corpus!

The system is an adaptation of the Swedish corpora search system Korp:
http://spraakbanken.gu.se/korp
If you are interested to help out, please do contact me.

Happy exploring!

mi'e .danr. ko banli mu'o
