corpus = tiki
original_dir = intermediate
really_original = chunked
files := $(basename $(notdir $(wildcard $(really_original)/*.xml)))

vrt_columns_annotations = word pos tags trans ref dephead
vrt_columns             = word pos tags trans ref dephead

vrt_structs_annotations = sentence.id sentence paragraph.n text.date text.title text.author text.original_author text.url text.datefrom text.dateto
vrt_structs             = sentence:id sentence paragraph   text:date text:title text:author text:original_author text:url text:datefrom text:dateto

xml_elements    = word  word:pos  word:tags  word:trans  word:ref  word:dephead  text text:date text:title text:author text:original_author text:url s        p
xml_annotations = token token.pos token.tags token.trans token.ref token.dephead text text.date text.title text.author text.original_author text.url sentence paragraph

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

define segment_rule
$(root)$(original_dir)/$(1).tk.xml: $(root)$(really_original)/$(1).xml
	mkdir -p $(root)$(original_dir)
	python -m sb.segment_crude --in_file $$(1) --out_file $$@ --cmd segment

$(root)$(original_dir)/$(1).xml: $(root)$(original_dir)/$(1).tk.xml
	mkdir -p $(root)$(original_dir)
	python -m sb.segment_crude --in_file $$(1) --out_file $$@ --cmd parse
endef

$(foreach file,$(files),$(eval $(call segment_rule,$(file))))

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
