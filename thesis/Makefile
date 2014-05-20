.PHONY: all clean

all: main.pdf
   
main.pdf: $(wildcard *.tex)
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex

clean:
	rm -f *.{log,dvi,aux,toc,lof,out} main.pdf
