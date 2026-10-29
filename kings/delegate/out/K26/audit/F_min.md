## 5. Minimum leak count per board (class d), with examples

The minimum total over all placements of a board and pawn limit (counts of totals 0, 1 and 2 are complete, section 1(d); per promotion piece; the same table is in section 2). The 3 + 2 and 2 + 3 results are equal on every board (the colour mirror τ is a symmetry of the P model).

| board | limits | minimum | placements at total 0 | at total 1 | at total 2 | example of the best non-exact placement (total, leak) |
|---|---|---|---|---|---|---|
| flat 7×6 | 2+2 | **0** | 2 (Z_B, mirror) | 12 | 4 | total 1: Ka5/a6, kc5/c6, Pb3 / pb4 pb5, leak Ka5×b4 (Z_A) |
| flat 7×6 | 3+2, 2+3 | **0** | the same 2 | 17 | 13 | |
| flat 8×6 | 2+2 | **0** | 2 (same as flat 7×6) | 12 | 4 | the same placements |
| cyl:7×6 | 2+2 | **0** | 2 (Z_B, mirror) | 0 | 8 | total 2: Ka1/a2, kc1/c2, Pa3 Pb2 / pa4: Pb2–b3 and Pb2–b4 both win |
| cyl:7×6 | 3+2, 2+3 | **0** | the same 2 | 2 | 10 | total 1: Ka1/a2, kc1/c2, Pa3 Pb2 Pb4 / pa4 pb5: Pb2–b3 wins |
| cyl:8×6 | 2+2 | **0** | 4 (Z_B, Z_C, mirrors) | 0 | 4 | total 2: as on cyl:7×6 |
| cyl:8×6 | 3+2, 2+3 | **0** | the same 4 | 2 | 6 | |
| flat 7×7 | 2+2 | **1** | 0 | 12 | 28 | total 1: Ka6/a7, kc6/c7, Pa3 Pb4 / pb5 pb6, leak Ka6×b5 (value W) |

- No exact dud has a third pawn on a side (every exact dud has 2 + 2 pawns), so the 3 + 2 and 2 + 3 searches add no group.
- On flat 7×7 (7 ranks) there is **no** exact dud and the minimum is 1; the next total is 2 (28 placements). The counts are COMPUTED-1 (one solver pair, no second enumerator for 7 ranks).
- With promotions counted once (section 2) the total-1 and total-2 counts of some boards change (a promotion that does not lose then counts 1, not 4), the minimum does not.
