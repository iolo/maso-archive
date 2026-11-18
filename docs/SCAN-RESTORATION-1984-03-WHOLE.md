# March 1984 whole-issue restoration handoff

The whole donated-scan issue is complete within the native restoration scope of
`PLAN-SCAN-RESTORATION.md`. All **44 canonical identities** have accepted outcomes:
**38 complete JPEG-backed article packages and six non-owning headings**, with no
partial articles or unclassified identities. All **273 supplied images** have
source dispositions, with none pending.

The [whole-issue result](../metadata/catalog/scan-restoration/1984-03-whole-issue.json)
pins the selected export, recipes, completion audit, fresh article rebuilds,
preservation checks and frozen M83 evidence. The
[progress record](../metadata/catalog/scan-restoration/1984-03-progress.json)
retains the complete article and heading selections. The earlier
[M01–M04 handoff](SCAN-RESTORATION-1984-03.md) remains historical supplementary
work; its mixed PDF/JPEG issue is preserved separately.

The selected whole issue is
`archive/scans/1984-03/packages/issue-whole-r01/`. Its **7,940 files** reproduce
exactly in two independent builds. It contains:

- All 38 unchanged article directories under `articles/`, totaling 7,878 files.
- The separate four-face native cover set under `covers/`.
- Six heading outcomes and their validation records under `headings/`.
- Thirty byte-identical original JPEGs under `other-sources/`.
- The issue JSON/schema, canonical ledger, source accounting, retained inputs,
  provenance and exact file manifest.

The article check is separate from copying packages into the issue. All **38
selected native articles were freshly rebuilt from pinned recipes** through the
public build/assemble APIs, without new OCR. Every output file matches its accepted
package. Native indexes, typed references, source ranges, original assets,
program contexts, assembly boundaries and recorded continuities remain intact.
Shared source 204 retains distinct ownership by the Sewoon feature and lower
advertising index; neither body is duplicated.

Check the issue with the shared runtime and its repository schemas:

```sh
env PYTHONPATH=.:src python3 -m tools.pdf_restore.image_issue \
  --check --output archive/scans/1984-03/packages/issue-whole-r01
```

Rebuild into a fresh output with the retained construction inputs available:

```sh
env PYTHONPATH=.:src python3 -m tools.pdf_restore.image_issue \
  --recipe archive/scans/1984-03/restoration/whole-issue-79/issue-recipe.json \
  --output work/validation/march-whole-issue-fresh
```

The standalone check passed with original archive, work, private and donor inputs
blocked. It uses the exported native artifacts plus the shared code/repository
schemas. Rebuilding requires the pinned original inputs. External evidence pins
are provenance references; the issue does not embed the entire working archive.
The result lists all 38 article recipes and their build/assemble entry points.
Treat frozen checkpoint helpers and implementation snapshots as data only:
**never execute, import or modify them**.

Source accounting distinguishes **239 article-source images, four covers and
30 other images**. The latter comprise eighteen advertisements/promotions, one
contents/credits/colophon scan, four non-owning section dividers, two notices,
four postal/subscription/payment-slip faces and one separate spine alternative.
They retain full original rasters and reviewed disposition labels, without a claim
of complete unlisted-text transcription. The four inserts keep their original
orientation and full width; recto/verso pairing and physical collation remain
unverified. The spine retains `reading_order: null`. Serialization after ordered
records does not assign it a physical location or folio. Filename numbers are
not substituted for observed printed folios.

The opt-in `source-dispositions-v2` export mode supports that unsequenced spine
and evidence-linked observed folio labels. Existing November behavior remains
qualified by its actual issue check. Information heading 0038 receives only its
missing canonical `parent_id: null` in a fresh documented projection; every
original field and the frozen M79 record remain unchanged.

The completion audit passes all 44 canonical outcomes, 273 source dispositions,
32 damaged actual accounting cases and **318 fresh regression tests**. All 273
masters, both donor ZIPs, original TOC/cleanup pins, 38 original PDF packages,
the original PDF issue and the historical supplement issue pass preservation
checks. M01–M04 and M77–M82 frozen evidence is freshly rehashed. The operating
OCR/PDF plans remain unchanged. Cleanup was preview-only, with no deletion.

All **318 original article gap/limitation notes** and source-local qualifications
remain preserved. Completion establishes source accounting, native structures and
artifact reproducibility. Human acceptance, character-perfect proofreading,
original encoded bytes, historical program execution and physical-paper
completeness remain unverified. Reading-room work and cosmetic reconstruction
are separate tasks. The next new issue in the chronological scan queue is
December 1983; it has not been started by this closeout.
