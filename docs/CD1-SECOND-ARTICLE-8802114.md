# Second article: schema v1 check

Step 10 recovers **스펠링 체커**, CD1 reference `8802114`, from February 1988,
and packages it through the approved reading-room v1 contract. **No schema change
was needed.** This is a second inspected case, not evidence that every remaining
CD article uses supported structures.

## Why this article

The first pilot is a long feature with numbered headings, short command examples,
mixed text/media code, figures, and a table image. This second article tests:

- Two **unnumbered** headings identified by their source formatting and context.
- Three long Pascal listings of **317, 36, and 96 paragraphs**, including empty
  lines and indentation, with numbered listing captions.
- A separate one-line command example.
- Fixedsys text, a font absent from the first pilot's decoded text.
- A single bitmap title badge, rather than many editorial images.
- Two real articles sharing one issue and TOC tree in a combined package.

The source selection also has strong boundary evidence: topics 151–152 were
already identified as the first pilot's neighboring introduction/body. The new
check verifies those spans against the checksummed MVB and RTF, resolves native
reference `8802114` and alias `1KN6EK` to hash `0x0e684098`, and checks the hidden
body link to introduction alias `3M4LHC`. The following separator is topic 153;
the next browse target is topic 155, belonging to a different article. It is not
treated as a continuation.

Three CD index occurrences agree on title and issue. The title matches exactly
one February TOC entry, `maso-1988-02-toc-0021`, under the utility section. The
body's explicit label `88.2.  114p` independently agrees with TOC page 114. The
end page remains unknown; the next article's page does not establish it. The
source supplies an editorial byline. Print completeness remains unverified.

## Extraction finding and bounded change

The initial probe recovered prose but flagged **417 Fixedsys text runs** because
the original pilot decoder supported only fonts 4, 5, and 6. The document header
identifies font 15 as `Fixedsys`; all 12,608 encoded bytes in those runs are ASCII.
This is an extraction-policy gap, not a missing reading-schema construct.

`recover_topic` now accepts an explicit font-to-codec policy. Its default remains
the original CP949 mapping. This second case opts font 15 into **strict ASCII**;
non-ASCII bytes remain unsupported instead of being guessed or replaced. Other
unknown fonts remain unsupported. Every decoded run round-trips to its original
encoded bytes. All 27,624 source bytes across both topics have contiguous token
accounting. The existing decompiler-brace handling accounts for 34 literal-brace
guards; it does not treat them as article characters.

The second mapper uses inspected paragraph ranges and source formatting:
body headings at 10 and 14; command at 18; listing captions at 24, 344, and 383;
listing bodies at 26–342, 346–381, and 385–480. It checks captions, `PROGRAM`/`END.`
boundaries, Fixedsys runs, blank separators, and exact paragraph/run coverage.
These are source-specific decisions, not a universal classifier. The first
pilot's numbered-heading rule is retained for that pilot.

Source spelling and apparent code errors remain unchanged. The programs have
not been compiled, repaired, or executed. Extraction integrity does not establish
that the printed source code was correct or complete.

## Results under the unchanged schema

| Check | Second article | Combined with first pilot |
| --- | ---: | ---: |
| Issues / TOC entries | 1 / 39 | 1 / 39 |
| Articles / established TOC matches | 1 / 1 | 2 / 2 |
| Sections | 2 | 4 |
| Blocks | 39 | 310 |
| Paragraphs | 485 | 808 |
| Media resources / occurrences | 1 / 1 | 22 / 22 |
| Available media assets | 1 | 20 |
| Deferred media | 0 | 2 |
| Markdown previews | 2 | 4 |
| Runtime files, including manifest | 8 | 30 |

The second article has 439 runs: 438 text runs and one media occurrence. Its
39 blocks comprise two titles, an issue label, a byline, two headings, four code
blocks, three captions, 11 prose paragraphs, and 15 spacing blocks. The three
listing captions link directly to the corresponding code blocks. Code is
preformatted; blank lines and trailing spaces survive. No code-language or
table-cell extension was introduced.

`bm40.bmp` becomes a 32 × 25 PNG through ImageMagick. Source and output dimensions
and decoded RGBA hashes agree. Visual inspection shows a small title badge;
its navigation behavior is not inferred. The original bitmap and conversion
evidence remain private. No new media failure required deferral.

The combined package retains the first article document, its media metadata,
previews, and accepted asset bytes. It adds the second article and updates the
shared issue/catalog with the second TOC link. **37 TOC entries remain unmatched.**
`bm54.wmf` and `bm55.wmf` remain deferred with null assets and original positions;
their suspect derivatives are absent. Both articles retain pending print status.

## Reproduce and inspect

```sh
make check-second-article
PYTHONPATH=src python3 -m tools.build_reading_room_package --verify build/cd1-second-article/8802114/single/content
PYTHONPATH=src python3 -m tools.build_reading_room_package --verify build/cd1-second-article/8802114/combined/content
make check
```

Build inputs are the original checksummed CD1 MVB/RTF and extraction manifest,
existing index/TOC imports, earlier topic-map evidence, the first pilot's validated
package and reviewed summary, and `convert`. Only this article is newly recovered.
The build verifies source hashes and rejects unreviewed controls, decoding issues,
or unsupported paragraph endings. It makes no network or publication request.

Private output root: `build/cd1-second-article/8802114/`.

- `single/content/` is the second article's standalone v1 package.
- `combined/content/` is the two-article v1 package, useful for reading-room work.
- `recovery.json`, `inventory.json`, and `blocks.json` retain source spans,
  formatting, byte accounting, and semantic decisions.
- `introduction.txt` and `body.txt` are exact recovered text projections.
- `provenance.json` holds native/topic and TOC/index evidence, font policy,
  conversion details, preview content ranges, input hashes, and output hashes.

Each `content/` directory can independently serve as the configured package base
URL. The standard standalone validator reads it without extraction inputs.
Runtime documents contain no local paths or byte-span ledgers. The code, tests,
and [metadata summary](../data/catalog/second-article-checks/cd1-8802114.json) are
tracked; publisher bodies, previews, images, and detailed evidence remain ignored.

The existing Markdown renderer now derives its article label/anchor namespace
from the CD reference. First-pilot output stays byte-identical. Package previews
use the current physical-magazine/media-status notes and retain source image
placeholders. All block-content byte ranges match the preserved rendering.

The default command compares its result with the reviewed metadata summary.
After an intentional reviewed source/tool change, use
`PYTHONPATH=src python3 -m tools.check_cd1_second_article --write-record` to refresh
that summary. Conversion version is recorded; no timestamps or temporary-directory
names enter output hashes. Each runtime package is validated in staging before
replacement; adjacent preservation files are replaced individually. Rerun after
an interrupted build to restore the complete deterministic set.

Seven new tests cover the opt-in ASCII policy, source boundaries/accounting,
every recovered run/mark, unnumbered headings and listing ranges, exact preview
content, bitmap pixels, deterministic rebuilds, and relocated single/combined
packages. The full suite also rechecks the first pilot's recorded output hashes.
The schema checksum remains
`2a160d646c4a92552fcc4647216348c14ee74c357a375412f23fed54bffc6f68`.

This supports v1 for the two inspected structures. Unknown RTF constructs,
uninspected fonts, source-specific segmentation, missing print evidence, and
collection-wide coverage still require their own work. The local inventory and
February coverage audit are now complete. Backup/restore remains deferred, and
article `8802030` is next under the current [CD1 plan](../PLAN-CD1.md).
