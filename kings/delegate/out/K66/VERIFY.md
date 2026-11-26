# K66: independent check of the K65 referee's findings (2026-11-25)

Checker of `kings/delegate/out/K65/verify/VERIFY.md` and `EDITS.md`. Paths are relative to `kings/delegate/out/K66/`
unless they start with `kings/`; every `logs/<name>.out` cited below except `logs/chess66.out` is inside `logs/runs.tar.xz`. Labels: KNOWN (tablebase), CHECKED-2 (two separately written programs agree),
COMPUTED-1 (one program). Before my numbers existed I read only LOOPY.md (Definition 4.8 to the remark after Corollary
4.23), the K65 referee's VERIFY.md and EDITS.md, and K61 brief §1; I did not open `ax65.cpp`, `pk_sum.cpp`, `tb65.py` or
any K65 result log, then or later.

## Verdict

- **N\* = 3 for C125_15 = `Kg5 ke5/ke6 Pb2 Pf2 Pf6 pc4 pf5 pf7`: CONFIRMED, every value.** Exact (every clause of
  Definition 4.8); eleven bad Black root moves; (B1) fails exactly at …Ke5–e4, …Ke5–d4, …Ke5–d6, …f5–f4 (e5 root),
  …Ke6–d6; Aux lost only at …Ke5–e4; there x_m ⊞ u_0 (White to move) is W beside T_0, T_1, T_2 and D beside T_3, T_4,
  T_5, T_6; the e5 root (Black to move) is W beside u_0 of T_0–T_2 and D beside T_3–T_6. With ax65 and pk_sum this is
  now three programs by two authors: CHECKED-2 in the strict sense. Proposition 4.24 as written in the referee's EDITS.md
  is supported.
- **Seven groups with the results of ω without (B1): CONFIRMED** (C125_09, C125_13, C125_22, C125_23, C145_16, C145_24,
  C145_25): each exact, the same bad-move counts, (B1) fails at exactly the listed moves, Aux won at every bad move.
- **C125_14, C125_16, C145_19 (N\* = 2): CONFIRMED**: one failing move each, Aux lost there, W beside T_0, T_1 and L
  (Black win) beside T_2 to T_4.
- **Chess, five exact over groups (C125_05, C125_08, C125_10, C145_07, C145_09): CONFIRMED (KNOWN)**, and the "no"
  verdict for the other ten probed groups is confirmed. The referee's reading is fair to Definition 4.8 (see section 4).
- **EDITS.md**: no factual error found; one citation should change (section 6, `EDITS.md`).

## Program

`src/k66.cpp` (mine, written from the note's definitions; no code shared with ax65, pk_sum, pk, vgsum59, pr57, aux60,
ref3m, `kp_p`). Flat 8×8, kings and pawns, P (a promotion ends the play as a win for the promoter), double steps, e.p.,
no move into check; P alone: mate loses, stalemate draws. As a D-sum component: a side in check may not move elsewhere, a
move elsewhere clears the mover's right, no move anywhere loses, infinite play draws. Aux = G ⊞ under_D with the Büchi
rule (White wins an infinite play iff it passed infinitely often), solved per block by νY.μX. Pawn configurations
(white pawns, black pawns, e.p. target) are closed under an over-approximation of pawn moves and king captures and solved
in an order in which every pawn move, capture or loss of a right goes to an earlier one; inside a block only king moves
(and White's pass in Aux) remain, solved by retrograde analysis. One byte of value and two of rank per state, sizes
checked against 1.6 GB before allocation. T_N, −1, 0 and under_D are given as small D-games. Modes: the group report
(Definition 4.8 clause by clause, then every bad move beside 0, −1, Aux, T_0…T_N, and both roots beside T_N), `pv`
(a line of play beside T_N) and `explain` (White's moves at x_m in P, 0, −1, Aux; Black's replies after a pass).
`src/chess66.py` (mine): Definition 4.8 with tablebase values, from the cached Lichess answers.

Internal check: at every one of the 92 bad moves of the 11 groups, Aux lost ⇔ some T_N (N ≤ 4 or 6) is not a White win,
as Theorem 4.18(c) says; the Büchi solver and the ladder solver are separate code paths.

## 1. Validation

| position | claim | mine | verdict |
|---|---|---|---|
| F2 `Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6` | exact; (B1) at all nine bad moves | exact (freezes b2–b4 at c4, b2–b3 at c5); 9 bad moves, all W beside −1, Aux W, W beside T_0–T_2 | confirmed |
| C125_14 `Kb5 kd5/kd6 Pb6 Pc2 Pf5 pb7 pc5 pf6` | (B1) fails only at …Kd5–d4; Aux lost there; W beside T_0, T_1, lost beside T_2 | 8 bad moves; −1: L at …Kd5–d4, W elsewhere; Aux lost only there; T_0..T_3: W W L L; root d5 (Black to move) W W L L | confirmed |

## 2. C125_15 (`logs/C125_15.out`, T up to 6)

| claim | mine | verdict |
|---|---|---|
| exact; freezes f2–f3 at e5, f2–f4 at e6 | exact, those freezes only; (O0)–(O4) hold; q's: White to move L, Black to move W | confirmed |
| eleven bad Black root moves | 6 at e5 (…Ke4, …Kd5, …Kd6, …Kd4, …c3, …f4), 5 at e6 (…Kd6, …Kd7, …Kd5, …c3, …f4) | confirmed |
| (B1) fails at …Ke5–d4, …Ke5–e4, …Ke5–d6, …f5–f4 (e5), …Ke6–d6 | beside −1: …Ke5–e4 L; …Kd4, …Kd6, …f4 (e5), …Ke6–d6 D; the other six W | confirmed |
| Aux lost only at …Ke5–e4 | yes; won at the other ten | confirmed |
| at …Ke5–e4, x_m ⊞ u_0: W beside T_0, T_1, T_2, D beside T_3, not W for T_4–T_6 | W W W D D D D | confirmed |
| e5 root, Black to move: W beside u_0 of T_2, D beside T_3 | W W W D D D D (T_0…T_6) | confirmed |
| (not claimed) e6 root, Black to move | W W W W D D D | — |
| (referee's VERIFY, not EDITS) after a White pass at …Ke5–e4 Black keeps Aux with …Kd3, …Ke5, …f5–f4 | exactly these three (`logs/ex15_e4.out`) | confirmed |

**How White wins beside T_2** (`logs/pv15_T2.out`; from x_m = `Kg5 ke4 Pb2 Pf2 Pf6 pc4 pf5 pf7`, White to move, T at
u_0; "T" is White's move u_i → u_{i+1}, the last one u_2 → ⊕). 1.Kh6 (the only move that does not lose; the T move
loses at once) Ke5 2.Kg7 Ke6 3.T Ke5 4.K×f7 Ke4 5.f3+ Ke5 6.f4+ Ke4 7.T Ke3 8.T (⊕). Black's alternatives are lost at
every ply, his move to z included. *Why:* White's king needs two moves (Kh6, Kg7) to reach the f7 pawn while Black's
king can only shuttle on e4–e6; at ply 4 (Kg7 against …Ke6) every White board move loses and White spends a T move as a
tempo, after which every Black move loses; once f7 falls the checks f3+, f4+ drive the king, and White's last two T moves
run out the ladder while Black's one move elsewhere loses at once. Beside T_2 White needs three T moves in all, and the
line supplies exactly three moments where one is safe.

**How Black holds beside T_3** (`logs/pv15_T3.out`). 1.Kh6 Ke5! (every other Black move loses) 2.Kg5 (forced: beside
T_3, 2.Kg7, which won beside T_2, now loses, as do the T move and the freezes) Ke4 3.Kh6 Ke5 4.Kg5 …, a repetition and so a
draw. *Why:* with one more step on the ladder White needs a fourth safe tempo moment; computed, beside T_3 the walk
2.Kg7 is a Black win, as are the T move and both freezes at every ply of the line, so White's only safe course is to
shuttle g5–h6 against Black's e4–e5: the king-walk counter of the remark after Corollary 4.23. I did not extract Black's
winning line after 2.Kg7. (The "why" sentences are my reading of the computed move values printed in the logs; only the values are
computed facts, COMPUTED-1 by my program, CHECKED-2 with the referee's.)

## 3. The seven groups without (B1), and 4. the other two N\* = 2 groups (T up to 4)

| group | exact | bad moves | (B1) fails at (value beside −1) | Aux | ladders at failing moves | verdict |
|---|---|---|---|---|---|---|
| C125_09 `Kc4 ke4/ke5 Pb5 Pf2 Pf6 pb6 pf7` | yes | 8 | …Ke5–e6 (D), …Ke5–d6 (D) | W at all 8 | W T_0–T_4 | confirmed |
| C125_13 `Kf6 ke8/kf8 Pc5 Pf2 pb7 pc6 pf7` | yes | 7 | …Kf8–g8 (L) | W at all 7 | W | confirmed |
| C125_22 `Ka4 kc4/kc5 Pb2 Pc3 Pf6 pb6 pb7 pf7` | yes | 7 | …b6–b5 at c4 (L), …Kc5–c6 (L), …b6–b5 at c5 (L) | W at all 7 | W | confirmed |
| C125_23 `Ke5 kg5/kg6 Pc3 Pf2 Pf6 pb7 pc6 pf7` | yes | 13 | …c6–c5 at g5 (D), at g6 (D) | W at all 13 | W | confirmed |
| C145_16 `Kb6 kb8/kc8 Pb2 Pe5 pb7 pe6 pf7` | yes | 7 | …Kb8–a8 (L) | W at all 7 | W | confirmed |
| C145_24 `Kc5 ka5/ka6 Pb2 Pb6 Pe3 pb7 pe6 pf7` | yes | 7 | …e6–e5 at a5 (D), at a6 (D) | W at all 7 | W | confirmed |
| C145_25 `Ka4 kc4/kc5 Pb2 Pe4 Pf2 pb6 pe5 pe7` | yes | 9 | …b6–b5 at c5 (D), …e7–e6 at c5 (L) | W at all 9 | W | confirmed |
| C125_16 `Ke5 kg4/kg5 Pb2 Pc3 Pf2 pb5 pc4 pf5` | yes | 12 | …f5–f4 at g4 (L) | lost there only | W W L L L | confirmed, N\* = 2 |
| C145_19 `Kc5 ka4/ka5 Pb2 Pe3 Pf2 pb5 pe4 pf5` | yes | 6 | …b5–b4 at a4 (L) | lost there only | W W L L L | confirmed, N\* = 2 |

Roots, Black to move, beside u_0 of T_N: W for every N ≤ 4 in the seven; C125_16 g4 root and C145_19 a4 root W W L L L.
The EDITS.md account of C125_09 (zugzwang with Black to move; with White to move only Kc4–d4 wins, after …Ke6 also f2–f4;
beside −1 every White move fails; in Aux the pass wins, Black's freeze is met by Kc4–d4, every Black king move by a
further pass or a board win) agrees move by move with `logs/ex09_d6.out`, `logs/ex09_e6.out`.

## 5. Chess (`src/chess66.py`, `logs/chess66.out`)

**What "exact in chess" means here.** Definition 4.8 with chess (Syzygy) values in place of P values, "a move loses at
once" read as "the position after it is lost, by the tablebase, for the side that made it": (O0) no king in check at the
roots and q's; (O1) at both roots, Black to move, the shuttle is legal and every other Black move loses; (O2) at both
roots, White to move, some White move does not lose (a freeze); (O3) for every freeze, q with Black to move (right if a
double step) has a move and every Black move loses; (O4) the same q, White to move, has a move and every White move loses.
Every non-losing White move is a freeze and must pass (O3), (O4). It says nothing about D-sums or P contexts in chess.

**Is the referee's reading fair?** Its words "the freeze is White's only non-losing move" are stronger than (O2)–(O4),
which allow several freezes. The difference never decides a verdict: in the five YES groups each root has exactly one
non-losing White move, so both readings agree; in C125_01 and C125_02 (and in several other "no" groups) the extra
non-losing moves are White king steps, and the q after such a step fails (O4) under the letter: White steps back to the
root square (legal, it was legal there), reaching the root with Black to move, which the tablebase gives as lost for
Black (draw in C125_04, C125_12, C125_13, C145_13, C145_15), so that move does not lose. This is the referee's remark,
confirmed; I deduced it from the cached root values and did not probe those q's. No cursed or blessed results (only
win/draw/loss in all 119 records used), so the 50-move rule changes nothing.

| group | men | mine | where it fails (first reasons) |
|---|---|---|---|
| C125_01 `Ke5 kg4/kg5 Pb3 Pf2 pb4 pf5` | 6 | no | six king freezes fail (O4) |
| C125_02 `Kc5 ka4/ka5 Pb2 Pf3 pb5 pf4` | 6 | no | six king freezes fail (O4) |
| C125_04 `Ka5 kc5/kc6 Pb2 Pf6 pb7 pf7` | 6 | no | (O1) king moves draw at both roots; (O3) q after b2–b3 draws |
| C125_05 `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6` | 7 | **YES** | — |
| C125_08 `Ke5 kc5/kc6 Pb2 Pb6 Pf6 pb7 pf7` | 7 | **YES** | — |
| C125_09 `Kc4 ke4/ke5 Pb5 Pf2 Pf6 pb6 pf7` | 7 | no | (O4) both q's draw; f2–f3 at e4 and f2–f4 at e5 do not lose and give check; Kc3, Kd3 do not lose |
| C125_10 `Kc5 ke5/ke6 Pb6 Pf2 Pf6 pb7 pf7` | 7 | **YES** | — |
| C125_11 `Kg5 ke5/ke6 Pc5 Pf2 Pf6 pb7 pf7` | 7 | no | (O4) both q's draw; king moves and the other pawn step do not lose |
| C125_12 `Ka4 kc4/kc5 Pb2 Pf3 Pf4 pb6 pf5` | 7 | no | (O1) draws at both roots; (O3) both q's draw |
| C125_13 `Kf6 ke8/kf8 Pc5 Pf2 pb7 pc6 pf7` | 7 | no | everything drawn |
| C145_07 `Kg4 ke4/ke5 Pe6 Pf2 Pf5 pe7 pf6` | 7 | **YES** | — |
| C145_09 `Kd4 kf4/kf5 Pe2 Pe5 Pf6 pe6 pf7` | 7 | **YES** | — |
| C145_13 `Ka5 kc5/kc6 Pb2 Pe5 Pe6 pb7 pe7` | 7 | no | (O1) draws; (O3) q at c5 draws |
| C145_15 `Ka4 kc4/kc5 Pb2 Pf3 Pf4 pb6 pe6` | 7 | no | (O1) draws at both roots; q at c5 drawn both sides |
| C145_16 `Kb6 kb8/kc8 Pb2 Pe5 pb7 pe6 pf7` | 7 | no | (O2) root c8, White to move, lost; …Kd7 wins for Black there; (O3) q at b8 draws |

All 15 verdicts equal the referee's table 3; with F1–F4 (K63) this is 5 of 19.

FENs of the five YES groups (roots: Black to move and White to move are the same board; q's: Black to move / White to
move, no e.p. right arises in any of them):

| group | root 1 | q after freeze at root 1 | root 2 | q after freeze at root 2 |
|---|---|---|---|---|
| C125_05 | `8/1p6/1Pp5/2P5/1k1K4/8/2P5/8` (kb4) | c2–c4: `8/1p6/1Pp5/2P5/1kPK4/8/8/8` | `8/1p6/1Pp5/1kP5/3K4/8/2P5/8` (kb5) | c2–c3: `8/1p6/1Pp5/1kP5/3K4/2P5/8/8` |
| C125_08 | `8/1p3p2/1P3P2/2k1K3/8/8/1P6/8` (kc5) | b2–b3: `8/1p3p2/1P3P2/2k1K3/8/1P6/8/8` | `8/1p3p2/1Pk2P2/4K3/8/8/1P6/8` (kc6) | b2–b4: `8/1p3p2/1Pk2P2/4K3/1P6/8/8/8` |
| C125_10 | `8/1p3p2/1P3P2/2K1k3/8/8/5P2/8` (ke5) | f2–f3: `8/1p3p2/1P3P2/2K1k3/8/5P2/8/8` | `8/1p3p2/1P2kP2/2K5/8/8/5P2/8` (ke6) | f2–f4: `8/1p3p2/1P2kP2/2K5/5P2/8/8/8` |
| C145_07 | `8/4p3/4Pp2/5P2/4k1K1/8/5P2/8` (ke4) | f2–f4: `8/4p3/4Pp2/5P2/4kPK1/8/8/8` | `8/4p3/4Pp2/4kP2/6K1/8/5P2/8` (ke5) | f2–f3: `8/4p3/4Pp2/4kP2/6K1/5P2/8/8` |
| C145_09 | `8/5p2/4pP2/4P3/3K1k2/8/4P3/8` (kf4) | e2–e4: `8/5p2/4pP2/4P3/3KPk2/8/8/8` | `8/5p2/4pP2/4Pk2/3K4/8/4P3/8` (kf5) | e2–e3: `8/5p2/4pP2/4Pk2/3K4/4P3/8/8` |

Append ` b - - 0 1` or ` w - - 0 1`. In each: root, Black to move, lost (every move, the shuttle included); root, White
to move, won by the freeze only; both q's lost for the side to move.

**Fresh lookups.** 25 requests through `realchess/probe.py` (own cache, ledger `tb_ledger.jsonl`, cap 25). 23 re-probed
cached answers of the YES groups (roots and q's): all 23 agree with the K65 cache in the category and in every move's
category. The other two were spent by a bug of mine before the spot check (the main pass was allowed online): one legal
position not in the K65 cache (C125_09, q after the non-freeze f2–f3 at e4, Black to move) and its White-to-move twin,
which is illegal (Black in check) and returned HTTP 400. Neither affects a verdict.

## 6. EDITS.md

Every computed statement in the referee's EDITS.md that I checked holds. One citation is off: in the Corollary 4.17 edit,
"White wins Aux at every bad move (Corollary 4.19)" — the step from Aux to the results of ω is Theorem 4.18 (c) and (b);
Corollary 4.19 is the T_K test and (B1) as a special case. Correction in `EDITS.md`. (Optional, not required: the
program lists for C125_09 and Proposition 4.24 may add "and the K66 checker's k66" as a further independent program.)

## What was not checked

- The census itself (23 + 25 hits, 38 distinct, 26 shapes, the four 2 + 2 groups), and (B1) for the 27 groups where it
  holds; the classes not searched by anyone.
- Cylinder boards (my program is flat 8×8 only); Z_O and H10 were not used for validation.
- The two wasted lookups' positions were not used; q's of the extra king freezes in chess were deduced, not probed.
- No hand proofs; the "why" sentences of section 2 are readings of computed move values.

## Memory and runs

All runs under a minute (longest 36 s), each under `/usr/bin/time -l` with a watchdog on the solver's own PID (0.2 s
polls, kill at 2.0 GB, plus a 60 s limit; `src/wdl.sh`; `src/wd.sh` is the heavy.sh variant, queued once for F2 and
stopped by me before it got a slot, so it never ran). Peak RSS 1.49 GB (C145_25, T up to 4); no watchdog kill. PIDs in
`pids.log`. Logs in `logs/runs.tar.xz` (all solver outputs) and `logs/chess66.out`; fresh-lookup cache in
`logs/tbcache66.tar.xz`. Binaries were built outside the repository and deleted.
