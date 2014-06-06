SHELL = /bin/bash

STANFORD_PARSER_DIR = $(shell first_existing /home/machacek/stanford-parser-full-2014-01-04)
MOSES_DIR = $(shell first_existing /opt/moses /home/mmachace/mosesdecoder /a/merkur3/TMP/machacek/statmt/trunk/playground/s.mosesgiza.0907b557.20140227-1940/moses)
TOKENIZER = $(MOSES_DIR)/scripts/tokenizer/tokenizer.perl
LOWERCASE = $(MOSES_DIR)/scripts/tokenizer/lowercase.perl
DEESCAPE = $(MOSES_DIR)/scripts/tokenizer/deescape-special-chars.perl
GIZAWRAPPER = $(shell first_existing /a/merkur3/TMP/machacek/statmt/trunk/scripts/gizawrapper.pl)
GIZABINDIR = $(shell first_existing /a/merkur3/TMP/machacek/statmt/trunk/playground/s.mosesgiza.0907b557.20140227-1940/bin)

.PHONY: all clean

.SECONDARY:


all: extracted.segments

tokenized: raw
	mkdir -p $@/candidates $@/corpus; \
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
	mkdir -p $@/candidates $@/corpus; \
	for file in $$(find $< -type f); do \
		new=$$(echo $$file | sed "s|^$</||"); \
		cat $$file \
			| $(MOSES)/scripts/tokenizer/replace-unicode-punctuation.perl \
			| $(LOWERCASE) \
			> $@/$$new; \
	done
	
	#filter out empty lines from europarl corpus	
	tmp_file=$$(tempfile); \
	paste $@/corpus/europarl.src $@/corpus/europarl.tgt \
		| grep -v  "^	" \
		| grep -v  "	$$" \
		> $$tmp_file && \
	cat $$tmp_file | cut -f1 > $@/corpus/europarl.src && \
	cat $$tmp_file | cut -f2 > $@/corpus/europarl.tgt && \
	rm $$tmp_file


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
		> $@

alignment.filtered: alignment.all
	cat $< | cut '-d	' -f1 > $@

alignments: alignment.filtered
	mkdir -p $@/candidates $@/corpus; \
	./split-from-giza.py $< \
		--change-prefix $@ \
		--splitinfo split.info; \
	rm -rf $@/corpus

source.parsed: tokenized
	java -mx3000m -cp "$(STANFORD_PARSER_DIR)/*:" edu.stanford.nlp.parser.lexparser.LexicalizedParser \
		-tokenized \
	   	-sentences "newline" \
		-escaper "edu.stanford.nlp.process.PTBEscapingProcessor" \
		-outputFormat "penn" \
		edu/stanford/nlp/models/lexparser/englishFactored.ser.gz \
		$</source \
		| tree-collapse \
		> $@

extracted.segments: tokenized alignments source.parsed
	for file in tokenized/candidates/*; do \
		alignment=$$(echo $$file | sed "s/^tokenized/alignments/"); \
		./segmented_tree.py \
			--parsed source.parsed \
			--align $$alignment \
			--target $$file \
			--source tokenized/source \
			--reference tokenized/reference \
			--minlength 3 \
			--maxlength 6; \
	done | sort | uniq > $@

extracted.systems: tokenized alignments source.parsed
	for file in tokenized/candidates/*; do \
		system=$$(basename $$file); \
		alignment=$$(echo $$file | sed "s/^tokenized/alignments/"); \
		./segmented_tree.py \
			--parsed source.parsed \
			--align $$alignment \
			--target $$file \
			--source tokenized/source \
			--reference tokenized/reference \
			--minlength 3 \
			--maxlength 6 \
			--system $$system; \
	done > $@

system.ranks: extracted.systems annotated.segments
	./all-systems-ranks.py \
		--annotated annotated.segments \
		--systems extracted.systems \
		> $@

one-out.ranks: extracted.systems annotated.segments
	./one-out-ranks.py \
		--annotated annotated.segments \
		--systems extracted.systems \
		> $@

		
clean:
	rm -rf extracted.segments source.parsed 

realclean: clean
	rm -rf tokenized normalized-for-ali concatenated.to.align split.info alignment.all alignment.filtered alignments
