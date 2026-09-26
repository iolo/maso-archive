# CD3 private readable reference

The private output is `build/cd3-reference/index.html`, a portable static
HTML/text/image reference built from the supplied CD3 ISO and checksummed M14
decoder probes. It is about 992 MB of files. Original media and recovered bodies
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
4. Run `make check-cd3-reference`. It checks 5,664 output files, all candidate
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

## Coverage and exceptions

The main RTF has 2,336 topics. Native title footnotes identify **967 article
candidates** in 18 provisional groups. Every candidate has readable text and
an explicit outcome: **792 success, 175 partial, none failed or blocked**.
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

The remaining **1,369** RTF topics are classified separately: 12 author bios,
1,355 auxiliary topics, and two document tails. Their context aliases, ordered
media, and checksummed source spans are in `supplements.json` and the private
candidate queue. They are not counted as paper articles. A reference page's
successful export establishes source reproducibility, not agreement with print.

## Validation and limits

The full pass built by native group and then passed an independent
`--verify-existing` rebuild and `make check-cd3-reference`. Chromium showed the
root and 9501 group navigation, Korean article text, a resolved 313×132 figure
in `topic-0037`, the figure and original CAB link in `topic-0015`, and the
missing-CAB notice alongside readable code in `topic-0104`. The only observed
console error was a missing favicon. `topic-0036` retains its inline C and
assembly spacing in the UTF-8 download and rendered paragraphs.

The CD is a secondary transcription. Article boundaries, CD date/page labels,
text, figures, and CAB contents have not been checked against physical magazines.
The implemented reading-room SPA still ends at 1993-12. Paper/OCR comparison,
verified corrections, 1995 SPA integration, and any publication decision are
separate follow-up work.
