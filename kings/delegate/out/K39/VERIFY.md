# K39 referee report (2026-10-29)

Brief: `kings/delegate/briefs/K39_cylinder_chess_duds.md`. Checked: `kings/delegate/out/K39/findings.txt` and
`kings/delegate/out/K39/EDITS.md`. Referee files are in `kings/delegate/out/K39/verify/`.

## Verdict

The main results stand: neither Z_B (cyl:7×6, cyl:8×6) nor Z_C (cyl:8×6) is exactly two-shuttle in chess, and the
counts, the drawing deviations and the drawing children are correct. **One sentence of EDITS.md is wrong** (the second
edit, about Kc3–d2 beside the (D, D) contexts), and `findings.txt` makes the same mistake in two places. A full
replacement set is in `verify/EDITS.md`. It changes only that sentence (and the header). All 8 of its edits apply to
LOOPY.md as it stands (8 applied, 0 rejected).

## 1. The referee's solver

`verify/rf39.cpp` (binary `rf39`, deleted when the runs finished) is a third solver. I wrote it from `kings/SPEC.md` alone
and did not read kpsolve.c, kp39.c, own39.cpp, own2.cpp, ownref.cpp or kq3.cpp while writing it. It is a different design
from both investigator families:
- it solves layers lazily and recursively, keyed by (pawns, sorted officer codes);
- it evaluates en-passant positions on the fly instead of storing them;
- inside a layer it runs counting retrograde analysis, finding predecessors by un-moving a king or officer and then
  checking each un-move forward.

It supports:
- the double step and e.p.;
- the cylinder;
- a total cap and a cap for each colour;
- a promotion set for each colour;
- bound A or bound B;
- the capture refinement, which I implemented from the definition in `findings.txt` §1. A capped promotion by the side
  the bound favours is scored as the opponent's best legal capture of the new piece. If no such capture exists, the
  promoter wins.

Usage and scripts:
- usage: `rf39 W H CYL A|B CAP CAPW CAPB PROMW PROMB REFINE`;
- run scripts: `verify/val.sh`, `verify/p1.sh`, `verify/p2.sh` / `p2b.sh` and `verify/val2.sh`, all through
  `kings/delegate/heavy.sh` at nice 15;
- comparison script: `verify/cmpk.py`, which compares root values and full move lists, with move names normalised;
- peak RSS 0.76 GB.

Validation against kpsolve:
- I compared 76 random cyl:7×6 positions from `in/rand_cyl_7x6.in` (bound A, no refinement) with the investigator's
  kpsolve output: 0 root differences and 0 move-list differences.
- I stopped the rest of that 150-position run myself, because it was slow (each random position opens new layers).
- `verify/val2.sh` compared random cyl:8×6 positions with the refinement, bound A, against kp39 `--refine`. I stopped it
  after 7 positions (2 of them illegal), because the machine load had reached about 150. Result: 0 root differences and
  0 move-list differences.
- The refinement is also exercised by all the part-1 and context-1 runs below, which agree with kp39 `--refine` move by move.

## 2. Part 1 values, re-run with rf39 (bounds A and B as separate runs)

| run | rf39 result | compared with | differences |
|---|---|---|---|
| Z_B cyl:7×6, refinement, roots + 2 children | 8 roots D at A and B; children `Kb2 kg5 … w`, `Kd2 kb5 … b` D | kp39 `--refine` (`ZB_kp39_*`, `ZBk_kp39_*`) | 0 root, 0 move |
| Z_B cyl:8×6, refinement, roots + 2 children | same (wrap move Ka4–h5) | kp39 `--refine` | 0 root, 0 move |
| Z_B cyl:8×6, no refinement | (W, L) at all 8 roots | kpsolve (`ZB_kp_cyl_8x6`) | 0 root, 0 move |
| Z_B flat 7×6, refinement, roots + child `Kd2 kb5 … b` | 8 roots D, child D | kp39 `--refine` | 0 root, 0 move |
| Z_C cyl:8×6 cap 1, with and without refinement | (W, L) at all 8 roots | kp39 / kpsolve | 0 root, 0 move |
| Z_C cyl:8×6 A′ (cap 2, capw 1, capb 1, promb Q, bound A, no refinement) | 8 roots D, 4 children D | kp39 A′ with refinement (`ZC_c2_Ap`, `ZCk_kp39_Ap`) | 0 root, 0 move |
| Z_C cyl:8×6 B′ (cap 2, capw 1, capb 1, promw Q, bound B, no refinement) | 8 roots D, 4 children D | kp39 B′ (`ZC_c2_Bp`, `ZCk_kp39_Bp`) | 0 root, 0 move |

A′ and B′ give identical move lists, so every Z_C value in these lists is exact.

Z_B on the cylinder:
- My counts: 38 moves at the 8 roots, of which 8 are shuttles.
- Of the 30 deviations, 28 lose and 2 draw: Kc3–d2 from (c3, b5), and Ka4–g5 (Ka4–h5 on cyl:8×6) from (b2, a4).
- The moves from both children are as findings §2.1 says.

Z_B on flat 7×6:
- 34 moves: 8 shuttles, 25 losing deviations, and Kc3–d2 from (c3, b5), which draws.

Z_C:
- 40 moves: 8 shuttles, 24 losing deviations and 8 drawing ones.
- The drawing deviations are Kc2–d2 and Kc3–d2 (each against ka4 and ka5) and Ka4–h5 and Ka5–h5 (each against Kc2 and Kc3).
- Their four children are exactly D.

So findings claims 1–9 are confirmed, and each now rests on three implementations.

Soundness of the restricted runs:
- A′ is bound A with Black restricted: a Black promotion beyond one queen counts as a White win, and Black may only
  promote to a queen. This can only raise the value, so A′ ≥ the true chess value.
- B′ is the mirror, so B′ ≤ the true value.
- The refinement only restricts the defender, so it is sound for both bounds.
- So A′ = B′ gives the exact value in unrestricted chess. The edits say "at cap 2 with one officer a side", which is
  weaker than this but not wrong.

## 3. Part 2, re-run with rf39: context 1 (Pe2 / pe4, flat 7×6, refinement, both bounds) and its parked comparison

- Z + H (`verify/out/c1_A.out`, `c1_B.out`):
  - all 8 roots are D;
  - every move value is the same as kp39p's;
  - bound A: 33,992 layers and 3.6e9 index slots, 3,692 s, 0.76 GB;
  - bound B: 34,034 layers, 8,003 s wall under load, 0.58 GB.
  - Compared with kp39p (`logs/r/c1_kp_{A,B}.out`): 0 root differences and 0 move-list differences at both bounds.
- Parked H (`Ka1 ka6 Pe2 pe4`):
  - White to move: W (Ka1–b2 wins);
  - Black to move: D.
  - This confirms findings claim 11 (parked W, Z + H D at the 4 White-to-move roots).
- Kc3–d2 beside e2/e4:
  - from (c3, b5) it **loses**;
  - from (c3, a4) it **draws**, and it loses at that root on the flat board alone.
  - rf39, kp39p and own39p all agree on this.

I did not re-run the other 7 contexts. Their part-2 values are CHECKED-2 by the investigator's two families. I read every
row of `logs/part2_table.txt` against the raw logs where it matters (below).

## 4. Errors in findings.txt and EDITS.md

1. **Kc3–d2 from (c3, b5) beside the (D, D) contexts (EDITS.md, second edit; findings §0 item 4 and §3).**
   - EDITS.md says the move "is still exactly D beside the four contexts whose prediction is (D, D)".
   - findings §3 says "exactly D in contexts 1, 67, 335, 670 …; it loses in contexts 0, 3, 4 and is undecided in 137".
   - The raw logs (`logs/r/c*_kp_{A,B}.out`, `c*_own_b{0,1}.out`) and rf39 on context 1 show otherwise:
     - five contexts, not four, have prediction (D, D): 0, 1, 67, 335 and 670;
     - from (c3, b5) the move is D in 67, 335 and 670, **L in 1**, L in 3 and 4, and undecided ((W, L)) in 137;
     - **in context 0 (e2/e3) the move is illegal**, because pe3 guards d2, so it does not "lose" there;
     - in context 1 the drawing Kc3–d2 is the one from **(c3, a4)**, a deviation that loses beside the empty context.
       `logs/part2_table.txt` lists it correctly ("c1 Kc3 ka4 … w -: Kc3d2 -> D"); the prose misread it.
   - No root value changes. The replacement sentence is in `verify/EDITS.md`.
2. findings §3 names contexts 4 and 137 as the decisive contexts where Z-moves of the winning side are not punished. Context 3
   (e2/f2, (L, L)) is decisive too, and several of Black's deviations win there (Kb5–a6, b6, c6, c4–c3, b3–b2). This is not
   in EDITS.md, so no edit is needed.
3. The Kc3–d2 sentence of the second edit is the only edit error. I checked every other number and label in the eight edits
   against the logs:
   - the 8 context pairs;
   - 60/64 exact roots, 0 disagreements, and the 4 roots at (W, L) (Pe4 / pf4, Black to move, prediction W);
   - parked Pe2 / pe4 with White to move: W against D;
   - 4,413 contexts and the estimate of about 61 days;
   - 28/30 and 24/32;
   - the wrap moves and children;
   - the CHECKED-2 / COMPUTED-1 / KNOWN labels.

   No edit labels a solver result PROVED.

## 5. Housekeeping

- `verify/pids.log` holds every PID I started.
- I killed only my own PIDs:
  - 86702 and 86818: the slow validation run;
  - 17748: the p2.sh shell, so that its bound-A run finished alone while bound B ran as p2b.sh;
  - 4092 and 4127: val2, under load.
- No pkill or killall.
- I deleted `verify/rf39` by exact name at the end. The source is kept.
- No file is over 256 KB.
