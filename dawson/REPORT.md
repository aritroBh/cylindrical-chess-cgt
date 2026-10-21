# Dawson's chess on flat boards and cylinders (workstream A6)

Saved by the parent session from the workstream's final report (workflow `wf_3dfce063-f42`). Workflow agents may not write report files, so the text below is the agent's, unedited apart from removing that notice. Verification verdicts come from the workflow's adversarial verifiers; "not verified" includes verifiers that were cut off by a usage limit.

Commands run from the project root. Each number gives its reproduce command (section 7) and a status:
- "two implementations": two independent programs agree;
- "one implementation": computed once by a single program;
- "literature": taken from a cited source;
- "proof": argued on paper, and machine-checked where stated.

## 0. Headline results

1. **Rules and the section 8 fix.**
   - Dawson's chess is a 3xn pawn game with compulsory captures.
   - Dawson posed it in 1935 as a misere game: the player who makes the last move loses.
   - Guy and Smith (1956) solved normal play by identifying it with the octal game 0.137.
   - The 2025 paper's section 8 gets three things wrong:
     - **The board and move rule.** Under the stated rule no first move exists.
     - **The Grundy recurrence.** It omits the end-file move and the 1-file move. Its G agrees with the true g at only 31 of the 301 values n = 0..300.
     - **The cylinder outcomes.** As a result they are wrong for 56 values of n <= 300.
   - Replacement text: dawson/section8_corrected.tex.
2. **Flat boards, normal play** (two implementations, plus literature).
   - Solving straight from the pawn rules agrees with 0.137 at every position reachable from the start. This holds on every flat board n <= 16, in both normal and misere play.
   - g(n) for n <= 300 has period 34. The only n with g(n) != g(n+34) are 14, 16, 31, 34, 51, so the last exception is n = 51.
   - The octal periodicity theorem then proves g(n+34) = g(n) for all n >= 52.
   - All of this is classical; it is reproduced here, not new.
3. **Cylinder, normal play** (proof, plus machine check for n <= 16).
   - **Ring rule.** On a full 3xn cylinder with n >= 3, every first move opens the ring into one strip of n-3 files. So R_n = mex{g(n-3)}, which is 0 or 1.
   - **Outcomes.** The first player wins exactly when g(n-3) = 0: n = 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57, 61, 65, 75, 79, ...
   - **Periodicity.** Period 34 for all n >= 38. The last exception is n = 37, and 34 is the least period there.
   - **Novelty.** The argument is elementary and probably folklore; I do not claim it as new.
4. **Misere play.**
   - **Exhaustive search.** It covered all 359,799,167 sums of strips with total length <= 100. Python and C agree on all 1,798,287 positions of total <= 60. Totals 61..100 come from the C program only.
   - **Quotient algorithm.** I wrote an independent implementation of the Plambeck–Siegel (MisereSolver) quotient algorithm. It reproduces their published partial quotient for strips <= 32 (= Dawson's Kayles heaps <= 33) exactly: **order 638, with 109 elements in the P-portion (the classes of losing positions)**.
   - **Checks on that quotient.** It was proved by full verification. It also agrees with exhaustive search on all 7,422,423 positions with strips <= 32 and total <= 70.
   - **Strips <= 33.** The next partial quotient did not converge. Candidate sizes went 1580, 1922, 5236, 6740, 18408 before the 28-minute timeout, on a machine with load average about 128 from other jobs. Plambeck–Siegel suspect this quotient is infinite; my run is consistent with that but is not evidence either way.
   - **No period.** No period is visible in the misere single-strip outcomes up to n = 100.
   - **Status in the literature.** Misere Dawson's chess is still open. I found no source claiming a solution.

## 1. Rules (task 1)

Source: T. R. Dawson, Caissa's Wild Roses (1935), reprinted in Five Classics of Fairy Chess (Dover, 1973). Description as in Plambeck & Siegel, arXiv:math/0609825 v5, section 1.

- **Board and start.** 3xn board. A White pawn on every square of rank 1, a Black pawn on every square of rank 3, rank 2 empty.
- **Moves.** Pawns move as in chess: one square straight forward onto an empty square, or one square diagonally forward to capture.
- **Captures are compulsory.**
- **No other pawn rules arise.**
  - There is never room for a double step, so there is no en passant.
  - No pawn ever reaches its last rank, so promotion never arises. A pawn that reaches rank 2 attacking an enemy pawn is always captured first. The direct solver confirms this: it never reaches a promotion on any board n <= 16, flat or cylinder.
- **Normal play.** The last player to move wins. This is the Guy–Smith analysis (Proc. Cambridge Philos. Soc. 52 (1956) 514–526), with the game equal to octal 0.137.
- **Dawson's own 1935 question was misere:** the last player to move loses. Plambeck–Siegel's footnote 2 quotes Guy recalling that Dawson proposed it as a losing game.

**Why the game is impartial and equal to 0.137.**
- **Untouched files.** Call a file untouched if it still has W on rank 1, B on rank 3 and an empty rank 2. In a quiet position (no capture available) the only legal moves are pushes from untouched files.
- **The forced sequence after a push on file f.**
  - Both neighbours untouched: 5 forced plies. Both neighbours end up empty, file f holds a blocked W/B pair, and the opponent is to move.
  - One neighbour untouched: 3 plies, and that neighbour is emptied.
  - No neighbour untouched: 1 ply, and the pushed pawn is blocked.
  - The choices inside these sequences do not change the result.
- **Empty and blocked files are inert forever.** A pawn can enter a file only by capturing a pawn already on that file. Blocked files have only empty neighbours.
- **Conclusion.** A row of n untouched files is a row of n pins in which a move removes a pin together with its surviving neighbours. That is 0.137, the same game tree as Dawson's Kayles 0.07 with n+1 pins.
- **Misere too.** Each forced sequence has odd length and ends with the mover's ply. So the last mover is preserved, and the equivalence also holds in misere play.

**Errors in the 2025 paper's section 8** (prior_work/main.tex lines 207–222; notes/audit.md, last row):

| Paper says | Correct statement |
|---|---|
| A 1xn strip where you "remove a pawn only if both neighbours are empty" | The 3xn pawn game above. Under the paper's rule there is no move from a full row (n >= 2). The pin model removes a pin together with its neighbours. |
| G(n) = mex{G(a) xor G(b) : a+b = n-3} | g(0) = 0, g(1) = 1, and for n >= 2: g(n) = mex({g(n-2)} ∪ {g(a) xor g(b) : a+b = n-3}). The paper's version gives G(1) = G(2) = 0 and G(4) = 1, against the true g(1) = g(2) = 1 and g(4) = 0. |
| Ring(n) = mex(G(n-3)) | The form is right once the correct g is used, for n >= 3. With the paper's G, the predicted cylinder winner is wrong for 56 values of n <= 300, the first being 4, 5, 7, 23, 31. Example: the paper calls 3x4 a first-player win; it is a loss. |
| "Periodicity carries over" | g has period 34 for n >= 52 (last exception 51). The ring outcome has period 34 for n >= 38 (last exception 37). |
| Misere play not mentioned | Dawson's original question was misere, and it is still open. |

## 2. Flat boards (task 2)

**2.1 Direct solve from the pawn rules** (dawson/pawnboard.py, written without using the octal game).

The program runs memoised minimax over every position reachable from the start, with either side moving first, and computes normal-play and misere outcomes. Results:

- **Outcomes vs 0.137.** At every quiet position the outcome agrees with the 0.137 prediction:
  - flat boards: xor of g over the runs of untouched files;
  - full cylinder: R_n;
  - misere: the heap solver of section 4.
  - There are 0 mismatches for every flat board n = 1..16 (up to 563,962 positions) and every cylinder n = 3..16 (up to 450,954 positions).
- **Legal moves.** In every quiet position, every legal move starts from an untouched file.
- **Macro-moves.** A macro-move is a push followed by all its forced captures. Every macro-move passes the turn. White's and Black's sets of resulting shapes are equal to each other and to the 0.137 options. The Grundy value computed on this macro-move graph equals g(n) (or R_n).
- **Flat-board outcomes, n <= 16.** The first player loses exactly for n = 4, 8, 14 in normal play, and exactly for n = 1, 2, 6, 7, 11, 15, 16 in misere play.
- **Cylinder outcomes, 3 <= n <= 16.** The first player wins exactly for n = 3, 7, 11 in normal play, and exactly for n = 4, 5, 9, 10, 14 in misere play.
- **Degenerate 2-file cylinder.** It behaves like the 2-file strip: a first-player win in normal play, a loss in misere.
- **Cross-check with existing code.** For n <= 7, the existing cylcgt/dawson.py (dawson/cylcgt_dawson_small.txt) gives the same start-position outcomes.

**2.2 Grundy values to n = 300** (dawson/octal.py, a generic octal-game evaluator).

- **Cross-checks.** It agrees with cylcgt.dawson.octal_0137 for n <= 300 (two implementations). Also 0.137 at n equals 0.07 at n+1 for all n <= 300.
- **Values.**
  - n = 0..33: 0 1 1 2 0 3 1 1 0 3 3 2 2 4 0 5 2 2 3 3 0 1 1 3 0 2 1 1 0 4 5 2 7 4
  - one full period, n = 52..85: 3 3 0 1 1 3 0 2 1 1 0 4 5 3 7 4 8 1 1 2 0 3 1 1 0 3 3 2 2 4 4 5 5 9
  - The maximum value up to 300 is 9.
- **Period 34, last exception 51** (confirmed). Exceptions g(n) != g(n+34) occur only at n = 14, 16, 31, 34, 51.
- **Why the periodicity is proved for all n >= 52.** The Guy–Smith periodicity theorem (Fact 2.2 in Plambeck–Siegel) applies with n0 = 52, p = 34, k = 3. It needs agreement only for 52 <= n < 141, and the data check 52 <= n <= 266.
- **Second-player wins (g = 0), n <= 200:** 0, 4, 8, 14, 20, 24, 28, 34, 38, 42, 54, 58, 62, 72, 76, 88, 92, 96, 106, 110, 122, 126, 130, 140, 144, 156, 160, 164, 174, 178, 190, 194, 198.

**2.3 Caution: the canonical form of the diagram is not *g(n).**
- The existing cylcgt.dawson.solve computes the partizan canonical form of the start diagram. It gives:
  - flat n = 5: * (but g(5) = 3);
  - flat n = 7: *2 (but g(7) = 1).
- The outcomes still agree.
- **Why.** The canonical form allows moves that global compulsory capture forbids, such as ignoring a forced capture or moving twice inside one capture sequence.
- **Consequence.** The right object is the macro-move game. Strips on one board combine by nim-sum, and section 2.1 checks this directly on multi-strip positions.
- The "flat value" column of `python -m cylcgt.dawson` should not be compared with g(n).

## 3. Cylinder (task 3)

**Lemma (ring rule).** On the full 3xn cylinder with n >= 3, every first move plus its forced captures leaves exactly one strip of n-3 untouched files, with the opponent to move. Hence:
- R_n = mex{g(n-3)}: R_n = 1 iff g(n-3) = 0.
- In misere play, the first player wins iff the strip of n-3 files is a misere P-position (a loss for the player to move).

**Proof.**
1. On a full ring every file f has two distinct untouched neighbours, since n >= 3.
2. A push on f forces five plies, alternating captures from the two neighbours. Either order ends with f-1 and f+1 empty, f blocked, and the opponent to move in a quiet position.
3. For n = 3 the two neighbours are also adjacent to each other. That adds no captures, because their rank-2 squares are never occupied, so the ring is simply used up.
4. The files f+2, ..., f-2 (there are n-3 of them) are untouched and consecutive. They are bounded by permanently empty files, so they form an ordinary strip.
5. Rotation, and colour reversal with rank reflection, make all first moves of both players equivalent. So the ring has exactly one option.
6. The misere statement follows the same way: the mover wins iff the single option is a P-position.

**Machine check.** For every cylinder 3 <= n <= 16, the macro-move graph of the full ring has exactly one option shape, the strip of n-3, for both colours.

**Values to n = 300** (dawson/octal_300.txt, dawson/report_tables.txt).
- First player wins, n <= 200: 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57, 61, 65, 75, 79, 91, 95, 99, 109, 113, 125, 129, 133, 143, 147, 159, 163, 167, 177, 181, 193, 197.
- Least period 34 for n >= 38. The last exception is n = 37, because g(34) = 0 but g(68) = 8.
- For comparison, the paper's recurrence predicts cylinder wins at n = 3, 4, 5, 11, 17, 27, 35, 37, 49, 59, 69, 81, 91 (n <= 100).

**Novelty.** Reducing a circular octal game to the linear game after the first move is standard; this is a correction, not a new theorem.

Note for RESEARCH_PLAN A6: misere on the ring is exactly as hard as misere on a single strip, by the lemma. The ring gives no extra tractability.

## 4. Misere play (task 4)

**4.1 Exhaustive outcomes for sums of strips.**

Two solvers: dawson/misere.py (memoised) and dawson/misere.c (bottom-up over a ranking of partitions). Exact simplifications used:
- strips of length 0 are dropped;
- a strip of 2 is replaced by a strip of 1, since their game trees are identical;
- nothing else is simplified.

| Check | Positions | Disagreements | Status |
|---|---|---|---|
| Python vs C, all positions of total <= 60 | 1,798,287 | 0 | two implementations |
| Pawn-level misere minimax vs the heap solver, all reachable quiet positions on boards n <= 16 (flat and cylinder) | all of them | 0 | two implementations |
| C alone, all positions of total <= 100 | 359,799,167 | none to compare | one implementation for totals 61–100 |

**Single strips that are misere P-positions, n <= 100** (the first player loses misere Dawson's chess on 3xn). Confirmed by Python for n <= 60 and by the quotient for n <= 32:

1 2 6 7 11 15 16 20 21 25 29 30 34 35 39 44 48 49 53 54 58 62 63 67 68 72 76 82 92 96

- Normal-play losses for comparison: 0 4 8 14 20 24 28 34 38 42 54 58 62 72 76 88 92 96.
- The two sequences differ at 30 values of n <= 100; the largest are 82 and 88.

**Single rings where the first player wins in misere, n <= 103** (the strip list shifted by 3):

4 5 9 10 14 18 19 23 24 28 32 33 37 38 42 47 51 52 56 57 61 65 66 70 71 75 79 85 95 99

**Counts of misere P-positions** (dawson/misere_c_100.txt):

| Total | Misere P-positions | All positions |
|---|---|---|
| 20 | 62 | 242 |
| 40 | 2,429 | 11,323 |
| 60 | 48,756 | 251,247 |
| 80 | 652,831 | 3,664,312 |
| 100 | 6,733,364 | 40,371,156 |

**Where the game stops being tame.**
- The "tame" prediction plays misere Nim on the normal Grundy values. It first fails at {1, 9} and at {11}, then at {1,1,1,9}, {1,1,11}, {1,3,9}, and so on.
- This matches the quotient: it is the tame quotient T2 (6 elements) up to strips of length 8, and becomes wild at 9.

**Periodicity probe.**
- For every p <= 34 there is a mismatch o(n) != o(n+p) with n >= 63. For example, p = 34 fails at n = 63.
- So no period of length <= 34 has begun by n = 63. The data cannot support any period.

**4.2 Literature** (8 web fetches and searches used, 2 of them failed).
- **Plambeck & Siegel, "Misere quotients for impartial games"**, arXiv:math/0609825 v5 (2007). I believe it was published in J. Combin. Theory Ser. A 115 (2008); I did not re-check that.
  - Section 1 calls Dawson's chess open after more than 70 years ("Although Dawson's Chess remains open").
  - Section A.3: Guy and Smith first identified it with 0.137. Ferguson's unpublished genus analysis reached 0.07 heap 24. MisereSolver gives Q33(0.07) of order 638 with P-portion 109.
  - Figure 6 lists 0.07 as unsolved. The authors suspect every unsolved two-digit octal has an infinite misere quotient, with the listed n being the last finite partial quotient. That is a conjecture that Q34(0.07) is infinite, not a proof.
- **Supplement**, arXiv:0705.2404, Figure 1, marks 0.137 and 0.07 as wild, with normal play solved and misere unsolved. Its Appendix C gives the algorithm I re-implemented.
- **Gaps.**
  - Two web searches found no later solution.
  - OEIS has no entry for the misere single-strip P-sequence, in either the 0.137 or the 0.07 indexing.
  - I could not fetch Ferguson's note or miseregames.org: there was a TLS failure, and archive.org is blocked. So I cannot rule out that published single-heap tables already go beyond 33.

**4.3 Partial misere quotients, computed independently** (dawson/quotient.py).

Q_n is the misere quotient of all sums of strips of length <= n. Since a 0.137 strip of n is the same game tree as a 0.07 heap of n+1, Q_n(0.137) = Q_{n+1}(0.07).

**Method.** A re-implementation of the MisereSolver strategy from the supplement's Appendix C:
- P-verification (Fact C.1);
- the N-verification lexicographic traversal with subsumption (Algorithm 1);
- mex interpolation (Corollary 5.6);
- recalibration by freeing generators into a monoid with one generator t and relation t^(m+k) = t^m, then reducing. The heuristic for which generators to free and when to raise m is my own.

**Why the result is rigorous.** A candidate is accepted only if both verifications find no failure. That proves, by induction, correct outcomes for every position. The candidate is also reduced and its map is onto, so it is the quotient. The heuristic affects only running time.

**Orders found:**

| Strips <= n | 1–2 | 3–8 | 9–12 | 13–23 | 24–25 | 26–28 | 29 | 30 | 31 | 32 |
|---|---|---|---|---|---|---|---|---|---|---|
| order | 2 | 6 (T2) | 12 | 24 | 144 | 176 | 360 | 520 | 552 | 638 |
| P-portion | 1 | 2 | 3 | 5 | 23 | 28 | 65 | 89 | 93 | 109 |

- **n = 32 matches the published Q33(0.07) exactly**: two independent implementations agree.
- **Checks on Q32.** Full verification passed. It agrees with exhaustive search on 1,771,812 positions (total <= 60) and on 7,422,423 positions (total <= 70), with no disagreements.
- **Context.** The intermediate orders are not in the P–S paper; they may be on their website. The jump at strip 24 (0.07 heap 25) comes just past heap 24, where Ferguson stopped.
- **Equivalent to the empty position.** In Q32, strips 4, 8 and 14 have Phi equal to the identity, i.e. they behave like no strip at all.
- **Strip 33.** Every candidate image allowed by the meximal-set condition failed verification, so Q33 != Q32. Recalibration then did not converge before the timeout (log: dawson/quotient_run_33.txt). This is inconclusive.

## 5. New vs known

| Item | Status |
|---|---|
| Rules, the 0.137 equivalence, period 34 and last exception 51 | Known (Dawson 1935; Guy–Smith 1956). Recomputed here. |
| Correction of section 8 | New, but only as a correction of this project's own 2025 paper. |
| Ring rule and cylinder period 34 from n = 38 | Elementary and probably folklore. Here with a clean statement, a proof and a machine check. |
| Pawn-level verification for n <= 16 | A check, not a result. |
| Canonical form != *g(n) | A modelling caution only. |
| Misere Dawson's chess | Open. Not solved here. |
| Q32(0.137) = Q33(0.07): order 638, P-portion 109 | Known. Independently reproduced. |
| Growth sequence of orders for strips <= 32 | Not in the paper; possibly on the P–S website. Low significance. |
| Exhaustive misere tables to total 100 (single strips to 100, rings to 103) | Possibly new as a table. Strips 33..100 lie beyond the published quotient. One implementation for totals 61..100. No structure found. |
| Is Q33(0.137) finite? | Undecided. |

## 6. Housekeeping

## 7. Reproduce (from the project root)

**Normal play:**
- `PYTHONPATH=. .venv/bin/python -m dawson.octal 300` writes dawson/octal_300.txt.
- `PYTHONPATH=. .venv/bin/python -m dawson.pawnboard 16 16` writes dawson/pawnboard_16.txt (about 3 minutes).
- `PYTHONPATH=. .venv/bin/python -u dawson/run_cylcgt_dawson.py 7` writes dawson/cylcgt_dawson_small.txt (about 3 minutes).

**Misere, exhaustive:**
- `cc -O2 -o dawson/misere_c dawson/misere.c`
- `dawson/misere_c 100` writes dawson/misere_c_100.txt (a few minutes, about 360 MB RAM).
- `dawson/misere_c 60 dawson/misere_c_60.bin`
- `dawson/misere_c 70 dawson/misere_c_70.bin`
- `PYTHONPATH=. .venv/bin/python -m dawson.misere 45`
- `PYTHONPATH=. .venv/bin/python -m dawson.compare_misere 60 dawson/misere_c_60.bin`

**Quotients:**
- `PYTHONPATH=. .venv/bin/python -m dawson.quotient 32` (about 260 s under load) writes dawson/quotient_run_32.txt and dawson/quotient_Q32.pkl.
- `PYTHONPATH=. .venv/bin/python -m dawson.check_quotient dawson/quotient_Q32.pkl 70 dawson/misere_c_70.bin`
- `PYTHONPATH=. .venv/bin/python -c "from dawson.quotient import resume; resume('dawson/quotient_Q32.pkl', 33, 'dawson/quotient_run_33.txt')"` did not converge within the 1700 s timeout.

**Tables quoted above:**
- `PYTHONPATH=. .venv/bin/python -m dawson.report_tables` writes dawson/report_tables.txt.

## Claims

| id | importance | worker status | adversarial verification | statement |
|---|---|---|---|---|
| C1 | headline | checked-two-ways | reproduce: confirmed; refute: confirmed; theory: confirmed | The partial misere quotient of Dawson's chess for strips of length <= 32 (= Dawson's Kayles heaps <= 33) has order 638, and 109 of its elements are in the P-portion. This independently reproduces the Plambeck-Siegel MisereSolver result. |
| C2 | headline | checked-two-ways | reproduce: confirmed; refute: confirmed; theory: partially-confirmed | Section 8 of the 2025 paper is wrong in three ways. (1) Its rule, 'remove a pawn whose neighbours are empty' on a 1xn strip, allows no first move. (2) Its recurrence G(n)=mex{G(a) xor G(b): a+b=n-3} omits the end-file move g(n-2) and g(1)=1; it agrees with the true g at only 31 of the 301 values n=0..300. (3) As a result its ring predictions are wrong for 56 values of n<=300 (first 4, 5, 7, 23, 31). The correct recurrence is g(0)=0, g(1)=1, and g(n)=mex({g(n-2)} ∪ {g(a) xor g(b): a+b=n-3}) for n>=2. |
| C3 | key | proved | refute: confirmed; reproduce: confirmed | Ring rule. On the full 3xn cylinder with n>=3, every first move together with its forced captures leaves exactly one strip of n-3 files, with the opponent to move. So R_n = mex{g(n-3)}, and the first player wins iff g(n-3)=0 (n = 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57, ...). In misere play, the first player wins iff strip n-3 is a misere P-position. The normal-play outcome has least period 34 for n>=38, with last exception n=37. |
| C4 | key | checked-two-ways | reproduce: confirmed; refute: confirmed | Normal-play Grundy values of 0.137 for n<=300 have period 34. The only n with g(n) != g(n+34) are 14, 16, 31, 34, 51, so the last exception is 51. The Guy-Smith periodicity theorem then proves periodicity for all n>=52 (it needs a check of 52<=n<141; the data cover 52<=n<=266). |
| C5 | key | computed-once | not verified | Solving the pawn rules directly (compulsory captures, no octal assumption) agrees with 0.137 at every reachable quiet position on every flat board n<=16 and every cylinder 3<=n<=16, in both normal and misere play. Promotion is never reached. Macro-moves always pass the turn, and White's and Black's option shapes coincide with the 0.137 options. |
| C6 | key | computed-once | not verified | Misere single strips that are P-positions (the first player loses misere Dawson's chess on 3xn), n<=100: 1 2 6 7 11 15 16 20 21 25 29 30 34 35 39 44 48 49 53 54 58 62 63 67 68 72 76 82 92 96. No period p<=34 is visible: every p<=34 has a mismatch at some n>=63. |
| C7 | minor | computed-once | not verified | Orders of the partial misere quotients Q_n (n = longest strip allowed): - n=1-2: 2; - n=3-8: 6 (the tame quotient T2); - n=9-12: 12; - n=13-23: 24; - n=24-25: 144; - n=26-28: 176; - n=29: 360; - n=30: 520; - n=31: 552; - n=32: 638. The corresponding P-portions are 1, 2, 3, 5, 23, 28, 65, 89, 93, 109. |
| C8 | minor | conjecture | not verified | Q33(0.137) = Q34(0.07) is not equal to Q32. My recalibration did not converge within 28 minutes: candidate orders went 1580, 1922, 5236, 6740, 18408. This is inconclusive about finiteness. Plambeck-Siegel conjecture that this quotient is infinite. |
| C9 | key | checked-two-ways | not verified | In the literature, misere Dawson's chess (Dawson's original 1935 question) is unsolved. Plambeck-Siegel (2007/08) reach heap 33 of 0.07, and their supplement marks 0.137 and 0.07 as wild with misere play unsolved. I found no later solution. |
| C10 | minor | checked-two-ways | not verified | Misere play is tame (quotient T2) for strips <= 8 and becomes wild at strip 9. The misere-Nim rule applied to normal Grundy values first fails at the positions {1,9} and {11}. |
| C11 | minor | computed-once | not verified | The partizan canonical form of the 3xn Dawson start diagram, as computed by cylcgt/dawson.py, is not *g(n). For example, flat n=5 gives * where g(5)=3, and flat n=7 gives *2 where g(7)=1. Outcomes still agree. The canonical form counts moves that global compulsory capture forbids, so the macro-move nimber is the right model. |

### How to reproduce each claim

- **C1**:

  ```
  PYTHONPATH=. .venv/bin/python -m dawson.quotient 32; dawson/misere_c 70 dawson/misere_c_70.bin; PYTHONPATH=. .venv/bin/python -m dawson.check_quotient dawson/quotient_Q32.pkl 70 dawson/misere_c_70.bin
  ```
- **C2**:

  ```
  PYTHONPATH=. .venv/bin/python -m dawson.octal 300
  ```
- **C3**:

  ```
  PYTHONPATH=. .venv/bin/python -m dawson.pawnboard 16 16; PYTHONPATH=. .venv/bin/python -m dawson.report_tables
  ```
- **C4**:

  ```
  PYTHONPATH=. .venv/bin/python -m dawson.octal 300
  ```
- **C5**:

  ```
  PYTHONPATH=. .venv/bin/python -m dawson.pawnboard 16 16
  ```
- **C6**:

  ```
  cc -O2 -o dawson/misere_c dawson/misere.c && dawson/misere_c 100; PYTHONPATH=. .venv/bin/python -m dawson.compare_misere 60 dawson/misere_c_60.bin
  ```
- **C7**:

  ```
  PYTHONPATH=. .venv/bin/python -m dawson.quotient 32
  ```
- **C8**:

  ```
  PYTHONPATH=. .venv/bin/python -c "from dawson.quotient import resume; resume('dawson/quotient_Q32.pkl', 33, 'dawson/quotient_run_33.txt')"
  ```
- **C9**:

  ```
  Read arXiv:math/0609825 (sections 1 and A.3) and arXiv:0705.2404 (Figure 1, Appendix C)
  ```
- **C10**:

  ```
  PYTHONPATH=. .venv/bin/python -m dawson.misere 45; PYTHONPATH=. .venv/bin/python -m dawson.quotient 12
  ```
- **C11**:

  ```
  PYTHONPATH=. .venv/bin/python -u dawson/run_cylcgt_dawson.py 7
  ```

## Bugs found

- Errors in prior_work/main.tex section 8:
- The rule as stated (1xn strip, remove a pawn whose neighbours are empty) allows no first move.
- The Grundy recurrence omits the end-file option g(n-2) and g(1)=1, so 270 of the 301 values n=0..300 are wrong.
- Ring predictions derived from it are wrong for 56 values of n<=300; e.g. 3x4 is predicted a first-player win but is a loss.
- The paper never mentions that Dawson's original question was misere. Replacement text: dawson/section8_corrected.tex.
- notes/dawson_small.txt is empty: 0 bytes, with no cylcgt.dawson process running at 22:54. The likely cause, an inference, is that the 900 s timeout killed `python -m cylcgt.dawson 8` before block-buffered stdout was flushed. n=7 alone takes about 150 s, so n=8 could not finish in 900 s.
- cylcgt/dawson.py prints partizan canonical forms of the diagram in its 'flat value' column next to the octal g(n). These differ (n=5: * vs 3; n=7: *2 vs 1) even though the outcomes agree, which invites a false 'contradiction' reading. The canonical form is the wrong object under global compulsory capture.
- RESEARCH_PLAN.md A6 suggests the misere ring 'may be tractable via misere quotients'. By the ring rule, the misere ring is exactly equivalent to a single misere strip of n-3, so it is no easier than the open strip problem.

## Open questions

- Is the partial misere quotient Q33(0.137) = Q34(0.07) infinite, as Plambeck-Siegel conjecture? My run did not converge but proves nothing.
- Are the misere single-strip outcomes of Dawson's chess eventually periodic? There is no sign of it up to n=100.
- Do Ferguson's note or miseregames.org already publish single-heap misere outcomes beyond heap 33, or the sequence of partial-quotient orders? Both were unreachable from here. If they do, the n<=100 table and the order sequence are not new.
- The exact journal citation of Plambeck-Siegel (J. Combin. Theory Ser. A 115 (2008)) and the Winning Ways chapter references were not re-checked.

## Next steps

- Save the report text from this summary as dawson/REPORT.md; the subagent was blocked from writing .md report files.
- Have a human (and a second model) review the ring-rule proof and dawson/section8_corrected.tex before replacing section 8 of the paper.
- Write a second, independent implementation (for example a different encoding, in Rust or C) of the exhaustive misere search for totals 61-100. This would upgrade the single-strip outcomes for n=61..100 to two implementations.
- To probe Q33: rerun dawson/quotient.py on an idle machine with a longer time budget, port its recalibration to C, or run Siegel's MisereSolver/CGSuite if installing it is approved. Treat any result only as evidence unless a finite quotient verifies.
- Optionally delete dawson/misere_c_70.bin (7.6 MB) and dawson/misere_c_60.bin (1.8 MB) once the checks no longer need them; *.bin is already git-ignored.
