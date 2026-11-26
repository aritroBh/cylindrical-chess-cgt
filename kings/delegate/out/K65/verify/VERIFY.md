# K65 referee report (2026-11-25)

Referee of `kings/delegate/out/K65/` (findings.txt, EDITS.md, src/, logs/). Paths below are relative to
`kings/delegate/out/K65/verify/` unless they start with `kings/`. Labels: KNOWN (literature or tablebase), CHECKED-2 (two
separately written programs agree), COMPUTED-1 (one program). A computed fact is never called PROVED; a statement proved
from computed facts is "PROVED, given CHECKED-2 computations".

## Verdict

- **C125_09 = `Kc4 ke4/ke5 Pb5 Pf2 Pf6 pb6 pf7` (flat 8×8) has the results of ω beside every finite D-game although (B1)
  fails: CONFIRMED, PROVED given CHECKED-2 computations.** Definition 4.8 is confirmed by a third program (ax65, mine);
  (B1) fails exactly at …Ke5–d6 and …Ke5–e6 and holds at the other six bad moves (ax65 and pk_sum, with vgsum59 and pr57);
  White wins Aux at both failing moves (ax65 and pk_sum, two Büchi solvers on two separately written move generators, with
  aux60). Theorem 4.18 applies (checks, e.p., promotions read below).
- **It is not the only one.** All 38 groups are now classified, every (B1) value CHECKED-2: (B1) holds for 27 groups and
  fails for 11. Seven of the 11 (C125_09, C125_13, C125_22, C125_23, C145_16, C145_24, C145_25) have the results of ω
  without (B1) (Aux won at every failing move, CHECKED-2). Four fail (C) at exactly one bad move: C125_14, C125_16, C145_19
  with N\* = 2, and **C125_15 = `Kg5 ke5/ke6 Pb2 Pf2 Pf6 pc4 pf5 pf7` with N\* = 3 at …Ke5–e4 (CHECKED-2): the first real
  exact group with a ladder length of 3**, which answers the question left OPEN after Corollary 4.23.
- **Census: CONFIRMED, now CHECKED-2 in both classes.** r48 on {b,e,f} (my run, 5.01 h, 1.04 GB) gives p45a's six
  counters exactly and the same 25 groups. The recount from the hit lists confirms 23 + 25 hits,
  38 distinct, 10 in both classes, 26 up to reflection and file translation, and four 2 + 2 groups in three shapes.
- **Chess (tablebase, KNOWN)**: 19 groups (not 18) have at most seven men. Five of them are exact over groups in chess:
  C125_05, C125_08, C125_10, C145_07, C145_09. The other 14 (F1–F4 by K63's referee, 10 by me) are not.
- The investigator's memory-rule breach (eight runs above 3 GB) is its own report; none of my runs came near the limit
  (largest: r48, about 1.0 GB; my own solvers at most 0.2 GB).

## Claims

| # | Claim (investigator) | Verdict | Method | Label |
|---|---|---|---|---|
| A1 | C125_09 is an exact over group (roots e4/e5, freezes f2–f4 at e4, f2–f3 at e5, q's as listed) | CONFIRMED | ax65 (mine, own generator) clause by clause; also ref3m, `kp_p` (investigator) | CHECKED-2 (3 programs) |
| A2 | (B1) fails exactly at …Ke5–d6, …Ke5–e6; holds at the other 6 | CONFIRMED | ax65, pk_sum beside −1; vgsum59, pr57 (investigator) | CHECKED-2 |
| A3 | White wins Aux at both failing moves | CONFIRMED (was COMPUTED-1) | ax65 (Büchi, νY.μX per block), pk_sum -aux (Büchi on K63's pk generator), aux60 | CHECKED-2 |
| A4 | x_m ⊞ u_0 and both roots (Black to move) are White wins beside T_0 … T_6 | CONFIRMED | ax65 and pk_sum (T_6); ax65's ladder layers are constant from T_4 on and equal the Aux layer bit for bit | CHECKED-2 |
| A5 | Hence the results of ω without (B1), "first real group known" | CONFIRMED, CORRECTED in scope: one of seven such groups in the same census (A1–A4 hold for all seven, see table 2) | Theorem 4.18 (b), (c) | PROVED given CHECKED-2 computations |
| A6 | Theorem 4.18 applies | CONFIRMED | No king in check at any root or q (ax65 tests it); K1, K2 hold (kings two apart, no attacked z square); the e.p. right after f2–f4 is empty (no Black pawn on e4 or g4), and in chess a right only adds moves (remark (2)); no promotion is within one move of a root or q, and both Aux solvers treat a promotion as the end of the play | reading |
| B1 | {b,c,f}: 23 exact, p45a = r48 on every counter and hit | CONFIRMED (hit lists) | own recount `src/recount.py` from the raw outputs | CHECKED-2 |
| B2 | {b,e,f}: 25 exact (p45a only) | CONFIRMED: r48 gives (3,718,505,519; 1,217,644,122; 820,498,702; 397,118,871; 362,051,648; 25), p45a's six counters, and the same 25 groups | r48 (my run), `src/recount.py` | CHECKED-2 |
| B3 | 38 distinct, 10 in both classes, 26 up to reflection and file translation | CONFIRMED | `src/recount.py` | KNOWN arithmetic on the hit lists |
| B4 | Smallest: four 2 + 2 groups in three shapes (findings §0) vs three named (EDITS.md) | SETTLED: four groups, three shapes; the EDITS.md sentence named only three groups (it left out `Ke5 kg4/kg5 Pb3 Pf2 pb4 pf5`, the reflected translate of `Kc5 ka4/ka5 Pb2 Pf3 pb5 pf4`) | `src/recount.py` | — |
| B5 | Group list (roots, shuttle, freezes, q's) | CONFIRMED for all 38, not only five: same freezes and q's, all exact | ax65 on every group, `src/cmp_freezes.py` | CHECKED-2 |
| B6 | The 38 listed in findings §3 are the hit sets | CONFIRMED | `src/recount.py` | — |
| C1 | C125_14: (B1) fails at …Kd5–d4 (vgsum59 only) | CONFIRMED | ax65, pk_sum (and vgsum59) | CHECKED-2 |
| C2 | C125_14: (C), N\* not decided | DECIDED: Aux lost at …Kd5–d4 (won at the other 7); x_m ⊞ u_0 wins beside T_0, T_1, lost (L) beside T_2: N\* = 2; root d5 (Black to move) lost beside T_2 | ax65, pk_sum | CHECKED-2 |
| C3 | (B1) not checked for 16 groups, COMPUTED-1 for C145_20 | DONE: all 17 checked; 7 + C145_20 satisfy (B1) at every bad move, 9 fail (table 2) | ax65 (2 bits a state per layer, no stored edges; ≤ 0.11 GB), pk_sum (≤ 0.2 GB) | CHECKED-2 |
| C4 | "No group with N\* ≥ 3 was found" | REFUTED: C125_15 has N\* = 3 at …Ke5–e4 (wins beside T_0, T_1, T_2; draw beside T_3; Aux lost); root e5, Black to move: W beside T_2, D beside T_3 | ax65 (T_0…T_6, stable from T_5, equal to Aux), pk_sum (T_0…T_3 at x_m and both roots; Aux) | CHECKED-2 |
| C5 | — | Aux at every failing move of the 11 (B1)-failing groups: lost at exactly C125_14 …Kd5–d4, C125_15 …Ke5–e4, C125_16 …f5–f4 (g4 root), C145_19 …b5–b4 (a4 root); won everywhere else; N\* = 2, 3, 2, 2 | ax65, pk_sum, move by move (`src/cmp_aux.sh`, 0 disagreements) | CHECKED-2 |
| D1 | (brief) 18 of the 38 groups have at most seven men | CORRECTED: 19 (4 with six men, 15 with seven) | count | — |
| D2 | Is any of them an exact over group in chess? | YES: C125_05, C125_08, C125_10, C145_07, C145_09 (table 3) | Syzygy via `realchess/probe.py`, 120 requests, `src/tb65.py`; move lists equal `realchess.movegen`'s | KNOWN |
| E1 | q notation "b f3" etc. | Harmless: in every listed q the e.p. right is empty (no Black pawn beside the double-stepped pawn); my programs drop such rights | — | — |
| E2 | Memory rule | The investigator broke it (its own section 4); my runs: largest r48 ≈ 1.0 GB, all others ≤ 0.2 GB; no watchdog kill | `/usr/bin/time -l`, `src/wd.sh` (0.1 s polls on the solver's own PID, kill at 2.0 GB) | — |

## A. C125_09 in detail

Programs (both mine; neither shares code with aux60, vgsum59, pr57, ref3m, `kp_p`, p45a, r48):
- `src/ax65.cpp`: my own move generator (flat or cylinder) and solver. Pawn configurations change only irreversibly, and so
  does the T-state except for White's pass in under; blocks (configuration, T-state) are solved in an order in which every
  move leaving a block goes to a solved one, inside a block by the Büchi fixpoint νY.μX (plain attractor when there is no
  pass). One bit per (configuration, side, king squares) per T-state; array sizes are computed and checked against 2 GB
  before allocation. It does Definition 4.8 (P solved for each side), (B1) (T = −1), Aux (T = under) and the ladders T_N.
- `src/pk_sum.cpp`: the K63 referee's P solver `pk.cpp` (flat 8×8), extended by me to sums under the sum's rule (T given
  as a small game, `-ladder N`, and `-aux` with the Büchi iteration per configuration). Its generator and retrograde loop
  are pk's; the changes are marked "K65".

Validation of ax65 before use: Z_O on cyl:8×6: exact; (B1) fails only at …e5–e4 (d4 root); Aux lost there and won at the
other ten; x_m ⊞ u_0 won beside T_0, T_1, lost from T_2 (N\* = 2), root d4 lost from T_2: all as in Corollaries 4.19 and
4.23 (`logs/val_logs.tar.xz`: v_ZO). H10 on cyl:10×6: exact, (B1) at all ten, Aux won at all ten. F2 on flat 8×8: exact,
(B1) at all nine. Validation of pk_sum: (B1) of C125_09 (= vgsum59, pr57, ax65); Aux of C125_09 (= aux60). On all 18 groups it was run
on it then agreed with ax65 at every bad move, for (B1) and for Aux.

Results (ax65 `logs/A_C125_09.out`; pk_sum `logs/groups_logs.tar.xz`, folder pk/):

| bad move | (B1) beside −1 | beside 0 | Aux | T_0 … T_6 |
|---|---|---|---|---|
| …Ke4–f3, …Ke4–f4, …Ke4–f5 (e4 root) | W | W | W | W |
| …Ke5–f4, …Ke5–f5, …Ke5×f6 (e5 root) | W | W | W | W |
| …Ke5–d6 | not W (D) | W | W | W |
| …Ke5–e6 | not W (D) | W | W | W |

Both roots, Black to move, are White wins beside u_0 of T_0 … T_6 (both programs).

How White wins Aux. After …Ke5–d6 (x_m = `Kc4 kd6 Pb5 Pf2 Pf6 pb6 pf7`, White to move) the board with Black to move is a
zugzwang: every Black move loses (beside 0). With White to move only Kc4–d4 wins on the bare board, and beside −1 it fails:
after 1.Kd4 Black does not spend its token but plays 1…Ke6 (or …Kc7, …Kd7), and every other White first move fails too.
In Aux White passes instead and hands Black the move. Black's options are then: spend its one freeze (then 2.Kd4 wins on
the board), or move its king (…Ke5, …Ke6, …Kc7, …Kd7), after which White passes again or wins on the board. One line:
1.pass Kd6–e5 2.pass Ke5–e4 3.pass Ke4–e5 4.pass … — Black's king shuttles and White passes for ever, which Aux scores as a
White win; this is exactly what over's own shuttle is matched by in the D-sum. After …Ke5–e6 the picture is the same
(Kc4–d4 and f2–f4 win on the bare board; after 1.pass Ke6×f6 White wins by 2.Kd5).

## B. Census

r48 on {b,e,f} (flat 8×8, ranks 2–7, ≤ 3 + 3; `logs/R88_f1_4_5.out`): placements 3,718,505,519, (O1) 1,217,644,122,
promotion freeze 820,498,702, (O1)+(O2) 397,118,871, loose 362,051,648, exact 25: every counter equal to p45a's, and the
hit set, mirrored into the over frame, equal to p45a's. 18,038 s wall, peak RSS 1.04 GB, no watchdog action.
So "{b,e,f} has no other exact over group" is now CHECKED-2, like {b,c,f}.

Recount (`src/recount.py`, from `../logs/search/A88_f1_2_5.out.xz`, `A88_f1_4_5.out.xz`, `R88_f1_2_5.out`): p45a {b,c,f}
23, p45a {b,e,f} 25, r48 {b,c,f} 23 and equal to p45a's set after the colour mirror; 38 distinct; 10 in both classes; 26
up to reflection and file translation; by men: six 4 groups (3 shapes), seven 15 (10), eight 19 (13). The four smallest:
`Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6` (F2), `Ka5 kc5/kc6 Pb2 Pf6 pb7 pf7`, `Kc5 ka4/ka5 Pb2 Pf3 pb5 pf4` and
`Ke5 kg4/kg5 Pb3 Pf2 pb4 pf5` (the last two one shape). The list of 38 in findings §3 equals the union of the hit sets.
The near-miss sub-counters of findings §0 (check, half exact, promotion-only) were not checked; r48 does not print them.

## C. Classification of the 38 groups

Every (B1) value below is CHECKED-2 (ax65 and pk_sum for the 18 groups that were open or COMPUTED-1; ax65 with vgsum59 and
pr57 for the other 20). Every Aux value at a failing move is CHECKED-2 (ax65, pk_sum). Definition 4.8: all 38 exact by ax65
(and by ref3m, `kp_p`).

Table 1. Summary.

| class | groups |
|---|---|
| (B1) at every bad move (results of ω by Lemma 4.15): 27 | C125_01–08, 10, 11, 12, 17, 18, 19, 20, 21; C145_07, 09, 12, 13, 15, 17, 18, 20, 21, 22, 23 |
| (B1) fails, Aux won at every failing move (results of ω by Theorem 4.18): 7 | C125_09, C125_13, C125_22, C125_23, C145_16, C145_24, C145_25 |
| Aux lost at one bad move (no results of ω): 4 | C125_14 (N\* = 2), C125_15 (N\* = 3), C125_16 (N\* = 2), C145_19 (N\* = 2) |

Table 2. Groups with a (B1) failure.

| group | bad moves | (B1) fails at | Aux lost at | N\* | men |
|---|---|---|---|---|---|
| C125_09 `Kc4 ke4/ke5 Pb5 Pf2 Pf6 pb6 pf7` | 8 | …Ke5–d6, …Ke5–e6 | — | ∞ | 7 |
| C125_13 `Kf6 ke8/kf8 Pc5 Pf2 pb7 pc6 pf7` | 7 | …Kf8–g8 | — | ∞ | 7 |
| C125_14 `Kb5 kd5/kd6 Pb6 Pc2 Pf5 pb7 pc5 pf6` | 8 | …Kd5–d4 | …Kd5–d4 | 2 | 8 |
| C125_15 `Kg5 ke5/ke6 Pb2 Pf2 Pf6 pc4 pf5 pf7` | 11 | …Ke5–d4, …Ke5–e4, …Ke5–d6, …f5–f4 (e5), …Ke6–d6 | …Ke5–e4 | **3** | 8 |
| C125_16 `Ke5 kg4/kg5 Pb2 Pc3 Pf2 pb5 pc4 pf5` | 12 | …f5–f4 (g4) | …f5–f4 (g4) | 2 | 8 |
| C125_22 `Ka4 kc4/kc5 Pb2 Pc3 Pf6 pb6 pb7 pf7` | 7 | …b6–b5 (c4), …Kc5–c6, …b6–b5 (c5) | — | ∞ | 8 |
| C125_23 `Ke5 kg5/kg6 Pc3 Pf2 Pf6 pb7 pc6 pf7` | 13 | …c6–c5 (both roots) | — | ∞ | 8 |
| C145_16 `Kb6 kb8/kc8 Pb2 Pe5 pb7 pe6 pf7` | 7 | …Kb8–a8 | — | ∞ | 7 |
| C145_19 `Kc5 ka4/ka5 Pb2 Pe3 Pf2 pb5 pe4 pf5` | 6 | …b5–b4 (a4) | …b5–b4 (a4) | 2 | 8 |
| C145_24 `Kc5 ka5/ka6 Pb2 Pb6 Pe3 pb7 pe6 pf7` | 7 | …e6–e5 (both roots) | — | ∞ | 8 |
| C145_25 `Ka4 kc4/kc5 Pb2 Pe4 Pf2 pb6 pe5 pe7` | 9 | …b6–b5, …e7–e6 (c5) | — | ∞ | 8 |

Ladders at the four Aux losses (x_m ⊞ u_0, White to move; both programs): C125_14, C125_16, C145_19: W beside T_0, T_1,
L beside T_2 (pk_sum: loss; ax65: not a White win from T_2 to the stable layer). C125_15 …Ke5–e4: W beside T_0, T_1, T_2,
**D** beside T_3 (both programs), not a White win from T_3 to T_6 (ax65; its layers are stable from T_5 and equal the Aux
layer). In each case the root of the failing move, Black to move, stops being a White win at the same N (C125_15: root e5
W beside T_2, D beside T_3), so C125_15 has the results of ω beside T_0, T_1, T_2 and not beside T_3.

C125_15 after …Ke5–e4 (x_m = `Kg5 ke4 Pb2 Pf2 Pf6 pc4 pf5 pf7`): no White board move and no pass wins Aux; after a pass,
Black has three replies that keep Aux from White (…Kd3, …Ke5, …f5–f4). Beside T_2, where White needs three moves in T
to reach the terminal win, White wins; beside T_3 (four moves) Black's counter lasts long enough and the result is a draw.

Memory: ax65 on the largest group (C145_25, 7,326 configurations) 18 MB; pk_sum at most 0.2 GB (C125_16, T_2). None of the
17 needed more than 0.2 GB, so no group was left out for memory.

## D. Chess (Syzygy tablebase via the Lichess API, queried 2026-11-25; KNOWN)

Reading of Definition 4.8 with chess values (as K63's referee did for F1–F4): at both roots every non-shuttle Black move
loses (no Black move but the shuttle avoids loss; in P the shuttle loses too, so it is not required to hold); the freeze is
White's only non-losing move; both q's lose for the side to move, either side. (Where a group fails only because White has
further non-losing king moves — C125_01, C125_02 — those moves are king freezes whose q, White to move, is won for White by
moving the king back to the root, where Black to move loses; so the verdict is the same under the letter of Definition 4.8.)
120 requests (15 groups × 8 positions), ledger `tb_ledger.jsonl`, cache `logs/tbcache.tar.xz`, full output `logs/tb/`.
No cursed or blessed results and no "maybe" categories anywhere, so the 50-move rule changes nothing.

Table 3.

| group | men | exact in chess? | where it fails |
|---|---|---|---|
| C125_01 `Ke5 kg4/kg5 Pb3 Pf2 pb4 pf5` | 6 | no | roots, White to move: king moves also do not lose (Ke6, Kf6 at g4; Kd4, Kd5, Kd6, Ke6 at g5) |
| C125_02 `Kc5 ka4/ka5 Pb2 Pf3 pb5 pf4` | 6 | no | roots, White to move: king moves also do not lose |
| C125_03 = F2 | 6 | no | K63 referee (KNOWN) |
| C125_04 `Ka5 kc5/kc6 Pb2 Pf6 pb7 pf7` | 6 | no | roots drawn; q at c5, Black to move, draw |
| **C125_05 `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6`** | 7 | **YES** | — |
| C125_06 = F3 | 7 | no | K63 referee |
| C125_07 = F4 | 7 | no | K63 referee |
| **C125_08 `Ke5 kc5/kc6 Pb2 Pb6 Pf6 pb7 pf7`** | 7 | **YES** | — |
| C125_09 `Kc4 ke4/ke5 Pb5 Pf2 Pf6 pb6 pf7` | 7 | no | both q's, White to move, draw; at the roots Kc3 (and Kd3 at e5) and the other pawn step also do not lose |
| **C125_10 `Kc5 ke5/ke6 Pb6 Pf2 Pf6 pb7 pf7`** | 7 | **YES** | — |
| C125_11 `Kg5 ke5/ke6 Pc5 Pf2 Pf6 pb7 pf7` | 7 | no | q's White to move draw; king moves and the other pawn step also do not lose at the roots |
| C125_12 `Ka4 kc4/kc5 Pb2 Pf3 Pf4 pb6 pf5` | 7 | no | roots drawn, q's Black to move draw |
| C125_13 `Kf6 ke8/kf8 Pc5 Pf2 pb7 pc6 pf7` | 7 | no | everything drawn |
| **C145_07 `Kg4 ke4/ke5 Pe6 Pf2 Pf5 pe7 pf6`** | 7 | **YES** | — |
| **C145_09 `Kd4 kf4/kf5 Pe2 Pe5 Pf6 pe6 pf7`** | 7 | **YES** | — |
| C145_12 = F1 | 7 | no | K63 referee |
| C145_13 `Ka5 kc5/kc6 Pb2 Pe5 Pe6 pb7 pe7` | 7 | no | roots drawn, q at c5 Black to move draw |
| C145_15 `Ka4 kc4/kc5 Pb2 Pf3 Pf4 pb6 pe6` | 7 | no | root c5 and q at c5 drawn; at c4 other White moves do not lose and some Black king moves draw |
| C145_16 `Kb6 kb8/kc8 Pb2 Pe5 pb7 pe6 pf7` | 7 | no | root c8: White to move loses, Black to move wins; q's not zugzwangs |

In the five YES groups, at each root White to move wins (only by the freeze) and Black to move loses (every move, the
shuttle included), and the four q positions are lost for the side to move, as in P.

## What was not checked

- The near-miss sub-counters of findings §0 (other than the counters r48 prints).
- The classes {a,b,e}, {a,d,e}, the eleven two-file classes outside {b,c,f} and {b,e,f}, part c of the brief: not
  searched by anyone.
- Aux "won" at the 7 + 4 groups rests on two Büchi solvers of mine (ax65 and pk_sum), which share no code but were
  written by the same referee; for C125_09 aux60 is a third, independent one.
- Chess: groups with eight men (no tablebase); only Definition 4.8 in chess was asked, not the D-sum behaviour in chess.
- No hand proofs of the computed facts.

## Files

`src/ax65.cpp`, `src/pk_sum.cpp` (solvers), `src/run.sh` + `src/wd.sh` (every run through `kings/delegate/heavy.sh` under
`/usr/bin/time -l`, watchdog on the solver's own PID, 0.1 s polls, kill at 2.0 GB; never fired), chain scripts,
`src/recount.py`, `src/cmp_freezes.py`, `src/cmp_aux.sh`, `src/tb65.py`; `in/` (query positions written from ax65's logs);
`logs/groups_logs.tar.xz` (ax65 on all 38 groups `g/`, ladders `lad/`, pk_sum runs `pk/`, watchdog and chain logs),
`logs/val_logs.tar.xz` (ax65 on Z_O, H10, F2), `logs/A_C125_09*.out` (C125_09 with ladders, and with the explanations),
`logs/R88_f1_4_5.*` (r48 on {b,e,f}), `logs/tb/` and `logs/tbcache.tar.xz` (tablebase; `tb65_first_criterion.out` is the
same data under a first, too strict reading that also required the shuttle not to lose), `tb_ledger.jsonl` (120 requests),
`pids.log`. Binaries deleted.

Process notes: one watchdog for the tablebase script was started with a wrong command name and never attached; a second
one was attached by hand (pids.log). A first pk_sum build crashed at once (a variable shadowed the T-state index; caught
by the address sanitizer, fixed before any result was used). No run was killed; nothing passed 1.1 GB.
