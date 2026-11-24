# R18: Does anything depend on S12.2 of the ToG supplement?

Read-only audit, 2026-11-23. Nothing was built or edited outside this folder. Page numbers are PDF pages of
dist/tog/supplement.pdf (108 pp.; text in supp.txt here); S12.1 = pp. 17-23 (top half), S12.2 = pp. 23-69.
Line numbers are for the sources: dist/tog/sections/*.tex (10-page paper), dist/tog/supp_src/*, dist/tog/tools/build_supplement.py
(supp/s*.tex are GENERATED from it, so edits go to the generator or its inputs, not to supp/).
Note: supp/s02.tex (S2) is copied by build_supplement.py:60-70 from the LONG paper, paper/ieee/sections/04_kings.tex lines 89-127, 129-154, 158-168.

## Bottom line
- Nothing in the 10-page paper depends on S12.2. Every claim there that is labelled S and cites S12 is proved in full in S12.1 (A.1-A.17).
- Only two S-labelled statements anywhere (both in S2, pp. 3-4) get their proof only from S12.2: Theorem S4 (spare moves, = Theorem 3.4)
  and the sentence on the (V2) passer test "known only if king moves also lose" (= Proposition 2.11). One more S-labelled sentence
  ("Clause (ii) cannot be weakened to h-1 moves", Theorem S1) is supported only by hand-checkable examples in S12.2 that the note itself labels CONJECTURE/data.
- The rest of S12.2 (about 40 of its 47 pages: Theorems 1.9-1.11(a,b), 1.14, 1.15, 2.3-2.7, Lemma 2.9, 3.2-3.3, 3.7-3.12, the checks) supports no
  claim in the paper or in S1-S11/S13-S17 that is not already proved in S12.1.

## A. The 10-page paper (dist/tog/sections/*.tex, tog.tex)

| # | Where | Sentence / claim | Label | Proved in full by S12.1? |
|---|---|---|---|---|
| A1 | 01_intro.tex:41-44 | contributions: (V1)-(V3) give the whole-board pawn game, (V4) the +-BIG value, sum-safety theorem | S | Yes: A.11, A.13, A.7 |
| A2 | 04_kings.tex:48-72 Thm validity; 66 "The full proof is in Section S12" | validity of the convention, board >= 5 ranks | S | Yes: A.10-A.12 (A.11 is the chess form of note Thm 1.14(i), proved as its sharp form) |
| A3 | 04_kings.tex:69-76 Cor v4 | (V4) gives the +-BIG result | S | Yes: A.13 (with A.7) |
| A4 | 04_kings.tex:80-86 | "certificate of horizon h ... In the promotion game such a move loses for its mover [S] ... The exact clauses and the proof are in Section S12; a local test for (V2) and the loopy games of kings with spare moves are in Section S2" | S for the first claim | Yes: A.15 (maps the sentence to C1-C3), A.16 (theorem), A.17. The (V2) test and "loopy games" are only pointed to (S2), not claimed here |
| A5 | 04_kings.tex:83-85 "in chess even wider margins can fail" | no label; examples in S2 p.4 are C1 | none | n/a (not S12.2) |
| A6 | 05_sums.tex:37-46 Thm hss; 44-46 "The full proof, by induction with (E), is in Section S12" | sum safety | S | Yes: A.1-A.9 (A.6, A.7 = frontier step and induction of note Thm 1.11(c)) |
| A7 | 05_sums.tex:53 "With BIG=256 the move bound always holds on boards up to 8x8" | tempo bound | no label | Yes: A.9 (168 < 256) |
| A8 | 05_sums.tex:54 "(E) ... in our model P (Section S12)" | (E) cannot be dropped | P | Yes: S12.1 Remark "(E) cannot be dropped" (supp_src/s12a_core.tex:200-208), hand argument |
| A9 | 05_sums.tex:56-61 Prop sumcounter | counterexample to top-level-only test | C2 | A.14(a),(b) proved in S12.1; (c) computed, "used nowhere" |
| A10 | 04_kings.tex:88-101 failure sweep (159/500, 128 mismatches, 2,154/2,049, 92.5%) | C1 | not in S12.2 at all (repo data; "Section S2", "Section S16") |
| A11 | 04_kings.tex:96-99 square-rule passer test; 14_conclusion.tex:5 | repair removes 52 failures | C1; "not sound on every board (Section S16)" | S16 (p.105) is self-contained, claims no proof; independent of S12.2 (Cor. 2.8 / "rule of the square" in S12.2 is a different thing: king distance, not the sdist test) |
| A12 | 14_conclusion.tex:13-14 | "certificate theory settles the promotion game, not chess; real trebuchets seem to need h about 5-7 [Conj] (Section S2); in the promotion game even a locked pawn pair can break their zero [C2]" | Conj, C2 | n/a. Evidence for the locked-pair claim is printed only in S12.2 p.49 (Z_T = Ka4 Pb3 kc3 pb4 on cyl:7x6 with G2 = {Pe2, pe3}; CHECKED-2, no hand proof); the paper cites S2, which only restates it. The h about 5-7 and 12.5-20.5% figures are not in S12.2 |
| A13 | 13_verify.tex:11, 15; 01_intro.tex:37,63 | "AI models wrote the full S proofs ... Sections S12-S15" | | still true with S12.1 only |
| A14 | 02_rules.tex:30 | "Maeser models such global threats with loopy games" | citation | none |

Not present in the 10-page paper at all: the horizon-1 proposition, Theorem 3.4 / "spare king moves are loopy", Proposition 2.11, the
"cannot be weakened to h-1" sentence. They live in S2 (copied from the long paper). So for the 10-page paper: the certificate statement in
Section IV is covered by A.15-A.17; "spare king moves are loopy" is a pointer only (04_kings.tex:85-86); the tempo bound by A.9; the
square-rule test is C1 + S16; the failure sweep is C1 with no S12.2 content.
The paper hard-codes "Section S12"; it stays correct if S12.2 goes (A.1-A.17 are S12.1); "S12.1" would be more precise, optional.

## B. The other supplement sections

Pointers (curious reader only; nothing needed for a claim):
- supplement.tex:85 and :104; p.1 and p.17: "Sections S12-S15 give the full proofs behind the S labels" (stays true only if the S labels in S2 are handled, see C).
- supp/s02.tex:2 (from build_supplement.py:64): "Full proofs are in Section S12" (p.3).
- supp_src/s12a_core.tex:295 remark (d): "Unlike (V1a) of Theorem 1.14 in the longer treatment, (V1) contains no condition (E)": comparison remark, not used.
- supp_src/s12a_core.tex:419-425 "Where to find the longer treatment" (p.23): maps A.x to note numbering (Lemma 2.2, Def 1.10, Thm 1.11(c), Prop 1.12, Thm 1.14, Prop 1.15(a), Def 2.6, Thm 2.7(a)). Pure pointer.
- S12.2's own preface (tools/build_supplement.py:349-355; p.23) and its dangling references to "Sections 4-8 and Appendix A of the source note, not reproduced".
- S13-S15 (pp. 70-104) cite only each other, S13 lemmas, and research/*/PROOF*.md; no S12.2 item (checked by grep of supp/s13-s15.tex and supp_src/s14,s15*). S1, S3-S11: no S12.2 item. S16 (p.105): none.

Used for a claim (S2, pp. 3-4; source supp/s02.tex, i.e. paper/ieee/sections/04_kings.tex):
- p.3 Theorem S1 [S] (s02.tex:11-15; ieee 04_kings.tex:97-101): first two sentences proved by S12.1 A.16/A.17. The last sentence "Clause (ii) cannot be weakened to h-1 moves" is NOT in S12.1. Its only support is S12.2 p.45 ("The conditions cannot be dropped", note lines 1039-1054; e.g. Kf5 kc6 Pe4 pb3, White wins in P, T = 2, mu_s = 2), where the note itself says "the claim keeps the label CONJECTURE; the races can be checked by hand".
- p.4 "For (V2) a local test is known only if king moves also lose [S]: ... its path is empty and every enemy pawn, passed or not, needs a move more to promote" (s02.tex:21): this is Proposition 2.11 (note lines 1306-1402, pp. 50-52; hypotheses H1-H5, H5 = timing mu >= e+1). Proof only there.
- p.4 Proposition S2 [S], horizon 1, >= 6 ranks (s02.tex:26-30): its own 4-line proof is printed in S2 and is self-contained. S12.2 Prop 2.10(a) (p.48, H >= 5) is a stronger version; not needed.
- p.4 Conjecture S3 [Conj]: no proof needed. "locked pawn pair can break their zero [C2]" and "h about 5-7 [Conj]": evidence in repo; S12.2 p.49 for the former.
- p.4 Theorem S4 [S] (s02.tex:51-55; ieee 04_kings.tex:136-148): only a 4-line "Proof sketch" in S2. Full proof = Theorem 3.4 (note lines 1636-1680, p.58) with Defs 1.1-1.3 (pp. 24-25) and Def 3.1 (p.56). The sketch's step "a winning side never needs to pass" needs S12.2's Lemma B / part (a) argument (Lemma B, p.66, warns "never passes is too strong"; a winning pass can exist, the stage argument on p.58).
- p.4 "Since on exceeds every number, +-B fails": KNOWN fact (note Thm 3.3, p.57 proves the shuttle version); unlabelled.
- S17 (pp. 105-108; supp_src/s17_provenance.tex, generated into supp/s16.tex:29-159): Table S9 row "Longer treatment, S12.2: Theorems 1.11(c), 1.14, 2.7, 3.4; Propositions 2.10(a), 2.11" (s17_provenance.tex:43-54; supp/s16.tex:70-81), and the paragraph "What the checks found" naming "Theorem 3.4" and "Theorem 1.11(c)" (s17_provenance.tex:125-126; supp/s16.tex:152-153; p.108). The row also carries the provenance statistics (22,522,464 comparisons for Thm 3.4 etc.). This is provenance of work in S12.2 and would become orphaned, and the cross-vendor check record for Thm 3.4 / Prop 2.11 would have to be kept somewhere if those stay.
- Table S9 caption (s17_provenance.tex:14) and S12 title (build_supplement.py:345; supp/s12.tex:1; TOC p.1) say "loopy games".

## C. Results labelled S/PROVED whose only proof is in S12.2

1. Theorem S4, outcomes with spare moves (S2 p.4; also the long paper's thm:loopy). Proof: note Theorem 3.4 (and the D-game defs 1.1-1.3, Def 3.1), pp. 24-25, 56, 58. About 2 pages of source; this is the only S claim whose statement is the headline of a whole S2 subsection ("Spare King Moves Are Loopy").
2. S2 p.4 sentence on the (V2) local test, labelled S (frozen-king passer certificate): note Proposition 2.11 + Cor. 2.11a, pp. 50-52 (about 2.5-3 pages; its checks run to p.54).
3. Last sentence of Theorem S1 ("cannot be weakened to h-1"): the note labels it CONJECTURE with hand-checkable data (p.45). It is an S-labelled claim without a proof anywhere in the supplement (label inflation): either cut the sentence or print the two-line example.
Not in C (already proved in S12.1 or inline): validity theorem, Cor v4, sum safety (= note Thm 1.11(c)), certificate theorem (= note Thm 2.7(a)), (E)-cannot-be-dropped remark, horizon-1 (inline in S2), A.14(a,b). Everything else in S12.2 is extra: it is not cited as the source of any labelled claim.

## D. Is LOOPY.md in the anonymous code copy?
Yes: dist/anon/out/cylinder-chess-review/kings/theory/LOOPY.md (4,166 lines, 514 KB) and REVIEWS.md; included by the whitelist rule
"kings/theory/*" in dist/anon/build.py (reason text "Section III, S12"). Caveats:
- It is a later revision than what S12.2 typeset (S12.2 is lines 225-2213 of the repo note at build time; the anon sections 1-3 are 2,248 lines vs 2,081 in supp_src/s12_kings.md, with K45-K55 and new "revised after ..." status text). The numbers of all cited items match (Thm 1.11 line 453, 1.14 line 722, sharp form 821, 2.7 line 1149, 2.8 line 1409, 2.10 line 1510, 2.11 line 1635, 3.4 line 1994), so pointers "Theorem 3.4 of kings/theory/LOOPY.md" would resolve. Statement wording and some labels differ (e.g. 1.11 "(a) PROVED, (b) PROVED after repair").
- The anon README (README.md:80) lists only kings/theory/REVIEWS.md for Section III, not LOOPY.md; S12.2 is the only place in the review PDFs that names it. A pointer would need to say the path, and the README row should add it.
- The anon supplement S17 says referee reports are not in the copy; REVIEWS.md is. LOOPY.md is 500 KB of working note (status table, K-numbers, sections 4-8); readable but not reviewer-friendly, which is the referee's complaint.
- LOOPY.md itself says the S12.2 results were mostly written by free models and read once (status table, lines ~19-60), so removing the printed copy removes the supplement's only edited, de-noised version.

## E. Recommendation
Choose (3), in its narrow form: delete S12.2 and keep only the two proofs the supplement's S labels still need, restated in S12.1 style.

Option 1 (keep as is): 108 pp., no edits; the referee's complaint stays.
Option 2 (remove all): 62 pp. (S13 would start on p.24, 108 - 46). But then S2 p.4 has two S labels without a printed proof (Theorem S4; the (V2) test) and the supplement's promise (p.1, p.17: "full proofs behind the S labels") is false for them. Needs the label changes below.
Option 3 (keep only list C): 
 - Theorem 3.4 with Defs 1.1-1.3, 3.1: about 2 pp., rewrite as A.18 in S12.1 (pp. 24-25, 56, 58 of the note).
 - Proposition 2.11 + Cor. 2.11a: about 3 pp. (pp. 50-52); optional if the p.4 sentence is cut or relabelled "see the repository note".
 - Sharpness example of the last sentence of Thm S1: 0.2 p., inline in S2, or cut the sentence.
 Resulting supplement: about 62 + 2 = 64 pp. without Prop 2.11, about 67-68 pp. with it.
 Recommended: keep both proofs (about 67 pp.), because it keeps the invariant that every S label in the supplement has a printed proof; cut the "cannot be weakened" sentence unless the example is printed.

Edits for option 2 or 3 (all line numbers in dist/tog/, not rebuilt):
1. tools/build_supplement.py:349-355: remove the "Longer Treatment" subsection and the MD('kings/theory/LOOPY.md', 225, 2213, ...) call and its NOTE text (option 2); for option 3 replace MD(...) by one or two small MD slices or hand-written A.18/A.19 appended to supp_src/s12a_core.tex.
2. tools/build_supplement.py:345 and supp/s12.tex:1 title: drop "Certificates and Loopy Games" if nothing about loopy games remains (option 2); no change for option 3.
3. supp_src/s12a_core.tex:419-425: replace the "Where to find the longer treatment" paragraph by one sentence: "The full working note, with further results, is kings/theory/LOOPY.md in the code copy". Also :295 (remark (d)): change "in the longer treatment" to "in kings/theory/LOOPY.md". Also the intro of S12.1 (lines 5-12) already says it can be read alone; "the one computed statement ... is used nowhere" stays.
4. supp_src/s17_provenance.tex:43-54 (supp/s16.tex:70-81): option 2 delete the row; option 3 shorten to "Theorem 3.4 (now A.18) ...; Proposition 2.11 ..." keeping the checker facts (Codex yes; 763,440 games; several programs). :125-126 (supp/s16.tex:152-153; p.108): keep the Theorem 3.4 sentence if kept (renumber to A.18); the Theorem 1.11(c) sentence refers to A.7's move-count step: rename or drop; caption :14 fix as in 2.
5. S2 (source: paper/ieee/sections/04_kings.tex copied by build_supplement.py:60-70; use .replace() in the generator rather than editing the long paper): 
   - Theorem S4 (ieee 04_kings.tex:136-148; supp/s02.tex:51-63): option 2: it has no printed proof, so change \lab{S} to a new label or delete the theorem and keep a pointer; option 3: keep label, replace "Proof sketch" by "Proof: Theorem A.18".
   - (V2) sentence (ieee 04_kings.tex:105-108; supp/s02.tex:21-24): option 2 change \lab{S} to a pointer "proved in kings/theory/LOOPY.md, Prop. 2.11"; option 3 keep and cite A.19.
   - Theorem S1 last sentence (ieee 04_kings.tex:100-101; supp/s02.tex:14): delete "Clause (ii) cannot be weakened to h-1 moves" or give the Kf5 kc6 Pe4 pb3 example.
6. supplement.tex:85, :104 (supplement_review.tex only wraps it): reword "Sections S12-S15 give the full proofs ... as written in the project's proof notes" (S12 is no longer a typeset note); optional.
7. 10-page paper: no required edit. Optional: 04_kings.tex:66, 86 and 05_sums.tex:46,54 "Section S12" -> "Section S12.1" (use \ref{S-core}? the paper has no access to supplement labels, so hard-code).
8. paper/ieee (long paper): none required (see F).
9. dist/anon README row for Section III (README.md:80 is generated by dist/anon/build.py): add kings/theory/LOOPY.md next to REVIEWS.md.
10. Rebuild order per tog/sbuild.sh: tog_review first, then tools/build_supplement.py, then supplement and supplement_review; recheck the TOC page numbers (S13 -> p.24 in option 2) and check_numbers.py.

## F. The long (IEEE) paper, paper/ieee/sections/*.tex
- It never cites S12.2 or the note by name (no hit for "S12", "LOOPY", "kings/theory", "Theorem 1.x/2.x/3.x" in sections/*.tex or main.tex). It says only that S proofs are "in the repository" (01_intro.tex:30-31; 05_sums.tex:111-112 "The proof, by induction with (E), is in the repository"; 05_sums.tex:120 "the position is in the repository"; 13_verify.tex:12-15, main.tex:32 "anonymized repository supplied to the editor").
- It does contain the S2 material in full with labels: Theorem cert (04_kings.tex:97-101) incl. "cannot be weakened", the (V2) test [S] (105-108), Proposition horizon1 [S] (111-120), Theorem loopy [S] with proof sketch (136-148). Their only full proofs are therefore the repository note (kings/theory/LOOPY.md, Thm 2.7, Prop 2.11, Thm 3.4), i.e. S12.2's source, plus S12.1 for validity/sum safety/certificate, which the long paper does not mention (it predates S12.1).
- Effect of removing S12.2 from the ToG supplement: none on the long paper's text; the long paper keeps pointing to the repository, where LOOPY.md remains (D). Check only that the anon copy used for the long paper also ships kings/theory/* (same whitelist).
