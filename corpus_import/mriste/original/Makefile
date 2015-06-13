sources = $(wildcard *.mail)

all: $(sources:.mail=.xml)

%.xml: %.mail
	python -m jk.maillist --fname $< > $@
