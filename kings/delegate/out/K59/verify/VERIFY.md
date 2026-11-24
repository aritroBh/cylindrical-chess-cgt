# K59 referee report

AI work (referee, one agent), no human re-derivation. I did not take part in K59. I wrote my own solver,
`verify/src/kref.cpp` (C++, about 400 lines), from LOOPY Definitions 1.1–1.3, 1.5 (P), 4.8, Lemma 4.15 and the brief's
rules, without reading the generators of pr56/pr57, vg/vgsum/vgsum59, ref3m, kp_p, p45a or r48; it shares no code
with anything in `kings/`. I read vgsum59.cpp and vgsum.cpp only for the diff review (part B), after kref was written
and its results were in. Paths are relative to `kings/delegate/out/K59/` unless they start with `kings/`.

## Verdict in short

| Claim | Verdict |
|---|---|
| 1. (B1) for T1–T4 of cyl:8×7 by vgsum59 and pr56 | CONFIRMED (from the logs and the code review; I did not run kref on T1–T4) |
| 2. F1–F5 on flat 8×7 are exact over groups and meet (B1) | CONFIRMED for all five by my own solver (Definition 4.8 clause by clause and (B1) under the sum's rule); move lists and values equal the investigator's |
| 2'. "five distinct groups" | CORRECTED in wording: five distinct placements, but F4 is F3 reflected left to right and moved one file, so four shapes up to reflection and translation |
| 3. §3d placements on flat 9×7 and 8×8; no cyl:8×7 group or translate exact on the flat boards | CONFIRMED from the logs (two programs each); reflections stated correctly; "three placements up to reflection" is right. Not re-run with kref |
| 4. Search of four file classes finds exactly these five | CONFIRMED as a log check: A and R counters equal in all four classes, hits as stated. Not re-run |
| Direct sums | CONFIRMED: kref gives 0 differences from over for F2 and F4 (63 games, 1,080 results each), and F2 beside K56's 600 random games (16,648 results, 0 differ) |
| "None of the five is tempo-exact" | CONFIRMED as a log reading (pr57 only, COMPUTED-1) |
| EDITS.md | applies (4 applied, 0 rejected) to the current LOOPY.md (after K60); replaced by `verify/EDITS.md` (6 edits, 0 rejected) |

So Corollary 4.17 (F1–F5) and the extension of Corollary 4.16 to T1–T4 are **PROVED, given CHECKED-2 computations**.
For F1–F5, Definition 4.8 and (B1) now each rest on three independently written programs (Definition 4.8: A = R
search, ref3m/kp_p, kref; (B1): vgsum59, pr57, kref).

## A. From-scratch check (kref)

Model: board flat or cylinder; kings and pawns; double step from the second rank, e.p. (right kept only when a pawn of
the side to move can take; this changes no value), no move into check; promotion is a terminal win for the promoter
and must itself be legal. P alone: checkmate loses, stalemate draws, infinite play draws. Sum: group ⊞ T for a finite
D-game T; a T move is not allowed in check and clears the e.p. right; a terminal of T or a promotion ends the play; a
side with no move loses. Values: graph of all states reachable from the seeds, least fixed point by repeated sweeps.
(B1) is group ⊞ −1 (`−1` = {∅ | 0}, Black's one token).

`kref check` tests Definition 4.8 in the over orientation as the note states it, clause by clause: K1/K2 geometry
for both z squares (no White attack on z, no Black attack on b0, king distance ≥ 2); (O1) at both Black-to-move roots
every non-shuttle move leads to a White win in P and the shuttle is legal; (O2) at both White-to-move roots some move
does not lose at once (a freeze = any move whose result is W or D, not only W), no freeze is a promotion; (O3) at each
q, Black to move with the right if any, Black has a move and every move loses at once; (O4) the same q with White to
move and no right is legal (Black not in check), White has a move and every move loses at once. Then (B1) for every
non-shuttle Black root move.

Sanity tests (logs/H10_check.out, logs/ZO_check.out, logs/ZO_star.out):
- H10 on cyl:10×6: exact, 0 failures; (B1) W at all 10 moves. Matches Corollary 4.16.
- Z_O on cyl:8×6: exact, 0 failures; (B1) fails at exactly one of 11 moves, 1…e5–e4 at the d4 root (L beside −1).
  Matches Corollary 4.16 and Corollary 4.19.
- Z_O beside \* (T = star): 1 of 24 results differs from over, the d4 root with Black to move (group L, over W),
  in Black's favour, as K47 found. So the sum code does detect a known difference.

Results on flat 8×7 (logs/F1_check.out … F5_check.out):

| Group | P graph nodes | Def. 4.8 | non-shuttle Black root moves | (B1) beside −1 | same move list as vgsum59 |
|---|---|---|---|---|---|
| F1 `Ka4 kc4/kc5 Pb2 Pe4 Pe5 pb6 pe6` | 1,520,123 | exact | 8 | all W | yes |
| F2 `Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6` | 883,243 | exact | 11 | all W | yes |
| F3 `Ke4 kc4/kc5 Pb2 Pb5 Pf5 pb6 pf6` | 1,275,940 | exact | 6 | all W | yes |
| F4 `Kc4 ke4/ke5 Pb5 Pf2 Pf5 pb6 pf6` | 1,276,714 | exact | 6 | all W | yes |
| F5 `Ka4 kc4/kc5 Pb2 Pe5 Pf4 pb6 pe6 pf5` | 5,397,871 | exact | 10 | all W | yes |

F2 in detail (my run against `logs/F2_def48_*.txt` and `logs/F2_vgsum.out`): Black-to-move roots: c4 root
c5 (shuttle), d3, d4, d5, …b5 (check), …b4; c5 root c4 (shuttle), d4, d5, c6, d6, …b5 (check), …b4; all non-shuttle
moves W in P and W beside −1. White-to-move roots: c4 root Ka3 L, b3 L, b4 W (freeze); c5 root Ka3 L, Kb3 L, b3 W
(freeze), b4 L. q after b2–b4 (Black to move): c3, d3, d4, d5, …b5, all W; with White to move: Ka3 L, b5 L. q after
b2–b3: Black's d4, d5, c6, d6, …b5, …b4 all W; White's Ka3 L, b4 L. Every move and every value equals ref3m's, kp_p's
and vgsum59's. After the double-step freeze b2–b4 no Black pawn can take e.p., so the right plays no role.
Disagreements: none.

## B. vgsum59 against vgsum

`src/vgsum.cpp` is byte-identical to `kings/delegate/out/K57/verify/src/vgsum.cpp`. The diff to `src/vgsum59.cpp` is
57 lines, all marked "K59 MEM": 64-bit to 32-bit offsets for forward, reverse and pass-reverse edge lists and the
token-game queue (with an abort if edges exceed 2^32 − 16; 2N < 2^32 holds for every run, the largest N being 16.6
million for T3); the forward edge list freed after the reverse lists are built (I checked that nothing reads `succ`
after that point: later code uses only `off` for move counts and the reverse lists); a `--reserve` capacity hint;
`--lowmem`, which stores no forward edges and regenerates each node's moves with the same `gen` in the same order
when building the reverse lists (the e.p. right is part of the node, so it is regenerated identically). No game logic
changed. Regression: I rebuilt vgsum59 and ran H10 with `--lowmem` and the K57 referee's six queries and 63 test games;
the output equals `kings/delegate/out/K57/verify/logs/h10.out` line for line except the "peak" lines
(logs/vg59_h10_lowmem.out; 0.86 GB). The investigator's own regressions (reg_h10, reg_h10_lowmem, reg_zoflat) also
diff to 0 lines against the K57 logs.

Independence: vgsum59's generator is the K56 referee's vg.cpp (written from SPEC.md); pr57 is K56's pr56 with an
explore mode. The two have different structure and code; both read the board kind themselves (`--board flat:WxH` or
`cyl:WxH`; each sets its own wrap flag). I found no shared code. So (B1) for T1–T4 and F1–F5 by vgsum59 and pr57 is
CHECKED-2 in the sense of the note, and for F1–F5 kref is a third program.

## C. Direct sums (kref, its own over_D ⊞ T solver)

Compared positions: the four roots (against ω, same side to move) and, for each freeze, q with Black to move and q
with White to move (against 0_D); every position t of T.
- F2 beside the 63 games of `in/T_h10.txt`: 1,080 results, 0 differ (logs/F2_sumT.out).
- F4 beside the same 63 games: 1,080 results, 0 differ (logs/F4_sumT.out).
- F2 beside K56's 600 random games `in/rnd_all.txt` (at most 5 nodes, 300 with terminals): 16,648 results, 0 differ
  (logs/F2_sumR.out; 23 minutes, 0.85 GB).
- Z_O beside {0, \*}: 1 of 24 differs, as expected (above).
(1,080 rather than the investigator's 1,215: vgsum59 also lists q with the unusable e.p. flag as a separate position.)
I also re-ran the investigator's comparison scripts on their logs: `cmp_sum.py` gives 1,215 results, 0 differ, for
each of F1–F5; `cmp56.py` gives 2,400 results, 0 differ, for each of F1–F5 and F1 on 9×7 and 8×8. Note that pr57's
2,400 are the four roots at T's start position only.

## D. Spot checks

- T1–T4 (logs/p1_T*.out): 11, 11, 13, 11 = 46 moves with a (B1) line, all W. pr56 logs are in
  `kings/delegate/out/K56/logs/` (B_T1/B_T2/B_T4/C_T3); I did not re-run the investigator's cmp_p1.py. Direct sums for
  T3 not run (memory), as stated.
- F1–F5 def48 logs: PASS by ref3m and by kp_p; the root and q move values are identical as sets (the move order
  differs between the two solvers). Counts of non-shuttle Black root moves 8, 11, 6, 6, 10 (F1–F5): confirmed by
  vgsum59 logs, pr57 logs ((N1) yes at each) and kref.
- search_table.txt against the xz logs: A (under and over) and R counters equal in all four classes; exact 1, 0, 3, 5;
  the over hits of A are F1 ({a,b,e}); F2, F3, F4 ({b,c,f}); all five ({b,e,f}); R's under hits are their colour
  mirrors. The four classes are the four reflection classes of the shapes {f, f+1, f+4} and {f, f+3, f+4} that fit
  on eight files.
- §3d: on 9 files, F3 moved two files = F4 reflected, F4 moved two files = F3 reflected, and F3 moved one file = F4
  moved one file reflected: three classes for the six placements. On 8×8, F3 moved one = F4 reflected and F4 moved one
  = F3 reflected. All stated correctly. (B1) logs for all 13 larger-board placements: every move W (vgsum59) and the
  pr57 runs report exact.
- Relations: on eight files, F4 reflected is `Kf4 kd4/kd5 Pc2 Pc5 Pg5 pc6 pg6` = F3 moved one file right. So F3 and
  F4 are one shape; on flat 8×7 they are different placements (pr57's tempo-failure counts differ, 8 and 4), and
  the search lists both because F3 lies in {b,c,f}/{b,e,f} and F3 moved one file lies in {c,d,g} ~ {b,e,f}. F1, F2, F5
  are not translates or reflections of each other or of F3; none is a translate of a cyl:8×7 group (those fail on
  the flat boards). "Five distinct groups" is right for placements; my edit says the five are four shapes.
- Tempo-exactness: pr57 reports "tempo-exact: NO" for all five and all larger-board placements (COMPUTED-1).

## E. Edits

The investigator's EDITS.md applies to the current LOOPY.md (after K60): 4 applied, 0 rejected. Problems: "not yet
refereed"; the move counts "8, 11, 6, 10 and 6" follow the listing order F1, F2, F3, F5, F4, which a reader will
easily mismatch; the larger-board sentence is vague ("some translates"); it does not mention that F4 is a reflected
translate of F3; the To-settle item asks for a referee check, now done; Lemma 4.13's "no known group" passage and
§8 item 2 are not updated. My `verify/EDITS.md` (6 edits, 0 rejected on the current file, table row still 5 fields)
fixes these: each group's count sits next to it, Corollary 4.17 sits at the end of Corollary 4.16's paragraph,
before Theorem 4.18, and is labelled PROVED given CHECKED-2 computations (Definition 4.8 and (B1) each by two or more
independently written programs). It keeps the claim at "has the results of over beside every finite D-game" and
says nothing about P contexts or chess.

## Not checked

- I did not run kref on T1–T4 (cyl:8×7); their (B1) rests on vgsum59 and pr56 (logs and code review only).
- I did not re-run any of the exhaustive searches (claim 4 is a log check) or the def48 runs for the 9×7/8×8
  placements and the 13 + 17 + 26 failing translates.
- kref direct sums only for F2 and F4 (and F2 beside the random games); F1, F3, F5 only through the investigator's
  logs.
- No hand proof of any computed fact; P contexts and chess not considered.

## Process

All kref and vgsum59 runs through `kings/delegate/heavy.sh` under `/usr/bin/time -l`; PIDs in `verify/pids.log`
(launcher PIDs; I stopped only my own batch script `runall.sh`, PID recorded, when I dropped two sum runs that would
have exceeded 2 GB: H10 and Z_O beside four-node games). Peak memory: 1.95 GB (Z_O beside \*), 1.93 GB (Z_O check),
1.87 GB (F5 check); everything else under 1.2 GB. Binaries were built in my scratch directory only and are not in the
repository. No git commands that change anything; nothing written outside `verify/` and my scratch directory.
