corpus = tiki
original_dir = intermediate
really_original = chunked
files := $(basename $(notdir $(wildcard $(really_original)/*.xml)))

vrt_columns_annotations = word pos tags trans ref dephead deprel
vrt_columns             = word pos tags trans ref dephead deprel

vrt_structs_annotations = sentence.id sentence paragraph.n text.title 
vrt_structs             = sentence:id sentence paragraph   text:title 

xml_elements    = word  word:pos  word:tags  word:trans  word:ref  word:dephead  word:deprel  text text:title s        p
xml_annotations = token token.pos token.tags token.trans token.ref token.dephead token.deprel text text.title sentence paragraph

parents = token|paragraph token|sentence token|text

custom_common = paragraph sentence pos

include ../Makefile.common

include ../Makefile.rules

include ../Makefile.jbo

