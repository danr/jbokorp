corpus = irclogs
original_dir = intermediate
really_original = original
files := $(basename $(notdir $(wildcard $(really_original)/*.xml)))

vrt_columns_annotations = word pos tags info rafsi longrafsi vlatai exp ref dephead deprel
vrt_columns             = word pos tags info rafsi longrafsi vlatai exp ref dephead deprel

vrt_structs_annotations = sentence.id sentence paragraph.n sentence.grammar text.nick text.date text.time text.datefrom text.dateto text.relay
vrt_structs             = sentence:id sentence paragraph   sentence:grammar text:nick text:date text:time text:datefrom text:dateto text:relay

xml_elements    = word  word:tags  word:info  word:ref  word:dephead  word:deprel  msg:nick  msg:date  msg:time  msg:relay  s        s:grammar        p         msg
xml_annotations = token token.tags token.info token.ref token.dephead token.deprel text.nick text.date text.time text.relay sentence sentence.grammar paragraph text

# Using tag word for words

# Using tag s for sentence

# No segmentation for paragraph

parents = token|paragraph token|sentence token|text

custom_common = paragraph sentence pos

dateformat = "%Y-%m-%d"
dateto   = text.date
datefrom = text.date

include ../Makefile.common

include ../Makefile.rules

include ../Makefile.jbo

