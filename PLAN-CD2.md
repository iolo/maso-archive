# CD2 extraction and reading-room content plan

Status: **deferred**. Created 2026-09-18 as a separate source-specific queue.
The active extraction queue is [PLAN-CD1.md](PLAN-CD1.md).

## Scope and evidence

The archive target is **1983-11–1995-12: 146 monthly issues**. This plan handles
the owner's official `masocd-2.iso`, whose inspected paths suggest **1994**
coverage. Exact issue/article coverage and content completeness are unverified.
The supplied TOC ends in 1990; do not fabricate later TOC matches or metadata.

Initial inspection found `DATA/MASO2.M12`, `BIN/MASO2.EXE`, and `MV*12.DLL` viewer
libraries. The owner specifies Windows 95 for this disc. Source sizes, hashes,
and observations are in [the source inventory](docs/SOURCE-INVENTORY.md).
CD1's successful decoder and encoding decisions are evidence to investigate,
not proof that they apply to CD2.

## First task when this plan is activated

**Input:** the original ISO, recorded hash, and its source inventory.

**Deliverable:** a private, reproducible CD2 source/format inventory and one
candidate article for a bounded extraction probe, with native identifiers and
available issue/title evidence. Record the original viewer entry point and
whether viewer reference evidence is available; use the Windows 95 environment
if needed rather than presuming CD1's working installation applies.

**Check:** confirm the supplied source hash, locate content/index/media containers,
and distinguish confirmed facts from candidate coverage/format interpretations.
If no article can yet be identified, record the specific indexing/format question
as the next task. No bulk extraction is part of this first task.

## Subsequent checkpoints — detail after inspection

Recover one article's text, structure, and media; compare it with the original
CD2 viewer; export a reading-room content package; test a second case; expand by
issue in bounded batches with coverage and review reports. Split each checkpoint
into numbered tasks using the evidence obtained. Reuse the versioned static
content contract from CD1 when applicable, while preserving disc-specific source
identities, provenance, unsupported content, and any required schema changes.

The [reading-room PRD](PRD-reading-room.md) owns UI implementation. This plan owns
offline extraction and static content preparation, independent of publication or
access-policy decisions. Keep source media and recovered bodies/assets private.
For every task, update [PROGRESS.md](PROGRESS.md), validate the result, inspect the
staged diff, and commit. A request to continue CD1 does not activate this plan.
