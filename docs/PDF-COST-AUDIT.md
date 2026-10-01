# PDF restoration cost audit — 2026-10-01

Audit cutoff: 2026-10-01 14:26:46 UTC, immediately before the audit request.
No restoration or pipeline changes were made after that request. The accounting
assembly's code and progress changes were already pending; it has not been closed
out or committed as a completed restoration checkpoint.

## Measured costs and scope

The main comparable sample is **24 completed February restoration batches plus
four completed assemblies**. These checkpoint intervals total **10h 34m 02s**.
This is elapsed time, including waits, context handoffs and interruptions, not CPU
or uninterrupted agent working time. The 24 restoration batches alone total
8h 05m 16s; their median is16m 53s. The current unfinished accounting assembly
adds5m 34s through the cutoff and is excluded from the completed sample.

Token counts below are measured usage records assigned to timestamp intervals.
The broad stage boundaries are recorded; finer activities within each interval
were not separately timed. Cached input is a subset of total input, not an extra
charge to add to it. Output includes the separately reported reasoning subset.
These are token counts, not monetary prices or an invoice.

| Recorded stage boundary | Elapsed time | Uncached input | Cached input | Output |
| --- | ---: | ---: | ---: | ---: |
| Batch start → review complete: mapping, rendering/OCR, transcription, visual review | 4h26m10s | 2,260,759 | 66,960,128 | 386,297 |
| Review complete → closeout: export, rebuild/validation, browser acceptance, documentation | 3h39m06s | 732,699 | 37,073,792 | 139,304 |
| Four completed assemblies, including implementation and acceptance | 2h28m46s | 192,408 | 14,435,840 | 72,949 |
| **Completed February sample** | **10h34m02s** | **3,185,866** | **118,469,760** | **598,550** |

The unfinished accounting assembly adds73,845 uncached input,748,416 cached input
and6,478 output tokens through the cutoff. It has475 article-package files and a
148,188,146-byte export; its unchanged source packages and repeated build account
for deliberate disk duplication, not additional OCR.

The separate current-goal window begins2026-10-01 03:25:03 UTC. Its measured
response records contain3,204,530 uncached input,127,892,224 cached input and618,617
output tokens, including74,515 reported reasoning tokens. Thus131.72M raw tokens
includes127.89M cached input; **97.6% of input tokens are cached**. The goal service
reported3,749,065 tokens and30,987 seconds at14:26:56 UTC, shortly after the request.
Its counter is a different accounting field; do not equate it with raw input plus
output. The current goal window and completed-checkpoint sample have different
boundaries and must not be added together.

For context, this entire conversation through the cutoff records524,269,123 raw
tokens:508,540,544 cached input,13,368,822 uncached input and2,359,757 output.
This includes earlier pipeline work and the previous issue. The event_msg
`token_count` snapshot can lag the cumulative `token_usage_record` totals; the
latter were used, with response IDs deduplicated and monotonic totals checked.

## Rendering/OCR and retries: directly recorded

The batch-state task ledgers record elapsed execution seconds, including task
orchestration. These are nested within the first table's batch intervals, not
additional elapsed time.

| Task execution | Attempts | Recorded seconds | Recorded task failures |
| --- | ---: | ---: | ---: |
| Initial passes | 769 | 1,093.86 | 0 |
| Subsequent states | 58 | 141.90 | 0 |
| **Total** | **827** | **1,235.76 (20m36s)** | **0** |

Of the58 subsequent executions,53 reran revised regions; five introduced new
regions in batch24. These are visual-quality/mapping revisions, not retries after
OCR process failures. Unchanged tasks reused cache entries. Summing the cached
processing totals from successive reports would double-count reused work, so the
per-state execution ledgers were used instead.

Batch24 is the largest documented revision case:73 initial tasks,30 corrected
regions, one new O label and four new complete listing panels =108 executions.
Its task execution totals68.11 seconds, including29.56 seconds in subsequent
states. Its full checkpoint elapsed24m09s. The preceding prose batch23 took
20m05s overall and42.69 seconds of recorded task execution.

## Repeated work and uncertainty

- Current goal window:11 recorded context compactions totaling27m53s. Whole
  conversation:39 totaling94m47s. These are measured event durations, already
  included in elapsed work; they are not added to checkpoint totals.
- Current goal window:784 image-view events for728 distinct paths, i.e.56 repeat
  views of an already viewed path. Some are justified comparisons; this is not a
  count of avoidable rereads or equivalent image content under different names.
- Current assembly verified4,438 prior-file pins and deliberately produced a
  second byte-identical build. Those are useful integrity checks. Repeatedly
  reconstructing their scripts and reading long JSON reports costs additional
  model interaction; aggregate CPU/I/O savings were not separately measured.
- The current assembly had one failed synthetic-test run due to an incorrect
  expected regional count, then a successful73-test full suite and a successful
  27-test assembly suite. Its validation script also initially counted three
  article headings as BASIC margin labels, then passed after the assertion was
  corrected. These are avoidable audit/test-authoring mistakes, not OCR defects.
- Prior news assembly retained a before-spacing export/rebuild and browser
  screenshots before correcting a mobile review-note overflow. This is concrete
  repeated export/browser work, but its incremental cost is not separately timed.
- Long elapsed checkpoints include news assembly115m05s, batch09 64m11s,
  batch21 51m25s and batch19 37m24s. Those include waiting/interruptions. They
  cannot honestly be described as equally long processing jobs or charged wholly
  to browser failures. No reliable time/token counter isolates user closing Chrome.
- Long-lived preview servers were excluded from command-time analysis: summing
  their concurrent lifetimes would spuriously report many hours of browser work.
  Foreground command durations in the goal window sum55m36s, but may overlap and
  are neither complete agent time nor additive to the checkpoint clocks.

## Finer token attribution — estimates, not measured stage billing

The following diagnostic attributes each model response to the latest tool action,
using command-name keywords. It uses the current goal window, not the28-checkpoint
sample. Mixed commands, intervening reasoning, heredocs and context restoration
make this approximate. Reused context is not evidence that all those tokens were
new work in the attributed stage. Shares use uncached input plus output only.

| Estimated activity | Uncached input | Output | Share |
| --- | ---: | ---: | ---: |
| browser acceptance | 432k | 77k | 13.3% |
| documentation/closeout/context | 414k | 101k | 13.5% |
| implementation/packaging/assembly | 274k | 8k | 7.4% |
| mapping/preparation | 55k | 9k | 1.7% |
| other/context/tool orchestration | 158k | 20k | 4.7% |
| render/OCR execution | 54k | 5k | 1.5% |
| transcription/visual review | 1,596k | 308k | 49.8% |
| validation/testing/rebuild | 221k | 91k | 8.1% |

Do not use these estimates to claim precise dollars, per-stage wall time, or
avoidable percentages. The stronger conclusion is that transcription/review and
coordination dominate; local OCR execution is a small part of elapsed work.

## Opportunities, ranked; none implemented by this audit

1. **Reduce repeated context and evidence loading.** Use smaller durable handoff
   summaries, targeted reads and concise tool results; avoid re-emitting full
   browser scripts, JSON records and already reviewed images. This directly
   targets context compactions,56 repeated image-path views and large cached
   context traffic while retaining saved evidence and correction records.
2. **Reuse checkpoint validation and closeout scaffolding.** Avoid authoring and
   debugging near-identical private scripts for each batch. Keep all existing
   integrity guarantees. The current incorrect assertions demonstrate a real
   source of preventable repeated work.
3. **Consolidate browser acceptance and its recovery.** Reuse a focused session
   with a compact state record; distinguish background server lifetime, actual
   checks and waiting. Preserve desktop/mobile checks and actual downloads.
4. **Improve initial region mapping for dense listings.** Earlier inspection of
   slanted edges, routine brackets and full-panel context could prevent repeated
   cropping and visual review. Batch24's30 revised regions are the strongest
   example. Direct execution savings are small; review savings are not measured.
5. **Reduce redundant full verification only after measuring it.** Reuse validated
   immutable manifests where guarantees remain equivalent; retain deterministic
   rebuild and tamper checks. Do not remove checks merely because they repeat.
6. **OCR engine speed is a low-priority target.** Even eliminating all recorded
   task execution would remove at most20.6 minutes from the634-minute checkpoint
   total (3.25%, ignoring overlap); removing every subsequent execution saves at
   most2.4 minutes (0.37%). These are illustrative upper bounds, not achievable
   forecasts. They do not include possible savings in human/model review.

Better timing boundaries would be the prerequisite for reliable optimization:
separate active time, tool processing, waits, transcription, review, browser work
and closeout; bind usage deltas to those boundaries and record retry reasons.
That instrumentation is a proposal only. No pipeline behavior, quality threshold,
correction format or retry policy was changed for this audit.

## Evidence

- Private aggregate and reproduction script:
  `private/pdf-restoration/cost-audit-2026-10-01/`.
- Per-checkpoint `checkpoint-plan.json`, `review-timing.json`, `closeout.json`, and
  `state*/ledger.json` under `private/pdf-restoration/12-1984-02-*`.
- Current assembly validation and test logs under
  `private/pdf-restoration/12-1984-02-accounting-assemble/`.
- Local conversation usage records and completed-event timestamps; raw conversation
  content was not copied into the report or committed.
