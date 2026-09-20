# CD1 linked auxiliary recovery and retry sample — checkpoint 14a

The first complete pass stopped 470 articles at its association check. Auditing
all **587 blocking link occurrences** found **111 separate auxiliary topics**:
31 leaf topics and 80 topics with outgoing links. None is owned by an article in
the native inventory. All **308 outgoing links** remain source references; the
retry policy does not recursively import their destination articles.

Ownership here means deciding which article a native topic belongs to. The new
policy retains auxiliary identities separately, preserving source boundaries and
article-to-auxiliary links. It does not infer ownership from adjacency or merge
auxiliary paragraphs into an article body. Semantic classification remains pending;
leaf topics are not automatically labeled biographies solely from their aliases.

## Results

**109 auxiliary topics recover successfully:** 774 paragraphs, 85,274 original
RTF bytes and 1,176 text runs pass independent source accounting and strict codec
round trips. Original resources are verified for 28 media references deduplicated
by resource name. Auxiliary media rendering remains deferred.

Topics **18 and 19** retain raw RTF, their native identities and inherited
formatting state because that state contains unsupported controls. They are
explicitly deferred, with no successful full-text claim. Every auxiliary retains
its original source bytes, aliases, outgoing links, decoder inventory/recovery
where available, and disposition.

The fixed retry sample passes for all six articles:

| Source reference | Case |
| --- | --- |
| `9308449` | Leaf auxiliary |
| `9103252` | Auxiliary with outgoing series links |
| `9010234` | Mixed leaf and series auxiliaries |
| `9201335` | Deferred auxiliary topic 18 |
| `9008224` | Deferred auxiliary topic 19 with series links |
| `9004200` | Shared auxiliary referenced by 49 candidates |

All six are **prepared with review exceptions**. They contain **791 paragraphs
and 284 blocks**, across ten source topics. Independent checks cover **128,520
RTF bytes and 718 text runs**. All **ten available bitmap derivatives** preserve
source pixels. Separate auxiliary recovery in the retry runner matches the audit
exactly, including both deferred dispositions. Generic semantic and physical
review remain pending.

The six standalone and six sample issue packages validate. They add six prepared
articles beyond 13d's historical 537, but the sample issue packages contain only
sample articles. They do not replace the prior combined issue handoffs. Step 14b
will retry the remaining 464 association candidates and reconcile successful
results into current combined packages and availability records.

## Commands and private evidence

```sh
make review-cd1-associations
make retry-cd1-association-sample
```

Both commands verify their recorded results on normal execution. To establish
an intentionally reviewed new record, use `ASSOCIATION_ARGS=--write-record`.
The retry command requires the same converter/font environment as the first pass.

- [Auxiliary audit record](../data/catalog/batch-runs/cd1-association-review.json)
  locates the private policy, recovery files, all blocking links and 470 retry
  targets under `build/cd1-associations/stages/review/<fingerprint>/`.
- [Retry sample record](../data/catalog/batch-runs/cd1-association-sample.json)
  locates private article/issue packages and durable job/source checkpoints under
  `build/cd1-association-sample/`.
- Each auxiliary directory retains `source.rtf`, `source-topic.json`,
  `inherited-state.json`, decoder artifacts where available and `disposition.json`.
- The retry runner records the extension's code and reviewed policy in a distinct
  pipeline identity. Completed jobs resume by verifying their source, package and
  stage hashes. Failures remain recorded instead of being silently retried.

The original root-level pipeline code, shared policy and full-pass records are
unchanged. Historical commands remain reproducible. The extension refuses an
output root inside `build/cd1-batch/`. Source bytes, native contexts, aliases,
incoming links and existing article ownership constrain auxiliary acceptance;
ambiguous or owned destinations remain unresolved.

## Validation and remaining work

**217 regression tests pass**, including six association tests. These cover
ambiguous/owned/missing targets, stale source bindings,
duplicate failure records, separate text recovery, deferred formatting evidence,
original-output protection and actual review/sample artifacts. Repeat audit and
sample commands reproduce the tracked records exactly. A fresh build with the
checkpoint helper explicitly fingerprinted preserves all **57 article runtime
files** byte for byte; the final artifact checks and resume also pass.

Step 14a does not assert that all 470 bodies can decode: later inventory, font,
structure or media checks may expose new exceptions. Step 14b records those
outcomes explicitly. TOC matching, other first-pass failure classes, physical
comparison, broken-image repair, independent backup verification, CD2/CD3,
publication/access decisions and reading-room UI remain separate work.
