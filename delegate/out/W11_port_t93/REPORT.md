# W11: port of the T93 wording fixes to the 16-page paper and the supplement sources

Nothing committed or pushed. Edits by exact-string python replacement (each old string asserted to occur exactly once per file).
Files edited: `paper/ieee/sections/*.tex` and `dist/tog/long/*.tex` (same edits in both; line numbers differ only where noted).
`dist/tog/sections`, `dist/tog/supp_src`, figures and `dist/tog/tools/build_supplement.py` were not touched (no REP needed updating; the build did not abort).

## Table

| # | Fix | paper/ieee (file:line) | dist/tog/long (file:line) | Status |
|---|---|---|---|---|
| 1 | Abstract "no whole-board position of at most six pawns" | 00_abstract.tex:5 | 00_abstract.tex:5 (older equivalent wording, left as told) | not changed: paper/ieee already has it |
| 2a | "just two nimbers above $0$" | 06_atlas.tex:11 | 06_atlas.tex:11 | ported |
| 2b | highest temperature without "apart from $\pm\BIG$" | 06_atlas.tex:41 | 06_atlas.tex:41 | adapted: "Among the atlas values free of $\BIG$, the highest temperature under the textbook test is $3$," (long text is in a subsection, no "their") |
| 2c | cylinder-only defined inside the atlas | 06_atlas.tex:47 | 06_atlas.tex:47 | ported: "occurs on a cylinder of the atlas but on none of its ordinary boards" |
| 2d | 3/4 reached by an ordinary board with six pawns | 06_atlas.tex:56 | 06_atlas.tex:56 | adapted: new sentence "An ordinary board also reaches $3/4$ under the textbook test, with six pawns: \pos{W a2 a4 b3 / B a7 b6 b7} \lab{C2}." after the Fig. hot3(b),(c) sentence |
| 3a | "we value a position as the sum of its components (Section~\ref{sec:sums-hss} tests this)" | 02_rules.tex:110 | 02_rules.tex:110 | ported |
| 3b | "(We use) $\BIG=256$, enough on boards up to $8\times8$" | 02_rules.tex:31 | 02_rules.tex:31 | adapted in long to its wording: "(our programs use $\BIG=256$, enough on boards up to $8\times8$)" |
| 3c | stops: "both play well until a number appears" | 02_rules.tex:22 | 02_rules.tex:22 | adapted: "both sides play well until a number appears" |
| 3d | "In these examples a move the opponent can answer with a passed pawn loses and drops out" | 03_basic.tex:5 | 03_basic.tex:5 | adapted: "In these examples a move that the opponent can answer with a passed pawn is a losing move" |
| 4a | "On the whole board the first passed pawn ends the game" | 05_sums.tex:88 | 05_sums.tex:88 | ported |
| 4b | "wins on the whole board" | 05_sums.tex:90 | 05_sums.tex:90 | ported |
| 4c | "They agree on these headline values:" | 05_sums.tex:141 | 05_sums.tex:138 | adapted: "The two models agree on these headline values:" |
| 5a | tinies for "a number $x>0$" | 07_targets.tex:6 | 07_targets.tex:6 | ported |
| 5b | table note: no census position tiny(x) for dyadic $x\notin\mathbb{Z}$ below 8, denominator at most 16 | 07_targets.tex:30 | 07_targets.tex:30 | adapted: note now reads "(count rule); no census position is $\tinyg{x}$ for a dyadic $x\notin\mathbb{Z}$ below $8$ with denominator at most $16$. Textbook column: ..." (kept on the same lines) |
| 5c | remove "Unlike Fig. 2(c), it needs no seam." | 07_targets.tex:83 | 07_targets.tex:83 | ported (long wording was "Unlike the Tiny~1 of Section~\ref{sec:basic-inf}, it needs no seam.") |
| 6 | "is a feature of the textbook test." | 09_real.tex:44 | 09_real.tex:44 | ported |
| 7a | classes "in the model under the textbook test" | 12_engines.tex:9 | 12_engines.tex:9 | ported |
| 7b | Stockfish "plays a tablebase-best move in all 233 positions at $10^5$ nodes, and in 232 already at $10^3$" | 12_engines.tex:16 | 12_engines.tex:16 | ported |
| 8a | "(Table ...; White to move throughout)" | 10_tablebases.tex:50 | 10_tablebases.tex:49 | adapted: the long text has the table reference in the lead-in sentence "...can force mate (Table~\ref{tab:tb}; White to move throughout)." |
| 8b | "The standard bishop-and-knight mate needs a corner" | 10_tablebases.tex:55 | 10_tablebases.tex:54 | adapted: "their standard mate needs a corner of the bishop's color" |
| 9 | group T placed beside the ordinary-board pawn positions of Sections targets--real | 04_kings.tex:19 | 04_kings.tex:19 | ported ("beside the ordinary-board pawn positions of Sections~\ref{sec:targets}--\ref{sec:real}"; both labels exist in the long version; the two 04_kings files are byte-identical, `cmp` ok) |
| 10a | "in our six-rank sweep a square-rule passer test" | 14_conclusion.tex:4 | 14_conclusion.tex:3 | ported |
| 10b | mis\`ere item: "each strip's mis\`ere outcome gives a cylinder's" | 14_conclusion.tex:25 | 14_conclusion.tex:23 | ported |
| 11a | "the least known ring" | (no matching sentence; the Fig.~least sentence is not in the long text) | (same) | not present |
| 11b | "If a pawn inside a wall moves, ... so these moves lose" | 08_star2.tex:150 | 08_star2.tex:150 | ported |
| 11c | "eight ten-pawn rings are $\nim{3}$, six of them also as sums" | 08_star2.tex:166-168 | 08_star2.tex:166-168 | not changed: the long text already says "three programs agree on all eight \lab{C2}, and as sums six keep the value" in the same passage |
| 12a | "(order 638, P-portion of size 109)" | 11_dawson.tex:87 | 11_dawson.tex:87 | ported |
| 12b | "a push with no untouched neighbor only blocks its file" | 11_dawson.tex:45 | 11_dawson.tex:45 | ported |
| prev | FEN wording ("main position with kings") | appendix_positions.tex:3 | appendix_positions.tex:3 | already present |
| prev | "machine-checked for $n\le16$" | 11_dawson.tex:68 | 11_dawson.tex:68 | already present; no `n\le22` anywhere in either tree |

Not ported on purpose (space trims of the 10-page paper): shortened "derivations are standard" sentence, removed "With $\BIG=256$ the move bound ..." sentence (the long text still has it, 05_sums.tex:118/115), removed `\lab{Conj}` definition, removed ", the least a ring can have,", "(Section~S4)" replacing "Section~S4 shows examples" (not in the long text anyway).

## Line counts of dist/tog/long/*.tex

Before and after identical for all 17 files (total 1393). (My first pass added one line to 07_targets.tex by a line break in the table note; fixed before the final build.)

## Builds

- `sh dist/tog/rebuild.sh`: tog 10, tog_review 10, supplement 67, supplement_review 67; "RESULT: all numbers found"; anon hits 0 and 0; overfull/undef-ref count "0 2" (two 2.4 pt overfull hboxes in the supplement log, lines 569 and 71--73 of the log's paragraphs; not checked whether they predate the edits). No build_supplement.py assertion fired. The script also refreshed `dist/tog/submission/files_to_upload.md` and `pdf_checks.md` (sizes and hashes), as it does on every run.
- Long version (tectonic, cache only): `main.pdf` 16 pages, `main_review.pdf` 16 pages. PDFs copied to `paper/Bhattacharjee_Cylinder_Chess_IEEE.pdf` and `paper/Bhattacharjee_Cylinder_Chess_IEEE_review_anonymous.pdf`. Only font-shape warnings in the log.
- `bash dist/arxiv/build.sh`: "RESULT: all arXiv rule checks passed".

## Text check (pdftotext, whitespace joined)

Long PDF: every ported phrase is present and every old phrase is gone (items 2--12 checked; the remaining "is blocked" hits are other, unrelated sentences).
Supplement PDF: the phrases of items 2a, 2c, 3d, 4c, 6, 8, 10b, 11b, 12 are present, and no old phrase survives. Fixes in sentences the supplement does not cut out (3a-3c, 4a-4b, 5, 7, 9, 10a, 2d) do not appear in it at all, new or old.

Old phrases that survive in the supplement because they come from `dist/tog/supp_src` or a string in `build_supplement.py`: none found (searched for every old phrase; the only grep hits were unrelated uses such as "blocked", "wall moves in Lemma 2" at `dist/tog/supp_src/s15_note2.md:46`, "beside every context" at `dist/tog/supp_src/s12_kings.md:1904,1908`, and `BIG=256` at `dist/tog/supp_src/s12a_core.tex:220,303`, which says nothing about the bound being enough on boards up to 8x8 beyond its own proof).
