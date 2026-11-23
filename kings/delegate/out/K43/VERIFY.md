# K43 referee report: over groups (LOOPY Conjecture 4.7, second half; §8 item 2)

Referee files: `kings/delegate/out/K43/verify/`. AI work, no human re-derivation.

## Verdict

**Confirmed, with small corrections to the text.** The main computational claim is CHECKED-2: an independent solver and test written by the
referee, from `kings/SPEC.md` and LOOPY Definition 4.8 only (the investigator's solver sources were not read), reproduces every counter of
every board. The two lemmas are correct, but Lemma 4.10 (3) needs one extra condition. Three statements in the proposed edits are wrong or
unclear (listed below). A full replacement set is in `verify/EDITS.md`. It applies to a copy of LOOPY.md: 4 applied, 0 rejected. The
investigator's `EDITS.md` also applies cleanly (4 applied, 0 rejected).

## 1. Independent solver and test (`verify/rv43.cpp`)

- **Solver.** One table per pawn configuration, holding every (White king, Black king, side to move). Layers are solved lazily in pawn-move
  order. Inside a layer, counting retrograde runs over king moves. Exits (pawn moves, captures, e.p.) are looked up in solved layers.
  Promotion wins at once for the promoter, stalemate is a draw, and a mated side loses. Positions with an e.p. flag are evaluated one ply on
  the fly.
- **Test.** The shuttler is White (under) or Black (over). Placements:
  - every unordered king-adjacent pair z0, z1 of the shuttler's safe squares (empty, not attacked by an enemy pawn);
  - every safe freezer-king square at king distance at least 2 from both, with wraparound on the cylinder.

  The conditions (U1)–(U4) are applied exactly as in Definition 4.8:
  - (U1): every non-shuttle move is answered by a win for the opponent, and a promotion fails.
  - (U2): at least one freeze, and no freeze is a promotion.
  - (U3): q with the e.p. flag if the freeze was a double step; the shuttler has a move, and q is lost for it.
  - (U4): q without a flag, legal, the freezer has a move, and q is lost for it.
- **Solver checks against ref3m** (K23's solver, run from `K44/bin/ref3m`):
  - 6,700 random positions of the referee's own generator, about 30 % with an e.p. flag where one is possible: cyl:7×6, 6×6, 9×6, 8×6 (5 files),
    8×7, and flat 7×6 and 8×6 in four windows. 0 differences.
  - The investigator's own 17,200 sample positions (`d1`, `d2`, `v_*`, `w_*` `.in`), including cyl:8×7 and 8×8. 0 differences against
    ref3m's `.ref` files. The investigator's `.txt` values also equal ref3m at all 17,200.
- **Test, regression ranges.** With the kings restricted to the group files (`rv43k.cpp`, `--kwin`):
  - K26's counts: 631,179 placements, and 120, 118, 142, 142 loose groups with one freeze on cyl:8×6, cyl:7×6, flat 7×6 and flat 8×6.
    The cyl:7×6 funnel (160,774 / 52,718 / 38,428) equals the investigator's `t_cyl7_f3.out`.
  - The three second-implementation ranges of findings §3: 63,378 placements, U1 17,438, one-freeze 10 (cyl:7×6, 2 files, 3 + 3);
    455,385, U1 34,062, one-freeze 23 (flat 7×6, 3 files, 3 + 1); 132, U1 31 (cyl:8×6, 1 file, 3 + 3). These are all equal.
  - Note: these three ranges have the kings on the group files. findings.txt does not say so, and the third range is tiny (132 placements).
- **Main search** (`verify/logs/*.out`; `verify/runq.sh` ran one process at a time through `heavy.sh` at nice 15; peak RSS 0.41 GB, 106 min in total).
  Every counter equals the investigator's table: placements, F1, F2, F3, one-freeze and F4 = 0, for each of the 9 boards and windows,
  in both orientations. The total is 6,363,129,120 placements per orientation. The layer count, 277,993, also agrees. The under and over
  counts are identical in every run. CHECKED-2.

  | board | placements | F1 | F2 | F3 | one-freeze | F4 | half-exact (referee) |
  |---|---|---|---|---|---|---|---|
  | cyl:6×6 a–d | 324,804,528 | 86,802,406 | 15,725,468 | 13,405,724 | 14,746 | 0 | 278 |
  | cyl:7×6 a–d | 555,083,926 | 150,558,022 | 27,171,815 | 23,713,838 | 25,310 | 0 | 376 |
  | cyl:8×6 a–d | 854,355,778 | 233,735,408 | 42,047,072 | 37,320,764 | 39,622 | 0 | 440 |
  | cyl:9×6 a–d | 1,223,372,878 | 336,857,625 | 60,645,813 | 54,668,909 | 62,740 | 0 | 436 |
  | flat 7×6 a–d | 540,252,838 | 148,213,198 | 27,176,949 | 24,184,446 | 37,846 | 0 | 156 |
  | flat 7×6 b–e | 494,167,071 | 133,433,083 | 23,982,314 | 21,251,107 | 28,172 | 0 | 326 |
  | flat 8×6 a–d | 832,030,888 | 230,613,197 | 42,651,951 | 38,635,165 | 61,263 | 0 | 156 |
  | flat 8×6 b–e | 772,499,055 | 211,436,086 | 38,317,797 | 34,610,215 | 47,441 | 0 | 330 |
  | flat 8×6 c–f | 766,562,158 | 207,367,994 | 36,552,662 | 32,730,598 | 37,328 | 0 | 374 |

- **Smaller check.** cyl:7×6, 3 files, 3 + 3: 92,289,276 / 25,442,949 / 5,226,857 / 4,419,901 / 5,784 / 0. Half-exact 40 and half-exact
  with one freeze 10 per orientation, as in findings §5. "40 ... both orientations" means 40 in each orientation.
- **Mirror windows.** The windows that were not run are file reflections of windows that were. The rules are symmetric under file
  reflection, so this is correct.

## 2. Near misses (findings §5)

The referee's run lists the same 10 under placements as `near1_cyl7_f3_33.txt`, plus their 10 colour mirrors in the over run.
`verify/near_ref3m.py` re-checks all 10 with ref3m alone (its own move lists): at every root (U1) holds; the zero root has one freeze, a Black
pawn push, with (U3) and (U4); the other root has one freeze, a Black king move, with (U3) and not (U4). CHECKED-2. Corrections:
- **The 10 placements are 6 king-and-pawn placements**, each with one or two shuttle partners. Up to the file reflection of cyl:7×6
  that fixes file b, they are 3 placements. The investigator's edit says "`Kb5 kg4 …` and 4 more such groups", which is wrong.
- **The other root's freeze is a king capture of a White pawn in 8 of the 10 cases.** In the other 2 (`Kg5 kb5 …` and `Kd5 kb5 …`) it is
  a plain king move. Lemma 4.9 forbids such a freeze only in exact groups.
- **"As Lemma 4.10 says it must" (findings §5) is too strong.** Lemma 4.10 assumes an exact group. At a half-exact placement it shows only
  that the push cannot be a freeze satisfying (U4) at the other root. That the push loses at once there is an observation.

## 3. Proofs (PROOF.md), re-derived

- **Lemma 4.10 (1), (2): correct.**
  - (1) uses only (U3) at R_a.
  - (2): the position after m from R_(1−a) with Black to move is exactly q̂. Both have the same pawns, the White king on z_(1−a), the Black
    king after m, and no flag, because the shuttle is a king move. So (U4) at R_(1−a) would make q̂ a White win, which contradicts (1).
- **Lemma 4.10 (3): a gap.** The statement says the position with the White king on z_(1−a) is won by the player to move, "whoever it is".
  The White-to-move half comes from (2) and needs m to be legal at R_(1−a).
  - Remark (i) of PROOF.md itself names the case where it is not: a Black double step across z_(1−a). The pawn then skips z_(1−a), the square
    stays empty and unattacked, and the shuttle can be legal in q.
  - Fix: state (3) for White to move only when m is legal at the other root. `verify/EDITS.md` does this.
- **Lemma 4.11 and its closure form: correct.** From R′, Black wins by the freeze, because q_m is lost for White ((U2), (U3)). So the
  shuttle loses at once. In a closure, every C-step reaches a state where (U2) and (U3) hold, so any adjacent pair satisfies (U1).
  - The core argument already appears in the proof of Lemma 4.9 ("the shuttle leads to the second root, value L"). The replacement edit
    credits it.
- **Labels.** PROVED is used only for the two lemmas, and the search is never called PROVED. The search was COMPUTED-1 and is now
  CHECKED-2. Non-existence stays a CONJECTURE with a search bound, as the investigator says.

## 4. Edits

- The investigator's `EDITS.md` applies cleanly: 4 of 4.
- `verify/EDITS.md` is a full replacement with the same four OLD texts. It also applies cleanly: 4 of 4. Changes:
  - CHECKED-2 for the four-file search;
  - Lemma 4.10 (3) condition;
  - the second-implementation ranges named (kings on the group files; 63,378, 455,385 and 132 placements);
  - the near-miss count and wording;
  - the K26 regression stated as 631,179 placements with 120 / 118 / 142 / 142.

  The original edit also cited 817,270 placements and 4, 2, 2, 2 exact duds; those come from the dud mode, which the referee did not
  re-run, so they are left out.

## 5. Housekeeping

- No investigator file exceeds 256 KB, and no binaries remain. `run_main.sh` and `run_ext.sh` contain absolute home-directory paths. This is
  harmless, but they could be made relative before publication.
- The referee ran one heavy process at a time through `heavy.sh` at nice 15, peak 0.41 GB. The PIDs are in `verify/pids.log`. No pkill,
  killall or pattern kill was used. The binaries `rv43` and `rv43k` were deleted by name. No git.
- Not checked by the referee: the dud mode, the `--diag` statistics (64,155,605 freeze records and so on), the Lemma 4.10 "38 roots,
  0 violations" counter, and the funnel figure "123,380,174 promotion losses". The last one equals the investigator's `promoFreeze` counter
  for cyl:7×6. The referee's counters do not split F1 − F2 by cause.
