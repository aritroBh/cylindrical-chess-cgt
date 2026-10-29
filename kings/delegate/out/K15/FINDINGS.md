# K15 FINDINGS: over-type and dud-type king groups on the cylinder (Conjecture 4.7, open question 2)

## 1. Summary and scope

**Summary (5 lines).**
1. **Classifier and Z_B.** The exact classifier `grp.c` (own move generator, exact local game of model P with real kings) labels Z_B `Kb2 ka4 Pa3 Pb4 pb3 pc4` **dud** at all four king states on flat 7×6 (plain P; PROVED by K27 for the board, CHECKED-2 here for the values); the brief's one-ply tests label it "other", because none of its 26 losing deviations is an immediate event (they lose in 3 to 11 plies) and the one-ply shuttle test also accepts 12 of them; the brief's own filter ("no passer at the root") rejects Z_B, whose four pawns are all passed pawns for `cylcgt.passed`.
2. **Search.** 80 census runs, 20 ranges: cyl:8×6 and 7×6 with 3 files ≤ 4+4, 4 files ≤ 3+3 and 5 files ≤ 3+2, cyl:8×8 (3 files ≤ 3+2, 4 files ≤ 2+2), cyl:7×7 and 8×7 (3 files ≤ 3+2), flat 7×6, up to 105 million roots a run, root passers excluded and allowed, plain P and free passes (all counts in section 5.1; cyl:8×8 3 files ≤ 3+3 and 4 files ≤ 3+2 need over 4 GB and were not run). **Over and under: 0 roots in every run.** The OpenCode classifier could never output dud (its shuttle test needs a frozen opponent) and so is no evidence.
3. **Open question 2: yes, dud groups without a pawn break exist on the cylinder.** G8a `Kb2 kc4 Pa3 Pe2 pa4 pe3` and G8b (one rank up), cyl:8×6, 5 files, two blocked pairs, no pawn move at all, no root passer: dud also against free passes; exactly two-shuttle in P (CHECKED-2: `kp_p`, `ref3m`, `grp`) and in chess (kpsolve cap 2, exact, COMPUTED-1); equal to dud_D beside 1,296 context positions (exhaustive file g) and 640 random ones in P (COMPUTED-1; CHECKED-2 on a 50-position sample), and in 5 of 6 chess contexts at cap 1 (the sixth is undecided for one side to move). Distinct dud groups found (up to symmetry): 43 on cyl:7×6, 40 on cyl:8×6, 25 on cyl:8×8; the ones that are dud only in plain P (Z_B family, D2, D2m) are not two-shuttle in chess (D2, D2m: 52 of 108 P-losing deviations draw in chess).
4. **Conjecture 4.7: no over group found; the second half has no support.** No structural over or under root in any range; an independent tempo-signature census finds no over signature on 3 files ≤ 3+3 and 20 candidate roots on 4 files ≤ 2+2 (all refuted beside contexts); of the near-over groups (12 on cyl:7×6, 12 on cyl:8×6, 4 on cyl:8×8, 1 each on 7×7 and 8×7) all are refuted beside contexts except one placement on cyl:7×6 whose window leaves no context file (its cyl:8×6 twin is refuted). The most persistent survivor, `Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4` (cyl:8×6 and 7×6), agrees with over_D at 130 of 130 positions on the far context file g (cyl:8×6) and fails 3 of 130 on the near file f (CHECKED-2 for one failure); it has no Black king shuttle. All COMPUTED-1 within the stated boundary (empty-context local game, kings on the group files at the root, no officers, the ranges above).
5. **Edits.** `K15/EDITS.md` replaces the old one: Conjecture 4.7 and its status row, §8 item 2, the Appendix A "Group search" bullet, and four consistency edits (§3.2′ text, §5.7 cylinder bullet, status row 3.2′, §7). Everything about Z_B stays as LOOPY has it (exactly two-shuttle in P on flat 7×6, PROVED by hand; chess open).

**Which files are whose.** `K15/fin2/` is the tree of the previous attempt of this item (scripts, census runs, confirmation runs, chess runs, draft sections), reused after the audit of section 3; `K15/r3/` holds what this attempt rebuilt and added (binaries, re-runs, second-solver checks, the Z\* tests, the chess runs on D2, D2m and Z\*, the notrun root checks); `K15/final/`, `K15/v2/`, `K15/f3/` and the files in the root of `K15/` are older attempts, used only where cited. Where a number below comes from the earlier tree, the reproduction command is in section 9 and this attempt re-ran the cheap ones (section 7.5). Sections 2 to 6 were drafted in `fin2/body_*.md` by the previous attempt and were audited and corrected in this one; where they say "the earlier attempt" they mean the attempts before `fin2/`. Labels: PROVED / CHECKED-2 / COMPUTED-1 / CONJECTURE; solver results are never PROVED.


## 2. The classifier: the tests, exactly

Two classifiers were built. Both have their own move generators (neither reads `kings/kpsolve.c` or `cylcgt`, except that the root-passer filter is checked against `cylcgt.pawns.passed`).

### 2.1 The exact classifier `grp.c` (used for every count below)

*Local game.* The board is W×H, a cylinder (the files wrap) or flat. Only the group's pieces stand on it, no context. The model is P of LOOPY: the first promotion wins; checkmate loses for the mated side; stalemate is a draw; e.p. is as in chess; infinite play is a draw. The pawns stand on the files a..F (F = 3, 4 or 5) and on the ranks 2..H−1, at most w White and b Black pawns. At the root both kings stand on the files a..F, on any rank, never adjacent, and no pawn attacks a king. The value V(x, s) in {win, loss, draw} for the side s to move is solved exactly by retrograde analysis over all king squares of the whole board (a king may leave the files a..F), layer by layer over the pawn sets (a layer is a pair of pawn sets; a pawn move or a capture leaves the layer).

*Two readings.* They differ only in whether passing is a move.
- **B (plain P, `--nopass`).** No passes. This is the test that K14 and K27 used for Z_B: every non-shuttle move must lose by force in P.
- **A (free passes, the default).** Both sides may pass when not in check. This is the game Z ⊞ dud_D of Theorem 3.4(a). A deviation counts as a suicide only if it loses although the deviator may pass at will (the punisher may pass too). A is the stricter reading of "decisively punished" (Definition 2.5). It is not nested in B in the corner case of a stalemate (in B a stalemated deviator draws), which never decided a label here.

*Kinds of a Z-move.* A Z-move is a king move or a pawn move; a pass is not a Z-move. Let m be a Z-move of the side s from y to y′.
- *suicide*: V(y′, s̄) = win for s̄ (the move is decisively punished in the local game);
- *winning*: m promotes, or V(y′, s̄) = loss for s̄;
- *safe*: otherwise (V(y′, s̄) = draw).

*Labels of a root x* (the first test that applies):
1. **check**: a king is attacked by a pawn at x, or at a state of the closure below;
2. **threat**: some side has a winning move at x;
3. **frozen**: neither side has a safe move at x (every Z-move is a suicide);
4. **on** (White passes): in the closure C of x under White's safe moves every state has at least one White safe move and no Black safe move, and no check, no winning move, no *leak* (a leak is a safe king move to a file outside a..F). **off**: the mirror;
5. **dud**: in the closure C of x under the safe moves of both sides every state has at least one safe move for White and at least one for Black, no check, no winning move, no leak. The size of C is at most 6000 (never reached);
6. **over** (Black passes): the A-states (every state reached from x by Black's safe moves) have at least one Black safe move and at least one White safe move; every Black safe move leads to an A-state; every White safe move leads to a Z-state, which has no safe move for either side and no check, winning move or leak. **under**: the mirror;
7. **leak** / **mixed**: everything else.

*Self-check.* In reading A every root labelled frozen, on, off, dud, over or under must have V = draw for both sides to move (0 violations in every A run). In B the frozen roots can be zugzwangs, so the check is not used.

### 2.2 The one-ply classifier `scripts/oneply.py` (the brief's tests)

It is the classifier the brief asks for, kept to test the regression.
- *imm(s, y)*: side s, to move at y, has an immediate decisive reply: a promotion, or a move after which s has a passed pawn (`cylcgt.passed`, e.p. ignored at the roots tested) and the other side has none.
- *suicide*: the Z-move leads to y′ with imm(opponent, y′).
- *safe shuttle*: a non-capturing king move u→v with u, v on the group files, legal, such that the move v→u is legal at the next turn and the position after u→v is not a suicide.
- *frozen*: every Z-move of the side is a suicide.
- Labels: frozen, on, off, dud, over, other. dud needs a safe shuttle for both sides and every other Z-move of either side, at every state of the closure under the shuttles, to be a suicide.

## 3. Audit of the tests against the brief and LOOPY

**What the brief asked and what was done.**
- The brief asked for one-ply tests. `oneply.py` implements them. The counts use `grp.c` instead, because the one-ply tests cannot label Z_B (section 4).
- The brief asked for roots without a passer (`cylcgt.passed`). `grp.c` has that filter (variant "strict", root passers excluded) and the unfiltered variant (root passers allowed). The filter in the C code skips exactly the layers in which `cylcgt.pawns.passed` holds for either side: 3,862 of 4,578 layers (flat 7×6, 3 files, ≤ 2+2), 38,372 of 43,298 (cyl:8×6, 3 files, ≤ 3+3) and 61,224 of 66,312 (cyl:8×6, 4 files, ≤ 3+2) (CHECKED-2: `scripts/passer_layers.py` against the counts printed by the C code; and 0 differences between the C-style test and `cylcgt.passed` on 160,000 random pawn sets, `scripts/passer_check.py`).
- Both kings are placed on the group files; the closure then explores the other king squares. A safe king move off the files is a leak and the root is "other".

**The filter is what hid Z_B.** All four pawns of Z_B are passed pawns for `cylcgt.passed` (Pa3 and Pb4 for White, pb3 and pc4 for Black), blockaded by the kings. The filter rejects Z_B and every other group of its kind.

**Defects of the earlier searches.**
- The OpenCode classifier (`K15/classify.py`, `search.py`; the same kind of test as the Appendix A scratch search). Its `has_safe_shuttle(pos, side)` first requires `opponent_frozen`, which is false whenever the opponent has a reversible king move. So a side has a safe shuttle only if the other side has none, and `ws and bs` (the dud test) can never hold: the class dud was unreachable by construction. Its over test counted only White king moves that freeze, and skipped pawn moves ("hard; skip for now"). Its "no dud and no over" is therefore no evidence. The same holds for Appendix A, "Group search", which used one-ply tests of this kind.
- The K14 search used the move-count cut-off 18 (already withdrawn in LOOPY).

**Mapping of the labels to LOOPY.**

| label | LOOPY statement | what the test establishes |
|---|---|---|
| frozen | Lemma 1.7: delete suicides; Z equals 0 | every Z-move is a suicide in the local game |
| on, off | Definition 3.1, Proposition 3.2, Theorem 4.2(c) | the safe moves of the passer form a cyclic graph in which every state has one (a p-morphism onto on_D after the other side's suicides are deleted); more general than the 2-cycle of Proposition 3.2 |
| dud | Definition 3.1, Proposition 3.2′, Theorem 3.4(a) | the same for both sides, on any closure, not only the four combined king states; it is Proposition 3.2′ with (T1)–(T4) read on the closure |
| over, under | Definition 4.4, Proposition 4.6, "Chess reading of over" | A-states and Z-states exactly as in over_D = {0 \| over_D}; the Z-state is frozen |

**What the tests do not do.**
- "Suicide" is decided in the empty context. That is necessary for (Pun) in every context, not sufficient. The confirmation beside contexts (section 7) tests the sufficiency; it is a sample, not a proof.
- Over cannot be searched in reading B. In plain P the freezing move of an over group leaves the opponent in zugzwang, so the move is a winning move and the root is labelled "threat" (an over group alone is a White win with either side to move, over > 0, Proposition 4.5). So the B counts of over and under are vacuous, and so are its counts of on and off (the opponent of a passer in plain P is in zugzwang and loses). The B reading is meaningful for frozen and dud only. The A reading is meaningful for all five classes. The tempo-signature census (section 5.3) tests over without passes.
- Kings at the root stand on the files a..F only. A group whose kings start outside is found from another root of its closure only if the closure reaches the files a..F.
- Pawns: at most w White and b Black pawns on the ranges listed in section 5. No promoted pieces, no officers.

**Checks of the classifier (data, not proofs).**
- Values. `grp.c` (reading B) against `kp_p --pmodel` (`kpp`, a private build of `kings/delegate/out/K7/scripts/draft/kp_p.c`) on 6,000 random positions on each of flat 7×6, cyl:7×6 and cyl:8×6: 0 mismatches (18,000 positions). CHECKED-2 (kp_p shares source with kpsolve, `grp.c` shares nothing).
- Labels, reading B. `grp.c` against the independent Python classifier `K15/f3/pycheck_np.py` (written by an earlier attempt; its output file `K15/final/chk/py_np_5x6_pa1.tsv` was reused, the C side was re-run with the rebuilt binary): cyl:5×6, 3 files, ≤ 2+2 pawns, root passers allowed, 634,628 roots, 0 different labels (56 dud roots). CHECKED-2.
- Labels, reading A. The same against `K15/pyv/p_*.tsv` (`pycheck.py`): 20 configurations (cyl:5×5, 5×6, 6×5, 3 files, up to 2+2 pawns, leak ignored or not, root passers allowed or not), 772,188 roots, 0 different labels. CHECKED-2. (Dud roots appear in this small-board range only when leaks are ignored.)
- Reproduction. The rebuilt `grp` is byte-identical to the earlier attempt's binary. Fifteen census runs were re-run (flat 7×6 ≤ 2+2, reading B; cyl:7×6 and cyl:8×6 with 3 files ≤ 3+3, 4 files ≤ 3+2 and 5 files ≤ 2+2, both readings: 12 runs; the tempo-signature census for 4 files ≤ 2+2 on both boards: 2 runs): the JSON documents and the candidate lists are identical to the earlier outputs. This shows determinism, not independence.

## 4. Regression test: Z_B on flat 7×6

Z_B = `Kb2 ka4 Pa3 Pb4 pb3 pc4` (shuttles b2–c3 for White and a4–b5 for Black), four combined king states, eight roots. LOOPY (§5.7) has it as exactly two-shuttle in P (PROVED by hand, K27; CHECKED-2 for the computations).

**Result.** The exact classifier labels Z_B **dud** at all four king states (`logs/zb_regression_final.txt`).
- Reading B (plain P): `class=dud csize=4`, each side has exactly one safe move (its shuttle) and every other Z-move is a suicide. This holds on flat 7×6, on cyl:7×6 and on cyl:8×6. It needs the root passers allowed: the strict variant (brief's filter) skips Z_B, because all four pawns are passed pawns for `cylcgt.passed`.
- Reading A (free passes): `mixed`. Against a defender who may pass, two of the pawn pushes are not suicides but draw: Black's c4–c3 at (b2, a4) and White's a3–a4 at (c3, b5) (so each of these states has a second safe move, a pawn move). The other deviations are still suicides. So Z_B is dud in plain P and not against free passes.
- The one-ply classifier of the brief labels Z_B **other** at all four king states. That is the regression failure of the brief's tests, and the reason is exact (below).

**How the one-ply tests differ from the exact P test** (`scripts/zb_regression.py`, `scripts/depth.py`, output in `logs/zb_depth.txt`; own Python move generator `oneply.py`).
1. *Horizon.* Of the 34 legal moves at the 8 roots, 8 are shuttles (they draw) and 26 are deviations. In plain P all 26 lose by force (CHECKED-2: `kp_p`, `ref3m`, and my own depth search agree on the 8 values and the 34 move values; K27's proof gives at most 11 plies). The number of plies after the move in which the opponent forces a promotion is 3 for 4 moves, 5 for 2, 7 for 6, 9 for 8 and 11 for 6. A one-ply suicide needs an immediate promotion or an immediate passed pawn: **none of the 26 is one.** So no deviation is ever recognised as decisively punished.
2. *The shuttle test is too weak.* The brief's safe shuttle is "a non-capturing king move inside the group, legal, reversible, with the same property afterwards". It does not ask that the move holds. 12 of the 26 losing deviations (White Kb2–a1, b1, c1 at both Black states; Black Kb5–a6, b6, c6 at both White states) pass that test and are counted as shuttles, although they lose in 7 to 9 plies. The other 14 are pawn pushes and king moves that the one-ply test calls "other".
3. *Closure.* A label dud needs every non-shuttle move at every state of the closure to be a suicide. With (1) and (2) the one-ply closure test fails at the first state (`closure ok = False`).

**On the whole range.** Flat 7×6, 3 files, ≤ 2+2 pawns, root passers allowed, reading B: the exact classifier labels 41 roots dud (4 groups: Z_B, its mirror, D2 and `Ka1 ka5 Pa4 Pb3 pa3 pb4`). The one-ply classifier labels **none** of the 41 as dud (`scripts/oneply_confusion.py`, `logs/oneply_confusion.txt`); it says "other" for all 41. For the other classes it recovers 18 of 52 frozen roots and 32 of 230 on and 32 of 230 off roots.

**The same on the cylinders.** `Kb2 ka4 Pa3 Pb4 pb3 pc4` on cyl:7×6 and cyl:8×6 has, at its 8 roots, the value (D, D) and exactly one drawing move for the side to move (its shuttle); every other legal move loses for the mover, the wrap-around king moves (Ka4–g5, g3 on 7×6, a4–h5, h3 on 8×6) included: 38 legal moves, 8 draw, 30 lose (CHECKED-2: `kp_p` and `ref3m`, `logs/zb_moves_*.txt`). It is not hand-proved on the cylinder (K27's proof is for the flat board).

## 5. The search

### 5.1 Ranges that ran

Every placement of both kings (on the files a..F) and of at most w White and b Black pawns on the files a..F, ranks 2..H−1, was classified (section 2.1), twice: with root passers excluded (the brief's filter: "strict") and allowed. A pawn count "w+b" means every placement with at most w White and at most b Black pawns (so ≤ 3+3 contains ≤ 3+2 and ≤ 2+3; the colour-and-rank flip of the board maps 2+3 to 3+2). Source: `fin2/runs/*.json` (own re-run, rebuilt binary) or, where marked "earlier", the earlier attempt's output of the same source (byte-identical binary).

| board | files | pawns W+B | reading | root passers | roots | frozen | on | off | dud roots (groups) | over | under | source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cyl:7x6 | 3 | 3+3 | A (passes) | allowed | 4800508 | 58 | 1193 | 1193 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 3 | 3+3 | A (passes) | excluded | 551176 | 18 | 540 | 540 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 3 | 3+3 | B (plain P) | allowed | 4800508 | 234 | 23 | 23 | 94 (5) | 0 | 0 | rerun |
| cyl:7x6 | 3 | 3+3 | B (plain P) | excluded | 551176 | 78 | 0 | 0 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 3 | 4+4 | A (passes) | allowed | 15366448 | 158 | 2143 | 2143 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 3 | 4+4 | A (passes) | excluded | 1364916 | 22 | 766 | 766 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 3 | 4+4 | B (plain P) | allowed | 15366448 | 486 | 153 | 153 | 103 (5) | 0 | 0 | rerun |
| cyl:7x6 | 3 | 4+4 | B (plain P) | excluded | 1364916 | 124 | 0 | 0 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 4 | 3+2 | A (passes) | allowed | 18281088 | 142 | 3290 | 842 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 4 | 3+2 | A (passes) | excluded | 1411716 | 68 | 1492 | 464 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 4 | 3+2 | B (plain P) | allowed | 18281088 | 456 | 58 | 0 | 156 (12) | 0 | 0 | rerun |
| cyl:7x6 | 4 | 3+2 | B (plain P) | excluded | 1411716 | 216 | 0 | 0 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 4 | 3+3 | A (passes) | allowed | 70154616 | 438 | 5390 | 5390 | 208 (10) | 0 | 0 | earlier |
| cyl:7x6 | 4 | 3+3 | A (passes) | excluded | 5089808 | 168 | 2652 | 2652 | 0 (0) | 0 | 0 | earlier |
| cyl:7x6 | 4 | 3+3 | B (plain P) | allowed | 70154616 | 1566 | 104 | 104 | 548 (36) | 0 | 0 | earlier |
| cyl:7x6 | 4 | 3+3 | B (plain P) | excluded | 5089808 | 640 | 0 | 0 | 0 (0) | 0 | 0 | earlier |
| cyl:7x6 | 4 | 4+2 | A (passes) | allowed | 53106424 | 156 | 4528 | 912 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 4 | 4+2 | A (passes) | excluded | 2888312 | 74 | 1898 | 534 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 4 | 4+2 | B (plain P) | allowed | 53106424 | 538 | 320 | 0 | 156 (12) | 0 | 0 | rerun |
| cyl:7x6 | 4 | 4+2 | B (plain P) | excluded | 2888312 | 248 | 0 | 0 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 5 | 2+2 | A (passes) | allowed | 19538236 | 318 | 1464 | 1464 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 5 | 2+2 | A (passes) | excluded | 1433658 | 138 | 686 | 686 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 5 | 2+2 | B (plain P) | allowed | 19538236 | 756 | 0 | 0 | 386 (38) | 0 | 0 | rerun |
| cyl:7x6 | 5 | 2+2 | B (plain P) | excluded | 1433658 | 332 | 0 | 0 | 24 (4) | 0 | 0 | rerun |
| cyl:7x6 | 5 | 3+2 | A (passes) | allowed | 105386440 | 490 | 7816 | 1710 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 5 | 3+2 | A (passes) | excluded | 5267194 | 202 | 3508 | 898 | 0 (0) | 0 | 0 | rerun |
| cyl:7x6 | 5 | 3+2 | B (plain P) | allowed | 105386440 | 1396 | 141 | 0 | 562 (50) | 0 | 0 | rerun |
| cyl:7x6 | 5 | 3+2 | B (plain P) | excluded | 5267194 | 632 | 0 | 0 | 32 (6) | 0 | 0 | rerun |
| cyl:7x7 | 3 | 3+2 | A (passes) | allowed | 9048610 | 28 | 2609 | 685 | 0 (0) | 0 | 0 | earlier |
| cyl:7x7 | 3 | 3+2 | A (passes) | excluded | 1246132 | 24 | 1351 | 400 | 0 (0) | 0 | 0 | earlier |
| cyl:7x7 | 3 | 3+2 | B (plain P) | allowed | 9048610 | 336 | 12 | 0 | 0 (0) | 0 | 0 | earlier |
| cyl:7x7 | 3 | 3+2 | B (plain P) | excluded | 1246132 | 184 | 0 | 0 | 0 (0) | 0 | 0 | earlier |
| cyl:8x6 | 3 | 3+3 | A (passes) | allowed | 4800508 | 62 | 1205 | 1205 | 0 (0) | 0 | 0 | rerun |
| cyl:8x6 | 3 | 3+3 | A (passes) | excluded | 551176 | 18 | 540 | 540 | 0 (0) | 0 | 0 | rerun |
| cyl:8x6 | 3 | 3+3 | B (plain P) | allowed | 4800508 | 240 | 23 | 23 | 102 (7) | 0 | 0 | rerun |
| cyl:8x6 | 3 | 3+3 | B (plain P) | excluded | 551176 | 84 | 0 | 0 | 8 (2) | 0 | 0 | rerun |
| cyl:8x6 | 3 | 4+4 | A (passes) | allowed | 15366448 | 162 | 2161 | 2161 | 0 (0) | 0 | 0 | rerun |
| cyl:8x6 | 3 | 4+4 | A (passes) | excluded | 1364916 | 22 | 772 | 772 | 0 (0) | 0 | 0 | rerun |
| cyl:8x6 | 3 | 4+4 | B (plain P) | allowed | 15366448 | 496 | 153 | 153 | 111 (7) | 0 | 0 | rerun |
| cyl:8x6 | 3 | 4+4 | B (plain P) | excluded | 1364916 | 130 | 0 | 0 | 8 (2) | 0 | 0 | rerun |
| cyl:8x6 | 4 | 3+2 | A (passes) | allowed | 18281088 | 136 | 3362 | 850 | 0 (0) | 0 | 0 | rerun |
| cyl:8x6 | 4 | 3+2 | A (passes) | excluded | 1411716 | 68 | 1500 | 464 | 0 (0) | 0 | 0 | rerun |
| cyl:8x6 | 4 | 3+2 | B (plain P) | allowed | 18281088 | 448 | 62 | 4 | 148 (12) | 0 | 0 | rerun |
| cyl:8x6 | 4 | 3+2 | B (plain P) | excluded | 1411716 | 224 | 0 | 0 | 16 (4) | 0 | 0 | rerun |
| cyl:8x6 | 4 | 3+3 | A (passes) | allowed | 70154616 | 426 | 5476 | 5476 | 208 (10) | 0 | 0 | earlier |
| cyl:8x6 | 4 | 3+3 | A (passes) | excluded | 5089808 | 176 | 2662 | 2662 | 0 (0) | 0 | 0 | earlier |
| cyl:8x6 | 4 | 3+3 | B (plain P) | allowed | 70154616 | 1554 | 108 | 108 | 524 (32) | 0 | 0 | earlier |
| cyl:8x6 | 4 | 3+3 | B (plain P) | excluded | 5089808 | 668 | 0 | 0 | 16 (4) | 0 | 0 | earlier |
| cyl:8x6 | 4 | 4+2 | A (passes) | allowed | 53106424 | 150 | 4654 | 900 | 0 (0) | 0 | 0 | rerun |
| cyl:8x6 | 4 | 4+2 | A (passes) | excluded | 2888312 | 74 | 1932 | 514 | 0 (0) | 0 | 0 | rerun |
| cyl:8x6 | 4 | 4+2 | B (plain P) | allowed | 53106424 | 526 | 324 | 4 | 148 (12) | 0 | 0 | rerun |
| cyl:8x6 | 4 | 4+2 | B (plain P) | excluded | 2888312 | 252 | 0 | 0 | 16 (4) | 0 | 0 | rerun |
| cyl:8x6 | 5 | 2+2 | A (passes) | allowed | 19538236 | 308 | 1572 | 1572 | 24 (4) | 0 | 0 | rerun |
| cyl:8x6 | 5 | 2+2 | A (passes) | excluded | 1433658 | 144 | 712 | 712 | 24 (4) | 0 | 0 | rerun |
| cyl:8x6 | 5 | 2+2 | B (plain P) | allowed | 19538236 | 752 | 8 | 8 | 362 (36) | 0 | 0 | rerun |
| cyl:8x6 | 5 | 2+2 | B (plain P) | excluded | 1433658 | 372 | 0 | 0 | 48 (10) | 0 | 0 | rerun |
| cyl:8x6 | 5 | 3+2 | A (passes) | allowed | 105386440 | 494 | 8164 | 1834 | 24 (4) | 0 | 0 | rerun |
| cyl:8x6 | 5 | 3+2 | A (passes) | excluded | 5267194 | 210 | 3654 | 936 | 24 (4) | 0 | 0 | rerun |
| cyl:8x6 | 5 | 3+2 | B (plain P) | allowed | 105386440 | 1389 | 153 | 8 | 538 (48) | 0 | 0 | rerun |
| cyl:8x6 | 5 | 3+2 | B (plain P) | excluded | 5267194 | 684 | 0 | 0 | 56 (12) | 0 | 0 | rerun |
| cyl:8x7 | 3 | 3+2 | A (passes) | allowed | 9048610 | 30 | 2643 | 677 | 0 (0) | 0 | 0 | earlier |
| cyl:8x7 | 3 | 3+2 | A (passes) | excluded | 1246132 | 24 | 1349 | 392 | 0 (0) | 0 | 0 | earlier |
| cyl:8x7 | 3 | 3+2 | B (plain P) | allowed | 9048610 | 362 | 12 | 0 | 0 (0) | 0 | 0 | earlier |
| cyl:8x7 | 3 | 3+2 | B (plain P) | excluded | 1246132 | 220 | 0 | 0 | 0 (0) | 0 | 0 | earlier |
| cyl:8x8 | 3 | 3+2 | A (passes) | allowed | 33867608 | 63 | 6335 | 1209 | 66 (6) | 0 | 0 | earlier |
| cyl:8x8 | 3 | 3+2 | A (passes) | excluded | 4967962 | 38 | 3429 | 666 | 0 (0) | 0 | 0 | earlier |
| cyl:8x8 | 3 | 3+2 | B (plain P) | allowed | 33867608 | 575 | 15 | 0 | 162 (16) | 0 | 0 | earlier |
| cyl:8x8 | 3 | 3+2 | B (plain P) | excluded | 4967962 | 386 | 0 | 0 | 8 (2) | 0 | 0 | earlier |
| cyl:8x8 | 4 | 2+2 | A (passes) | allowed | 48191072 | 176 | 2834 | 2834 | 144 (16) | 0 | 0 | earlier |
| cyl:8x8 | 4 | 2+2 | A (passes) | excluded | 5879000 | 132 | 1448 | 1448 | 0 (0) | 0 | 0 | earlier |
| cyl:8x8 | 4 | 2+2 | B (plain P) | allowed | 48191072 | 936 | 4 | 4 | 216 (30) | 0 | 0 | earlier |
| cyl:8x8 | 4 | 2+2 | B (plain P) | excluded | 5879000 | 568 | 0 | 0 | 16 (4) | 0 | 0 | earlier |
| flat:7x6 | 3 | 2+2 | A (passes) | allowed | 634628 | 34 | 418 | 418 | 0 (0) | 0 | 0 | rerun |
| flat:7x6 | 3 | 2+2 | A (passes) | excluded | 99694 | 14 | 206 | 206 | 0 (0) | 0 | 0 | rerun |
| flat:7x6 | 3 | 2+2 | B (plain P) | allowed | 634628 | 52 | 230 | 230 | 41 (4) | 0 | 0 | rerun |
| flat:7x6 | 3 | 2+2 | B (plain P) | excluded | 99694 | 20 | 65 | 65 | 0 (0) | 0 | 0 | rerun |
| flat:7x6 | 3 | 3+3 | A (passes) | allowed | 4800508 | 234 | 1732 | 1732 | 9 (1) | 0 | 0 | rerun |
| flat:7x6 | 3 | 3+3 | A (passes) | excluded | 551176 | 34 | 707 | 707 | 0 (0) | 0 | 0 | rerun |
| flat:7x6 | 3 | 3+3 | B (plain P) | allowed | 4800508 | 278 | 815 | 815 | 110 (10) | 0 | 0 | rerun |
| flat:7x6 | 3 | 3+3 | B (plain P) | excluded | 551176 | 50 | 236 | 236 | 8 (2) | 0 | 0 | rerun |

How to read the table.
- Reading A (passes) is the meaningful one for on, off, dud, over and under; reading B (plain P) is meaningful for frozen and dud (section 3).
- "dud roots (groups)": the number of roots labelled dud and, in brackets, the number of different closures (distinct groups before the symmetry reduction of section 6).
- **over and under: 0 in every row.**
- The tempo-signature census (below) is independent of the structural classifier.

### 5.2 What was asked, what ran, what did not fit

| asked by the brief | boards | result |
|---|---|---|
| ≤ 3+2, ≤ 2+3 and ≤ 3+3 on 3 files | cyl:8×6, cyl:7×6 | ran (≤ 3+3 and ≤ 4+4), both readings |
| ≤ 2+2 and ≤ 3+2 on 4 files | cyl:8×6, cyl:7×6 | ran (≤ 3+2 and ≤ 3+3), both readings |
| cyl:8×8 "if it fits" | 3 files ≤ 3+2, 4 files ≤ 2+2 ran | 3 files ≤ 3+3 needs a 4.86 GB table, 4 files ≤ 3+2 needs 4.48 GB: do not fit under 3 GB |

Beyond the brief, and completed: 5 files ≤ 2+2 (cyl:7×6, 8×6); 3 files ≤ 4+4 (cyl:7×6, 8×6); 3 files ≤ 3+2 on cyl:7×7 and cyl:8×7; flat 7×6, 3 files ≤ 2+2.
All of these runs completed (17 runs with a `.done` file in `fin2/runs/`, listed in the table of 5.1 with source "rerun").

The table size is the number of layers times 2·N² bytes (N = number of squares). Ranges that were not run because the table exceeds 3 GB: cyl:8×6, 5 files ≤ 3+3 (5.4 GB); cyl:7×7 and cyl:8×7, 3 files ≤ 4+4 (6.1 and 8.0 GB), 4 files ≤ 3+3 (5.6 and 7.3 GB); cyl:8×8, 3 files ≤ 3+3 (4.9 GB), 4 files ≤ 3+2 (4.5 GB). Ranges that fit and were not run (not asked for): cyl:8×8 with 5 files ≤ 2+2 (1.6 GB), cyl:7×7 and cyl:8×7 with 4 files ≤ 3+2 (1.0 and 1.3 GB) and 5 files ≤ 2+2.

### 5.3 Tempo-signature census (no structural assumption, no passes)

For every root the 16 outcomes (side to move, and the contexts "one private White tempo move", "one private Black tempo move", "one shared move", in all 8 combinations) are computed in plain P, and compared with the signatures of the six abstract games zero, on, off, dud, over, under. This does not use the labels of section 2. Note that the signature of dud is the all-draw vector, so the "dud" column only says "draws in all 16 contexts" and is not a dud test.

| board | files | pawns W+B | root passers | roots | all-draw signature (dud sig.) | over signature | under signature | source |
|---|---|---|---|---|---|---|---|---|
| cyl:7x6 | 3 | 3+3 | excluded | 402488 | 6621 | 0 | 0 | rerun |
| cyl:7x6 | 3 | 3+3 | allowed | 3239040 | 12418 | 0 | 0 | rerun |
| cyl:7x6 | 4 | 2+2 | excluded | 376214 | 17630 | 18 | 18 | rerun |
| cyl:7x6 | 4 | 2+2 | allowed | 3484260 | 33836 | 20 | 20 | rerun |
| cyl:8x6 | 3 | 3+3 | excluded | 402488 | 7242 | 0 | 0 | rerun |
| cyl:8x6 | 3 | 3+3 | allowed | 3239040 | 13215 | 0 | 0 | rerun |
| cyl:8x6 | 4 | 2+2 | excluded | 376214 | 18950 | 4 | 4 | rerun |
| cyl:8x6 | 4 | 2+2 | allowed | 3484260 | 35268 | 20 | 20 | rerun |


On 3 files ≤ 3+3 no root has the over (or under) signature. On 4 files ≤ 2+2 there are over-signature roots; they are the candidates tested in section 7.3.

## 6. The groups found

### 6.1 Over and under

**No over or under group was found** in any range of section 5.1 (structural classifier, reading A, root passers excluded or allowed), and none on 3 files ≤ 3+3 by the tempo-signature census. Candidates that are close in some sense:
- 20 distinct groups with the over signature on 4 files ≤ 2+2 (10 on cyl:7×6 and 10 on cyl:8×6 up to symmetry, from 20 over-signature roots per board; the colour-and-rank flip maps the over signature to the under signature);
- the *near-over* roots of the structural classifier: Black has a safe shuttle and every White safe move leads to a frozen state, but the closure condition fails elsewhere (distinct groups, near-over / near-under: cyl:7×6 12 / 15, cyl:8×6 12 / 16, cyl:8×8 4 / 2, cyl:7×7 1 / 0, cyl:8×7 1 / 0).

All are tested in section 7.3.

### 6.2 Dud

Distinct dud groups, up to file translation (cylinder), file mirror and the colour-and-rank flip: **43 on cyl:7×6, 40 on cyl:8×6, 25 on cyl:8×8, 9 on flat 7×6 (cyl:7×7 and cyl:8×7: 0 and 0)** (readings A or B, root passers allowed; the full list with the confirmation result of each is `fin2/dud_groups.md`). Every group is listed there with notation in full (43, 40, 25 and 9 groups). Beside contexts (section 7.1): 31 groups on cyl:7×6 and 28 on cyl:8×6; at the root only (section 7.5): the other 12 + 12 + 25 groups (cyl:7×6, cyl:8×6, cyl:8×8).

*Without a root passer* (the brief's filter):
- cyl:8×6, 5 files, ≤ 2+2 pawns: two groups that are dud in **both** readings, A and B (CHECKED-2 for the move lists):
  - **G8a = `Kb2 kc4 Pa3 Pe2 pa4 pe3`** (blocked pairs a3/a4 and e2/e3 on files four apart; White shuttles b2–c2, Black c4–d4);
  - **G8b = `Kb3 kc5 Pa4 Pe3 pa5 pe4`** (the same one rank higher).
  `cylcgt.passed` is false for both pawn sets. Four combined king states each, 8 roots each, all (D, D); 72 legal moves at the 16 roots: 16 shuttles that draw, 56 deviations that lose (`logs/g8_moves_*.txt`; `kp_p` and `ref3m` give the same values and move lists). Every deviation loses by force in 11 to 21 plies (the earlier attempt's `scripts/depth2.py`, not re-run here, `logs/g8a_pv.txt` has the principal variations; also against free passes, reading A, by the classifier).
- cyl:7×6: the same two placements are dud in plain P only (reading B) and the window leaves no context file (7 files = 5 + 2 buffer files), so they are confirmed in the empty context only.
- cyl:8×6, 3 files: `Ka2 kc4 Pa4 Pc2 pa5 pc3` is dud in plain P (reading B) without a root passer, but it is **not** equal to dud_D beside contexts (section 7.1).
- cyl:7×6 and cyl:8×6, 5 files ≤ 2+2 (reading B): further no-passer groups, listed in `dud_groups.md`.

*With a root passer* (blockaded by a king, as in Z_B): the families D2 `Ka1 ka4 Pb4 Pc3 pb3 pc4`, D2m `Ka1 ka6 Pa3 Pb4 pa4 pb3`, D3 `Ka1 ka6 Pa3 Pb4 Pc3 pa4 pb3 pc4`, **Z_B on the cylinder** (`Kb2 ka4 Pa3 Pb4 pb3 pc4`, canonical form `Ka2 kb4 Pa4 Pb3 pa3 pg4` on 7×6), and groups made of one of these and extra blocked pairs on further files. On flat 7×6 (≤ 2+2 pawns, 3 files) the census finds four dud groups: Z_B, its mirror, D2 and `Ka1 ka5 Pa4 Pb3 pa3 pb4`.

## 7. Confirmation

Method (P model, exact, `kp_p --pmodel`, the private build `fin2/bin/kpp`): each group is put beside pawn-only contexts G on the files at distance at least 2 from the group's files (so no context pawn can ever meet a group pawn or attack a group square, Lemma 2.2), on one file or on two non-adjacent files, with no capture possible. For a dud group every king state of the shuttle closure (found by the moves that `kp_p` values as draws) and both sides to move are tested. The prediction is the brute-force value of G ⊞ dud_D (G ⊞ over_D, G ⊞ under_D) of Theorem 3.4(a) and Proposition 4.6, by `confirm.py` (D-model solver written for the earlier attempt, re-read; it uses the pushes and double steps of G only, a promotion is a decisive event, a player without a move loses, infinite play is a draw). "Agree" means `kp_p` returns an exact value (A = B) equal to the prediction. Four named contexts are always included: empty, a blocked pair (mutual zugzwang), a one-move pair, a gap pair; the others are random with up to 3 pawns.

### 7.1 Dud groups (P model)

| run | board | groups | positions | agree | DISAGREE | inexact | missing | groups with no difference |
|---|---|---|---|---|---|---|---|---|
| strictA8 | cyl:8x6 | 2 | 640 | 640 | 0 | 0 | 0 | 2 |
| c7x6 | cyl:7x6 | 31 | 16340 | 16268 | 72 | 0 | 0 | 29 |
| c8x6 | cyl:8x6 | 28 | 20448 | 20150 | 298 | 0 | 0 | 23 |

`strictA8` = the two A-dud groups without root passer, 40 contexts; `c7x6`, `c8x6` = the distinct dud groups of the census at the time (section 6.2), beside 24 contexts each (the four named ones and random ones) as far as the window leaves context files. The groups found by later census runs and the cyl:8×8 groups were not put beside contexts; they are checked at the root only (section 7.5).

Groups with at least one difference (all of them are dud in plain P in the empty context, none is dud against free passes):

| run | group | positions | agree | DISAGREE | contexts with a difference |
|---|---|---|---|---|---|
| c7x6 | `Kb1 ka5 Pb3 Pd4 pc3 pd5` | 288 | 264 | 24 | ['C2_onemove', 'C3_gap2'] |
| c7x6 | `Ka1 kc5 Pa4 Pc3 pa5 pb3` | 288 | 240 | 48 | ['C2_onemove', 'C3_gap2', 'R_f2_f4', 'R_f2f3_f5'] |
| c8x6 | `Kb1 ka5 Pb3 Pe3 pc3 pe4` | 432 | 378 | 54 | ['C2_onemove', 'C3_gap2', 'R_g2_g4'] |
| c8x6 | `Ka2 kb6 Pc4 Pe2 pb4 pe3` | 432 | 360 | 72 | ['C2_onemove', 'C3_gap2', 'R_g2_g4', 'R_g2_g5'] |
| c8x6 | `Kb1 kc5 Pa3 Pd3 pa4 pc3` | 432 | 378 | 54 | ['C2_onemove', 'C3_gap2', 'R_g2_g3g5'] |
| c8x6 | `Kb1 kc5 Pa4 Pd3 pa5 pc3` | 432 | 360 | 72 | ['C2_onemove', 'C3_gap2', 'R_g2_g5', 'R_g3_g5'] |
| c8x6 | `Ka2 kc4 Pa4 Pc2 pa5 pc3` | 192 | 146 | 46 | ['C1_blocked', 'C2_onemove', 'C3_gap2', 'R_e2_e3', 'R_e2e3_e4', 'R_f3_f5'] |

Groups whose window leaves no (or almost no) room for a context are confirmed in the empty context (or a few contexts) only, and the agreement there says little: `Kb1 ka5 Pb3 Pe3 pc3 pe4`, `Ka2 kb6 Pc4 Pe2 pb4 pe3`, `Kb1 kc5 Pa3 Pd3 pa4 pc3`, `Kb1 kc5 Pa4 Pd3 pa5 pc3`, `Kc1 ka4 Pb4 Pc3 pc4 pd3`, `Ka1 kc6 Pc3 Pd4 pb3 pc4`, `Kb3 kc5 Pa4 Pe3 pa5 pe4`, `Kb2 kc4 Pa3 Pe2 pa4 pe3`, `Ka3 kd5 Pd4 Pe3 pb3 pc4`, `Kc3 ka4 Pa3 Pb4 pc4 pd3`.


### 7.2 Exhaustive single-file contexts

For a group, a context file X and every one of the 3^(H−2) assignments of {empty, White pawn, Black pawn} to the squares X2..X5 (`scripts/ctx_exh.py`):
- **G8a and G8b** (cyl:8×6, context file g, the only file at distance ≥ 2): all 4 king states of each, both sides to move, against dud_D: 8 runs, 1296 positions, **1296 agree, 0 differ**, 0 inexact (`logs/ctx_exh_G8.txt`).
- **Z_B on the cylinders** (`Kb2 ka4 Pa3 Pb4 pb3 pc4`, 4 king states): cyl:7×6 with the context file e or f, cyl:8×6 with e, f or g: 20 runs, 3240 positions, **3240 agree, 0 differ**, 0 inexact (`logs/ctx_exh_ZB.txt`).
- **The two over-signature candidates that survived the 40 random contexts** (cyl:8×6, `Kc4 kd6 Pd3 Pd5 pa5 pd4` and `Kb4 ka6 Pa3 Pa5 pa4 pd4`, file f or g, against over_D): 4 runs, 648 positions, 634 agree, **14 differ**; every one of the four runs has 3 or 4 differences (`logs/ctx_exh_over_survivors.txt`). Both are refuted. Neither has a king shuttle: Black's only safe moves are pawn moves (a5–a4 and a5–a3 in the first group, d4–d3 in the second), a finite supply, so they are not over groups in the structural sense.


### 7.3 Over and under candidates (P model, root only)

| run | board | class | groups | positions | agree | DISAGREE | inexact | missing | groups with no difference |
|---|---|---|---|---|---|---|---|---|---|
| o7x6 | cyl:7x6 | over | 10 | 800 | 730 | 70 | 0 | 0 | 0 |
| o8x6 | cyl:8x6 | over | 10 | 800 | 745 | 55 | 0 | 0 | 2 |
| nol7x6 | cyl:7x6 | over | 12 | 84 | 33 | 51 | 0 | 0 | 2 |
| nul7x6 | cyl:7x6 | under | 12 | 84 | 32 | 52 | 0 | 0 | 2 |
| nol8x6 | cyl:8x6 | over | 12 | 96 | 45 | 51 | 0 | 0 | 2 |
| nul8x6 | cyl:8x6 | under | 12 | 96 | 41 | 55 | 0 | 0 | 2 |
| nol8x8 | cyl:8x8 | over | 4 | 32 | 17 | 15 | 0 | 0 | 0 |
| nul8x8 | cyl:8x8 | under | 2 | 16 | 10 | 6 | 0 | 0 | 0 |
| nol7x7 | cyl:7x7 | over | 1 | 8 | 7 | 1 | 0 | 0 | 0 |
| nol8x7 | cyl:8x7 | over | 1 | 8 | 7 | 1 | 0 | 0 | 0 |
| no7x6 | cyl:7x6 | over | 12 | 804 | 52 | 10 | 0 | 742 | 0 |
| no8x6 | cyl:8x6 | over | 12 | 960 | 787 | 129 | 0 | 44 | 0 |

`o7x6`, `o8x6`: the tempo-signature candidates (4 files ≤ 2+2), 40 contexts. `nol*`, `nul*` (and the older `no*`, `nu*`): the near-over and near-under roots of the structural classifier, the four named contexts (`nol*`, `nul*`) or up to 40 contexts (the partial `no7x6`). Root only, both sides to move.

**Near-over and near-under roots, and the one candidate that survived the first tests.**
- *Definition.* A root is near-over when Black has a shuttle in reading A (free passes), every White safe move at the root leads to a Z-state (no safe move for either side, no check, no winning move, no leak), but the closure condition of "over" fails somewhere. Near-under is the colour mirror. The census prints every such root (no run reaches the print limit of 40, so the lists are complete): distinct groups up to symmetry, near-over: 12 on cyl:7×6, 12 on cyl:8×6, 4 on cyl:8×8, 1 on cyl:7×7, 1 on cyl:8×7; near-under: 15, 16, 2, 0, 0 (`fin2/summary.json`). The near-under lists are not all images of the near-over lists in the table above (12 groups each were tested on cyl:7×6 and cyl:8×6; the other near-under groups were not).
- *Named contexts first* (rows `nol*`, `nul*`: empty, blocked pair, one move, gap; root only, both sides to move). On cyl:7×6 and cyl:8×6 ten of the twelve near-over groups differ from r(G ⊞ over_D) in at least one of the four contexts. Two agree at all 8 positions: `Ka5 kc4 Pb2 Pe3 pb5 pe4` and **Z\* = `Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4`**. (On cyl:7×6 `Ka5 kc4 Pb2 Pe3 pb5 pe4` has only the two root positions of a one-file window.)
- *40 random contexts* (row `no8x6`, cyl:8×6; the cyl:7×6 run `no7x6` was cut off by machine load, 742 of 804 positions missing, and is not used). `Ka5 kc4 Pb2 Pe3 pb5 pe4`: 78 agree, 2 differ (contexts `R_g2_g3`, `R_g2_g3g4`): refuted. Z\*: 69 agree, 0 differ, 11 positions not finished.
- *Z\* in detail.* Z\* has 3 + 3 pawns on 4 files (a, b, c, d) and no root passer (cylcgt's test), so it is found with the brief's filter. Empty context, P model: (W, W) at both roots; White's only non-losing move is d2–d3 (it wins), the other six White moves lose; all six Black moves lose (`kpp --moves`, `r3` build). So Black has no shuttle in P. In reading A (free passes) the root is a draw, White has one safe move (d2–d3) and Black has three safe moves, which is why the classifier lists it as near-over. In reading B the label is "threat" (`r3/logs/zstar_classify_A.txt`, `zstar_classify_B.txt`).
- *Exhaustive single-file contexts for Z\* (this attempt, section 7.5).* File g of cyl:8×6, all 65 assignments with at most 3 context pawns, both sides to move: 130 of 130 positions agree with r(G ⊞ over_D), among them 35 with prediction (W, W), 23 with (L, L) and 7 with (W, L). File f (cyl:8×6 and cyl:7×6): 127 of 130 agree and **3 differ** (the same three on both boards). **Z\* is refuted**: it does not equal over_D beside every context. Its Black d-pawn move d4–d3 is a spare tempo (a one-move gap on the d file, shared by both sides) that wins when the context lets Black play it, and over_D has no such move.
- *What this shows.* Beside the far context file g alone, Z\* looks like an over group (130 of 130, plus 77 earlier positions). The nearer file f separates it. A confirmation that uses only the context file farthest from the group can support a wrong conjecture. The earlier confirmations of dud groups (section 7.1) use all context files at distance ≥ 2, random contexts with up to two files, and the exhaustive single-file run (section 7.2) for G8a and G8b on the only file g.
- *Not done for Z\*:* contexts with 4 pawns on one file and contexts with two files (adjacent files let pawns capture, which the predictor does not model); chess.


### 7.4 Chess (kpsolve)

Private build `fin2/bin/kp` (rebuilt byte-identically in `r3/bin/kp`) (`cc -O2 -o kp kings/kpsolve.c -lpthread`); every run through `heavy.sh` with a watchdog (3 GB, 1100 s); result `A B` = lower and upper bound from White's point of view, A = B means exact. Runs are at cap 1, and at cap 2 where stated; the chess prediction is that of the D-model (the P and chess models can differ, Theorem 3.2‴ needs (A_Q)).

| board | cap | position | White to move: A B | Black to move: A B | dud_D prediction (W to move, B to move) | agrees | kpsolve time, peak RSS |
|---|---|---|---|---|---|---|---|
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3` (G8a alone) | D D | D D | D D | yes / yes | 11.8 s, 145 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg3 pg4` (G8a + Pg3 pg4 (blocked pair)) | D D | D D | D D | yes / yes | 240.9 s, 969 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg3 pg5` (G8a + Pg3 pg5 (one move)) | D D | D D | D D | yes / yes | 310.4 s, 1168 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg2 pg5` (G8a + Pg2 pg5 (gap pair)) | D D | D D | D D | yes / yes | 376.1 s, 1391 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg2` (G8a + Pg2 (one White pawn, far from queening)) | W W | W W | W W | yes / yes | 143.3 s, 567 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 pg5` (G8a + pg5 (one Black pawn)) | L L | L L | L L | yes / yes | 151.3 s, 587 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg4 pg3` (G8a + Pg4 pg3 (two passers racing)) | W W | W L | W L | yes / undecided at cap 1 (bounds W L; the value is between them) | 862.3 s, 2891 MB |

**G8a and G8b, all 16 roots (4 king states x 2 sides to move x 2 groups), chess at cap 2, `--moves`** (`fin2/chess/cyl_8x6_G8_states_c2_mv.out`; 526.9 s CPU, peak RSS 515 MB): the value is exact (A = B, no "capped promotions met" line) and (D, D) at all 16 roots; 72 legal moves, 16 of them draw (the shuttles, one for each side at each root), the other 56 each lose for the side that plays them (exact). The 16 root values and the 72 per-move values are the same as in the P model (`kp_p --pmodel` and `ref3m`): move lists identical at 16 of 16 roots (rest: see the file). At cap 1 the roots are exact (D, D) too, but 12 of the 72 move values are bounds only (`fin2/chess/cyl_8x6_G8_states_c1_mv.out`, 15.2 s), which is why cap 2 was run.


### 7.5 Re-checks made in this attempt (`r3/`)

This attempt rebuilt every binary itself (`r3/bin/`: `grp` from `K15/grp.c`, `kp` from `kings/kpsolve.c`, `kpp` from `K7/scripts/draft/kp_p.c`, `ref3` and `ref3m` from the K23 sources). The five builds are byte-identical to the binaries of the earlier attempt (md5).

- **Census re-runs (COMPUTED-1, reproduction).** Re-run with the rebuilt `grp` (one CPU-minute each, nice 15): 6 runs (flat 7×6 ≤ 2+2 plain P; flat 7×6 ≤ 2+2 with passes; cyl:8×6 and cyl:7×6, 3 files ≤ 3+3, both readings). The candidate lists are byte-identical and the JSON counts are identical (`r3/logs/rerun.log`). This shows determinism of one source, not independence.
- **Z_B regression (CHECKED-2 for the values).** `scripts/zb_regression_final.sh` and `scripts/depth.py` re-run: the logs are identical to `fin2/logs/zb_regression_final.txt` and `fin2/logs/zb_depth.txt`. `kpp` and `ref3m` on the 8 roots of Z_B on flat 7×6 give (D, D) at all 8 roots, 8 drawing moves and 26 losing moves (`r3/logs/`, same lists as LOOPY §5.7). On cyl:7×6 and cyl:8×6 (`r3/logs/zb_cyl7_*.txt`, `zb_cyl8_*.txt`): `kpp` and `ref3m` give the same root values (all D) and the same move lists at all 8 roots; 38 legal moves, 8 draw, 30 lose, on both boards.
- **G8a and G8b (CHECKED-2 in P, COMPUTED-1 in chess).** `kpp` and `ref3m` on the 16 roots (cyl:8×6): identical root values and identical sorted move lists (`r3/logs/g8_kpp_r3.txt`, `g8_ref3m_r3.txt`). The chess cap-2 lists of `fin2/chess/cyl_8x6_G8_states_c2_mv.out` equal the P lists at all 16 roots (value D D, same moves, same values). Chess has only kpsolve here: `ownchess` of K27 is a flat-board program, so no second chess solver covers the cylinder.
- **Second solver on the confirmation tables (CHECKED-2 for the sample).** c8x6 sampled 100 ref3 done 100 agree 100 differ 0 kpp inexact 0; c7x6 sampled 100 ref3 done 100 agree 100 differ 0 kpp inexact 0; strictA8 sampled 50 ref3 done 50 agree 50 differ 0 kpp inexact 0. The positions are seeded random samples of the inputs of the confirmation runs (`r3/scripts/sample_ref3.py`: seeds 7, 8, 9); `ref3` shares no code with `kp_p` (`r3/scripts/cmp_ref3.py`). So the kp_p confirmation tables are CHECKED-2 on these 250 positions and COMPUTED-1 on the rest.
- **Root check of the 49 dud groups that the earlier attempt had not confirmed** (found by the later census runs: 12 on cyl:7×6, 12 on cyl:8×6, 25 on cyl:8×8; their rows in `fin2/dud_groups.md` said "not run" before). `kpp --pmodel --moves` at the two roots of each (`r3/data/notrun_*.out`, `r3/scripts/chunkrun.py`): the value is (D, D) at both roots and every non-draw move loses for the mover, for cyl:7x6: 12 of 12 groups, cyl:8x6: 12 of 12 groups, cyl:8x8: 25 of 25 groups. This agrees with the exact classifier `grp` (reading B) at the root (CHECKED-2: independent code). No context was run for these 49: they are dud in the empty context only.
- **Chess on the 7×6 cylinder, D2 and D2m (COMPUTED-1, kpsolve cap 1, `--moves`, all 24 king states of each, both sides to move; `r3/logs/chess_cyl7_c1_mv.out`).** The root values are exact (D, D) at all 96 roots. Against the P move lists, over the 48 roots of each group: D2  Ka1 ka4 Pb4 Pc3 pb3 pc4: 116 moves draw in P and in chess (exact); of the 108 moves that lose in P, 52 lose in chess (exact), 52 draw in chess (exact) and 4 are undecided at cap 1; D2m Ka1 ka6 Pa3 Pb4 pa4 pb3: 116 moves draw in P and in chess (exact); of the 108 moves that lose in P, 52 lose in chess (exact), 52 draw in chess (exact) and 4 are undecided at cap 1. So D2 and D2m are **not** two-shuttle in chess: about half of the deviations that lose in P draw in chess (among them king moves across the wrap, such as Ka1–g1 and Ka1–g2 from the root of D2m, which lose in P and draw in chess).

**The over-like survivor Z\* (section 7.3).** Context runs of this attempt, `r3/scripts/ctxexh_chunked.py` (all assignments of {empty, White pawn, Black pawn} to the squares X2..X5 of one context file X with at most 3 context pawns; both sides to move; prediction r(G ⊞ over_D) by `confirm.solve_d`; value by `kp_p --pmodel`, exact):

| board | context file | contexts (≤ 3 pawns) | positions | agree | DISAGREE | inexact | missing |
|---|---|---|---|---|---|---|---|
| cyl:8x6 | g | 65 | 130 | 130 | 0 | 0 | 0 |
| cyl:8x6 | f | 65 | 130 | 127 | 3 | 0 | 0 |
| cyl:7x6 | f | 65 | 130 | 127 | 3 | 0 | 0 |

The disagreements (same three on both boards, file f; the assignment is read f2 f3 f4 f5 with W = White pawn, B = Black pawn, . = empty): context .WBB stm b: predicted W, kp_p L; context W.BB stm w: predicted W, kp_p L; context WBB. stm b: predicted W, kp_p L. One of them, `Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4 Pf3 pf4 pf5 b -`, was also solved by `ref3` (value L, equal to `kp_p`; the over prediction is W): CHECKED-2 (`r3/data/zstar_f3.ref3.out`). There Black plays d4–d3 and wins; in the empty context that move loses.

`ref3` on 16 sampled positions of the file-g contexts (≤ 2 context pawns, `r3/data/zstar_ref16.in`, `.out`): 16 equal the over prediction, 0 do not (CHECKED-2 for this sample of the 130 agreeing positions).

Chess for Z\*: not run: the `heavy.sh` job waited about 50 minutes for a slot of the shared lock (held by other jobs) and was cancelled by its owner (PIDs in `r3/logs/my_queued_heavy_pids.txt`); not claimed.

The queued full run of `ctx_exh.py` (all 81 assignments per file, which includes the contexts with 4 pawns, and the context files e and f of the 7×6 board) waited about two hours for a slot of the shared lock and was cancelled; the 4-pawn contexts are untested for Z\*.


## 8. Verdicts

Labels as in the brief. All statements are for the model and boundary named; solver results are never PROVED.

**V0. Regression and classifier (section 4, section 3).**
- The exact classifier labels Z_B dud on flat 7×6, in plain P (reading B), at all four king states: **CHECKED-2** for the values (`grp` against `kp_p` on 18,000 random positions, 0 mismatches; `kp_p`, `ref3m` and the depth search agree on the 8 root values and the 34 move values). The geometry and the 26 certificates are K27's PROVED result and are not re-proved here.
- The brief's one-ply tests label Z_B "other". Exact difference: a one-ply suicide needs an immediate promotion or an immediate passed pawn, and none of the 26 losing deviations has one (they lose in 3, 5, 7, 9 or 11 plies: 4, 2, 6, 8 and 6 moves); and the one-ply shuttle test (a reversible non-capturing king move) accepts 12 of the 26 deviations as shuttles. On the 41 dud roots of flat 7×6 (≤ 2+2, plain P) the one-ply classifier finds none (the exact classifier agrees with an independent Python classifier on 634,628 roots of cyl:5×6, CHECKED-2: the earlier attempt's cross-check, whose C side this attempt re-ran for the passes reading in `r3/logs/xcheck2_r3.txt`).
- The brief's no-passer filter rejects Z_B: all four pawns are passed pawns for `cylcgt.passed` (blockaded by kings). With the filter on, dud groups need blocked pawn pairs on files two or more apart (G8a, G8b).
- Reading A (dud against free passes) is stricter than reading B (plain P, LOOPY's (Pun)): Z_B is dud in B and "mixed" in A (two pawn pushes draw against a defender who may pass). The two readings agree on G8a and G8b.

**V1. Open question 2: do dud groups exist without a pawn break on the cylinder? Yes.**
- *P model, CHECKED-2.* G8a `Kb2 kc4 Pa3 Pe2 pa4 pe3` and G8b `Kb3 kc5 Pa4 Pe3 pa5 pe4` on cyl:8×6 (files a and e, kings between): the four king states of each (White b2/c2 with Black c4/d4) have value (D, D) at all 16 roots; of the 72 legal moves at these roots 16 draw (the shuttles) and 56 lose for the mover. The groups have no pawn move, no root passer, and are dud against free passes too. `kp_p`, `ref3m` and `grp` agree.
- *Chess, COMPUTED-1.* kpsolve at cap 2 is exact (A = B) at all 16 roots and gives the same 72 move values as P. So G8a and G8b are exactly two-shuttle in chess (cap 2, exact, one solver family).
- *Beside contexts.* P: 1,296 positions (81 file-g assignments × 4 king states × 2 sides to move × 2 groups) and 640 random-context positions agree with r(G ⊞ dud_D), 0 differ (COMPUTED-1; a 50-position sample of the second set and the other tables agree with `ref3`, CHECKED-2 for the sample). Chess, cap 1: empty, blocked pair, one-move pair, gap pair, one White pawn, one Black pawn agree exactly; two racing passers give (W, W) and bounds (W, L) with Black to move (undecided, consistent).
- *Other dud groups.* Up to symmetry 43 (cyl:7×6), 40 (cyl:8×6), 25 (cyl:8×8), 9 (flat 7×6) distinct groups are dud in the empty context (section 6.2). Of the 59 that were put beside contexts, the 18 that are dud also against free passes (reading A) all agree with dud_D in every context; of the 41 that are dud only in plain P, 7 do not equal dud_D beside some context (among them `Ka2 kc4 Pa4 Pc2 pa5 pc3` on cyl:8×6, which has no root passer). So "dud in the empty context" is necessary, not sufficient, and reading A is the better predictor (COMPUTED-1; a CONJECTURE that A suffices). The 49 groups found by the later census runs were checked only at the root (section 7.5).
- *Chess for the Z_B family.* Z_B on cyl:7×6: bounds (W, L) at cap 1 (kpsolve, `fin2/chess/cyl_7x6_cyl7_alone_c1.out`), as on the flat board; cyl:8×6 not run. D2 `Ka1 ka4 Pb4 Pc3 pb3 pc4` and D2m `Ka1 ka6 Pa3 Pb4 pa4 pb3` (cyl:7×6) are (D, D) in chess at cap 1 but not two-shuttle: of the 108 deviations that lose in P (per group, 24 king states, both sides) 52 draw in chess (exact), 52 lose, 4 are undecided at cap 1.
- Not claimed: a hand proof for any cylinder group; cyl:8×8 beside contexts; chess beyond the lines above.

**V2. Conjecture 4.7 (over with wider groups): first half COMPUTED-1 (stronger than stated); second half CONJECTURE, no support.**
- *No over or under group in the searched boundary.* Every placement of both kings (on files a..F, any rank) and of at most w White and b Black pawns (files a..F, ranks 2..H−1; no officers; empty context), cyl:8×6 and 7×6 with F = 3: w, b ≤ 4+4; F = 4: ≤ 3+3; F = 5: ≤ 3+2; cyl:8×8: F = 3 ≤ 3+2, F = 4 ≤ 2+2; cyl:7×7 and 8×7: F = 3 ≤ 3+2; flat 7×6: F = 3 ≤ 3+3. Root passers excluded and allowed. Reading A (the only reading in which the structural test can output over). 0 over and 0 under roots in all 80 runs. The classifier is CHECKED-2 against an independent Python classifier (772,188 roots with passes, 634,628 in plain P, 0 label differences).
- *Reading-B blind spot.* In plain P the freezing move of an over group wins at once, so the structural test cannot find over there. The tempo-signature census covers that case without structure: none on 3 files ≤ 3+3 (cyl:7×6 and 8×6); 20 candidate roots per board on 4 files ≤ 2+2 (10 groups per board), all refuted beside contexts. It does not cover 4 or 5 files beyond ≤ 2+2 (table size).
- *Near-over groups* (section 7.3): all refuted beside contexts but one placement on cyl:7×6 whose window leaves no context file. The most persistent, Z\*, agrees with over_D at 130 of 130 positions on the far context file g and at 77 earlier ones, and is refuted by 3 of 130 positions on the near file f on both boards (CHECKED-2 for one). Lesson: contexts on the farthest file only can support a wrong conjecture.
- *So:* no over group is known in this boundary. The second half of the conjecture (over exists with wider groups) has no support; "none exists" is not claimed either, since the boundary is small (at most 8 pawns, 5 files, empty-context test).
- The Appendix A search could not have found dud or over: its one-ply classifier cannot output dud (OpenCode's code: `has_safe_shuttle` needs a frozen opponent, so `dud` is unreachable; its over test skips pawn moves). Its negative statement is withdrawn.

**V3. What stays open.** Chess for the plain-P duds (Z_B on flat 7×6: five deviations undecided at cap 1, cap 2 not run, LOOPY §5.7; Z_B on the cylinders: not examined move by move; D2 and D2m are not two-shuttle in chess); the cylinder groups beside contexts in chess beyond G8a; over in plain P beyond the tempo-signature ranges; hand proofs.


## 9. Reproduce

All commands run in `kings/delegate/out/K15/fin2` (abbreviated; paths relative to it), PYTHONPATH = the repository root, Python = the repository's `.venv/bin/python` where `cylcgt` is needed.
```
cc -O2 -o bin/grp ../grp.c
cc -O2 -o bin/kp   kings/kpsolve.c -lpthread
cc -O2 -o bin/kpp  kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread        # run with --pmodel
c++ -O2 -std=c++17 -o bin/ref3m kings/delegate/out/K23/verify/ref3m.cpp         # boards: cyl:8x6 or flat7x6 (quirk)
# census (one run = both root-passer variants; B = --nopass, A = default)
bin/grp [--nopass] [--flat] --W 8 --H 6 --F 5 --wmax 2 --bmax 2 --sp-variants --out runs/NAME > runs/NAME.json
bin/grp --tempo --W 7 --H 6 --F 4 --wmax 2 --bmax 2 --out runs/NAME > runs/NAME.json
# one root
bin/grp [--nopass] --flat --W 7 --H 6 --F 3 --wmax 2 --bmax 2 --classify "Kb2 ka4 Pa3 Pb4 pb3 pc4 w -"
# Z_B regression
./scripts/zb_regression_final.sh ; python3 scripts/depth.py ../final/logs/zb_roots.in ; python3 scripts/oneply_confusion.py val/flat76_B_roots.tsv 3000
# P-model confirmation
python3 conf2.py gen cyl:8x6 dud cf/g_strictA_8x6.txt cf/strictA8 --nctx 40 --seed 11 --allstates
bin/kpp --board cyl:8x6 --ep on --cap 0 --pmodel < cf/strictA8.chunk.aa > cf/strictA8.chunk.aa.out ; python3 conf2.py cmp cf/strictA8 cf/strictA8.out
python3 scripts/ctx_exh.py cyl:8x6 dud g "Kb2 kc4 Pa3 Pe2 pa4 pe3"
# chess
kings/delegate/heavy.sh scripts/wd.sh chess/X.pid 3000000 1100 bin/kp --board cyl:8x6 --cap 1 --threads 2 < chess/G8a_alone.in
# this attempt (r3), all in kings/delegate/out/K15/r3:
cc -O2 -o bin/grp ../grp.c ; cc -O2 -o bin/kp kings/kpsolve.c -lpthread ; cc -O2 -o bin/kpp kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread
c++ -O2 -std=c++17 -o bin/ref3 kings/delegate/out/K23/verify/ref3.cpp ; c++ -O2 -std=c++17 -o bin/ref3m kings/delegate/out/K23/verify/ref3m.cpp
scripts/rerun.sh                                   # census re-runs, compared with fin2/runs
python3 scripts/sample_ref3.py c8x6 cyl:8x6 100 8  # seeded samples (c7x6 seed 7, strictA8 seed 9, 50 lines); then scripts/run_ref3_unlocked.sh and scripts/cmp_ref3.py c8x6 c7x6 strictA8
python3 scripts/chunkrun.py cyl:8x8 data/notrun_cyl_8x8.in data/notrun_cyl_8x8.out 2 --moves
python3 scripts/ctxexh_chunked.py cyl:8x6 over g "Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4" logs/ctxexh_surv_chunked.txt 4 3     # Z*, file g; f and cyl:7x6 likewise
bin/kp --board cyl:7x6 --cap 1 --threads 2 --moves < data/cyl7_states.in                                           # D2, D2m in chess (through heavy.sh)
python3 scripts/mkchess_r3.py ; python3 scripts/mkadditions.py ; python3 scripts/mkedits.py ; (cd ../fin2 && python3 scripts/assemble.py)
# checks of the classifier
scripts/passer_layers.py, scripts/passer_check.py, scripts/xcheck2.sh, the dumprand comparison in logs/ (see the commands in section 3)
```

## 10. Files

In `kings/delegate/out/K15/`: `FINDINGS.md` (this file), `EDITS.md` (proposed edits of LOOPY, replaces the old one), `summary.json`, `fin2/` (the earlier attempt's tree, reused after the audit: `scripts/` classifiers, harnesses and queue scripts; `logs/` tables, depth and move lists, run logs; `runs/` census JSON and candidate lists; `cf/*.cmp.txt`, `cf/*.table.json` confirmation results; `chess/` inputs, outputs and logs of the kpsolve runs; `dud_groups.md` every dud group; `body_*.md` parts of this report), and `r3/` (this attempt: `scripts/`, `logs/`, `data/` root checks and Z\* inputs and outputs, `xs/` the ref3 samples, `runs/` the census re-runs; `zstar_summary.json`). Bulk batches (confirmation inputs and outputs, root dumps, validation dumps) and all binaries were deleted at the end; the scripts above rebuild them (`confirm`/`conf2.py gen` regenerate the confirmation inputs; the Python classifier's outputs `pyv/p_*.tsv` and `final/chk/py_np_5x6_pa1.tsv` and the root dumps in `val/` were deleted as well, and `pycheck.py`, `pycheck_np.py` and `grp --dumproots` regenerate them; so `r3/scripts/cmp_ref3.py` and `fin2/scripts/xcheck2.sh` need that regeneration first). The older attempts (`final/`, `v2/`, `f3/`, `pyv/`, `val/`, `runs/`, `conf/`, root files of `K15/`) are not part of this report.
