PYTHON ?= python3

.PHONY: ocr-qwen3-vl benchmark-ocr-qwen3-vl test-ocr-qwen3-vl
ocr-qwen3-vl:
	PYTHONPATH=src $(PYTHON) -m tools.ocr_qwen page $(OCR_QWEN_ARGS)

benchmark-ocr-qwen3-vl:
	PYTHONPATH=src $(PYTHON) -m tools.ocr_qwen benchmark $(OCR_QWEN_ARGS)

test-ocr-qwen3-vl:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -p 'test_ocr_*.py' -v

.PHONY: inventory-tocs normalize-tocs ocr-tocs compare-tocs prepare-toc-images
inventory-tocs:
	PYTHONPATH=src $(PYTHON) -m tools.toc_restore inventory $(TOC_ARGS)

normalize-tocs:
	PYTHONPATH=src $(PYTHON) -m tools.toc_restore normalize $(TOC_ARGS)

ocr-tocs:
	PYTHONPATH=src $(PYTHON) -m tools.toc_restore ocr $(TOC_ARGS)

compare-tocs:
	PYTHONPATH=src $(PYTHON) -m tools.toc_restore compare $(TOC_ARGS)

prepare-toc-images:
	PYTHONPATH=src $(PYTHON) -m tools.toc_restore prepare $(TOC_ARGS)

PDF_RECIPE ?= archive/pdf/shared/restoration/pilot/package-recipe.json
PDF_OUTPUT ?= archive/pdf/shared/packages/pilot
PDF_COMPARISON_RECIPE ?= archive/pdf/shared/restoration/7-cd-comparison/comparison-recipe.json
PDF_COMPARISON_OUTPUT ?= archive/pdf/shared/packages/7-cd-comparison

.PHONY: inventory-pdf prepare-pdf-covers install-pdf-covers build-pdf-article check-pdf-article test-pdf
inventory-pdf:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.inventory $(PDF_ARGS)

prepare-pdf-covers:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.covers prepare

install-pdf-covers:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.covers install

build-pdf-article:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.build --recipe $(PDF_RECIPE) --output $(PDF_OUTPUT)

check-pdf-article:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.build --check --output $(PDF_OUTPUT)

.PHONY: assemble-pdf-article
assemble-pdf-article:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.assemble --recipe $(PDF_RECIPE) --output $(PDF_OUTPUT)

test-pdf:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -p 'test_pdf_*.py' -v

.PHONY: compare-pdf-cd check-pdf-comparison
compare-pdf-cd:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.compare --recipe $(PDF_COMPARISON_RECIPE) --output $(PDF_COMPARISON_OUTPUT)

check-pdf-comparison:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.compare --check --output $(PDF_COMPARISON_OUTPUT)

.PHONY: export-pdf-reader
export-pdf-reader:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.scan $(PDF_READER_ARGS)

.PHONY: export-pdf-issue export-pdf-issue-reader
export-pdf-issue:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.issue $(PDF_ISSUE_ARGS)

export-pdf-issue-reader:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.scan_issue $(PDF_ISSUE_ARGS)

PDF_BATCH_STATE ?= archive/pdf/shared/restoration/10-batch/state
PDF_BATCH_REQUEST ?= archive/pdf/shared/restoration/10-batch/request.json
PDF_BATCH_OUTPUT ?= archive/pdf/shared/packages/10-batch
.PHONY: prepare-pdf-batch resume-pdf-batch export-pdf-batch check-pdf-batch
prepare-pdf-batch:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.batch prepare --request $(PDF_BATCH_REQUEST) --state $(PDF_BATCH_STATE) $(PDF_BATCH_ARGS)

resume-pdf-batch:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.batch resume --state $(PDF_BATCH_STATE) $(PDF_BATCH_ARGS)

export-pdf-batch:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.batch export --state $(PDF_BATCH_STATE) --output $(PDF_BATCH_OUTPUT)

check-pdf-batch:
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.batch check --state $(PDF_BATCH_STATE)
	PYTHONPATH=src $(PYTHON) -m tools.pdf_restore.batch check --output $(PDF_BATCH_OUTPUT)

.PHONY: import-toc import-cd1-index reading-room-example reading-room-package check-second-article prepare-cd1-interview prepare-cd1-editor prepare-cd1-graphics prepare-cd1-keyboard close-cd1-february prepare-cd1-issue inventory-cd1-sources inventory-cd1-processing batch-cd1 validate-cd1-batch run-cd1-full-pass report-cd1-full-pass review-cd1-associations retry-cd1-association-sample review-cd1-fonts retry-cd1-font-sample run-cd1-font-pass report-cd1-font-pass run-cd1-association-pass report-cd1-association-pass audit-cd1-issue restore-toc-snapshot prepare-cd1-transfer test check

import-toc:
	PYTHONPATH=src $(PYTHON) -m maso_archive import-toc

restore-toc-snapshot:
	PYTHONPATH=src $(PYTHON) -m tools.toc_snapshot

import-cd1-index:
	PYTHONPATH=src $(PYTHON) -m maso_archive import-cd1-index

reading-room-example:
	PYTHONPATH=src $(PYTHON) -m tools.build_reading_room_example

# Adapt output locations without changing these historical, hash-pinned tools.
reading-room-package:
	PYTHONPATH=src $(PYTHON) -c 'from tools import build_reading_room_package as tool; from maso_archive.storage import canonical_path; tool.OUTPUT = canonical_path(tool.OUTPUT); raise SystemExit(tool.main())'

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
	PYTHONPATH=src $(PYTHON) -c 'from tools import inventory_cd1_processing as tool; from maso_archive.storage import canonical_path; tool.OUTPUT = canonical_path(tool.OUTPUT); raise SystemExit(tool.main())'

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

.PHONY: prepare-cover-thumbnails cleanup-legacy-covers
prepare-cover-thumbnails:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.covers prepare $(COVER_ARGS)

cleanup-legacy-covers:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.covers cleanup $(COVER_ARGS)

.PHONY: export-reading-room demo-reading-room build-reading-room check-reading-room test-reading-room
export-reading-room:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.export --all-discs $(READING_ROOM_ARGS)

demo-reading-room:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.export --demo
	cd web && READING_ROOM_OUTPUT=dist/reading-room-demo npm run build

build-reading-room:
	cd web && npm run build

check-reading-room:
	PYTHONPATH=src $(PYTHON) -m tools.reading_room.check --require-thumbnails

test-reading-room:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -p 'test_reading_room*.py' -v
	cd web && npm test && npm run build -- --outDir ../work/validation/reading-room-ui

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

# Unified volunteer reader. Preserve release snapshots under archive/releases/.
VOLUNTEER_OUTPUT ?= dist/reading-room
VOLUNTEER_BASE ?= ./
VOLUNTEER_PORT ?= 4189
VOLUNTEER_INPUT ?= archive/releases/reading-room-2026-10-16/data
VOLUNTEER_LEDGER ?= archive/pdf/1984-09/evidence/reader-integration-2026-10-16/export-ledger-r02.json
VOLUNTEER_RELEASE ?= reading-room-2026-10-16-september
.PHONY: export-volunteer-reading-room build-volunteer-reading-room check-volunteer-reading-room preview-volunteer-reading-room
export-volunteer-reading-room:
	PYTHONPATH=src:. $(PYTHON) -m tools.reading_room.volunteer export --base $(VOLUNTEER_INPUT) --ledger $(VOLUNTEER_LEDGER) --data $(VOLUNTEER_OUTPUT)/data

build-volunteer-reading-room:
	cd web && READING_ROOM_OUTPUT=$(VOLUNTEER_OUTPUT) READING_ROOM_BASE=$(VOLUNTEER_BASE) npm run build

check-volunteer-reading-room:
	PYTHONPATH=src:. $(PYTHON) -m tools.reading_room.volunteer check --data $(VOLUNTEER_OUTPUT)/data

preview-volunteer-reading-room:
	cd web && READING_ROOM_OUTPUT=$(VOLUNTEER_OUTPUT) READING_ROOM_BASE=$(VOLUNTEER_BASE) npm run preview -- --port $(VOLUNTEER_PORT) --strictPort

# Keep historical recipe paths usable after restoring the local archive.
.PHONY: init-storage check-storage restore-volunteer-reading-room
init-storage:
	$(PYTHON) -m tools.storage_layout compat

check-storage:
	$(PYTHON) -m tools.storage_layout verify

restore-volunteer-reading-room:
	$(PYTHON) -m tools.storage_layout restore-reader $(VOLUNTEER_OUTPUT) --release $(VOLUNTEER_RELEASE)
