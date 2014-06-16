# Run:
#   make miniclean
#   make wips -B
#   make xmls -B

wips: all_logs.txt
	python -m jk.irclogs --in_file $<

irclogs.zip:
	wget http://www.lojban.org/irclogs/irclogs.zip

all_logs.txt: irclogs.zip
	unzip $<
	touch $@


miniclean:
	rm -f irc*.wip
	rm irclogs.zip

clean:
	rm -f irc*.xml
	rm -f irc*.wip
	rm -f irclogs.zip
	rm -f all_logs.txt

wips = $(wildcard *.wip)

xmls = $(wips:.wip=.xml)

%.xml: %.wip
	if [ ! -e $@ ]; then cp $< $@; fi
	diff $< $@ >/dev/null || cp $< $@

xmls: $(xmls)

.PHONY: miniclean clean xmls wips


