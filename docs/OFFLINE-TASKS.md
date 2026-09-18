# Offline tasks for the owner

These tasks provide physical-magazine evidence for later content verification in
[PLAN-CD1.md](../PLAN-CD1.md). Do them when convenient; extraction and reading-room
content preparation continue independently. No original CD-viewer comparison,
screenshots, copy/export tests, or new Windows setup are required.

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

The owner confirmed there is no independent backup yet. CD1's local source
inventory is complete; backup/restore remains pending as step 11b before bulk
processing. When separate storage is available, start with `masocd-1.iso`, the
entire `private/cd1-probe/` tree, inventory, and repository snapshot described in
the [CD1 preservation instructions](CD1-PRESERVATION.md). Keep prepared private
artifacts and toolchain evidence too when practical. The ISO plus probe tree is
about 624 MB, before repository/prepared content.

Record the backup location privately and use the documented restore command to
check a newly restored ISO and all its files. A same-disk copy is not independent
storage; a local inventory check is not a restore test. Preserve the sole working
copy. CD2/CD3 ISO backups are also useful when convenient; their known hashes are
in [the initial source inspection](SOURCE-INVENTORY.md).

## 5. Gather information for the later scan phase

When convenient, list which 1983–1987 issues can be obtained or scanned and any
known missing pages. Start by locating **1983-11**. A cover, TOC, and typical article
page are enough to plan a later scanning pilot. Keep available source scans under
`private/scans/`; bulk scanning is a separate future task.

The first package, [second-article check](CD1-SECOND-ARTICLE-8802114.md), and local
source inventory are complete. Step 11b remains deferred pending independent
storage. The [February coverage audit](CD1-COVERAGE-1988-02.md) and expanded TOC
import are complete. The corrected 1991–1993 entries are imported with stable IDs.
The next article task, `8802030`, remains gated on backup/restore readiness.
Physical reference collection and print comparison (step 7) remain independent.
