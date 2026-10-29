# K30 VERIFY: referee report on the hand proof that P7 w is a draw

Verdict: ACCEPT_WITH_FIXES. I could not refute any claim. I re-derived Lemma D, parts A, B and C by hand and re-ran
every number with my own code. Fixes: the "no referee" wording in EDITS.md (replaced in `verify/EDITS.md`) and one
cosmetic slip in PROOF.md section 2 (see "Problems").

All runs were under about 1 CPU-minute each (the longest, `myx.py`, 12 s of CPU per board), at `nice -n 15`, under
1.3 GB RSS (`myx.py`: 1.26 GB). No `heavy.sh` slot was obtained: my queued kpsolve runs waited 13 minutes and were killed by me (own PIDs
only), so chess exact was NOT re-run by me (see claim 4).

## What I reused and what I wrote

- Reused (read only): K30's position lists `logs/compare_positions_{cyl,flat}_8x8.txt`, K24's `mine.c`, K23's `ref3.cpp`,
  K24's kpsolve log `K24/logs/kpsolve_{cyl,flat}8x8.txt` (for chess).
- Not reused: any K30 code. `verify/myx.py`, `verify/mykpk.py`, `verify/mysigma.py`, `verify/mycmp.py` are mine, written
  from `SPEC.md` and the text of PROOF.md. `myx.py` first had a bug (the Black king could step onto its own pawn). My
  `mysigma.py` showed it through a count mismatch (3,403 against 3,348 tau states). I fixed it and reran everything
  quoted below with the fixed version.

## Checks

1. **Statement 0 (four White moves).** By hand (section 1 of the proof: d6, f6 attacked by e7, Kxe7 protected by kd8,
   d7 blocked by kd8): correct. My generator gives exactly {e5, d5, f5, f7} on both boards (`mysigma_*.log`).
   CONFIRMED, PROVED.
2. **Part A (White cannot win).** By hand: each of the four squares is two or more steps from d7, so ...Kxd7 is legal; White
   then has a lone king, which cannot promote and cannot give check or mate. In EPW rule tau needs a non-corner free
   neighbour. I re-checked Lemma K by hand: common neighbours of two non-adjacent kings are at most 3 (corner: at most 2),
   the own pawn (d7 or e7) is adjacent to no corner and no square next to a corner, and an edge non-corner square keeps
   at least 5-3-1 = 1 free neighbour. Correct. My own enumeration of the tau game: 3,348 White-to-move and 3,348
   Black-to-move states on cyl, 3,164 and 3,164 on flat, Black always has a tau move: exactly the claimed counts.
   CONFIRMED, PROVED.
3. **Part B (Black cannot win after Ke5, Kd5, Kf5).** By hand I checked the table of Black replies (...Kxd7, ...Kc7,
   ...e6, ...e5 and nothing else: c8 and e8 are attacked by Pd7, e7 holds the pawn), the ...Kc7 line (Ke6, then
   ...Kd8 gives X again, otherwise Kxe7), the two captures (Kxe6, Kxe5 are legal: kd8 is not adjacent to e6 or e5), free
   mode (Lemma K), and every case of Lemma D: F, M, L (r >= 4 and r = 3), the double step at r = 7 (blocked for M, F;
   handled for L), the stalemate at r = 2, and the starting positions. Each step is right as written. Details I
   re-derived: N(p') minus N(w) = {(-1,0),(1,0),(1,-1),(1,-2)} in the L case; the squares (1,-1) and (1,-2) cannot hold
   b' because all their neighbours are adjacent to w, the pawn square, or in Z_L; M is illegal exactly for b' in
   {(1,-1),(1,-2),(1,-3)}.
   Machine: my own exact solver of king + Black pawn against king (Black wins = promotion or mate of White, all pawn files,
   worklist retrograde analysis; sanity: it flags a1/d7/e7 Black to move as a Black win) gives 129,812 (flat) and
   130,176 (cyl) Black-to-move Black wins, and **0 of the 918 positions of S** are among them, on both boards. My own
   implementation of S and of the five rules of rho, written from the text: |S| = 918 per board (201 each for r = 7..4, 112
   for r = 3, 2 for r = 2); closure over every Black move: 6,777 pairs (cyl: 2,467 captures, 2 stalemates, 4,308 in S) and
   5,985 pairs (flat: 2,247, 2, 3,736); 1,488 distinct White positions on each board; no promotion, no mate of White;
   the three starts rho-map into S. All numbers equal K30's. (`mykpk_{cyl,flat}.log`.)
   Strategy tree: my own enumeration of sigma (sortie, Kc7 -> Ke6, capture of a pushed or unprotected pawn, free mode,
   rho): White-to-move states 3,694 / 3,696 / 3,696 (cyl) and 3,738 / 3,740 / 3,740 (flat) for Ke5 / Kd5 / Kf5, Black never
   has a promotion, White never mated. Equal to K30's counts. (`mysigma_*.log`.) CONFIRMED, PROVED.
4. **X = D in chess.** The hand argument is valid for chess: no promotion occurs on any play consistent with sigma, no
   Black piece other than king and pawn exists, and White is never mated, so Black cannot win; Black's Kxd7 plan shows
   White cannot win. This is PROVED by the same steps as A and B. Independent computation: K24's kpsolve log (not re-run
   by me) has X = D D on both boards with Kf7 = L in chess too (so "Kf7 loses" holds in chess as well, which K30 did not claim).
   Exact solver of the whole game (my `myx.py`, K30 material, no officers): X = D in P, EPW and EPB, both boards, with the
   four White moves valued D, D, D (sorties) and L (Kf7) in P and EPB, D for all four in EPW. `ref3` (K23, P) agrees on X, the three
   sorties after the move, Kf7 (= L) and the three KPk starts. CONFIRMED, PROVED.
5. **Part C (Kf7 loses in P).** By hand: Black plays ...e5 and pushes every move with the king on d8; before W_k the White
   king is on rank >= 8-k and the pawn on rank 6-k, so it can neither capture (needs rank <= 7-k) nor block (needs
   rank 5-k after W_k, but it is on rank >= 7-k); no White pawn can capture the pawn; the king d8 is never attacked.
   Promotion at the 4th push after ...e5, 10 plies from X. My own enumeration: 52 (cyl) and 47 (flat) White-to-move states,
   promotion only at depth 4. CONFIRMED, PROVED (in P; also in EPB).
6. **Three implementations agree (CHECKED-2).** On K30's lists of 15,536 (cyl) and 15,695 (flat) positions, my `myx.py`,
   `ref3` and `mine.c` give the same P value, and `myx.py` and `mine.c` (bb = EPW, bw = EPB) the same EPW and EPB values:
   0 differences, 0 positions illegal in my generator. My value counts equal K30's value sets (cyl P W 6,333 D 4,983 L 4,220;
   EPW W 6,363 D 9,173; EPB D 11,316 L 4,220; flat P W 6,421 D 5,030 L 4,244; EPW W 6,451 D 9,244; EPB D 11,451 L 4,244).
   (`mycmp_*.log`.) I did not re-run `kp_p --pmodel`. CONFIRMED, CHECKED-2.
7. **Not covered (CONJECTURE): P5 and other board sizes.** Agreed: nothing was run. I did not try. The proof uses
   8 ranks only through r = 7 (double step) and the rank r-3 for r >= 4. Label stays CONJECTURE for the claim "carries over".
8. **Hidden cut-offs.** None found: S, the rule and the strategy trees are finite and complete; Lemma D is a closure
   argument, not a depth-bounded search; the solvers have no depth limit.

## EDITS.md

All 11 OLD texts occur exactly once in the current LOOPY.md (dry run: 11 applied, 0 rejected, output not kept). NEW texts match
the evidence above. Fix: they say "not yet re-derived by a referee" or "no referee yet". `verify/EDITS.md` replaces that
wording (11 edits, same OLD, dry run 11 applied, 0 rejected) and adds one referee bullet to Appendix A.

## Problems (none changes a label)

- PROOF.md section 2: "the distances from d7 are 2, 2, 3, 2" should be 2, 2, 2, 2 (Ke5, Kd5, Kf5, Kf7 are all two steps from d7). The
  conclusion (not adjacent) is unaffected.
- FINDINGS.md says compare.py was "5 s of CPU"; not rechecked, immaterial.
- The invariant S is not maximal (K30 says so itself). Not a defect.

## Commands (all in this directory, `PY` = the repo venv python, `PYTHONPATH` set)

    nice -n 15 $PY myx.py cyl; nice -n 15 $PY myx.py flat        # exact P/EPW/EPB solve of the whole game; X = D
    nice -n 15 $PY mykpk.py cyl; nice -n 15 $PY mykpk.py flat    # exact KPk solve, S, rho closure
    nice -n 15 $PY mysigma.py cyl; nice -n 15 $PY mysigma.py flat   # tau, Kf7 and sigma trees
    bin/ref3 --board cyl:8x8 < ../logs/compare_positions_cyl_8x8.txt    # ref3: cc/c++ -O2 -std=c++17 K23/verify/ref3.cpp; flat: flat8x8
    bin/mine --board cyl:8x8 --model p|bb|bw < (chunks of 4000 lines)    # mine.c reads at most 4096 queries per run
    $PY mycmp.py cyl; $PY mycmp.py flat                           # needs ref3_*.out and mine_*_{p,bb,bw}.out
