# K55 referee report (2026-11-23)

Independent check of `findings.txt` and `EDITS.md`. Everything the referee ran is in `verify/` (code, inputs, `logs/`,
`pids.log`). The referee's own solver is `verify/rv55.cpp`, written for this check from the model statement only; it
shares no code with za, zb or rz.

## Verdicts

| Claim | Verdict | What was run |
|---|---|---|
| 1. The widened keys of za and rz are sound on cyl:10×6 | **CONFIRMED** | diffs read; injectivity argued; node counts matched by an own solver |
| 2. P values of the modified solvers on the 2 + 3 group | **CONFIRMED** (one stalemate case explained) | 300 sampled states: za, rz, rv55 against `kp_p --pmodel` |
| 3. The 2 + 3 group H10 has the results of over on the battery; G9, G10 show Z_O's 38 differences | **CONFIRMED** on every test re-run | rv55 on 31 test games (124 results per group), H10, Z_O, G9, G10; rz with both stalemate conventions on H10 |
| 4. Mechanism | **found** (below) | rv55 with T = −1…−6, −10, −20, −40, off, per-move values |
| 5. tiny-2 refuted at d4, ⇑\* refuted at d5 by their negatives | **CONFIRMED** (encodings correct) | rv55 on Z_O with miny-2 and ⇓\*; own Python for tiny-2 + miny-2, ⇑\* + ⇓\* |
| 5′. "No candidate survives at either root" | **CONFIRMED, but not by the investigator's data**: {0 ∣ tiny-30} survived all 752 games of the scan (`logs/cands.txt`) and was never run against tests55c/d; the referee refuted it | rv55: Z_O ⊞ −{0 ∣ tiny-30}; own Python: {0 ∣ tiny-30} ⊞ T for tests55c/d against za's Z_O column |
| 6. Z_O is not a stopper (4-cycle Kd4–d5, Kf5–f6, Kd5–d4, Kf6–f5) | **CONFIRMED** | each move is in rv55's legal-move list at the four positions; attacks checked by hand |
| 7. §3 defines no order on loopy D-games; the difference test is not reflexive here | **CONFIRMED** | read §3: only "equals a number" for stoppers (Prop. 3.9′), the "Left wins G + n second" convention, the Reading after Thm 3.8 (Siegel's forms for stoppers); Prop. 4.5's proof is the difference game |
| Edits | **apply `verify/EDITS.md`** (replacement; the investigator's set applies cleanly but needs wording fixes) | apply_edits.py on scratch copies |

## 1. The code changes (za, rz against K47)

`diff K47/src/za.cpp K55/src/za.cpp` and `diff K47/verify/rz.cpp K55/src/rz.cpp`. Squares are r·W + f. Pawns stand only
on ranks 2 to 5 (a promotion leaves the board), so pawn bits are at most 4·10 + 9 = 49 on cyl:10×6; e.p. targets are on
ranks 3 and 4 (≤ 39); king squares ≤ 59 need 6 bits.
- za: key = (wp | wk≪50 | bk≪56, bp | (ep+1)≪50). Fields 50–55 and 56–61, each 6 bits, values ≤ 60: injective. The map is
  `unordered_map` with full key equality, so hash collisions cost time only. The K47 key (wk≪48) overlapped pawn bits
  48, 49 and was wrong for W = 10 only. Freeing the map and node list after the build is safe (root ids taken first;
  the e.p. flag kept in `hasEp`).
- rz: K1 = wp | wk≪50 | ep≪56 (63 = none), K2 = bp | bk≪50: injective. Open addressing compares both 64-bit keys; the
  table (2^25) stops the run above 80% load. Value and counter packed in one byte (counter overflow aborts); the FIFO
  replaced by level bit sets, which changes only the order of retrograde steps, not the fixed point. Terminal parsing
  (W in L, B in R) is not used by the decisive tests.
- No truncated field, so no node can be merged with another and no Black move can be lost. Independent evidence: rv55
  (file-major squares, its own key) finds exactly za's component sizes: H10 2,550,522, Z_O 3,914,687, G9 5,232,179,
  G10 6,743,855 nodes. A merge would lower these counts.

## 2. P values on the 2 + 3 group (`verify/cmpP.py`, `logs/cmpP.txt`)

300 states sampled (seed 5555) from za's value dump at T = 0 (every 97th node): 220 without e.p., 20 drawn ones, 60
with an e.p. target. `kp_p --pmodel` (compiled from `K44/scripts/kp_p10.c`, bounds exact at all 300): values L 183,
W 89, D 28. za differs at 1 of 300; rz and rv55 (240 states without e.p., run with the placements as roots) differ at 0.
The one difference, `Kb1 kb4 pa3`, White to move (with or without the e.p. flag): kp_p D, za L, and rz and rv55 also L.
After Ka1/Ka2 lines Black can stalemate White; P counts stalemate as a draw (Definition 1.5), the sum's rule "a side with
no move loses" as a loss. So this is the convention, not a key error; rz with convention C gives D there. It does not
touch the battery: rz with stalemate = draw gives the same 104 results for H10 on 26 test games as with N
(`logs/rzC_H10_main.out`, `logs/rzN_H10_main.out`).

## 3. Third solver on the decisive tests (`verify/rv55.cpp`, `gen_rv.py`, `cmpInv.py`)

Model reading used: the group is the P game of its own pieces (files wrap, ranks do not; double steps from the first
rank, e.p.); a legal promotion is a terminal win for the promoter; a side in check may not move in T; a move in T clears
the e.p. right; a side with no legal move loses; infinite play is a draw. Values by repeated sweeps of all product states
(group node × test node × mover) to the least fixed point. Test games are built by its own Python game algebra
(`gen_rv.py`), and r(over ⊞ T) by its own small sweep.

Tests: 0, \*, ↑, ↓, ↓ + \*, ↑ + \*, under, under + \*, over, over + \*, ↓ + ↓, under + ↑, under + ↓, under + under,
1 + ±1, ±1, 1, −1, on, off, dud, over + ↓, miny-2, tiny-2, ⇑\*, ⇓\* (26), plus −2 … −6; both roots, both sides.
- H10: equal to over at all 104 results of the 26 tests (under, under + \*, under + ↑, under + ↓, under + under: DD,
  as over; \*, ↓, ↓ + \*, ↓ + ↓, miny-2, ⇓\*: WW, as over). rz (N) gives the same 104.
- Z_O (cyl:8×6): reproduces K47's differences exactly where they fall in these tests (\* at d4 with Black first; ↓ at
  d4 both and d5 Black first; under and every under sum at all four; ↓ + \*, ↑ + \*, 1 + ±1 at d4 Black first;
  ↓ + ↓ as ↓). So the solver separates the two groups.
- G9, G10: identical to Z_O on all 104 results of the 26 tests.
- Against the investigator's za logs (31 test names matched, 124 results per group): 0 differences for H10, 0 for Z_O.
Peak memory 0.60 GB (H10) to 1.68 GB (G10).

## 4. Mechanism (`logs/tempo_*.out`, `logs/tempo2_*.out`; COMPUTED-1, rv55)

Value after each Black move at the roots, with T = −n (n spare Black moves) and with off (Black may pass at will).
"loses" = White wins after the move.
- Z_O d4 root (Black: Kc4, Kd5 shuttle, Ke3, a3, e4, e3): e5–e4 **wins for every n = 1…6, 10, 20, 40**; Kc4, Ke3, a3,
  e3 lose for every n. Against off: e5–e4 still wins, e5–e3 draws, the others lose. The same holds for miny-n (Black's
  move to 0 is a spare tempo): Z_O ⊞ miny-n is a Black win at d4 for every n tried.
- Z_O d5 root (Kc4, Kc6, Kd4 shuttle, Kd6, a3, e4, e3): every non-shuttle move loses for every finite n tried; against
  off, Kd6, e4, e3 draw.
- H10 f6 root (Ke6, Kg6 shuttle, a4, a3, e4, e3): **every non-shuttle move loses for every n = 1…6, 10, 20, 40**;
  against off, Ke6, e4, e3 draw, a4, a3 lose.
- H10 g6 root (Kf6 shuttle, Kh6, a4, a3, e4, e3): every non-shuttle move loses for every finite n tried; against off,
  e3 draws, the rest lose.
So Z_O's defect is one move, e5–e4 at d4, that loses in P alone only by zugzwang and wins as soon as Black owns a single
tempo; in the 2 + 3 group no Black move has this property against any finite reserve up to 40. That is the structural
reason it tracks over on the battery. It is not a proof: only Black's moves at the two roots were examined, and White's
side (the freezes against White reserves) was not analysed this way.

## 5. Part 2 spot checks

- Encodings (`tests55.txt`): tiny2 = {0 ‖ 0 ∣ −2}, miny2 its negative, dbl_upstar = {0 ∣ ↑} = ⇑\*, dbl_downstar its
  negative: correct.
- Z_O d4 ⊞ miny-2 = (L, L) (rv55), while tiny-2 ⊞ miny-2 = 0 = (L, W): tiny-2 refuted at the Black-first result.
  Z_O d5 ⊞ ⇓\* = (L, L), while ⇑\* ⊞ ⇓\* = (L, W): ⇑\* refuted. CONFIRMED.
- {0 ∣ tiny-n} at d5: the scan (`logs/cands.txt`, 752 games) leaves {0 ∣ tiny-30} as the only survivor at root B; the
  findings then say "no candidate survives" without a run of it on tests55c/d. Referee (`verify/b30.py`,
  `logs/b30.txt`, `logs/negB_G8.out`): Z_O d5 ⊞ −{0 ∣ tiny-n} = (L, L) for n = 20, 30, 40, while the game minus itself
  is (L, W); and against the 21 loopy games of tests55c, {0 ∣ tiny-30} differs from za's Z_O column at 9 results
  (0 against tests55d). So the statement holds, now with data; COMPUTED-1 (referee).
- Order tests and the stopper count were not re-run; the 4-cycle was checked (claim 6). For the 2 + 3 group (the edits
  say it is not a stopper) the cycle Kf6–g6, Kg4–h4, Kg6–f6, Kh4–g4 is legal by hand (h4 and g4 are attacked by no
  Black pawn or king; f6, g6 by no White piece), so that remark holds too.

## 6. Edits

The investigator's set applies cleanly to the current LOOPY.md (after K48's commit): 3 applied, 0 rejected, table cell
counts unchanged, `**` balanced. Problems:
1. The K55 bullet says the 2 + 3 group "equals over at all 1,100 results"; it must say "has the results of over".
2. "The d5 root has those of {0 ∣ tiny-n} except against −{0 ∣ tiny-n}" is incomplete (for n ≤ 20 it also fails at
   miny-m, m > n), and "no candidate survives" rested on {0 ∣ tiny-30} never being run against its negative; the
   referee's refutation is now cited.
3. Not-done items that limit the H10 claim were missing: not run against the loopy and D-game candidate games, nor
   beside P contexts; cyl:11×6 and wider not tested.
4. "every result below CHECKED-2" sat next to a COMPUTED-1 candidate scan; reworded to "every solver result".
5. Added: the third solver's agreement, the P-value check, the stalemate remark, the mechanism (COMPUTED-1), and the
   explicit refutation of tiny-2 and ⇑\*.
**Apply `verify/EDITS.md`** (same three anchors): 3 applied, 0 rejected on the current LOOPY.md, cell counts unchanged,
`**` balanced; the scratch copy was deleted. Labels: solver results CHECKED-2, candidate scan and referee additions
COMPUTED-1, nothing PROVED.

## 7. Process

- All solver runs through `kings/delegate/heavy.sh` (nice 15) under `verify/run.sh` (`/usr/bin/time -l`, a watchdog on
  its own child PIDs at 2.9 GB, never triggered). First measurement: rv55 on Z_O with T = 0, 0.90 GB. Peak of all runs
  1.68 GB (rv55, G10, 26 tests); rz 1.01 GB; kp_p 19 MB. No ref3m.
- Every PID in `verify/pids.log`; nothing was killed; no pattern kills. K56's files and processes untouched. No git.
- Binaries (`rv55_k55ref`, `za_k55ref`, `rz_k55ref`, `kpp_k55ref`) deleted; the only output over 256 KB, the za dump,
  is `logs/dumpza_H10.out.xz`.
