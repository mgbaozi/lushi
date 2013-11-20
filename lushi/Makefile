.PHONY: all
all: packet

.PHONY: packet
packet:
	$(MAKE) -C packet

.PHONY: run
run: all
	python application.py &

.PHONY: clean
clean:
	$(CLEAN) -C packet
	rm -f *.pyc
