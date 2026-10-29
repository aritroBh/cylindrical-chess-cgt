# T70 Referee Report: `PROOF_S3T3.md`

## Five-line verdict summary

1. **GAP** — The finite proof establishes the NNNPNN outcome signature against nim heaps, not equality to the standard partizan CGT game `*3`.
2. **PROVED** — The T/S wall phases, insertion cuts, local windows, and the chosen induction starts satisfy the cited insertion hypotheses after narrowing one overbroad S-wall sentence.
3. **COMPUTED-1** — Independent reduced graphs reproduce T20 (1,305 nodes) and S23 (40,445 nodes), with the stated zones, no flags, no passers, and signature NNNPNN.
4. **COMPUTED-1** — Both T insertion steps and both S insertion steps preserve every checked K/T option; all lower base sizes give NNNPNN under both en-passant heap readings.
5. **GAP** — Rename the claim as nim-heap outcome equivalence, or prove standard game equality; also correct the S pawn-count arithmetic and clarify the S zone wording.

## Overall verdict

**GAP for the theorem as a standard CGT claim.** The finite computations and insertion argument support the stated nim-heap outcome test. But §3 defines “`G = *3`” to mean that `G + *h` has the same outcome as `*3 + *h` for each heap `h < 256`. This is a restricted outcome relation, not standard equality of partizan games. The proof does not show that these ring games are impartial or that testing only nim heaps determines their standard CGT value.

**PROVED — The restriction matters.** Distinct positive numbers 1 and 2 both have outcome L after addition of every nim heap `*h`, but `1 != 2` as CGT games. For `h=0`, each is L. For `h>0`, Left can move the heap to zero and leave a positive number with Right to move; every Right heap move leaves a smaller `1 + *k` or `2 + *k`, which is L by induction. Thus nim-heap outcome tests are not an injective test for general partizan games. The proof must either state the weaker nim-heap equivalence as its theorem or supply a standard-value argument.

**PROVED — SOUND WITH FIXES for the weaker claim.** Under the proof’s explicit restricted definition, the NNNPNN signature gives P only at `h=3`. For `6 <= h < 256`, either player can move the heap to `*3`, reaching the checked P-position, so the sum is N. The finite and insertion checks below support that restricted conclusion for the two families.

## H1 — Wall, phase, insertion, and induction starts

**PROVED — T family.** The wall is files `0..n-11`, with `B4` on even files and `W2` on odd files. Its length is `n-10`; its endpoints are `B4` at file 0 and `W2` at file `n-11`. With `c=4`, the required arc `c-4..c+5` is `0..9`, exactly the wall at `n0=20`. It does not fit at the preceding even size 18. Insertion after file 4 adds `W2,B4` on new files 5,6 and preserves the alternating phase. The tail has 10 files and 11 pawns because `W6B7` contains two pawns, so the family has `n+1` pawns.

**PROVED — S family.** The wall is files `3..n-9`, alternating `W2` on odd files and `B4` on even files. With `c=7`, the required arc is `3..12`. The changed zone contains the last two wall files, `n-10,n-9`; at `n=21` these are files 11,12 and overlap the arc. At `n0=23` they are 13,14, outside the arc, so the selected base size is the first odd size where this fixed cut avoids the changing zone. Insertion after file 7 adds `B4,W2` on new files 8,9 and preserves the phase.

**PROVED — S pawn-count correction.** The S tail occupies 8 files but has 9 pawns because `W6B7` has two. Its count is `3 + (n-11) + 9 = n+1`. The proof note’s `3 + (n-11) + 8 = n` counts tail files as pawns; the displayed family itself has the required `n+1` pawns.

**COMPUTED-1 — S zone wording.** At S23, the changed-file zone is `{0,1,2,13,14,16..22}`. Files 13 and 14 are wall files. Therefore the sentence in §2 saying that “the wall files are pattern files” is too broad for S. The needed statement is that the fixed arc `3..12` is pattern in every reduced node. It is disjoint from the zone at S23, and the insertion maps the zone to `{0,1,2,15,16,18..24}` at S25 while extending the fixed pattern run through file 14. This does not break the induction.

**COMPUTED-1 — Pump-start clarification.** The proof’s main text selects S `n0=23`, while its pump-log sentence mentions the first displayed insertion as `25->27`. My checker confirms both `23->25` and `25->27`; `n0=23` is valid.

## H2 — A wall pawn cannot capture or become a passer

**PROVED.** On each pattern triple, a `W2` pawn’s diagonal capture squares are rank 3 while adjacent `B4` pawns are on rank 4; a `B4` pawn’s capture squares are rank 3 while adjacent `W2` pawns are on rank 2. Thus the wall pawn only pushes. After a push, an opposing adjacent pawn remains ahead of it. A `W2` double-step to rank 4 is still protected by a live en-passant right when an adjacent `B4` can take it; under the adopted test that pawn is not passed. This is the local geometry required by Lemma 2(a).

## H3 — Lemma-2 windows at both ends of the insertion arc

**PROVED — T windows.** At T20, the arc is `0..9`; the first central pawn is `W2` on file 1 with window `0..4`, and the last is `B4` on file 8 with window `5..9`. At T22 the central range is files 1..10; its boundary windows are `0..4` and `7..11`. These windows are inside exact pattern files. At T24 the arc extends to `0..13`.

**PROVED — S windows.** At S23, the arc is `3..12`; the first central pawn is `B4` on file 4 with window `3..7`, and the last is `W2` on file 11 with window `8..12`. At S25 the mapped pattern interval extends to `3..14`; the corresponding boundary windows for files 4 and 13 are `3..7` and `10..14`. The variable S wall-end files 13,14 at the S23 base are outside the arc and outside both boundary windows.

**COMPUTED-1 — Lemma 2 move classification.** The independent checker enumerated 10,440 wall-pawn positions and 15,660 moves at T20; 13,050 positions and 19,575 moves at each of T22/T24; and 323,560 positions and 485,340 moves at S23. Every checked wall move was L or P, never T or K, and after each move the moving side had no passer. The two endpoint windows above were checked in every reduced node.

## H4/H5 — Flags, passers, and race preservation

**COMPUTED-1 — H4.** The T20 reduced graph and S23 reduced graph have no canonical live en-passant flags and no passed pawns in any node. The start is among those nodes. All single-pawn files in the required insertion arcs remain exactly at their starting contents.

**PROVED — H4 at the starts.** Neither start has an en-passant right because no pawn has just double-stepped. Every wall pawn is blocked from being passed by the opposite-colour pawn on a neighboring wall file. In T, the core is likewise blocked: `B5/W2`, the co-located `W6B7`, then adjacent `W3/B7`, `B6/W3`, `W2/B6`, and `W2`. In S, the leading `B4,B6,W3` are blocked by the seam `W2` at file `n-1`, `W3` at file 2, and wall `B4` at file 3; the trailing core after `W6B7` has the same adjacent-opponent pattern. Thus neither root has a passer.

**PROVED — H5.** The insertion shifts files but keeps every pawn’s rank and preserves the three-file pattern around the cut. It therefore preserves the passed-pawn set and each promotion distance used by the `count` race rule. The result is specific to the whole-board game and the stated race semantics; it does not establish a component-sum result.

## H6 — Reduced graphs and two insertion steps

**COMPUTED-1 — T base and pump.** T20 has 1,305 nodes, 4,018 K edges, 1,212 T edges, no flags, no passers, zone `{10,11,13..18}`, and signature NNNPNN for `h=0..5`. T22 and T24 have the same node/edge counts and signature; their zones shift to `{12,13,15..20}` and `{14,15,17..22}`. Full rebuilt graph comparisons establish exact insertion isomorphisms `20->22` and `22->24`.

**COMPUTED-1 — S base and pump.** S23 has 40,445 nodes, 141,252 K edges, 86,822 T edges, no flags, no passers, zone `{0,1,2,13,14,16..22}`, and signature NNNPNN for `h=0..5`. At S25 and S27 the mapped graphs retain those node/edge counts and signature; the zones are `{0,1,2,15,16,18..24}` and `{0,1,2,17,18,20..26}`.

**COMPUTED-1 —** For the S insertions, the checker mapped the complete graph, then independently recomputed the target K/T children at every mapped node for both sides: 80,890 node/side pairs on each step. It found exact correspondence for `23->25` and `25->27`; all target K children lie in the mapped node set. This checks closure as well as equality of the K and T options. The compressed graphs are 1.38 MB (S23), 1.36 MB (S25), and 1.42 MB (S27).

**PROVED — H6 induction after the finite checks.** The zones shift by the insertion map, and the fixed arcs remain outside them for every later size of the right parity. Once the base reduced graph has no flags or passers and the arc is pattern in each node, Lemma 3 applies node by node; the two computed steps agree with that correspondence. The proof’s all-wall-files wording for S should be replaced with the fixed-arc invariant described under H1.

## H7 and all sizes below `n0`

**COMPUTED-1 — Signature.** The reduced graphs and direct base searches give `NNNPNN` for `h=0..5`: N at 0,1,2; P at 3; N at 4,5. The heap move to 3 proves N for each `6 <= h < 256` in the note’s restricted test.

**COMPUTED-1 — Direct searches below the induction starts.** I searched the unreduced whole-board game for every lower size, under both EP-on-heap readings (`expire` and `keep`). Every result was NNNPNN:

| Family sizes | Result under both readings | Cached states per reading |
|---|---|---|
| T12, T14, T16, T18 | NNNPNN | 156,993; 268,627; 437,841; 763,845 |
| S13, S15, S17, S19, S21 | NNNPNN | 1,486,796; 3,411,211; 5,940,085; 9,931,674; 15,775,446 |

The T18 and S17/S19/S21 cases are needed below `n0`; the cited C2 command in the proof note lists only T12–T16 and S13–S15. This independent search supplies those missing finite cases as **COMPUTED-1**. Peak RSS was 2,853,421,056 bytes in the all-S run and 3,094,347,776 bytes in a standalone S21 run, both below 4 GB.

## Implementation and reproduction

**COMPUTED-1 — Implementation boundary.** [independent.py](independent.py) uses only Python’s standard library. It implements cylindrical pawn movement, canonical EP rights, EP-aware passers, count-race terminals, whole-board minimax, reduced-graph classification, and packed integer memo keys. It imports none of `cylcgt`, `rg`, or `myeng.py`. The EP-aware passed test is active; both heap-EP readings are computed in each direct base search. The assertion-based `self_check()` covers EP pass status/capture and the empty game.

From the project root, these commands reproduce the complete checks. Run S stages in order because each writes the compressed graph consumed by the next stage.

```sh
/usr/bin/nice -n 15 env PYTHONPATH=. .venv/bin/python -u research/star3_check/independent.py graphs-T
/usr/bin/nice -n 15 env PYTHONPATH=. .venv/bin/python -u research/star3_check/independent.py S-base
/usr/bin/nice -n 15 env PYTHONPATH=. .venv/bin/python -u research/star3_check/independent.py S-step1
/usr/bin/nice -n 15 env PYTHONPATH=. .venv/bin/python -u research/star3_check/independent.py S-step2
/usr/bin/nice -n 15 env PYTHONPATH=. .venv/bin/python -u research/star3_check/independent.py bases-T
/usr/bin/nice -n 15 env PYTHONPATH=. .venv/bin/python -u research/star3_check/independent.py bases-S
/usr/bin/nice -n 15 env PYTHONPATH=. .venv/bin/python -u research/star3_check/independent.py bases-S 21
```

**COMPUTED-1 — Execution conditions.** The sandbox rejected `nice -n 15` (`setpriority: Operation not permitted`); I ran one heavy process at a time and polled each recorded PID. The complete logs are `graphs_T_compact.log`, `S_base_compact.log`, `S_step1_compact.log`, `S_step2_compact.log`, `bases_T_compact.log`, and `bases_S_compact_all.log`. My interrupted exploratory runs are `graphs.log`, `S_base.log`, and `bases_S_21.log`; they are not used for the verdict.

## Fixes needed before stating the theorem as written

1. **GAP:** Replace the standard-value claim `T_n = S_n = *3` with the precise nim-heap outcome equivalence actually proved, or add a proof of standard partizan CGT equality in the intended game model.
2. **PROVED:** In §2, say that the fixed arc is pattern for S; not every S wall file is fixed, because the changed zone reaches files `n-10,n-9` inside the wall.
3. **PROVED:** Correct the S pawn-count line to count 9 pawns in its 8-file tail.
4. **COMPUTED-1:** Cite all direct lower cases below `n0`, including T18 and S17/S19/S21; the new independent run gives NNNPNN for each.
5. **COMPUTED-1:** Clarify that S n0=23 is valid and that both insertion checks `23->25` and `25->27` pass, even though the cited pump sentence begins at 25.

## Referee materials

I read `RESULTS.md`, `RESEARCH_PLAN.md` §3, `research/star3_proof/REPORT.md`, the full `PROOF_S3T3.md`, the prior `ring_n_plus_2_check/REPORT.md`, the odd report, and the Q checker files. The brief names `research/ring_n_plus_2_check/Q/REPORT.md`, but that path is absent; the available directory is lowercase `q/` and contains `independent.py` and its log.
