# Rings *3 with n+1 pawns (2026-10-27)

Whole-board pawn game on C_n (8 ranks, race rule "count", e.p. on, a pawn that can be taken e.p. is not passed, the
game ends at the first passed pawn). *3 = signature NNNP for G+*h, h = 0..3 (NNNPNN for h = 0..5).

## Summary

1. **C11: the least is 12 = n+1.**
   - No eleven-pawn ring is *3 (all 15,461,385; `../work/c10c11_npawn_totals.txt`; C1).
   - Two twelve-pawn rings are *3, `B4 B7 W4 W6B7 W3 B7 B6 W3 W2 B6 W2` and `B5 W2 W5 B7 W3 B7 B6 W3 W2 B6 W2B3`. rg,
     Codex's `independent.py` (both e.p. readings) and OpenCode's engine agree (`../npawn/cross_check_star3.out`; C2).
2. **C10: the least is 12 = n+2.** No ten- or eleven-pawn ring is *3 (all 142,191,474 eleven-pawn rings in 4+7 and 5+6,
   counts equal to `../validate/` and `../extend/count_c10p11.txt`, 0 unresolved; C1). Three eleven-pawn rings are *2
   (`../work/c10p11_hits.txt`). Twelve-pawn rings *3 exist (the n+2 family, paper Section VIII).
3. **Two families with n+1 pawns, one pawn per file except one file with two:**
   - T_n = (B4 W2)^((n-10)/2) B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2, every even n = 12..58 (`res_fam3_even.tsv`);
   - S_n = B4 B6 W3 (W2 B4)^((n-11)/2) W6B7 W3 B7 B6 W3 W2 B6 W2, every odd n = 13..59 (`res_fam3_odd.tsv`).

   Both are *3 by rg at every n (C1). Both non-Claude solvers agree at n = 12, 14 (T) and 13, 15, 17, 19 (S)
   (`../npawn/cross_check_T3.out`, `cross_check_S3.out`; C2). The n = 10 and 11 members are not *3 (LLNL, NNNR).
4. **Proof-ready structure** (`research/ring_n_plus_2_proof/pump_verify.py`; logs in `research/star3_proof/logs/`):
   - T: 1305 nodes for every n = 12..40, no e.p. flag; the Lemma-3 insertion is an isomorphism from 20 -> 22 on.
   - S: 40445 nodes from n = 19 on, no flag; the insertion is an isomorphism from 25 -> 27 on.

   Proof note T69 (OpenCode), `research/star3_proof/`.
5. **Consequence.** A ring *3 with n+1 pawns exists on every C_n with 11 <= n <= 59 (C2 for n <= 15 and n = 17, 19), against n+2
   in the paper's earlier families. On C11, n+1 is the least.

## How the families were found

- `pump3.py` took the 68 distinct *3 rings with n+1 pawns on C11..C13 from `../extend/` (single-file and pair
  insertions into the C9 hits). For every cut c it repeated files c, c+1, with k = 1..4 extra copies, giving 1,586 legal
  candidates (`cand_pump3.tsv`).
- The k = 1 stage (`res_pump3_k1.tsv`, 388 rings) gave 114 *3 rings: 2 on C13, 10 on C14 and 102 on C15. The first
  stage (`res_pump3.tsv`, 40 rings) had shown base B10 (`bases.txt`) staying *3 for k = 1..4 at two cuts.
- These two generators, run to n ≈ 60, became S and T.
- Solver: the unmodified rg (`../extend/rg`, MAXN = 64) through `../extend/solve.py`.
