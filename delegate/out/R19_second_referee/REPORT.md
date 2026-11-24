# R19: second-round referee report (IEEE ToG, double-anonymous)

Read: dist/tog/tog_review.pdf (10 pp., built Nov 23 18:35) with dist/tog/sections/*.tex and tog.tex; dist/tog/supplement_review.pdf
(109 pp.): S1-S11 (pp. 1-16), S12.1 (pp. 17-23), S13-S17 (pp. 70-109) in full, S14-S15 notes read for the statements the paper
cites; S12.2 (pp. 23-69) not reviewed, only searched for dependencies. First-round material: R14, W2, W4, W5, W6 reports and
paper/IEEE_CHECKLIST.md from "Submission readiness" on. Nothing was run except pdftotext/pdftoppm and a FEN check of Table S8
(all 17 rows match their men lists).

## 1. Recommendation: MINOR REVISION (first round: major)

The first-round errors that a referee could check against the supplement are gone: Corollary 4 is per side, the real-king
sentence, Definition 5 and the engine statistics now match their sources, and Table I (puzzles) has moved to S3. Every number
I checked agrees across abstract, intro, body, tables, captions, supplement and project records. What remains is one definition
that now reads wrongly (Definition 12), two label semantics that the AI-use policy makes important (a ⟨P⟩ that is an AI-written
supplement proof; a ⟨C2⟩ definition that does not fit the Lichess-tablebase cases), and the supplement's reliance on the
47-page S12.2 for three small claims.

Three changes that would most move it:
1. Fix Definition 12 (finding 1) and the two label definitions (findings 2, 3). Cheap, and the paper gets shorter.
2. Decide S12.2. If it goes, move the three things that depend on it into S2 (finding 7); in the remaining notes (S14-S15)
   say once that "hand proof" means an AI-written argument without computation (finding 6).
3. Have a human read S12.1 (7 pp.) and S13 (4 pp.). Every ⟨S⟩ result in the paper rests on these 11 pages, and both are now
   short and self-contained. Even one named-in-the-cover-letter human check would change how an editor reads Sections I and XIII.

## 2. First-round items (R14) after the fixes

| R14 | Status | Note (current text quoted where not fully fixed) |
|---|---|---|
| 1 Corollary 4 per side | fixed | 04_kings.tex:69-72 "for that side to move the chess result is the one given by the components' ±B value"; matches A.13. |
| 2 ⟨C2⟩ overstates independence | partly fixed | 01_intro.tex:38 "two separately written programs agree, the second from the rules alone (both AI-written; Section S17)". The shared rules text is said only in S17 ("Limits"), and "both AI-written" is false where the second check is the Lichess tablebase (finding 2). |
| 3 Real-king sum sentence | fixed | 05_sums.tex:68-69. Recounted from Table S3: 19 exact sides, all agree; the 19 bounds all contain the model's result. |
| 4 Definition 12 draw scoring | fix introduced a new problem | Finding 1. |
| 5 Engine statistics | fixed | Metric (±150 cp), Fisher test and "by depth 8" are in 12_engines.tex:17-21; depth-1 counts recomputed from Table IV (55/68, 45/57, 27/37, 12/20, 9/17, 8/27). Intro bullet (01_intro.tex:60-61) is supported at depth 1. |
| 6 92.5% not a random sample | fixed | 04_kings.tex:99 and 14_conclusion.tex:4. |
| 7 Definition 5 (threat) | fixed | 05_sums.tex:32-34; Remark A.3 now says the notions agree. |
| 8 Notation | partly fixed | C_n ranks (02_rules) fixed; reference games R fixed; (V4) scope now clear. Not fixed: "Tiny 1" (abstract, intro, Fig. 2, Sec. VII) beside "tiny(1)" (Sec. III, VII, Table I); h is both certificate horizon (IV-A) and heap (V-B); in the supplement S13 still writes "C1 ⟨C2⟩", "C2 ⟨C2⟩" (p. 72) and names players X, Y, Z (p. 70), clashing with labels, the context X and the king group Z. B and S(X) renaming: declined, not repeated. |
| 9 Anonymity, note residue | fixed for the review PDFs; S12.2 residue remains | No name, institution, e-mail, Morley, user path or author GitHub URL in the text, strings or metadata of either review PDF (grep of pdftotext and `strings`). Upload names are tog_review.pdf / supplement_review.pdf (submission/files_to_upload.md). Revision dates removed. Still present, all inside S12.2 or S15: "References to §4–§8 and to Appendix A are to later parts of the source note, which are not reproduced here" (p. 24) and "two adversarial AI reviewers" (S15 notes). Repository paths and harness names: declined, not repeated. |
| 10 Table I (puzzles) | fixed | Now Table S1 in S3; V-A points there. The pointer is given twice (finding 8, used to pay for other edits). |
| 11 ChessSums | declined | Not repeated. |
| 12 Labels and numbers | fixed, one fix introduced a new problem | "n ≤ 61 ⟨C2⟩" matches S13 C2 (odd 5-61, even 6-60); S13 now refereed across vendors (S17 Table S10); Prop. 7 states e.p. off and count rule; candidate bullet labelled ⟨C1⟩; IX-B gives the 12 races; S7.1 no longer claims a free buffer file. New problem: "(E) ... in our model ⟨P⟩ (Section S12)" (finding 3). |
| 13 Typos, figures | partly fixed | Fixed: "at most two queens at a time", Fig. 6 now plots C7 and C8 (W5), Lemma 3 hat. Not fixed: 13_verify.tex:12 "no human referee has yet." (finding 4). S5 lead-in now repeats itself (finding 11). "changes at least 18,137" (02_rules) is still explained only in S1 (optional, not repeated below). |
| (i) "state when" overclaim | fixed | Abstract: "give conditions for frozen kings to match chess." |

## 3. Findings

### Must fix

**1. Definition 12 now gives the wrong leaf for two of the three draw treatments (fix introduced a new problem).**
Where: dist/tog/sections/09_real.tex:10-12; PDF p. 7, right column.
Current: "If a side is drawn, the draw treatment counts that draw as a win for black, as a win for white, or as worth 0,
scoring the end position {B r_W | B r_B} (r_W, r_B ∈ {−1,0,1}: white's results with white and with black to move; a dead
draw is scored ⋆)."
Why: the participle now attaches to all three treatments. Read so, a drawn-drawn end position under "draws are black wins"
gives r = (−1,−1) and the leaf {−B | −B} = −B + ⋆, and a drawn/white-win end position under "draws are white wins" gives
{B | B} = B + ⋆. The computation (realchess/oracle_value.py:630-643, `pair_game`) recodes the draw and then uses the first
sentence's +B, −B, {+B | −B}, 0; it uses {B r_W | B r_B} only for "draw0". Theorem 14(c) ("draws as wins for black") is a
value statement, so the leaf rule matters.
Replace with (+3 rendered characters; paid by finding 8):
"If a side is drawn, the draw treatment counts that draw as a win for black or for white, scored as above, or as worth $0$,
scoring the end position $\game{\BIG r_W}{\BIG r_B}$ ($r_W,r_B\in\{-1,0,1\}$: white's results with white and with black to
move; a dead draw is $\star$)."
Checked against the code: draw0 returns +B/−B only when r_W = r_B ≠ 0, which cannot happen when a side is drawn, so the
formula is exact for draw0.

**2. A ⟨P⟩ that the paper's own label key forbids.**
Where: dist/tog/sections/05_sums.tex:54; PDF p. 5, left column, top.
Current: "and so is (E): without it, sums fail even in the pawn game with no passed-pawn rule ⟨C1⟩ (Section S3), and in our
model ⟨P⟩ (Section S12)."
Why: 01_intro.tex:37 defines ⟨P⟩ as "proved here" and ⟨S⟩ as having "a full AI-written, AI-refereed proof in the
supplement". The proof cited is the "(E) cannot be dropped" remark of S12.1 (p. 20), which S17 Table S9 lists as written by a
Claude Opus model (S12.1, A.1-A.9) and checked by AI referees. The example itself is correct (I re-derived it: W(X) is a
first-player win, S(X) = −B−1 + ⋆ is a black win), but the label tells the reader a human-style proof is in the paper. The same
clash, inside the supplement only, is S13's "Lemma 1 (Reduction; ⟨P⟩)", "Lemma 2 ... ⟨P⟩", "Lemma 3 ... ⟨P⟩" and "(⟨P⟩, given
the computed facts C1 and C2.)" (pp. 70-72), all AI-written (Table S10).
Replace "\lab{P} (Section~S12)" with "\lab{S} (Section~S12)" (same length). In the supplement, either relabel S13's lemmas ⟨S⟩
or add to the supplement's label paragraph (supplement.tex, p. 1): "Inside Sections S12-S15, ⟨P⟩ marks a step proved in full
there; all of these proofs were written by AI models (Section S17)." I could not tell who wrote or checked the main text's
own ⟨P⟩ proofs (Theorem 2, the {B|0}+{0|−B} = 0 example, Lemma 13, Theorem 16); the authors should say so in Section XIII if
it was not a human (see finding 4 for the room).

### Should fix

**3. The ⟨C2⟩ definition does not fit the tablebase-confirmed ⟨C2⟩ results.**
Where: 01_intro.tex:38; PDF p. 1, right column; same wording on supplement p. 1 (supplement.tex, not editable by the builder).
Current: "⟨C2⟩, two separately written programs agree, the second from the rules alone (both AI-written; Section S17);"
Why: several ⟨C2⟩ results are our solver plus the Lichess tablebase: Fig. 3(b) ("the Lichess tablebase confirms that it is a
mutual zugzwang ⟨C2⟩", p. 3), the Puzzle 2 king group ("our solver and the Lichess tablebase", p. 4). The tablebase is not
AI-written. Also, as R14 noted, S17 "Limits" says the second programs were written "from one description of the rules"; the
main text does not.
Replace "(both AI-written; Section~S17)" with "(ours are AI-written; Section~S17)" (+4 characters; paid by finding 8).

**4. Section XIII: unfinished sentence (R14 item 13, not fixed).**
Where: 13_verify.tex:11-12; PDF p. 10, left column.
Current: "AI referees, some from another vendor, checked them, and programs ran the ring base cases; no human referee has yet."
Replace "no human referee has yet." with "no human has read them." (−2 characters).

**5. Proposition 7 is labelled ⟨C2⟩, but the records show one program for S(X).**
Where: 05_sums.tex:56-60; PDF p. 5; A.14 (p. 21) says part (c) is "Checked by computer only".
Why: notes/lemmas.md:351-355 records o(S(X)) = R from the engine and o(W(X)) = N "checked two ways" (lemmas/common.py minimax
and crosscheck/minimax.py); RESULTS.md:135 says the same. I found no second program for "S(X) is a black win whoever starts".
The brute-force sum solver of Section XIII covers 3-5 files, not C8. What I could not check: whether a later run (not in these
notes) recomputed S(X).
If no second program exists, replace "\begin{proposition}[\lab{C2}]" by "\begin{proposition}[\lab{C1}]" (same length), or add a
second computation of S(X).

**6. The supplement calls AI-written proofs "hand proofs".**
Where: S12.1 p. 17 (supp_src/s12a_core.tex:7, "every proof is a hand proof"); S12.2 p. 23; S14 p. 74 ("PROVED = by hand");
S15 Notes 1-4 (about 15 more uses of "hand proof", "by hand", "re-derived by hand").
Why: in every case the writer is an AI model (S17 Tables S9-S10). A referee checking the AI-use statement will read "hand
proof" as human work.
Add one sentence after the first sentence of the "Full proofs" preface (p. 16 bottom, build_supplement.py), no page limit:
"Here a "hand proof" or a step done "by hand" means a written argument that uses no computation; all such proofs in Sections
S12-S15 were written by AI models (Section S17)."

**7. What depends on S12.2 (asked for), and one conclusion claim with no evidence in the supplement.**
Nothing in the main text's ⟨S⟩ results depends on S12.2: S12.1 (A.1-A.17) is self-contained, as it says, and I found no step
that cites S12.2; its only references to it are A.12(d) ("Unlike (V1a) of Theorem 1.14 in the longer treatment") and the
closing paragraph "Where to find the longer treatment". The following do depend on it:
- S2.1 (p. 4): "For (V2) a local test is known only if king moves also lose ⟨S⟩" (Proposition 2.11 of S12.2) and S2.2
  Theorem S4 ⟨S⟩ (proof sketch only; full proof is Theorem 3.4 of S12.2). The main text points to both (04_kings.tex:85-86:
  "a local test for (V2) and the loopy games of kings with spare moves are in Section S2"). S2's opening says "Full proofs
  are in Section S12".
- S2.2 (p. 4): "removing the edges changes the class of 12.5–20.5% of them ⟨C2⟩" (data in S12.2).
- S2.1 (p. 4) and Conclusion item 3 (14_conclusion.tex:13-15, PDF p. 10): "in the promotion game even a locked pawn pair can
  break their zero ⟨C2⟩". The only evidence I found is the (V1a) row in S12.2 (cyl 6×6, Ka2 kb4 Pa3 pa4 Pd2 pe3, three solvers).
- S17 Table S9 row "Longer treatment, S12.2" and three sentences of "What the checks found" (Theorem 3.4, Theorem 1.11(c),
  the horizon-1 proposition).
Separately, Conclusion item 3 says "Real trébuchets seem to need h ≈ 5–7 ⟨Conj⟩ (Section S2)". S2 repeats the sentence with
no evidence, and I did not find the evidence in S12.2 either (searched for "≈", "horizon", "5–7"). The project source is
kings/REPORT.md:522 ("slower (T ≈ 5–7)"). A ⟨Conj⟩ needs at least a sentence of evidence.
If S12.2 is removed: move the locked-pair example (position, result, the three solvers) into S2.1; label the (V2) local test
and Theorem S4 as statements whose proofs are in the code repository, or drop their ⟨S⟩; drop "Full proofs are in Section
S12" from S2's opening; delete A.12(d) and "Where to find the longer treatment"; remove the S12.2 row of Table S9.
Conclusion item 3, replace "Real tr\'ebuchets seem to need $h\approx5$--$7$ \lab{Conj} (Section~S2), and in the promotion
game even a locked pawn pair can break their zero \lab{C2}." with "In the promotion game even a locked pawn pair can break a
tr\'ebuchet's zero \lab{C2} (Section~S2)." (−39 characters), unless S2 gets the evidence for h ≈ 5–7.

### Optional

**8. V-A gives the S3 pointer twice (use this to pay for findings 1 and 3).**
05_sums.tex:17, PDF p. 4. Current: "has the same value (Section~S3 shows the puzzles)." The first sentence of the paragraph already
says "(Section S3 shows them and tabulates the claimed and the exact values)". Replace with "has the same value." (−31).
Net for findings 1, 3, 4, 7, 8: +3 +4 −2 −39 −31 = −65 rendered characters; the paper stays within 10 pages.

**9. V-B: the HSS count belongs to the default setting, but the sentence says so later.**
05_sums.tex:49-50, p. 4-5. Current: "Of all 599,098 positions ... the 540,503 HSS ones all agree in outcome and, in the default
setting, 19.3% of the rest differ". Table S2: 540,503 is the e.p.-aware count; under the textbook test it is 539,893. Replace
"Of all" with "In the default setting, of all" and delete ", in the default setting," (+3 characters).

**10. VIII-E: "played in a window of five or six files" holds for the n+3 family only.**
08_star2.tex:114-115, p. 7. S13's zones are 6 (odd n) and 5 (even n) files, but S14's zones for the n-pawn families have 7 and
8 files (p. 74: "{n − 8..n − 3, n − 1} resp. {0} ∪ {n − 7..n − 1}"), and the next sentence says "The same argument proves the two
n-pawn families". Replace "played in a window of five or six files," with "played in a window of a few files," (−4).

**11. Small supplement wording.**
- S5 p. 8 (build_supplement.py lead-in): "Theorem 9 of the main text states that the position of its Fig. 4(a) has value
  exactly 1/8. To see why, look at Fig. 4(a). If white moves first" → delete "To see why, look at Fig. 4(a)." (long/07_targets.tex:62
  is the source of that sentence).
- S7.1 p. 13 (long/09_real.tex:72): "no file between its pawns and T is free of pawns" (there is no file between e and f at all)
  → "file e holds pawns and file f the white king, so T has no empty buffer" (true: T = W Kf5 g4 / B Kh4 g5).
- S14 p. 74 and Notes 2-4 state their theorems "for every heap h < 256"; the main text's definition (05_sums.tex:27-28) says
  "for every heap h". The heap step of each note uses no bound (as S13 and Note 1 now say), so write "for every heap h ≥ 0" in
  those statements.
- 01_intro.tex:63: "the material moved out of this version" tells a reviewer that another version exists. "further details"
  is shorter.

**12. Submission files (outside the PDFs).** dist/tog/submission/pdf_checks.md:3 still says "supplement 106 pages"; the review
supplement has 109. scholarone_fields.md:11 says "3 words of headroom" for a 199-word abstract with a 200-word limit.

## 4. Checks that passed (no finding)

- Theorem 3, Corollary 4, Definition 5, Theorem 6 and the certificate sentence against A.3, A.7, A.11, A.13, A.15-A.16: the
  main-text hypotheses imply the precise ones (A.3), five ranks and buffer match A.III, both proof sketches sketch the
  supplement's proofs. Proposition 7 (a), (b) re-derived from A.14.
- Section VIII ring statements against S13 Theorem 1, Lemmas 1-3 and C1-C2, S14, S15 Notes 2-6 and Table S4: n+3 family for
  n ≥ 5 with two programs to n ≤ 61; M10 and O11 match S14's formulas (M10 = W b2 d2 e3 h3 j5 / B a4 c6 f6 g7 i7, also Fig. 1(b));
  E8 example ring of S6.3 matches S13's E_n; ⋆3 families n+2 (even ≥ 8, odd ≥ 11) and n+1 (≥ 12) match Notes 2-4; Möbius minima
  6, 8, 6, 8, 8, 8 and 10, 10, 11 match Table S4; Fig. 6 matches W5's records (C7, C8: 10; C10: 12; C11: 12; C12: 13).
- Numbers: 92.5% = 1896/2049, 83.0%, 83.7%; 128 = 159 − 31; 52 = 18 + 34; 19.3% = 11,300/58,595; Table IV row sums 226 = 233 − 7;
  290 + 12 = 302, 283 + 5 + 2 = 290; 326,640 = 160,656 + 165,984; census 6,724 / 4,042 (RESULTS.md:47); 793,299 (RESULTS.md:289);
  5,503,282 (research/star2_frontier/REPORT.md:26); 1,418,480 (RESULTS.md:653); Table III against RESULTS.md:71-80; 0.66%
  (RESULTS.md:426); S10's "two more problems" = 6 − 4. dist/tog/check_numbers.out reports all numbers found (run Nov 22, before
  the last rebuild).
- Section pointers S1-S17 in the paper all resolve to the right content.
- Pawn histories of the 1/8, ↑²⋆, Tiny 1, A and B; FENs of Table S8 (script check, 17/17).
- References: all entries have authors, venue, year or access date; no missing data found.
- AI-use statements: Section XIII, the acknowledgment, the supplement's preface and S17 agree on who wrote and who checked the
  ⟨S⟩ proofs, and S17's tables cover every ⟨S⟩ result of the paper (S12.1, S13, S14, Notes 2-6). Gaps: findings 2, 3, 6.

## Summary

Recommendation: minor revision (first round: major).
R14 items: 7 fixed (1, 3, 5, 6, 7, 10, (i)); 3 partly fixed (2, 8, 13); 2 fixes introduced a new problem (4: Def. 12;
12: the (E) ⟨P⟩); 9 fixed in the review PDFs, residue only in S12.2/S15; 11 declined.
New findings: 2 must fix, 5 should fix, 5 optional (12 in all).
Must fix:
1. Definition 12 (09_real.tex:10-12, p. 7): "scoring the end position {B r_W | B r_B}" now applies to all draw treatments and
   disagrees with oracle_value.py for draws counted as wins; replacement given (+3 chars).
2. "(E) ... in our model ⟨P⟩ (Section S12)" (05_sums.tex:54, p. 5): an AI-written supplement proof labelled "proved here";
   make it ⟨S⟩; same issue for S13's ⟨P⟩ lemmas in the supplement.
Should fix: ⟨C2⟩ definition vs Lichess-tablebase cases (+4 chars); "no human referee has yet." (−2); Prop. 7 ⟨C2⟩ with one
program for S(X) in the records; "hand proof" for AI-written proofs in the supplement; S12.2 dependencies (S2's (V2) test and
Theorem S4, the 12.5-20.5% loopy data, the locked-pair ⟨C2⟩ of Conclusion item 3) and the unevidenced h ≈ 5-7 ⟨Conj⟩.
Main-text ⟨S⟩ results do not depend on S12.2.
Space: the proposed paper edits save 65 rendered characters net (finding 8 pays).
