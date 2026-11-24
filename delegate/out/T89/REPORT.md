# T89 referee report on Section S13

## Verdict in five lines

- **Holds with fixes — PROVED given C1 and C2.** The odd and even wall rings have the stated whole-board outcome against nim-heaps at every width from 5 onward.
- **PROVED.** Reduction preserves the winner for each starting side. The wall lemma needs the capture on the side of the five-file window. The printed direction can lose a tied race.
- **PROVED.** Insertion preserves the side-labelled kept children and the availability of an immediate win. A separate argument for the opponent's replies closes the gap in line 75.
- **CHECKED-2.** The base graphs have 144 and 104 pawn positions. Two archived unreduced engines cover every width from 5 to 16. A fresh third search gives NNPN at every width from 5 through 17.
- **PROVED.** P at heap 2 gives the full heap signature. It also gives ordinary CGT equality under the explicit signed-integer, disjunctive-sum interpretation. Neither argument transfers the theorem to component splitting.

## Mathematical findings

Line numbers refer to the current `research/ring_family_proof/proof.tex`. **PROVED** below denotes a deduction from the stated rules, conditional on a finite premise where cited. **CHECKED-2** denotes agreement of independent implementations. **COMPUTED-1** identifies observations from one implementation. Command blocks A–E at the end reproduce the numerical evidence. N means either starter wins, P means either starter loses. A P-move in the proof is a *poisoned pawn move*, a different use of P.

**1. Lines 21–26, 39–45. “A side wins G + ⋆h moving first iff it wins the reduced game moving first.” Gap in the domain, sound proof after repair — PROVED.** A resolved race needs its winner, including who just moved in case of a tie. A terminal root must already carry that result or be excluded. The search starts at unresolved roots. For either choice of mover, a T-move wins, an L-move loses, and the opponent can answer a P-move immediately with a T-move, even with a heap available. Deleting every move when all are losing leaves the same loss. On a K-move the board advances, on a heap move the heap decreases. The sum of all pawns' remaining single steps to the last rank plus the heap size strictly decreases on either kind of move. These facts prove the recursion for both starters. “Keep their values” in line 45 is stronger wording than this induction establishes for individual followers.

**Replacement for the lemma and last clause of its proof.** “For a pawn position with no passed pawn, either starting side, and any heap in the stated range, the full and reduced games give that starter the same win/loss result. A resolved root is scored directly. For K- and heap moves the opponent's win/loss result agrees by induction on total remaining pawn distance plus heap size. Heap moves leave the pawn position, including its flag, unchanged.”

**2. Lines 49–57. “After any move of q, Z has no passed pawn.” Sound for either colour, with the stated flag hypothesis — PROVED.** On the exact triple of files, the two enemy pawns are two ranks ahead in the mover's direction. Neither is one rank ahead for an ordinary capture or abreast for e.p. A single push keeps both blockers ahead. The only double push is White's E-type move from 2 to 4. The adjacent B4 can take on rank 3, so the stepped pawn fails the e.p.-aware passed test. Under the textbook test it would be passed. No enemy piece was displaced. Expiry of the old flag cannot release a passer of the mover, since the old victim belongs to the opponent. The statement is needed even when a flag exists after the opponent's preceding move, not for an arbitrary flag on the mover's own pawn.

**Replacement for lines 55–57.** “Let q be the pawn on file j and let Z be its colour and the side to move. Each adjacent file contains only an enemy two ranks ahead of q. Thus neither ordinary capture nor e.p. capture by q is available. After a single push q still faces an enemy strictly ahead on an adjacent file. After the only possible double push, W2–4, an adjacent B4 can capture q en passant. No other pawn of Z gains passed status, since no enemy moved and any expiring flag concerned an enemy pawn.”

**3. Lines 52, 58–60, 106–117. “Y takes q ... with his pawn on j+1”; “the one X pawn whose status changed”. False as a direction for both windows. The lemma's conclusion is sound — PROVED.** Choose a sign from the hypothesis. Only the pawn two files away on the *chosen* side could lose its blocker. It stays blocked, so its passed status does **not** change. The five table rows give the correct geometry for the right window. In O, W3–4 is taken by B5 on rank 4, and B5–4 by W3 on rank 4. In E, W2–3 is taken by B4 on rank 3, W2–4 by B4 en passant on rank 3, and B4–3 by W2 on rank 3. Each is a poisoning reply only after ruling out an immediate L.

A counterexample to using the printed direction in the left-window case is the following eleven-file O-type position, no flag. Files 3 through 8 contain W3, B5, W3, B5, W3, B5. All other files are empty. Black plays the pawn on file 6 from rank 5 to 4. The child has no passer. White's capture from file **7** to (6,4) releases the B5 on file 8. Both promotion distances are four, so Black wins the tie. White's capture from file **5** instead leaves both surviving black pawns blocked and wins outright. The hypothesis holds on files 3 through 7. This example refutes the uniform choice of reply, not Lemma 2(b). Also, in an E-type five-file window B4,W2,B4,W2,B4 on files 4 through 8 of an otherwise empty ten-file board, W2–4 on file 5 is L. The B4 on file 4 immediately becomes passed. The vulnerable white pawn is not passed. Both examples follow by inspection and can be replayed with E.

**Replacement for lines 58–60 and the table heading.** “Write X for the mover and choose s in {−1,+1} so that j−s,j,j+s,j+2s,j+3s are pattern files. By (a) the mover has no passer. If Y already has one, the move is L. Otherwise Y captures q from j+s, en passant after W2–4. The capturer has no enemy on j−1,j,j+1 and is passed. Among surviving X pawns only the pawn on j+2s could lose a blocker when the capturer leaves j+s. The enemy on j+3s still blocks it. Thus Y alone has a passer and the original move is P.” Table heading: “Wall advances and their poisoning replies in the non-terminal branch (s=+1 shown).”

**4. Lines 63–73. “Every pawn of p has the same three-file view”; “all their moves are L or P.” Sound, with a missing definition of insertion on flagged children — PROVED.** The unflagged parent has identical local file contents at each old pawn. Across the cut a copy supplies the former neighbour. Each new pawn has two enemy pattern neighbours strictly ahead. No old pawn changes passed status and no new one is passed. For step (i), the old central origins are c−3 through c+4. A right-hand five-file window fits for j≤c+2, a left-hand one for j≥c−1. Their overlap is harmless. On the enlarged board the central range is c−3 through c+6, and the enlarged pattern ends at c+7. Lemma 2(b) applies to all those pawns, including double pushes immediately beside the cut. No central move survives as K or T.

For step (ii), an outside move changes files at distance at most one from its origin. It cannot cross the cut or change c−2 through c+3. A double push puts its flag on its own file, with the same eligible neighbouring capturers. The old cylindrical seam outside the insertion still joins the same old files. Therefore making the move commutes with inserting the pair. The new pawns stay blocked. Each old passer has the same rank, the same own-file occupancy for the front-pawn test and the same e.p. eligibility. The last mover also agrees. This preserves the winner in a count race, including ties, not just the existence of some passer.

**Replacement addition to lines 64–65, 72–73.** “Use consecutive representatives of the ten distinct files in one alternating wall arc. Write u(f)=f for f≤c and u(f)=f+2 otherwise. Keep every old file at u(f), place copies of c+1 and c at new c+1 and c+2 respectively, and carry any flag to the image of its original victim, with the same capture right. Do not flag a copy. For an outside move, its changed squares, and the neighbours relevant to any double step, avoid the cut. Its child therefore maps to the corresponding child. The inserted pawns are blocked, and each image passer has the same rank, front-pawn test and e.p. eligibility. With the same last mover the count result is unchanged.”

**5. Lines 74–76. “with the same children and, by (ii), the same result”; “never win for Y”. Logical gap and an overstatement in the explanation — PROVED after repair.** Step (ii) concerns first moves from a flag-free parent, with origins outside a wider interval. A reply from c−2 or c+3 need not meet those hypotheses and can be made from a flagged child. Step (iii) needs to exclude an **immediate terminal win** by a near replying pawn. Lemma 2(a) does not decide whether some later continuation wins. Children on boards of different widths correspond under insertion.

**Replacement for lines 74–76.** “Suppose the child of the outside move is non-terminal. Its files c−2 through c+3 are unchanged pattern files. For Y, the origins c−1 through c+2 on the old board, and c−1 through c+4 on the enlarged board, have exact pattern triples. Any flag is on X's pawn. By Lemma 2(a) a reply from one of these origins cannot give Y a passer. Every other reply corresponds on the two boards. A reply from c−2 may touch c−1, and one from c+3 may touch c+2, but neither can touch c or c+1. An e.p. victim left by the first move lies on its far origin file, so its capturer and skipped square are outside the cut as well. Any new double-step flag and its eligible neighbours correspond. Hence insertion commutes with each far reply and preserves its terminal winner by the three-file and race argument above. A terminal-winning reply exists on one board iff it exists on the other. This proves P equivalence, hence K-child correspondence and equality of the two side-specific T indicators.”

**Comparison with S15 Note 1 §2b.** The written-out argument proves this replacement for either mover and either phase. Its different family, wall endpoints and cut are applications, not extra hypotheses. Its stronger observation that the far T-moves themselves correspond suffices for S13's T indicator. Its view lemma V1 for arbitrary positions is about *file contents*. It would be false to infer unrestricted e.p.-move correspondence from V1 alone. For example, after W2–4 on old c, an adjacent B4 on old c+1 can capture. After copying these files, the first copy of B4 may capture the flagged original, but the image of the original B4 is no longer beside it. Such a flagged cut is excluded here. The parent is flag-free, the first move under comparison is far, and every surviving far reply leaves c,c+1 untouched. Thus §2b supplies the needed proof under the same effective hypotheses. Neither text proves that a near reply loses the eventual game.

**6. Lines 79, 88–93. “induction on the distance from the start”; “the shifted zone.” Sound, with no missing width — PROVED given C1/C2.** For odd n the fixed interval outside the zone is [5,n−2]. The cut 9 uses [5,14], requiring n≥16, first odd width 17. For even n the interval is [4,n−2]. The cut 8 uses [4,13], requiring n≥15, first even width 16. These are sufficient bases for these cuts and zones. Stabilisation of a node count at an earlier width would not supply the ten-file hypothesis. In O/E an arc made entirely of wall files cannot traverse the core at file 0. When the small ring has too few distinct wall files for a lemma's window, that application is simply unavailable. Overlapping allowed windows in a larger wall require only one valid choice.

In both roots the wall colours alternate and each pawn has an opposing blocker strictly ahead on its own or an adjacent file. In the odd core the stacks on files 0 and 2 block each other within each file, and B5 on 1 sees white pawns on both sides. In the even core the mixed stacks on 1 and 2 block each other within each file, and B5 on 0 sees W2 on 1. The endpoints of each wall have an opposing blocker within the wall or core. Inserting one correctly phased pair preserves each root, including its empty flag. Both moves that increase width and moves within a graph are accounted for. Deleting the inserted files recovers the old position, so insertion is injective. Lifting a path gives inclusion in the new reachable set. Conversely, starting from the image root, Lemma 3 says that *every* K-successor of an image node is again an image node. This gives surjectivity by path length. T-wins need only be preserved per side at each node. No computation at the next width is a premise.

**Replacement for lines 90–93 up to the outcome claim.** “Insertion takes the root to the next root and has a left inverse obtained by deleting the new files. Lift and project paths of K-edges from the roots, using Lemma 3 in both directions. This identifies all reachable pawn positions, their side-labelled K-edges and their T indicators. The flag stays absent. The low end of the zone is unchanged and its old file n−1 becomes n+1, the last file of the new board. Thus the same invariant holds at width n+2. The odd induction starts at 17 and the even induction at 16. C2 supplies odd 5,7,9,11,13,15 and even 6,8,10,12,14. The case 16 is C1 for the even induction.”

**7. Lines 18, 35–36, 93. “Gₙ + ⋆2 is a P-position, i.e. Gₙ = ⋆2.” Sound as a normal-play difference test, ambiguous as an operational assertion — PROVED.** A four-entry signature is not a general test set for comparing two arbitrary games. Here the P-entry occurs at the *candidate's negative*. There are two precise deductions.

- Under the heap rules alone, if both starters lose at heap 2, every heap move from 2 to 0 or 1 hands a win to the other side. Exchanging the starter proves N for each smaller heap. From any larger allowed heap either starter can move to heap 2 and win. Thus the outcome is P exactly at 2, N otherwise, throughout the text's range 0≤h<256. The observed NNPN is sufficient and its N entries are redundant.
- In ordinary short partizan normal play, represent each adjudicated child by its signed integer +256 or −256 and keep the board flag across a move in the other summand. This gives a fixed board game G. Against a heap, the signed integer has the outcome of its sign: the favoured side may empty a nonempty heap, and the unfavoured side has only heap moves. Induction identifies the operational outcome with the ordinary sum at the root. A short normal-play game is zero iff both starters lose. Since −⋆2=⋆2, the observed P-position is precisely G−⋆2=0. This gives genuine CGT equality, hence substitution against arbitrary ordinary addends **in that representation**. Immediate adjudication of a pawn win in a compound with arbitrary side games is a different rule. For example, in ordinary arithmetic +256 added to −256 is zero. The proof does not justify overriding that cancellation.

**Replacement for the theorem and final inference.** “For every n≥5 and every heap 0≤h<256 the whole-board position Gₙ + ⋆h is P if h=2 and N otherwise. Indeed both starters lose at heap 2. Its heap options give the two smaller N outcomes, and every larger heap can move to 2. With resolved children represented by the signed integers ±256 and disjunctive heap moves preserving the board state, the normal-play difference test also gives Gₙ=⋆2.” The finite premises qualification in line 93 is already correct.

## Finite evidence and attribution

**8. Lines 81–83. “Two independent programs build the same graph.” Sound for the graph actually compared — CHECKED-2.** C1 counts pawn positions reachable from the root by K-moves of either colour. Either side can be chosen at each K-step when constructing the graph, even if the preceding K-step had the same colour. Actual play alternates sides and may interleave heap moves. The node key includes a canonical e.p. flag. The graph omits heap sizes, starters and terminal sinks from the node count. `rg.c reduce` produces the first graph. `reduced_cyl.py` builds the other with `cylcgt` pawn moves, passed tests and race resolution. `logs/reduced_cyl_odd.log` covers odd 5–23 and `logs/reduced_cyl_even.log` even 6–22, inclusive by twos. The equality test compares the full node sets and sets of (source, side, target) triples, collapsing T to one target per side and source. It does not compare distinct moves that lead to the same target.

| C1 base | Pawn nodes | K-moves | T-moves before collapsing | Distinct triples, K and T | Flagged nodes | Files that differ somewhere |
|---|---:|---:|---:|---:|---:|---|
| O, 17 | 144 | 209 | 246 | 308 | 0 | 16, 0, 1, 2, 3, 4 |
| E, 16 | 104 | 177 | 97 | 231 | 0 | 15, 0, 1, 2, 3 |

The `pump_odd_c9.log` and `pump_even_c8.log` records supply move counts, flags, deviations and reduced outcomes for heaps 0–7, over odd 9–61 and even 8–60. The comparisons at cut 9 start with 17→19, at cut 8 with 16→18. This review reran the separate `verify/red.py` at both bases and `verify/zonecmp.py` against both zone-state lists. Both base signatures were NNPN and both projected node sets agreed exactly. The unreduced C search tests the actual board plus the heap. `reduced_value.py` instead evaluates the independently generated reduced board with `cgt.make` and signed integer T-options. Its log gives canonical ⋆2 for odd 5–25 and even 6–26. The latter is the value of the **reduced** board. Lemma 1 connects the two outcome calculations. Commands B–D.

**Replacement for C1.** “Count the K-reachable pawn positions with their flags, excluding sinks and the heap. At O₁₇ and E₁₆ there are respectively 144 and 104 positions, all flag-free, with deviations confined to the stated zones. The C and cylcgt-based builders agree on node sets, side-labelled K-successors and existence of T at each side and node. Direct unreduced heap search and canonical evaluation of the cylcgt-based reduced board both give P at heap 2.”

**9. Line 84. “unreduced search; whole-board cylcgt for n≤10”; paper: “checked by two programs for n<17”. True at every claimed width — CHECKED-2.** The uniform pair is `rg.c solve 3`, driven by `fullsweep.py`, and the separate Python `verify/eng.py` (`Solver.win`), whose per-width outputs are `verify/sweep_O.txt` and `verify/sweep_E.txt`. Both search the unreduced whole board for both starters. Neither uses Lemma 2 or 3. The C sweep in `logs/fullsweep.log` alone is **COMPUTED-1**. Its O and E rows cover 29 odd widths 5–61 and 28 even widths 6–60. Its 113 total includes 56 F positions. The verifier's two O/E files independently record every one of the 57 O/E widths. Rerunning the same C executable via another wrapper would not give a second implementation.

| Widths in the paper's claim | Archived comparison | Additional evidence |
|---|---|---|
| 5, 6, 7, 8, 9, 10 | C unreduced vs verifier Python unreduced | Direct whole-board canonical `cyl_whole.py`: O at 5,7,9 and E at 6,8,10 |
| 11, 12, 13, 14, 15 | Same two unreduced engines | Independent cylcgt reduced graph and reduced canonical value |
| 16 | Same two unreduced engines | Also the even C1 base with both graph builders and reduced canonical value |

The two `logs/cyl_whole_*.log` files end at 9 odd and 10 even. Accordingly, attributing the **two unreduced checks at 11–16** to C plus whole-board canonical `cylcgt` would be false. Even within `logs/` alone the C and independently built reduced-canonical routes support the low-width result via Lemma 1. The verifier files provide the stronger direct comparison. Commands B–D.

**Replacement for C2.** “For every member through width 61 (odd 5–61, even 6–60), the unreduced C solver and the independent Python verifier give NNPN for heaps 0,1,2,3. Whole-board canonical cylcgt separately gives ⋆2 at widths 5 through 10. The induction uses only the widths strictly below the respective bases from this sweep.”

**New check — CHECKED-2 against the archived engines.** `delegate/out/T89/check.py` was written from the family and game descriptions, using Note 1 §1 for the missing count formula, before inspecting the cited solver implementations. It has no project imports. Each rank is a row of bits, with circular file shifts for captures. The recursion evaluates pawn moves and all smaller heap moves directly, stopping when it finds a winning move. It uses no poison pruning, graph transfer or canonical-form routine. On every width **5 through 17**, both starting sides win at heaps 0, 1 and 3 and lose at 2. Its built-in checks exercise a double push with a capture across the seam, the changed passed status when the flag is removed, and a tied count race for either last mover. Command A. This is an outcome calculation, not a fresh canonical-form computation.

## Definitions, wording and remaining lines

**10. Lines 18–33. “race rule ‘count’”; “that side wins the race”; “A pattern file contains precisely its one starting wall pawn.” Gap in the stand-alone model; the current pattern definition suffices when read as square occupancy — PROVED.** The text names the count rule without defining the distance, own-file eligibility or tie break. The winner does not determine whether a position is terminal: any passer triggers adjudication. Specify which side owns the capture right, what the heap does to the flag, and that the four classes are for pawn moves. “Starting pawn” should denote exactly the prescribed colour and rank, independent of any historical identity. A file with its original pawn **and an extra pawn** is excluded by the current word “precisely”. Files 3 through n−1 comprise one wall with a fixed phase. A single file elsewhere that happens to match a wall token is not thereby part of that wall. Under this reading all later O/E pattern uses are legitimate.

**Replacement for the model paragraph, retaining the four class definitions.** “Ranks are 1 through 8 and files are indexed modulo n. White advances towards 8 and Black towards 1. Use the usual unobstructed pawn steps, home-rank double steps and diagonal captures, including across the seam. A double push records the victim and the opponent's right to capture onto the skipped square only if an enemy pawn stands beside the landing square. A pawn move consumes the previous flag and may create a new one. A heap move preserves the board and flag. A pawn is passed if no enemy lies strictly ahead on its own or either neighbouring file and it is not currently e.p.-capturable. A child with any passer is resolved immediately. If both sides have a passer, compare each side's least promotion distance over passed pawns with no pawn ahead on their own file. At rank r use 8−r−[r=2] for White and r−1−[r=7] for Black; an empty minimum is infinite. The smaller distance wins and a tie goes to the side that did not just make the pawn move. Give a resolved child its winner's signed integer ±256. At an unresolved node a side with no legal move loses. Classify pawn moves separately for each colour as follows.”

**Replacement addition to the rings paragraph.** “Read the displayed files in order from 0 to n−1, with no initial flag. Set Gₙ=Oₙ for n odd (integer k≥1) and Gₙ=Eₙ for n even (integer m≥0). A pattern file is a file in this wall occupied by exactly one pawn of its prescribed starting colour and rank. Call that pawn a wall pawn on file j when applying the local lemmas.” For O there are 3+2k files and 6+2k pawns. For E there are 4+2(m+1) files and 7+2(m+1) pawns. Both counts give n+3. The same two-file phase repeats across either insertion.

**11. Lines 79–82, 100–104, 120–123. “the three window files”; “never move and are never captured”; “radius ≥3”. Mixed scope — PROVED for reachable-node contents, COMPUTED-1 for the original radius experiment.** The zone is the set of files on which some K-reachable node differs from the start. Calling files 0,1,2 the core avoids introducing a new “window”. The base node lists, in the stated cyclic order, lift unchanged. Agreement outside the zone rules out a K-move changing a frozen file. It says nothing about variational play after choosing a deleted move or about the board behind a collapsed T sink. For instance, the deep W3 of the odd root can legally advance in the full game, exposing itself to capture. The whole-board restriction at 120–121 is sound. The radius is a *sufficient* hypothesis, not a lower bound. The archived odd-family sensitivity experiment used correct-phase radii 1,2,3 and a wrong-phase run at 5. Its counts of failures were respectively 217, 1, 0 and 1,968. The separate correct-phase runs at 5 found none. These are sampled results, not an examination of every radius or every position. Commands B, D.

**Replacement.** “Call files 0,1,2 the core. At each base let the zone be the union of the files differing from the start over all K-reachable nodes. Beyond the base the same zone contents occur in corresponding nodes, with its last-file coordinate shifted. On every K-path the files outside the zone retain their initial contents. This proof uses a ten-file pattern interval (radius 5). In the reported odd-family sensitivity sample, the correctly phased insertion failed at radii 1 and 2 and had no failure at 3; the wrongly phased insertion failed at radius 5. The correct-phase radius-5 samples had no failure.”

**12. Lines 124–125. “The same proof applies to the single-step family Fₙ.” Incomplete as a stand-alone transfer, irrelevant to O/E — PROVED for the applicability of the induction given the F finite premises; CHECKED-2 for the archived base sizes.** A core and a type of wall do not specify the phase at the join, the extra file at even width, the exceptional missing width or where the zone is. Command D identifies the F base logs and independent pump checks. The row saying “no cut” at a base compares that row with the *previous smaller* width. It does not test insertion out of that base.

**Replacement.** “For completeness put K=(W3B6,B6,W4B7,W4,W6B7). At odd n≥5 set Fₙ=(B4,W2)^((n−5)/2) K; at even n≥8 set Fₙ=(B4,W2)^((n−6)/2) K W2. The flag-free even base at 18 has 662 positions with zone {n−7,…,n−3}; the odd base at 19 has 3,568 with zone {0,1,n−6,…,n−2}. Both have the required P outcome at heap 2. The even cut 4 uses [0,9] and the odd cut 6 uses [2,11], entirely in the unchanged prefix wall. Insertion lengthens that alternating prefix by one pair and shifts precisely the high zone coordinates by two. Apply the same induction, using the separate F outcomes at defined widths below the bases.” This is a conditional transfer; this review did not independently solve F.

Lines 1–17, 37–38, 46–48, 61–63, 67–68, 77–80, 85–87, 94–99, 107–109, 115–116, 118–119 and 126 contain source comments, headings or TeX structure apart from the statements audited above. The five move rows at 110–114 and the no-enemy assertion at 117 are sound under finding 3's choice of orientation and non-terminal branch. Line 4 describes a label; the qualification actually printed at line 93 correctly records the dependence on computations.

## Reproduction and limits

Run from the project root with the existing environment. These commands leave the archived reports and logs intact. Set the following variables in the shell for blocks A–E.

```sh
D=research/ring_family_proof
P=.venv/bin/python
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
```

**A. Fresh full-board signatures and embedded rule checks.**

```sh
"$P" -B delegate/out/T89/check.py 5 6 7 8 9 10 11 12 13 14 15 16 17
```

**B. Base graphs, zones and finite comparisons.** The verifier rebuilds were run for this review. The remaining lines give the original builders' reproduction commands, using the existing C executable.

```sh
"$P" -B "$D/verify/red.py" O 17
"$P" -B "$D/verify/red.py" E 16
"$P" -B "$D/verify/zonecmp.py"
"$P" -B "$D/reduced_cyl.py" odd 5 7 9 11 13 15 17 19 21 23
"$P" -B "$D/reduced_cyl.py" even 6 8 10 12 14 16 18 20 22
FIXC=9 "$P" -B "$D/pump_verify.py" odd 9 61
FIXC=8 "$P" -B "$D/pump_verify.py" even 8 60
"$P" -B "$D/reduced_value.py" odd 5 7 9 11 13 15 17 19 21 23 25
"$P" -B "$D/reduced_value.py" even 6 8 10 12 14 16 18 20 22 24 26
```

**C. Archived unreduced results and direct canonical checks.** The width ranges below use zsh brace expansion. The canonical commands are the original, slower runs.

```sh
"$P" -B "$D/fullsweep.py" 61
"$P" -B "$D/verify/eng.py" O {5..61..2}
"$P" -B "$D/verify/eng.py" E {6..60..2}
"$P" -B "$D/cyl_whole.py" odd 5 7 9
"$P" -B "$D/cyl_whole.py" even 6 8 10
```

**D. Inspect exact archived coverage, stress results and F data.** These are the evidence underlying the cited ranges. To regenerate the radius sample use the four indicated calls, without overwriting its log.

```sh
cat "$D"/logs/{fullsweep,cyl_whole_odd,cyl_whole_even,reduced_cyl_odd,reduced_cyl_even,reduced_value}.log
cat "$D"/verify/sweep_{O,E,F,F2}.txt
cat "$D"/logs/pump_{odd_c9,even_c8,Feven_c4,Fodd_c6}.log
cat "$D"/verify/F_pump_l3.txt
cat "$D"/logs/lemmaL_{sensitivity,odd,even,F}.log
for r in 1 2 3; do "$P" -B "$D/lemmaL_test.py" odd 30000 11 "$r"; done
MUTATE=1 "$P" -B "$D/lemmaL_test.py" odd 30000 11 5
for family in odd even F; do "$P" -B "$D/lemmaL_test.py" "$family" 100000 11 5; done
```

**E. Replay the two local counterexamples of finding 3.** Coordinates use the file numbering in S13. The assertions give the winner after each possible capture and the class of the E-type double step.

```sh
"$P" -B - <<'PY'
import sys
sys.path.insert(0, 'research/ring_family_proof/verify')
from eng import classify_moves, moves, parse, status
p = parse('- - - W3 B5 W3 B5 W3 B5 - -'.split())
q, flag = next((u, f) for u, f in moves(p, None, 'B') if u[6] == (0, 8))
assert status(q, flag, 'B') is None
winners = {next(j for j in (5, 7) if not u[j][0]): status(u, f, 'W')
           for u, f in moves(q, flag, 'W') if u[6] == (8, 0)}
assert winners == {5: 'W', 7: 'B'}
p = parse('- - - - B4 W2 B4 W2 B4 -'.split())
assert [(k, f) for k, u, f in classify_moves(p, None, 'W')
        if u[5][0] == 8] == [('L', (5, 'W'))]
PY
```

**Limits.** The fresh search covers O/E through 17, heaps 0–3, the e.p.-aware rule, count races and persistent board flags. The larger widths, the direct canonical calculations, the F data and the random stress tests above are attributed to their archives. This review did not rerun those sweeps, formally verify the move generators or CGT arithmetic, evaluate the component-sum model, or check real chess. The sandbox denied the requested niceness adjustment, so only short, sequential checks were run at the inherited priority. No network was used.
