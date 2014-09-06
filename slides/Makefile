all: main.tex
	pdflatex $<
	bibtex main
	pdflatex $<
	pdflatex $<

clean:
	rm -f main.aux main.bbl main.blg main.log main.pdf main.nav main.out main.snm main.toc
