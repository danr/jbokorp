
tatoeba.xml: sentences_detailed.csv links.csv
	python bregau.py > tatoeba.xml

sentences_detailed.csv:
	wget http://tatoeba.org/files/downloads/sentences_detailed.csv

links.csv:
	wget http://tatoeba.org/files/downloads/links.csv
