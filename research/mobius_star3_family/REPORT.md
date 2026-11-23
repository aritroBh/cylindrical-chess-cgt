# A *3 family on the Möbius strip with n + 1 pawns

Rules, ring notation and signatures follow `research/mobius_rings/REPORT.md` (h = 0..3; NNNP = *3; the reduced-graph
tool prints h = 0..4, NNNPN). Written by an Opus agent on 2026-11-23; saved by the main session from its hand-back.

## Headline
**Family found: yes.** A *3 ring with n + 1 pawns exists on M_n for n = 9, 11 and every n >= 12. For n = 10 only rings
with n + 2 pawns were found.
- **TT(m) = B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2 (B4 W2)^m**: n = 2m+10, m >= 1. It is the cylinder family T_n with the seam
  between the last wall W2 and B5.
- **SS(m) = B6 W3 (W2 B4)^m W6B7 W3 B7 B6 W3 W2 B6 W2 B4**: n = 2m+11, m >= 0. It is S_n with its leading B4 moved to
  the end.

Labels:
- CHECKED-2 (mob1_32, mob2_32) for TT n = 12..32 and SS n = 11..31.
- For all n: proof plan only. The criteria of `research/mobius_rings_proof/PROOF.md` section 4 hold literally; C1 is
  COMPUTED-1 (rgraph.py + fgame.py), and the bases below m0 are CHECKED-2.
- Additional n+1 families H2 (odd n = 9..31) and E2 (even n = 12..32) are CHECKED-2, but their reduced graphs carry
  e.p. flags.

## 1. Families
`confirm.py FAM lo hi` runs mob1_32 and mob2_32, one ring per process. Logs: `logs/confirm_TT_SS.log`,
`logs/confirm_H2_H4_G6.log`, `logs/confirm_E2.log`.

| family | ring | n | pawns | NNNP (mob1 = mob2) for |
|---|---|---|---|---|
| TT | `B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2 (B4 W2)^m` | 2m+10 | n+1 | m = 1..11 (m = 0 is LLLL) |
| SS | `B6 W3 (W2 B4)^m W6B7 W3 B7 B6 W3 W2 B6 W2 B4` | 2m+11 | n+1 | m = 0..10 |
| H2 | `B5 W3 (W2 B4)^m W4 B7 B7 W3 W2 W2B7 B7` | 2m+9 | n+1 | m = 0..11 |
| E2 | `B5 W3 (W2 B4)^m W2 W4 B7 B7 W3 W2 W2B7 B7` | 2m+10 | n+1 | m = 1..11 |
| H4 | `B5 W3 W4 B7 (W2 B4)^m B7 W3 W2 W2B7 B7` | 2m+9 | n+1 | m = 0..11 |
| G6 | `B7 W4 W23 B5 W3B7 W4B7 (W2 B4)^m` | 2m+6 | n+3 | m = 0..13 |

## 2. Proof plan (PROOF.md section 4 criteria)
`fverify.py` = rgraph.py of `research/mobius_rings_proof`, unchanged, running on fgame.py. fgame.py was checked equal
to mgame.Board on 5000 random positions (`fgame_test.py`, 0 mismatches).

**TT** (`logs/fverify_TT.log`, m = 1..8)
- For every m: 1305 nodes, 4018 K-edges, 1212 T-moves; flagged 0, passer nodes 0; zone {0,1,3..8}; NNNPN. These are
  the cylinder's C1T numbers.
- The insertion step holds at every block cut for steps 1->2 .. 7->8.
- Wall B4/W2 on files 10..n-1. Cut c = 14, arc 10..19 (a chart interval ending at the seam file), m0 = 5.
- ins_14 copies files 15 (W2) and 14 (B4), so it maps the start of m to the start of m+1 and leaves the zone fixed.

**SS** (`logs/fverify_SS.log`, m = 1..7)
- From m = 4: 22755 nodes, 72730 K-edges, 49694 T-moves; flagged 0, passers 0; zone {0,1} + {2m,2m+1} + {2m+3..n-1}.
- Wall W2/B4 on files 2..2m+1. Cut c = 6, arc 2..11, m0 = 6 (n = 23).
- The insertion step holds at c = 6 for 6->7; it fails only at the two cuts next to the zone.

**Needed for a proof:** Lemmas 1-3 used verbatim with the induction of PROOF.md section 4. C1 (the m0 line) is done by
one program. C2 is done: TT m = 1..4, SS m = 0..5. Missing: a second, independent program for C1, and the written note.

## 3. H2 and E2
- Graphs are constant from m = 2 (H2: 12825 nodes) and m = 1 (E2: 26328 nodes), and the insertion step holds.
- 307 (H2) and 617 (E2) nodes are flagged. The flags lie on tail files next to the seam (`logs/flagan_*.log`), far
  from the arc.
- In flagged nodes, wall pawns have T-moves: a wall move lets a flag protecting the mover's own pawn lapse.
- A proof would need a far-flag extension of Lemmas 2 and 3. It was random-tested on 1500 flagged positions with 0
  mismatches (`lemma_flag_test.py`, `logs/lemma_flag_test_1_1500.log`); it is not proved.

## 4. What was tried
- `stage1.py`: pumps on the 3 known *3 rings, 5060 rings. Blocks: wall pairs, all single files, all two-file blocks,
  every cut, m = 1, 2; survivors to m = 8. Results are in section 1, plus non-wall B5/W3 and B6/W4 pumps.
- `stage2.py 18`: all rotations of T_n (n = 10..18) and S_n (n = 11..17), 144 rings. TT and SS were *3 at every n
  tried. The *2 families F1, F2, F3 and the n = 10 ring plus one pawn: 1371 rings, no *3.
- `stage3.py single`: H2 plus one extra file, 330 rings. Found E2.
- `stage4.py 10 6000 40`: n = 10, targeted. 18k rings with 11 pawns: no *3. 14k rings with 12 pawns: 4 *3 rings,
  confirmed by both solvers (`logs/n10_hits_confirm.log`): `B5 W2 W2B4 W4 B7 B7 W3 W2 W2B7 B7`,
  `B5 W3 W2B3 W4 B7 B7 W3 W2 W2B7 B7`, `B5 W3 W4 W2B7 B4 B7 W3 W2 W2B7 B7`, `B5 W3B4 W2 W4 B7 B7 W3 W2 W2B7 B7`.
- Smallest n found: n + 1 pawns at n = 9 (the known ring); n + 2 pawns at n = 10.
- Earlier exhaustive scans found no *3 with n+1 or n+2 pawns for n <= 7. n = 8 with 9 or 10 pawns was never scanned.
  n = 10 with 11 pawns is open.

## 5. Not done
- An independent C1 program; a written proof.
- SS insertion steps beyond 6->7.
- Exhaustive scans of n = 8 (9 or 10 pawns) and n = 10 (11 pawns).
- Nimbers above *3; other race rules; the component-sum model; a proof of the flagged-node extension for H2/E2.
- Resources: one fverify run peaked at 5.8 GB before the caches were capped (later runs 2.45 GB); one process at a
  time, nice 15, about 1.5 h in total.

## Files
`lib.py`, `stage1.py`-`stage4.py`, `confirm.py`, `fverify.py`, `fverify_lib.py`, `fgame.py`, `fgame_test.py`,
`flagan.py`, `lemma_flag_test.py`, `rprobe.py`, `logs/`.
