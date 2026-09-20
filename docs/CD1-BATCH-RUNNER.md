# CD1 shared batch runner — checkpoint 13b

The runner re-extracts February's six articles through shared stages and composes
independent article packages into an issue package. **13b is complete.** Its results below describe the February checkpoint.
The subsequent [13c frozen-sample validation](CD1-BATCH-VALIDATION.md) also passes;
**13d, the complete CD1 pass, is next**. Schema v1 remains unchanged.

## Commands and outputs

```sh
make batch-cd1 BATCH_ARGS="--issue 1988-02"
make batch-cd1 BATCH_ARGS="--article 8802030"
PYTHONPATH=src python3 -m tools.build_cd1_batch_profiles
```

Article selectors also accept a stable article ID or queue job ID. `--all` selects
the full queue, including explicit ownership blockers; 13c's checks now pass.
The runner requires the verified 13a inventory, original MVB/RTF/probe artifacts,
current TOC import, and the historical February handoff. It rechecks their hashes
before processing. It never calls an article-specific preparation script.

Private output lives in `build/cd1-batch/`:

- `articles/<job-hash>.json` points to each last successful article package.
- `issues/maso-YYYY-MM.json` points to the composed issue package.
- `stages/<stage>/<fingerprint>/content/` is a standalone v1 runtime package for
  package stages; other stages hold extraction evidence and checkpoints.
- `run-report.json` records the latest selection, per-job outcomes, issue results,
  and cache hits/builds/failures. Failures return a nonzero CLI exit status after
  the other selected jobs have been attempted.

Read a pointer's `package` relative to `build/cd1-batch/`, then use its `content/`
directory as the static package root. The existing [base-URL contract](CD1-ISSUE-1988-02.md#static-base-url-and-metadata-search)
applies unchanged: URL resolution belongs to the consumer, and all runtime paths
remain relative. For example, `/archive/maso/content/` can serve that directory.
No machine-specific paths, extraction tools, or source CDs are required to load it.
The nested-URL sample checks will be repeated during 13c.

`--output build/<private-name>` (or `/tmp/<name>`) creates a separate run. A
successful full February run can write the metadata-only checkpoint record with
`--write-record`; ordinary runs leave tracked records alone.

## Stages and preservation

1. **Association:** validate selected topic hashes and inspected queue links;
   retain original topic RTF and native/context/TOC evidence. Multiple introductions
   or unreviewed linked content outside the selected ownership scope fail explicitly.
   Three source-bound auxiliary topics reviewed in 13c are recovered separately.
2. **RTF inventory:** establish scoped inherited character/paragraph state across
   preceding topics, then inventory every selected token, group, control and object.
   Unknown inherited formatting or unsupported constructs retain failure evidence.
   First-line indentation, tab stops and double underline are also preserved after
   the source checks in 13c.
3. **Recovery:** strictly decode with explicit font/codec policies; retain every
   paragraph, run, source span, formatting property, token disposition and object.
   Undecodable runs retain their encoded evidence and cannot become reading text.
4. **Semantics:** apply common paragraph preservation and source-bound reviewed
   decisions. Unclassified nonempty paragraphs remain `unresolved`. The 13c shared rules
   retain Fixedsys passages as preformatted candidates, with semantic review still
   pending, and preserve supported headings without inventing missing parents.
   Unknown font policies fail recovery for inspection instead of guessing.
5. **Media:** reuse checked shared resources and reviewed dispositions. New bitmap
   conversion checks decoded pixels; WMF conversion retains diagnostics and rejects
   suspect/blank output. Failed conversions stay deferred at their occurrences.
6. **Markdown:** preserve source projections, formatting, code whitespace and
   caption links; record protected content ranges independently of preview notes.
7. **Package:** check v1 identity, relationships, source-text projections, media
   references, previews and hashes before publishing a successful generation.

The [February profiles](../data/catalog/batch-profiles/cd1-february.json) contain
metadata, source hashes and exceptional block ranges/properties, not article text.
Ordinary paragraph/spacing decisions use shared rules. Profiles bind exact source
topics and reviewed content hashes, including differing Fixedsys policies. The
exporter checks reproducibility against prior block maps; regenerating profiles
requires explicit `--write`. Original scripts, records and artifacts are retained.

## Resume, failure isolation, and composition

A stage fingerprint includes its upstream output hashes, source/job/configuration,
profile and schema hashes, Python/package versions, pipeline code, converter
versions and installed font-file hashes. Every cache hit checks the exact file
population and all output hashes. Different inputs/configuration produce a separate
generation; a damaged generation is quarantined before its validated replacement.

Stages write to temporary directories. Only successful validation publishes a
final directory. An interruption leaves partial evidence, which is never accepted
as a completed checkpoint. Ordinary failures also retain a `failure.json`; retries
reuse completed predecessor stages and attempt the failed stage again. Earlier
successful generations and article pointers survive failed replacements. Local
runs are single-writer: do not run two batch processes against the same output
root concurrently. Use separate `--output` roots for concurrent experiments.

Media conversion checkpoints are shared by source identity and policy. The four
known WMFs are reused as deferred dispositions without another repair attempt.
Issue composition reads all successful independent article packages for the
current pipeline identity in that issue, deduplicates shared media, and rebuilds
TOC links. It does not depend on a chain of historical combined packages. A
partial issue retains unmatched TOC entries and makes no completeness claim.
Historical generations remain available but are not silently imported into a new
pipeline configuration.

## February result and validation

The [13b checkpoint record](../data/catalog/batch-runs/cd1-february.json) locates
validated output and hashes. Compared with the native February handoff:

| Population | Shared runner result |
| --- | ---: |
| Articles / sections | 6 / 12 |
| Blocks / paragraphs | 677 / 2,821 |
| Media records / occurrences | 38 / 40 |
| Available assets / deferred WMFs | 34 / 4 |
| Markdown previews / runtime files | 12 / 56 |

Article JSON and Markdown bytes, media records and accepted asset bytes match
the baseline. Combined catalog/media ordering is canonicalized during independent
composition; that packaging order does not change source reading order. Coverage,
Gary Kildall bibliographic context, the graphics CP949/Johab ambiguity, and image
review records remain in private provenance. Deferred resources are `bm54.wmf`,
`bm55.wmf`, `bm57.wmf`, and `bm58.wmf`.

Tests cover source/run projection, profile drift, unsafe paths, inherited scoped
formatting, unknown fonts/controls, interruption with partial recovery evidence,
resumption, cache corruption and configuration invalidation, isolated article
failure, exact February regression, and incremental issue composition. Run
`make check` for the full suite. Reading-room UI, physical comparison, missing
scans, image repair, backup verification, publication/access policy and CD2/CD3
remain separate work.
