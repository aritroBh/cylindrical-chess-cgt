HOLDS WITH FIXES  
**PROVED** — F1 and F2 for every $m\ge1$, and F3 for every $m\ge0$, have the outcomes of $\star 2$ against every finite nim-heap under the stated whole-board rules.  
**PROVED** — The ten-file insertion and the original cuts work. Specify one alternating wall in the view lemma and make the root and race conventions explicit in the reduction lemma.  
**CHECKED-2** — Every base statistic agrees. Independent unreduced minimax also matches the published signatures through $m=13$, including both exceptions at zero.  
**COMPUTED-1** — All 3,000 ten-file insertion tests passed. With the cut still admissible, shortening just the wall to four files produced four counterexamples in 96 tests.

## A. Hand referee

Line references are to `research/mobius_rings_proof/PROOF.md`. File indices start at zero. The rules used throughout are the e.p.-aware passed test, a canonical flag that survives a heap move, and the count race rule. A passed pawn ends the game immediately, including when a heap remains.

**PROOF.md:33–41, 59–61 — View lemma V. CORRECT WITH A FIX (PROVED).** The two copied files must be consecutive files of **one** alternating wall, including its phase. Reading “pattern files” separately is insufficient. For example, `B4 W2 | W2 B4` consists of two exact E walls. Cut between the whites. Each white originally sees a black ahead. After insertion both new whites see only whites and are passed. The executable self-check includes this witness. At line 39, append the following sentence, which also settles the use of “pattern files” in Lemma 2.

> In a hypothesis on consecutive pattern files, all those files belong to the same wall and follow its single alternating phase, with exactly the stated pawn and direction on each file.

**PROOF.md:59–61 — V1–V3 under that reading (PROVED).** Compare views in local coordinates with the flag transported to the image of the stepper. At either cut edge the replacement neighbour has the old neighbour's colour, rank and direction. The seam retains its twist. A flagged pawn can only be up on rank 4 or down on rank 5. None of the four pattern tokens can be that stepper, so a copy cannot duplicate a flag or replace a flagged neighbour across the cut. The new pawns each have an enemy strictly ahead on each neighbouring file. “Blocked” here concerns passed status. The old passers retain their ranks, directions and entire own-file contents. This preserves eligibility as a front pawn, both minimum race distances, and the tie decision for a fixed mover.

**PROOF.md:37, 63–65 — Lemma 1. CORRECT WITH A FIX (PROVED).** The reduced-node definition gives options and T-flags but does not specify a payoff at an already-terminal root. For example, a lone white pawn already wins for White even with heap zero. Treating its terminal root as an empty ordinary node gives P. A tied race also needs the identity of the mover who created it. All roots used in the induction are live. Replace line 63 with:

> **Lemma 1 (reduction).** For every non-terminal pawn root $g$, every finite heap $\star h$, and either player to move, that player wins $g+\star h$ if and only if that player wins $R(g)+\star h$. An already-adjudicated terminal root keeps its assigned winner for every heap.

At line 65, replace “A T-move wins (the game ends, the holder of the passer wins whoever moves). An L-move loses.” with:

> A terminal pawn move ends the whole game immediately. If just one colour has a passed pawn, that side wins. If both do, the count rule decides, with ties going to the opponent of the mover. Thus a T-move wins for its mover and an L-move loses for its mover.

**PROOF.md:65 — Reduction argument (PROVED).** A P-option gives the opponent a winning terminal reply at every heap size. It can be discarded along with L-options. Induct on the sum of the heap size and all pawns' remaining single steps to their directional promotion edges. A capture across the seam reduces the capturer's remaining distance by one because rank and direction flip together. Removing the victim cannot increase the sum. Every remaining pawn or heap option strictly decreases the measure, and the retained heap option carries the same flag in both games. The argument preserves the two first-mover win tests.

**PROOF.md:67–71 — Lemma 2(a,b). CORRECT (PROVED), with “pattern files” as specified above.** Write $s=+1$ for the window from $j-1$ to $j+3$, and $s=-1$ for its reflection. In the following table the reply starts on file $j+s$ and lands on file $j$. It is played only if the first move leaves a live board.

| Wall | Move on $j$ | Reply | Victim's rank |
|---|---|---|---|
| E | W2–3 | B4 takes on 3 | 3 |
| E | W2–4 | B4 takes e.p. on 3 | 4 |
| E | B4–3 | W2 takes on 3 | 3 |
| O | B7–6 | W5 takes on 6 | 6 |
| O | B7–5 | W5 takes e.p. on 6 | 5 |
| O | W5–6 | B7 takes on 6 | 6 |

**PROOF.md:69–70 — Before the reply (PROVED).** The mover's ordinary diagonal destinations are empty. E.p. onto rank 3 would require an up-stepper on 4 in a neighbouring file. Neither a down B4 nor a W2 is such a stepper. The O case reflects ranks and directions. No enemy moves on a straight step. A previous flag, if allowed by (a), protected the enemy, so its expiry cannot release a friendly passer. A single step leaves an enemy strictly ahead. After a double step the skipped square is empty and an adjacent enemy can take there. The canonical flag protects the stepper. Thus the mover has no passer in each case. A newly passed opponent ends the game with L before any reply is required.

**PROOF.md:71 — After the reply (PROVED).** The landing file contains just the capturer. Its neighbouring files contain one friendly pawn and an empty file. No flag survives a capture. Hence the capturer is passed. The departure from $j+s$ can remove a blocker only for an enemy on $j,j+s,j+2s$. The first two now contain no such enemy. The pawn on $j+2s$ still has its enemy on $j+3s$ strictly ahead. The arrival can only add an enemy blocker, and the only potentially flag-protected first mover was the captured stepper. Therefore the reply gives exactly one passed colour. This argument proves both orientations even when the *end* of the window touches the seam. All edges used for the reply and the surviving blocker are chart edges.

**PROOF.md:73–79 — Lemma 3(i–iii). CORRECT (PROVED).** The following are inclusive file intervals. Taking complements in the relevant board gives the far sources in each row.

| Side and stage | Central or near sources in old board | Far sources in old board | Central or near sources after insertion | Far sources after insertion |
|---|---|---|---|---|
| First mover | $[c-3,c+4]$ | $f\le c-4$ or $f\ge c+5$ | $[c-3,c+6]$ | $f\le c-4$ or $f\ge c+7$ |
| Reply after a live far move | $[c-1,c+2]$ | $f\le c-2$ or $f\ge c+3$ | $[c-1,c+4]$ | $f\le c-2$ or $f\ge c+5$ |

**PROOF.md:76–77 — First move (PROVED).** The right-extending window covers central sources from $c-3$ through $c+2$, the left-extending one from $c-1$ through $c+4$. Their ranges overlap. The enlarged chart arc supplies the same windows through $c+6$. Lemma 2(b) discards these moves. From a far source, a straight move changes one file, a capture its source and destination files. Even for e.p. the victim and landing square share a file. Across the seam the affected pair is exactly the two board ends, both far. Thus the old middle $[c-2,c+3]$ survives, and so does its enlarged counterpart $[c-2,c+5]$. No e.p. capture is possible on this first move because the parent is unflagged. A fresh double step has corresponding capturers, since its source and possible capturers are away from the cut. Copying and moving therefore commute for both the board and its flag. V3 preserves terminal adjudication.

**PROOF.md:78–79 — Reply (PROVED).** Each near reply has its three-file view inside the surviving pattern. Its only possible incoming flag protects the other side. Lemma 2(a) excludes a passer for the replier, hence also a terminal win for that replier. A far reply in the old board changes only files $f\le c-1$ or $f\ge c+2$, and its image changes only $f\le c-1$ or $f\ge c+4$. Neither the original cut files nor their copies are touched. An e.p. reply has its victim on the first mover's double-step file ($f\le c-4$ or $f\ge c+5$). Its source is adjacent, hence far, including when that edge is the twisted seam. The flag expires on an ordinary move or capture and is transported if a new double step sets one. All corresponding replies commute with insertion, apart from the near replies already excluded from terminal wins. Consequently a live first move is poisoned on exactly the same side of the correspondence. Both partitions in the table exhaust the board.

**PROOF.md:55, 76–78, 88, 146 — Cut at the seam end. CORRECT (PROVED).** At $c=4$, file 0 is far as a first source. Its full view is compared only with its *twisted* image view. For a window starting at 0, an interior pawn may use the *content* of file 0 on a chart edge. This does not require file 0's other neighbour to be a chart neighbour. In particular a central pawn on file 1 can use files 0 through 4 and reply from file 2. A far capture between 0 and the last file leaves files 4 and 5 intact. There is no need to move the cut or enlarge the base.

**PROOF.md:85–97 — Start, invariant and induction step. CORRECT (PROVED, finite base CHECKED-2 below).** In F1/F2 the inserted pair following file 4 is W2, B4. It adds one period to the prefix, pushes the suffix right by two and carries the zone $[2m,2m+5]$ to $[2m+2,2m+7]$. In F3 the inserted pair following file 10 is W5, B7. It extends the middle block, leaves the zone $[0,5]$ in place and shifts the final two-pawn file intact. For $m\ge5$ each full arc is outside its zone. Every reachable old node is live and has its original pattern there by the invariant. Starting at the corresponding roots, lift any old K-path edge by edge for one inclusion. For the reverse inclusion, every K-edge from an image is supplied by Lemma 3, so a new K-path cannot leave the image. Deleting the two copies recovers each old node. Images have no flag, their unchanged exterior files match the new root, and so do the two copied files. This proves the new invariant as well as the rooted, side-labelled graph isomorphism with T-flags.

**PROOF.md:130–140 — Theorem and large heaps. CORRECT (PROVED).** The finite checks give N, N, P for heaps 0, 1, 2 in the theorem's parameter ranges. For every $h>2$, either player can reduce the heap to 2 while leaving the pawn board fixed. The opponent then moves first at the same pawn board in a P-position and loses. This proves the claimed signature for all heaps, including arbitrarily large ones. The theorem specifies comparison against nim-heaps in this immediate-terminal whole-board game.

## B. Independent reduced graphs

**PROOF.md:25, 101–109 — C1, CHECKED-2.** For each row **all seven entries agree** with the published result. K-edges and T-moves count legal moves over all distinct live source positions and both choices of mover. A T-flag is the Boolean existence of a T-move for one side at one node. The zone is the union of files whose pawn contents, including directions, differ from the root in at least one node.

| Family at $m=5$ | Nodes | K-edges | T-moves | Flagged nodes | Nodes with passer | Zone (inclusive) | $R+\star h,\quad 0\le h\le4$ |
|---|---:|---:|---:|---:|---:|---|---|
| F1 | 435 | 1118 | 404 | 0 | 0 | 10–15 | NNPNN |
| F2 | 417 | 1082 | 356 | 0 | 0 | 10–15 | NNPNN |
| F3 | 435 | 1112 | 428 | 0 | 0 | 0–5 | NNPNN |

**PROOF.md:103–109 — Extended reduced check, CHECKED-2.** Every entry below agrees through $m=7$. Every row has zero flagged and zero passed nodes. This table and the base table give the full requested range without interpolation.

| Family | $m$ | Nodes / K / T | Zone | Heaps 0–4 |
|---|---|---|---|---|
| F1 | 0 | 411 / 944 / 476 | 0–5 and 7 | RNRRR |
| F1 | 1 | 453 / 1154 / 452 | 2–7 | NNPNN |
| F1 | 2–7 | 435 / 1118 / 404 | $2m$–$2m+5$ | NNPNN |
| F2 | 0 | 452 / 1172 / 456 | 0–5 | NNRRR |
| F2 | 1 | 441 / 1128 / 428 | 0 and 2–7 | NNPNN |
| F2 | 2–7 | 417 / 1082 / 356 | $2m$–$2m+5$ | NNPNN |
| F3 | 0 | 453 / 1148 / 476 | 0–5 | NNPNN |
| F3 | 1–7 | 435 / 1112 / 428 | 0–5 | NNPNN |

**PROOF.md:33–37 — Method (COMPUTED-1).** The independent checker stores four square bitsets and the capturable stepper's square. It constructs the mirrored diagonal and ahead squares directly from coordinates. A traversal with a stack starts at the root, tries moves for either colour, tests the actual terminal winner, and scans legal enemy replies to classify live children. Only K-children enter the traversal. A separate win recursion uses the recorded K-children, T-flags and heap moves. This work used the two named rules texts without reading, importing or executing any solver from the Möbius rings directories.

## C. Independent unreduced game

**PROOF.md:26, 103–107, 114–122 — CHECKED-2 for the signatures.** Each range in the table was evaluated at every integer. The separate minimax evaluates legal pawn and heap options directly with the same geometry and terminal adjudicator as part B. It short-circuits on a winning option, including an immediate terminal win. It never calls the K/L/P/T classifier or consults the reduced graph. The comparison is with the published results, including the published reduced signatures for the larger widths.

| Family | $m=0$ | Every $m=1..13$ | Heap range |
|---|---|---|---|
| F1 | RNRR | NNPN | 0–3 |
| F2 | NNRR | NNPN | 0–3 |
| F3 | NNPN | NNPN | 0–3 |

**PROOF.md:116–120 — Interpretation (CHECKED-2).** Both exceptional zero-parameter starts agree with the reference and lie outside their respective theorem domains. F3 includes its zero-parameter start. N means either first player wins, P either second player wins, and R Black wins with either choice of first player.

## D. Adversarial insertion tests

**PROOF.md:73–79, 126 — COMPUTED-1.** The ten-file run tested 3,000 distinct (board, cut) pairs on 2,993 distinct boards. Of these, 751 boards allowed at least one legal capture across the seam at the sampled root, and 2,651 pairs had an arc touching a chart end. **Zero failures.** Each test compared the full sets of K-child positions after insertion, including direction and flag, and the Boolean T-flag separately for each mover.

**PROOF.md:73 — Sampling (COMPUTED-1).** The seeded generator chooses an admissible ten-file chart interval, favouring intervals touching either end. It picks the wall type and phase and randomises the exterior with empty files or up to three pawns per file on distinct ranks 2–7, allowing either colour and either direction. It rejects passed roots and starts without a flag. The sample is biased toward seam cases and is not exhaustive.

**PROOF.md:73, 126 — Short-wall controls (COMPUTED-1).** The primary control retains the original width and cut bounds and randomises everything except the four central alternating files. It found four failures among 96 distinct boards, 25 seam-capture-capable. An exploratory control instead let the four-file window itself touch an end. It found four failures among 96 distinct boards, 22 seam-capture-capable. All failures are listed below. In each case exactly one old K-child image was absent, no additional K-child appeared and both sides' T-flags agreed. The named side made the missing move. The complete positions are in the two control result files, indexed by sample number.

| Cut rule | Sample | $n$ | $c$ | Missing old K-move (old file) | T-flag of that side, both boards |
|---|---:|---:|---:|---|---|
| Admissible | 2 | 10 | 4 | White 5–6 (5) | yes |
| Admissible | 14 | 10 | 4 | White 5–6 (5) | yes |
| Admissible | 30 | 10 | 4 | Black 4–3 (4) | yes |
| Admissible | 90 | 12 | 4 | Black 4–3 (5) | yes |
| Unrestricted | 12 | 10 | 1 | Black 4–3 (1) | yes |
| Unrestricted | 15 | 10 | 1 | White 5–6 (1) | yes |
| Unrestricted | 50 | 10 | 1 | White 5–6 (1) | yes |
| Unrestricted | 67 | 10 | 1 | Black 4–3 (2) | no |

**PROOF.md:76–79 — One failure in detail (COMPUTED-1).** Admissible sample 2 is `- w5 W2B3 W5 B7 W5 B7 W5b3 W2w7 -`, cut at 4. Lowercase marks a pawn moving opposite its colour's initial direction. White's old file-5 advance to rank 6 is K. On the enlarged board the same old pawn advances on file 7. The new black pawn on file 6 then captures it on file 7 at rank 6 and wins immediately. The old child also changes a file being copied, so copying after the old move differs from moving once after copying. This is precisely the central move the longer wall excludes from K.

## Reproduction and limits

From the repository root run the following commands sequentially. The script uses only the standard library, bounds its search caches and sets a 44-minute deadline per invocation. The runs requested niceness 15. This sandbox denied the priority adjustment and executed the programs at inherited priority.

```sh
export PYTHONPATH=.
p=delegate/out/T82/referee.py
nice -n 15 .venv/bin/python -B "$p" selfcheck
nice -n 15 .venv/bin/python -B "$p" reduced 0 7
nice -n 15 .venv/bin/python -B "$p" full 0 7
nice -n 15 .venv/bin/python -B "$p" full 8 13
nice -n 15 .venv/bin/python -B "$p" attack 10 3000 82
nice -n 15 .venv/bin/python -B "$p" attack 4 96 82
nice -n 15 .venv/bin/python -B "$p" attack 4 96 82 --unrestricted-cut
```

The reduced and full commands reproduce B and C. The attack commands reproduce D, printing each failing board, the per-side counts of missing and additional images, and the missing old moves as (source file, source rank, target file, target rank). The self-check includes the out-of-phase example for V, a seam-crossing e.p. capture and a tied race. The output files beside this report preserve the computed data.

**PROOF.md:27, 110, 112, 124, 138–140 — Scope.** This review covers the stated cuts, model and heap comparisons. I did not rerun the all-cuts graph-isomorphism sweep, the cylinder control, the original random sample, other terminal conventions or tests against arbitrary partizan addends. Parts B and C share one new move generator. The second implementation for CHECKED-2 is the previously reported one. The proof uses the finite graph checks and induction. The random attack is supporting evidence only.
