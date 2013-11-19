export CLEAN = make clean
MAKEFLAGS = -w
.PHONY: all
all: lushi

.PHONY: lushi
lushi:
	$(MAKE) -C lushi

.PHONY: run
run: lushi
	$(MAKE) run -C lushi

.PHONY: clean
clean:
	$(CLEAN) -C lushi
