# Mock review 3 (IEEE Transactions on Games, double-anonymous)

Paper: "Chess Endgames on a Cylindrical Chessboard: Exact Combinatorial Game Values, Real-Chess Checks, and Tablebases" (10 pp.) and its 95-page supplement.
Reviewer stance: sceptical expert in combinatorial game theory (CGT) and game solving. Sections 1-6 were written before any earlier review or project notes were opened. Line references are to `dist/tog/sections/*.tex` and `dist/tog/supp/*.tex`.

---

## 1. Summary and novelty

**Summary (five sentences).**
(1) The paper studies king-and-pawn endgames on the cylinder (files a and h joined) in Elkies' pawn-only model: a passed pawn is worth ±B, and the kings stand frozen in a trébuchet worth 0.
(2) It adds a passed-pawn test that takes en passant into account (Def. 1). It gives conditions (V1)-(V4) under which the frozen trébuchet and the component-sum model give the chess result (Thm 3, Cor 4, Thm 6), and it shows that a cut along an empty file reduces the cylinder to an ordinary board (Thm 2).
(3) By exhaustive search it finds that no ⋆k with k ≥ 2 has six pawns or fewer, and that ⋆2 first appears with seven pawns, in one position and its colour-reversed twin (Thm 11). It gives least-pawn ring nimbers on C_n, with insertion ("wall") proofs for infinite families (Fig. 6, S13-S15).
(4) It tests model values against real chess through an "oracle value" that keeps the model tree and puts tablebase or solver results at its leaves. The textbook ⋆2 candidate is hot in chess, and the 1/8 position keeps oracle value 1/8 with frozen kings and queen promotions only.
(5) Side studies: pawnless and KPK tablebases on the cylinder and torus, a corrected ring rule for Dawson's chess on the cylinder, and a 233-position engine pilot.

**What is new relative to the cited literature.**
- *Elkies 1996 [5]* set up the model: ±B passed pawns, the trébuchet, and the values 1/2, 1/4, ↑, ⋆ and tinies on the ordinary board, with en passant left as an open issue. New here: the cylinder setting, a precise e.p.-aware test, explicit hypotheses under which frozen kings and the sum model are right (Elkies uses both informally), exhaustive censuses, and legal 10-man positions for 1/8, ↑²⋆ and tiny(1). The paper says plainly that these kinds of value are not new (07_targets.tex:8). That is accurate.
- *Elkies 2002 [6]* builds higher nimbers from Dawson-like pawn play on large boards. The paper's main claim is a model ⋆2 on the 8×8 board with seven pawns on four files, and a minimality proof by census. This is new only if [6] (and [5]) contain no ⋆2 on 8×8 in the same model. The paper never says exactly what [6] proves for the 8×8 board; it says only "Elkies' higher nimbers need larger boards" (08_star2.tex, end of VIII-E). The authors must quote, with section or page, what [5] and [6] say about ⋆2 on 8×8.
- *Drummond-Cole 2005 [8]*: ⋆2 in chess using pieces other than kings and pawns. The paper's ⋆2 is a pawn-model value whose real-chess value is open, so it does not supersede [8]. The abstract says so ("its real-chess value is open"). Good.
- *Wu, Yü and Landry [10]*: only the presentation format is borrowed. Fine.
- *Dawson [7], Guy-Smith [17]*: the strip values (octal 0.137) are classical. The cylinder ring rule (Thm 16) is a short new observation. The claimed novelty, "we correct earlier work", refers to an *unpublished* manuscript [9], so it is not a contribution to the literature (see M4).
- *Mäser 2002 [11]* models global threats (a passed pawn ending the game) in CGT. It is cited in one clause (02_rules.tex:30). It is the closest prior work to the sum-safety theorem (Thm 6) and the whole-board versus sum distinction, and it needs a real comparison: does Mäser already give a sufficient condition for when the sum model is right?

**Possibly missing prior work** (only items I am confident exist):
- M. Müller, "Decomposition search: A combinatorial games approach to game tree search, with applications to solving Go endgames," IJCAI 1999. This is directly relevant to Section XII-C (alpha-beta versus CGT on sums, "4-9 times as many nodes per added component").
- E. Berlekamp and D. Wolfe, *Mathematical Go: Chilling Gets the Last Point*, A K Peters, 1994. This is the standard example of exact CGT applied to endgames of a real game. It is the right comparison for "exact values in real endgames".
- T. E. Plambeck, "Taming the wild in impartial combinatorial games," *Integers* 5 (2005), G5. This is the origin of misère quotients, relevant to the misère Dawson discussion beside [18].
- A. N. Siegel's CGSuite (software). It is the obvious independent tool for checking canonical forms such as {0,⋆|↓} = ↑²⋆, and it should be cited if any check used it.
- Not sure of exact references: (i) prior tablebases for chess variants (cylinder or torus boards, or other variant tablebases), beyond the prose sources [14], [15]. The claim "We found no earlier tablebase for them" (10_tablebases.tex:8) needs a stated search. (ii) Work that tests engines on zugzwang or fortress positions, for Section XII.

**Is the novelty claimed accurately?** Mostly yes inside the body, with careful hedges ("in the model", "its real-chess value is open"). Three exceptions: the abstract's "We correct earlier work" (unpublished work); "give conditions under which frozen kings are exact" (the conditions (V2) and (V3) assume the chess results at the decisive events; see M2); and the title's "Exact Combinatorial Game Values", which are exact only in a model that disagrees with the tablebase in 52 of 233 small positions (12_engines.tex:10-11).

---

## 2. Recommendation: **Major revision**

The three reasons that drive it:
1. **Proof status.** The ⟨S⟩ results are the paper's main theorems: validity of the convention, sum safety, and the n-pawn and n+1-pawn ring families. By the paper's own statement (13_verify.tex:11-12) they rest on AI-written proofs that no human has checked, including, apparently, the authors. The supplement shows that the checks were uneven: some proofs were refereed only by the writer's model family, and one was revised by its only referee (S15 Notes 2 and 3).
2. **Model-reality gap and hidden hypotheses.** The exact values belong to a pawn-only model that disagrees with real chess in 7.5% of decisive 8×8 positions, in 159 of 500 swept components under the textbook test, and in 22% of the engine suite. The validity theorem moves the hard part into hypotheses (V2) and (V3), which cannot be checked without solving chess. Several hypotheses in the stated theorems sit only in the supplement.
3. **Scope, readability and verifiability.** About twelve studies are packed into 10 pages. Definitions and numbers are compressed to the point that many sentences cannot be parsed. Table I concerns an unpublished manuscript reviewers cannot see. The supplement is largely internal proof notes "typeset unchanged", with repository paths and dangling references. The code link is a placeholder, so no C1 or C2 claim can be checked.

The ⋆2 census, the seven-pawn ⋆2 with its minimality, the ring families and the cylinder tablebases are interesting and in scope for ToG. With the changes below the paper could be accepted.

---

## 3. Major issues

### M1. Theorem statements leave out hypotheses that the full proofs need (soundness)
- **Thm 3 / Cor 4** (04_kings.tex:45-72). The precise forms in S12.1 (A.11-A.13) need: (i) a board with at least five ranks (Remark A.12(c); Lemma A.2(c) fails on four ranks); (ii) a *local* race rule (Remark A.3); (iii) a pawn on its last rank stays a pawn and counts as passed (Remark A.3); (iv) (V1)-(V3) for *each* side to move for which the result is claimed. A.13 gives a king group, W Kb6 c7 / B Ka8 a5, where the hypotheses hold with only one side to move. Yet the main text states "the chess result, with either side to move, is the outcome of W(X)".
  *Smallest change:* at 04_kings.tex:45, "Let a position consist of" -> "On a board with at least five ranks, let a position consist of". At 04_kings.tex:58, "with either side to move" -> "for each side to move for which (V1)-(V3) hold". Add one sentence to Section II-C: "Race rules are local, and a pawn on its last rank stays and counts as passed."
- **Thm 6** (05_sums.tex:57-61). "B exceeds the number of moves either side can make" is undefined in the main text; S12 uses N(X), the largest number of moves of one side in any sequence of legal pawn moves from X. The main-text Definition 5 and the threat definition omit "before the first passed pawn". Remark A.3 then has to argue that the main text's version implies its own. State the precise form in the paper, since it is no longer.
- **"W(X) is a ⋆k"** (05_sums.tex:47-49) is defined as matching ⋆k + ⋆h in outcome for every heap h. S14 and S15 restrict this further to h < 256 and say they do *not* claim equality against arbitrary addends. In fact, once terminal positions are scored ±B, W(X) is an ordinary short game, and S13's proof concludes G = ⋆2 from "G + ⋆2 is a P-position", which *is* CGT equality. Pick one meaning, state it once, and drop the "against nim-heaps only" hedges in S14 and S15 if equality holds. As it stands, the reader cannot tell whether "ring ⋆2" means a CGT value or a Grundy-like signature.
- **Thm 2** carries ⟨P⟩, ⟨C2⟩, and **Prop 7** carries ⟨C2⟩, but S12 A.14(c) says the S(X)/W(X) outcomes were "checked by computer only". It does not say by two programs. Reconcile the labels.
- **Theorem 16** "⟨P⟩, machine-checked for n ≤ 22". The proof is fine (I checked it; see below). Say which program checked it and against what.

**Spot check 1: sum safety, S12.1 (Lemmas A.4-A.6, Theorem A.7).** I read it line by line and found it sound under its precise hypotheses. The induction on Φ_W + Φ_B is correct. A.4 uses (E) correctly to drop unusable rights from the sum. In A.6, White's "move only in +B" strategy works because, by A.5, Black's moves never create a threat for Black; Black's moves after μ extend the play from X to a legal sequence, so there are at most N(X) of them; and B > N(X) gives White enough moves. The bound N(X) ≤ n(H-1)(H-2)/2 = 168 < 256 on 8×8 (A.9) is right. Two remarks: (a) the result is essentially a "no opposite threats, therefore no cancellation" argument, and the main text should say it is this simple; (b) HSS is a condition on the whole reachable set, which costs a search as large as solving W(X). The paper should say how HSS is decided in practice (05_sums.tex:68-71 reports 540,503 HSS positions) and why one would then use S rather than W.

**Spot check 2: n-pawn rings, S14 (with the lemmas of S13).** Lemma 1 (reduction), Lemma 2 (wall pawns; I re-derived the five poisoned moves of the table in S13) and Lemma 3 (insertion) are correct as far as I can see. One point needs fixing: in S13 Lemma 2(b), "Z = X" uses X both as "the player making the move" and as a position name in the main text; reword. The theorem for n ≥ n_0 is, however, a **computer-assisted proof**. It needs the facts C1 (the 441-node and 2132-node reduced graphs, their "zone", and that every node keeps files c-4..c+5 as pattern files) and C2 (n = 10..16 and 11..17 by direct search). S14 itself says "proved modulo C1" (S14 §6.3). The main-text label ⟨S⟩ ("proof sketched; full proof in the supplement") hides this.
*Smallest change:* define a combined label, ⟨S+C2⟩ ("hand proof whose finite base was computed by two programs"), and use it in the intro bullet (01_intro.tex:51), at 08_star2.tex:117-122 and in the Fig. 6 caption.

**Spot check 3: small computations (my own Python).** All of the following are correct:
- the Dawson recurrence (1): g(0..39) is the known 0.137 sequence, with period 34 and last exception at n = 51;
- the ring-rule list n = 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57;
- the identities {0,⋆|↓} = ↑²⋆, {0|1/4} = 1/8 and {0|-1} = -1/2 ± 1/2;
- 0 < tiny(1) < ↑;
- {2±1 | -2±1} is neither 0 nor ⋆2, with mean 0 and temperature 2.

By hand I also checked: Fig. 2(b) is 0; the W a2 b3 / B b4 example is 0 under Def. 1 (after a2-a3 b4×a3 both sides have passers, and black's needs 2 moves against white's 5); and the S16 counterexample (W a4 b6 / B c7, Black to move: c×b6, a5, b×a5) is valid.

### M2. Overclaiming about the validity of frozen kings
The abstract says "give conditions under which frozen kings are exact" (00_abstract.tex:4-5), and the intro credits "conditions (V1)-(V3) under which a frozen trébuchet gives the result". But (V2) ("in chess, the side that gets a passed pawn wins") and (V3) ("in chess, every move in Z loses") *assume* the chess outcome at every decisive event. Theorem 3 is then a bookkeeping lemma: if every decisive event is scored correctly, the game is scored correctly. The only local test, the certificate, works for the promotion game and "in chess even wider margins can fail" (04_kings.tex:85). The data agree: 107 of 159 failures come from the kings, and 128 mismatches remain after the square-rule repair.
*Smallest change (abstract):* "and give conditions under which frozen kings are exact" -> "and state when frozen kings give the chess result". Add to Section IV-A one sentence: "(V2) and (V3) refer to chess itself; we can certify (V3) only in the promotion game." The paper has about two spare lines; this sentence needs about one.

### M3. The role of AI: the ⟨S⟩ label as described would not satisfy a ToG editor
The text (01_intro.tex:36-40; 13_verify.tex:11-12; Acknowledgment) says AI models wrote the full proofs, AI referees "some from another vendor" checked them, and "no human referee has yet". Problems:
1. **Author responsibility.** IEEE policy lets AI tools help but makes the authors responsible for the correctness of all content, and the acknowledgment says "the authors ... are responsible for all content". Yet "no human referee has yet" tells the editor that the authors themselves have not verified the proofs. Either the authors verify each ⟨S⟩ proof and say so ("The authors have checked each ⟨S⟩ proof line by line"), or those results must be presented as conjectures supported by unverified machine-generated arguments.
2. **The label is not uniform.** The supplement shows three tiers. Some proofs were refereed by another vendor (S12 core, S14, S15 Note 4). One had a single cross-vendor referee who then rewrote the text, "so the final text has had no referee independent of it" (S15 Note 2). One was refereed "only by AI models of the same model family" (S15 Note 3, the odd-n ⋆2 and ⋆3 families behind "n+1 pawns ... ⋆3 on every C_n with n ≥ 12 ⟨S⟩"). The paper's single ⟨S⟩ label erases this.
3. **"Referee" is the wrong word** for a model run; it implies peer review. Use "AI checker".
4. **Independence of the "independent programs".** Several C2 programs were "written from the rules by a different AI model" or by "one of the referees" (S14, S15). Two programs generated from the same specification by language models can share specification-level mistakes, for example the e.p.-flag convention, which the notes say needed repairs. C2 should say what was shared (the rules text) and what was not.

*Smallest change:* in Section XIII, replace "AI models wrote the full ⟨S⟩ proofs. AI referees, some from another vendor, checked them, and programs checked their finite parts; no human referee has yet." with "AI models wrote the full ⟨S⟩ proofs; Table S0 lists, per result, the writer, the AI checkers and their vendors, the programs that checked its finite parts, and whether an author has verified it." Add that one-table index (Table S0) to the supplement. Make the definition of ⟨S⟩ in the intro say "AI-written, AI-checked, finite parts computed; see Table S0".

### M4. Table I and the "earlier work" corrected are unpublished and unavailable
01_intro.tex:34-36, Table I (05_sums.tex:11-35), Section V-A, Fig. 3(c) and Section XI ("What was wrong") correct "an unpublished 2025 study" [9], cited as "Anonymous, Title withheld for review". Reviewers cannot see the puzzles (they are in S3), cannot check the claimed values, and have no reason to value a correction to a manuscript that was never published. The abstract's "We correct earlier work on cylinder Dawson's chess" is presented as a contribution.
*Smallest change:* drop Table I and the "What was wrong" paragraph, and keep one sentence: "Some values in an earlier unpublished study [9] are corrected in Section S3." That frees roughly a third of a column for the definitions asked for in M1 and M5. Abstract: "We correct earlier work on cylinder Dawson's chess:" -> "For Dawson's chess on the cylinder,". If [9] stays, give the editor an anonymized copy.

### M5. Clarity for a CGT reader who does not know the project
- **Notation clashes.** "S" is used for the sum model S(X), the evidence label ⟨S⟩, the supplement section prefix S1-S16, and the "test S" of S16. "Tiny 1" (abstract, 01_intro.tex:46, 07_targets.tex:9) is used alongside tiny(1). B is used for ±B and for "position B". W is used for White and for W(X). Proposition 7 calls its position X, which is also the pawn context of Theorem 3. *Fix:* rename the evidence label ⟨S⟩ to ⟨A⟩ ("AI-written proof") or ⟨F⟩; rename position B to A′ (it is A with colours reversed); use tiny(1) throughout.
- **Undefined at first use:** "count rule" (abstract), "whole-board" (abstract; defined only in Section V-B), "oracle value" (abstract; Section IX), "trébuchet T" (used in Fig. 4 and 5 captions before the reader is told where T stands), "default setting" (abstract), "decisive event" (used in Thm 3 before (V1)), "the census" and "the atlas" (Section II-D uses "the census of Section VI" before it is defined), "birthday at most 292" (why 292?), "square rule" (04_kings.tex:97, defined only in S16), "labeled placements" (08_star2.tex).
- **The "any width" step** (08_star2.tex:86-90) needs one sentence: a component without a passed pawn has at least two pawns, so seven pawns span at most nine files once empty runs are shrunk to one file. I believe this holds (components of widths 2 + 2 + 3 plus two gaps), but the paper does not say it.
- **The model scope of each headline** (S or W) shifts: Theorem 10 is about S (CGT engine plus C solver), while the "any width" extension and the rings are about W. Put the model in each theorem statement.
- **Figures and tables that need the supplement:** Table I (the puzzles are only in S3); Table III's "not ⋆2" entries (the values are in S6); Fig. 6 (the computed versus proved markers and the ⋆3 series start at n = 10 with a caption caveat).
- **The supplement is not a readable companion.** S12.2 (about 49 pages), S13, S14 and S15 are internal notes "typeset unchanged" with their own label system (PROVED/CHECKED-2/COMPUTED-1/KNOWN), internal file paths (research/.../PROOF_N.md, check_N1.py, cylcgt, kings/SPEC.md), and references to "§4-§8 and Appendix A ... not reproduced here" (S12.2 header). A ToG reviewer will not referee 95 pages in this form. *Fix:* keep S12.1 (self-contained and good) and rewrite S13-S15 in the paper's labels and numbering; move S12.2 to the repository.

### M6. Over-statement and selection in the real-chess numbers
- "The model names the real winner in 92.5% of 2,049 decisive 8×8 positions" (04_kings.tex:99-101; repeated in 14_conclusion.tex). These are the positions "whose real results we know", that is, small ones within tablebase reach. Say so in the conclusion: "of 2,049 decisive tablebase-sized 8×8 positions".
- The engine suite reports model-tablebase disagreement in 52 of 233 positions (12_engines.tex:10-11) without discussion. That is a larger error rate than the 7.5% above, and it should be reconciled or explained in one clause.
- "Stockfish at low depth is weakest on infinitesimals ⟨C1⟩" (01_intro.tex:60) rests on n = 27 and n = 17 classes of hand-picked positions. ⟨C1⟩ is a label for computations, not statistical claims. *Fix:* "in a 233-position pilot, Stockfish at depth 1-2 scored lowest on infinitesimals" and drop the label; give a significance test or a confidence interval in Table V.
- "Real-chess oracle value" (Def. 12) keeps the frozen-king pawn tree and uses chess only at the leaves. "Real-chess" overstates it. Call it the *leaf-oracle value*, or say "model tree with chess leaves" in the definition.

### M7. Reproducibility: what the anonymous repository must contain
"available at anonymized repository link" (13_verify.tex:14; supplement p.1) is a placeholder. Most claims are C1 or C2. The reviewers need an anonymized archive (for example an anonymous mirror or a Zenodo deposit under embargo) with:
1. Both programs behind every C2 claim, kept separate (CGT engine `cylcgt`, whole-board solver, C census solver, reference KP solver, the two retrograde tablebase solvers, the ring pump `rg.c` and the Python checkers E, C, R, F), each with a README saying which spec it was written from and by whom (human or model).
2. A claim-to-script table: for every number in the paper, the command, the expected output and the runtime, with hashes of large outputs. The C3 census (231,071 records), the 5,503,282-root scan, the 24 tablebases (607M values) and the 6.1×10^10-state solve cannot be rerun by a reviewer, so their output files or checksums must be deposited.
3. The FEN and model encodings of every named position (S11 covers only positions with kings).
4. The engine harness: Stockfish and Lc0 versions, the Lc0 network hash, node and depth settings, and the 233 positions with their labels.
5. Anonymization: the repository must not contain author names, git history or agent transcripts.

---

## 4. Minor issues

1. 00_abstract.tex:5: "no whole-board nimber above star has at most six pawns" -> "no position of six or fewer pawns has a whole-board nimber above star".
2. 00_abstract.tex:7-8: "star two needs six pawns on three files" -> "the least ring star two has six pawns, on three files".
3. 00_abstract.tex:9 and 01_intro.tex:46, 07_targets.tex:9: "Tiny 1" -> "tiny(1)" (in the abstract, "tiny one").
4. 01_intro.tex:51: "⟨S⟩" -> "⟨S+C2⟩" (see M1 spot check 2); the same at 08_star2.tex:117-122 and in the Fig. 6 caption.
5. 02_rules.tex:78: "changes at least 18,137 of the 231,071 values" -- why "at least"? If it is a lower bound because some values were not computed under both tests, say so; otherwise -> "changes 18,137 of the 231,071 values".
6. 02_rules.tex:30: "where B exceeds any count of spare moves (our programs use B = 256)" -> "where B exceeds the number of moves either side can make (we use B = 256)", which matches Theorem 6.
7. 04_kings.tex:92: "queen promotions only, at most two)" -> "queen promotions only)"; the trailing "at most two" cannot be parsed.
8. 05_sums.tex:83: "Our CGT engine computes S, as Elkies does [5]" -> "Our CGT engine computes S, the model of [5]".
9. 05_sums.tex:47-49: add "with terminal positions scored ±B" and drop "every heap h" if equality is meant (see M1).
10. 06_atlas.tex:6: "confirms their textbook winners" -> "confirms their outcomes under the textbook test".
11. 08_star2.tex (VIII-B): "every position in scope has birthday at most 292" -- give the reason in five words (presumably B = 256 plus the longest play), since it is what makes the search for ⋆k complete.
12. 09_real.tex:33 (Thm 14(a)): "1. a4 is unresolved ⟨C2⟩" -- an unresolved move cannot be ⟨C2⟩; move the label to the resolved clauses.
13. 09_real.tex:57: "A tablebase-backed oracle value" -- the 8- and 9-man leaves come from the authors' solver, not a tablebase -> "A solver-backed oracle value".
14. 10_tablebases.tex:8: "We found no earlier tablebase for them." -> "We know of no earlier tablebase for them." (and give the search done in the response).
15. 10_tablebases.tex:63-65: "They agree on all 326,640 cylinder positions and differ on exactly 6 ordinary-board positions, where only a rook promotion wins" -- say that the second solver is queen-only *by design*, so the 6 differences are expected, and the C2 label covers the cylinder only.
16. Table IV: "KBBK has the bishops on opposite colors" -> "KBBK: bishops on squares of opposite colour".
17. 12_engines.tex:50: "is perfect at all four budgets ... all 17 draws included ⟨C1⟩" -- an engine result is not a ⟨C1⟩ mathematical claim; drop the label.
18. 14_conclusion.tex: "nine make a ⋆3" -> "nine make a ⋆3 and no eight do on up to eight files ⟨C1⟩".
19. Fig. 3 caption: "a king group from the 2025 study" -> "a king group from [9]".
20. References: [10] is an undergraduate course paper with an "Accessed: Oct. 27, 2026" date; [12], [14], [15], [19], [20] are web resources. This is acceptable, but cite Syzygy (de Man) for the tablebase itself rather than only the Lichess API.
21. 13_verify.tex:1-3: the source comments mention "named build: the repository URL". Harmless in the PDF, but make sure no source files are uploaded.
22. Supplement p.1: "as written in the project's proof notes" -> "as proved in full".

---

## 5. The ten hardest sentences, with rewrites (each no longer than the original)

1. 00_abstract.tex:5-6. "With this test and the count rule, no whole-board nimber above star has at most six pawns on ordinary boards of any width, but star two appears with seven, in one position and its color-reversed twin, confirmed by three programs"
   -> "Under this test and the count rule, no position of at most six pawns on an ordinary board of any width has a nimber above star; with seven, star two appears once, plus its color-reversed twin, confirmed by three programs"
2. 00_abstract.tex:9-10. "We find positions with a legal pawn history worth one-eighth, up-second star and Tiny 1; with frozen kings and queen promotions only, the one-eighth position's tablebase-backed oracle value is one-eighth."
   -> "Positions with a legal pawn history have values one-eighth, up-second star and tiny one; the one-eighth survives tablebase leaves with frozen kings and queen promotions."
3. 02_rules.tex:99-100. "A ring leaves no pawn-free buffer for a king group (Section IV-A), so ring values belong to the pawn-only model."
   -> "A ring has no empty file to separate a king group (Section IV-A), so ring values are pawn-model values only."
4. 04_kings.tex:95-98. "The e.p.-aware test repairs the 18 e.p. failures, but the kings undo 13 of these repairs. ... Ending the game only at a passer that wins the race by the square rule removes all 52 convention failures with frozen kings; with real kings 31 stay repaired, which leaves 128 mismatches, all from the kings"
   -> "The e.p.-aware test fixes the 18 e.p. failures, but real kings break 13 again. Ending the game only at a passer that the square rule certifies fixes all 52 pawn failures with frozen kings, 31 with real kings; 128 king failures remain"
5. 04_kings.tex:82-85. "a move in Z has a certificate of horizon h if, with only Z on the board, the punisher promotes or mates within h moves of its reply, no defender pawn outside Z is that fast, and no stalemate comes first."
   -> "a move in Z is certified with horizon h if, with Z alone, the punisher promotes or mates within h moves, no defender pawn elsewhere promotes as fast, and no stalemate intervenes."
6. 05_sums.tex:87-89. "Of the 38 positions, 19 are exact and all agree with the sum; for the other 19, every second-player win among them, we have only bounds, and each contains it"
   -> "Of the 38 positions, 19 are solved and agree with the sum; the other 19, all the second-player wins, have only bounds, each consistent with the sum"
7. 05_sums.tex:73-75. "HSS cannot be dropped (Proposition 7); without (E) the decomposition already fails in the pure pawn game, without the passed-pawn rule"
   -> "HSS is needed (Proposition 7), and so is (E): without it, sums fail even in the pawn game with no passed-pawn rule"
8. 09_real.tex:10-13. "If a side is drawn, the draw treatment counts that draw as a win for black, as a win for white, or as worth 0; in the last case the end position is {B r_W | B r_B}"
   -> "A draw counts, by choice of draw treatment, as a black win, a white win, or 0; with 0, the end position is {B r_W | B r_B}"
9. 09_real.tex:41-44. "In the textbook tree we rule out ⋆2 only when draws count as wins for black or for white ⟨C1⟩; with draws worth 0 the textbook tree is not decided."
   -> "In the textbook tree, ⋆2 is excluded if draws count as wins for either side ⟨C1⟩, and undecided if draws count 0."
10. 09_real.tex:52-54. "A search for the larger end positions that decide the value leaves, after one eight-man result against the model, one eight-man position and three of nine men"
   -> "Of the larger deciding end positions, one 8-man result contradicts the model, and one 8-man and three 9-man positions remain open"

Runners-up: 08_star2.tex:80-81 ("The candidate needs the textbook test but survives e.p. off; A and B need en passant but not the textbook test") and the Möbius sentence at 08_star2.tex:134-135 ("by the cylinder's insertion proof away from the seam").

---

## 6. Anonymity

- PDF metadata: both PDFs carry only a Title (no Author, Subject or Keywords). OK.
- "Anonymized for review" byline; Acknowledgment names no people; the AI-tool disclosure (Claude, Codex, OpenCode, Kilo) is fine and required.
- **Self-citation [9]:** "This paper extends an unpublished 2025 study ... we check every position by computer, correct its errors" together with "Anonymous, 'Title withheld for review'". This all but says that [9] is the authors' own work. Under double-anonymous rules this is acceptable as phrased, but "Title withheld" is a giveaway and the work cannot be checked. See M4: either drop it or give the editor an anonymized copy.
- **Repository and package names in the supplement (main risk).** "cylcgt" appears 43 times, along with repository paths such as research/ring_n_proof/PROOF_N.md, kings/theory/LOOPY.md, kings/SPEC.md, research/v2_mechanisms/cc.py, rg.c and pump_verify.py (S12.2 header, S13-S16). If the project repository is public, a web search for "cylcgt" or these paths may reveal the authors. Remove the paths and rename the library ("our CGT engine") in the review supplement.
- S15 Note 5 says "U = a full-game solver ..., by the same author" -- internal, but it hints at a single-author project; drop it.
- Source comments (13_verify.tex:1) mention a "named build" with the repository URL; do not upload source files with the review PDFs.
- Nothing in either PDF names a person, institution or home path (I searched for these strings).

---

## 7. Comparison with the previous mock review (delegate/out/tog_review2/REPORT.md)

Review 2 (2026-11-22) had five blockers (B1-B5) and twelve should-fix items (S1-S12). I checked each one against the current source.

**Fixed**
- B1 (the conclusion mixed the 8×8 accuracy with the six-rank sweep; "⋆2 appears with seven pawns" was false for rings). 14_conclusion.tex now separates the two: 92.5% of 2,049 decisive 8×8 positions, and the square-rule repair "on six ranks". It also says "on four files of the ordinary board". Fixed.
- B3 (AI authorship of the proofs not in the acknowledgment). The acknowledgment now says the assistants "wrote the full proofs of Sections S12-S15". Fixed.
- B4 (S10 contradicted the Möbius results). supp/s10.tex:16-17 now matches. Fixed.
- B5 (S6.4 overstated the n = 6 Möbius check). supp/s06.tex:135 now says "below the least, and at the least ...", and "two programs by one AI model" replaces "by one author". Fixed.
- S1/S2 (the AI-referee sentence and the label definition). Both now say the proofs are AI-written and AI-refereed, and "independent" is gone. Fixed as wording. My M3 argues that the underlying problem remains.
- S3 (the 92.5% denominator), S5 (HSS "in outcome" and "default setting"), S6 (Möbius labels; ⋆3 on five and six files) and S8 (FEN spelled out): all taken. Fixed.
- S12 (no supplement entry for the sum checks). S3 now has "Two Checks of the Sum Model". Fixed.

**Partly fixed**
- S4 (real-kings paragraph). "Queen promotions only" was added. Two things remain: the selection ("components the model gets right alone") is still not stated, and the new wording "every second-player win among them, we have only bounds, and each contains it" is still hard to parse (my Section 5, item 6).
- Weak point 2 of review 2 (a thin, convenience-sample bridge to real chess). The denominator is now explicit, but the conclusion still gives the 92.5% without saying the positions are tablebase-sized and were solved for other sections (my M6). The 52/233 model-tablebase disagreement in the engine suite is still not discussed.

**Remaining**
- B2 (the code link is a placeholder). Still "anonymized repository link" in both PDFs. Not fixed (my M7).
- S7 (Wikipedia cited). [14] WikiCylinder is still cited at 10_tablebases.tex:7. Not fixed.
- Weak point 1 of review 2 (⟨S⟩ rests on AI-only refereeing, some within one model family). It is now disclosed, but the substance is unchanged: no human, apparently including the authors, has checked the proofs, and the single label hides the three tiers of checking (my M3).
- Weak point 3 of review 2 (readability and too many topics in 10 pages). Unchanged (my M4, M5).

**New in this review (not raised by review 2)**
- M1: hypotheses that appear only in the supplement (at least five ranks, a local race rule, last-rank pawns, per-side-to-move validity); ⟨S⟩ hiding computer-assisted proofs (S13/S14 are "proved modulo C1"); the double meaning of "W(X) is a ⋆k".
- M2: (V2) and (V3) assume the chess result, so "conditions under which frozen kings are exact" overclaims.
- M4: Table I and the Dawson "correction" concern an unpublished, unavailable manuscript.
- M5: notation clashes (S, B, W, X, Tiny 1); internal notes typeset unchanged with dangling references to sections not reproduced.
- M6: "real-chess oracle value" naming; the engine-pilot claim carries a C1 label.
- Anonymity: "cylcgt" (43 times) and repository paths in the supplement may let a reviewer find the project if the repository is public.
- Related work: no comparison with Mäser [11] for sum safety, and Müller (IJCAI 1999) is missing for engines on sums. Review 2 also treated the seven-pawn ⋆2 as a clean answer "open since Elkies". I would make that conditional on a precise statement of what [5] and [6] show for 8×8.
