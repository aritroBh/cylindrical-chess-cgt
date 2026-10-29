# K32 referee report (VERIFY.md), 2026-10-28

Verdict: ACCEPT WITH FIXES. The mathematics is right and every number I re-computed matches. The fixes are to labels and wording (list in section 5). Replacement edits are in `verify/EDITS.md`; they replace K32's three blocks.

I reused nothing from an earlier referee (`verify/` was empty). I read K32's `EDITS.md`, `summary.json`, the logs `A_enum4_root.txt`, `A_root_n123.txt`, `named_table.txt`, `cmp_earlier.txt`, and the header comments of `stopsA.c` and `stopsB.c`. My code (`verify/scripts/vref.c`, `pyref.py`) was written from the definitions, not from their solvers. Their logs were used only to compare my output with.

## 1. Definitions used (LOOPY section 3 Conventions)

Terminal-free finite game, "wins" = forced win in finitely many moves (least fixed point), no draws for a stopper plus a short number. y + C is y with C Left tokens, which is the integer game C. lambda(y) is the least C >= 0 with Left winning y + C moving second, rho(y) the least C >= 0 with Right winning y - C moving second (Left first). Stops: Siegel's recursion D1 with the number clause (y equals a number x iff both players lose moving first in y - x), and the supremum characterisation D2 (RS(y) = sup of the dyadic x with Left winning y - x second, LS(y) = sup of the x with Left winning y - x first).

## 2. The proof, re-derived

- (R1) is the case x = -C of D2. (R2): if RS(y) > -C, some dyadic x > -C has Left winning y - x second; y + C = (y - x) + (C + x) with C + x a positive number, Left wins second in both summands, and the proof of Lemma 3.8a works for any two components, so Left wins y + C second. So (R1), (R2) are exactly D2 read at the integers. The one imported fact is D1 = D2 for stoppers (Siegel, ch. VI). I could not check the page (no network) and I could not derive it from the recursion in a few lines: a direct induction gives (R2) for non-numbers but (R1) needs LS >= RS for non-numbers, which is the number-avoidance theorem. So the label "PROVED from (R1), (R2), which are KNOWN" is the right strength, and it should say that the import is D1 = D2. D1 = D2 holds in all my runs (0 mismatches, section 3).
- (a), (b): every step is correct (C = max(0, floor u + 1) > u, also when C = 0; the three cases for the bounds are right).
- (c): the mirror is right (swap options; lambda(mirror) = rho; RS(mirror) = -LS; the number x goes to -x; the mirror of a stopper is a stopper).
- (d): right. Finite RS >= 2 gives ceil(-RS) + 1 <= -1 < 0 <= lambda. For RS < 2: u in (-2, -1] gives lambda = 0 = ceil(u) + 1, u in (-1, 0) gives 0 = ceil(u), u >= 0 uses (b). So the literal form fails exactly for finite RS >= 2.
- (e): K32 proved the last sentence but only pointed to data for the four pairs. I wrote the hand proof (it is short: *, up, over, under) into the replacement edit. The stops 0 of up, down, * are KNOWN.
- (f): correct for a terminal-free S (Corollary 3.8b is for terminal-free S; K32's text said only "a stopper"), and the bound floor(-min RS) + 1 is undefined when min RS = +infinity (then every lambda is 0). Both fixed in the edit.
- Edge points checked: RS = +inf gives lambda = 0 (R2 with C = 0, fine for infinite stops); RS = -inf gives lambda = inf (R1).

## 3. Numbers re-computed (all commands from the repository root; binaries built in a scratch directory and deleted)

Code V (`verify/scripts/vref.c`): a plain fixed-point sum solver (least fixed points of "Left wins" and "Right wins", checks that exactly one side wins every state), number games on a dyadic grid, D1 by memoised recursion, D2 checked on the whole grid, lambda and rho read from the grid. Code P (`verify/scripts/pyref.py`): Python, token-count recursion for lambda/rho (cross-checked against the number-game solver), Fraction number games on a 1/32 grid, own stops recursion.

| Check | Result |
|---|---|
| Class counts, own enumeration, root 0, all nodes reachable, canonical under permutations of the other nodes (`vref all N 3`) | 3, 43, 4,281: equal to K32 |
| 4 nodes: all 2^32 labelled graphs, `vref enum4 lo hi 3` in 64 chunks (`scripts/run_enum4.sh`, merge `scripts/merge_enum4.py`, `logs/enum4_merged.txt`) | 12,958,975 labelled rooted stoppers; 2,169,427 classes: equal to K32 (this was COMPUTED-1 for K32; now two enumerators agree) |
| Corrected relation, lambda and rho, at every node of every 4-node class (8,677,708 nodes) and every root | 0 violations; infinity pairing 0 violations; D2-vs-D1 grid mismatches 0; number ambiguity 0 |
| Literal form, root only | 3 (3 nodes) and 1,210 (4 nodes): equal to K32; literal fails outside "RS >= 2 / LS <= -2" 0 times, holds inside it 0 times: so "exactly" is confirmed |
| Signature table (lambda, rho, LS, RS) of the 4-node classes | 48 signatures, counts identical to `logs/A_enum4_root.txt` |
| Random labelled stoppers, 4 to 8 nodes (`logs/vref_rand*.txt`; about 700,000 nodes) | 0 violations of the corrected relation, 0 D2 mismatches; literal form fails exactly for RS >= 2 / LS <= -2 |
| Python P on 1,100 random stoppers of 4 to 6 nodes (5,200 nodes, `logs/sample_for_py.txt`) | 0 mismatches against V; 0 corrected violations; literal iff RS < 2 asserted at every node |
| Named games (`scripts/named_py.py`, `logs/named_py.txt`) | all 18 rows equal K32's `named_table.txt`: on, off, 0, over, under, *, 1, 2, -1, -2, 1/2, up, down, +-1, {on\|off}, {0\|off}, {on\|0}, K21's tempo stopper |
| Smallest counterexample | the integer 2 = {1\|}, 3 nodes, RS = 2, lambda = 0; it is one of the 3 literal violations on 3 nodes |

Hidden cut-offs: the grid ranges over |x| <= n + 2 (n + 2 is above any finite stop and reserve in the tested sizes) and denominators 1/8 (n <= 4 exhaustive), 1/16 to 1/64 (random); a lambda above the range would show up as an infinity-pairing violation, and there are none. The 5-node class count was not computed by anyone; the extrapolation in K32's text is labelled as such. The random generator has edge probability 8 to 30 percent and is not uniform over classes; K32 says so.

## 4. Labels

- Reduction to (R1), (R2): PROVED (confirmed). Import: D1 = D2 for stoppers, KNOWN (Siegel), not re-derived by K32 or by me; the reference is from memory in both reports. Fine as labelled once the import is named exactly.
- Data: CHECKED-2 holds (three C implementations and one Python agree). K32's own n = 4 class count was COMPUTED-1; it is now CHECKED-2 through my enumerator.

## 5. Problems and fixes

1. The import is described as "(R1), (R2)"; it is really D1 = D2. Named in the edit. Minor.
2. (e): first sentence rests on data, not on a proof, although the header says PROVED. Fixed with a hand proof.
3. (f): "a stopper S" should be "a terminal-free stopper S"; min RS = +infinity case. Fixed.
4. Status row: named T3.9' but it is a proposition and the table has a P3.9-P3.10 row; placed after T3.11. Renamed P3.9' and moved after the P3.9-P3.10 row. A row for the referee table (second table) added.
5. Tags: K32's text has no referee tag; added "re-derived by the K32 referee, 2026-10-28".
6. K32's chapter reference [S, ch. VI] for the stops is from memory in both of us. Marked in the edit.
7. OLD blocks of K32's EDITS.md occur exactly once in the current LOOPY.md (checked by script against the file as of 01:58); the same holds for the four blocks in `verify/EDITS.md`. K32's block 3 (anchor after T3.11) is replaced by mine; do not apply both.

## 6. Housekeeping

Binaries and the scratch directory were deleted; no process of anyone else was touched (I stopped only my own waiting driver, PIDs 99509 and 99518, by PID). The 4-node chunks ran at nice -n 15 without the lock, each under one CPU-minute (about 2 to 20 CPU-seconds). `verify/` is about 2 MB.
