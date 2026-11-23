HOLDS WITH FIXES

**PROVED** given C1 and C2. The two families have the outcomes of ∗3 against every finite nim-heap, at every claimed width.  
**PROVED.** TT can start its induction at width 20 with a changing seam neighbour. A far first move preserves six middle files. A far reply need preserve only the copied pair.  
**CHECKED-2.** Both reduced bases, both fixed-cut base steps, both strip seam censuses and every small-width whole-board signature agree across implementations.  
**CHECKED-2.** The optional interior TT base at width 22 and the direct width-20 signature also agree.  
**COMPUTED-1.** Only R tested the remaining cuts and compared the full TT strip and cylinder reduced graphs.

## Findings and exact replacement text

Line numbers for `PROOF.md` refer to `research/mobius_star3_family/PROOF.md`. “Note 5” means the corrected `dist/tog/supp_src/s15_note5.md`. No blocker. The first finding corrects a false assertion in the proof itself.

1. **PROOF.md:56 — MAJOR · PROVED.** “In every case files $c-2..c+3$ are untouched” incorrectly extends the first-move bound to the reply. In TT(5), White can push W2–3 on file 1, leaving a live position. Black can then push B4–3 on file 12. This is a far reply in (iii), with $12=c-2$. It changes file 12 alone. Note 5:73 actually says “so $c,c+1$ stay pattern files” for that reply. Also, *far* is a fresh partition in (iii), and the two far first-move sources at the arc endpoints themselves must be pattern files in the parent. Replace the sentences beginning “In every case” and “The far pawns” with:

   > After the far first move, files $c-2..c+3$ still have their pattern contents. If the child is live, replies from $c-1..c+2$ are near and cannot win immediately by Lemma 2(a). All other replies are far and have matching moves on the enlarged board. Such a reply can change a file of $c-2..c+3$, but it leaves $c,c+1$ intact, so insertion commutes with it and V3 compares its winner. The arc endpoints satisfy the parent pattern hypothesis. The exterior seam neighbour may vary from node to node.

2. **PROOF.md:11,54 — MINOR · PROVED.** The summary says nothing uses the contents outside the arc. A far pawn can read those contents, and they can decide a capture, a passer or the winner. V compares a position with its own image. Replace the last sentence of line 11 with:

   > The exterior neighbour may change between reduced nodes. At each node insertion preserves the actual contents on both sides of the seam and the reflected view across it (§2).

   At line 54 replace “files $c,c+1$ are pattern files and $c+1\le n-1$” with “$0\le c<c+1\le n-1$ and files $c,c+1$ are consecutive pattern files of one wall in its single phase”. Note 5:39 expressly requires “the same wall and follow its single alternating phase”.

3. **PROOF.md:24–25,29,93 — MAJOR · CHECKED-2.** The C3 row asserts success at *every cut tested*, contradicted even by R's own SS failures at line 80. The status of the seam census and of C1 at the end of the note predates the completed T87 run. At line 29, “gave the same graphs” suggests a cross-program comparison of node and edge identities. The report can compare R’s and T87’s statistics. T87 tests exact insertion *within* its implementation. Replace the C3 and S rows' claim and label cells with:

   > C3 | Insertion results by width and cut, including the SS failures in §4 | CHECKED-2 for TT(5), cut 14, and SS(6), cut 6. The remaining sweep is COMPUTED-1 (R).
   >
   > S | Seam move and arc censuses at the two strip bases | CHECKED-2 (R and T87). The TT strip/cylinder comparison of node sets, side-labelled K-children and T-counts is COMPUTED-1 (R). The cylinder counts have separate support in Note 4.

   At line 29 replace “gave the same graphs” with “reproduced both sets of C1 statistics and signatures”. Replace line 93 with:

   > C1 is CHECKED-2 at both bases. R and T87 use separate rules implementations and agree on the counts, zones, absence of flags and passers, and heap signatures. Each also checked its own rooted insertion isomorphism at the base cut. The computations share the same written rules.

4. **PROOF.md:94–95 — MINOR · PROVED.** The statement about the earlier random test's coverage goes beyond its log. Note 5:111 reports “2826 with the arc touching the seam”. The sampler chooses either endpoint and randomises the exterior (`research/mobius_rings_proof/lemma_test.py:42–50`). The counter pools the endpoints and records no statistic about exterior mobility along K-paths. The earlier referee's random test also sampled both ends (T82 report, “Adversarial insertion tests”). Replace the sentence beginning “Note 5's random test” up to “not stressed” with:

   > Note 5's family bases F1 and F2 use the left endpoint with a frozen seam neighbour. Its random test pooled the two endpoints. Here file 0 actually changes, while the TT(5) strip census found no crossing captures and only P pushes from file 19.

   At line 95, the first right-hand zone file is 12, but the zone also contains 0 and 1. At SS(6), cut 7 already has an arc meeting file 12 yet passes the graph test. Replace line 95 with:

   > At SS(6) the arc ends at 11, immediately before zone file 12. Among tested cuts with both copied files in the wall, precisely those whose copied pair meets the zone failed at steps $m=4,5,6$. Other cuts whose ten-file arc meets the zone can pass the finite test. The proof uses only cut 6 from $m=6$ onward.

5. **PROOF.md:26 — MINOR · COMPUTED-1.** The D test never calls `F.moves`. It iterates `A.moves`, compares both root passer lists, and compares passer lists and terminal adjudications on the resulting children. “Classes” could be read as the four reduced move classes. Note 5:109 describes its own D as “signatures of $G+\star h$, $h=0..3$, by U and by M2”; this is a different test. Replace the D row with:

   > D | On 2000 unflagged random roots tested on both surfaces, the two Board variants agreed on root passer lists and on passer lists and terminal adjudications at children generated by the original Board | COMPUTED-1, zero recorded mismatches. FBoard delegates move generation to Board and caches it. Note 5's D compared whole-game heap signatures using U and M2.

6. **PROOF.md:16,33,40,67 — MINOR · PROVED.** R names both a program and a game. The note uses $R_m$, K, T, “zone”, “flag” and the letters of a signature before defining them locally. “Far” has the two source ranges distinguished in finding 1. Note 5:37 distinguishes a side's “T-flag (has a T-move)” from an e.p. right. Append to line 16:

   > Let $\mathrm{start}_m$ be the displayed family word with its starting directions and no e.p. right, and let $R_m$ be its reduced game (Note 5 §1). For a given mover, T wins immediately, L loses immediately, P permits an immediate winning terminal reply, and K is any remaining move. The graph follows K-moves of either colour and stores K-children and the existence of a T-move separately for each colour. An unqualified pawn flag is an e.p. right. A signature lists outcomes in increasing heap size. N means the starter wins, P means the starter loses, and L means White wins with either starter.

   Replace the line 40 label “zone $Z_m$ (C1, C3)” with “proposed zone $Z_m$ (the union of files differing from the root across K-reachable nodes; finite rows in §4, propagation in §3)”. At line 67 replace “Induction on K-distance from the root” with “Insertion is injective by deleting the two copies. Since every old K-edge lifts and every K-edge out of an image lifts back, induction on path length from the corresponding roots”. This makes the reverse inclusion explicit.

7. **PROOF.md:90 — MINOR · PROVED.** Note 5:67 allows in Lemma 2(a) “a flag (if any) that protects a pawn of the player not to move”. Part (b) and Lemma 3 require an unflagged parent. Replace the final clause about H2/E2 with:

   > Their sampled reduced graphs include e.p.-flagged nodes, so the no-flag hypotheses of Lemma 2(b) and Lemma 3 fail there. Lemma 2(a) has its own flag condition. No all-width induction for these families is supplied.

## Why the induction works at the seam

**PROVED — V1–V3 (Note 5:59–61).** Fix a particular node or descendant at which the cut pair still has its pattern contents. The chart-edge neighbour lost by an old cut pawn is replaced by an identical copy. The old seam pair $(n-1,0)$ becomes $(n+1,0)$ with exactly the same contents, reflected ranks and reversed directions in the opposite view. This also transports a canonical right and its eligible capturers. A flagged stepper would be up on rank 4 or down on rank 5, so neither copied type-E pawn can duplicate the right. The two new pawns have chart neighbours of the opposite colour strictly ahead. By V2 and V3, only images of old pawns can be passed, with the same e.p. eligibility, own-file front status, race distances and tie outcome for the same mover. None requires file 0 at TT(5) to keep its *root* contents.

**PROVED — Lemma 2 (Note 5:67–69).** All central sources have a five-file chart window, including those in the enlarged wall. At the TT right extreme $j=18$, the reflected window is $15..19$. A replying capturer from 17 lands on 18 and sees 17,18,19. Its departure can remove a blocker only for files 16,17,18, and the pawn on 16 still sees its blocker on 15. A W double step in the wall can be taken e.p. and gives no White passer. The expiry of a permitted old flag in (a) can release only an opponent's pawn. The proof uses the content on 19 and the global hypothesis of no initial passer. It never asks for a chart-only view *centred* on 19.

**PROVED — Lemma 3 (Note 5:71–73).** Its bound is explicitly “$4\le c\le n-6$”. The parent arc has no internal twisted edge, even at equality. Part (i) excludes T and K from central sources $c-3..c+4$ and the enlarged $c-3..c+6$. In (ii) the old far first mover starts at or outside an arc endpoint. A straight move touches its file, a capture also touches the target file. Across the seam these are 0 and $n-1$, both far. The central six files survive and the child, including a fresh flag, commutes with insertion. In (iii), after a live first move the near reply sources are $c-1..c+2$ (enlarged $c-1..c+4$). Any new right protects the first mover's stepper. Lemma 2(a) excludes an immediate win by a near replier. Every far reply has a counterpart, and even an e.p. victim lies on the target file. The cut pair survives. V3 therefore preserves the existence of a winning terminal reply in both directions. This matches P and hence K as well as the immediate awards. The endpoint is justified by the lemma. S is optional evidence.

**PROVED — phase, roots and zones (PROOF.md:35–48,63–67).** Both walls alternate the single W2-up and B4-down tokens of type E. TT has B4 on even files and SS has W2 on even files. For each family the chosen cut is inside the wall with its successor from $m=3$. TT inserts old 15,14 as W2,B4 after 14. SS inserts old 7,6 as B4,W2 after 6. Each extends the word by one period with its tail intact. The stronger induction thresholds are different. TT needs $2m+9\ge19$, hence $m\ge5$, and its whole zone is left of the cut. SS's fixed wall run ends at $2m-1$, so $2m-1\ge11$ requires $m\ge6$. SS(5) has its arc inside the wall but its last two files in the zone. Under insertion SS fixes $\{0,1\}$ and shifts both $\{2m,2m+1\}$ and $[2m+3,2m+10]$ by two for $m\ge4$. This gives exactly the next prescribed zone. At the bases C1 establishes the invariant. Thereafter Lemma 3 matches the rooted K-paths of both colours and their T-flags in both directions. Every image retains absence of an e.p. flag, agrees with the new root outside the transported zone, and supplies an image witness for each previously changing file. A K-child is live by definition and V3 keeps the roots live. No property of an uncomputed larger graph is assumed.

**PROVED — range and meaning (PROOF.md:5–9,78,84–90).** The even direct widths are 12,14,16,18, followed by induction from 20. The odd direct widths are 11,13,15,17,19,21, followed by induction from 23. Every file is occupied and exactly one token, W6B7, contributes a second pawn. C1 and Lemma 1 give N,N,N,P at heaps 0 through 3 for the large roots. C2 gives the same outcomes for the small ones by direct whole-board search. Those cases need no assertion about flags at intermediate nodes. From any finite heap $h>3$ either starter can reduce it to 3, leaving the opponent to move in a P-position with the same pawn state. This proves N for every such $h$. It establishes the stated heap outcome equivalence in the e.p.-aware whole-board game with immediate passer awards, count races and ties against the mover. It supplies neither an arbitrary-addend comparison nor a canonical partizan value. Note 4 H7 restricts its cylinder claim to $h<256$; Note 5:63 expressly allows “every finite heap”. The immediate-terminal convention of Note 5 applies here.

## Finite comparisons

**CHECKED-2 for overlaps specified below.** T87's JSON lines 2–11 contain both sets of base, source, seam, last-file capture and insertion records. Lines 12–22 contain every scheduled whole-board case including the exception. The final usage record is present. Nothing expected from T87 is missing. The startup-only T87 report predates this run. K counts are per-side edges, T counts are winning moves before conversion to Boolean flags. Evidence keys below refer to the reproduction commands.

| Quantity | Note or author's log | T87 run_all.log | Assessment |
|---|---|---|---|
| TT(5), width 20, arc 10..19 | 1305 nodes / 4018 K / 1212 T. Flagged 0, passers 0. Zone {0,1,3..8}. NNNPN | Same, line 2 | CHECKED-2 · A,B |
| SS(6), width 23, arc 2..11 | 22755 / 72730 / 49694. Flagged 0, passers 0. Zone {0,1,12,13,15..22}. NNNPN | Same, line 7 | CHECKED-2 · A,B |
| TT seam and arc | Changed file 0 in 435 nodes, file 19 in 0. Arc deviations, K moves touching arc and crossing captures all 0. From 19, 1305 single and 1305 double pushes, all P, total 2610. From 0, single K/P = 323/982 | Same, lines 2–5 | CHECKED-2 · A,C |
| SS seam and arc | Changed files 0/22 in 16002/5170 nodes. Arc deviations and K moves touching arc 0. Crossings 0→22 and 22→0 = 1705 and 1640, all ordinary T | Same, lines 7–10. Of 5170 captures *from* 22, 3530 go to 21 | CHECKED-2 · A,C |
| SS endpoint source breakdown | From 0, single K/L/P/T = 5145/1705/5742/5115, captures K/P/T = 916/4199/1705. From 22, single K/P/T = 3530/14055/5170, captures T = 5170 | Same, line 8 | CHECKED-2 · A,C |
| Fixed-cut insertions | TT $5\to6$, $c=14$ and SS $6\to7$, $c=6$ pass | Lines 6,11. Roots and whole image sets agree, 1305→1305 and 22755→22755 nodes. All 2610 and 45510 side comparisons pass | CHECKED-2 · A,B |
| TT all-cuts sweep | $m=1..7$, every $c=10..2m+8$ passes. At $m=5$ only 14 is lemma-admissible | Only $m=5,c=14$ tested | COMPUTED-1 for remaining sweep. Admissibility follows by interval arithmetic · A,B |
| SS all-cuts sweep | $m=4,5,6$, pass $c=2..2m-2$, fail $2m-1,2m$. At $m=6$ only 6 is lemma-admissible | Only $m=6,c=6$ tested | COMPUTED-1 for remaining sweep. Admissibility follows by interval arithmetic · A,B |
| SS reduced node counts for $m=1,2,3$ and then $4..7$ | 18649, 28307, 24837, then 22755 at each sampled width | 22755 at $m=6,7$ only | CHECKED-2 on overlap, COMPUTED-1 on other displayed widths. Induction gives constant size for $m\ge6$ · A,B |
| C2 whole-board heaps 0..3 | TT $m=1..4$, SS $m=0..5$, all NNNP. TT(0) is LLLL | Same, lines 12–22 | CHECKED-2 with three agreeing full searches, M1, M2 and T87. R also gives NNNPN at TT $1..4$, SS $1..5$ · A,B,D |
| Extra whole-board rows | TT $m=5..11$, SS $m=6..10$, all NNNP from M1 and M2 | Outside T87's whole-board range | CHECKED-2 from M1/M2 · D |
| Cylinder controls | TT(5) matches its untwisted graph on all 1305 positions, K-children and per-side T-counts. SS(6) has 22755 strip nodes vs 40445 for its rotated cylinder word | T87 tests only strip positions | COMPUTED-1 for TT's graph identity. Note 4 independently reports the cylinder sizes and TT's 4018/1212 totals. Compare the *cylinder* words by rotation · C,E |
| Optional TT interior base | $m=6,n=22$, arc 10..19, 1305/4018/1212, 0 flags and passers, same zone, NNNPN. TT(5) direct NNNP | T87 line 6 counts 1305 target nodes but does not emit a target C1 census or direct TT(5) signature | CHECKED-2 for the complete alternative via the additional T88 run · B,D,F |

**PROVED.** For the zero K-touch count, T87's audited arc agrees with the root at every node, including every K-child. Any K-move entering, leaving or pushing on the arc would change a file there. R counts K-moves touching the arc directly. On TT file 19, the unchanged single W2 permits at most one push of each length per node. The two totals of 1305 therefore give one push of each length at every node. For the optional base, $n-1=21$ leaves files 20 and 21 beyond the arc. Moving width 20 to the direct cases removes the endpoint issue entirely.

## Reproduction and limits

Run from the project root. A–E retrieve the exact evidence used in the table without starting a search. The formulas and bounds can be checked against the numbered proof texts in G.

~~~sh
d=research/mobius_star3_family
l="$d/logs"
# A — complete independent records, including each endpoint census
nl -ba delegate/out/T87/run_all.log
# B — reduced graph rows and the cut-by-cut successes, failures and admissibility
cat "$l/fverify_TT.log" "$l/fverify_SS.log"
# C — seam/arc counts and the direct TT cylinder comparison
cat "$l/seam_check_TT5.log" "$l/seam_check_SS6.log" "$l/cyl_compare_TT5.log"
# D — both whole-board solvers at every stated width, one ring per invocation
cat "$l/confirm_TT_SS.log"
# E — independent cylinder results and rotation of the words
rg -n 'C1T|C1S|H7|T_n =' dist/tog/supp_src/s15_note4.md
# F — recompute the reply witness, fallback C1 and direct TT(5)
PYTHONPATH=. nice -n 15 .venv/bin/python -B delegate/out/T88/check.py
# G — exact lemma statements, random-test scope and underlying evidence
nl -ba "$d/PROOF.md"
nl -ba dist/tog/supp_src/s15_note5.md
cat "$l/fgame_test.log" research/mobius_rings_proof/logs/lemma_test_3_3000.log
nl -ba "$d/fgame_test.py"
nl -ba research/mobius_rings_proof/lemma_test.py
rg -n 'Sampling|ten-file run' delegate/out/T82/REPORT.md
~~~

To regenerate T87's figures with its original solver on a host granting the requested priority, run `PYTHONPATH=. nice -n 15 .venv/bin/python -B delegate/out/T87/check.py all`. To regenerate the author's table inputs with the same settings, the original commands below are serial. These longer searches were read from their logs in this review.

~~~sh
d=research/mobius_star3_family
run() { PYTHONPATH=. nice -n 15 .venv/bin/python -B "$@"; }
run "$d/fverify.py" TT 1 8
run "$d/fverify.py" SS 1 7
run "$d/seam_check.py" TT 5 14
run "$d/seam_check.py" SS 6 6
run "$d/cyl_compare.py" TT 5
run "$d/confirm.py" TT 0 11
run "$d/confirm.py" SS 0 10
~~~

**Scope of checking.** The current sandbox denied the niceness change. Only short, serial checks ran here at the inherited priority, including F using the T87 implementation. The report relies on the completed project run for the main independent bases. I did not compare the two implementations' full serialized graphs against each other, rerun the SS all-cuts sweep, repeat the random tests, or solve the cylinder controls afresh. I did not audit the separate H2/E2 families or search for a width-10 witness. No minimality or novelty result follows from this review.
