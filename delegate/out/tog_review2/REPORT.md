# ToG review 2: anonymous 10-page paper and supplement (2026-11-22)

Reviewer: read-only Claude agent. Files read: `dist/tog/tog_review.pdf` (10 pages), `dist/tog/sections/*.tex`,
`tog.tex`, `macros.tex`, `refs.bib`, `supplement_review.pdf` (80 pages, spot-checked), `supp/s06.tex`, `supp/s10.tex`,
`tools/build_supplement.py`; raw reports `RESULTS.md`, `research/sum_truth_cyl/REPORT.md`,
`research/sum_whole_census/REPORT.md`, `research/mobius_rings/REPORT.md`, `research/mobius_rings_check/REPORT.md`,
`research/c9_rings/star3/REPORT.md`, `research/flat_xtarget_census/REPORT.md`, `realchess/REPORT.md`; earlier audits
`delegate/out/tog_review/REPORT.md` and `delegate/out/ieee_audit/AUDIT.md`. Nothing was built or edited outside this
directory.

Counts: **BLOCKERS 5, SHOULD-FIX 12**, plus 4 minor notes.

Line numbers are those of `dist/tog/sections/*.tex` (or the file named). Word counts are for the LaTeX source.

---

## 1. Verdict

**Major revision** (close to minor). The computations are careful, the evidence labels are a real asset, and the
new text checks out number by number against the raw reports. What keeps it from minor: the conclusion's opening
sentence mixes two different experiments, the AI authorship of the [S] proofs is disclosed only in the
supplement, the code link is still a placeholder, and the supplement now contradicts the main text on the
Möbius strip.

**Scope fit for ToG.** Good. The paper is about solving and valuing endgames, tablebases and engines, and it
tests a mathematical model against real chess. It is denser in CGT than most ToG papers. The engine section
(Section XII) and the real-chess checks are what tie it to the ToG readership, and the abstract should lead with
a games question, not a board definition (Section 6 below).

**Three strongest points (as a reviewer would write them)**
1. The seven-pawn ⋆2 on four files of the ordinary board (Theorem 11), with an exhaustive lower bound (no ⋆k, k ≥ 2,
   with six pawns or fewer, any width) and three programs agreeing. It is a clean answer to a question open since
   Elkies, and it fits on a real board.
2. Exemplary honesty about evidence. Every claim carries P/S/C1/C2/Conj. The paper reports where its own model fails
   (Table I, Theorem 14, the 159/500 sweep, the HSS census with 19.3% disagreement off the safe set) instead of
   hiding it.
3. Model and real chess are separated carefully: the sandwich lemma, the oracle value and the new real-king sum
   test (19 exact sides, all agreeing, 0 contradictions) are the right tools and are reported with their bounds.

**Three weakest points**
1. The [S] results (sum safety, validity, the wall families for all n) rest on AI-written proofs that only AI
   referees have read, some of them only by referees of the writer's own model family (supplement S15 Notes 2 and
   3). Supplement S16 shows that an AI-refereed lemma in this same project was false. The main text says the
   referees were AI, but the acknowledgment and the label definition do not say that AI wrote the proofs.
2. The bridge to real chess is thin and partly a convenience sample. The 92.5% comes from 2,049 positions "whose
   real results we know", which is whatever earlier runs had solved (`flat_xtarget_census/REPORT.md` item 2);
   105 real draws are excluded; positions are correlated; small boards give 50% to 88.5%. The real-king sum test
   uses one board, one anchor set and components pre-selected because the model already gets them right alone.
3. Readability. Ten pages carry a census, rings, walls, ⋆3 families, Möbius rings, oracle values, tablebases,
   Dawson's chess and engines. A games reader will struggle with Section VIII-E (walls, cores, "reduced game")
   on one reading. Several results could move to the supplement to give the main result room.

---

## 2. BLOCKERS

### B1. Conclusion mixes the 8×8 accuracy with the six-rank sweep
`14_conclusion.tex:3-4`
> Against real chess the model is right in $92.5\%$ of the decisive $8\times8$ positions we can check; its pawn
> errors vanish under a square-rule passer test, and the rest come from the kings \lab{C1}.

The square-rule result (52 convention failures removed, 128 left, all king effects) is from the six-rank boards
(`04_kings.tex:96-98`; `RESULTS.md` "Why the passer convention fails", cyl:7x6 etc.). On the 8×8 set the raw
report says the opposite: "Kings: the model ignores king moves; every disagreement therefore includes king
effects. They are not separated here." (`research/flat_xtarget_census/REPORT.md:34`). So "its pawn errors vanish
... the rest come from the kings" is unsupported for the 92.5% set. The square-rule test is also not sound in
general (supplement S16). In addition, "In the model, ⋆2 appears with seven pawns" is false as written: the C3
ring is a six-pawn ⋆2 in the model (`08_star2.tex:106`), and so are Möbius rings on 3 and 5 files.

Replacement for lines 3-5 (54 words for 54; also a sharper opening, see Section 6):
```
In Elkies' model, seven pawns on four files of the ordinary board make a $\nim{2}$, and no six do; nine make a
$\nim{3}$. The model names the real winner in $92.5\%$ of $2{,}049$ decisive $8\times8$ positions \lab{C1}; on
six ranks its pawn errors vanish under a square-rule passer test. Section~S10 lists more problems.
```

### B2. Code link is a placeholder in both review PDFs
`tog.tex:26` defines `\anoncodeurl` as the literal text "anonymized repository link"; the paper prints "The code
and data are available at anonymized repository link." (`13_verify.tex:14`, page 10), and the supplement's first
paragraph says the same. ToG asks for an anonymous.4open.science link; a reviewer cannot reach code or data.
This was ieee_audit item 2 and it has not been fixed. Replacement at `tog.tex:26` (same length in print):
```
\newcommand{\anoncodeurl}{\url{https://anonymous.4open.science/r/<id>}}
```
(create the mirror first; no other text change).

### B3. AI authorship of the [S] proofs is not disclosed in the paper
The supplement says the proofs were AI-written ("The hand proof was drafted by one AI model", S15 Note 2, pdf
line ~3679; similar in Notes 1, 3, 4). The paper's acknowledgment (`tog.tex:139-144`) says the assistants "wrote
and ran ... the software" and "helped draft and edit the text", which does not cover writing the proofs. IEEE's
AI policy asks for the content generated and where. Replacement for `tog.tex:142-143` (anonymous branch; mirror
it in the named branch at `tog.tex:151-152`):

Current:
```
and cross-checks of Sections~II--XIII and the scripts that draw the figures, and helped draft and edit the
text of all sections.
```
New (+6 words; pays from the cut in S1 below):
```
and cross-checks of Sections~II--XIII and the scripts that draw the figures, wrote the full proofs of
Sections~S12--S15, and helped draft and edit the text of all sections.
```

### B4. Supplement S10 contradicts the new Möbius results
`supp/s10.tex:15-17` (printed S10, item 5):
> Pawn play across the twisted seam of the M\"obius strip (Section~\ref{sec:tb}), where a pawn reverses
> direction, remains open.

Section VIII (`08_star2.tex:133-136`) and S6.4 now settle the least ring ⋆2 for n = 3..8, and the main
conclusion asks only whether the Möbius rings "come in families" (`14_conclusion.tex:9-10`). The reference to
Section X (tablebases) is also wrong for pawn rings. Replacement (supplement has no page limit):
```
  stay undecided, and KPPK comes next. On the M\"obius strip the least ring $\nim{2}$ is known for $n\le8$
  (Section~S6.4); families for all $n$, and the kings, remain open.
```

### B5. Supplement S6.4 overstates the independent Möbius check for n = 6
`supp/s06.tex:135` (= `tools/build_supplement.py:122`):
> and on the number of $\nim{2}$ rings in every scan up to the least for $n=3,4,5,6,8$ and with seven pawns for $n=7$

For n = 6 the least is 8 pawns, but Codex's census (`research/mobius_rings_check/REPORT.md`, table "Census and
comparison") ran n = 6 only with 6 and 7 pawns. The C2 label for the least value still holds (lower bound by both
scans, upper bound by the checked witness), but the sentence is false for n = 6. Replacement:
```
and on the number of $\nim{2}$ rings in every scan below the least, and at the least for $n=3,4,5,8$
```
(Edit `tools/build_supplement.py:122`, then rebuild; do not hand-edit `supp/s06.tex` only.) While there,
"two programs by one author" (`build_supplement.py:120`) reads as the human author in an anonymous supplement;
write "two programs by one AI model".

---

## 3. SHOULD-FIX

### S1. The "AI referees" sentence (`13_verify.tex:11-12`)
> The \lab{S} proofs have been checked by computer on their finite parts and by independent AI referees; no human
> referee has checked them yet.

Honest, but a reviewer will attack two things: (a) "independent" is too strong, since S15 Note 3 (odd-n ⋆2/⋆3
families) "was checked only by AI models of the same model family as the model that wrote it" and Note 2 "has had
no referee independent of it"; (b) the reader is not told the proofs themselves were AI-written. Replacement
(27 words for 24):
```
AI models wrote the full \lab{S} proofs; AI referees, for most proofs from another vendor, and computer checks of
the finite parts found them sound. No human has refereed them.
```
Pay for this, B3, S3 and S4 with one cut at `13_verify.tex:14`: delete
"Our CGT engine is in Python~3 (standard library only) and the fast solvers are in C." (16 words, about 1.3
lines; the information is in the repository).

### S2. Label definition hides the AI role (`01_intro.tex:37`)
> \lab{S}, proof sketched here and given in full in the supplementary material;

Replacement (12 words for 11):
```
\lab{S}, proof sketched here, with a full AI-written, AI-refereed proof in the supplement;
```

### S3. The 92.5%: denominator and sample (`04_kings.tex:98-100`)
> Over the $2{,}049$ decisive $8\times8$ positions beside a tr\'ebuchet whose real results we know, the model agrees
> with chess in $92.5\%$; the count rule beats the mover and opponent rules ($83\%$) \lab{C1}; Section~S2 has more detail.

The denominator is stated (2,049), but "decisive" hides the 105 real draws of the 2,154-position pool, "whose real
results we know" hides that the pool is whatever earlier runs solved (not an enumerated class), and "(83%)"
rounds 83.0% and 83.7% to one figure. Raw: `research/flat_xtarget_census/REPORT.md` items 1, 2, 4. Replacement
(44 words for 37; paid by the S1 cut):
```
On the $8\times8$ board, of the $2{,}154$ positions beside a tr\'ebuchet in our solved trees, $105$ are real
draws; on the other $2{,}049$ the model names the winner in $92.5\%$, against $83\%$ and $84\%$ for the mover and
opponent rules \lab{C1} (Section~S2).
```
Optionally add to S2 (supplement, no limit): "The pool is the union of positions solved for Sections VII-IX, not a
sample of a defined class; without the 244 positions known only from Lichess 8-man categories the rate is 95.2%."

### S4. "Real kings" paragraph: selection and conditions (`05_sums.tex:87-89`)
> \emph{Real kings.} On a six-rank $\cyl{8}$ we solved $19$ sums of two components beside a tr\'ebuchet with real
> kings. Of the $38$ positions, $19$ are exact and all agree with the sum; the rest, among them every
> second-player win, are bounded, none against it \lab{C1}.

All numbers are right (`research/sum_truth_cyl/REPORT.md`, "12 GB runs", Totals). Missing: queen promotions only
(`--promote Q --cap 1`); the components were chosen from those the model already gets right alone (`gen.py`:
`verdict == match` rows) or are live non-passer components; 9 of the 19 sums contain a locked zero component and
test additivity only weakly (report, Caveats). "Bounded, none against it" is opaque. Replacement (+5 words; paid
by the S1 cut):
```
\emph{Real kings.} On a six-rank $\cyl{8}$, with queen promotions only, we solved $19$ sums of two components that
the model gets right alone, beside a tr\'ebuchet. Of the $38$ results, $19$ are exact and match the sum; the other
$19$, every second-player win among them, are bounds that contain it \lab{C1}.
```

### S5. HSS census: say "in outcome" and the setting (`05_sums.tex:69-71`)
> Of all $599{,}098$ positions without a passed pawn that have at most six pawns on flat boards three to five
> files wide, counted up to symmetry, the $540{,}503$ HSS ones all agree and $19.3\%$ of the rest differ,

540,503 is the e.p.-aware HSS count (textbook: 539,893) and 19.3% is count rule, e.p.-aware; the comparison is of
outcome classes only (`sum_whole_census/REPORT.md`, "Exact coverage", last bullet). Replacement (+3 words; fits the S1 cut):
```
Of all $599{,}098$ positions without a passed pawn that have at most six pawns on flat boards of width $3$--$5$,
up to symmetry, the $540{,}503$ HSS ones all agree in outcome and, in the default setting, $19.3\%$ of the rest differ,
```

### S6. Möbius paragraph: label the least counts (`08_star2.tex:134-136`)
> The least ring $\nim{2}$ then has $6, 8, 6, 8, 8, 8$ pawns for $n=3,\dots,8$ files, against $6, 7, 8, 9, 10, 10$
> on the cylinder: on eight files one pawn per file is enough. Nine pawns give a $\nim{3}$ on five files \lab{C2}
> (Section~S6).

The least counts are the CHECKED-2 headline but carry no label; the ⋆3 also exists on six files. Replacement (same
length):
```
The least ring $\nim{2}$ then has $6, 8, 6, 8, 8, 8$ pawns for $n=3,\dots,8$, against $6, 7, 8, 9, 10, 10$ on the
cylinder \lab{C2}: on eight files one pawn per file is enough. Nine pawns give a $\nim{3}$ on five and six files
\lab{C2} (Section~S6.4).
```

### S7. Wikipedia still cited (`10_tablebases.tex:6`, `refs.bib:186`)
ieee_audit item 9 flagged `WikiCylinder`; it is still cited. Replace `\cite{WikiCylinder,HGMCylinder}` by
`\cite{HGMCylinder}` (or `\cite{Pritchard,HGMCylinder}`), and drop the entry. Saves about one reference line.

### S8. FEN undefined in the main text (`01_intro.tex:63`)
> and the FEN of
Replace with `and the Forsyth--Edwards Notation (FEN) of` (+3 words; the reference line saved in S7 pays).

### S9. "the count rule" line, Section IV: one figure for two rates
Covered by S3. If S3 is not taken, at least change `($83\%$)` to `($83\%$, $84\%$)`.

### S10. Abstract at 197 words
Under 200, but any added word risks the limit. If B1's numbers or S2's wording leak into the abstract, cut
"in one position and its color-reversed twin," elsewhere first. (Suggestion 1 in Section 6 shortens it.)

### S11. "beside T" before readers know T on small boards (`05_sums.tex:87`)
Not an error, but the real-king test uses a different trébuchet (Pa3 pa4 Kh4 kb3 on cyl:8x6) than T. With S4's
text this is clear enough; no further change needed if S4 is taken.

### S12. Supplement has no section for the two new Section V results
Neither the HSS census nor the real-king sum test has a supplement entry, so a reviewer cannot see the tables.
Add a short S3.4 (no page limit) with the Table 1 rates by rule and test from `sum_whole_census/REPORT.md` and the
19-row pair table from `sum_truth_cyl/REPORT.md`, and cite it as "(Section~S3)" at the end of
`05_sums.tex:72` and `05_sums.tex:89` (2 words each).

### Minor notes
- M1. `14_conclusion.tex:9` "Do the M\"obius rings come in families?" is fine; keep it consistent with B4.
- M2. Fig. 6 caption (`08_star2.tex:98`): "\lab{C1} for $\nim{3}$" is right for the least values, though the
  twelve-pawn C11 rings are C2 (intro line 52). No change needed.
- M3. Build log: `TU/ptm` font shape warnings (`build/tog_review.log:19-38`); the PDF embeds Nimbus/TeX Gyre, so
  harmless, but run IEEE PDF eXpress (AppleSymbols has no ToUnicode map).
- M4. The square-rule sentence at `04_kings.tex:96-98` is a computation on 500 components and stays correct; the
  supplement S16 counterexample does not touch it.

---

## 4. Budget for the replacements
Additions: B3 +6, S1 +3, S2 +1, S3 +7, S4 +5, S5 +3, S8 +3 = about +28 words (about 2 lines).
Cuts: the Python/C sentence (`13_verify.tex:14`, 16 words), the Wikipedia reference (about 1 line), B1 (-0).
Net about 0. If S3 is too long, take only its "105 are real draws" clause.

---

## 5. Numbers verified against raw files

| Number | Paper location | Raw file |
|---|---|---|
| 599,098 positions; 540,503 HSS; 19.3% (11,300/58,595) | `05_sums.tex:69-71` | `research/sum_whole_census/REPORT.md` Table 1 and "By heredity"; `RESULTS.md:452-461` |
| W a5 d3 / B b6 e4, sum P, board N | `05_sums.tex:71-72` | same, "Smallest S != W" |
| 19 sums, 38 positions, 19 exact all agree, every P-class bounds only, 0 contradictions, cyl:8x6 | `05_sums.tex:87-89` | `research/sum_truth_cyl/REPORT.md` "12 GB runs", Totals; `RESULTS.md:568-576` |
| Möbius least ⋆2: 6, 8, 6, 8, 8, 8 (n = 3..8) | `08_star2.tex:134-135` | `research/mobius_rings/REPORT.md` headline; `research/mobius_rings_check/REPORT.md` census table |
| Cylinder 6, 7, 8, 9, 10, 10 | `08_star2.tex:135` | Fig. 6 data; supplement S6.3; `RESULTS.md` |
| Nine-pawn ⋆3 on five files (C2) | `08_star2.tex:136` | `mobius_rings/REPORT.md` (mob1 = mob2, Part B); T77 witness NNNP |
| 92.5% = 1,896/2,049; 83.0%, 83.7% | `04_kings.tex:98-100`, `14_conclusion.tex:3` | `research/flat_xtarget_census/REPORT.md` items 2, 4 |
| 52 failures removed, 128 left; 159/500, 107, 18, 34, 13 | `04_kings.tex:91-98` | `RESULTS.md` section 7 "Why the passer convention fails"; supplement S2.3 |
| 55,195; 4,967,550 (= 2 × 2,483,775); 2,483,775; 1,070 | `13_verify.tex:7-10` | `RESULTS.md:124-131` |
| 160 positions | `13_verify.tex:11` | `realchess/REPORT.md:56` |
| 6,724 zeros, 4,042 stars; 793,299; 134,920,191 | `08_star2.tex:37,41,128` | `RESULTS.md` (one hit each) |
| ⋆3 with n+2 (even n ≥ 8, odd n ≥ 11), n+1 for n ≥ 12; C11 least 12 | `08_star2.tex:125-127`, `01_intro.tex:52` | `research/c9_rings/star3/REPORT.md` items 1-3; supplement S15 Notes 2-4 |
| 2.80% | `01_intro.tex:57` | `RESULTS.md` |
| 216 vs 160 reciprocal zugzwangs | `10_tablebases.tex:67` | `RESULTS.md:92` |
| Abstract 197 words | `00_abstract.tex` | counted from source |

Not traced (not re-derived; outside the new text): 5,503,282 root positions (found only in
`research/star2_frontier/REPORT.md`, consistent with the supplement; not in RESULTS.md); "about 24 million rings";
6.1 × 10^10 states, 15.6 h; the 302/290/283/5/2 end-position split in Section IX-B. "With B = 256 the move bound
always holds on boards up to 8×8" is a reasoning claim (at most 8 pawns × 6 moves a side), not a computation.

Cross-references spot-checked (all exist and contain what the paper says): S1, S2 (S2.3 holds the sweep and the
92.5%), S3 (S3.1 puzzles, S3.2 condition (E), S3.3 two models), S4, S5, S6 (S6.1 candidate, S6.2 seven pawns,
S6.3 counts, five files, any-width argument, S6.4 Möbius), S7, S8, S9 (Dawson and the LSTM experiment), S10 (six
problems, but see B4), S11 (FEN), S12 (Theorem 1.11(c), sum safety by induction with (E)), S12-S15 (full proofs).

Anonymity: no name, affiliation, user path or repository owner in either PDF's text or `strings`; PDF metadata has
no author. "The authors thank" is used in the review build. Clean apart from B2's placeholder.

---

## 6. Making it more memorable to a games audience (no added length)

1. **Abstract, third sentence** (`00_abstract.tex:4-7`, 44 words to 42). Lead with the nim-heap, which every games
   reader knows:
   ```
   With this test and the count rule, the smallest ordinary-board position worth star two, a nim-heap of size two,
   has seven pawns: one position and its color-reversed twin, confirmed by three programs; none has six or fewer.
   Its real-chess value is open.
   ```
   (Replaces "With this test and the count rule, no whole-board nimber above star has at most six pawns on ordinary
   boards of any width, but star two appears with seven, in one position and its color-reversed twin, confirmed by
   three programs; its real-chess value is open.")

2. **Title** (`tog.tex:97`, `tog.tex:40`): the current title takes three lines. A shorter title names the result and
   may save a title line:
   ```
   Nim Heaps in King-and-Pawn Endgames on Cylindrical and Ordinary Chessboards
   ```

3. **Conclusion opening**: the B1 replacement doubles as the "one sentence to remember": "In Elkies' model, seven
   pawns on four files of the ordinary board make a ⋆2, and no six do; nine make a ⋆3."
