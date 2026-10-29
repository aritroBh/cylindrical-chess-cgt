# K30 VERIFY (second referee round, 2026-10-28): the hand proof that P7 w is a draw

Verdict: ACCEPT_WITH_FIXES. I could not refute any claim. I re-derived Part 0, A, B and C and every case of Lemma D by
hand, then re-checked every number with new code written from `kings/SPEC.md` and the text of `PROOF.md` only. The fixes
are small: a replacement `verify/EDITS.md` (12 edits, one more than K30's, and a longer referee bullet in Appendix A), and two
wording slips in K30's files (see "Problems"). No label changes.

An earlier referee round had stopped files in `verify/` (its report is kept as `verify/r2/VERIFY_earlier_referee.md`, its EDITS as
`verify/r2/EDITS_earlier_referee.md`). This report replaces `VERIFY.md`.

## What I reused and what I wrote

- Reused, read only: K30's position lists `logs/compare_positions_{cyl,flat}_8x8.txt`; the solver sources K23 `ref3.cpp`, K24 `mine.c`,
  K7 `kp_p.c`, and `kings/kpsolve.c` (built privately, binaries deleted); K30's `PROOF.md`, `FINDINGS.md`, `summary.json`, `EDITS.md`,
  `pids.log`. I did not re-run K30's own scripts (they write into K30's `logs/`, which is outside my output directory).
- Re-run as a consistency check only: the earlier referee's `verify/mysigma.py` and `verify/mykpk.py` (they are the reproduce
  commands of the claims). Same numbers as before (`verify/r2/reuse_*.log`). I did not re-run its `myx.py` and `mycmp.py`; my `r2_x.py`
  and `r2_k30list.py` replace them.
- Written new by me, in `verify/r2/`: `r2_lib.py` (board, move generator with check, pawns, promotion terminal; whole-game retrograde
  solver for P, EPW, EPB), `r2_kpk.py` (own exact king + Black pawn against king solver for all pawn files; the invariant S and the
  five rules of rho coded from the text; closure check), `r2_tree.py` (the tau, Kf7 and sigma trees), `r2_x.py`, `r2_dump.py`,
  `r2_cmp.py`, `r2_k30list.py`, `r2_lemmaK.py`, `r2_kpk_mut.py`. No line of K30's code or of the first referee's code was used. A first run of `r2_tree.py`
  stopped on two gaps of my own (it did not encode Kxe7 after Kc7, Ke6, Kb6; and it asserted that Black always has a move, while a
  Black king alone can be stalemated, which is a draw). I fixed my code, not the proof.
- All runs under 15 CPU-seconds, `nice -n 15`, no `heavy.sh` slot needed. The longest were the two kpsolve runs (9.5 CPU-s each,
  1.13 GB and 1.04 GB RSS). No pkill, no git, nothing written outside `verify/`. My only background job was one zsh loop that ran the two
  kpsolve runs; it has ended (pid file deleted). Binaries and bulk files are deleted; `verify/` is 264 KB.

## Claim by claim

1. **P7 w is D, PROVED (cyl:8x8 and flat:8x8; P, EPW, EPB, chess).** CONFIRMED.
   - Statement 0 (four moves): by hand (d6, f6 attacked by e7; Kxe7 protected by kd8; d7 blocked by kd8). My generator gives
     exactly e5, d5, f5, f7 on both boards (`r2_x_*.log`).
   - Part A: by hand, each of the four squares is two steps from d7, so ...Kxd7 is legal (checked by generator after each). A lone king cannot
     promote or mate. For EPW, tau (never move the pawn, step to a free non-corner neighbour) always has a move by Lemma K.
     **Lemma K checked exhaustively** (`r2_lemmaK.py`): for every pair of non-adjacent king squares and each own pawn in {none, d7, e7}, a free
     neighbour exists (0 failures in 10,484 cyl and 10,616 flat cases), and a free non-corner neighbour exists when s is not a corner;
     the common-neighbour bound is 3 (corner: 2, flat), as written.
     My tau tree: 3,348 (cyl) and 3,164 (flat) White-to-move states with the pawn still on e7 (6,916 and 6,536 if K against K
     states are counted too); Black always has a tau move; no state is a White win in EPW. The counts equal K30's.
   - Part B: by hand, the table of Black replies (Kxd7, Kc7, e6; and e5 after Kd5, Kf5) is complete (generator: exactly these, also
     the five replies after Kc7, Ke6). The Kc7 line, the captures Kxe6 and Kxe5, free mode (Lemma K) and the starting positions of
     Lemma D are right. In EPB the only place where White must not promote is free mode; Lemma K covers it.
   - Lemma D re-derived case by case (F, M, L with r >= 4 and r = 3, the double step at r = 7, the stalemate at r = 2, the starts). I
     recomputed the neighbour differences used: N(p') minus N(w) = {(1,-2),(1,-1),(1,0),(-1,0)} in case L; N(M) minus N(L) = {(1,-3),(1,-2),(1,-1)};
     N(F) minus N(M) = {(-1,0),(1,0)}; the squares (1,-1), (1,-2) cannot hold b' since all their neighbours are adjacent to w, the pawn
     square or in Z_L. The seam of the cylinder plays no role (every neighbour set used has files within three of the e file, and a and h
     are never both involved). Correct as written.
   - Machine (own code, `r2_kpk.py`): |S| = 918 per board (201 for r = 7..4, 112 for r = 3, 2 for r = 2); 0 of them is a Black win in my exact
     solver (326,640 cyl and 331,352 flat KPk states; 130,176 and 129,812 Black-to-move Black wins, 97,584 and 103,616 White-to-move); closure
     over every Black move: 6,777 pairs on cyl (2,467 captures, 2 stalemates of White, 4,308 replies in S) and 5,985 on flat (2,247, 2, 3,736); 1,488
     distinct White-to-move positions per board; 0 failures; none of those White-to-move positions is a Black win. The three starting
     positions map into S (Ke5 -> d5; Kd5, Kf5 -> e5). Every number equals K30's.
   - Mutation: cutting one row from Z_L gives |S| = 934, 16 Black wins inside S and 18 closure failures; dropping the d3, f3 exclusion at
     r = 3 gives 2 Black wins and 2 failures (`r2_mut.log`). So S is tight at those two places and the check has teeth.
   - Sigma tree (`r2_tree_*.log`): White-to-move states for Ke5, Kd5, Kf5: cyl 3,694 / 3,696 / 3,696 (3,341 free mode), flat 3,738 / 3,740 / 3,740
     (3,385). Black has no promotion move in any visited state; White is never mated; White is stalemated once (the r = 2 line); no visited state
     is L in EPB or in P. Equal to K30's counts.
2. **Black cannot win after Ke5, Kd5, Kf5, PROVED.** CONFIRMED (same evidence). Whole-game exact solve (below): the three sortie
   positions are D in P, EPW and EPB.
3. **Kf7 loses in P, PROVED.** CONFIRMED. By hand (rank argument: before W_k the White king is on rank >= 8 - k, the pawn on rank 6 - k, so it can neither
   capture nor block; the king d8 is never attacked; promotion on the 4th push, 10 plies from X). My enumeration: 52 (cyl) and 47 (flat)
   White-to-move states, no White move captures the pawn, the push is always available, promotion only at push 4, every such state is L in P. ref3
   gives Kf7 = L on both boards. Extra: Kf7 is also L in chess (kpsolve exact, below); the proof does not claim that.
4. **Chess value D, PROVED directly.** CONFIRMED. The hand argument uses no promotion, no officer, and no Black promotion move exists on any play
   consistent with sigma. Independent computation: **kpsolve exact in chess, re-run by me** (`kp_cyl.out`, `kp_flat.out`; cap 1, lower and upper bounds equal): X = D D on both boards,
   after Ke5, Kd5, Kf5 the position is D D (Black's replies: Kxd7 D, Kc7 D, e6 W, and e5 D), after Kf7 it is L L. The first referee had not re-run this (no lock slot).
5. **Implementations agree (CHECKED-2).** CONFIRMED, and stronger than claimed. On K30's own lists (15,536 cyl and 15,695 flat) my own solver, `ref3` (P), `mine.c` (P, EPW, EPB) and
   `kp_p --pmodel` (P) give the same value everywhere: 0 differences (`r2_k30list_*.log`). Value sets equal K30's (cyl P W 6,333 D 4,983 L 4,220; EPW W 6,363
   D 9,173; EPB D 11,316 L 4,220; flat P W 6,421 D 5,030 L 4,244; EPW W 6,451 D 9,244; EPB D 11,451 L 4,244). On every position reachable from X (92,598 cyl and 93,830 flat, from
   my generator, 3 models): 0 differences against `ref3`, `mine.c` (all three models) and `kp_p` (`r2_cmp.log`, `r2_dump.py`). X = D in P, EPW and EPB, both boards (`r2_x_*.log`).
   Kf7 is L in P and EPB and D in EPW.
6. **P5 and other boards carry over, CONJECTURE.** NOT_CHECKED. Nothing was run, by K30 or by me. The label is right.

Side remark of FINDINGS checked: with Black to move, pawn e7 and kd7, the White king also draws from d3 and e3 (ref3, both boards) and loses from c3. So S is not maximal, as stated.

## EDITS

K30's `EDITS.md`: all 11 OLD texts occur exactly once in the current `kings/theory/LOOPY.md` (modified 2026-10-28 01:58, md5 3da46b286b59cee5da28df055df1d1f3), also one by one after
the earlier edits are applied; `apply_edits.py` dry run: 11 applied, 0 rejected. The NEW texts are accurate against the evidence above (918 positions, 15.5k positions, three
implementations, Kf7 for P only, P5 still open). Remaining mentions of "no hand proof" in LOOPY are about P5 or other items, so no edit is missing there.
One stale sentence remains: §2.7a, "Application", says "not a hand proof of the draw in P" (about the lemma). `verify/EDITS.md` adds a note there
(edit 12) and extends the Appendix A bullet with this second round (kpsolve exact re-run, `ref3`, the mutation test). Dry run of all 12: 12 applied, 0 rejected.
Tags use "2026-10-27" as the task asks.

## Problems (none changes a label)

- `FINDINGS.md` says all runs were "under 300 MB RSS" and `summary.json` has `max_rss_mb: 300`, but `pids.log` records an aborted `compare.py` at 5.5 GB (killed by the author,
  above the 3 GB limit). Wording should say so. No numbers are affected.
- `PROOF.md` section 4.1 says "Name five squares" and lists four (F, M, L, R). Cosmetic.
- `PROOF.md` section 5 calls the proof "board-independent in its logic". The proof uses 8 ranks and the files c..g; only cyl:8x8 and flat:8x8 were checked. Read it as CONJECTURE beyond those.
- Lemma D is proved by hand and by a finite closure check on each of the two boards; the "PROVED" label is fair for these two boards. It is not a proof for other sizes.

## Boundary of negative results

No hidden cut-offs: the solvers explore the whole reachable graph with no depth limit; S, rho and the sigma trees are finite; kpsolve's "depth 8" is its layer count, and bounds A and B are equal.
En passant cannot arise in this family (the only White pawn is on d7); `ref3`, `mine.c` and `kpsolve` have e.p. on and agree with my e.p.-free generator. Not run: P5, other board sizes, kpsolve on 7-rank or 6-rank analogues.

## Commands (all in `verify/r2/`; PY = repo venv python, PYTHONPATH = repo root)

    K=/Users/aritro/Downloads/Research/Chessendgames/kings; mkdir -p bin
    c++ -O2 -std=c++17 -o bin/ref3 $K/delegate/out/K23/verify/ref3.cpp; cc -O2 -o bin/mine $K/delegate/out/K24/scripts/mine.c
    cc -O2 -o bin/kpp $K/delegate/out/K7/scripts/draft/kp_p.c -lpthread; cc -O2 -o bin/kp $K/kpsolve.c -lpthread
    for b in cyl flat; do nice -n 15 $PY r2_kpk.py $b; nice -n 15 $PY r2_tree.py $b; nice -n 15 $PY r2_x.py $b; nice -n 15 $PY r2_k30list.py $b; done
    nice -n 15 $PY r2_lemmaK.py; MUT=1 $PY r2_kpk_mut.py cyl; MUT=2 $PY r2_kpk_mut.py cyl
    nice -n 15 $PY r2_dump.py cyl   # writes all_cyl.txt, own_vals_cyl.json, compares with ref3; then run mine.c (models p, bb, bw, chunks of 4000 lines, needs ref to bin/mine) and bin/kpp --pmodel on all_cyl.txt, and $PY r2_cmp.py cyl
    nice -n 15 bin/kp --board cyl:8x8 --cap 1 --moves < q5.txt     # and flat:8x8; about 10 CPU-s, 1.1 GB
