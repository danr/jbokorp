corpus = ca_pa_djedi
original_dir = original
files := $(basename $(notdir $(wildcard $(original_dir)/*.xml)))

vrt_columns_annotations = word pos tags trans
vrt_columns             = word pos tags trans

vrt_structs_annotations = sentence.id sentence paragraph.n
vrt_structs             = sentence:id sentence paragraph

xml_elements    = word  word:pos  word:tags  word:trans  text
xml_annotations = token token.pos token.tags token.trans text

# Using tag word for words

# Using tag s for sentence

# No segmentation for paragraph

parents = token|paragraph token|sentence

custom_common = paragraph sentence pos

include ../Makefile.common

include ../Makefile.rules

%.paragraph : %.token.n %.token.pos
	$(python) -m sb.pos_segment --pos_segment --out $@ --text $(1) --pos $(2) --delimiter NIhO --element paragraph

%.sentence: %.token.n %.token.pos
	$(python) -m sb.pos_segment --pos_segment --out $@ --text $(1) --pos $(2) --delimiter "I|NIhO" --element sentence


## vrt_columns_annotations = word trans tags
## vrt_columns             = word trans tags
## vrt_structs_annotations = sentence paragraph.n
## vrt_structs             = sentence paragraph
##
## xml_elements    = text word word:trans word:tags s        p
## xml_annotations = text word word.trans word.tags sentence paragraph
## xml_skip        =
##
## include ../Makefile.common
##
## token_chunk =
## token_segmenter =
##
## sentence_chunk =
## sentence_segmenter =
## sentence_model = $(punkt_model)
##
## paragraph_chunk =
## paragraph_segmenter =
##
## custom_common = sentence paragraph word
##
## parents = token|word token|word.trans token|word.tags
## chain   = token.word token.word.trans token.word.tags
##
## ################################################################################
## #                                  RULES                                       #
## ################################################################################
##
## include ../Makefile.rules
