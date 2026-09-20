# CD1 processing inventory and batch input contract

Step **13a is complete**. The inventory reconciles native topic metadata, all
three CD indexes, the current TOC import, and February's six prepared articles.
It supplies the input queue for the shared runner in **13b**. This step recovers
no new article text, converts no images, and changes no prepared content package.

The tracked [reviewed record](../data/catalog/processing-inventories/cd1.json)
contains source/output hashes, counts, issue groups, unresolved ownership records,
context-offset evidence, and the fixed validation sample. Full metadata artifacts
are private under `build/cd1-processing-inventory/`.

## Population accounting

| Population | Result |
| --- | --- |
| Native/RTF topics | 3,099, all classified and retaining source spans. |
| Native contexts | 2,103; each maps to exactly one exported alias/topic. |
| Index entries | 3,032: 2,462 reference occurrences, 567 categories, three terminators. |
| Distinct index targets | 1,080: 1,038 numeric, 41 suffixed, one named. |
| Index target roles | 1,079 dated article candidates and the `mscdmenu` navigation topic. |
| Dated article candidates | 1,088 across 72 months, January 1988–December 1993. |
| Already prepared | Six February articles, with original identities and evidence. |
| Ready for runner validation | 1,074 candidates. |
| Blocked on ownership | Eight candidates with adjacent unattributed content. |
| Unindexed dated candidates | Nine, including the prepared KEYBOARD LOCK. |
| Current TOC entries | 5,497, all accounted for; section/outside-coverage states are explicit. |

“Ready” means the metadata permits the runner to start its checks. It does not
claim complete article boundaries, successful decoding, verified structure, or
agreement with the printed magazine. One job represents a dated native body
candidate; final multipart article relationships may need additional evidence.

Topic roles are **1,088 dated article candidates, 883 linked introduction
candidates, 993 formatting-only separators, 114 linked auxiliary topics, three
embedded application-resource topics, ten navigation topics, and eight
unattributed content topics**. Introductions require an explicit body link to the
immediately preceding untitled topic. Auxiliary links, aliases, incoming references,
and source spans remain available; auxiliary topics are not silently discarded
or counted as articles. The runner must inspect related links before claiming
complete extraction.

## Identity and source evidence

The builder checks the original MVB/RTF hashes and reuses the native metadata scan
from February's closeout. It reproduces index entries/grouping from the preserved
CP949 sources and reproduces current TOC entries from TOC.md and its identity
registry. Every February runtime file is checked against its package record, and
native topic spans are compared with the reviewed article provenance.

Every index target resolves through its context hash to one exported alias. No
suffixed target is collapsed into a numeric reference. Unindexed bodies keep their
native alias and context evidence; numeric references are not guessed from pages.
The previously reviewed `8802162` identity is retained. Other unindexed candidates
use provisional article identities such as `cd1:article:native-<context-hash>`.
Job identities use `cd1:job:<context-hash>`; topic identities use the original native
ordinal, such as `cd1:topic:0146`. Source fingerprints bind these identities to the
preserved disc/export.

All **31 context/header-offset differences** fall strictly within their topic's
native interval. Eleven belong to dated bodies; the rest belong to other topics.
Ordered native header links, unique aliases, interval bounds, and matching
native/RTF titles for dated bodies support the metadata association. These cases
are recorded as `inside_native_topic_interval`; the context offset must not be
used as an article-header address. Actual extraction boundaries remain a runner
check. The earlier February-only report is preserved unchanged.

TOC matching uses exact native/index titles, explicit issue labels, and observed
opening page labels, plus the six existing reviewed matches. No fuzzy matching or
reference-suffix page inference is used. The current conservative results are
**66 matched TOC entries, 185 title candidates needing review, 2,780 without an
exact-title match, 1,909 outside observed CD1 issue coverage, and 557 sections**.
These are metadata relationships, not article-preparation counts. Each title
candidate records page agreement/disagreement. An unmatched TOC entry does not
block extraction of an independently identified CD article.

## Eight ownership cases retained for review

| Article body topic | Adjacent unattributed topic | Finding |
| --- | --- | --- |
| 1436 | 1437 | Untitled, unaliased content after the dated body. |
| 1454 | 1453 | Preceding aliased content lacks the expected direct body link; body links elsewhere. |
| 1734 | 1733 | Preceding aliased content lacks a direct body link. |
| 2132 | 2133 | Untitled, unaliased content after the dated body. |
| 2366 | 2367 | Untitled, unaliased content after the dated body. |
| 2437 | 2436 | Preceding aliased content lacks a direct body link. |
| 2704 | 2703 | Preceding aliased content lacks a direct body link. |
| 2750 | 2749 | Preceding aliased content lacks a direct body link. |

The three following topics contain substantial content rather than blank
separators. The five preceding topics are possible introductions whose ownership
needs evidence. The inventory retains their exact spans and blocks the affected
jobs; it does not merge them based on adjacency. These cases can be investigated
independently while the other candidates proceed.

## Files and input contract

`manifest.json` has `schema_version: 1`, `inventory_version: "1.0.0"`, source and
implementation fingerprints, counts, and hashes for every output. The runner
should call `load_inventory()` before consuming it, then validate source and
configuration fingerprints at extraction time. A standalone inventory verification
checks its own consistency and hashes; it does not reread original sources.

| File | Purpose |
| --- | --- |
| `topics.jsonl` | Every topic's native metadata, RTF span/hash, alias, links, role, and lexical feature hints. |
| `contexts.jsonl` | Every native context entry, alias, associated topic, and native interval evidence. |
| `index-entries.jsonl` | Every original imported entry, including categories and terminators. |
| `index-references.jsonl` | Every distinct target and occurrence ID, resolved topic/job, and issue-conflict state. |
| `jobs.jsonl` | Ordered article-candidate queue, source topics, identities, blockers, and TOC evidence. |
| `toc-coverage.jsonl` | Every TOC identity/source locator and its candidate/matched jobs or availability state. |
| `issues.json` | Ordered issue groups, job IDs, and per-issue counts. |
| `review-items.json` | Unattributed topic ownership cases, including exact topic IDs. |
| `validation-sample.json` | Frozen step 13c sample with source identities, selection reasons, and review concerns. |

Each job has version/kind/identity fields, `body_topic_id`, optional
`introduction_topic_ids`, `source_topics` with native/RTF evidence, `related_links`,
`issue_id`, `title`, an observed-or-missing `opening_page`, original index references
and occurrences, `toc` relationship evidence, and a state:

- `already_prepared`: linked to reviewed February preparation, including source
  spans, extraction status, TOC IDs, and pending physical verification.
- `ready`: eligible for later extraction checks; no known metadata blocker.
- `blocked`: explicit `blockers` identify the source or ownership dependency.

The validator checks complete populations, unique ownership, context intervals,
reference/occurrence grouping, topic links, job states, source evidence, and
bidirectional TOC/job relationships. Font IDs, control names, paragraph-control
counts, tabs, and resource extensions are **lexical screening hints**, not a full
RTF feature inventory or proof of semantic structure. Inherited formatting must
be reconstructed by the shared runner.

## Frozen validation sample

Nine ready candidates span all six observed CD1 years. Selection occurred before
new article recovery. The sample supplements February's six regression articles;
it does not change their original preparation evidence.

| Body topic | Source reference | Issue | Selection reason |
| --- | --- | --- | --- |
| 185 | `1KP6JK` (unindexed alias) | 1988-04 | Short topic with bitmap media and unindexed identity. |
| 302 | `8901152` | 1989-01 | Math-library title, font 15, many vector occurrences. |
| 1150 | `9011288` | 1990-11 | Long font-15 topic, mixed media, interior context offset. |
| 1433 | `9105358` | 1991-05 | Additional font 26 and many vector occurrences. |
| 2182 | `9209394a` | 1992-09 | Suffixed reference and font-15 content. |
| 2502 | `9302402a` | 1993-02 | Short suffixed topic; opening date omits its second period. |
| 2611 | `9304310` | 1993-04 | Additional font 95 and many bitmap occurrences. |
| 2985 | `9311000` | 1993-11 | Supplement with no numeric opening page label. |
| 3049 | `9312167` | 1993-12 | Late-disc long font-15 topic and interior context offset. |

Media failures and source-specific exceptions can remain recorded during 13c.
Preservation or runner defects must be corrected before 13d's full pass.

## Reproduce and verify

```sh
make inventory-cd1-processing
PYTHONPATH=src python3 -m tools.inventory_cd1_processing --check
PYTHONPATH=src python3 -m tools.inventory_cd1_processing --verify build/cd1-processing-inventory
```

Normal builds must reproduce the tracked record. `--check` rebuilds in memory and
compares it without writes. `--write-record` establishes an intentionally reviewed
new inventory. Generation validates a staged directory before replacing the prior
inventory; failed validation leaves the previous output intact. The manifest and
reader provide the batch input contract without introducing runtime dependencies
on the original disc into reading-room packages.

The [shared runner](CD1-BATCH-RUNNER.md) is complete for 13b.
The [frozen-sample validation](CD1-BATCH-VALIDATION.md) also passes.
The [13d full-pass report](CD1-FULL-PASS.md) now reconciles every candidate;
individual source exceptions remain subsequent bounded work. Physical comparison,
missing scans, deferred repairs, backup/restore,
CD2/CD3, publication/access decisions, and reading-room UI remain separate work.
