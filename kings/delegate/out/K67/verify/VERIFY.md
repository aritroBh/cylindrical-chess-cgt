# K77 referee report on K67 (2026-11-26)

Referee of `kings/delegate/out/K67/` (findings.txt, EDITS.md, src/, logs/, in/), brief `kings/delegate/briefs/K77_brief.md`.
Paths are relative to `kings/delegate/out/K67/verify/` unless they start with `kings/`. Labels: KNOWN (tablebase),
CHECKED-2 (two separately written programs agree; named), COMPUTED-1. No computed fact is called PROVED.

## Verdict

1. **Search: CONFIRMED, CHECKED-2 (p45a, r48).** I read the four raw outputs myself (`src/recount77.py`, own parser):
   {a,b,e} (4,018,737,400; 1,320,170,800; 895,942,831; 424,206,769; 385,255,761; 10) and {a,d,e} (3,992,135,379;
   1,302,596,389; 885,042,479; 417,540,383; 377,285,211; 3) are the same six counters from both programs, and the hit
   sets are equal after the colour mirror (10 and 3). p45a differs from K65's copy only by a header line and the memory
   guard (two lines placed before the allocation; no other change), r48 only by a header line (diff). Spot check with a
   third program, p74 (the K74 referee's P solver, `kings/delegate/out/K72/verify/src/p74.c`, copied unchanged to
   `src/p74.c`), driven by my own Definition 4.8 checker `src/def77.py`: all 13 hits are exact (both roots each side to
   move, every Black root move, every White root move, both q's each side to move, K1, K2), with the freezes K67 lists;
   30 near misses (same pawns; White king or the shuttle pair moved by one square, K1 and K2 kept, none a hit of any
   class) are all not exact. My own solver s77 (P mode) gives the same value as p74 for all 500 root and q positions
   and all 3,278 moves of these runs (0 differences).
2. **Census: CONFIRMED** (arithmetic on the CHECKED-2 hit lists). Recount from the hit lists of all four classes
   (`src/recount77.py`, written without K67's census.py or K65's recount.py): 48 distinct groups, 27 up to reflection
   and file translation; 6, 7, 8 men: 5, 19, 24 groups (4, 10, 13 shapes); 10 new (not among K65's 38); 3 of the 10
   {a,b,e} hits are K65 groups (F1 = C145_12, C145_13, C145_22, pawns on b and e only); 0 groups in both new classes;
   one new shape, `Ka5 kc4/kc5 Pa4 Pa6 Pb2 pa7` (3 + 1 pawns; freezes b2–b4 at c4, b2–b3 at c5).
3. **Classification of the 10 new groups: CONFIRMED, CHECKED-2 (ax65, `pk_sum`, s77).** s77 (`src/s77.c`, my own move
   generator, retrograde and Büchi solver, written from Definitions 1.1–1.3 and Theorem 4.18 (c), sharing no code with
   ax65, `pk_sum`, k66 or p74) gives, at every bad Black root move of the 10 groups: (B1) at every bad move for 7;
   C014_04 (B1) fails only at …Ke8–f8 (beside −1 a White loss), Aux won; C014_09 (B1) fails only at …b6–b5 at both
   roots (draw beside −1), Aux won; C014_08 (B1) fails only at …e5–e4 from f4 (loss beside −1), Aux lost, x_m ⊞ u_0
   White to move W beside T_0, T_1, L beside T_2 and T_3, root f4 (Black to move) W beside T_0, T_1, L beside T_2:
   N\* = 2. These are exactly K67's values (ax65 and `pk_sum`, `logs/cls/*.sum`); bad-move counts 8, 7, 9, 3, 12, 13,
   9, 6, 6, 10 agree too. Validation of s77 before use, on K65 groups: C125_15 ((B1) fails at the five moves of the K65
   table, Aux lost only at …Ke5–e4, ladder W, W, W, D for T_0…T_3, root e5 D beside T_3: N\* = 3), C125_09 ((B1) fails
   at …Ke5–d6, …Ke5–e6, Aux won), C125_14 (N\* = 2 at …Kd5–d4, root d5 L beside T_2): all as in Proposition 4.24 and
   the K65 referee's table. The three old {a,b,e} groups: (B1) at all 6, 9, 9 bad moves (s77, as K65). Totals over
   48: (B1) 34 (27 + 7), Aux won where (B1) fails 9 (7 + 2), Aux lost 5 (4 + 1; N\* = 3 once, 2 four times): CONFIRMED.
4. **Chess: CONFIRMED, KNOWN.** Re-read offline from K67's cache (`logs/tbcache.tar.xz`, unpacked in my tmp/, deleted)
   with my own FEN builder and reading (`src/tbr77.py`; reading checked on the cache: a move's category is from the side
   to move after it). C034_01 and C034_02 are exact over groups in chess; C014_01, C014_04, C014_05 are not, for the
   reasons K67 gives. 0 tablebase requests (every needed answer was cached; the 17 uncached positions my script lists
   are q's after extra chess "freezes" of C014_05, not needed because that group already fails (O4) at both P freezes).
   C034_01 = C145_07 and C034_02 = C145_09 reflected and moved one file: CONFIRMED (no plain translate).
   **Correction:** findings §0 says the 7 chess-exact groups are "only in 5 shapes"; they are in **2** shapes:
   {C125_05, C145_07, C145_09, C034_01, C034_02} and {C125_08, C125_10}.
5. **The edit: written anew** against the current `kings/theory/LOOPY.md` (`EDITS.md`; one edit, replaces only the
   census paragraph of Corollary 4.17 from "*Flat 8×8 census (K65" to "…eleven two-file classes, other shapes.";
   tested with `kings/delegate/apply_edits.py` on a scratch copy: applies, every other line identical). Every number
   checked: 10, 3, 23, 25; 48; 27; 5, 19, 24; five six-man groups (four 2 + 2 in three shapes, one 3 + 1); 34, 14, 9,
   5; N\* = 3 once, 2 four times; 7 of 24 in chess, the other 17 not; two chess shapes; seven two-file classes left
   ({a,c}, {a,f}, {a,g}, {a,h}, {b,d}, {b,g}, {c,e}: the 16 two-file classes up to reflection minus the 9 inside a
   searched class or its reflection; recounted by hand). No "not yet refereed" mark.

## Corrections to the investigator's numbers or wording

- findings §0, chess: "7 of the 24 … but only in 5 shapes" → **2 shapes** (see 4).
- EDITS.md: its OLD no longer matches the note (the K65 census paragraph was installed in a changed form); it cites
  Corollary 4.19 where the note now cites Theorem 4.18 (b), (c) for "Aux won at every failing move"; it omits the
  count of the groups not exact in chess (17). Superseded by `EDITS.md` here.
- C014_08 Aux value: `pk_sum` prints "N(D)"; Aux is a win/lose game (an endless play without White passes is Black's),
  so the value is a Black win (s77: L; ax65: not won). Cosmetic.
- findings §5 gives RSS; p45a's peak memory footprint was 1.28 GB (still under 2 GB).
- No error found in any counter, hit, freeze, q, bad-move count, (B1), Aux or ladder value, or chess verdict.

## Table of the 13 hits of {a,b,e} and {a,d,e}

Black king shuttles z0/z1; q = position after the freeze. "Def 4.8": programs that find the group exact.
"(B1)/Aux": programs that agree on the per-move values. N\* = ∞: results of ω (Lemma 4.15 or Theorem 4.18).

| name | group | men | class | freezes (q) | bad | (B1) fails at | Aux lost | N\* | chess | Def 4.8 | (B1)/Aux |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C014_01 | `Ka5 kc4/kc5 Pa4 Pa6 Pb2 pa7` | 6 | abe | b2–b4 at c4 (`Ka5 kc4 Pa4 Pa6 Pb4 pa7`), b2–b3 at c5 (`… kc5 … Pb3`) | 8 | — | — | ∞ | no | ref3m, kp_p, ax65, p74, s77 | ax65, pk_sum, s77 |
| C014_04 | `Ke6 kd8/ke8 Pb5 Pe2 pa7 pb6 pe7` | 7 | abe | e2–e3 at d8, e2–e4 at e8 | 7 | …Ke8–f8 | — | ∞ | no | same five | same three |
| C014_05 | `Kf5 kd5/kd6 Pb5 Pe2 Pe6 pa7 pe7` | 7 | abe | e2–e3 at d5, e2–e4 at d6 | 9 | — | — | ∞ | no | same five | same three |
| C014_06 | `Kc4 ka4/ka5 Pb2 Pb5 Pe6 pa7 pb6 pe7` | 8 | abe | b2–b4 at a4, b2–b3 at a5 | 3 | — | — | ∞ | (8 men) | same five | same three |
| C014_08 | `Kd5 kf4/kf5 Pa2 Pb3 Pe2 pa5 pb4 pe5` | 8 | abe | e2–e4 at f4, e2–e3 at f5 | 12 | …e5–e4 (f4) | …e5–e4 (f4) | **2** | (8 men) | same five | same three (ladder T_0–T_2 and root f4 too) |
| C014_09 | `Kd5 kf5/kf6 Pb3 Pe2 Pe6 pa7 pb6 pe7` | 8 | abe | e2–e3 at f5, e2–e4 at f6 | 13 | …b6–b5 (f5, f6) | — | ∞ | (8 men) | same five | same three |
| C014_10 | `Kf5 kd5/kd6 Pb5 Pe2 Pe6 pa7 pb6 pe7` | 8 | abe | e2–e3 at d5, e2–e4 at d6 | 9 | — | — | ∞ | (8 men) | same five | same three |
| C034_01 | `Kc4 ke4/ke5 Pd2 Pd5 Pe6 pd6 pe7` | 7 | ade | d2–d4 at e4, d2–d3 at e5 | 6 | — | — | ∞ | **YES** | same five | same three |
| C034_02 | `Kf4 kd4/kd5 Pd6 Pe2 Pe5 pd7 pe6` | 7 | ade | e2–e4 at d4, e2–e3 at d5 | 6 | — | — | ∞ | **YES** | same five | same three |
| C034_03 | `Kd4 kf4/kf5 Pa6 Pe2 Pe5 pa7 pd7 pe6` | 8 | ade | e2–e4 at f4, e2–e3 at f5 | 10 | — | — | ∞ | (8 men) | same five | same three |
| C145_12 (F1) | `Ka4 kc4/kc5 Pb2 Pe4 Pe5 pb6 pe6` | 7 | abe, bef | b2–b4 at c4, b2–b3 at c5 | 6 | — | — | ∞ | no (K63) | K65's three, p74, s77 | K65 + s77 |
| C145_13 | `Ka5 kc5/kc6 Pb2 Pe5 Pe6 pb7 pe7` | 7 | abe, bef | b2–b3 at c5, b2–b4 at c6 | 9 | — | — | ∞ | no (K65) | K65's three, p74, s77 | K65 + s77 |
| C145_22 | `Kd4 kf4/kf5 Pb4 Pb5 Pe2 pb6 pe6 pe7` | 8 | abe, bef | e2–e4 at f4, e2–e3 at f5 | 9 | — | — | ∞ | (8 men) | K65's three, p74, s77 | K65 + s77 |

Each q is the root with the freeze played (e.p. flag for Black after the double step, never live here); for all 13,
q is lost for the side to move either way (p74 and s77; `logs/def77.txt`). Values of the roots: all four roots of all
13 groups are White wins in P (Black or White to move). Every bad Black root move is listed with its value in
`logs/def77.txt` (P) and `logs/cls77_*.txt` (beside −1 and Aux). In chess, per position: `logs/tbr77.txt`.
Programs and authors: ref3m, `kp_p` (K45/K48 lineage), ax65 and `pk_sum` (K65 referee), p74 (K74 referee),
s77 (me). For the new groups the (B1)/Aux/ladder values now rest on two authors, not one.

## Recount (`logs/recount77.txt`)

| class | placements | exact | p45a = r48 | also in another class |
|---|---|---|---|---|
| {a,b,e} | 4,018,737,400 | 10 | six counters and hit set | 3 |
| {a,d,e} | 3,992,135,379 | 3 | yes | 0 |
| {b,c,f} | 3,712,376,700 | 23 | yes | 10 |
| {b,e,f} | 3,718,505,519 | 25 | yes (r48 run by the K65 referee) | 13 |

Four classes: 48 distinct, 27 up to reflection and file translation; by men 5 / 19 / 24 groups in 4 / 10 / 13 shapes;
new 1 / 4 / 5 groups, 1 / 0 / 0 new shapes. The regressions K67 reports (p45a flat 8×7 {b,c,f}: 785,481,597 … 3 with
F2, F3, F4; r48 8×8 {b,c,f} 2 + 2: 180,865,972 … 4) match K65's logs (read).

## Process notes

- Investigator: every run went through heavy.sh with a 0.1 s watchdog on its own PIDs; no watchdog kill; no breach of
  the 2 GB rule (largest p45a 1.28 GB footprint, r48 1.04 GB). It ran the two r48 searches side by side (`src/chainB.sh`),
  so it held **both heavy slots** from about 22:29 to 00:03 (1.6 h). Its brief only capped all agents at two heavy
  processes, so this was allowed there, but it blocks every other agent (my brief forbids it). It stopped its own first
  p45a run at a mistaken hand-back (own PIDs 68036, 51025, recorded). Solver time 11.3 h against a ten-hour budget.
  No binaries, no `__pycache__`, no executable bits, no absolute home paths in K67's files (checked); 40 tablebase
  requests in its ledger (cap 150).
- Me: about 3 minutes of solver time in all; peak RSS 68 MB (s77, T_3 ladder on C014_08); p74 at most 46 MB. Smallest
  inputs measured first (p74: 0.11 s, 20 MB; s77: 0.12 s, 12 MB); every run under 9 s. All runs direct, one at a time,
  through `src/run77.sh` (PIDs in `pids.log`), except: the validation set (C125_15, C125_09, C125_14) went through
  heavy.sh one run at a time with my watchdog `src/wd77.sh` (0.15 s polls on the solver's own PID; peak 48 MB), and one
  s77 run (P mode on the 52 root positions, 5.2 s, 46 MB) was started in the foreground without recording its PID (noted
  in `pids.log`). No watchdog kill, no kill or signal of any process. 0 tablebase requests, so no ledger or cache.
  Binaries and the unpacked cache were in `tmp/`, now deleted; no `__pycache__` (all Python run with -B), no executable
  bits, nothing written outside this folder, no git command that changes anything.

## Files

`VERIFY.md`, `EDITS.md`, `pids.log`; `src/`: recount77.py, def77.py, p74.c (copy), s77.c, cls77.py, cmp77.py, tbr77.py,
run77.sh, wd77.sh, groups_new77.txt, groups_val77.txt, groups_old3_77.txt; `logs/`: recount77.txt, def77.txt,
cmp77_p74_s77.txt, cls77_new.txt, cls77_val.txt, cls77_old3.txt (+ .err with times), tbr77.txt, def77_runs.tar.xz
(p74 and s77 inputs and outputs), cls77_runs.tar.xz (s77 inputs and outputs).
