# Successor notes — 2026-09-26

The owner has asked to stop here and leave future work to a successor. No new
extraction, viewer implementation or recovery pass is in progress. Wait for the
owner's next direction before starting another workstream.

## Start here

- Completed deliverable: `build/cd1-reference/index.html`, opened directly in a
  browser. Source/tooling commit: `6fc15db`.
- Read [the reference guide](CD1-READABLE-REFERENCE.md), then the current status in
  [PLAN-CD1](../PLAN-CD1.md). [PROGRESS](../PROGRESS.md) contains historical evidence;
  older checkpoint requirements should not override the owner's later priorities.
- The current export has 1,080 article texts across 72 CD1 issues: 1,047 without
  marked decoding gaps and 33 with localized gaps. It includes 3,125 listing/text
  downloads, 4,979 viewable images and 1,111 deferred images with original links.
  Eight candidates have unresolved article boundaries/source attribution. Historical
  records sometimes call these "ownership" blockers; this is content assignment,
  not proof of legal ownership or a user-access requirement.
- The old 19b baseline of 995 prepared packages is preserved. Step 20 provides
  additional readable references from all 85 previously failed candidates; it does
  not rewrite their historical processing outcomes.

## What matters to the owner

Paper magazines are authoritative. The CDs are a convenient secondary transcription
for reading and comparison with later paper OCR, especially source code. CD and TOC
data were edited by different people; inconsistent formatting and metadata are
expected. The owner will revalidate restored material against paper.

Preserve readable text, code characters and whitespace, useful structure, images,
source evidence and explicit uncertainty. Exact fonts, margins, justification and
original-viewer appearance are not acceptance gates. Do not reopen cosmetic RTF
investigations simply to remove every exception. Do not guess uncertain code or
silently replace OCR with CD text. Broken images may stay deferred with records.

The project spent too long on technical fidelity before delivering something
usable. Prefer a concrete improvement that helps reading or paper restoration,
with a clear stopping point. Avoid another chain of speculative checkpoints.

## Future work, when requested

- Use the reference and record concrete reading/correction problems. February 1988
  is a useful starting point; the owner particularly likes the Gary Kildall interview
  (`8802030`). Preserve paper-supported corrections separately from CD transcription.
- Resolve text gaps, article boundaries, TOC associations or deferred images when
  a specific restoration need justifies the work. Their existence does not reopen
  the completed CD1 reference deliverable.
- Implement the richer viewer under its own PRD. At handoff, `PRD-reading-room.md`
  has owner edits and `PRD-local-web.md` is untracked owner work. Read them as current
  input, but do not overwrite or accidentally include them in unrelated commits.
- CD2 and CD3 belong to [PLAN-CD2](../PLAN-CD2.md) and [PLAN-CD3](../PLAN-CD3.md).
  Confirm each disc's actual coverage. Before expanding, consider consolidating the
  successful extraction path into a smaller documented workflow.
- Earlier paper scans remain future sources; their absence does not block use of
  the CD1 reference. The owner has the local ISO and physical CD but reported no
  accessible CD-ROM drive or independent backup. Do not reinstate backup verification
  as a prerequisite for ordinary local extraction. Preservation and future public
  access decisions remain separate work.

## Working notes

New reference tools live in `tools/reference/`; the historical pipeline, schemas
and policies were left unchanged. Text/media exports are private, ignored build
artifacts, not committed publication content. A Git checkout alone does not include
the source media or finished reference folder.

`make check-cd1-reference` validates the existing export. The focused test command is
`PYTHONPATH=src python3 -m unittest discover -s tests -p test_cd1_reference.py -v`.
At completion, all 12 tests passed; validation covered 26,828 files, 7,994 HTML pages
and 81,086 local links. A complete rebuild reproduced every file. Browser checks
confirmed Korean text, code whitespace, text downloads and images. These establish
extraction consistency and usability, not agreement with paper.

`make export-cd1-reference` rebuilds in isolation and checks against the existing
output. If changing the exporter, use a new `build/cd1-reference-*` output path as
documented in the guide; do not overwrite the prior evidence. Avoid rerunning the
whole historical test suite for documentation-only work. Log substantive work in
PROGRESS.md and commit scoped changes, as the owner requested.
