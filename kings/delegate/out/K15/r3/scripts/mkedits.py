#!/usr/bin/env python3
"""K15 r3: write K15/EDITS.md.  Every OLD block is taken from the CURRENT kings/theory/LOOPY.md and must occur exactly once (checked here)."""
import os, sys
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); K15 = os.path.dirname(R3)
LOOPY = '/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md'
T = open(LOOPY).read()
edits = []
def edit(label, old, new):
    n = T.count(old)
    if n != 1:
        print('OLD occurs %d times: %s' % (n, label)); sys.exit(1)
    edits.append((label, old, new))

TAG = '(revised after K15, 2026-10-27)'
NEWTAG = '(new, K15, 2026-10-27)'

# ---- 1. Conjecture 4.7 ----
old = T[T.index('- **CONJECTURE 4.7:** no over-type group'):T.index('---\n\n## 5. Applications')].rstrip('\n')
new = '''- **CONJECTURE 4.7 (restated after K15, 2026-10-27; `kings/delegate/out/K15/FINDINGS.md`, `summary.json`; AI work, no human re-derivation):** over is realisable on the cylinder with wider groups. No over-type group is known.
  - *Search, COMPUTED-1 (new, K15, 2026-10-27).* K15's classifier (`K15/grp.c`, own move generator) solves the exact local game of model P (real kings, empty context) for every placement of both kings and of at most w White and b Black pawns on the files a..F, ranks 2 to H − 1, no officers, with root passers excluded or allowed, with free passes (the reading in which over can be output) and in plain P. Ranges, on cyl:8×6 and cyl:7×6: F = 3 with w, b ≤ 4 + 4; F = 4 with ≤ 3 + 3; F = 5 with ≤ 3 + 2. On cyl:8×8: F = 3 with ≤ 3 + 2, F = 4 with ≤ 2 + 2. On cyl:7×7 and cyl:8×7: F = 3 with ≤ 3 + 2. On flat 7×6: F = 3 with ≤ 3 + 3. That is 80 runs, up to 105 million roots each: **0 over and 0 under roots**. This covers the old first half (no over with ≤ 2 + 2 pawns on 3 files of the 8×6 cylinder) and goes well beyond it. Ranges that need over 3 GB of table (cyl:8×8 with F = 3 and ≤ 3 + 3, F = 4 and ≤ 3 + 2, and others) were not run.
  - *The classifier, CHECKED-2 (new, K15).* An independent Python classifier gives the same label at 772,188 roots (cyl:5×5, 5×6, 6×5, 3 files, ≤ 2 + 2, with passes) and at 634,628 roots in plain P; its local game values equal `kp_p`'s on 18,000 random positions (flat 7×6, cyl:7×6, cyl:8×6). It labels Z_B (§5.7) dud in plain P. The one-ply tests of the original brief label Z_B "other", because none of its 26 losing deviations is an immediate event.
  - *A blind spot of the structural test.* In plain P the freezing move of an over group wins at once, so only the free-pass reading can output over. A second search needs no structure: the 16 outcomes of a root beside the contexts (a, b, c) ∈ {0, 1}³ (a private White tempo move, a private Black one, a shared one) are compared with those of zero, on, off, dud, over and under. It finds no over signature on 3 files with ≤ 3 + 3 pawns (cyl:8×6, 7×6) and 20 roots per board on 4 files with ≤ 2 + 2 pawns (10 groups per board, up to symmetry); `kp_p` beside up to 40 pawn contexts and then beside every assignment of one context file refutes all of them (COMPUTED-1).
  - *Near-over groups, COMPUTED-1.* The classifier also lists roots where Black has a shuttle in the free-pass reading and every White safe move freezes, but the closure test fails (12 groups on each of cyl:7×6 and cyl:8×6, 4 on cyl:8×8, 1 each on cyl:7×7 and cyl:8×7). Beside contexts every one differs from r(G ⊞ over_D) except one placement on cyl:7×6 whose window leaves no context file. The longest survivor is `Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4`: it agrees with over_D at all 130 positions of the exhaustive single-file contexts with at most 3 pawns on file g of cyl:8×6, and fails at 3 of 130 on file f (cyl:8×6 and cyl:7×6; one of the three also solved by the independent solver `ref3`, CHECKED-2). It has no Black king shuttle in P (all six Black moves lose). A context test on the farthest file alone would have supported it.
  - *Second half, CONJECTURE, no support:* nothing was found in those ranges. "None exists" is not claimed: the boundary is at most 8 pawns, 5 files and the empty-context local game.
  - *To settle:* more files and pawns, kings off the group files, officers; chess (kpsolve was not run for any over candidate).
  - The scratch search of Appendix A could not have found either class (its classifier could not output dud or over, K15), so it was no evidence for the old first half. (Revised after K15, 2026-10-27; before, the first half rested on that search.)'''
edit('C4.7 restated', old, new)

# ---- 2. status row ----
old = '| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched) | R1 item 10, R4 item 8 |'
new = '| C4.7 | Over exists with wider groups: CONJECTURE, no support. No over or under group in K15\'s ranges (cyl:8×6 and 7×6: 3 files ≤ 4 + 4, 4 files ≤ 3 + 3, 5 files ≤ 3 + 2; cyl:8×8, 7×7, 8×7 in smaller ranges; flat 7×6): COMPUTED-1, the classifier CHECKED-2; a tempo-signature search and the near-over groups are refuted beside contexts (revised after K15, 2026-10-27) | R1 item 10, R4 item 8; K15 |'
edit('status row C4.7', old, new)

# ---- 3. section 8 item 2 ----
i0 = T.index('2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder?')
i1 = T.index('3. King-against-king fights inside Z')
old = T[i0:i1].rstrip('\n')
new = '''2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist? **Answered in part by K15
   (2026-10-27; `kings/delegate/out/K15/FINDINGS.md`, `summary.json`; AI work, no human re-derivation; revised after K15, 2026-10-27).**
   - *Dud, yes.* G8a `Kb2 kc4 Pa3 Pe2 pa4 pe3` and G8b `Kb3 kc5 Pa4 Pe3 pa5 pe4` on cyl:8×6 (pawns on files a and e, kings between; two blocked
     pairs, no pawn move at all, no root passer): the four king states of each have value (D, D) at all 16 roots, 16 of the 72 legal moves
     draw (the shuttles) and the other 56 lose for the mover, also against a defender who may pass. P model, CHECKED-2 (`kp_p`, `ref3m` and K15's
     exact classifier agree). Chess: kpsolve at cap 2 is exact at all 16 roots and gives the same 72 move values, so G8a and G8b are exactly
     two-shuttle in chess, COMPUTED-1 (one solver family; `ownchess` is flat-board only). Beside contexts, P: 1,296 positions (every assignment of
     one context file, both sides) and 640 random-context positions equal r(G ⊞ dud_D), 0 differ (COMPUTED-1; a 50-position sample re-solved with
     `ref3`, CHECKED-2); chess at cap 1: five of six contexts agree exactly, the sixth (two racing passers) is undecided for one side to move.
   - *More dud groups, COMPUTED-1.* On the cylinders the Z_B placement `Kb2 ka4 Pa3 Pb4 pb3 pc4` is exactly two-shuttle in P at its 8 roots on
     cyl:7×6 and cyl:8×6 too (38 legal moves, 8 draw, 30 lose; CHECKED-2). K15's census finds 43 distinct dud groups on cyl:7×6, 40 on cyl:8×6, 25 on
     cyl:8×8 and 9 on flat 7×6 (≤ 3 + 3 to ≤ 4 + 4 pawns, 3 to 5 files; dud in the empty context in plain P; up to file translation, mirror and colour flip).
     Beside contexts the 18 groups that are dud also against free passes all equal dud_D; of the 41 that are dud only in plain P, 7 do not (for example
     `Ka2 kc4 Pa4 Pc2 pa5 pc3` on cyl:8×6, no root passer). "Dud in the empty context" is therefore necessary, not sufficient; that the free-pass reading is
     sufficient is a CONJECTURE.
   - *Chess is not P.* D2 `Ka1 ka4 Pb4 Pc3 pb3 pc4` and D2m `Ka1 ka6 Pa3 Pb4 pa4 pb3` (cyl:7×6) are (D, D) in chess at cap 1, but 52 of the 108 deviations that
     lose in P draw in chess (COMPUTED-1), so they are not two-shuttle in chess. Z_B stays as in §5.7 (exactly two-shuttle in P, PROVED by hand on flat 7×6;
     chess open: bounds (W, L) at cap 1 on cyl:7×6 too; cyl:8×6 not run).
   - *Over, none found.* See Conjecture 4.7: no over or under group in K15's ranges, and every candidate (a tempo-signature search, the near-over groups) is refuted
     beside contexts but one placement without a context file. Open: more files and pawns, kings off the group files, officers, chess, hand proofs, cyl:8×8 beside contexts.
     (Earlier text of this item, after K14 and K27: Z_B on flat 7×6 is exactly two-shuttle in P, PROVED by hand, CHECKED-2 for the computations; unchanged.)'''
edit('section 8 item 2', old, new)

# ---- 4. Appendix A ----
i0 = T.index('  - no dud and no over group. (This scratch search covered the cylinders only.')
i1 = T.index('- **Local promotion game.**')
old = T[i0:i1].rstrip('\n')
new = '''  - no dud and no over group. **Withdrawn (revised after K15, 2026-10-27):** the classifier of this scratch search could not output dud
    (a side counted as having a shuttle only if the opponent was frozen, so both sides never had one at once; its over test skipped pawn moves),
    so the statement was no evidence. K15's exact census finds dud groups on both cylinders and no over group (§5.7, §8 item 2, Conjecture 4.7).
    (Also: this scratch search covered the cylinders only. K14 repeated the dud search on the 7×6
    cylinder and the flat 7×6 and 7×7 boards with kpsolve as the filter, with a move-count cut-off (18), which excluded
    Z_B (§5.7); its negative result is withdrawn. A search of flat 7×6 without the cut-off found Z_B.)'''
edit('Appendix A group search', old, new)

# ---- 5. consistency: section 3 text ----
old = 'open: chess\n  (cap 2), the cylinder, other boards (§8, item 2). Z_A (§5.7) has one White break.'
new = 'open: chess\n  (cap 2), other boards (§8, item 2). On the cylinders K15 (2026-10-27) found P-model dud groups, among them Z_B\'s placement and G8a, G8b with no pawn break, and G8a, G8b are exactly two-shuttle in chess at cap 2 (COMPUTED-1; §8 item 2) (revised after K15, 2026-10-27). Z_A (§5.7) has one White break.'
edit('section 3 text', old, new)

# ---- 6. 5.7 cylinder bullet ----
old = '  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact, and 225\n    of the 885 contexts are untested. It is open on the cylinder and on other boards.'
new = '''  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact, and 225
    of the 885 contexts are untested. It is open on other boards.
  - **The cylinders (new, K15, 2026-10-27; `kings/delegate/out/K15/FINDINGS.md`).** On cyl:7×6 and cyl:8×6 the placement `Kb2 ka4 Pa3 Pb4 pb3 pc4` has value (D, D) at its
    8 roots in P, with 38 legal moves of which 8 draw (the shuttles) and 30 lose, the wrap-around king moves (Ka4–g5, Ka4–g3 on 7×6) included: `kp_p` and
    `ref3m` give the same values and move lists at every root (CHECKED-2). It is not hand-proved on the cylinder (K27's proof is for the flat board). The brief of K15
    filtered roots with a passer by `cylcgt.passed`; all four pawns of Z_B are passed pawns for it (blockaded by the kings), so that filter rejects Z_B. K15's classifier
    labels Z_B dud in plain P and "mixed" against free passes (two pawn pushes then draw), and its one-ply tests (immediate promotion or passed pawn) label it "other",
    because none of the 26 losing deviations is an immediate event (they lose in 3 to 11 plies). Chess: bounds (W, L) at cap 1 on cyl:7×6, as on the flat board (cyl:8×6 not run).'''
edit('5.7 cylinder bullet', old, new)

# ---- 7. status row P3.2' ----
old = 'Open: chess (those five deviations, cap 2), the cylinder, other boards.'
new = 'Open: chess (those five deviations, cap 2), other boards. On the cylinders see §5.7 and §8 item 2 (K15): P-model dud groups exist (Z_B\'s placement, G8a, G8b), and G8a, G8b are exactly two-shuttle in chess at cap 2 (COMPUTED-1) (revised after K15, 2026-10-27).'
edit('status row P3.2prime', old, new)

# ---- 8. section 7 line ----
old = 'and the cylinder and other boards are open.)'
new = 'and other boards are open. On the cylinders K15 (2026-10-27) found P-model dud groups without a pawn break, and one pair (G8a, G8b) that is exactly two-shuttle in chess at cap 2, COMPUTED-1; §8 item 2.)'
edit('section 7 dud bullet', old, new)

out = ['# K15 proposed edits of kings/theory/LOOPY.md (replaces the earlier EDITS.md)', '',
       'Each OLD block occurs exactly once in the current `kings/theory/LOOPY.md` (checked by `K15/r3/scripts/mkedits.py` when this file was written). '
       'Changed claims carry their label and a "(revised after K15, 2026-10-27)" or "(new, K15, 2026-10-27)" tag. Z_B is left as LOOPY has it.', '']
for label, old, new in edits:
    out += ['### EDIT ' + label, '<<<<<<< OLD', old, '=======', new, '>>>>>>> NEW', '']
open(os.path.join(K15, 'EDITS.md'), 'w').write('\n'.join(out))
print(len(edits), 'edits written')
