# K38 referee report: hand proof that P5 w is a draw

**Verdict: ACCEPT WITH FIXES.** The hand proof is correct. I re-derived every case of Lemma D, Parts 0, A, B, C and Lemma K′ by hand, and checked each one with my own code, written from `kings/SPEC.md` and the text of PROOF.md only (I did not read K38's `p5gen.py` or `p5check.py`). All of K38's numbers reproduce.

There is one fix, about how a chess claim is labelled. K38 says that Kd5 losing in chess is CHECKED-2 on flat because of K28's `ownref`. But `ownref` (like `kq3`) has no double step. Its own run log shows "second-rank pawn seen: 1", and the Black pawn c5 stands on its second rank. So `ownref` solves a different game here and does not count as a check. My own chess solver `verify/rchess.cpp` (all of SPEC: double step, e.p., wrap, QRBN, cap 1, bounds A = B) now supplies the second check. It agrees with kpsolve cap 2 on all 15 test lines on both boards. So the chess claims are CHECKED-2 on both boards, including Kd5 = L on cyl, which K38 had as COMPUTED-1.

K38's edit texts are accurate, but they say "not yet re-derived by a referee". Use the replacement edits in `verify/EDITS.md`: the same 7 OLD texts, all 7 apply once each (`verify/logs/apply_edits.log`).

## Claim table

| # | Claim (K38) | Referee's re-run | Verdict | Label |
|---|---|---|---|---|
| 1 | X = `Kc4 Pb5 kb6 pc5` w is D in P, cyl:7x6 and flat:7x6 | I rebuilt and re-ran `kp_p --pmodel` and `ref3`/`ref3m` (`cyl:7x6`, `pln:7x6`). My own solver (`verify/rgen.py`, least fixed point) gives D. Logs: `logs/kp_p.log`, `logs/ref3.log`, `logs/rcheck.log` | CONFIRMED | PROVED (hand); also CHECKED-2 |
| 2 | X w is D in EPW and EPB; X b is W in P and EPW, D in EPB | My own solver, both boards | CONFIRMED | CHECKED-2 (K24 + referee) |
| 3 | X w is D in chess; X b is W in chess | kpsolve cap 2 re-run under heavy.sh, exact on both boards. My `rchess.cpp` at cap 1 gives A = B (exact) on both boards: D and W | CONFIRMED | w: PROVED (hand); b: CHECKED-2 |
| 4 | After Kb3, Kc3, Kd3: D; after Kd5: L, in P and in chess | kp_p, ref3m, kpsolve cap 2 and rchess, both boards | CONFIRMED | P: PROVED; C: CHECKED-2 (D entries also PROVED) |
| 5 | After a sortie and ...Kxb5, the only drawing replies are Kb3–c3, Kc3–b3 and Kd3–c3 | kpsolve, ref3m, kp_p and rchess all list exactly these | CONFIRMED | CHECKED-2 |
| 6 | After ...Ka5 Kc4 the position is D, and only ...Kb6 holds | All four solvers. The cylinder adds Kg4, Kg5 and Kg6 (all W for White) | CONFIRMED | CHECKED-2 |
| 7 | ...Ka5 right after a sortie is W in P (b6 promotes) and D in chess | kp_p and ref3: W. kpsolve and rchess: D | CONFIRMED | P: PROVED (trivial); C: CHECKED-2 |
| 8 | ref3/ref3m with `cyl7x6` or `pln7x6` give X for every position | Re-run: all X ("layers solved 0"). The code does `sscanf(board+4, "%dx%d")`, so the size is read from the fifth character on. `cyl:7x6` and `pln:7x6` work | CONFIRMED | (tool fact) |
| 9 | (0) White's only moves at X are Kb3, Kc3, Kd3 and Kd5 | By hand, and with my generator | CONFIRMED | PROVED |
| 10 | (A) White cannot win in P, EPW, EPB or chess (...Kxb5; in EPW, tau) | By hand. Also mechanically: ...Kxb5 is legal after all 4 moves; I explored tau against every White move and every Black king move (2,724 cyl / 2,788 flat nodes), 0 failures | CONFIRMED | PROVED |
| 11 | Lemma K′ (a king always has a move; on flat a corner needs the pawn not orthogonally adjacent) | By hand. Also exhaustively on both boards, all s, t, at most one own pawn anywhere, either colour: 75,348 (cyl) and 77,304 (flat) instances, 0 failures. On flat, 16 instances that the hypothesis excludes do have no king move, so the clause is needed (`logs/rlemmaK.log`) | CONFIRMED | PROVED |
| 12 | K30's Lemma K flat clause is false on flat:7x6 for these pawns, and K′ repairs it | K30's text says "if s is next to a flat corner, the own pawn is not adjacent to s". b5 is adjacent to a5 and b6, and c5 is adjacent to b6, all next to a6. True | CONFIRMED | PROVED |
| 13 | Lemma D: S has 296 positions per board (113 at r = 5, 113 at r = 4, 68 at r = 3, 2 at r = 2) and is closed under rho; Black never promotes; White is never mated | All cases re-derived by hand (below). Own coding of S and rho: 1,991 (cyl) and 1,728 (flat) Black moves. Replies: 789/693 captures, 2/2 stalemates, 1,200/1,033 back in S. 0 failures. Every position of S is D in P (my own solver) | CONFIRMED | PROVED |
| 14 | Damaged S fails the check | My own mutations: cut row y = −3 from Z_L (5 failures), the same for Z_R (5), drop the b3/d3 exclusion at r = 3 (2). All rejected on both boards | CONFIRMED | (check) |
| 15 | The starting replies after ...Kxb5 land in S | (Kb3, kb5) to Kc3, (Kc3, kb5) to Kb3, (Kd3, kb5) to Kc3; all in S on both boards | CONFIRMED | PROVED |
| 16 | (B) sigma after Kb3, Kc3 or Kd3: always defined, no promotion by either side, White never mated | Whole sigma tree with my code. White nodes: 2,824/1,824/2,824 (cyl) and 2,945/2,935/2,945 (flat). 0 failures | CONFIRMED | PROVED |
| 17 | (C) Kd5 loses in P with ...c3 c2 c1 (T = 6) | By hand (rule of the square, two pushes after the double step). Mechanically: 43 White moves checked per board, 0 failures | CONFIRMED | PROVED |
| 18 | Kd5 loses in chess: CHECKED-2 on flat (kpsolve and `ownref`), COMPUTED-1 on cyl | kpsolve cap 2 re-run: L on both boards. `ownref` is out of its domain (no double step, see the fix above), so it does not count. My `rchess` (cap 1, A = B) gives L on both boards | CONFIRMED (value); REFUTED (the stated basis: `ownref`) | CHECKED-2 on both boards (kpsolve + referee's rchess) |
| 19 | The own solver, kp_p and ref3 agree in P on 27,688 (cyl) and 28,373 (flat) positions reachable from X | I reproduced the same counts with my own solver; 0 differences against `kp_p --pmodel` and `ref3` (`logs/compare.log`) | CONFIRMED | CHECKED-2 |
| 20 | 7 edits, each OLD exactly once | `apply_edits.py` applies all 7. The content is correct except "not yet re-derived by a referee" | CONFIRMED | replaced by `verify/EDITS.md` |

## Hand re-derivation (summary of what I checked step by step)

- **Part 0.** The neighbours of c4 are b3, c3, d3, b4, d4, b5, c5 and d5. b4 and d4 are attacked by c5, c5 is protected by b6, and b5 is White's own pawn. The pawn b5 is blocked, and a6 and c6 are empty. Four moves remain.
- **Part A.** After every move b5 is unprotected: b3, c3 and d3 are two ranks away and d5 is two files away. ...Kxb5 is legal. After that, White has a lone king, which cannot promote or give check. In EPW, tau and Lemma K′ apply. Lemma K′: for non-adjacent s and t, |N(s) ∩ N(t)| ≤ 3 holds on width 7 (file distance 3 has no overlap, since s+4 ≡ s−3 ≠ s−1). In the flat-corner case, the two orthogonal neighbours u and v have N(u) ∩ N(v) = {s, d}, so t is adjacent to at most one of them.
- **Part C.** After Kd5 ...c3, the White king is on rank ≥ 4 before W1 and before W2. To capture it must stand on rank ≤ 4, then ≤ 3; to block it must reach c2, then c1. Neither is possible. White is not stalemated after ...c3, because d4, e4, e5, e6 and d6 are free. E.p. by b5 is impossible.
- **Part B.** Black's moves after the sortie: ...Kxb5, ...Ka5, ...c4, and ...c3 (only after Kb3 and Kd3). After Kb3 and Kd3, ...c4 gives check; it is unprotected and Kxc4 answers it. After ...Ka5, Kc4 is legal. Black then has Kb6, Ka4, and on the cylinder Kg4, Kg5 and Kg6. After every move except Kb6, c5 is unprotected. Kb6 repeats X, which is infinite play, a draw.
- **Lemma D.** I recomputed every set difference.
  - Case F: N(0,0)∖N(F)∖{F} = {(−1,1), (0,1), (1,1)}.
  - Case M, pawn step: {(−1,0), (1,0)}. The new M at (0,−3) exists for r ≥ 4. At r = 3, b3 and d3 are excluded, so the pawn is captured.
  - Case M, king move: F is illegal only when b′ = (±1,0). L and R are then legal and land in S.
  - Case L, pawn step: the protecting squares are {(−1,0), (1,0), (1,−1), (1,−2)}. Three of them are in Z_L, and rule 5 goes to (0,−2).
  - Case L, double step: the protecting squares (1,−1..−3) are all in Z_L, so the pawn is captured.
  - Case L, king move: M is illegal only for b′ = (1,−1..−3). (1,−1) and (1,−2) are unreachable: I verified both neighbour lists. For (1,−3), F is legal.
  - r = 3 cases: b1/b3 to c1, and the pawn step to (c1, b3) at r = 2.
  - r = 2: the moves to a2, a3, a4, b4 and c4 drop c2. ...Kc3 stalemates White (b1 and d1 are attacked by c2, b2 and d2 are adjacent to c3, and c2 is protected).
  - The flat mirror argument only names squares with |x| ≤ 2, which exist on both sides of c on flat:7x6.

  I found no gap.

## Files (all in `kings/delegate/out/K38/verify/`)

- `rgen.py`: my move generator and P/EPW/EPB solver, from SPEC.md.
- `rcheck.py`: S, rho, sigma, tau, Part C, mutations, values. Log: `logs/rcheck.log`.
- `rlemmaK.py`: the exhaustive Lemma K′ check. Log: `logs/rlemmaK.log`.
- `rchess.cpp`: my own chess solver, cap 1, flat and cyl, double step and e.p. Log: `logs/rchess.log`. Each run used under 9 CPU-seconds, under heavy.sh; the binary is deleted.
- `logs/kp_p.log`, `logs/ref3.log` (including the bad spellings) and `logs/kpsolve_cap2.log` (cap 2, both boards, under heavy.sh: 63 s and 149 s).
- `logs/compare.log`. The bulk position lists and solver outputs (`*.xz`) are compressed with xz.
- `EDITS.md`: the replacement edits.
- `pids.log`: the PIDs of my two background scripts. Both finished; nothing was killed.
