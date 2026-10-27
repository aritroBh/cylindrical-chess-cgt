# The whole-board Q family is $\star3$ for every even $n\ge8$

## Summary

1. **PROVED [AI], conditional on finite checks:** the insertion proof gives $Q_n=\star3$ for even $n\ge22$.
2. **CHECKED-2:** the $Q_{22}$ reduced graph has 7,968 nodes and signature NNNPN; two engines agree.
3. **CHECKED-2:** full-game signatures for even $n=8,\ldots,24$ are NNNP for $h=0,1,2,3$.
4. **COMPUTED-1:** an independent full-game run also checks $h=4$ and Lemma 2(b) on every $Q_{22}$ node.
5. Scope: whole-board game, race rule `count`, en passant on, and the e.p.-aware passed-pawn test.

## 0. Claims and labels

**PROVED** means a hand argument conditional on cited lemmas and finite checks; **CHECKED-2** means two independently written programs agree; **COMPUTED-1** means one program. The programs share the written rules, not implementation code.

| Claim | Status and evidence |
|---|---|
| T50 Lemmas 1–3 and the insertion detail in `PROOF.md` §2b | **PROVED** in T50; the generic insertion argument is reused here. |
| H1–H8 and the induction below | **PROVED [AI]** conditional on C1 and on the T50 lemmas. |
| C1: $R_{22}$ graph, zone, flags, and reduced signature | **CHECKED-2**: A (`rg.c`, saved `pump_Q_8_60.txt`) and E (`verify_compute/myeng.py`, rerun in `q/check_wall_q22.py`); E also checked no passer at every node. |
| C2: unreduced signature NNNP, $h=0..3$, even $n=8..24$ | **CHECKED-2**: A (`unreduced_Q_8_60.txt`) and F (`q/independent.py`). |
| F's $h=4$ result in both heap/e.p. interpretations; P8 control | **COMPUTED-1**. |
| Lemma 2(a),(b) on actual $R_{22}$ nodes | **COMPUTED-1**: E, 111,552 wall-pawn moves, zero failures. |

A is the saved C whole-board engine; E is the independently written Python engine in `verify_compute/myeng.py`; F has its own move generation and whole-board recursion and calls only `cylcgt.pawns.passed` for the passed-pawn predicate. B, `reduced_cyl.py`, rebuilds reduced graphs with `cylcgt`; its saved Q comparison stops at $n=8,10,12$, so it is **not** evidence for C1 at $n=22$ or for unreduced signatures. The pump log beyond $n=22$ is a one-program check and is not used in the proof.

## 1. Model and lemmas

The game is the whole-board normal-play game on $C_n$: White is Left, Black is Right, and a side with no move loses. Race rule is `count`; en passant is on, and an e.p.-capturable pawn is not passed. A passer ends the game; if both sides have one, compare their shortest promotion distances, with a tie won by the side that did not just move. The terminal score convention is $\pm256$, so heaps considered in the value statement have $h<256$.

For even $n\ge8$, the files of $Q_n$ are
\[
 W4,\ B7,\ (B4,W2)^{(n-8)/2},\ W3B6,\ W3,\ W2B5,\ B5,\ W2,\ B4.
\]
Thus $Q_8$ is exactly `W4 B7 W3B6 W3 W2B5 B5 W2 B4` (the repeated block is empty), and every $Q_n$ has $n+2$ pawns. A **pattern file** is a file whose content is exactly its starting pawn and nothing else.

Use T50's reduction and wall-pawn lemmas as stated in `research/ring_family_proof/proof.tex`; the exact-content pattern-file reading and the written-out insertion reply argument are in `PROOF.md` §§2–2b. Lemma 2(b) says that, with no flag and no passer at the position, a moving wall pawn with a five-file pattern window has only L or P moves. The Q wall has the opposite phase from P: W2 is on odd files and B4 on even files. The same local proof applies: W2 advances $2\to3$ or $2\to4$ (the latter is e.p.-capturable), and B4 advances $4\to3$; the adjacent opposite-colour wall pawn captures the advance, creating a passer unless the move is already L. The X pawn on $j+2$ remains blocked by Y's pawn on $j+3$; the reversed window is its mirror. Lemma 2(a) excludes a passer for the mover after every such advance.

For Lemma 3 at $c=9$, the required pattern arc is $5..14$. In $p$, files $6..13$ have five-file windows inside that arc; after insertion, files $6..15$ do inside the extended arc $5..16$. As in `PROOF.md` §2b, central moves are L/P, far moves preserve the same three-file views and passed-pawn set, far replies correspond, and near wall replies cannot give Y a passer by Lemma 2(a). Hence T-flags and K-children correspond under insertion. No second or “symmetric” arc is used.

## 2. Q hypotheses H1–H8

1. **H1 — Wall and pattern.** The periodic wall is files $2..n-7$: B4 on even files and W2 on odd files, with black two ranks above white. Pattern files require exact single-pawn content. The base graph has files $4..14$ fixed in every node; insertion preserves this, in particular $5..14$.
2. **H2 — Phase and the two relevant ends.** The ten-file arc for $c=9$ is $5..14$. At the two ends of the invariant pattern run, the applicable Lemma 2(b) windows are $4..8$ at $q$ on file 5 and $10..14$ at $q$ on file 13. On all actual $R_{22}$ nodes these windows hold; both cases and every intervening wall move were checked explicitly (C1). Lemma 3 invokes Lemma 2(b) only on central files $6..13$ (and $6..15$ after insertion), not at the physical wall endpoints 2 or $n-7$, where its five-file premise need not hold.
3. **H3 — No wall captures.** With pattern neighbors, a W2/B4 pawn's diagonal target on rank 3 is empty; B4 cannot e.p.-capture a W2 still on rank 2. Thus the wall moves in Lemma 2 are advances only. The lemma's L case covers any move after which Y already has a passer.
4. **H4 — Race and passed test.** This theorem uses `count` and the e.p.-aware passed test. The wall lemma gives no passer to the mover; insertion preserves passer identities, ranks, and e.p. protection on far moves, so it preserves the race result.
5. **H5 — Root and insertion.** The root has no passer: W4(0) is blocked by B7(1); B7(1) by W4(0); wall W2/B4 pawns by their adjacent opposite-colour wall pawns; W3B6, W3, W2B5, B5, and the closing W2/B4 pair by same-file or adjacent suffix pawns. It has no flag. For $n\ge22$, file 9 is W2 and file 10 is B4; inserting B4,W2 after file 9 extends the alternating block, so $\mathrm{ins}_9(\mathrm{start}_n)=\mathrm{start}_{n+2}$.
6. **H6 — Base zone and cut.** Take $n_0=22$, $c=9$. The base zone is $Z_{22}=\{0,1,2,3\}\cup\{15,16,17,18,19\}\cup\{21\}$. Files $5..14$ lie outside it and are exact pattern files. The bound is the first even $n$ for which $c+5=14\le n-7$.
7. **H7 — Inductive invariant.** Let $Z_n=\{0,1,2,3\}\cup\{n-7,\ldots,n-3\}\cup\{n-1\}$. Every node of $R_n$ has no passer or flag and agrees with its root outside $Z_n$. C1 gives this at $n=22$. If it holds at $n$, Lemmas 2–3 apply on $5..14$; H5 maps the root, and insertion maps every K-edge and T-flag. Since $\mathrm{ins}_9(Z_n)=Z_{n+2}$, the invariant holds at $n+2$ and $R_{n+2}$ is isomorphic to $R_n$ with T-flags.
8. **H8 — Meaning of $Q_n=\star3$.** It means that for every nim heap $\star h$, $h<256$, $Q_n+\star h$ and $\star3+\star h$ have the same outcome; it does not claim equivalence against arbitrary addends. It suffices to show NNNP at $h=0,1,2,3$: for every $h>3$, the move $\star h\to\star3$ reaches the P-position $Q_n+\star3$, so the sum is N, as is $\star3+\star h$. The root has no flag; the reduced nodes and K-children have none, so the heap-move e.p. convention does not affect this argument.

## 3. Finite checks and theorem

**C1 (CHECKED-2).** $R_{22}$ has 7,968 nodes, 21,063 K-edges, 17,784 T-edges, no flags, and zone $Z_{22}$; A and E agree on the graph and its NNNPN signature for $h=0..4$. E checked that no node has a passer and checked all 7,968 nodes and 71,712 q/node positions: 111,552 moves, zero Lemma 2(a) violations and zero Lemma 2(b) T/K violations. In particular, file-5 moves classify L/P as 5,691/10,245 and file-13 moves as 414/15,522. These end counts make the two boundary-window checks explicit.

**C2 (CHECKED-2 / COMPUTED-1).** A's saved unreduced log and F agree on NNNP for every even $n=8..24$. F additionally computes $h=4$ and both e.p.-across-heap readings (`keep`, `expire`): NNNPN for each of those nine sizes. The control $P_8$ is NNPNN in both readings, so it is not $\star3$ (its P is at $h=2$). The $h=4$ row and the control are COMPUTED-1 by F.

**Theorem (PROVED [AI], conditional on C1–C2 and T50 Lemmas 1–3).** H7 gives the same reduced game and T-flags as $R_{22}$ for every even $n\ge22$, so C1 and Lemma 1 give NNNP. H8 completes the heap comparison. For $8\le n<22$, C2 gives NNNP directly and H8 again completes it. Therefore $Q_n=\star3$ for every even $n\ge8$ in the stated whole-board model.

**Reproduction, from the project root:**

```sh
PYTHONPATH=. .venv/bin/python -u research/ring_n_plus_2_check/q/check_wall_q22.py
/usr/bin/time -l nice -n 15 env PYTHONPATH=. .venv/bin/python -u research/ring_n_plus_2_check/q/independent.py
```

The cited A outputs are the pre-existing `research/ring_n_plus_2_proof/logs/pump_Q_8_60.txt` and `unreduced_Q_8_60.txt`; their original reproduction command is `sh research/ring_n_plus_2_proof/run_all.sh` (not run here because it writes outside `q/`). `reduced_cyl_Q.txt` is only a reduced-graph comparison for n=8,10,12 and is not used for the claims above.

## 4. Referee (T62)

**Verdict: SOUND**, conditional on the finite computations C1–C2 and the cited T50 lemmas. No transfer gap remains for the even Q family at cut $c=9$ and base $n_0=22$.

**Recomputed:** the Q22 reduced graph and signature with E; Lemma 2(a),(b) on all 7,968 actual nodes, including both boundary windows; the full-game signatures $h=0..4$ for Q_n, even $n=8..24$, in both e.p. heap modes; and P8 as a non-*3 control.

**Changed:** replaced the “by inspection” window claim with explicit windows and actual-node counts; removed the unnecessary symmetric-arc assertion; corrected Q8's definition; separated reduced-graph evidence from unreduced signatures and marked B's limited range; stated H1–H8 and the exact meaning of $=\star3$; corrected labels and added exact reproduction commands.
