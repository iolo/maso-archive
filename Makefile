PYTHON ?= python3

.PHONY: import-toc test check

import-toc:
	PYTHONPATH=src $(PYTHON) -m maso_archive import-toc

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

check: test
	git diff --check
