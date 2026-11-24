# T90 referee report on Section S13

## Verdict in five lines

- **PROVED given C1 and C2 — sound with wording fixes.** The O/E induction covers every width from 5. Both fixed cuts satisfy the repaired hypotheses.
- **PROVED.** Flag transport and commutation work on the stated insertion domain. Step (iii) establishes equivalence of *immediate terminal-winning* replies. Two sentences still omit that qualification.
- **PROVED.** The heap outcome is P exactly at 2 for every finite nonnegative heap, including the stated range below 256. Replacing each resolved child by its winner’s signed integer gives ordinary CGT equality to ★2.
- **CHECKED-2.** The archived independent searches agree at every claimed O/E width. A fresh verifier rebuild reproduced both base graphs’ counts, zones and signatures. The text misnames the programs that solve the reduced graphs.
- **PROVED.** All the cited notes’ actual induction cuts use consecutive files in a single alternating wall. Some generic restatements omit hypotheses. Specify an alternating subarc explicitly and qualify the separate F-family node counts by width.

## Disposition of T89 findings 1–12

References are to the supplied 222-line `research/ring_family_proof/proof.tex`. Quotations use rendered mathematical notation. “Retain” means that the quoted sentence can stand. The numbered reviews below give exact replacement text wherever a change is needed. Proof labels on the mathematical findings refer to the deductions under the printed model. The finite evidence is identified separately.

| T89 | New sentence and location | Disposition |
|---|---|---|
| 1 | 61, “Let g be a non-terminal position, h≥0, and let either side move first.” | **PROVED, resolved.** The recursion at 64–70 compares each starter’s outcome. Retain. |
| 2 | 84–85, “No enemy pawn moves, and the old flag, if any, protected an enemy pawn; so no other pawn of Z becomes passed.” | **PROVED, resolved.** The preceding enumeration excludes both kinds of capture. Retain. |
| 3 | 87, “Choose s∈{1,−1} such that j−s,j,j+s,j+2s,j+3s are pattern files.” | **PROVED, resolved.** Lines 88–93 use that same side for the capture and the surviving blocker. The table and example agree. Retain with the subarc convention below. |
| 4 | 100–101, “The new files continue the alternation, so they are pattern files of the lengthened wall.” | **PROVED, resolved.** Lines 98–100 keep the flag on the old victim and exclude a victim on either cut file. Facts (V) and (C) suffice for all children on which insertion is used. |
| 5 | 132–133, “By (V), ν wins for Y iff ν̂ does.” | **PROVED for terminal wins, partly resolved in print.** The new far-reply argument supplies the missing implication. “Wins” at 129 and 133 still invites the stronger reading identified in T89. Use the two replacements in finding 5 below. |
| 6 | 161, “Also 4≤c≤n−6.” 164–165, “Thus ins_c is an isomorphism of the reduced games: nodes, side-labelled K-edges and, for each side, the existence of a T-move.” | **PROVED given C1, resolved.** Both path directions, the root and the shifted zone are accounted for. Retain. |
| 7 | 180, “As Ĝₙ+★2 is a P-position, Ĝₙ=★2 in normal-play CGT.” | **PROVED given C1 and C2, resolved in substance.** Lines 170–182 establish both interpretations. Align the quantifiers at 56–57 and 177. |
| 8 | 145–147, “The P-outcome at heap 2 was obtained by solving this graph (rg.c, eng.py), by the canonical value ★2 of the cylcgt-built reduced game in cylcgt’s CGT arithmetic, and, without reduction, by C2 at n₀.” | **CHECKED-2, numerical claim resolved, attribution partly resolved.** Both named engines supply rules or nodes. The reduced recursions are in two other files. |
| 9 | 150–151, “In addition, the canonical value of the whole board Gₙ, computed with cylcgt, is ★2 for 5≤n≤10.” | **CHECKED-2 for C2, resolved.** The two unreduced searches at 148–150 cover their full parity ranges. This additional canonical calculation is **COMPUTED-1** as a direct library route. |
| 10 | 26, “Every pawn move removes the old flag (and may record a new one); a heap move leaves the board and the flag unchanged.” | **PROVED by rule comparison, resolved.** The distance, front-pawn test and tie break are supplied at 29–32. The family, exact file content and flag-free roots are defined at 45–53. Clarify “of one wall” for the general lemmas. |
| 11 | 191–192, “This says nothing about play after an L- or P-move, or after a T-move.” | **PROVED, resolved** for reduced positions at and above the bases. Lines 214–216 correctly call radius 5 sufficient and describe the shorter-radius evidence as a sample (**COMPUTED-1**). |
| 12 | 220, “The analogues of C1 and C2 were computed for it (C2 by the same two searches for n=5 and 7≤n≤61).” | **PROVED conditionally, substantially resolved.** The two words, cuts, zones and exceptional missing width are now specified. Qualify the node counts at 218–219 and say which F base facts are required. |

## Mathematical findings and line-by-line decisions

**1. Model, lines 21–42 — sound (PROVED by comparison with the rules and sources).** “A pawn move to a terminal position ends the game, won by the winner of that position whoever would move next.” Retain. A canonical flag identifies the victim and the side entitled to capture. A heap move switches the mover and retains that entire board state. In particular, having the move does not itself confer the capture right. For example, if the holder lowers the heap, the victim’s owner now has the move while the opponent still holds the right. A pawn move consumes the flag. Strictly-ahead enemies on three files decide blocking; a flagged victim is excluded from the passed set. Having any passer triggers adjudication, while only front, passed pawns enter the race minimum. The home-rank correction is one step. Equal minima, including two empty minima, favour the opponent of the last **pawn** mover. The programs’ empty-minimum sentinel exceeds every finite distance. Sources and commands are in A below. The raw library records even inert double-step flags. Its eligibility test and the graph builder’s normalization give the printed canonical semantics.

**2. Lemma 1, lines 60–70 — sound (PROVED).** “So X has a winning option in one game iff in the other.” Retain. At 61 g is unresolved. At 64–66 every board move advances the mover and removes a nonnegative amount of remaining distance on capture. A heap move strictly reduces the other summand of the induction measure. At 67–68 T wins immediately, L loses immediately and P gives the opponent a legal immediate win at every heap size. At 68–70 the K-successor is in the graph by construction, and a heap move leaves the entire node fixed. The induction hypothesis applies to the opponent in each case, including positions with a flag. If every full-game move loses and pruning leaves no move, the reduced starter loses by normal play. No comparison of follower *values* is needed.

**3. Lemma 2, lines 73–95 and 194–209 — sound on an alternating window (PROVED).** “So Y alone has a passed pawn, the reply wins for Y, and the move is P.” Retain. At 81–83 the only enemy on either neighbouring file is two ranks ahead. Both diagonal targets are empty and there is no abreast e.p. victim. The five listed pushes exhaust both wall types. At 84–86 the single step leaves an enemy ahead. The only double step leaves the white pawn e.p.-capturable by B4. All other mover pawns keep their blockers, and expiration of an enemy victim’s flag cannot make a mover pawn passed. At 87–89 choose the orientation *before* selecting the capturer. Part (a) gives the L branch if Y already has a passer. Otherwise the capture from j+s is legal, onto the skipped square after the double step. At 89–93 the capturer has three files clear of X. Its departure can release a surviving X pawn only on j+2s. The enemy on j+3s is still strictly ahead there. The expired flag belonged to the captured pawn. This proves sole passage, stronger than winning a count race. Lines 195–204 correctly restrict the table to the live branch. In the example at 207–209, capturing from file 5 leaves Black without a passer. Capturing from 7 frees the B5 on 8; both distances are four, and Black wins the tie. See D.

**Scope of “one wall”, lines 49–53, 75, 77, 98 and 112 (PROVED).** “On a pattern file, each neighbouring pattern file holds a single enemy pawn two ranks further on in the direction of the file’s own pawn.” This is the intended local alternation. For general positions, membership in a set of files alone does not imply it across the join of a run’s endpoints. On five files take the linear run W3,B5,W3,B5,W3, flag-free. If the two ends of this run on the cylinder may be joined merely because both belong to it, the window 4,0,1,2,3 qualifies by membership. W3–4 on file 0 is K. Neither side then has a passer. Black can push on file 1 or 3, or capture from 1 onto 0. In every case Black still lacks a passer (after the capture W3 on file 4 blocks B4 on file 0). This is a counterexample to the membership reading, not to a lemma about an alternating subarc. It does not occur in O/E or any of the stated induction cuts. **Replace 52–53 after “wall pawn” by** “An interval of pattern files of one wall means a consecutive subarc of that wall, with the prescribed alternation along every edge of the interval. Each neighbouring pawn within the subarc is an enemy two ranks ahead in the direction of the first pawn.” Use this convention also for the pair c,c+1. It permits a genuinely alternating arc across the file-number seam.

**4. Insertion and Lemma 3(i)–(ii), lines 98–125 — sound (PROVED).** “If a pawn move ν in q changes no square on files c,c+1, the image pawn has the corresponding move ν̂ in ins_c(q), and ins_c(qν)=ins_c(q)ν̂.” Retain.

- **98–106, definition and (V).** Old files strictly right of the cut shift by two. Only originals c and c+1 exchange an old neighbour for a copy of equal content. The victim is on neither boundary file, so its adjacent files are the images of its old adjacent files, even at the cylindrical seam. Its rank, potential capturers, skipped square and holder agree. A copy receives no flag. Thus an old pawn sees the same local move choices and the same blockers, and a new pawn is blocked. For the same last mover the old front-pawn test, rank distances and tie break all agree. This proves terminal-winner equivalence. (V) does not claim that making every possible move commutes with insertion.
- **107–109, (C).** Source, destination and any e.p. victim avoid the two cut files. Their incidences persist, the contents being copied are unchanged in the child, and any new flag is on the original double-step file. Its adjacent potential capturers correspond. This proves the identity including the child flag. An old flag may disappear even though its pawn was never moved.
- **111–120, hypotheses and (i).** The bounds make the ten old files distinct and nonwrapping in the chosen representatives. The image has twelve consecutive pattern files. The two five-file windows cover every old origin c−3 through c+4 and every new origin c−3 through c+6. Both parents have no passer or flag. Lemma 2(b) excludes K and T throughout, including moves by copies.
- **121–125, (ii).** Outside these central ranges every pawn on either board has a unique mate. A move from the old exterior can change neither c−2 through c+3 nor their copied interior. A capture across the file-number seam stays in the exterior union. A double step places any new flag on its exterior origin. Apply (C) to the move and (V) to its child with last mover X. The three possibilities T, L and unresolved correspond in both directions.

**5. Lemma 3(iii), lines 126–135 — sound for terminal replies, gap if “wins” means eventual victory (PROVED).** At 126–129 a non-terminal child retains the six-file old subarc and the eight-file new subarc. Every near origin has an exact alternating triple. Any flag is on X’s pawn, as Lemma 2(a) requires when Y replies. At 130–132 the remaining origins correspond. A far reply may change c−1 or c+2 but avoids c,c+1. A capture e.p. of X’s far double-stepper also avoids the cut. Thus (C) applies to this *second* move from a possibly flagged child. At 132–135, (V) compares terminal results for last mover Y. It follows that there exists a T reply on one board iff one exists on the other. This is exactly the test for P. The unresolved, unpoisoned moves are K, with the stated image children. No recursive comparison after the reply is required.

- 129, “so the reply does not win for Y”; **replace by** “so the reply does not reach a terminal position won by Y”.
- 132–133, “By (V), ν wins for Y iff ν̂ does.” **Replace by** “By (V), ν reaches a terminal position won by Y if and only if ν̂ does.”

**6. Root and induction, lines 154–169 — sound (PROVED given C1 and C2).** “Also 4≤c≤n−6. So Lemma 3 applies to every node.” Retain. At 155–158 the mixed files block their own pawns, the isolated core B5 has a neighbouring white blocker, and the alternating wall supplies blockers at both ends in each family. Insertion adds one period to the root and preserves the empty flag. At 159–161 K-reachability excludes resolved children. In the odd base the required interval [5,14] lies in the fixed files [5,15], and 4≤9≤11. In the even base [4,13] lies in [4,14], and 4≤8≤10. Both inequalities loosen as n grows. At 162–164 deleting the copies recovers an old node and its flag. Lifting K-paths from the old root gives inclusion, and lifting *backwards along the image correspondence* at each step of a path from the new root gives the reverse inclusion. At 165–166 the side and existence of T are preserved and the last zone file advances by two. These facts re-establish the invariant on **all** new nodes. At 167–169 the finite recursion depends only on that labelled graph and the heap. C1 gives P at heap 2, Lemma 1 transfers it, and C2 covers the odd widths 5–15 and even widths 6–14 by twos. No observed equality of graph sizes is used as an induction step.

**7. Theorem and equality, lines 55–57, 170–182 — sound, with two justified stronger statements (PROVED given C1 and C2).** “The theorem gives the outcome of Gₙ+★h for every heap; the proof uses no bound on h.” In the immediate-adjudication model both starters lose at heap 2. Each starter can lower that heap to 0 or 1, so the *other* player wins from each of those children. Applying this to both starters gives N. From any finite h>2 either starter can hand over the P-position. This proves more than the displayed numerical range. Separately, assign the signed integer to each *incoming terminal move*, so opposite last movers in a tied race may produce different options even on the same final diagram. A positive integer plus a nonempty heap is a Left win as either starter: Left can empty the heap, and every Right move only decreases the heap. At an empty heap the positive integer already wins. Reverse the colours for a negative integer. Recursion at unresolved nodes now identifies the operational outcome with that of the ordinary sum. Since −★2=★2 and a short normal-play game is zero iff it is P, the P result tests the exact difference Ĝₙ−★2. Thus Ĝₙ can be substituted for ★2 against arbitrary **ordinary disjunctive addends**. No result about a compound adjudicated at its first passer, default component splitting, another race rule, or real chess follows.

**Replace 56–57 by** “For every n≥5 and integer h≥0, Gₙ+★h is P for h=2 and N otherwise. In particular the outcomes agree with those of ★2+★h throughout 0≤h<256.” **Replace the first sentence of 177 by** “For the corresponding equality in ordinary normal-play CGT, use the following representation.” A journal wishing to retain the bounded theorem can instead replace only 57 by “Thus the two games agree against every nim-heap in the stated range” and the first sentence of 177 by “The same argument proves the outcome formula for all finite h≥0.”

**8. Separate F remark, lines 217–221 — sound transfer, width qualification needed (PROVED given the F finite premises).** “Its reduced games have 662 nodes (even n, n₀=18, cut c=4, zone …) and 3568 nodes (odd n, n₀=19, cut c=6, zone …).” Read over every just-defined F width, this is false: the reduced-value log reports 372 nodes for F₅ (**COMPUTED-1**, B below). At the even base the arc [0,9] is in the alternating prefix [0,11] and avoids the zone [11,15]. At the odd base [2,11] lies in the prefix [0,13] and avoids {0,1,13,…,17}. Both cuts satisfy 4≤c≤n−6. The same insertion fixes the low zone files and shifts the high ones. The F sweeps cover 5 and 7–61, omitting the undefined width 6. The independent F verifier also records the two base sizes and outgoing insertion checks. **Replace from “Its reduced games” through 221 by** “At the flag-free even base F₁₈ the reduced graph has 662 nodes and zone {n−7,…,n−3}; at the flag-free odd base F₁₉ it has 3568 nodes and zone {0,1,n−6,…,n−2}. Both give P at heap 2. The cuts 4 and 6 use the respective unchanged prefix intervals [0,9] and [2,11]. Insertion extends that prefix by one period and carries each zone to the next. The preceding induction therefore gives these node counts from the respective bases onward. The two unreduced searches also give NNPN at 5 and at every width from 7 through 61, covering all defined smaller cases.” This uses only the required analogues of the finite premises. The archived reduced canonical F calculation does not run through the F induction bases.

## Computational findings

**9. C1, lines 141–147 — counts and graph comparison match; correct the solver attribution (CHECKED-2).** “The graph (nodes and, for each side, the K-children and the existence of a T-move) was built by rg.c (C) and, identically, by a second builder that uses the move generator, passed-pawn test and race rule of the library cylcgt.” Retain. The second builder is `reduced_cyl.py`. It compares actual sets of pawn positions and (source, side, target) triples. T is one target per side at a source. The same rule does not merge separate K-successors. Nodes exclude the heap and terminal sinks and allow K-edges of either side in any order.

| Base | Nodes | K-edges | T-moves before collapsing | Distinct K/T triples | Files differing somewhere | Flagged nodes | Outcome at 2 |
|---|---:|---:|---:|---:|---|---:|---|
| O₁₇ | 144 | 209 | 246 | 308 | 16,0,1,2,3,4 | 0 | P |
| E₁₆ | 104 | 177 | 97 | 231 | 15,0,1,2,3 | 0 | P |

The C/library graph comparisons cover odd 5–23 and even 6–22 by twos. The canonical *reduced* library runs cover odd 5–25 and even 6–26. The pump logs give counts and reduced outcomes, and the fresh `verify/red.py` rebuild and `verify/zonecmp.py` run give the same base statistics and the same two published sets of zone states. **Replace the last sentence of C1 (145–147, quoted in T89 row 8) by** “At both bases, graph.py solves the graph emitted by rg.c reduce, and verify/red.py independently builds and solves the graph using verify/eng.py for the pawn rules. Each gives P at heap 2. The canonical computation in reduced_value.py gives ★2 for the cylcgt-built reduced game, and the unreduced searches of C2 also give P at both bases.” The C executable’s `solve` mode and the Python engine’s `Solver.win` are the **unreduced** searches.

**10. C2, lines 148–151 — coverage and independence match (CHECKED-2).** “Neither search uses the reduced game or Lemmas 1–3.” Retain. The C sweep tests 29 odd widths 5–61 and 28 even widths 6–60. Each per-width Python verifier record gives NNPN, with exactly the same width sets. Both searches generate legal moves, score terminal children, and try unresolved children and heap options for each starter. Stopping once a winning move is found requires no wall lemma. The separate whole-board canonical computation disables splitting and gives ★2 at odd 5,7,9 and even 6,8,10 (**COMPUTED-1** for that route). It supplies no direct canonical computation at 11–16. **Replace** “for each side moving first” (150) **by** “where N means either starter wins and P means either starter loses”. **Replace** “The proof uses only the widths n<n₀” (151) **by** “The theorem uses C2 to cover the widths below the respective bases; C1 supplies both induction bases.” C1 also cites C2 at the bases as corroboration.

## Consistency with the five cited notes

**11. Actual applications — sound (PROVED from the stated family words and invariants, conditional on each note’s own base checks).** At every induction root the no-passer condition needed by Lemma 1 is established. For each old-board cut the table gives the single uninterrupted patterned interval and the base value of the upper bound n−6. The integer bounds persist at all subsequent induction widths. The notes’ smaller directly solved widths and their off-hypothesis control cuts are not proof steps.

| Note and lines | Family, base, cut | Interval | Base upper bound | Decision |
|---|---|---|---:|---|
| S15 Note 1, 48, 52–54, 75–89, 104–106 | P, 18, 12 | 8–17 | 12 | Equality in the cut bound is allowed. Ending at the last file is allowed. |
| S14, 34–37, 43–46, 52–64, 76 | M, 18, 4 / O, 19, 5 | 0–9 / 1–10 | 12 / 13 | M uses one E wall. For O, colour swap with rank reflection r↦9−r carries B7/W5 to W2/B4, including the home double step, holder and count tie break. Apply the full local result in the transformed position and carry it back. |
| S15 Note 2, 36–50, 59 | Q, 22, 9 | 5–14 | 16 | Both boundary windows in H2 are in the same E wall. The proof calls Lemma 1 on the unresolved root. |
| S15 Note 3, 36–55, 70 | R and Qo, 19, 6 | 2–11 | 13 | The leftmost file of the wall is used as a neighbour. The five-file windows are consecutive in that wall. |
| S15 Note 4, 34–44, 50–62, 76 | T, 20, 4 / S, 23, 7 | 0–9 / 3–12 | 14 / 17 | The T arc is the whole designated wall at the base. The S arc avoids the changeable end of its wall. |

**12. Restatements and qualifications (PROVED by comparison).** These are textual changes to the cited notes, not changes required to their chosen cuts.

- **S15 Note 1, 52–54.** The three statements already include “non-terminal”, the flag ownership restriction, “of one wall” and 4≤c≤n−6. Retain. At **59–61** the raw copy operation and (V1), a fact about occupancy, are described for “any position”. S13 now defines its named insertion only for a consecutive pattern pair and a victim off that pair. **Replace the first sentence of 61 by** “For the S13 insertion suppose that 0≤c≤n−2, that c,c+1 form a consecutive pattern pair of one wall and that neither carries the flagged pawn. The occupancy assertion (V1) also holds for the unrestricted file-copy operation.” Add after V1, “Since the victim is off the cut pair, the image of each prospective e.p. capturer remains beside its victim.” A copied occupancy alone cannot justify unrestricted correspondence of e.p. moves. For instance, after W2–4 on old c beside B4 on old c+1, unrestricted copying puts the **copy** of B4 beside the flagged original while moving the original B4 away. In **63–71** the parents are flag-free, any first-move flag is far, and far replies leave the cut pair unchanged. The near-reply sentence at 67 already says “not terminal-won by Y”. Its proof of (ii)–(iii) therefore applies as written to this family. At **73** read “only role of the cut” subject to the numeric bounds. At **78** replace “j−3..j+3” by “one of j−1..j+3 and j−3..j+1”. Those are alternative windows. At **91** describe h<256 as the displayed theorem’s range. At **56, 109–110** replace editorial claims that the reply proof or exact pattern definition still needs repair in S13 by “Section 2b gives the local proof in the coordinates of Pₙ.”
- **S14, 37.** The shorthand “a side wins G+★h moving first iff it wins the reduced game moving first” omits the domain. **Replace the line by** “Use Lemmas 1–3 as stated in S13. Lemma 1 starts at a non-terminal board. The triple and the alternative five-file window of Lemma 2 must be consecutive in one wall, with the flag conditions of parts (a) and (b). In Lemma 3 the parent is non-terminal and flag-free, 4≤c≤n−6, and c−4,…,c+5 is a consecutive pattern interval of one wall. For each side the K-child sets correspond and the T-existence indicators agree.” Lines **45–46, 52, 60, 64** discharge the conditions.
- **S15 Note 2, 20, 38–40.** “Use the reduction and wall-pawn lemmas as stated in Section S13” imports the hypotheses. No substantive change is needed. For a self-contained summary, append to line 40 “Here 4≤9≤n−6 for n≥22 and the interval lies in the single periodic Q wall.” At **20**, the proof of (ii)–(iii) is now in *both* sources. At **31**, “shortest promotion distances” can refer explicitly to “the front passed pawns eligible under the count rule of S13”. At **38**, “the adjacent opposite-colour wall pawn” can be made precise as “the adjacent enemy on the side extending two further pattern files”.
- **S15 Note 3, 39.** This is the most consequential stale restatement. Lemma 1 lacks the non-terminal premise. Lemma 2(a) lacks both the no-passer premise and the restriction on whose pawn may be flagged. Without the former, an unrelated existing passer can simply persist. The symbol c in “if c has no flag” denotes the position here but denotes the cut in Lemma 3. Lemma 3 omits the cut bound and common wall. **Replace the line by** “Use Lemmas 1–3 in the form stated in S15 Note 1, lines 52–54. In Lemma 2 let p be non-terminal and let any e.p. flag mark an opponent’s pawn; part (b) further requires p to be flag-free. Each stated window is a consecutive pattern interval of one wall. The Lemma 3 cut is c=6, with 4≤c≤n−6 throughout the induction.” At **5** replace “neither end enters the lemmas” by “no central origin is a wall endpoint; a window may use the first wall file as a neighbour”. At **42** replace “By C1” for all n≥19 by “At the base by C1, and at the induction step by the assumed invariant”. Lines **49, 51, 55, 70** supply the actual windows and non-terminal boards.
- **S15 Note 4, 41–44, 50–62.** No missing hypothesis in the application. At **54** make the two coordinate ranges explicit if this paragraph is used as a restatement. **Replace** “For j≤c+2 …” through “(Iₙ, H6)” **by** “On the source central range use the right window for j≤c+2 and the left window otherwise. On the image central range the right window fits through j=c+4, and the left window fits thereafter. Each chosen window lies in the same alternating wall.” At **81** refer to S13 lines 126–135 as well as Note 1 §2b.
- **Control cuts in S15 Note 1, 88, 101, 119; S14, 48, 70–71; S15 Note 3, 42, 64, 78; S15 Note 4, 46, 70–71.** Preserve the empirical comparisons. Wherever a control can copy a non-pattern pair, call the operation the “unrestricted file-copy map”. Wherever only the surrounding ten-file hypothesis fails, call it “a test of the conclusion outside the sufficient hypotheses”. Examples are c=5 in Note 1 (file 5 is core), c=10 at S14’s O₁₉ (11 lies beyond the designated wall), and c=9 at Note 4’s T₂₀ (10 is core). Replace “Lemma 3 fails” in these descriptions by “the tested correspondence fails at this control cut”. None is a counterexample to S13.
- **Race and scope shorthand.** S15 Note 1 **25, 83** and S15 Note 3 **53** say any function of the passed pawns and last mover works. For an arbitrary such function, absolute file labels or the circumference could matter. Use “any race rule invariant under this file embedding and determined by preserved data, including the front-pawn information and last mover needed for count”. The named count/mover/opponent rules satisfy that locality. S14 **66** and S15 Note 4 **64** already explain signed-integer equality. The narrower heap-only conclusions in S15 Notes 1 **12, 91**, 2 **12, 51** and 3 **11, 57** can stand. If attributing h<256 to S13, call it the range *stated in the theorem*; the operational recursion and the signed-integer comparison also work above that range.

## Other wording for the published text

**13. Definitions and notation (PROVED by inspection).**

| Lines | Printed wording | Exact replacement or insertion |
|---|---|---|
| 30–33, 55–57 | “the least value of 8−r−[r=2] …”; “G+★h” | After the distance formula insert “Here [A] is 1 if A holds and 0 otherwise.” At the first heap reference insert “Write ★h for the nim-heap of integer size h≥0; a heap move replaces h by any smaller nonnegative integer.” Before the theorem insert “In a P-position either starter loses; in an N-position either starter wins.” |
| 32 | “the side that did not make the last move” | “the opponent of the player who made the terminal pawn move”. |
| 74–75, 87 | “protecting a pawn”; “By (a) X=Z has no passed pawn after the move. If Y …” | Use “marking an e.p.-capturable pawn” for flag ownership. At the start of (b) insert “Write X=Z and let Y be the other side.” X and Y were defined in the earlier move classification but have not been bound locally in this proof. |
| 98–109, 121–135 | “the same three files and the same flag status: the same moves and the same status”; “qν” | Use “the same three-file contents and e.p. eligibility, hence the same legal move directions and passed status.” Before (C) insert “Write qν for the child of q after ν and ν̂ for the corresponding move by the image pawn.” At 130–131 add “in old-board coordinates” after “starts on a file”. |
| 170 | “every option loses” | “every move by either starter hands the opponent a win” (retain the examples that follow). |
| 176, 186–192 | “What is and is not proved”; “one of the zone states listed in the code repository”; “Zₙ holds … the wall pawns next to them” | Use “Scope and ordinary game value”. At 189 identify “the base zone states listed in zone_states_odd.txt and zone_states_even.txt, in the displayed cyclic order”. At 190 use “At the root the zone contains …”. Pawns in the zone may move on a K-path. |
| 194–196, 207 | “The five poisoned wall moves”; “Example for the side” | “Wall advances and their replies”; “Why the side of capture matters”. An advance classified L is resolved before a poisoning reply. |
| 212–213 | “a decisive passer in one component can be cancelled by a −256 option in another” | “A resolved White win contributes +256 in a disjunctive sum; a resolved Black win in a second component contributes −256. Their sum is zero.” The signed value and an available option to that value are different objects. |
| 217–221 | “This transfer has not been written out in full.” | Use the F replacement in finding 8, which gives the induction step and its premises directly. |

The wrapper’s source comments at 1–4 are not printed. The proof’s P label denotes proof status, P-move means poisoned, P-position is an outcome, and the label [C2] also appears beside the premise named C2. If the surrounding supplement has no label key, print “PROVED” and “CHECKED-2” in the status tags and retain C1/C2 as the premise names.

## Reproduction and limits

Run from the project root in zsh. All commands below are read-only on project artifacts. Cited numbers in family definitions, cut bounds and note intervals follow by substitution in the cited lines; the archive commands retrieve the finite observations. In the fresh checks the Python interpreter ran with bytecode writes disabled.

```sh
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
P=.venv/bin/python
D=research/ring_family_proof
S=dist/tog/supp_src
```

**A. Printed hypotheses, model implementations and program roles (PROVED by inspection).**

```sh
nl -ba "$D/proof.tex"
nl -ba "$D/rg.c" | sed -n '35,41p;86,195p;260,333p'
nl -ba "$D/verify/eng.py" | sed -n '29,192p;194,225p'
nl -ba cylcgt/pawns.py | sed -n '39,67p;118,176p;220,249p'
cat "$D"/{reduced_cyl,reduced_value,cyl_whole,graph,pump_verify,fullsweep}.py
rg -A12 '^def norm_ep' "$D/difftest.py"
for note in s14_ringn s15_note1 s15_note2 s15_note3 s15_note4; do nl -ba "$S/$note.md"; done
```

**B. Finite evidence.** The first three commands are the fresh independent-base rebuild and exact zone-set comparisons. The subsequent commands reproduce the archive comparisons, F exception, radius observations and width coverage.

```sh
"$P" -B "$D/verify/red.py" O 17
"$P" -B "$D/verify/red.py" E 16
"$P" -B "$D/verify/zonecmp.py"
cat "$D"/logs/{pump_odd_c9,pump_even_c8,reduced_cyl_odd,reduced_cyl_even,reduced_value}.log
cat "$D"/logs/{fullsweep,cyl_whole_odd,cyl_whole_even}.log
cat "$D"/logs/{pump_Feven_c4,pump_Fodd_c6}.log "$D/verify/F_pump_l3.txt"
cat "$D"/logs/{lemmaL_sensitivity,lemmaL_odd,lemmaL_even,lemmaL_F}.log
rg 'MUTATE|lemmaL_test.py' "$D/run_all.sh"
"$P" -B - <<'PY'
from pathlib import Path
d = Path('research/ring_family_proof/verify')
for files, expected in [(('O',), range(5,62,2)), (('E',), range(6,61,2)),
                        (('F','F2'), [5,*range(7,62)])]:
    rows = [s.split() for f in files for s in (d/f'sweep_{f}.txt').read_text().splitlines() if s.strip()]
    assert [int(r[1]) for r in rows] == list(expected)
    assert all(r[5] == 'NNPN' for r in rows)
    print(files, len(rows), 'complete, all NNPN')
PY
```

**C. Original numerical routes.** These invocation examples regenerate the O/E base results and the two O/E unreduced sweeps. The archive in B suffices for checking the slower library and F runs. The last two commands regenerate the direct canonical values and can be slow. Run separately if reproducing them.

```sh
"$P" -B "$D/graph.py" odd 17
"$P" -B "$D/graph.py" even 16
"$P" -B "$D/reduced_cyl.py" odd 17
"$P" -B "$D/reduced_cyl.py" even 16
"$P" -B "$D/reduced_value.py" odd 17
"$P" -B "$D/reduced_value.py" even 16
"$P" -B "$D/reduced_value.py" F 5
"$P" -B "$D/fullsweep.py" 61
"$P" -B "$D/verify/eng.py" O {5..61..2}
"$P" -B "$D/verify/eng.py" E {6..60..2}
"$P" -B "$D/cyl_whole.py" odd 5 7 9
"$P" -B "$D/cyl_whole.py" even 6 8 10
```

**D. Local examples and all induction cuts (PROVED by the arguments above; executable checks).**

```sh
"$P" -B - <<'PY'
import sys
sys.path.insert(0, 'research/ring_family_proof/verify')
from eng import classify_moves, moves, parse, prom_dist, status
p = parse('W3 B5 W3 B5 W3'.split())
assert status(p, None, 'B') is None
assert [k for k,q,e in classify_moves(p,None,'W') if q[0] == (8,0)] == ['K']
p = parse('- - - W3 B5 W3 B5 W3 B5 - -'.split())
q,e = next((q,e) for q,e in moves(p,None,'B') if q[6] == (0,8))
assert status(q,e,'B') is None
wins = {}
for t,f in moves(q,e,'W'):
    if t[6] == (8,0):
        origin = next(j for j in (5,7) if not t[j][0])
        wins[origin] = status(t,f,'W')
        if origin == 7:
            assert prom_dist(t,f,'W') == prom_dist(t,f,'B') == 4
assert wins == {5:'W',7:'B'}
# Far double step, surviving flag, then a far e.p. reply across the seam.
# Reflect the board to put the old victim on each side of the insertion.
from pump import insn
word = ['W2'] + ['W2','B4']*5 + ['W2B4']
for toks, victim, taker in [(word,0,11), (word[::-1],11,0)]:
    p = parse(toks)
    assert status(p,None,'B') is None
    q,e = next((q,e) for q,e in moves(p,None,'W') if e == (victim,'W'))
    a,ae = insn((p,None),5)
    b,be = insn((q,e),5)
    assert (b,be) in moves(a,ae,'W') and be == (victim if victim == 0 else 13,'W')
    assert status(q,e,'W') is None and status(b,be,'W') is None
    r,f = next((r,f) for r,f in moves(q,e,'B') if r[victim] == (0,4) and r[taker] == (2,0))
    t,g = insn((r,f),5)
    assert (t,g) in moves(b,be,'B') and f is g is None
    assert status(r,f,'B') == status(t,g,'B')
# (base, cut, first and last guaranteed pattern file at the base)
for n,c,a,b in [(17,9,5,15),(16,8,4,14),(18,4,0,9),(19,6,2,11),
                (18,12,7,17),(18,4,0,9),(19,5,1,10),(22,9,4,14),
                (19,6,2,11),(20,4,0,9),(23,7,3,12)]:
    assert 4 <= c <= n-6 and a <= c-4 <= c+5 <= b
PY
```

**Limits.** I reviewed the supplied TeX source, T89, the named notes, the relevant source routines and the saved records. I reran the verifier at the two O/E bases, the zone comparison, the sweep-coverage check and the local examples. The large sweeps, canonical values, F bases and random samples are attributed to their archives. I did not rebuild the journal PDF, re-audit the independent finite computations for S14/S15, formally verify the engines, test real chess or establish a component-sum theorem. The sandbox denied the requested niceness adjustment; fresh checks were short and sequential. No network or version-control command was used.
