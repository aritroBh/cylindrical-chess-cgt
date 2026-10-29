# K26 referee report (VERIFY)

Referee of `kings/delegate/out/K26/FINDINGS.md` and `EDITS.md` (P model). Date of the checks: 2026-10-29.
All files written by me are in `kings/delegate/out/K26/verify/` (scripts in `verify/scripts/`, logs in `verify/logs/`, `verify/summary.json`, `verify/EDITS.md`).

## 0. Verdict

**ACCEPT WITH FIXES.** Every computed number I re-derived with my own code agrees with K26, to the last digit. I found no counterexample, no hidden cut-off and
no false number. The fixes are about scope and labels: one overstated sentence in EDIT 5.7 (which pawn limits were searched on which board), widths 11 and 12 (not
solvable by ref3m), a "141,293 / 2,866" split that depends on move order, a Proposition 4.6 count taken from an old sample, a missing promotion/e.p./check rule in Definition 4.8, and a few labels that can be raised
(Z_B and Z_C context results, the 3 + 2 and 2 + 3 searches: COMPUTED-1 to CHECKED-2). Replacement edits are in `verify/EDITS.md` (5 blocks: §5.7, the P3.2′ status-row tail, §8 item 2 question, Conjecture 4.7 with Definition 4.8 and Lemma 4.9, the C4.7 status row; the other 5 blocks of K26's EDITS.md stand as written).

What is **not** confirmed: the four-file under/over search (5,793,156 placements), the loose-group counts for four files and for 3 + 2 / 2 + 3 on boards other than cyl:8×6, the exact-on counts beyond 2 + 2 pawns (the 103 / 78),
the on-group context agreement, the sampled Proposition 4.6 tables, flat 8×6 for under/over, and widths 11, 12 and flat 12 for the named groups. These stay as K26 labelled them (COMPUTED-1, reused) or are marked NOT_CHECKED below.

## 1. What I reused and what I did myself

- **Reused (read only):** the problem statements (LOOPY, FINDINGS, EDITS, summary.json), the solver sources `kp_p.c`, `ref3.cpp`, `ref3m.cpp`, `kpsolve.c`
  (md5 equal to K26's `summary.json`: kpsolve.c 8ff499658aa67448c89ad0955dfcbcfe, kp_p.c f668d4d4861e1d89792245632e01516c, ref3.cpp a9cd9ed267e3016c789138d86974d658, ref3m.cpp 1b0c8cd670ab54a9e3b385e14717cd63).
- **Not reused:** none of K26's logs or scripts, and nothing from the stopped earlier referee (`verify/scripts/my_t2.py`, `verify/logs/my_*`, `chainA/B`): I did not read or run them. (K26's FINDINGS call that old `my_t2.py` its "third enumerator"; I did not use it.)
  The old files are still in `verify/` (`boards.py`, `chainA.sh`, `chainB.sh`, `my_t2.py`, `logs/my_*`, ...) and I left them alone.
- **Built privately** in `verify/bin/`: `kpp` (kp_p.c, `--pmodel`), `ref3m` (K23's `ref3m.cpp`), `ref3`, `kp` (kpsolve.c). Binaries are deleted at the end.
- **My own code, written from the task text and FINDINGS section 1 (not from K26's scripts):**
  - `scripts/ref_enum.py`, `scripts/ref_enum2.py`: enumerator of two-shuttle placements (F_Z = {a, b, c}, adjacent king pairs, K1, K2, pawns on F_Z ranks 2..H−1) and leak classifier on ref3m `--moves` output. No passer filter. Every placement, every pawn limit, no cut-off.
  - `scripts/ref_under.py`: exact under groups (U1)–(U4) from the proposed Definition 4.8, **without** Lemma 4.9 and without a king filter; builds each q, with the e.p. flag for White to move.
  - `scripts/ref_on.py`: exact on / on_weak.
  - `scripts/dud_ctx.py`: my own implementation of Theorem 3.4(a) (Λ and Ρ predicates over the pawn-only game with e.p.), compared with the ref3m value of Z + context at all 8 roots.
  - `scripts/named.py`: the named-group table (4 groups, 20 boards); `scripts/roots.py`, `scripts/chk_edits.py`, `scripts/build_edits.py`, queue scripts.
- Solvers: ref3m for the searches and contexts (so my side shares no solver with K26's kpp-based searches); kpp and ref3m on the named roots; `kp` for one chess probe.
- Lock: the long runs went through `heavy.sh` (two-shuttle searches, flat 7×7); the ≤ 1 CPU-minute runs (under/over shards, contexts) ran at nice 15 without it. RSS was measured on a 2 + 2 run (0.19 GB); the larger runs stream their placements in chunks of 60,000 or run one pawn-configuration shard at a time. No pkill; I stopped my own chains by recorded PID.

## 2. Results by claim

### Claim 1: dud groups without a pawn break exist on the cylinder (Z_B, Z_C)

**CONFIRMED. CHECKED-2 stands (in fact three implementations).**

- **Roots and move lists.** `ref3m --moves` and `kpp --pmodel --moves` give identical values and move lists for Z_B on cyl:7×6 and cyl:8×6 and Z_C on cyl:7×6 and cyl:8×6 (8 roots each). Z_B: D at all 8 roots, every non-shuttle move L (White) or W (Black), on both boards.
  Z_C on cyl:8×6: D at all 8 roots, every non-shuttle move loses at once; on cyl:7×6 Z_C is (W, L) with Kc2–d2 / Ka4–g5 as the wrap leaks. All as in FINDINGS 2. `logs/` and `work/zb.txt`, `work/zc.txt` (roots) were reproduced; the commands are in section 4.
  The two extra Black wrap moves of Z_B at the a4 roots (Ka4–g3, Ka4–g5 on cyl:7×6; Ka4–h3, Ka4–h5 on cyl:8×6) exist and lose at once (value W): confirmed.
- **The search.** My enumerator counts **817,270** placements (2 + 2, H = 6, flat and cylinder), **1,886,421** (3 + 2 and 2 + 3, H = 6) and **4,040,080** (2 + 2, H = 7) before any solver is used: the same as K26 and `audit/count_cands.py`.
  Totals of leaks over the 8 roots (promotions counted once, because ref3m prints one entry per promoting move; T = 2 in stage 1, so the counts of totals 0, 1, 2 are complete), `logs/own_*.txt`, `logs/own2_*.txt`:

| board | pawns | exact (total 0) | total 1 | total 2 | K26 (collapsed promotions) |
|---|---|---|---|---|---|
| cyl:7×6 | 2+2 | 2 (Z_B, mirror) | 0 | 8 | 2 / 0 / 8 |
| cyl:7×6 | 3+2 | 2 | 2 | 10 | 2 / 2 / 10 |
| cyl:7×6 | 2+3 | 2 | 2 | 10 | same as 3+2 |
| cyl:8×6 | 2+2 | 4 (Z_B, Z_C, mirrors) | 0 | 4 | 4 / 0 / 4 |
| cyl:8×6 | 3+2 | 4 | 2 | 6 | 4 / 2 / 6 |
| cyl:8×6 | 2+3 | 4 | 2 | 6 | 4 / 2 / 6 |
| flat:7×6 | 2+2 | 2 | 12 | 6 | 2 / 12 / 6 |
| flat:7×6 | 3+2 | 2 | 17 | 18 | per-piece counting: 2 / 17 / 13 (the total-2 count depends on how promotions are counted; totals 0 and 1 do not) |
| flat:7×6 | 2+3 | 2 | 17 | 18 | same as 3+2 |
| flat:8×6 | 2+2 | 2 | 12 | 6 | 2 / 12 / 6 |
| flat:7×7 | 2+2 | **0** | 12 | 36 | 0 / 12 / 28 (per piece) |

  The exact groups are the same sets as K26's (all 10 exact duds). Z_C and its mirror are the only exact placements without a textbook passer (Pa2/pa3 and Pc4/pc5 are blocked pairs, no pawn has an enemy pawn ahead on its own or a neighbouring file).
  So "exact duds on the cylinder: cyl:7×6 Z_B + mirror, cyl:8×6 Z_B, Z_C + mirrors" is confirmed for ≤ 2 + 2 (all boards), 3 + 2 and 2 + 3 (flat 7×6, cyl:7×6, cyl:8×6).
  Hidden cut-offs: none found. K26's stage-1 threshold T only filters on the leak count at one root, which is a lower bound of the total, and my own run uses the same argument (total ≥ leaks at root 0) with T = 2.
  The definition itself restricts to F_Z = {a, b, c} and kings on adjacent pairs, and pawns on F_Z only: that is a boundary, stated in FINDINGS, not a cut-off.
- Label: CHECKED-2 for ≤ 2 + 2 on the four six-rank boards (K26 had it), and now also **CHECKED-2 for 3 + 2 and 2 + 3** on flat 7×6, cyl:7×6, cyl:8×6 and for flat 7×7 at 2 + 2 (K26 had COMPUTED-1; my enumerator and my classifier on ref3m agree with K26's counts).
  Z_B on the cylinder is **not PROVED by hand** (K27's 26 certificates are flat): K26 says so, correct.

### Claim 2: regression on flat 7×6, 8×6, 7×7; minimum leak counts

**CONFIRMED.** See the table above. Flat 7×6 and 8×6 give Z_B and its mirror only; 12 placements at total 1 (2 + 2); flat 7×7 has no exact group and the minimum is 1, with 12 placements (my example `Ka6/a7, kc6/c7, Pa3 Pb4 / pb5 pb6` is among them; the root `Ka6 kc6 Pa3 Pb4 pb5 pb6 w` has the leak Ka6xb5 at (a6, c7), value W).
Note that K26's "leak count" is the count of non-shuttle, non-losing moves; in the total-1 placements of flat 7×7 the shuttle itself is not always a draw (root values are mixed W/D), so those are not near-duds in the sense of Proposition 3.2′. K26 does not claim they are.

### Claim 3: Z_B on other boards, Z_C table, wrap moves

**CONFIRMED for flat width 5, 7, 8, 9, 10 and cylinder width 5 to 10 on six ranks, and for the 7-rank, 8-rank and 5-rank boards of the table; NOT CONFIRMABLE for width 11, 12 and flat 12.**
`scripts/named.py` (my code, ref3m) reproduces every cell of FINDINGS 2.2 for the 20 boards I ran: flat 5×6, 7×6, 8×6, 9×6, 10×6, 7×7, 7×5, 8×8; cyl 5×6, 6×6, 7×6, 8×6, 9×6, 10×6, 8×5, 6×7, 7×7, 8×7, 9×7, 8×8 (`logs/named_own.txt`).
Z_B: 0 leaks, root values D on all six-rank boards of that list; 8 to 13 leaks on the 5-, 7- and 8-rank boards. Z_C: 0 leaks only on cyl:8×6 and cyl:9×6; 8 on cyl 6×6, 7×6, 10×6; 12 on cyl:5×6; 16 on every flat board of six ranks (its mirror 16, and 6 on flat 7×7, 8×8). Z_C does not fit on 7×5 or cyl:8×5 (illegal root), as K26 says.
kpp refuses boards with more than 64 squares **and** boards wider than 8 (it prints its usage line for width 9 and 10 too), so for widths 9 and 10 only ref3m runs, as K26 said.
**Widths 11 and 12** (cyl:11×6 = 66 squares, cyl:12×6 and flat 12×6 = 72) run in ref3m but its pawn sets are 64-bit masks, `1ULL << sq` and `>> sq` for squares of the top rank are shifts of 64 or more (undefined behaviour). The code happens to give the expected answer on this machine
(pawns never stand on the top rank; the stray bits fall on rank 1, where no pawn is), so Z_B shows 0 leaks there, but this is luck, not a computation. I did not use these cells and EDIT 5.7 should not claim them (done in `verify/EDITS.md`).

### Claim 4: contexts beside Z_B and Z_C

**CONFIRMED, and the label can be raised to CHECKED-2.** `scripts/dud_ctx.py` has my own predictor (Theorem 3.4(a): Λ_L, Λ_R, Ρ_R, Ρ_L over the pawn-only game with the e.p. flag, promotion = decisive event, both sides may pass) and compares it with the ref3m value of Z + context at all 8 roots.
Every placement of at most 3 context pawns of either colour on ranks 2..5 (counts 1 + 24 + 264 + 1,760 = 2,049 on three files, 1 + 16 + 112 + 448 = 577 on two):

| group | board | files | contexts | roots | contexts that differ | K26 |
|---|---|---|---|---|---|---|
| Z_B | cyl:8×6 | e–g | 2,049 | 16,392 | 0 | 0 |
| Z_B | cyl:7×6 | e–f | 577 | 4,616 | 0 | 0 |
| Z_B | flat 7×6 | e–g | 2,049 | 16,392 | 0 | 0 |
| Z_C | cyl:8×6 | e–g | 2,049 | 16,392 | **131** (35 with 2 pawns, 96 with 3, 0 with fewer; 754 roots) | 131 (35, 96), 754 roots |

`Pe2 pe3` beside Z_C gives (W, W) at all 8 roots, the prediction is (D, D); with kpp and ref3m `Kc2–d3` is W, and also the shuttle `Kc2–c3` is W (it leads to Kd3 next). So "Kc2–d3 wins there" is true; it is not the only winning move.
I did not diff my predictor against `dmodel.py`; both give the same outcomes on the contexts above. Files d and h (next to F_Z) were not tried by K26 or by me.

### Claim 5: no exact under or over group; loose groups; Conjecture 4.7

**CONFIRMED for ≤ 2 + 2 pawns on three files of cyl:8×6, cyl:7×6 and flat 7×6, by my own search without the king filter; and for 3 + 2 and 2 + 3 on cyl:8×6 (all 24 pawn-configuration shards of each, no exact group); NOT_CHECKED for the four-file search and for flat 8×6.**
`scripts/ref_under.py` (my code, ref3m, no use of Lemma 4.9, promotion freezes recorded separately, check by the freezing pawn recorded):

| board | pawns | placements | (U1) at both White roots | (U1)+(U2) | (U1)+(U2)+value L after every freeze (promotion = L) | exact | loose, exactly one freeze at each root |
|---|---|---|---|---|---|---|---|
| cyl:8×6 | 2+2 | 631,179 | 160,540 | 160,469 | **144,159** | **0** | **120** |
| cyl:7×6 | 2+2 | 631,179 | 160,774 | 160,697 | **144,411** | **0** | **118** |
| flat:7×6 | 2+2 | 631,179 | 154,899 | 154,802 | **140,389** | **0** | **142** |

The counts 144,159, 144,411, 140,389 and 120, 118, 142 equal those of K26's `over2.py` table and FINDINGS section 4 exactly (K26 used kpp; I use ref3m and my own enumerator). The one-shuttle placement counts (631,179 for 2 + 2) also agree.
My own count of `exact on` and `on_weak` (`scripts/ref_on.py`) equals K26's: cyl:8×6 4 / 152,262, cyl:7×6 4 / 152,554, flat 7×6 17 / 146,766.
**One reporting problem (EDIT 4.7):** K26 splits the 144,159 into "141,293 fail (U4)" and "2,866 have a promotion as the freeze". That split depends on the order in which `over2.py` tries the freezes (the first failure wins). With my order the same 144,159 split into 143,831 that fail (U4) at some freeze and 328 that pass (U4) at every freeze that is not a promotion
but have a promotion as a freeze (cyl:8×6); in total 5,791 of the (U4) failures are a freezing pawn that gives check, so that q with Black to move is not legal. The total is solid, the split is not; the replacement edit gives the total and says the split depends on order.

| board | pawns | placements | (U1) at both White roots | (U1)+(U2)+value L after every freeze | exact | loose, exactly one freeze at each root |
|---|---|---|---|---|---|---|
| cyl:8×6 | 3+2 | 1,602,414 | 271,267 | 254,258 | **0** | 198 (K26: 198) |
| cyl:8×6 | 2+3 | 1,517,293 | 599,723 | 545,277 | **0** | 175 (K26: 175) |

(K26's `over3.py` table lists smaller numbers for these two lines because it applies the king filter of Lemma 4.9 and counts the survivors of its own stages; the placement counts and the loose counts are equal, and both give 0 exact groups.)
My search treats a promotion freeze as value L and as not exact, a check by the freezing pawn as (U4) failing, and the e.p. flag only for White to move: the rules K26 used (`over2.py`, `apply_move`), now written into Definition 4.8 by the replacement edit.

### Claim 6: Lemma 4.9 (no non-capturing king freeze)

**CONFIRMED. PROVED stands.** I re-derived it against the definitions.

1. Let b0 → b1 be a freeze that captures nothing, at the root R_a = (z_a, b0, Black to move), and q the position after it. No pawn has moved, so there is no e.p. right, and the pawn sets are unchanged.
2. In q with Black to move, the move b1 → b0 is legal: b0 is empty (the king has just left it); no White pawn attacks b0 (K1 for the group; the pawns are unchanged); b0 is not adjacent to the White king, which stands on z_a (K2); the squares b0, b1 are king-adjacent. Also q itself with Black to move is a legal position (K1 for z_a: no Black pawn attacks z_a).
3. The move leads to R′ = (z_a, b0, White to move). By (U1) every non-shuttle White move at R′ loses at once, and the shuttle is legal and leads to the other Black-to-move root R_b = (z_b, b0, Black to move). By (U2) and (U3) applied at R_b, Black has a freeze m′ there, and either m′ is a promotion (Black wins) or q′ = after m′ has White to move with
   a legal move and all White moves losing, value L. In both cases R_b has value L (P model: promotion wins at once; stalemate cannot occur since White has a legal move).
4. So every White move at R′ leads to value L: R′ has value L. So b1 → b0 does not lose at once (the value after it is L, not W): (U4) fails. ∎
The points a careless proof would skip are all covered: the use of K2 for the return square, the use of (U1) at R′ and of (U2), (U3) at the other root, the promotion case at the other root, and the absence of an e.p. flag. The lemma does not need the groups to be searched; and K26's `over3.py` filter rests on it (my unfiltered runs agree with the filtered counts, no group in either).

### Claim 7: exact on / off groups ("103 distinct, 78 passer-free"; context agreement)

**PARTLY CONFIRMED.** Counts of exact on groups for 2 + 2 confirmed by my own code (table in claim 5). The union of 103 over all pawn limits and 78 passer-free: NOT_CHECKED. The context agreement (Theorem 3.4(b), (c)) and the "(Pun) fails near the wrap" diagnosis: NOT_CHECKED; FINDINGS section 4 says "not diagnosed further", while `summary.json` (`verdicts.exact_on_off`) states a diagnosis ("the frozen king can reach a context pawn through the wrap or ..."); these two do not agree, and the claim text in the task summary repeats the diagnosis. Not in EDITS.md, so no edit needed, but the sentence should not be quoted as a result.

### Claim 8: fresh re-runs reproduce the earlier attempt

**CONFIRMED in substance:** every count I could compare (above) is equal to the one K26 gives, including those it marked "reused". I did not compare line by line against `audit/compare_fresh.txt`.

### Claim 9: minimum leak counts per board

**CONFIRMED** (table in claim 1). K26's per-piece promotion counting changes only the total-2 counts, as FINDINGS section 2 says.

## 3. The EDITS

- **OLD blocks:** all 10 occur exactly once in the current `kings/theory/LOOPY.md` (`scripts/chk_edits.py`, run against the file as it stands now). The same check on `verify/EDITS.md` passes.
- **NEW blocks that are accurate and can be applied as they are:** EDIT 5.3 (scratch evidence withdrawn), EDIT 3 (kings bullet tail), the P3.2′ status-row tail, EDIT 7, EDIT 8 item 2 tail, Appendix A, status row C4.7. Their numbers match (Z_C has no textbook passer: confirmed under any usual passer test, not only cylcgt's; every statement about Z_B and Z_C on the cylinder is confirmed).
- **NEW blocks that need a replacement (in `verify/EDITS.md`; the date tag there is 2026-10-27, as the task text asks):**
  1. **EDIT 5.7.** (a) "finds exactly Z_B and its mirror on flat 7×6, flat 8×6 and cyl:7×6" follows a list of pawn limits "2 + 2, then 3 + 2 and 2 + 3" and so reads as if every board had all three; flat 8×6 was searched for 2 + 2 only, flat 7×7 for 2 + 2 only. (b) Widths 11, 12 and flat 12 are not computable by ref3m (section Claim 3). (c) The context result for Z_B can be CHECKED-2 and the Z_C count (131 of 2,049) is now CHECKED-2 as well. (d) "exact alone only on cyl:8×6 and cyl:9×6" is about the boards tried. (e) Files d and h were not tried.
  2. **EDIT 8 item 2 question.** "COMPUTED-1 for 3 + 2, 2 + 3 and flat 7×7 (no exact dud there; ...)" can be read as "no exact dud with 3 + 2 pawns". It means: no new group for 3 + 2, 2 + 3, and no group at all on flat 7×7. Reworded, labels raised.
  3. **EDIT 4.7.** (a) Definition 4.8 does not say what a promotion freeze, the e.p. flag and a freezing pawn that gives check are; the search treats them as: promotion = not exact (counted separately), flag set for White to move only, check = (U4) fails. (b) The "141,293 / 2,866" split. (c) "762 of the 768 premise roots" is from the earlier, different sample; K26's final sample is 537 of 552 (FINDINGS section 6). (d) The 3 + 2, 2 + 3 and four-file claims are labelled by what the referee did, and the conjecture label is split (CHECKED-2 for the 3-file searches, COMPUTED-1 for the four-file one). (e) The proof of Lemma 4.9 gets two clauses it was missing (q with Black to move is a legal position; the freeze at the other root may be a promotion). The statement and the argument stand.
  4. **Status row P3.2′ tail** and **status row C4.7:** only the labels (COMPUTED-1 to CHECKED-2) change, so that the rows agree with the replaced §5.7 and §4.7.
- No NEW block contains a claim I could refute. No label is too strong (K26 says COMPUTED-1 where only one implementation exists and CHECKED-2 only where two agree). Two statements in the task summary are wider than FINDINGS: the label "113 groups ... kpp and ref3m" (113 groups were checked with ref3m alone; 20 groups, the 10 duds included, with both solvers) and "Fresh re-runs ... reproduce exactly" (only part of the runs were fresh; FINDINGS section 8 says which).

## 4. Reproduce (all under `kings/delegate/out/K26/verify/`; python is `/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python` or any python3, no other dependency)

- Build: `cc -O2 -o bin/kpp ../../K7/scripts/draft/kp_p.c -lpthread`, `c++ -O2 -std=c++17 -o bin/ref3m ../../K23/verify/ref3m.cpp`, `cc -O2 -o bin/kp ../../../../kpsolve.c -lpthread`.
- Roots: `python3 scripts/roots.py zb > work/zb.txt` (also `zc`, `zbm`, `zcm`); `bin/ref3m --board cyl:8x6 --moves < work/zc.txt`; `bin/kpp --board cyl:8x6 --ep on --promote QRBN --cap 1 --pmodel --moves < work/zc.txt`; flat boards in ref3m are written `flat7x6`, not `flat:7x6`.
- Two-shuttle search: `CHUNK=60000 python3 scripts/ref_enum2.py gen cyl:8x6 2 2 work/T && TMAX=2 python3 scripts/ref_enum2.py run cyl:8x6 2 2 work/T` (or `scripts/runone.sh BOARD nW nB`, `scripts/runone2.sh`); placement count: `python3 scripts/ref_enum.py count BOARD nW nB x`. Logs `logs/own_*.txt`, `logs/own2_*.txt`.
- Named table: `echo "flat:7x6 cyl:8x6 ..." | python3 scripts/named.py` → `logs/named_own.txt`.
- Contexts: `python3 scripts/dud_ctx.py ZB cyl:8x6 efg 3 i/24` (shards 0..23; ZC likewise; `ZB cyl:7x6 ef 3 i/4`; `ZB flat:7x6 efg 3 i/24`) → `logs/ctx_exh_*.txt`, `logs/ctx_*.json`.
- Under: `python3 scripts/ref_under.py cyl:8x6 2 2 3 i/40` (stride sharding of placements; for the 3 + 2 and 2 + 3 runs the shards are by pawn configuration, `i/24`), sums with `python3 scripts/sumunder.py 'logs/under_cyl8x6_22_f3_*of40.json'`. On groups: `python3 scripts/ref_on.py cyl:8x6 2 2 3 0/1`.
- Chess probe: `bin/kp --board cyl:8x6 --ep on --promote QRBN --cap 1 < work/zc.txt` gives (W, L) at all 8 roots of Z_C (15 s, 39,490,560 states, capped promotions met), as FINDINGS says (kpsolve.c md5 as in summary.json).
- Edits: `python3 scripts/chk_edits.py ../EDITS.md` and `python3 scripts/chk_edits.py EDITS.md`.

## 5. Not done

- The four-file under/over search (5,793,156 placements; K26's runs reused, not repeated), flat 8×6 under/over, flat 7×7 under/over, 3 + 2 / 2 + 3 under on cyl:7×6 and flat 7×6 (K26 did not run them either).
- Exact-on counts beyond 2 + 2, the 103 / 78 union, the on-group and loose-group context tables, the Proposition 4.6 failures, the collapsed-promotion runs.
- Any hand proof of Z_B or Z_C on the cylinder; chess beyond the one cap-1 probe.
