PYTHON ?= python3

.PHONY: import-toc import-cd1-index reading-room-example reading-room-package check-second-article test check

import-toc:
	PYTHONPATH=src $(PYTHON) -m maso_archive import-toc

import-cd1-index:
	PYTHONPATH=src $(PYTHON) -m maso_archive import-cd1-index

reading-room-example:
	PYTHONPATH=src $(PYTHON) -m tools.build_reading_room_example

reading-room-package:
	PYTHONPATH=src $(PYTHON) -m tools.build_reading_room_package

check-second-article:
	PYTHONPATH=src $(PYTHON) -m tools.check_cd1_second_article

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

check: test
	git diff --check
