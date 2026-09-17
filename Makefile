PYTHON ?= python3

.PHONY: import-toc import-cd1-index test check

import-toc:
	PYTHONPATH=src $(PYTHON) -m maso_archive import-toc

import-cd1-index:
	PYTHONPATH=src $(PYTHON) -m maso_archive import-cd1-index

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

check: test
	git diff --check
