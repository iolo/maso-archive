# CD3 private readable reference

The private output is `build/cd3-reference/index.html`, a portable static
HTML/text/image reference built from the supplied CD3 ISO and checksummed M14
decoder probes. It is about 1.3 GB of files. Original media and recovered bodies
remain under ignored `private/` and `build/` paths; the tracked
`data/catalog/preservation/cd3-readable-reference.json` contains hashes and
counts, not article text. Serve it locally with
`python3 -m http.server 4179 --directory build/cd3-reference` and open
`http://127.0.0.1:4179/`. The pages use relative links and need no runtime
extractor, application server, or database.

## Reproduce and verify

1. Prepare the two decoder probes using the pinned HELPDECO revision and commands
   in [the source map](CD3-SOURCE-MAP.md). The owner reports that disc setup
   creates only a viewer shortcut; no software installation is needed.
2. Run `make inventory-cd3-sources` and `make map-cd3-candidates` to check the
   original ISO, extracted tree, M14 outputs, CAB member listings, and candidate
   queue against the tracked metadata records.
3. Run `make build-cd3-reference`. Its 18 CD-native groups build independently.
   `make build-cd3-reference CD3_ARGS=--resume` verifies and reuses completed
   group packages. `CD3_ARGS=--verify-existing` rebuilds all groups and requires
   identical manifests; the completed pass met this check.
4. Run `make check-cd3-reference`. It checks 11,346 output files, all candidate
   identities and outcomes, source topic spans, text and code whitespace against
   ordered blocks, media and CAB bytes, auxiliary topics, unassigned media, and
   every generated HTML link. The verified root manifest matches the tracked
   SHA-256 record.

Each article has a browsable page, `article.txt` with the same literal text and
inline code spacing, and `blocks.json` with ordered source runs, byte spans,
media positions, and localized issue records. Available figure previews appear
beside their article captions and link to the original BMP. Original CAB
attachments are copied byte-for-byte, and their member names and sizes are
recorded in the private source inventory. No separate CD3 code-list container
was found: inline code remains in the article text download, while source files
inside CAB archives remain available in their original archives.
Article pages link their native text boxes, author bios, and related articles.
The `supplements/index.html` shelf is available in the private output, including
three longer auxiliary texts without
an article link. Every supplemental topic has a source-backed page and text
download; image-only topics link to their original BMP. All 1,570 decoded BMP
originals are retained under `media-sources/`.

## Coverage and exceptions

The main RTF has 2,336 topics. Native title footnotes identify 967 article
candidates, and one additional 1995-06 body without a title footnote is retained
under its visible lead phrase. All **968 candidates** have readable text and
an explicit outcome: **792 success, 176 partial, none failed or blocked**.
Partial means a localized decoding, figure, attachment, or issue-label exception;
it does not mean the body was discarded. The groups include 12 apparent 1995
months, some 1994 labels, one 1996 label, and seven candidates without a unique
date. These are CD-native labels, not verified paper issues. The supplied
library TOC ends at 1993-12, so no 1995 TOC links or page matches were invented.

The article RTF contains 1,139 image markers. **971** viewer Click icons have
figure links; **969** resolve to separate figure topics. The two unresolved
aliases are visible in their article pages. Eight resolved figure topics name
image files missing from the decoded probe; those positions show unavailable
states. All **1,039** copied group media records have validated PNG previews
and original files. Another **511** decoded BMPs have no RTF marker and are
retained under `unassigned-media/` with an explicit unassigned state. The
complete source map also records **253** missing image occurrences across
article and auxiliary topics; most are in auxiliary topics and are not silently
placed into articles.

Of 80 native CAB actions, **79** have copied original attachments. The missing
`Files\\9504\\Grid.cab` action in `topic-0104` is shown as unavailable while
its text remains readable. The text parser retains **1,869** undecodable byte
runs across 158 articles and **17** unsupported RTF controls across five
articles as visible markers with source evidence in `blocks.json`. It preserves
paragraphs, line breaks, tabs, spaces, bold, italic, and underline where present.
No uncertain bytes or code have been guessed.

The CD3 RTF export flags over 99% of article text as underlined, across all
968 candidates, because [HELPDECO misreads the character-set byte as double
underline](CD3-HELPDECO-UNDERLINE-BUG.md). The owner confirms normal rendering
in the Windows viewer. Reading pages and the reading-room adapter suppress
underlining, including supplemental pages. The decoder is unpatched: generated
RTF and `blocks.json` retain its erroneous flags, not verified original emphasis.
The workaround also suppresses genuine underline. Text downloads, bold, italic
and other marks are unchanged; a decoder correction and probe migration remain
deferred.

The remaining **1,368** RTF topics are classified separately: 12 author bios,
1,355 auxiliary topics, and one document tail. All have private pages and
downloads: 1,118 export without parser/media gaps and 250 retain explicit
partial states; none failed. Their context aliases, ordered media, and
checksummed source spans are in `supplements.json` and the private candidate
queue. They are not counted as paper articles. A reference page's successful
export establishes source reproducibility, not agreement with print.

## Validation and limits

The full pass built by native group and then passed an independent
`--verify-existing` rebuild and `make check-cd3-reference`. Chromium showed the
root and 9501 group navigation, Korean article text, a resolved 313×132 figure
in `topic-0037`, the figure and original CAB link in `topic-0015`, and the
missing-CAB notice alongside readable code in `topic-0104`. The only observed
console error was a missing favicon. A later browser check followed the
`topic-0004` sidebar link to readable `topic-1052` and opened the provisional
`topic-0859` article with its missing-title note. `topic-0036` retains its
inline C and assembly spacing in the UTF-8 download and rendered paragraphs.

The CD is a secondary transcription. Article boundaries, CD date/page labels,
text, figures, and CAB contents have not been checked against physical magazines.
The [reading room](READING-ROOM.md) now includes CD3 through its version 2
adapter, retaining native date groups, article identities and explicit gaps.
Library TOCs still end at 1993-12. Paper/OCR comparison, verified corrections
and any publication decision remain separate follow-up work.
