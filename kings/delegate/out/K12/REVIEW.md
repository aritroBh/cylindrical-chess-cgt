# K12 review: root clause sweep, rechecked without e.p. rights on cyl:6x6, 7x6 and 8x6 by a second checker

**Outcome (2026-10-27).** Accepted. On the 6x6 roots without an e.p. right, an independent recheck finds the
same root set and **0 certified roots whose frozen value disagrees with the credit**. The P11 root clause is
CHECKED-2 there; the rest of K12 stays COMPUTED-1.

## What K12 claims

- Class: Ka1, black king at the top of the a-file, pawns on files c..W−2, both sides to move, legal e.p. rights
  included. 6x6 and 7x6 with ≤ 3 pawns a side, 8x6 with ≤ 2.
- 716,962 roots with a passer. Of these, 687,262 are certified by Proposition 2.11, and none is a violation.
- 20,376 roots where the credit W(X) disagrees with the frozen value. None of them is certified, so the root
  clause is what keeps P11 sound on them.
- Controls: dropping (H4) gives 48 violations; weakening (H5) gives 15,868.

## Recheck (integrator)

Script: `integrator_v.py` (run as `v.py W H maxp`). It shares no code with K12's `gen.py`, `checker.py` or
`process.py`.

- **Roots.** I enumerate the same layout without e.p. rights. That gives **76,744** roots on 6x6. K12's
  `gen.process_board(6,6,3)`, restricted to `ep is None`, also gives 76,744. Its other 5,630 roots carry an e.p.
  right, so its total is 82,374.
- **Credit.** For a single passer, `cylcgt.pawns.value()` (asserted ±BIG). For a race, the count rule of
  `_child`, with N the side to move.
- **Frozen value.** The repository's `kings/kpsolve --frozen --cap 1`, run through `heavy.sh`.
- **Certification.** `hyps()` from the K10r2 search reviewer's `chk.py`, written by a different agent from
  K12's `checker.py`. A root is certified if some passer p of the credited side β satisfies (H1)–(H5).

| 6x6, no e.p. | single | race | total |
|---|---|---|---|
| certified, agree | 24,614 | 49,796 | 74,410 |
| certified, **disagree** | **0** | **0** | **0** |
| uncertified, agree | 476 | 12 | 488 |
| uncertified, disagree | 1,758 | 88 | 1,846 |
| roots | 26,848 | 49,896 | 76,744 |

- My uncertified-disagree list contains K12's example, `Ka1 ka6 Pc2 pd3 pe5 w -`. Its frozen value is WW
  against a credit for Black. I checked it by hand: (H4) fails because d3 is at ρ(p)+2.
- My certified count (74,410) cannot be compared with K12's 79,698 for 6x6, because K12's figure includes the
  e.p. roots. K12 does not publish its counts without them.

## Labels

- P11 root clause on cyl:6x6, pawns on c..e, ≤ 3 a side, no e.p. right: **CHECKED-2**. Two checkers, two
  generators and two hypothesis implementations agree, with 0 certified violations.
- The e.p. roots: **COMPUTED-1**. K12's brute-force μ_ω check was written by the same author, so it does
  not count as a second check.
- 8x6, ≤ 2 a side, no e.p. right: **CHECKED-2** as well. The recheck (`v.py 8 6 2`) gives 68,036 roots, the same number
  as K12's `gen.process_board(8,6,2)` restricted to `ep is None` (its other 3,876 roots carry an e.p. right).

| 8x6, no e.p. | single | race | total |
|---|---|---|---|
| certified, agree | 10,482 | 54,472 | 64,954 |
| certified, **disagree** | **0** | **0** | **0** |
| uncertified, agree | 872 | 88 | 960 |
| uncertified, disagree | 1,746 | 376 | 2,122 |
| roots | 13,100 | 54,936 | 68,036 |

- 7x6, ≤ 3 a side, no e.p. right: **CHECKED-2** (2026-10-28). `integrator_v2.py 7 6 3 20000`, the same check run in 26
  chunks of 20,000 roots through `heavy.sh`, so the slot was released between chunks (22:40–about 01:00, at load ~270).
  It gives 515,780 roots, the same number as K12's `gen.process_board(7,6,3)` restricted to `ep is None` (its other
  46,896 roots carry an e.p. right; `logs/k12gen_7x6_noep.txt`). Output: `logs/v2_7x6_3.json`.

| 7x6, no e.p. | single | race | total |
|---|---|---|---|
| certified, agree | 113,916 | 382,932 | 496,848 |
| certified, **disagree** | **0** | **0** | **0** |
| uncertified, agree | 4,072 | 204 | 4,276 |
| uncertified, disagree | 13,020 | 1,636 | 14,656 |
| roots | 131,008 | 384,772 | 515,780 |

- Still COMPUTED-1: the 56,402 roots with an e.p. right (5,630 + 46,896 + 3,876 on 6x6, 7x6, 8x6).
