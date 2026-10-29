# VERIFY.md (referee for K29, second pass, 2026-10-29)

Verdict: ACCEPT_WITH_FIXES.

Every number I re-checked is right, and no counterexample to a claim was found. The two PROVED lemmas are right
(Lemma N1 needs one more hypothesis). Three things in K29's text are wrong or unsupported, and they carry into its EDITS.md:
1. EDITS item 6 says the exact P-win takes "4 White moves after any White move and 5 Black moves after any Black move". The movers are the wrong way round:
   the punisher moves. Correct: after every White move Black needs exactly 4 moves, and after every Black move White needs exactly 5.
2. K29 says `Kb3 Pa2 Pa4 ka5 pa3 pb4` "and its mirror" `Kb3 Pc2 Pa4 ka5 pc3 pb4` fail beside `Pf2 pf3 pf4 pf5`. Both do fail, but the second is not the mirror
   of the first. They are two different symmetry classes (the true mirror of the first is `Kb3 Pc2 Pc4 kc5 pb4 pc3`, a member of the first class).
3. K29 says the LOOPY guess (a sortie king that cannot reach the buffer in time) "does not separate survivors from failures", and EDITS 4 deletes that
   open sub-question. That is not shown. K29's own table has no group of that kind on cyl:7x6 (every enumerated group has a king sortie that can touch
   a context pawn within its exact punishment length), and no other board has sortie data. The guess is untested, not refuted.
Also: "T >= 2" in the EDITS is K29's exact-P number T_P, not the T of Definition 2.6, which was not computed for these groups. The edits must say so.
Replacement edits are in `verify/EDITS.md`. Each OLD occurs exactly once in the current LOOPY.md (`verify/scripts/chk_edits.py`: 4 of 4).

## What I reused, what I did not
- An earlier referee's report for K29 (2026-10-28, an older stage of K29) was in this file; I replaced it. I read its `verify/` files but reused no result of them.
  Everything below was run again by me. I rebuilt kpsolve, kp_p (`--pmodel`) and ref3 privately in `verify/bin/` (deleted at the end).
- Another referee instance worked in `verify/r2/` at the same time. I did not touch it, and I used `verify/me/` for my own files.
- New code of mine (`verify/me/src/`, `verify/scripts/surv.py`): `ref3d.cpp` (ref3m's move generator with my own level-synchronous exact depth to win, written new),
  `depthcmp.py`, `enum_own.py` (my enumerator: it feeds every candidate position to ref3, no code from grp.c), `surv.py`, `ctxcheck.py`, `wit.py`, `witsym_own.py`,
  `lowmoves.py`, `mech_own.py`, `orbits_own.py`, `dist2.py`, `gen3.py`, `chk_edits.py`.
- Solver pairs: Phi by `kp_p --pmodel` (kpp) and ref3; Psi by `kpsolve --frozen` (kp) and `ref3 --frozen`. kp and kpp share one source ("kp family"); ref3 shares nothing with them.
  `ref3d` shares ref3m's move generator, so it is not independent of ref3 on legality; it is independent of grp2 for the depths.

## Results per claim

### 1. Four cyl:7x6 classes act as 0 beside all 885 contexts (CHECKED-2): CONFIRMED
- `verify/scripts/surv.py cyl:7x6 cyl:7x6 ef a1 a6` with the four groups `Kb3 Pa2 Pc2 kb1 pa3 pc3`, `Kb1 Pa2 Pb3 ka3 pb2 pc5`, `Kb3 Pa2 Pa4 ka5 pa3 pb4`, `Kb3 Pc2 Pa4 ka5 pc3 pb4`.
  My own context generator (files e,f, ranks 2-5, at most 2 pawns a side, 885 contexts, both sides to move, e.p. "-", 1,770 positions per group).
  Result (`verify/logs/surv_cyl7x6_f3.txt`): Psi from kp and ref3 agree on all 1,770 positions; for each group Phi from kpp and ref3 agree on all 1,770;
  Phi = Psi in all 885 contexts, for both pairs. No illegal position (X count 0). (404 CPU-s in all; see "Rule deviations".)
- Parking: Psi with the kings parked on `Kb1 kc6` and on `Kc3 ka4` equals Psi on `Ka1 ka6` in all 1,770 positions (ref3 --frozen; 0 differences).
- T_P: my own exact depths (`ref3d`) give loss depths 8 and 10 plies for `Kb3 Pa2 Pc2 kb1 pa3 pc3`: all five White moves have T_P(m) = 4 and both Black moves have T_P(m) = 5, so T_P = (4, 5).
  `Kb1 Pa2 Pb3 ka3 pb2 pc5`: 4 and 16 plies, White moves T_P = 1 (Kb1c2) and 2 (Pb3b4), Black moves 4 and 8: T_P = (2, 8). The two (6, 7) groups: 12 and 14 plies.
  Note that White's side of the (2, 8) group has T_P <= 2: the group is "T_P >= 2 on both sides" only in the weak sense 2 and 8.
- Label CHECKED-2 is right.

### 2. Same classes on other boards; 107 survivor classes re-checked (CHECKED-2): CONFIRMED on a sample, rest NOT_CHECKED
Own runs, two solver pairs, all contexts of the stated set, 0 differences and 0 solver disagreements each (through heavy.sh):
- cyl:8x6, contexts on e,g (885): `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5` (`verify/logs/me_surv_cyl8x6_eg_1.txt`, `_2.txt`).
- flat:7x6 with F_Z = c-e, contexts on a,g (885), parked kings `Kc1 kc6`: `Kd3 Pc2 Pe2 kd1 pc3 pe3` and `Kd1 Pc2 Pd3 kc3 pd2 pe5` (`me_surv_flat7x6_z2_ag_1.txt`, `_2.txt`).
- flat:7x6 with F_Z = a-c, contexts on e,f (885), parked kings `Ka1 ka6`: `Kb3 Pa2 Pc2 kb1 pa3 pc3` (`me_surv_flat7x6_ef_1.txt`).
- One-file runs (63 contexts on f), 14 random survivor classes: cyl:7x6 f4 (6 groups), cyl:8x6 f4 (4), flat:7x6 f4 (4): all 14 survive (`verify/logs/me_surv_f4_*.txt`).
Not re-run by me: the other verified classes (I re-ran 9 of the 107 on 885 contexts and 14 of them on the 63-context sets) and the 15 d3 classes. K29's own `data/ver_*.cmp` has 122 lines (107 main + 15 d3), every one with 0 differences (I checked the lines).
Counts of verified classes (4+28+4+17+5+4+45 = 107) and screen-only classes (70) add up. A survivor of a one-file context set (63 contexts) is a weak statement, as K29 says.
Note on the summary text: "the same classes survive ... flat:7x6 (885 on e,f)" holds for two of the four (K29's table: `Kb3 Pa2 Pc2 kb1 pa3 pc3` and the (2, x) class), and all four survive on flat:7x6 with F_Z = c-e.

### 3. 269 classes fail, confirmed by two solver pairs; 96 members (CHECKED-2): CONFIRMED
- All 278 witnesses of `data/table_all.tsv` (269 main + 9 d3) re-solved with my `wit.py` (kpp and ref3 for Phi, kp --frozen and ref3 --frozen on the parked-king position):
  278 of 278 confirmed (same pair from both P solvers, same pair from both frozen solvers, Phi != Psi, no illegal position). Log: `verify/logs/me_wit_all_full.txt`.
- Symmetric images: for 227 of the 269 failing representatives (nine configurations; not flat:8x6 f4) I mapped group and witness by a random symmetry (colour swap with rank flip,
  and the file reflection of F_Z where it is a board symmetry) and solved the image: 227 of 227 confirmed (`verify/logs/me_witsym.txt`).
- Counts: 12+38+13+48+13+12+55+13+23+42 = 269 failing classes, 4+28+4+17+5+4+45+5+7+58 = 177 surviving, 446 in all.

### 4. `Kb3 Pa2 Pa4 ka5 pa3 pb4` and its "mirror" fail beside `Pf2 pf3 pf4 pf5` (CHECKED-2): CONFIRMED, with a wording fix
Both `Kb3 Pa2 Pa4 ka5 pa3 pb4` and `Kb3 Pc2 Pa4 ka5 pc3 pb4` give Phi = (L, D) and Psi = (L, W) in kpp, ref3, kp --frozen and ref3 --frozen (`verify/me/src/ctxcheck.py`).
The same context leaves `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5` at Phi = Psi. But the second group is not the mirror of the first (see the verdict, point 2;
`verify/me/src/` orbit computation: the class of the first has four members and does not contain the second).

### 5. No failing context among contexts 0-2681 of 3,237 for two groups (COMPUTED-1): NOT_CHECKED as a whole; sample agrees
I did not repeat the 2,682 contexts. My sample: for each of `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5`, 60 random contexts of five or six pawns and 80 random contexts of four pawns
(at most three a side, on e,f), kpp, ref3, kp --frozen and ref3 --frozen: 0 failing contexts, 0 solver disagreements (`verify/logs/me_c3_*.txt`, seeds 101 and 202 in `verify/me/run_c3.sh`).
Context counts re-derived: 3,237 = 93+512+1,176+1,456; at most 5 pawns: 2,677; six-pawn contexts: 560. The sample is small next to the six-pawn tier (not run by K29, 560 contexts).
The label COMPUTED-1 for the full run stays; my sample is two solver pairs on 140 contexts per group, no more.

### 6. Independent depth-3 check, 12 moves with punisher length <= 2 (CHECKED-2): CONFIRMED
With `ref3d` (full exact depth, not only a depth-3 test) on the 20 (group, configuration) survivor pairs of cyl:7x6 f3, flat:7x6 f3 z0 and z2, and flat:8x6 f3 z2: the moves with T_P(m) <= 2 are exactly
Kb1c2, Kb1a2, Kd1e2, Kd1c2 (T_P = 1) and Pb3b4, Pd3d4 (T_P = 2): six distinct moves, 12 occurrences over the 20 pairs (Kb1c2 2, Kb1a2 1, Kd1e2 2, Kd1c2 1, Pb3b4 3, Pd3d4 3), as K29 says (`verify/me/src/lowmoves.py`). Every one of the 20 has a sortie with T_P >= 3.
Note: this is vacuous as a filter. All 1,236 candidates have a loss depth of at least 10 plies for one side (T_P >= 5), so every candidate has such a sortie.

### 7. Lemma: T_P(m) >= 3 excludes a T = 1 certificate (PROVED): CONFIRMED (conditional on Theorem 2.7(a), which LOOPY lists as PROVED after repair)
Re-derived. Theorem 2.7(a) with T = 1: if LC_1(m) holds at Y with reply r, then s-bar plays r and wins by its next move, a promotion or a mate. That is a forced win within 3 plies after m
(r, any move of s, the winning move), so the exact depth d(m) <= 3 and T_P(m) = (d(m) + 1)/2 <= 2. The bare group is a position Y of Definition 2.1 (kings and Z-pawns on F_Z, no context), m is a
legal non-promoting Z-move, (L2) is vacuous. So T_P(m) >= 3 contradicts the existence of LC_1(m). Correct. What it does not give: the T of the local game is not computed, so "T >= 2" in the sense of Definition 2.6 is not established
(it says only that the T = 1 route of Proposition 2.10(a) is closed for that sortie).

### 8. Lemma N1 (stalemate) (PROVED): CONFIRMED with one hypothesis added
The proof is right with this addition: the statement must also assume that s is NOT in check in Z. If s is in check in Z and all its legal moves are covered, s is mated beside G (value L, equal to Psi), not stalemated.
The proof's remark "s is not in check (context pawns do not attack F_Z)" shows only that G adds no check. Everything else holds: by Lemma 2.2 the context neither occupies nor attacks F_Z, the Z-moves are the same in Z+G as in Z,
the exit squares are on the buffer files, G gives s no pawn move, and the parked king has a step and loses at once in the frozen model. Example checked: `Ka1 Pb2 Pa3 kb3 pa2 pa4 pf3`, White to move
(cyl:7x6): kpp gives `D D`, ref3m gives D with no move (Kg2 is covered); without pf3 the only White move is Ka1g2; the parked frozen position `Ka1 ka6 pf3` is L for White to move (ref3 --frozen).
The 47 stalemate witnesses are all stalemates in P (Phi = D side), so they do not rely on the missing hypothesis.
The closing remark "a universal zero needs ... at least three coverable exit squares" is an unproved heuristic, not part of the lemma.

### 9. Race predictor "T_P >= 5 forces failure" is false (COMPUTED-1): CONFIRMED for the counterexample; the last sentence of the claim is REFUTED as worded
`Kb1 Pa2 Pb3 ka3 pb2 pc5` has Black sorties Ka3g2 (T_P = 4, d = 7) and Ka3g4 (T_P = 8, d = 15) onto the buffer file g (ref3d `--moves`), and acts as 0 beside all 885 contexts (claim 1, also on cyl:8x6 and flat:7x6). The numbers are CHECKED-2 (my solver and grp2 agree on every depth of all 1,236 groups).
The sentence "The guess in LOOPY section 8 item 6 ... does not separate survivors from failures" is not shown. LOOPY asks about groups in which NO sortie king can reach the buffer in time. K29's sortie table (`data/S/S_cyl7x6_f3.txt`, the only configuration with such data) has, for each of the 16 classes,
at least one king sortie with e(m) <= T_P(m) (I recomputed this from the table: 0 classes with all king sorties too slow), so no group of that kind exists on cyl:7x6 f3, and nothing was computed for the other nine configurations. e(m) is a lower bound on the touching time, so even "e <= T_P" does not prove that the king gets there.
The survivors' statement "sortie kings do reach the buffer" holds as a plain fact for three of the four (they have sorties that land on file g at once); for `Kb3 Pa2 Pc2 kb1 pa3 pc3` the king needs two moves.

### 10. Mechanism counts (COMPUTED-1): CONFIRMED for agent A's table; agent B's counts NOT_CHECKED
- Agent A, 271 lines: the 224 "A escape" lines (buffer sortie 124, stalemate 47, step inside F_Z 45, pawn move 8) were re-classified by my own code from ref3m `--moves` (non-losing moves of the side to move, by type of move): 224 of 224 identical to K29's tags (`verify/me/src/mech_own.py`).
  The 47 "B refuted" lines (34 + 13) are consistent in the table but I did not re-derive them.
- 267 of the 269 first failing contexts have a pawn at file distance exactly 2 (I recomputed it from the table; the other two are the flat:7x6 f4 ones with `Pg2 pg4 pg5` and `Pg2 pg3 pg4`, distance 3).
- Agent B's totals (98, 51, 47, 46, 39 = 281): arithmetic only.

### 11. Enumeration: 1,236 groups, 446 classes, grp and the referee's enumerator agree (CHECKED-2): CONFIRMED
- My enumerator (`verify/me/src/enum_own.py`; every pawn set with 0-2 white and 0-2 black pawns, at least one pawn, on F_Z, ranks 2-5, both kings on any F_Z square; each position sent to ref3 for both sides to move; keep (White to move L, Black to move W)) gives exactly K29's sets in all ten configurations:
  60, 264, 62, 260, 36, 200, 58, 36, 200, 60 groups (`verify/logs/me_enum_f3.txt`, `me_enum_*_f4.out`; 0 only-mine and 0 only-K29 in every one). About 2.8 million positions per three-file board and 16.3 million per four-file board.
- Exact depths: `ref3d` gives (L, W) and the same two loss depths as the K29 enum files for all 1,236 groups (`verify/logs/me_depth_f3.txt`, `me_depth_f4.txt`). Smallest larger depth 10, largest 38. 202 groups have a side with T_P = 1 (loss depth 2). Of the 221 surviving classes, 201 have T_P >= 2 on both sides and 20 have T_P = 1 on one side (as K29 says).
- Orbits (`orbits_own.py`): 16, 17, 18, 16, 18, 30 classes for the six three-file configurations (colour swap with rank flip; reflection of F_Z where it is a board symmetry); the lists are closed. The four-file classes 66, 65, 100, 100 and the total 446 equal K29's rep files (I did not recount the four-file orbits; the earlier referee did).
- No hidden cut-off found in the enumeration. The restrictions are those K29 states (pawns only on F_Z, at most 2 a side, ranks 2-5, no e.p.); they are limits of the search, not theorems.

## Edits
`EDITS.md` of K29: all four OLD blocks occur exactly once in the current LOOPY.md. The NEW blocks are accurate except for these points, fixed in `verify/EDITS.md`:
1. Item 6: "4 White moves after any White move and 5 Black moves after any Black move" (wrong movers).
2. Item 6: "`Kb3 Pa2 Pa4 ka5 pa3 pb4` and its mirror" (the second group is a different class).
3. Item 6: "on the wider boards two context files, or a 300-context screen": the |F_Z| = 4 boards used one context file (63 contexts).
4. Item 6: "the guess ... is not what separates them: the survivors' sortie kings do reach the buffer" is not shown (claim 9). Replaced by the plain statement that the guess was not tested.
5. Items 2-4: "T >= 2" for groups whose local-game T was not computed. Replaced by "a sortie of exact punishment length >= 3 (no T = 1 certificate)".
6. Edit 4: it deletes the open sub-question "groups in which no sortie king can reach the buffer in time". K29 did not settle it. Kept as open.
7. The "2,682 of 3,237" figures are correct and stay; my 140-context sample per group is added to the text.

## Rule deviations (mine)
- `scripts/surv.py` on the four cyl:7x6 survivors ran without heavy.sh: 404 CPU-s in all (about a dozen solver processes of at most about 50 CPU-s each, nice 15, RSS at most about 0.3 GB on the samples I saw). I saw it would pass one CPU-minute in total, tried to stop it by PID, and the permission layer refused the kill, so it ran to the end.
- All other unlocked runs were short (the longest 51 CPU-s: the flat:7x6 f4 witness batch). Runs through heavy.sh: survivor runs on cyl:8x6, flat:7x6 (885 contexts each), the three four-file enumerations, the 140-context samples (`verify/me/run_*.sh`; the PIDs of the chains are in `verify/logs/me_pids.log`).
- No git, no pkill, no network, no installs, nothing written outside `kings/delegate/out/K29/verify/` and this file.

## Files
`verify/EDITS.md` (replacement edits), `verify/scripts/` (surv.py, chk_edits.py and the earlier referee's scripts), `verify/me/src/` (my code), `verify/me/run_*.sh`, `verify/logs/me_*`, `verify/me/depth_*.txt`, `verify/me/enum_own_*.txt`, `verify/summary_refB.json`.
`verify/bin/` and bulk position files are deleted at the end.
