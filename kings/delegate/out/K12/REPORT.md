# K12: end-to-end sweep over roots that already have a passer

## 5-line summary
- Enumerated 716,962 legal roots with a passer on cyl:6x6 (82,374), cyl:7x6 (562,676) and cyl:8x6 (71,912), both sides to move, e.p. rights included.
- Certified 687,262 of them by Proposition 2.11 (H1)-(H5); 0 certified root disagrees with `kpsolve --frozen` (no violation).
- The remaining 29,700 roots split into 9,324 uncertified-but-agreeing and 20,376 uncertified-and-disagreeing, so P11's root clause is needed there.
- A second implementation (brute-force BFS for μ_ω) agrees with the checker on all 716,962 roots; dropping (H4) or weakening (H5) produces 48 / 15,868 certified disagreements, so the checker can see failures.
- Recommended label for P11's root clause: CHECKED-2.

## 1. Exact position class and passed test

Layout: White king Ka1, Black king on the top rank of the a-file (KaH), b-file and last file empty, pawns only on files c through the file two before the last (indices 2..W-2), ranks 2..H-1. At most K pawns per side: (a) cyl:6x6 K=3; (b) cyl:7x6 K=3; (c) cyl:8x6 K=2. Both sides to move are separate roots. Only legal positions (side not to move not in check) are kept. Every legal e.p. right is a separate instance.

Passed test: cylcgt's e.p.-aware `passed` (`PASSED_RESPECTS_EP = True`), self-tested against an independent per-pawn reimplementation on all 716,962 roots (0 mismatches).

## 2. Root splitting

- Single (exactly one side has a passer): credited side is that side.
- Race (both sides have a passer): credited side b by Corollary 2.11a's extension: b = side to move N if dp(N) <= dp(M), else M.

## 3. Tables

| Board | Roots | Single | Race | Certified | Uncert agree | Uncert disagree |
|---|---|---|---|---|---|---|
| cyl:6x6 | 82,374 | 28,996 | 53,378 | 79,698 | 718 | 1,958 |
| cyl:7x6 | 562,676 | 144,940 | 417,736 | 539,748 | 6,716 | 16,212 |
| cyl:8x6 | 71,912 | 14,350 | 57,562 | 67,816 | 1,890 | 2,206 |
| Total | 716,962 | 188,286 | 528,676 | 687,262 | 9,324 | 20,376 |

More detailed (certified / uncertified × agree / disagree):

cyl:6x6 single: cert agree 26,444; cert disagree 0; uncert agree 694; uncert disagree 1,858.
cyl:6x6 race: cert agree 53,254; cert disagree 0; uncert agree 24; uncert disagree 100.

cyl:7x6 single: cert agree 124,288; cert disagree 0; uncert agree 6,280; uncert disagree 14,372.
cyl:7x6 race: cert agree 415,460; cert disagree 0; uncert agree 436; uncert disagree 1,840.

cyl:8x6 single: cert agree 10,982; cert disagree 0; uncert agree 1,550; uncert disagree 1,818.
cyl:8x6 race: cert agree 56,834; cert disagree 0; uncert agree 340; uncert disagree 388.

## 4. Violations

None. Zero certified roots disagree with `--frozen`.

## 5. Examples (uncertified and disagreeing)

Up to 20 (all single-side cases unless noted):

1. `Pc2 pe5 pd3 Ka1 ka6 w -` (6x6, stm W, beta B) -> frozen W
2. `Pc3 pe5 pd3 Ka1 ka6 w d4` (6x6, race, stm W, beta W) -> frozen L
3. `Pc3 pe4 pd4 Ka1 ka6 w -` (6x6) -> frozen W
4. `Pc3 pe5 pd4 Ka1 ka6 w -` (6x6) -> frozen W
5. `Pc4 pc3 pd5 Ka1 ka6 w -` (6x6) -> frozen W
6. `Pc4 pd3 pd5 Ka1 ka6 w -` (6x6) -> frozen W
7. `Pc4 pd4 pd5 Ka1 ka6 w -` (6x6) -> frozen W
8. `Pc4 pd5 pe3 Ka1 ka6 w -` (6x6) -> frozen W
9. `Pc4 pe4 pd5 Ka1 ka6 w -` (6x6) -> frozen W
10. `Pc4 pe5 pd5 Ka1 ka6 w -` (6x6) -> frozen W
11. `Pd4 pc3 pc5 Ka1 ka6 w -` (6x6) -> frozen W
12. `Pd4 pc3 pe5 Ka1 ka6 w -` (6x6) -> frozen W
13. `Pd4 pc4 pc5 Ka1 ka6 w -` (6x6) -> frozen W
14. `Pd4 pe5 pc4 Ka1 ka6 w -` (6x6) -> frozen W
15. `Pd4 pc5 pd3 Ka1 ka6 w -` (6x6) -> frozen W
16. `Pd4 pc5 pe3 Ka1 ka6 w -` (6x6) -> frozen W
17. `Pd4 pe4 pc5 Ka1 ka6 w -` (6x6) -> frozen W
18. `Pd4 pe5 pd3 Ka1 ka6 w -` (6x6) -> frozen W
19. `Pd4 pe5 pe3 Ka1 ka6 w -` (6x6) -> frozen W
20. `Pd4 pe4 pe5 Ka1 ka6 w -` (6x6) -> frozen W

Race example: `Pe3 pc5 pd3 Ka1 ka6 w d4` -> frozen L, beta W.

## 6. Controls

- (H4) dropped: 687,766 certified, 48 certified roots disagree with `--frozen` (showing (H4) is needed).
- (H5) weakened to μ_ω >= e: 711,714 certified, 15,868 disagreements (showing the +1 bound matters).
- Second implementation (brute-force BFS for μ_ω instead of memoized DFS) agrees on all 716,962 roots (0 mismatches).

## 7. Reproduce

```
cd /Users/aritro/Downloads/Research/Chessendgames
PYTHONPATH=. .venv/bin/python kings/delegate/out/K12/gen.py
PYTHONPATH=. .venv/bin/python kings/delegate/out/K12/process.py
# then kpsolve per board:
kings/delegate/heavy.sh kings/delegate/out/K12/kp --board cyl:6x6 --frozen --cap 1 --threads 2 < kings/delegate/out/K12/in_6x6.txt > kings/delegate/out/K12/out_6x6.txt
kings/delegate/heavy.sh kings/delegate/out/K12/kp --board cyl:7x6 --frozen --cap 1 --threads 2 < kings/delegate/out/K12/in_7x6.txt > kings/delegate/out/K12/out_7x6.txt
kings/delegate/heavy.sh kings/delegate/out/K12/kp --board cyl:8x6 --frozen --cap 1 --threads 2 < kings/delegate/out/K12/in_8x6.txt > kings/delegate/out/K12/out_8x6.txt
PYTHONPATH=. .venv/bin/python kings/delegate/out/K12/controls.py
PYTHONPATH=. .venv/bin/python kings/delegate/out/K12/fullbrute.py
```

## 8. Recommended label

CHECKED-2 (counts reproduced by an independent brute-force implementation of μ_ω on all 716,962 roots).
