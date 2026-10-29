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
