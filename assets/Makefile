GVS := $(wildcard *.gv)
SVGS := $(patsubst %.gv,%.svg,$(GVS))
PNGS := $(patsubst %.gv,%.png,$(GVS))

all: $(GVS) $(PNGS)

%.svg: %.gv
	dot $< -Tsvg > $@

clean-svg:
	rm -- *.svg

%.png: %.gv
	dot $< -Tpng -Gdpi=72 > $@

clean-png:
	rm -- *.svg

%.gv: Makefile.helpers/diagrams.py Makefile.helpers/diagrams.gv
	python $+ $@

Makefile.helpers/diagrams.gv:
	@


.PHONY: all clean-png clean-svg
