# ToG 10-page version: what changed

Source: `paper/ieee/` (long version, 15 pages named / 14 anonymous), copied here and edited. `paper/` was not touched.
`long/` holds an untouched copy of `paper/ieee/sections/`, which `tools/build_supplement.py` reads.

## Builds and measured size

Build everything with `sh sbuild.sh` from `dist/tog/` (each step is `tectonic -X compile --only-cached ...`):

| PDF | Pages | Notes |
|---|---:|---|
| `build/tog_review.pdf` (anonymous, `tog_review.tex` = `\def\anonbuild{}\input{tog}`) | **10** | right column of p. 10 ends 4.36 in above the bottom margin: **4.36 column-inches free**, i.e. about **9.78 pages** used |
| `build/tog.pdf` (named) | 10 | 3.66 column-inches free (the author footnote costs ~0.7 in) |
| `build/supplement_review.pdf` (anonymous) | 87 | S1–S11 moved material (pp. 1–13), S12–S16 full proofs (pp. 14–87) |
| `build/supplement.pdf` (named) | 87 | |

Logs: no overfull box and no undefined reference or citation in either paper build (`build/tog_review.log`,
`build/tog.log`). No table of contents in either paper build. `sh freespace.sh build/tog_review.pdf` re-measures the
free space.

Free space: the target was about 9.7 pages; the anonymous build ends at about 9.78 pages, with 4.36 column-inches
free in the last column, enough for the 3–4 column-inches reserved for the two pending results. Their slots are the
comments `% SLOT: real-king sum test` (end of Section V, `sections/05_sums.tex`) and `% SLOT: Möbius rings`
(Section VIII-E, `sections/08_star2.tex`, before the closing paragraph). If they need more, the cheapest next cuts
are the Section VIII-D five-file sentence and the Section X twisted-board sentence (both are in the supplement in full).

## Global changes

- Title shortened as AUDIT §2.1 suggests: "Combinatorial Game Values and Tablebases for Chess Endgames on a
  Cylindrical Board"; running heads "... on a Cylindrical Board".
- `\anoncodeurl` defined once at the top of `tog.tex` as the text "anonymized repository link"; the anonymous
  `\codeavail` is "available at \anoncodeurl". Replace its definition by the anonymous.4open.science `\url{...}`.
- Named author footnote copied from the current `paper/ieee/main.tex` (University of Illinois Urbana-Champaign).
- `refs.bib` re-copied after the coordinator's DOI update (five DOIs).
- Every "in the repository" proof pointer now says "in Section S*n* of the supplementary material".
- Appendix (FEN table and text) removed from the main text (→ S11); the Introduction ends with one sentence on
  the supplementary material.
- Theorem counter: 16 numbered statements instead of 21 (Thm 5, Prop 6, Conj 7, Thm 8, Prop 12 moved).
- Board figures regenerated (`make_figures.py`, "small" preset: coordinate labels 12.5 pt instead of 9 pt). All
  main-text boards are included at 0.32\columnwidth (scale 0.67), so labels print at about 8.4 pt. The Grundy plot
  (Fig. 7) and Figs. 1, 6 are included at natural size (8 pt text or more). Supplement boards: 6 small boards at
  0.165\textwidth (≈8.0 pt), atlas boards at height 1.1 in (≈8.1 pt), others larger.
- Section numbers I–XIV are unchanged (Section III kept as a short section so the AI statement "Sections II–XIII"
  and the coordinator's slot references stay valid).

## Section by section

| Section | Stayed | Shortened | Moved (supplement section) |
|---|---|---|---|
| Title, abstract, index terms | abstract and keywords verbatim | title (AUDIT §2.1) | – |
| I Introduction | cylinder, CGT/Elkies conventions, three changes, ⋆2 question, 2025 study relation and what is corrected (now pointing to Table I and Section XI), label definitions | contributions: 8 bullets → 6 (Model+Kings merged; Tablebases+Dawson merged); nimber definition moved to II-B; wide Fig. 1 (ring M_10) added at the top of p. 2 | FEN pointer → S11 |
| II Rules | board and moves, Def 1, cut lemma, race rules, nine settings, the 18,137/231,071 statistic (one sentence) | Notation to one paragraph (now also defines nimbers, up, Tiny 1); conventions as one paragraph + the race-rule list; new compact Fig. 2 (e.p. test, seam zero, seam Tiny 1) replaces Figs. 1 and 2 | six-board Fig. 2 and the "few more hidden changes" remark → S1 |
| III Basic positions | seam zero, the 2 vs ⇑⋆ e.p. remark, seam Tiny 1 | to the two seam positions | derivations of 1, 2, ⋆, ↑, ⇑⋆ → S1 |
| IV Kings | intro (1,418,480 test positions), the two trébuchets, Fig. 3 (a)–(c), Thm 3 + sketch, Cor 4, failure list, IV-D headline (500/159/107/18/34/13/52/128, 92.5%, 83%) | certificate theory to two sentences | certificate definition, Thm 5, small-margin examples, (V2) local test, Prop 6, Conj 7, h≈5–7, loopy Thm 8 and the K+P census, the 143-of-159 and 8×8 king-move check (94/449/41/7), new Fig. f3 → S2; full proofs → S12 |
| V Sums | Table I (all 8 rows), HSS, Thm 6, sample 1,500/1,297, Prop 7, "two models" | two principles to two sentences; puzzle walk-throughs to one paragraph of results; two-models paragraph halved | puzzle figure and walk-throughs, Prop 12 (condition E), the full two-models paragraph → S3; sum-safety proof → S12 |
| VI Atlas | definitions and counts, two nimbers, Prop 8, robustness | one example (3/4) | hottest ±3 walk-through, Fig. 5, C3/C4 examples → S4 |
| VII Small values | Table II, Fig. 4 (1/8, ↑²⋆, Tiny 1), Thm 9 | walk-throughs to a few lines; legality derivations kept; "two textbook values that fail" to one sentence | mirror-image legality argument, full walk-throughs, the two failing textbook values → S5 |
| VIII ⋆2 question | candidate value, Thm 10 + checkers, Thm 11 + A walk-through, Table III, counts/five files headline, ring minima, walls, n+3 / n / n+2 / n+1 families, ⋆3 with nine pawns, no ⋆4 (134,920,191 + 24 million), nim-sum of cores | candidate to one paragraph; B to one sentence (mirror of A); ring census replaced by Fig. 6 (f2, least pawns, instead of the plan's new table) + one paragraph per topic | full candidate and B walk-throughs, the game histories of A and B, every listed ring, count and check per cylinder (Section VIII-D of the long version verbatim) → S6; wall proofs → S13–S15 |
| IX Real chess | Def 12, Lemma 13, Thm 14, Prop 15, 15.6 h / 6.1×10^10, second candidate, A/B status | 1/8 search narrative to 5 lines | full narrative, five-file ⋆2 status → S7 |
| X Tablebases | Table IV, 2.80%, torus, bishops, Möbius/Klein one line, KPK headline (326,640; 6 rook-promotion positions; 16,538 / 15,930; 216 vs 160) | rules+verification to 4 lines; rook pawn described in text | Table V (KPK counts), Fig. 8 (rook pawn), Table VI (other widths), "A pawn each" (KPKP), coloring remark → S8 |
| XI Dawson | rules, (1), Thm 16 + proof, period 34, what was wrong (31/301/56, n=4), misère result (order 638, 109 P-positions) | forced sequence by a third; what was wrong to 3 lines; misère to 2 lines; Grundy plot to column width, n ≤ 80 | Fig. 9 (Dawson boards), the n=4 walk-through, the exhaustive-search check (7.4 million), "a warning about sums" → S9 |
| XII Engines | XII-A/B, Table V (Stockfish by class), Lc0, engines on sums | ChessSums merged into "Engines on Sums" (3 lines); section renamed "Engines and Sums" | "Learning Dawson's chess" → S9 |
| XIII Verification | cross-checks | code-availability sentence now uses `\codeavail` (anonymous: `\anoncodeurl`) and names S11–S16 | – |
| XIV Conclusion | 92.5% summary, 4 open problems (ring minima and ⋆4; real-chess 1/8 and A/B; when a trébuchet is zero; misère Dawson) | 6 problems → 4 | the full list of six (KPKP 11%, Möbius pawn play, …) → S10 |
| Appendix | – | – | FEN text and table → S11 |
| Acknowledgment, references | unchanged | – | PyTorch reference now only in the supplement |

## Supplement (`supplement.tex`, one column, same anonymous switch)

S1 basic positions and e.p. statistics · S2 kings: certificates, loopy games, failure sweep, Fig. S3 (model vs
chess, f3) · S3 puzzles and condition (E) · S4 atlas · S5 small values · S6 ⋆2 details and ring listings · S7 real
chess · S8 tablebases and KPK · S9 Dawson (boards, details, learning) · S10 further open problems · S11 FEN table ·
S12 full proofs: validity (Thm 3 = LOOPY Thm 1.14), Cor 4 (1.14(ii)), sum safety (Thm 6; LOOPY 1.11, 1.14(ii)),
certificates (2.7), horizon-1 (2.10(a)), loopy outcomes (3.4), from `kings/theory/LOOPY.md` §§1–3 · S13 wall rings
n+3 (`research/ring_family_proof/proof.tex`) · S14 n-pawn ⋆2 (`research/ring_n_proof/PROOF_N.md`) · S15 Lemma 3
write-up and ⋆3 families (`research/ring_n_plus_2_proof/PROOF.md`, `PROOF_Q.md`, `PROOF_odd.md`,
`research/star3_proof/PROOF_S3T3.md`) · S16 square-rule test (`research/v2_mechanisms_proof/PROOF_S.md`).

S1–S11 are the long version's text, verbatim, by line range (`tools/build_supplement.py`); references to the main
text print the main text's numbers (the script copies the `\newlabel` lines of `build/tog_review.aux`, since `xr`
is not in the offline bundle). The Markdown notes were converted by `tools/md2tex.py` (pandoc is not installed):
headings, lists, tables (split into ≤18-row tabulars; `longtable` is not in the bundle), code, emphasis; math
passes through. The mathematics was not rewritten. Glyph-level changes only: Unicode sub/superscript digits →
`\textsubscript`/`\textsuperscript`, symbols the text font lacks → math font, `ȳ` and combining macrons →
`\bar{}`, and the local absolute path `/Users/.../Chessendgames/` in one command line of PROOF_S.md → a
repository-relative path (anonymity). The notes keep their own numbering, labels (PROVED, CHECKED-2, …), task
names and file paths; each section starts with a source line and a map to the main-text statements. Typeset log:
no missing glyph, no undefined reference; 18 overfull boxes, the largest 13 pt, in converted tables.

## Plan items not followed, and why

1. **Table I to five rows**: kept all eight rows (saves only 0.4 col-in; the c- and f-file rows show that the
   earlier values were right there, which is part of the relation to the 2025 study).
2. **Intro: drop the per-bullet labels**: bullets cut from 8 to 6, but the labels stay, because without them
   several bullets (n pawns from C_10 on, n+1 for ⋆3) would read as stronger than ⟨S⟩/⟨C1⟩ claims.
3. **New Section VIII table**: replaced by Fig. 6 (`f2_least_pawns.pdf`) as instructed.
4. **Drop the Wikipedia reference**: kept. The sentence attributes two claims to the two prose sources together,
   and offline I could not check which source makes which claim; dropping one could misattribute.
5. **Fig. 9 (Dawson boards)**: moved to S9 to make room for the wide Fig. 1 (the plan said keep, drop if pressed).
6. **Fig. f3 (model vs chess)**: no room; it is Fig. S3 in S2 (with the caveat that the intervals are optimistic).
7. **Merge VI into VII**: not done, to keep the section numbering (I–XIV) that the AI statement and the slots use.
8. **Fig. 3(c)**: kept, as the plan allows (no saving; it illustrates the (V3) failure and Table I's "not mutual").
9. **Biographies**: none (review build).

## Number check

`python3 check_numbers.py > check_numbers.out`: all 32 distinct numbers of the long version's abstract,
introduction, Section VIII and conclusion appear in `tog_review.pdf` or `supplement_review.pdf` (the abstract has
none written in digits). An ad-hoc run of the same test over every long-version section also found no missing
number.

## Fidelity fixes (2026-11-22)

Applied the independent check in `delegate/out/tog_review/REPORT.md` and the coordinator's notes.

- **Title**: the original title is restored (by the coordinator, in `tog.tex` and `supplement.tex`); the
  "Title shortened" entries above are superseded.
- **Main text, BLOCKER**:
  - B1: the Introduction says "with the e.p.-aware test"; Section IX-A ends with "with draws worth $0$ the
    textbook tree is not decided".
  - B2: the corrected long-version sentence ($n+1$ pawns: $\cyl{11}$ ⟨C2⟩, every $n\ge12$ ⟨S⟩).
  - B3: "without the passed-pawn rule ⟨C1⟩" restored in V-B.
  - B4: ⟨Conj⟩ and "so we trust a frozen trébuchet only beside slow or locked components" restored in the
    conclusion.
- **Main text, SHOULD FIX**:
  - S1: the Model bullet as given.
  - S2: the section list.
  - S3: the default setting defined at first use.
  - S4: the textbook/e.p.-aware tree sentence (the inline definitions in Thm 14 are reverted).
  - S5: the certificate defined in IV-B.
  - S8: Fig. 7 now follows the paragraph that cites it; it lands at the top of the page of its first citation (p. 9).
  - S9: last-page balancing is left for after the two slots, as instructed.
- **Main text, MINOR**:
  - M1: census scope in II-D.
  - M2: the ⋆3 note in the Fig. 6 caption.
  - M3: "the two $n$-pawn families above".
  - M4: "(Section S7)" for the other non-default ⋆2 positions.
  - M5: misère P-position clause in XI.
  - M6: ⟨C1⟩ on temperature 3.
  - M8: "(Section V-B)" in the proof of Cor. 4.
  - M7 was not in the requested set and was not applied.
- **Section XIII**: the long version's sentence "The ⟨S⟩ proofs have been checked by computer on their finite parts and by
  independent AI referees; no human referee has checked them yet."
- **Space**: the restored hedges cost about 2 column-inches. To recover it:
  - The five-file sentence of VIII-D is cut (its numbers, 14,680,983 / 21 / 15 and the five-file ⋆2, are in
    S6); VIII-D is renamed "Counts".
  - Small wording cuts in IV-D, V-A, VII and X.
- **Supplement**:
  - S6/S7: `tools/clean_notes.py` post-processes the proof notes before conversion. It removes task and agent IDs, shell
    commands, code blocks with commands, log and script paths, dates of revisions, and the repeated "human check" lines.
    It also replaces first person and "the author" with impersonal wording. One statement at the head of the proofs part
    (before S12) replaces the human-check lines. Paths to the notes typeset here become "Section S13", "Note 1 of
    Section S15" and so on.
  - The math is checked: every `$...$` segment of every note survives the clean-up unchanged (counted per note).
    Sentences with mathematics, statement keywords (Theorem, PROVED, CHECKED-2, …) or numbers are never dropped; only
    their ID/path tokens are removed. The hypothesis names (K1), (K2), (T1)–(T4) are kept.
  - M9: "the long version" no longer appears in S1, S6 or S10.
  - Overfull boxes: converted tables now size each column to at least its longest word and fit the line width
    exactly. The supplement has 0 overfull boxes (was 18), 0 missing glyphs and 0 undefined references.

Measured after the fixes:

| PDF | Pages | Free space |
|---|---:|---|
| `tog_review.pdf` (anonymous) | 10 | 3.36 column-inches in the last column |
| `tog.pdf` (named) | 10 | 1.94 column-inches (longer restored title and the author footnote) |
| `supplement_review.pdf` / `supplement.pdf` | 83 / 83 | – |

- **Checks**:
  - `check_numbers.py`: all numbers found.
  - No overfull box and no undefined reference in either paper build.
  - Both `% SLOT:` comments are kept (`sections/05_sums.tex`, `sections/08_star2.tex`).
