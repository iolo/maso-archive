# March 1984 supplementary-source restoration handoff

This is the historical **M01–M04 supplementary campaign**, not whole-issue
restoration completion. The active scope is all 273 March scans under
[PLAN-SCAN-RESTORATION.md](../PLAN-SCAN-RESTORATION.md). The latest accepted result
is [M48, the complete database article](SCAN-RESTORATION-1984-03-M48.md).
March has 24 accepted complete articles and remains active; M49 continues with
the medical-insurance program on 178. Completion and
next-issue statements below describe the superseded supplementary scope.

Completed 2026-11-16 through M01–M04 under
[PLAN-SCAN-RESTORATION.md](../PLAN-SCAN-RESTORATION.md#4-finish-the-pilot-issue-then-expand).
The new native issue is `archive/scans/1984-03/reference/issue-r01/`:
**7,016 files / 1,845,627,186 bytes**, independently reproduced exactly.
All **44 canonical identities** have outcomes: **38 complete article packages**
(`readable`, assistant `sample-reviewed`) and **six non-owning headings**.
Availability, review level and artifact reproducibility remain separate claims.

## What changed

The PDF restoration of **한글 워드 프로세서 프로그램**
(`maso-1984-03-toc-0035`) preserves actual printed **244–249**, ending within
statement **3190**. Printed **250–251** are absent from that PDF; they are present
and legible in the donated JPEGs. Full-page and enlarged region comparison
verified their folios and continuity, the final **4150 GOTO 1330**, and the
separate 터널 통과 게임 opener on 252. Actual 244 and 245 corroborate identity
and the printed routine guide.

M01's immutable JPEG supplement is
`archive/scans/1984-03/packages/word-supplement-r01/`: **28 exact files**, 295
physical rows and 96 visible statement labels (3200–4150), plus the incoming
3190 fragment. Four initial mapped Tesseract tasks were followed by one targeted
crop repair each for three clipped regions. Initial maps and raw attempts remain
preserved; no engine switch or unchanged successful OCR repeat occurred.

M02's selected article revision is
`archive/scans/1984-03/packages/word-complete-r02/`: **136 exact files**. It retains
both original native components unchanged, with six PDF source pages and two
JPEG source views. The same program has **748 physical rows, 316 numbered source
units (1000–4150), 7,240 source tokens, 25 regional text spans and 13 source
qualification occurrences**. The 3190 source boundary and the 3470, 3670 and
3870 column/page boundaries retain their physical source fragments. The original
screen and flowchart remain images, with the literal flowchart caption associated
with its original block. The original diagram/listing overlap remains preserved.

Only the source-supply and segment-boundary limitations are resolved for the
new revision. Historical source errors, uncertain punctuation near 3490, small
marks near 3320, title-string padding, fine jamo forms and other original review
limits remain explicit. Original encoded/control bytes, technical correctness,
program execution and full human proofreading are unverified.

## Preserved sources and covers

The original PDF word-processor package, its ledger's missing-source partial
outcome and the old PDF issue export remain unchanged. The original PDF native
freshly reproduces **95 exact files** using its historical TOC in an isolated
input root. The 37 other selected PDF article packages remain unchanged:
**6,862 files**. They were checked and copied, not counted as fresh native
rebuilds in this supplementary campaign. Their original evidence remains the
basis for source fidelity and local uncertainties.

The separate `archive/scans/1984-03/packages/covers-r01/` contains all four
original cover faces: **11 exact files**, independently rebuilt. Original JPEG
bytes retain the artwork, advertisements, dated spine, torn/worn edges, creases
and stains. Nine selected printed labels were compared with master-derived
crops. Cover advertisement and front-teaser text is not fully transcribed.
The historical front-cover derivative remains in the issue alongside this
separate original cover set; the global cover selection was not changed.

Every one of the **273 JPEG masters** is accounted for in
`supplements/source-selection.json` inside the new issue:

| Selection outcome | Images |
| --- | ---: |
| Selected word-processor continuation | 2 |
| Selected cover faces | 4 |
| Retained subscription/payment-form inserts | 4 |
| Retained separate spine alternative | 1 |
| Other retained supplementary-source images | 262 |

All master hashes were freshly verified during M03. The four form scans remain
intact in their supplied orientations; physical recto/verso pairing remains
unverified. The spine extra remains separate. This targeted pass did not newly
align the 262 unselected page images to PDF pages or classify each at full
resolution. Their original cleanup review and source hashes remain available;
no duplicate-content or missing-body conclusion follows from their selection
status. Filename gaps 11–12 and provisional late-page order remain the cleanup
record, not new claims about physical completeness.

## Reproduce and check

Run these commands from the repository root, choosing fresh output directories.
Required masters, native packages, reviewed inputs and pinned runtime remain in
`archive/`; Git alone does not back them up. No command below runs OCR or builds
a reading room.

```sh
# Regenerate the selected JPEG supplement from its reviewed inputs.
PYTHONPATH=src:. python3 -m tools.pdf_restore.build \
  --recipe archive/scans/1984-03/restoration/supplement-01/word/recipe.json \
  --output work/validation/march-supplement-fresh

# Regenerate the complete native article from both immutable components.
PYTHONPATH=src:. python3 -m tools.pdf_restore.source_revision \
  --recipe archive/scans/1984-03/restoration/revision-01/recipe.json \
  --output work/validation/march-word-fresh
PYTHONPATH=src:. python3 -m tools.pdf_restore.source_revision \
  --check --output work/validation/march-word-fresh

# Regenerate the original cover set.
PYTHONPATH=src:. python3 -m tools.pdf_restore.image_covers \
  --recipe archive/scans/1984-03/restoration/covers-01/cover-recipe.json \
  --output work/validation/march-covers-fresh

# Export and check the complete supplemented issue.
PYTHONPATH=src:. python3 -m tools.pdf_restore.issue \
  --ledger archive/scans/1984-03/restoration/closeout-01/issue-ledger.json \
  --base archive/scans/1984-03/restoration/closeout-01/catalog-input \
  --output work/validation/march-issue-fresh
PYTHONPATH=src:. python3 -m tools.pdf_restore.issue \
  --check --output work/validation/march-issue-fresh
```

The public issue exporter verifies and copies the selected article packages;
it does not rebuild them. The preceding article commands are separate rebuilds.
The historical PDF-native recipe and isolated-root reconstruction are recorded
in `restoration/revision-01/original-pdf-rebuild.json` and its companion script.
The script refuses an existing input root; use a fresh root for a future repeat.

Standalone issue checking uses retained article components, TOC/accounting,
source inventories and cover/source-selection companions. An actual whole-issue
check passed while all original workspace inputs outside the exported issue and
shared schemas were denied to restoration file readers. External reconstruction
and detailed review paths in original components remain historical pins, not
claims that every private review aid is embedded in the issue.

## Validation and next work

The final audit verifies every canonical outcome, exact issue rebuild, unchanged
other article copies, original partial outcomes, source-specific geometry,
cover faces and complete selection accounting. Thirteen damaged actual
canonical/source-companion cases are rejected. M01 rejects 19 damaged supplement
cases, M02 rejects 21 damaged source-revision cases, and M03 rejects 11 damaged
cover/selection cases. All 7,061 initial preservation pins and frozen checkpoint
evidence remain unchanged.

Fresh checks pass **214 PDF tests, 52 image tests, four source-revision tests and
three issue-supplement tests**. The initial issue export rejected historical
compatibility symlink paths. The new ledger projects those paths to their current
physical archive locations with identical manifest hashes; original ledgers and
packages remain unchanged. Failed attempts and earlier revision outputs remain
preserved. Cleanup was preview-only.

This completes March's canonical issue and the plan's targeted supplementary
campaign. Full proofreading, execution, cosmetic reconstruction, additional
JPEG/PDF comparisons, HTML, reading-room integration and deployment remain
separate work. The next full new issue in the chronological scan queue is
**December 1983**; it has not been started by this closeout.

See the [final result](../metadata/catalog/scan-restoration/1984-03-issue.json)
and [progress record](../PROGRESS-SCAN-RESTORATION.md).
