# Least number of pawns in a ring *2 on C9, C10, C11 (and families to n = 60)

Whole-board pawn game on the n-file cylinder C_n:
- 8 ranks; race rule "count"; e.p. on;
- a pawn that can still be taken e.p. is not passed;
- the game ends at the first passed pawn.

A *root ring* has a pawn on every file and no passed pawn. Rings are counted up to rotation and reflection, with colours
not exchanged. Signature = outcome of G+*h for h = 0..3; NNPN = *2, NNNP = *3.

## Summary

1. **C9: the least is 10 = n+1 [C2].**
   - None of the 948,860 nine-pawn rings is *2 or *3.
   - Exactly 7 of the 44,960,428 ten-pawn rings are *2, all with five pawns a side. They form 4 classes under colour
     reversal. No ten-pawn ring is *3.
2. **C10: the least is 10 = n [C2]**, the fewest a ring can have.
   - Of the 4,304,243 ten-pawn rings in splits 4+6 and 5+5, exactly one is *2 (C1):
     M_10 = `B4 W2 B6 W2 W3 B6 B7 W3 B7 W5`. 6+4 is the colour mirror of 4+6.
3. **C11: the least is 11 = n [C2].** O_11 = `B4 B7 W5 B7 W3 B7 B6 W3 W2 B6 W2` is *2.
   - Of the 15,461,385 eleven-pawn rings in splits 4+7 and 5+6, it is the only *2 (C1), and none is *3. 7+4 and 6+5
     are the colour mirrors, so O_11 and its reversal are the only *2 eleven-pawn rings on C11.
4. **Families with n pawns [C1].** Both are *2 at every n tested:
   - M_n = (B4 W2)^((n-8)/2) B6 W2 W3 B6 B7 W3 B7 W5, every even n = 10..60;
   - O_n = B4 (B7 W5)^((n-9)/2) B7 W3 B7 B6 W3 W2 B6 W2, every odd n = 11..59. O_9 is RRRR.

   Their reduced games have the structure of the proved wall families: 441 and 2132 nodes, no e.p. flag, and the
   Lemma-3 insertion is an isomorphism from n = 18 and 19 on. Proof note T65, `research/ring_n_proof/`; referee T66.
   Also *2 (C1, n+1 pawns): N1_n = (B4 W2)^((n-7)/2) B6 W2 W3 B6 B7 W3 W6B7 for every odd n = 9..59.
5. **Consequence.** The least number of pawns in a ring *2 is n+3 for n = 3..7, ten for n = 7..10 and n for
   n = 10..60 (C1 for n > 11).

## C9, 9 pawns (exhaustive)

- **Enumeration.** `enum_rings.c` and the Python `p9/pyenum.py` give the same orbit sets in every split:
  3+6 28,160; 4+5 446,270; 5+4 446,270; 6+3 28,160; total 948,860.
  - OpenCode's `codex/enum.py`, written from the rules, gives the same counts.
  - `p9/pyenum.py` matches brute force for n = 3..6 and `enum_rings` for n = 4..8.
- **Solving.**
  - `rg`, `rg_copy` and the Python ring set all give identical signature histograms with 0 unresolved
    (`p9/solve/`, `p9/aggregate.txt`).
  - OpenCode's engine (`codex/engine.py`, written without reading rg or cylcgt) solved 3+6 and 4+5. Its histogram
    equals rg's in every class, e.g. 4+5: NNNN 324,047, RRRR 107,647, PNNN 573, NPNN 474; 0 NNPN, 0 NNNP. Its 5+4 and
    6+3 runs resumed after the 20:43 reboot (`codex/resume_after_reboot.log`).
  - cylcgt on 24 sampled rings and Codex's `independent.py` on 20 also agree.

## C9, 10 pawns

- **Scan.** 824 jobs, all splits; audit in the `check:enum` result, `validate/`:
  3+7 598,950; 4+6 10,793,489; 5+5 22,175,550; 6+4 10,793,489; 7+3 598,950.
  - These equal an independent transfer-matrix and Burnside counter (`validate/ring_counter.py`).
  - Every job finished with 0 unresolved.
- **Hits.** 7 NNPN, all in 5+5:
  - H1 `B4 B7 W3 B5 W2B7 W2 W3 B7 W2`
  - H2 `B4 B7 W3 W2B5 B7 W3 W2 B7 W2`
  - H3 `B4 W2 B6 W2 W3 B6 B7 W3 W6B7`
  - H4 `B6 B7 W3 B7 W5B4 W2 B6 W2 W3`

  H1, H2 and H3 each stand for a hit and its colour reversal; H4 is its own reversal (`verify_hits/classes.tsv`).
  All are legal root rings (`verify_hits/legality.tsv`).
- **Checks of the hits.**
  - rg in three builds (`verify_hits/step3.out`).
  - Codex's `independent.py` on all 14 rings and reversals, under both e.p.-across-heap readings, plus 3 near-miss
    controls (PNNN, NPNN, PNNN) (`verify_hits/logs/independent_*.log`).
  - OpenCode's engine on all 14 (`codex/hits.log`).
  - cylcgt as a whole-board game: H3, H4 *2. As a sum of components: H1 (reversed), H3, H4 *2. H1 and H2 whole and
    H2 sum are queued in `verify_hits/queueC_after_reboot.txt`.
- **Extensions.** They are in `extend/`; see the `check:extend` result:
  - single-file and pair insertions give *2 rings with n+1 pawns on C10..C13 (and *3 on C11..C13);
  - pumping gives *2 up to C33.

## C10 and C11, n pawns

- **C10.** 110 jobs, 4,304,243 rings, 0 unresolved, 1 NNPN (M_10, its own reversal), 0 NNNP.
- **C11.** 290 jobs, 4+7 1,482,250 and 5+6 13,979,135 rings, 0 unresolved, 1 NNPN (O_11), 0 NNNP. 7+4 and 6+5 are
  mirrors. The one RRNR ring, `B4 B7 W4 B7 W3 B7 B6 W3 W2 B6 W2`, is O_11 with W5 moved to W4.
- **Counts.** Per split, the ring counts equal `validate/ring_counter.py` (transfer matrix and Burnside; written
  without reading the enumerator): `validate/c10_p10_orbits.txt`, `validate/c11_p11_orbits.txt`. With one pawn per
  file each pawn needs an enemy pawn on an adjacent file, so there are no 3+7 or 3+8 rings.
- **Files.** The merged histograms and hits are in `work/c10c11_npawn_totals.txt`. The raw chunk outputs, including the
  signature files, are in `work/c10p10_results.tar.zst`, `work/c11p11_results.tar.zst` and `work/c9p10_results.tar.zst`
  (local only; `*.zst` is not committed).
- **Second programs.** Codex's `independent.py` (both readings) and OpenCode's engine give NNPNN for M_10, M_12,
  M_14, O_11, O_13 and N1_11, N1_13, and RRRRR for O_9 (`npawn/cross_check*.out`).
- **Families.** `extend/family_F_9_60.out` (N1 and its even variant), `extend/npawn_even.out` (M) and
  `npawn/O_family.out` (O) hold the rg runs; `research/ring_n_proof/logs/pump_*.txt` hold the reduced-graph structure.

## Provenance

- The workflow `c9-n-plus-1-verify` (four Claude agents) ran 19:13-20:43. Three agents finished: enumeration VALID,
  9-pawn exhaustive, extensions. The fourth, the hit checks, was cut by the machine reboot at 20:43, and its
  remaining cylcgt jobs were requeued by hand.
- The C10/C11 n-pawn scans, the families and the cross-checks were run by the orchestrating session on 2026-10-27
  between 20:50 and 21:15.
