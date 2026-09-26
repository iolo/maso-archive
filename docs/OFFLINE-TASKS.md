# Offline tasks for the owner

CD1, CD2, CD3 restoration and the combined reading room are complete. These
optional tasks provide physical-magazine evidence and independent preservation
for later work; they do not block the delivered reader. See the
[current handoff](SUCCESSOR-NOTES.md). No routine original-viewer comparison,
screenshots, copy/export tests or new Windows setup are required. The owner's
existing Windows observation for the [CD3 underline bug](CD3-HELPDECO-UNDERLINE-BUG.md)
is retained as diagnostic evidence, not paper verification.

## 1. Locate the pilot in the physical magazine

Start with **February 1988, “유닉스란 무엇인가?”**. The current TOC and CD record
point to **page 65**, but the full printed page range has not been established.

Record the issue/date, edition if relevant, displayed title, author, and printed
page range. Check for continuations on later pages and note where the article ends.
If that issue is not available yet, simply leave its print comparison pending.

## 2. Capture reference pages when available

Scans or clear photos of the complete article are useful. Preserve page numbers,
margins, headings, code examples, figure/table captions, and readable small text.
Keep the originals; any cropped or enhanced review copies should remain separate.
Record missing, cut-off, or unreadable pages rather than implying full coverage.

Begin with the opening and ending pages if collecting the full article takes
longer. Partial captures can support partial comparisons; they do not verify
uncaptured content. Include the issue's TOC if readily available.

Broken converted images remain deferred. Capturing their corresponding printed
figures as part of a page is fine, but no special investigation of `bm54.wmf` or
`bm55.wmf` is required now. Do not assume CD badges, navigation icons, or layout
objects have equivalents in print.

The graphics article starting at page 180 also has two deferred inline WMFs and
a possible mixed-encoding string in its demo listing. Their locations and the
unapplied Johab alternative are recorded in the [article notes](CD1-GRAPHICS-8802180.md).
Include those passages if collecting reference pages; no separate investigation
is needed now.

## 3. Keep provenance with the reference pages

Suggested private location (already excluded from Git):

```text
private/reference/print/1988-02/8802065/
  notes.md
  page-065-original.jpg
  ...
```

Use the actual printed page numbers and original capture formats. A short note
is enough:

```text
Physical issue / edition:
Printed title / author:
Article start, end, and continuation pages:
Pages captured and corresponding filenames:
Missing or unreadable portions:
Capture date and source copy:
Observed differences from the CD-derived preview, if any:
```

Later comparison will cover metadata, article boundaries, text, headings, code,
figures, tables, and captions. Differences may come from the CD edition or from
extraction. Keep CD-derived text intact and record any print-based correction
separately, with its page evidence. Existing CD-viewer captures may be retained
as historical diagnostic evidence; they are not print-verification evidence.

## 4. Make an independent source backup

The working `masocd-1.iso` was extracted from the retained original CD. No
optical drive is currently available. Local inventory is complete; independent
recovery verification remains deferred as step 11b, separately from extraction. A [prepared transfer archive](CD1-PRESERVATION.md#prepared-local-transfer-set)
groups an earlier CD1 ISO/probe/artifact/Git snapshot into about 674 MB. It is a
historical CD1 transfer set, not a backup of the completed CD2/CD3 references
or combined reading room.
When separate storage is available, copy the prepared `.tar` and `.sha256` files
there and verify the checksum. A fresh read from the physical CD is another
verification route once an optical drive is available. This
local staging does not count as an independent backup.

For a manual copy instead, start with `masocd-1.iso`, the
entire `private/cd1-probe/` tree, inventory, and repository snapshot described in
the [CD1 preservation instructions](CD1-PRESERVATION.md). Keep prepared private
artifacts and toolchain evidence too when practical. The ISO plus probe tree is
about 624 MB, before repository/prepared content.

Record the backup location privately and use the documented restore command to
check a newly restored ISO and all its files. A same-disk copy is not independent
storage; a local inventory check is not a restore test. Preserve the working image and original CD. CD2/CD3 ISO backups are also useful when convenient; their known hashes are
in [the initial source inspection](SOURCE-INVENTORY.md).

## 5. Gather information for the later scan phase

When convenient, list which 1983–1987 issues can be obtained or scanned and any
known missing pages. Start by locating **1983-11**. A cover, TOC, and typical article
page are enough to plan a later scanning pilot. Keep available source scans under
`private/scans/`; bulk scanning is a separate future task.

The pilot, February slice, full CD1 pass, subsequent CD2/CD3 references and
combined reading room are implemented. The original references retain their
coverage reports and unresolved cases. Use the current reader to identify a
specific passage or figure for comparison; the historical pilot/batch steps
are not a new work queue. Physical review, missing scans and independent
backup/restore verification remain optional follow-up work until requested.
