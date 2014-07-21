SHELL = /bin/bash
.PHONY: all clean

all: main.pdf abstract_cz.pdf abstract_en.pdf

abstract_%.pdf: abstract_%.tex abstract_text_%.tex
	pdflatex $<
   
main.pdf: $(wildcard *.tex)
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex

clean:
	rm -f *.{log,dvi,aux,toc,lof,out,bbl,blg,lot} main.pdf abstract_cz.pdf abstract_en.pdf
