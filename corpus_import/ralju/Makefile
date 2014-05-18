corpus = ralju
original_dir = intermediate
really_original = original
files := $(basename $(notdir $(wildcard $(really_original)/*.xml)))

vrt_columns_annotations = word pos tags trans ref rafsi longrafsi dephead deprel
vrt_columns             = word pos tags trans ref rafsi longrafsi dephead deprel

vrt_structs_annotations = sentence.id sentence paragraph.n text.date text.title text.author text.original_author text.url text.datefrom text.dateto
vrt_structs             = sentence:id sentence paragraph   text:date text:title text:author text:original_author text:url text:datefrom text:dateto

xml_elements    = word  word:pos  word:tags  word:trans  word:ref  word:dephead  word:deprel  text text:date text:title text:author text:original_author text:url s        p
xml_annotations = token token.pos token.tags token.trans token.ref token.dephead token.deprel text text.date text.title text.author text.original_author text.url sentence paragraph

parents = token|paragraph token|sentence token|text

custom_common = paragraph sentence pos

dateformat = "%Y-%m-%d"
dateto   = text.date
datefrom = text.date

include ../Makefile.common

include ../Makefile.rules

include ../Makefile.jbo

