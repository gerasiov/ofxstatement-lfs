VERSION := 0.0.1
SOURCES := $(shell find $(CURDIR) -name '*.py')

.PHONY: all
all: dist

.PHONY: gen
gen: requirements.txt

.PHONY: clean
clean:
	rm -rf dist

.PHONY: dist
dist: dist/ofxstatement-lfs-$(VERSION).tar.gz

.PHONY: install
install: dist/ofxstatement-lfs-$(VERSION).tar.gz
	pip3 install $<

.PHONY: docker
docker: dist
	docker build -t local/ofxstatement-lfs:$(VERSION) .

dist/ofxstatement-lfs-$(VERSION).tar.gz: $(SOURCES) requirements.txt
	python3 setup.py sdist

#
# Naive attempt to freeze the *whole* dependency graph instead of the
# top ones only.
#
requirements.txt: requirements.in
	pip-compile --output-file $@ $<
