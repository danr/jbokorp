

irclogs.zip:
	wget http://www.lojban.org/irclogs/irclogs.zip

all_logs.txt: irclogs.zip
	unzip $<
	touch $@

irc0.xml: all_logs.txt
	python -m sb.irclogs --in_file $< --out_prefix irc

miniclean:
	rm -f irc*.xml

clean:
	rm -f irc*.xml
	rm -f irclogs.zip
	rm -f all_logs.txt


.PHONY: miniclean clean


