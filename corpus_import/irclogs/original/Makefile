

irclogs.zip:
	wget http://www.lojban.org/irclogs/irclogs.zip

all_logs.txt: irclogs.zip
	unzip $<
	touch $@

irc.xml: all_logs.txt
	python -m sb.irclogs --in_file $< > $@

