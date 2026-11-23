# R7: audit of the long version (paper/ieee) against the 10-page version (dist/tog)

Scope: `dist/tog/sections/*.tex`, `dist/tog/tog.tex` (reference) against `paper/ieee/main.tex`,
`paper/ieee/sections/*.tex`. `dist/tog/supp/*.tex`, `dist/tog/supp_src/s12a_core.tex` and `RESULTS.md` (latest
entries, 2026-11-22/23) were used to decide which side is current. Nothing was edited or built. `main.pdf` is newer
than every `.tex` of the long version (09:49 on 2026-11-23), so `pdftotext` reflects the sources.

Result in one line: the long version already carries most of today's edits (sum model with the moved component
tested first is only half-worded, Möbius families S in section VIII, engines "no conclusion", HSS threats in any
order, "X has no passed pawn"). Real defects: the certificate of horizon is worded differently from (C1)-(C3); the
conclusion still treats the Möbius least ring as open; one result (nine-pawn nim3 on six Möbius files) is missing;
the S(X) sentence does not say "the moved component".

Counts: Task 1: 4 own findings (+3 cross-referenced); Task 2: 1; Task 3: 6 (a:1, c:1 [same as T2], e:4, b/d/f:0);
Task 4: 0; Task 5: 2 minor.

---------------------------------------------------------------------------------------------------------

## Task 1. Statement-by-statement disagreements (long vs 10-page)

All theorems, propositions, corollaries, definitions and labelled sentences of the 10-page text were matched.
Disagreements only:

| # | 10-page | Long | Problem | Current |
|---|---|---|---|---|
| 1.1 | `dist/tog/sections/08_star2.tex:135`: "Nine pawns give a $\nim{3}$ on five and on six files \lab{C2}." | `paper/ieee/sections/08_star2.tex:195-196`: only the five-file nine-pawn ring `W b4 c2 d2 e5 / B a6 a7 c6 d5 e7` is given; six files missing | A result is missing from the long version (the six-file nine-pawn Möbius nim3). RESULTS.md (entry "Pawn rings on the Moebius strip 2026-11-22": "*3 with 9 pawns on n = 5 and n = 6") and `dist/tog/supp/s06.tex:136-137` (ring `B7 W4 W23 B5 W3B7 W4B7` on six files, C2) support the 10-page text | 10-page |
| 1.2 | `dist/tog/sections/01_intro.tex:49`: "with the e.p.-aware test the textbook $\nim{2}$ candidate is not $\nim{2}$, however draws are treated" | `paper/ieee/sections/01_intro.tex:49`: "with the new test ..." | "the new test" is undefined in the introduction (the long version has no earlier mention); the claim in sec. IX is for the e.p.-aware tree (Theorem oracle-cand (b)) | 10-page |
| 1.3 | `dist/tog/sections/08_star2.tex:124-125`: the sentence "Wall insertion gives a whole-board nim3 with n+2 pawns on every cyl n with even n>=8 and odd n>=11" has no label; only "n+1 on cyl11 [C2]" and "n>=12 [S]" are labelled | `paper/ieee/sections/08_star2.tex:168-170`: "... odd n>=11 \lab{S}" | Long is labelled, 10-page is not. No change to the long version; the 10-page text should carry \lab{S} on the n+2 families (long is the right form) | long |
| 1.4 | `dist/tog/sections/04_kings.tex:96-100` and `paper/ieee/sections/04_kings.tex:96-100`: Theorem cert: "holds wherever every move in $Z$ has one" | identical | Both versions: Remark A.17 of `s12a_core.tex` says certificates are needed "for every Z-move at every position" of the reachable set R(Q), not only at the root. Low priority wording, identical in both | supplement A.17 |

Cross-referenced (counted under later tasks): S(X) wording (3a); certificate clauses (3e); conclusion item 5 (2/3c).

Replacement for 1.1 (long, after `08_star2.tex:196`, in the Möbius paragraph): change
"On five files the nine-pawn ring ... is $\nim{3}$ \lab{C2}, while $\cyl{5}$ has no $\nim{3}$ ring with nine pawns or fewer \lab{C1}."
to
"On five files the nine-pawn ring \pos{W b4 c2 d2 e5 / B a6 a7 c6 d5 e7} is $\nim{3}$, and so is a nine-pawn ring on six files \lab{C2}, while $\cyl{5}$ has no $\nim{3}$ ring with nine pawns or fewer \lab{C1}."

Replacement for 1.2 (`paper/ieee/sections/01_intro.tex:49`): "with the new test" -> "with the e.p.-aware test".

---------------------------------------------------------------------------------------------------------

## Task 2. Headline numbers of the long version's abstract, introduction, conclusion

Abstract: identical to the 10-page abstract word for word (six/seven pawns, three programs, six pawns on three
files, ten files, ten-pawn rings on seven files, 1/8, up-second star, Tiny 1, "ring is a first-player win
exactly when the strip three files shorter has Grundy value zero"). Introduction: 2.80%, 233, 92.5% / 2,049, 10-man,
n+1 on cyl 11 and n>=12, ten on cyl7..10, six on cyl3, all as in the 10-page version. Conclusion: 92.5% of 2,049,
nine pawns nim3, 11% undecided KPKP (10-page supplement `s08.tex:115-116`: 89% decided; `s10.tex:15`: 11%),
n+3 for 3<=n<=7, ten for 7<=n<=10, n for n>=10, nim3 n+2 / n+1 (as `s10.tex`), h approx 5-7: all agree.

| # | File:line (long) | Problem | Replacement |
|---|---|---|---|
| 2.1 | `paper/ieee/sections/14_conclusion.tex:20-23` (item 5) | "the least ring nim2 is known up to eleven files and one pawn per file suffices from ten files on; the least for n>=12 and the kings remain open." Self-contradictory: a ring has at least one pawn per file, so one pawn per file for every n>=10 (proved, label S, sec. VIII) makes the least equal to n for every n>=10. Not open. The same stale sentence stands in the 10-page supplement `dist/tog/supp/s10.tex:~17-18` ("known for n<=11 ... the least for n>=12 and the kings remain open"); it needs the same fix | see below |

Replacement for the whole item (long):

```
\item \emph{Endgames without edges.} With at most one new piece, $11\%$ of KPKP positions on the cylinder
  stay undecided, and KPPK comes next. On the M\"obius strip, where a pawn that
  crosses the seam reverses direction, the least ring $\nim{2}$ has $6, 8, 6, 8, 8, 8, 10, 10, 11$ pawns for
  $n=3,\dots,11$ files and $n$ pawns, one per file, for every $n\ge10$ \lab{S} (Section~\ref{sec:star2}); the kings
  on the strip remain open.
```
(The sequence 6,8,6,8,8,8,10,10,11 is RESULTS.md "So the least ring *2 on the strip is ... for n = 3..11"; the
8-file value is the isolated ring, C2.)

---------------------------------------------------------------------------------------------------------

## Task 3. Changes of today

### 3a. Sum model S(X): moved component tested first

| # | File:line (long) | Problem | Replacement |
|---|---|---|---|
| 3a.1 | `paper/ieee/sections/05_sums.tex:91-94` | "after a move, a component in which a side has a passed pawn becomes $\pm\BIG$ (by the race rule if both have one); otherwise it is re-split ... The test comes before the split." Does not say that only the MOVED component is tested (any other component cannot have a passed pawn, since it would already be frozen, but the theorem and the engine test the moved one: RESULTS.md, "Wording error found in the paper and fixed"). 10-page (`05_sums.tex:44-47`) says "the moved component becomes $\pm\BIG$ if a side has a passed pawn in it (by the race rule if both have one); otherwise it is re-split along empty files (one ring if no file is empty)". | Replace the clause by the 10-page wording and keep the last sentence: "and $S(X)$ for its sum model: after a move, the moved component becomes $\pm\BIG$ if a side has a passed pawn in it (by the race rule if both have one); only otherwise is it re-split along empty files (one ring if no file is empty); and the components add up. The test comes before the split." |

### 3b. Hereditary sum safety

Long `05_sums.tex:98-100` (reachable = moves of either side in any order; threats; "opposite threats") and
Theorem hss `:103-107` ("Suppose that $X$ has no passed pawn and is HSS ...") and Theorem validity
`04_kings.tex:54` ("let $X$ ... have no passed pawn") match the 10-page text. No finding. (No sentence in the long
version still says "alternating".)

### 3c. Möbius strip: see 2.1. The body (`08_star2.tex:188-204`) is current (label S, "every n>=10", base case 435
or 417 positions, "seam only changes that base"). No "up to 32 files" anywhere in `paper/ieee`; only the conclusion is stale.

### 3d. Engines on sums
`paper/ieee/sections/12_engines.tex:63-73`: "So we draw no conclusion from them", random baseline 49%, 163/200, 61,
27, 13 of 13. The introduction (`01_intro.tex:56`) claims only the 233-position suite. No finding.

### 3e. Certificate of horizon h: long (`04_kings.tex:89-93`) against (C1)-(C3) of `s12a_core.tex:317-337`

| # | Clause | Long says | (C1)-(C3) says | Difference |
|---|---|---|---|---|
| 3e.1 | (i) goal | "the punisher promotes within $h$ of its own moves after its reply" | (C1): promotes OR checkmates ("a checkmate of $s$ is a win for $\bar s$") within its first $h$ moves | Long allows promotion only: a mate-only certificate is not covered. The long form is stronger as a hypothesis (so the theorem is still true), but not the same clause. The 10-page text says "promotes or mates". |
| 3e.2 | (i) rules of the local game | "with the pawns outside $Z$ removed ... even if the defender may pass" | The defender may pass only when not in check; the punisher may not pass and its king may step only onto the files of $Z$; the reply $r$ must be a Z-move that does not promote and leaves the king on those files; a promotion by the defender is a failure | Long omits: no pass in check; punisher never passes, king stays on $F_Z$; the defender promoting first (with its Z-pawns) counts as failure. The last one matters because long (ii) says the defender's Z-pawns "fall under (i)". Counting: both count the punisher's moves AFTER its reply r (not the reply itself): same. |
| 3e.3 | (ii) which defender moves | "no defender pawn in the context can promote within $h$ of its own moves" | (C2): in $Q^\circ$ only the defender moves, king AND pawns; its king steps on squares holding no own pawn and not attacked by a punisher pawn (it may capture); punisher context pawns stay put, no e.p.; every sequence ending in a promotion has at least $h+1$ moves | Long counts "defender pawns" only; (C2) counts any sequence of defender king and pawn moves (a king capture that opens a file counts). Same bound ($>h$ moves = "cannot promote within $h$"). The defender's pawns in Z are excluded in both (covered by (i)). |
| 3e.4 | (iii) stalemate | "the defender is never stalemated on the forcing line" | (C3): the punisher has a guided strategy, each move a winning move of the local game, such that in NO play following it is the defender stalemated before the punisher's $h$-th move | "on the forcing line" (singular) reads as one line; (C3) quantifies over all defender replies and the strategy. Same clause, wording weaker. |

Also Theorem cert (long `04_kings.tex:96-100`): identical to the 10-page text and to `dist/tog/supp/s02.tex:11-15`.
"Clause (ii) cannot be weakened to $h-1$ moves": supported only by the sharpness example at
`dist/tog/supp/s12.tex:969` ("(L2), sharpness of mu_s >= T+1": `Kf5 kc6 Pe4 pb3`, T = 2 = mu_s, White wins in P; with the
pawn on e3, mu_s = 3 and Black wins), and not stated in Theorem A.16. In the supplement's terms (ii) reads "mu_s >= h+1"; "weakened to h-1 moves" means allowing mu_s = h, which fails. Consistent, but the sentence is not proved in A.16; in the long version it can stay with a pointer "(the example is in the repository)" or be rewritten as below.

Replacement for the long sentence group `paper/ieee/sections/04_kings.tex:89-93` (close in length to the present text, in the long version's own words):

```
A local test for (V3) is the \emph{certificate of horizon $h$} of a move in $Z$. Let the punisher answer with a move
in $Z$ that does not promote and leaves its king among the files of $Z$, and call the position then reached $Q$, with
the defender to move. (i) With all pawns outside $Z$ removed, the punisher wins the local game: whatever the
defender does, and even if it may pass whenever it is not in check, the punisher (who never passes) promotes or mates
with one of its first $h$ moves counted from $Q$, and the defender promotes first in no play. (ii) With the
punisher's king and all pawns in $Z$ removed, and the defender alone to move, no sequence of defender king and pawn
moves ends in a promotion within $h$ moves (a king may capture, never steps onto a square attacked by a punisher
pawn, and the punisher's other pawns stand still); the defender's pawns in $Z$ fall under (i) (the
\emph{counter-promotion condition}). (iii) The punisher can follow its winning strategy of (i) so that in no play is the
defender stalemated before the punisher's $h$-th move. It works in the \emph{promotion game}, where the first
promotion wins.
```

### 3f. A pawn on its last rank counts as passed
No sentence of the long version contradicts it and none states a board-height condition for the validity theorem
(the only height condition is Proposition horizon1, "at least six ranks", whose proof says a pawn that can promote in one
move stands on the rank before the last; that is compatible with the convention). The convention itself is not
written in either version (grep "last rank" in `dist/tog/sections` and `paper/ieee/sections`: no hit); the supplement
has it (`s12.tex:56`, `:123`, `:426`) and states H >= 5 for the validity theorem (`s12.tex:219`, `:286`: "The main
text leaves implicit that the board has at least five ranks; all its boards with kings have at least six"). Optional
addition (long version, `02_rules.tex`, end of the Normal Play subsection after line 44): "A pawn that reaches its last
rank stays a pawn, cannot move, and counts as passed under every test, as in our engine; the theorems on kings assume
a board of at least five ranks."

---------------------------------------------------------------------------------------------------------

## Task 4. Internal hygiene of the long version
- `pdftotext paper/ieee/main.pdf -` : no "??" (also none in `main_review.pdf`). 15 pages. `main.log`: only 4 font-shape warnings (TU/ptm), no undefined or multiply-defined labels.
- `\ref`/`\eqref` to non-existing labels: none (scripted over `main.tex`, `sections/*.tex`, `macros.tex`).
- Duplicate labels: none.
- `\cite` keys missing from `paper/ieee/refs.bib`: none.
- Phrases only meaningful in the 10-page version ("Section S6", "the supplement", "supplementary material", "Section~S"): none. "in the repository" occurs at `05_sums.tex:112` and `01_intro.tex` (intentional). `01_intro.tex:59` "The Appendix gives each position with kings in FEN" matches `appendix_positions.tex`/`appendix_table.tex`.
No findings.

---------------------------------------------------------------------------------------------------------

## Task 5. Acknowledgment and AI-use statement

Long, `paper/ieee/main.tex:156-176` (named build; mentor name replaced by [mentor] here):
"The author thanks Prof. [mentor] for mentoring the 2025 study on which this work builds, and the maintainers of the Lichess tablebase, Stockfish and Lc0 for making their tools freely available. AI coding assistants (Claude, Anthropic; Codex, OpenAI; and open models run through the OpenCode and Kilo tools) wrote and ran, under the author's direction, the software for the simulations, endgame searches, tablebases and cross-checks of Sections II--XIII and the scripts that draw the figures, wrote the full proofs kept in the repository, and helped draft and edit the text of all sections. The author chose the research questions, directed the work and is responsible for all content."

10-page, `dist/tog/tog.tex` (same place): identical except "... wrote the full proofs of Sections S12--S15, and helped draft ...". The anonymized branch is identical in both with the same single difference (and "The authors"). 

| # | Difference | Substance | Action |
|---|---|---|---|
| 5.1 | "the full proofs kept in the repository" (long) versus "of Sections S12--S15" (10-page) | Intended: the long version has no supplement | none |
| 5.2 | "Sections II--XIII" in both. In the long numbering II-XIII is Rules to Verification (Conclusion is XIV), correct. In the 10-page numbering (no "Basic positions" section) XIII is the Conclusion, which contains no software or cross-checks; the software is in II--XII | Cosmetic, in the 10-page text | optionally change `dist/tog/tog.tex` to "II--XII" |

The disclosure of AI referees ("AI referees, some from another vendor, checked them ... no human referee has yet")
is in section "Verification" of both versions, identical.

---------------------------------------------------------------------------------------------------------

## Checked and fine
- Abstract, keywords, section order (long has extra sections III Basic, appendix table, sec. XIII Verify text) and the
  evidence-label legend (only the proof location differs, intentionally).
- Rules: Definition e.p.-aware, census count 18,137 / 231,071 / 4,070 [C1], nine settings, cut lemma [P],[C2].
- Kings: opening paragraph (1,418,480 [C2]), trébuchet claims [C2], Theorem validity [S], Corollary V4 [S],
  Proposition horizon1 [S], Conjecture horizon2, h 5-7 [Conj], locked pair [C2], loopy theorem [S] (long has it,
  10-page moved it), K+P-vs-K [C2], sweep numbers 500/159/107/18/34/52/31/128, 2,154/105/2,049/92.5%/83%/84% [C1].
- Sums: Definition hss, Theorem hss [S], 599,098 / 540,503 / 19.3% [C1], Proposition sumcounter [C2], two models,
  19 real-king sums / 38 / 19 [C1]. Long additionally proves Proposition condE [C1] (10-page only points to S3).
- Atlas and Targets: 1,223,689 / 12,568 / 4,000 / 231,071 / 459,443, 53 cylinder-only (40+13) [C1], Table of targets,
  Theorem eighth [C2], upsec star and Tiny 1 labels.
- Star2: Theorem census [C2] (6,724 zeros, 4,042 stars, 793,299, 292), Theorem star2seven [C2], table of settings,
  counts 5,503,282 [C1]/[C2], ring minima n+3 (3..7) [C2], ten on cyl8-9 [C2], n per file n>=10 [S], wall families
  n+3 n>=5 [S] with n<17 [C2] and n<=12 sums [C1], nim3 nine pawns [C2], eight pawns none [C1], cyl7 eight rings [C2],
  n+1 cyl11 [C2] and n>=12 [S], heights [C2], no nim4 [C1], Möbius 6,8,6,8,8,8 and 10,10,11 [C2], n>=10 [S].
- Real chess: definition, Lemma sandwich [P], Theorem oracle-cand [C1]/(a)[C2], Proposition eighth-real [C1],
  302 / 290 / 283 / 5 / 2, 10 and 12 open end positions [C1], A and B 8-man [C2].
- Tablebases: 24 tables, 607 million [C2], Table, 2.80%, KRK Möbius / Klein 0.66% [C2], KPK 326,640 / 6 / 16,538 /
  15,930 / 216 vs 160 [C2]; long adds the width table and KPKP (as in 10-page supplement S8).
- Dawson: Grundy recurrence, period 34, exception 51 [C2], 31 of 301 and 56 [C2], Theorem ring [P], misère
  quotient 638 / 109 [C2], list n = 3,7,11,17,...
- Engines: 233 / 181 / 52, Stockfish figures and table, Lc0 [C1], ChessSums 26,000 / 418 / 37 / 5 / 4,887 / 4-9x,
  no-conclusion wording on the 200-sum test.
- Verification: 55,195 / 4,967,550 / 2,483,775 / 1,070 / 160, AI-proof statement.
- Hygiene (Task 4) clean; theorem numbering and labels have no duplicates; no leftover supplement pointers.
- Note for the 10-page side only: the supplement's open-problem list `dist/tog/supp/s10.tex:~17-18` has the same
  stale Möbius sentence as 2.1.
