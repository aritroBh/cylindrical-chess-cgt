# From 15 (named) / 14 (review) pages to 10: a cut plan for IEEE Transactions on Games

## How the sizes were measured

Sizes come from the fresh scratch build in `delegate/out/ieee_audit/build/` (named build, same layout as the review
build apart from the table of contents and the byline).

- **Units.** One column is 9.8 in tall, so one page = 19.6 column-inches (col-in). A full-width float of height h
  counts 2h.
- **Section sizes.** Measured with `pdftotext -bbox` from heading to heading, then minus the floats that physically
  land inside that span. Floats are assigned to the section that owns them.
- **Float sizes.** From the top margin to the first text line after the float, so the float separation is included.
- **Accuracy.** The sum of the parts is about 2% above the true 14 × 19.6 = 274 col-in of the review build, so read
  every figure as ±0.3 col-in.

**Budget.** 10 pages = 196 col-in. Allow about 5% for float packing and headings, so the content target is
≤ 186 col-in.

**Supplement.** "Supplementary Material" is one PDF (not counted by ToG) plus the archived repository
(anonymous.4open.science during review, Zenodo DOI after). It holds:
- the full [S] proofs;
- the moved walk-throughs, tables and figures;
- the FEN appendix;
- the per-cylinder ring listings.

## Item-by-item budget

| Item | Now (col-in) | Now (pp) | Verdict | Target (col-in) | Saving |
|---|---:|---:|---|---:|---:|
| Title + byline block (full width) | 4.5 | 0.23 | SHORTEN: two-line title (AUDIT §2.1) | 4.0 | 0.5 |
| Abstract + Index Terms | 3.35 | 0.17 | KEEP (already ~194 of 200 words) | 3.35 | 0 |
| Table of contents (named build only) | 2.45 | 0.13 | DROP from any IEEE build | 0 | (2.45, named only) |
| I Introduction | 15.2 | 0.78 | SHORTEN: contribution list to 6 one-line bullets; move the nimber definition to II-B; drop the per-bullet label strings (one sentence on labels) | 9.5 | 5.7 |
| II Rules, Values, Conventions (text) | 18.8 | 0.96 | SHORTEN: Notation to one paragraph citing [2]–[4]; race rules to one sentence plus the list; move the 18,137 / 231,071 change statistics and the nine-settings detail to the supplement | 13.5 | 5.3 |
| Fig. 1 e.p. test (column) | 1.75 | 0.09 | MERGE into the new compact Fig. 1 (next row) | 0 | 1.75 |
| Fig. 2 basic values (full width, six boards) | 4.8 | 0.24 | SHORTEN to one column-width figure of three boards: e.p. test, seam zero (a), seam Tiny 1 (f); (b)–(e) (1, 2, star, up) are textbook values → supplement | 2.6 | 2.2 |
| III Basic Positions (text) | 11.2 | 0.57 | SHORTEN: keep only the two seam positions and the 2 vs ⇑⋆ e.p. remark; star, up and the ⇑⋆ derivations are standard (cite [5], [10]) → supplement | 6.0 | 5.2 |
| Fig. 3 king groups | 2.5 | 0.13 | KEEP (a) and (b); drop (c) if the puzzles move out (same height, so no saving) | 2.5 | 0 |
| IV Kings (text) | 28.1 | 1.43 | SHORTEN: keep Thm 3 (V1–V3) with its sketch, Cor 4 (V4), and Thm 5 stated with a one-line idea; keep a 4-sentence summary of IV-D (159/500 failures, the 92.5% agreement, the square-rule repair). MOVE TO SUPPLEMENT: the small-margin examples, the (V2) local test, Prop 6, Conj 7, IV-C (loopy Thm 8 and the K+P loopy census) | 19.0 | 9.1 |
| Fig. 4 three puzzles | 2.25 | 0.11 | MOVE TO SUPPLEMENT | 0 | 2.25 |
| Table I puzzles: claimed vs exact | 1.8 | 0.09 | SHORTEN to a 5-row table: it is the in-text statement of what is corrected in the prior study, which ToG requires | 1.4 | 0.4 |
| V Sums (text) | 21.1 | 1.08 | SHORTEN: keep the two principles (2 sentences), Def 9 HSS, Thm 10, Prop 11 and the "two models" paragraph (cut by half). Puzzle walk-throughs → one paragraph of results plus Table I. Prop 12 (condition E) → supplement | 11.0 | 10.1 |
| VI Atlas (text) | 8.4 | 0.43 | SHORTEN: definitions of atlas and census, Prop 13, one sentence on robustness; the ±3 hottest-position walk-through → supplement. Consider merging VI into VII as "VI. Census Results" | 4.5 | 3.9 |
| Fig. 5 atlas values | 2.1 | 0.11 | MOVE TO SUPPLEMENT | 0 | 2.1 |
| VII Elkies' Small Values (text) | 10.1 | 0.52 | SHORTEN: Thm 14 with its 3-line walk-through; ↑²⋆ and Tiny 1 in 4 lines; "Two textbook values that fail" in 2 lines | 7.0 | 3.1 |
| Table II small-value counts | 2.15 | 0.11 | KEEP (drop the "tiny(x), x ∉ Z" all-zero row; put the note in the caption) | 2.0 | 0.15 |
| Fig. 6 1/8, ↑²⋆, Tiny 1 boards | 2.35 | 0.12 | KEEP (headline: legal 10-man positions) | 2.35 | 0 |
| VIII The ⋆2 Question (text) | 33.2 | 1.69 | SHORTEN (hardest cut 1): candidate in 6 lines; Thm 15 plus one sentence on the checkers; Thm 16 with position A's walk-through only (B is its color-reversed mirror, one sentence); VIII-D: replace the ring-by-ring prose with the new table below plus one paragraph on walls (definition, the reduced-game argument, the ⋆2 and ⋆3 families) and one on ⋆3/⋆4. Every listed ring, count and five-file detail → supplement | 21.0 | 12.2 |
| Fig. 7 candidate, A, B | 2.2 | 0.11 | KEEP | 2.2 | 0 |
| Table III settings | 1.6 | 0.08 | KEEP | 1.6 | 0 |
| NEW Table: least pawns for a ring ⋆2 / ⋆3 on C_n (n = 3..12, ≥ 10, ≥ 12) with labels | 0 | 0 | ADD (replaces about 8 col-in of prose) | 1.6 | −1.6 |
| IX Model to Real Chess (text) | 14.5 | 0.74 | SHORTEN: Def 17 and Lemma 18 tightened; Thm 19 kept; the 1/8 search narrative to 5 lines before Prop 20; the second candidate and the A/B status in 2 lines each | 9.5 | 5.0 |
| X Tablebases (text) | 16.7 | 0.85 | SHORTEN: rules + verification (4 lines), KRK/KBNK, the bishop pair and the torus in one paragraph each, twisted boards in 1 line; X-A KPK reduced to the headline counts (16,538 / 15,930 / 216 vs 160); "Other widths" and "A pawn each" → supplement | 9.5 | 7.2 |
| Table IV pawnless endings | 2.6 | 0.13 | KEEP (headline) | 2.6 | 0 |
| Table V KPK counts | 1.4 | 0.07 | MOVE TO SUPPLEMENT (numbers in the text) | 0 | 1.4 |
| Fig. 8 rook-pawn KPK | 1.55 | 0.08 | MOVE TO SUPPLEMENT (the line is described in the text) | 0 | 1.55 |
| Table VI KPK on C_n | 1.7 | 0.09 | MOVE TO SUPPLEMENT | 0 | 1.7 |
| XI Dawson's Chess (text) | 12.5 | 0.64 | SHORTEN: rules plus the forced sequence (cut by a third); keep (1), Thm 21 and its proof; "what was wrong" in 3 lines; misère to 2 lines; drop "A warning about sums" | 8.0 | 4.5 |
| Fig. 9 Dawson boards | 1.5 | 0.08 | KEEP (or drop if pressed; the rules are stated in text) | 1.5 | 0 |
| Fig. 10 Grundy plot (full width) | 4.2 | 0.21 | SHORTEN to column width, n ≤ 80 (the period-34 pattern is still visible) | 2.0 | 2.2 |
| XII Engines and Learning (text) | 12.3 | 0.63 | SHORTEN: keep XII-A/B (the ToG-relevant result) and "Engines on sums"; ChessSums to 3 lines; "Learning Dawson's chess" → supplement | 8.5 | 3.8 |
| Table VIII Stockfish by CGT class | 2.5 | 0.13 | KEEP (core ToG content) | 2.5 | 0 |
| XIII Verification | 2.75 | 0.14 | KEEP (add the anonymous link) | 2.5 | 0.25 |
| XIV Conclusion | 5.76 | 0.29 | SHORTEN to 4 open problems, one line each (⋆4 / ring minima; real-chess ⋆2 and 1/8; when a trébuchet is zero; misère Dawson). The others → supplement | 3.5 | 2.3 |
| Appendix text | 1.72 | 0.09 | MOVE TO SUPPLEMENT (with "FENs for all positions are in the supplementary material" in I) | 0 | 1.7 |
| Table VII FEN table (full width) | 8.6 | 0.44 | MOVE TO SUPPLEMENT (also fixes the table-order FAIL) | 0 | 8.6 |
| Acknowledgment | 2.06 | 0.11 | KEEP; the expanded AI statement adds about 0.25 | 2.3 | −0.25 |
| References (19) | 10.0 | 0.51 | KEEP; drop the Wikipedia entry; Wu–Yü–Landry and Pritchard stay | 9.5 | 0.5 |
| Biographies | 0 | 0 | NONE in review; if production requires them, one `IEEEbiographynophoto` (+1.0) | 0 | 0 |

## Result

| | Col-in | Pages |
|---|---:|---:|
| Now (review build, true size) | 274 | 14.0 |
| Sum of targets | 177.0 | 9.0 |
| Corrected for the 2% measurement excess | ≈ 173.5 | 8.85 |
| Plus about 5% float-packing and heading slack | ≈ 182 | **≈ 9.3** |

- Expected outcome: **10 pages**, with about 0.7 page of slack. Spend the slack on biographies (if production
  wants them) or on keeping Fig. 10 full width; do not spend it on prose.
- **Headline results all stay in the main text:**
  - the e.p.-aware test (Def 1) and the cut lemma (Thm 2);
  - Validity (Thm 3) and Cor 4;
  - Sum safety (Thm 10) and the counterexample (Prop 11);
  - the legal 1/8, ↑²⋆ and Tiny 1 (Thm 14, Fig. 6);
  - no ⋆2 with ≤ 6 pawns (Thm 15) and ⋆2 with seven (Thm 16, Table III);
  - the ring minima and the n-pawn ⋆2 and (n+1)-pawn ⋆3 families (new table);
  - the real-chess oracle results (Thm 19, Prop 20);
  - the pawnless tablebases (Table IV, KRK 2.80%, the torus);
  - the KPK seam effects (in the text);
  - the Dawson ring rule (Thm 21);
  - the engine pilot (Table VIII).
- **Moved to the supplement:** walk-throughs, listings, 4 figures (Figs. 4, 5, 8, plus boards (b)–(e) of Fig. 2),
  3 tables (V, VI, VII), Props 6 and 12, Conj 7, Thm 8, and the FEN appendix.
- **Consequences to handle while editing:**
  - Renumber the theorems (the shared counter drops from 21 to about 16).
  - Keep the cross-references to moved items as "Supplementary Section S-n".
  - Make the supplement self-contained, with its own references.
- Order of work (each step verifiable by `pdfinfo | grep Pages` on a scratch build):
  1. Do the moves to the supplement first (≈ 30 col-in, about 1.5 pages).
  2. Then the large text cuts in VIII, IV and V (≈ 31 col-in).
  3. Then the rest.

## The three hardest cuts, with a recommendation

1. **Section VIII-D, the ring census prose (−12 col-in).**
   - It holds several headline claims (least ring ⋆2 per cylinder, the n-pawn families for n ≥ 10, the ⋆3
     families, no ⋆4 in 134.9 M + 24 M positions). They are written as one long run of examples with labels.
   - *Recommendation:* keep every claim but move it into one table (n, least pawns for ring ⋆2, label, least for
     ⋆3, label), and keep one paragraph that defines walls and states the reduced-game argument.
   - Example rings, counts per twin and the five-file list go to the supplement, with FEN-style lists.
   - Nothing headline is lost; the reader gains a table that is easier to cite.
2. **Section IV, the king-validity material (−9 col-in).**
   - Reviewers in games research will care about when the frozen-king model is exact, and Thm 3 + Cor 4 are the
     answer, so these stay.
   - *Recommendation:* the certificate theory (Thm 5, Prop 6, Conj 7) and the loopy-game outcome theorem (Thm 8)
     are secondary and mostly [S]/[Conj]. Move them, with full proofs, to the supplement, and state Thm 5 in one
     sentence in the main text.
   - Keep the empirical failure rates (92.5% agreement, the square-rule repair): they are the honest calibration
     of the model.
3. **The 2025-study puzzles and the FEN appendix (−12.6 col-in combined).**
   - ToG requires the relation to prior work to be explicit in the text, and the FEN table is the reproducibility
     anchor for chess readers.
   - *Recommendation:* keep a compact Table I (claimed vs exact) as the explicit statement of what is corrected,
     with one paragraph. Move Fig. 4 and the walk-throughs out.
   - Move the FEN table entirely to the supplement and the repository (FENs are machine data). Say so in
     Section I and in the Data Availability sentence.
   - This also removes the table-order FAIL.

(Next hardest: Section X. The KPK per-width table and the KPKP results are genuinely new but secondary to the
pawnless headline; they go to the supplement with one summary sentence each.)

## Fallback: a 12-page version (no justification letter needed; $400 mandatory charge)

Start from the 10-page plan and put back:

| Put back | Col-in |
|---|---:|
| Fig. 2 full width with all six boards (instead of three in a column) | +2.2 |
| Fig. 4 puzzles + the full Table I | +2.65 |
| Fig. 5 atlas | +2.1 |
| Fig. 8 rook pawn + Table VI KPK on C_n | +3.25 |
| Fig. 10 full width, n ≤ 120 | +2.2 |
| Section IV keeps Thm 8 (loopy) and the small-margin examples | +5 |
| Section V keeps the puzzle walk-throughs (compressed) | +3 |
| Section VIII keeps examples for C_3, C_4, C_7 next to the table | +5 |
| Section X keeps "Other widths" | +3.5 |
| Section XII keeps "Learning Dawson's chess" | +1 |
| A compressed FEN table (6 key positions: T, the 1/8, A, B, the candidate, the five-file ⋆2) at column width | +3.5 |
| Sections I and II slightly longer | +3.5 |
| **Total added** | **≈ +37** |

- Total ≈ 214 col-in, or about 210 after the 2% correction, plus 5% slack ≈ 220 col-in = **11.2 pages**: within
  12, so no justification letter is needed.
- Cost: pages 11–12 at $200 each = $400 mandatory (or $110 × 12 = $1,320 voluntary, which would waive it).

## Alternative worth considering

The paper is two papers:
- (a) a CGT paper on cylinder pawn endgames (Sections II–IX, XI);
- (b) a tablebases-and-engines paper (Sections X, XII).

Splitting, so that (a) goes to Integers or the ICGA Journal and (b) to ToG as a short or full paper, avoids every
hard cut above. `paper/SUBMISSION.md` already lists these venues. This is a decision for the author; the plan
above assumes one ToG paper.
