SHELL = /bin/bash

MOSES = $(shell first_existing /opt/moses /home/mmachace/mosesdecoder)
TOKENIZER = $(MOSES)/scripts/tokenizer/tokenizer.perl
LOWERCASE = $(MOSES)/scripts/tokenizer/lowercase.perl
DEESCAPE = $(MOSES)/scripts/tokenizer/deescape-special-chars.perl

.PHONY: all clean

all: tokenized

tokenized: raw
	mkdir -p $@/candidates
	mkdir -p $@/corpus
	for file in $</candidates/* $</reference $</corpus/*.tgt; do \
		new=$$(echo $$file | sed "s|^$</||"); \
		cat $$file \
		  	| $(TOKENIZER) -l cs \
			| $(DEESCAPE) \
			> $@/$$new; \
	done
	for file in $</source $</corpus/*.src; do \
		new=$$(echo $$file | sed "s|^$</||"); \
		cat $$file \
		  	| $(TOKENIZER) -l en \
			| $(DEESCAPE) \
			> $@/$$new; \
	done

normalized-for-ali: tokenized
	mkdir -p $@/candidates
	mkdir -p $@/corpus
	for file in $$(find $< -type f); do \
		new=$$(echo $$file | sed "s|^$</||"); \
		cat $$file \
			| $(MOSES)/scripts/tokenizer/replace-unicode-punctuation.perl \
			| $(LOWERCASE) \
			> $@/$$new; \
	done

clean:
	rm -rf tokenized normalized-for-ali
