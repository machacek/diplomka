SHELL = /bin/bash

MOSES = $(first_existing /opt/moses /home/mmachace/mosesdecoder)
TOKENIZER = $(MOSES)/scripts/tokenizer/tokenizer.perl
NORMALIZEPUNCT = $(MOSES)/scripts/tokenizer/normalize-punctuation.perl
REPLACEUNICODE = $(MOSES)/scripts/tokenizer/replace-unicode-punctuation.perl
LOWERCASE = $(MOSES)/scripts/tokenizer/lowercase.perl

.PHONY: all clean

all:

clean:
	rm -f  
