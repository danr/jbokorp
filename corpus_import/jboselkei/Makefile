corpus = jboselkei
original_dir = intermediate
really_original = original
files := $(basename $(notdir $(wildcard $(really_original)/*.xml)))

vrt_columns_annotations = word pos tags trans rafsi longrafsi vlatai exp ref dephead deprel
vrt_columns             = word pos tags trans rafsi longrafsi vlatai exp ref dephead deprel

vrt_structs_annotations = sentence.id sentence paragraph.n text.author text.date text.datefrom text.dateto text.difficulty text.comment text.time text.value text.reviews text.source text.sourceauthor text.sourceid text.sourcelang text.sourcecomment
vrt_structs             = sentence:id sentence paragraph   text:author text:date text:datefrom text:dateto text:difficulty text:comment text:time text:value text:reviews text:source text:sourceauthor text:sourceid text:sourcelang text:sourcecomment

xml_elements    = word  word:pos  word:tags  word:trans  word:ref  word:dephead  word:deprel  msg:author  msg:date  msg:difficulty  msg:comment  msg:time  msg:value  msg:reviews  msg:source  msg:sourceauthor  msg:sourceid  msg:sourcelang  msg:sourcecomment s        p         msg
xml_annotations = token token.pos token.tags token.trans token.ref token.dephead token.deprel text.author text.date text.difficulty text.comment text.time text.value text.reviews text.source text.sourceauthor text.sourceid text.sourcelang text.sourcecomment sentence paragraph text

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

