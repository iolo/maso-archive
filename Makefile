PYTHON ?= python3

.PHONY: import-toc import-cd1-index reading-room-example reading-room-package check-second-article prepare-cd1-interview prepare-cd1-editor prepare-cd1-graphics prepare-cd1-keyboard close-cd1-february prepare-cd1-issue inventory-cd1-sources inventory-cd1-processing batch-cd1 validate-cd1-batch run-cd1-full-pass report-cd1-full-pass review-cd1-associations retry-cd1-association-sample review-cd1-fonts retry-cd1-font-sample run-cd1-font-pass report-cd1-font-pass run-cd1-association-pass report-cd1-association-pass audit-cd1-issue restore-toc-snapshot prepare-cd1-transfer test check

import-toc:
	PYTHONPATH=src $(PYTHON) -m maso_archive import-toc

restore-toc-snapshot:
	PYTHONPATH=src $(PYTHON) -m tools.toc_snapshot

import-cd1-index:
	PYTHONPATH=src $(PYTHON) -m maso_archive import-cd1-index

reading-room-example:
	PYTHONPATH=src $(PYTHON) -m tools.build_reading_room_example

reading-room-package:
	PYTHONPATH=src $(PYTHON) -m tools.build_reading_room_package

check-second-article:
	PYTHONPATH=src $(PYTHON) -m tools.check_cd1_second_article

prepare-cd1-interview:
	PYTHONPATH=src $(PYTHON) -m tools.prepare_cd1_interview

prepare-cd1-editor:
	PYTHONPATH=src $(PYTHON) -m tools.prepare_cd1_editor

prepare-cd1-graphics:
	PYTHONPATH=src $(PYTHON) -m tools.prepare_cd1_graphics

prepare-cd1-keyboard:
	PYTHONPATH=src $(PYTHON) -m tools.prepare_cd1_keyboard

close-cd1-february:
	PYTHONPATH=src $(PYTHON) -m tools.close_cd1_february

prepare-cd1-issue:
	PYTHONPATH=src $(PYTHON) -m tools.prepare_cd1_issue

run-cd1-association-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.association_pass

report-cd1-association-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.association_coverage $(REPORT_ARGS)

review-cd1-associations:
	PYTHONPATH=src $(PYTHON) -m tools.batch.associations $(ASSOCIATION_ARGS)

retry-cd1-association-sample:
	PYTHONPATH=src $(PYTHON) -m tools.batch.retry_associations $(ASSOCIATION_ARGS)

report-cd1-full-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.report $(REPORT_ARGS)

run-cd1-full-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.full_pass

validate-cd1-batch:
	PYTHONPATH=src $(PYTHON) -m tools.validate_cd1_batch $(VALIDATION_ARGS)

batch-cd1:
	PYTHONPATH=src $(PYTHON) -m tools.run_cd1_batch $(BATCH_ARGS)

inventory-cd1-processing:
	PYTHONPATH=src $(PYTHON) -m tools.inventory_cd1_processing

inventory-cd1-sources:
	$(PYTHON) -m tools.inventory_cd1_sources

prepare-cd1-transfer:
	PYTHONPATH=src $(PYTHON) -m tools.prepare_cd1_transfer

audit-cd1-issue:
	PYTHONPATH=src $(PYTHON) -m tools.audit_cd1_issue

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

check: test
	git diff --check

review-cd1-fonts:
	PYTHONPATH=src $(PYTHON) -m tools.batch.font_review $(FONT_ARGS)

retry-cd1-font-sample:
	PYTHONPATH=src $(PYTHON) -m tools.batch.retry_fonts $(FONT_ARGS)

run-cd1-font-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.font_pass

report-cd1-font-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.font_coverage $(REPORT_ARGS)

.PHONY: review-cd1-ordinary-fonts retry-cd1-ordinary-font-sample
review-cd1-ordinary-fonts:
	PYTHONPATH=src $(PYTHON) -m tools.batch.ordinary_font_review $(FONT_ARGS)

retry-cd1-ordinary-font-sample:
	PYTHONPATH=src $(PYTHON) -m tools.batch.retry_ordinary_fonts $(FONT_ARGS)

.PHONY: run-cd1-ordinary-font-pass report-cd1-ordinary-font-pass
run-cd1-ordinary-font-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.ordinary_font_pass

report-cd1-ordinary-font-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.ordinary_font_coverage $(REPORT_ARGS)

.PHONY: review-cd1-font-declarations retry-cd1-font-declaration-sample
review-cd1-font-declarations:
	PYTHONPATH=src $(PYTHON) -m tools.batch.font_declaration_review $(FONT_ARGS)

retry-cd1-font-declaration-sample:
	PYTHONPATH=src $(PYTHON) -m tools.batch.retry_font_declarations $(FONT_ARGS)

.PHONY: run-cd1-font-declaration-pass report-cd1-font-declaration-pass
run-cd1-font-declaration-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.font_declaration_pass

report-cd1-font-declaration-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.font_declaration_coverage $(REPORT_ARGS)

.PHONY: review-cd1-symbols retry-cd1-symbol-sample
review-cd1-symbols:
	PYTHONPATH=src $(PYTHON) -m tools.batch.symbol_review $(FONT_ARGS)

retry-cd1-symbol-sample:
	PYTHONPATH=src $(PYTHON) -m tools.batch.retry_symbol_sample $(FONT_ARGS)

.PHONY: retry-cd1-symbol-arrows
retry-cd1-symbol-arrows:
	PYTHONPATH=src $(PYTHON) -m tools.batch.retry_symbol_arrows $(FONT_ARGS)

.PHONY: run-cd1-symbol-pass report-cd1-symbol-pass
run-cd1-symbol-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.symbol_pass

report-cd1-symbol-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.symbol_coverage $(REPORT_ARGS)

.PHONY: review-cd1-codecs retry-cd1-oem-sample
review-cd1-codecs:
	PYTHONPATH=src $(PYTHON) -m tools.batch.codec_review $(FONT_ARGS)

retry-cd1-oem-sample:
	PYTHONPATH=src $(PYTHON) -m tools.batch.retry_oem_sample $(FONT_ARGS)

.PHONY: run-cd1-oem-pass report-cd1-oem-pass
run-cd1-oem-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.oem_pass

report-cd1-oem-pass:
	PYTHONPATH=src $(PYTHON) -m tools.batch.oem_coverage $(REPORT_ARGS)

.PHONY: export-cd1-reference check-cd1-reference
export-cd1-reference:
	PYTHONPATH=src $(PYTHON) -m tools.reference.export $(REFERENCE_ARGS)

check-cd1-reference:
	PYTHONPATH=src $(PYTHON) -m tools.reference.check

.PHONY: export-reading-room demo-reading-room build-reading-room check-reading-room test-reading-room
export-reading-room:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.export

demo-reading-room:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.export --demo
	cd web && READING_ROOM_OUTPUT=build/reading-room-demo npm run build

build-reading-room:
	cd web && npm run build

check-reading-room:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.check

test-reading-room:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -p test_reading_room_web_export.py -v
	cd web && npm test && npm run build

.PHONY: inventory-cd2-sources map-cd2-candidates build-cd2-reference check-cd2-reference
inventory-cd2-sources:
	$(PYTHON) -m tools.inventory_cd2_sources

map-cd2-candidates:
	$(PYTHON) -m tools.map_cd2_candidates

build-cd2-reference:
	$(PYTHON) -m tools.build_cd2_reference --all $(CD2_ARGS)

check-cd2-reference:
	$(PYTHON) -m tools.verify_cd2_reference

.PHONY: inventory-cd3-sources map-cd3-candidates build-cd3-reference check-cd3-reference
inventory-cd3-sources:
	$(PYTHON) -m tools.inventory_cd3_sources

map-cd3-candidates:
	$(PYTHON) -m tools.map_cd3_candidates

build-cd3-reference:
	$(PYTHON) -m tools.build_cd3_reference --all $(CD3_ARGS)

check-cd3-reference:
	$(PYTHON) -m tools.verify_cd3_reference
