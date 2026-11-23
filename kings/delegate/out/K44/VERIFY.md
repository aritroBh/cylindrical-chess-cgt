# K44 referee report (king-against-king fights, LOOPY section 8 question 3), 2026-11-22

AI work, no human re-derivation. Labels: nothing here is PROVED (solver results only); CHECKED-2 means two independently
written implementations agree.

## Verdict

**Accepted.** Every number I re-ran agrees, with 0 differences. I used my own solver `verify/rk.cpp`, written from K20's definition text
(`kings/delegate/out/K20/summary.json`, "definition") and LOOPY Definitions 1.1 to 1.3. I did not read `kg44.cpp`, `lk_ref.cpp` or
`lk3.py`. I raised some labels because `rk` now reproduces results that were one implementation only (COMPUTED-1). The replacement
edit set is in `verify/EDITS.md`. No claim had to be withdrawn.

## The referee's solver

`rk` builds the LK game graph from the roots: kings step inside the region, own pawns block, enemy pawn attacks are tested after
the capture, and a capture that leaves exactly one side with a passer is a terminal for that side. It builds the 34 B34 games
explicitly (on = {on|}, off = {|off}, dud, over = {0|over}, under = {under|0}, tis = {tisn|}, tisn = {|tis}, integers, 1/2, up and so on).
It solves the D-sum G + K by retrograde analysis on (G node, K node, mover). A move to a terminal ends the play, a player with no
move loses, and an undecided state is a draw. It names a root when its 68-outcome signature equals that of a reference game H + K.
Options: a coarsest-bisimulation quotient (`RK_BISIM`), and contexts made of every sum of two B34 games (`RK_PAIRS`, 629 contexts).

Sanity check against K20: flat:6x6 `Kc3 ka4 Pa2 pa3 Pc4 pc5` is 0, tis, +1 and +1 with the kings confined to {a..c}, {a..d}, {a..e}
and the whole board. `Kd3 ka4` is {1|0} with {a..e}, and it is the same on flat:7x6 and 8x6. cyl:6x6 `Kd3 kd1 Pa2 pa3` is +1. All of
these match LOOPY.

## Results

| Claim | Referee check | Result |
|---|---|---|
| Configuration lists: 2,131 cases (60, 396 and 1,675 by number of pairs) | own count of classes up to rotation and reflection, window 6, ranks 2 to 4 | 76, 102, 135, 162, 177 free configurations for W = 6..10 (177 for 11 and 12) = cfg/ files; 2,131 cases; agrees |
| Every case of W = 6..10, all regions | `verify/cmp_rk.py`: multiset {B34 signature: roots} of every case against kg44's `logs/fsig_new_*` | 2,131 cases, 1,756,517 root entries, **0 differing cases**. The 23 deleted fsig files cover only W = 6 m0, m1, m2 and W = 7 m2 among the new runs; those 129 cases were run by rk without a comparison file, and their class counts still enter the totals below |
| Class totals (0 2,996; * 76; +-1 98; over and under 4; {1|0} and {0|-1} 21; tis and tisn 336; {on|off} 3,938; dud 88,554; on and off 64,078; decisive 646,164; unclassified 885,715) | sum of rk's per-case classes (`verify/agg_rk.py`) | all equal |
| Baseline: 1,137 signatures (967 cyl, 676 flat); distinct-root counts as K20 | `verify/base_rk.py`, K20's enumeration re-run by rk (2,327 cases) | 967, 676, 1,137: equal |
| 2,976 signatures in the new runs, 1,909 absent from the baseline | set difference of rk's sets | 2,976 and 1,909: equal (`verify/new_minus_base.txt`) |
| over: cyl:10x6 a2 c4 f2, `Kc3 ka4`, `Kc3 ka5` (2 of 1,994 roots); under: a2 c4 h4, `Kc2 ka4`, `Kc3 ka4` | rk, all roots | equal; the full class table of both configurations equals kg44's (0 8, unclassified 1,055 with 48 signatures, on, off, over or under 2) |
| over against every sum of at most two B34 games (629 contexts, both movers) | `RK_PAIRS=over` | 0 mismatches for both over roots; 0 for both under roots against under. Control: `Kc3 ka6` has 239 mismatches |
| over not on cyl:9x6; over on 11x6, 12x6, 13x6, 14x6, 16x6, 10x7 (also `Kc4 ka5`, `Kc4 ka6` for a3 c5 f3) | rk, all roots | equal. Also none on cyl:9x7 (referee only, COMPUTED-1) |
| +1 family on files -2, 0, 2 at ranks 4, 2, 3: one root on every W = 7..12, none on W = 6 | rk | `Kf3/Kg3/Kh3/Ki3/Kj3/Kk3 ka4`: +1 on W = 7..12; on cyl:6x6 the root `Ke3 ka4` is 0 and the configuration has no +-1; the colour mirror on cyl:7x6 `Kc3 ka4 ... Pe3 pe4` is -1 |
| +1 and integer 1 in pair contexts | `RK_PAIRS=+1` on cyl:7x6 and 9x6 roots, `-1` on the cyl:7x6 mirror | 0 mismatches in 629 contexts |
| Free +1 totals W = 6..12: 17, 6, 26, 4, 30, 9, 29 | rk | equal. Every +-1 root on an odd width is a three-pair root (32 on W = 7, 9; 18 on W = 11); none with one or two pairs |
| Switches cyl:8x6 `Kf3 ka4 a2 c3 g4` {1|0}, `Kc3 kh4 a2 c4 e3` {0|-1}; * roots `Kg2 kh4` (cyl:9x6), `Ke2 kf4` (cyl:7x6), `Kc2 kb4` (cyl:8x6) | rk | equal |
| Short roots in box(0) of cyl:8x6 `Ka1 kc1 Pa2 pa3 Pc2 pc3` {|-}, `Kb5 ka1 Pa4 pa5 Pc4 pc5` {+|} | rk (region a-c) | names equal. I did not re-run the acyclicity counts (80 short roots, none outside box(0)) |
| W = 11, 12 free totals (0 439 + 455, * 8 + 8, +1 9 + 29, {1|0} 3 + 3, tis 26 + 33, {on|off} 1,165 + 1,283, dud 1,212 + 1,418) | rk, all 177 configurations each | the sums over 11 and 12 are equal, and so are the +1 counts per width. Under is on a2 c4 i4 (11) and a2 c4 j4 (12), as reported |
| Smallest new value `Ka1 kb6 Pa3 pa4 Pe3 pe4`, cyl:8x6: its signature row, 1,332 nodes, 353-node quotient, 3,526 option edges; `Kb1 ka5` also 353 | rk and `RK_BISIM` | equal. The four configurations a2 e2, a2 e4, a3 e3, a4 e4 give exactly 4 new signatures, and no new-signature root of them has a quotient smaller than 353 |
| over root: 1,994 nodes, no reduction by bisimulation; 337-node new value `Kd3 ka4 a2 c2 e4` in box a..e | rk | equal (the over root has 21,153 distinct option edges in the quotient) |
| P model: ref3m equals kp_p; D = P in 52,814 of 57,030 (cyl:7x6), 52,992 of 57,944 (cyl:8x6), 6,980 of 12,050 (non-faithful), 7,488 of 7,976 (cyl:10x6) | `verify/p_check.py` on the K44 logs. The LK "alone" column of every key line was recomputed by rk | the LK column has 0 differences (all 135,000 legal lines). ref3m and kp_p differ on 0 lines, with no gap between kp_p's bounds. All agreement counts and percentages are equal. I did not re-run the P solvers themselves (their agreement is K44's two-solver result) |
| EDITS.md applies | `apply_edits.py` on a copy | 6 applied, 0 rejected; LOOPY.md unchanged. The same holds for `verify/EDITS.md` |

## Remarks (no change of substance)

1. "Canonical form" (brief item 2): K44 gives the bisimulation-minimal game graph. For a loopy game that is not a stopper this
   is not a CGT canonical form, and the report says so ("in the only sense available"). That is acceptable. The brief's request
   is answered by this graph plus the B34 signature, not by a canonical form.
2. "Equals over" is battery equality: B34, B4553, the 23,716-game battery and the 629 pair contexts, now also checked by rk. It is
   not equality in all sums, and the edits say so.
3. Labels raised (`verify/EDITS.md`): over on 13x6, 14x6, 16x6 and 10x7 (lk and rk); the class totals of the 2,131 cases; the
   1,909 new signatures (all reproduced by rk, not only 1,625 by lk3). Each is now CHECKED-2. The short-root zeros outside box(0)
   remain COMPUTED-1, and so does the claim that the over root graph is not a stopper (not re-run).
4. The deleted `logs/fsig_*.txt` files (findings, section 8) are not needed: rk reproduces every class count of the affected cases,
   and its signature sets are in `verify/sigs_*.txt`.
5. Process: the referee's comparisons ran through `heavy.sh` (two wrappers, PIDs in `verify/pids.log`; both have finished). They used
   under 100 MB each. The binaries were built in a scratch directory and deleted by name.

## Files (verify/)

`rk.cpp` (solver), `cmp_rk.py`, `base_rk.py`, `p_check.py`, `agg_rk.py`, `cmp_rk.out`, `extra_rk.out` (run logs), `sigs_*.txt` and
`new_minus_base.txt` (signature sets, coded 0 = White wins, 1 = draw, 2 = Black wins, White to move then Black to move, contexts
in the kg order), `EDITS.md` (replacement set), `pids.log`.

Build and run: `c++ -O2 -std=c++17 -o rk verify/rk.cpp`; `rk cyl:10x6 all a2,c4,f2` (all roots) or `rk cyl:10x6 all a2,c4,f2 c3/a4`.
Environment flags: `RK_ALL` prints every root; `RK_NAMED`; `RK_SIGS`; `RK_BISIM`; `RK_PAIRS=<name>`.
