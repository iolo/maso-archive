# CD3 extraction and reading-room content plan

Status: **deferred**. Created 2026-09-18 as a separate source-specific queue.
The active extraction task remains step 6 in [PLAN-CD1.md](PLAN-CD1.md).

## Scope and evidence

The archive target is **1983-11–1995-12: 146 monthly issues**. This plan handles
the owner's official `masocd-3.iso`, whose inspected paths suggest **1995**
coverage. Exact issue/article coverage and content completeness are unverified.
The supplied TOC ends in 1990; do not fabricate later TOC matches or metadata.

Initial inspection found `MASO3.M14`, `LIST.M14`, `MASO3.EXE`, `MV*14N.DLL` viewer
libraries, and CAB attachments. The owner specifies Windows 95 for this disc.
Source sizes, hashes, and observations are in
[the source inventory](docs/SOURCE-INVENTORY.md). Attachment dates and inconsistent
filesystem timestamps do not establish article coverage or publication dates.
Compatibility with either earlier disc's decoder must be tested separately.

## First task when this plan is activated

**Input:** the original ISO, recorded hash, and its source inventory.

**Deliverable:** a private, reproducible CD3 source/format inventory and one
candidate article for a bounded extraction probe. Locate native index/content
relationships and distinguish article media from downloadable attachments.
Record the original viewer entry point and available reference evidence; use
the Windows 95 environment if needed.

**Check:** confirm the source hash, identify candidate content/index/media paths,
and keep confirmed observations separate from format/coverage assumptions.
If no article can yet be identified, record the specific indexing/format question
as the next task. No bulk extraction is part of this first task.

## Subsequent checkpoints — detail after inspection

Recover one article's text, structure, and media; compare it with the original
CD3 viewer; export a reading-room content package; test a second case; expand by
issue in bounded batches with coverage and review reports. Split each checkpoint
into numbered tasks using the evidence obtained. Reuse the versioned static
content contract from CD1 when applicable, while preserving disc-specific source
identities, provenance, unsupported content, and any required schema changes.

The [reading-room PRD](PRD-reading-room.md) owns UI implementation. This plan owns
offline extraction and static content preparation, independent of publication or
access-policy decisions. Keep source media and recovered bodies/assets private.
For every task, update [PROGRESS.md](PROGRESS.md), validate the result, inspect the
staged diff, and commit. A request to continue CD1 does not activate this plan.
