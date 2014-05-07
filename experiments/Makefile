SHELL = /bin/bash

MOSES = $(shell first_existing /opt/moses /home/mmachace/mosesdecoder /a/merkur3/TMP/machacek/statmt/trunk/playground/s.mosesgiza.0907b557.20140227-1940/moses)
TOKENIZER = $(MOSES)/scripts/tokenizer/tokenizer.perl
LOWERCASE = $(MOSES)/scripts/tokenizer/lowercase.perl
DEESCAPE = $(MOSES)/scripts/tokenizer/deescape-special-chars.perl
GIZAWRAPPER = $(shell first_existing /a/merkur3/TMP/machacek/statmt/trunk/scripts/gizawrapper.pl)
GIZABINDIR = $(shell first_existing /a/merkur3/TMP/machacek/statmt/trunk/playground/s.mosesgiza.0907b557.20140227-1940/bin)

.PHONY: all clean

all: concatenated.to.align

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

concatenated.to.align: normalized-for-ali
	candidates=$$(find $</candidates/ -type f | sort); \
	cand_sources=$$(echo "$$candidates" | sed "s|^.*$$|$</source|"); \
	./concat-for-giza.py \
		--sources $</corpus/corpus.src $</corpus/europarl.src $</source    $$cand_sources \
		--targets $</corpus/corpus.tgt $</corpus/europarl.tgt $</reference $$candidates \
		--splitinfo split.info \
		$@

alignment.all: concatenated.to.align
	$(GIZAWRAPPER) $< \
		--lfactors=0 --rfactors=0 \
		--tempdir=/tmp \
		--bindir=$(GIZABINDIR) \
		--dirsym=gdf,revgdf,gdfa,revgdfa,left,right,int,union \
		| cut '-d	' -f1 \
		> $@

clean:
	rm -rf tokenized normalized-for-ali concatenated.to.align split.info
