#!/usr/bin/env python3
"""K26: build EDITS.md for kings/theory/LOOPY.md.  Every OLD text is checked to occur exactly once in the CURRENT LOOPY.md; numbers come from the logs.
Usage: build_edits.py [--check-only]"""
import json, glob, os, sys, ast, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
LOOPY = '/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md'
s = open(LOOPY).read()

# ---- numbers from the logs
fc = json.load(open(os.path.join(LOG, 'final_ctx.json')))      # the earlier attempt's table
_fresh = os.path.join(LOG, 'f', 'final_ctx_fresh.json')
if os.path.exists(_fresh):
    _f = json.load(open(_fresh))
    _need = {'ZB|cyl:8x6|efg': 12, 'ZB|cyl:7x6|ef': 4, 'ZB|flat:7x6|efg': 12, 'ZC|cyl:8x6|efg': 12}
    if all(k in _f['exhaustive'] and _f['exhaustive'][k]['shards'] == v for k, v in _need.items()):
        fc = _f       # this attempt's fresh exhaustive runs are complete: use them
print('exhaustive context numbers from', 'fresh run' if fc is not None and 'f/' in str(_fresh) and fc.get('exhaustive') is not None and os.path.exists(_fresh) and fc is _f else 'earlier attempt')
ex = fc['exhaustive']
def exv(key):
    e = ex[key]
    return e['contexts'], e['bad'], e['shards']
zb_c8, zb_c8_bad, _ = exv('ZB|cyl:8x6|efg')
zb_c7, zb_c7_bad, _ = exv('ZB|cyl:7x6|ef')
zb_f, zb_f_bad, zb_f_sh = exv('ZB|flat:7x6|efg')
zc_c8, zc_c8_bad, _ = exv('ZC|cyl:8x6|efg')
o3 = {}
for f in sorted(glob.glob(os.path.join(LOG, 'over3_*.json'))):
    d = json.load(open(f))
    o3[os.path.basename(f)] = d
nf4 = [d for k, d in o3.items() if '_nf4_' in k]
nf4_done = len(nf4)
nf4_cand = sum(d['candidates'] for d in nf4)
nf4_groups = sum(len(d['groups']) for d in nf4)
nf4_A = sum(d['stageA_survivors'] for d in nf4)
nf4_B = sum(d['stageB_survivors'] for d in nf4)
o32 = json.load(open(os.path.join(LOG, 'over3_cyl_8x6_32.json')))
o23 = json.load(open(os.path.join(LOG, 'over3_cyl_8x6_23.json')))
assert len(o32['groups']) == 0 and len(o23['groups']) == 0
nf4_complete = (nf4_done == 3)
flat_complete = (zb_f_sh == 12)
flat_txt = ('flat 7×6, files e–g: %s contexts' % format(zb_f, ',')) if flat_complete else ('flat 7×6, files e–g: %s contexts so far of 2,049 (the run was not finished)' % format(zb_f, ','))

fm = lambda x: format(x, ',')
E = []
def edit(label, old, new):
    assert s.count(old) == 1, ('OLD occurs %d times for %s' % (s.count(old), label))
    E.append((label, old, new))

# 1. §5.7: the last bullet of the Z_B block
edit('5.7 Z_B on other boards, Z_C, contexts (new, K26)',
"""  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact, and 225
    of the 885 contexts are untested. It is open on the cylinder and on other boards.""",
"""  - **Other boards and the cylinder (new, K26, 2026-10-27). The searches COMPUTED-1, the 8 roots and their move lists CHECKED-2 (kpp and ref3m).**
    Z_B has total leak count 0 (every non-shuttle move loses at once in P, at all 8 roots) on cyl:7×6, cyl:8×6 and flat 8×6,
    and on every six-rank board that was tried: flat width 5, 7, 8, 9, 10, 12 and cylinder width 5 to 12 (width 9 and more: ref3m only,
    COMPUTED-1). It fails on 5, 7 and 8 ranks (8 to 13 leaks; flat 7×7, 7×5 and 8×8, cyl 8×5, 6×7 to 9×7, 8×8). On cyl:7×6 it has two more
    legal Black moves, Ka4–g3 and Ka4–g5 (the wrap), and the mirror has Ka3–g2 and Ka3–g4. They lose at once as well. K27's 26 certificates
    do not cover them, so Z_B is **not PROVED** exact on the cylinder.
    The search of K26 (`kings/delegate/out/K26/`; F_Z = {a, b, c}, no cut-off; at most 2 + 2 pawns, then 3 + 2 and 2 + 3; 817,270 placements for 2 + 2
    and 1,886,421 for 3 + 2 and 2 + 3) finds exactly Z_B and its mirror on flat 7×6, flat 8×6 and cyl:7×6. For 2 + 2 this is CHECKED-2: a second
    enumerator and a second solver (ref3m) agree on 2.4 to 2.8 million root move lists per board, 0 differences. On flat 7×7 no placement has
    leak count 0 (the minimum is 1; COMPUTED-1).
  - **A second exact group, Z_C (new, K26, 2026-10-27).** On cyl:8×6 the search also finds White king c2/c3 (shuttle), Black king a4/a5 (shuttle), pawns
    Pa2 Pc4 / pa3 pc5, and its colour mirror. All four pawns are blocked, so no pawn can move, and it has no textbook passer. Every king move off the
    shuttles loses at once at all 8 roots (CHECKED-2). It is exact alone only on cyl:8×6 and cyl:9×6: it has 8 leaks on cyl:6×6, 7×6, 10×6, 11×6 and 12×6, 12 on cyl:5×6
    and 16 on every flat board of six ranks and on flat 7×7. In chess with cap 1 the bounds of Z_C alone are (W, L) at all 8 roots (kpsolve, COMPUTED-1), so chess is open for it. It is **not** a two-shuttle component beside contexts: with at most 3 context pawns on files e–g of cyl:8×6, %s of %s contexts give
    a P-result different from r(G ⊞ dud_D). One of the smallest is Pe2 pe3, where P is (W, W) at all 8 roots, because Kc2–d3 wins there (it loses alone). So (Pun) fails for Z_C
    beside a pawn that its king can reach (COMPUTED-1).
  - **Contexts beside Z_B (new, K26, 2026-10-27). COMPUTED-1** (kpp; the sampled runs were partly re-solved with ref3, 0 mismatches). Every placement of at most 3
    context pawns of either colour on ranks 2 to H−1: cyl:8×6, files e–g: %s contexts, 0 differ from r(G ⊞ dud_D); cyl:7×6, files e–f: %s contexts, 0 differ;
    %s: 0 differ. (Each context at 8 roots.)
  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact. It holds in every context tried (the K14 and K27
    families and the exhaustive families above; revised after K26, 2026-10-27). Open: a hand proof on the cylinder, chess, other contexts.""" % (fm(zc_c8_bad), fm(zc_c8), fm(zb_c8), fm(zb_c7), flat_txt))

# 2. §5.3 scratch bullet
edit('5.3 scratch evidence withdrawn',
"""- *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. This is the earlier scratch search on the cylinders only, with
    one-ply tests, not re-run; it says nothing about flat boards, where Z_B exists (§5.7). "dud may not occur in small
    K+P groups" remains a CONJECTURE for chess and for the cylinder.""",
"""- *Scratch evidence (withdrawn; revised after K26, 2026-10-27):* the earlier scratch statement "no both-sides-shuttle group without a pawn
    break exists among 3-file groups with ≤ 2 + 2 pawns and no passer on the 8×6 cylinder" is **false**. K26 searched exhaustively, with no cut-off
    (§5.7): on cyl:8×6 the group Z_C (Pa2 Pc4 / pa3 pc5, kings c2/c3 and a4/a5) has no textbook passer, no pawn that can move, and every non-shuttle
    move loses at once at all 8 roots in P (CHECKED-2). Z_B of §5.7 also works on cyl:7×6 and cyl:8×6. "dud may not occur in small K+P groups" is
    therefore refuted in P on the cylinder and remains open in chess.""")

# 3. section 3 bullet tail
edit('3 loopy kings bullet tail',
"""(cap 2), the cylinder, other boards (§8, item 2). Z_A (§5.7) has one White break.""",
"""(cap 2). On the cylinder Z_B and a passer-free group Z_C are exact at the 8 roots in P (CHECKED-2, §5.7; new, K26, 2026-10-27), and Z_C
  is not exact beside every context. Z_A (§5.7) has one White break.""")

# 4. status row 89 tail
edit('status table P3.2′ row tail',
"""Open: chess (those five deviations, cap 2), the cylinder, other boards. Z_A (§5.7) is a second group, with one White break (Kxb4).""",
"""Open: chess (those five deviations, cap 2). On the cylinder, Z_B and a passer-free group Z_C are exact at the 8 roots in P, and Z_B equals dud_D in every context tried (K26; §5.7; COMPUTED-1; revised after K26, 2026-10-27). Z_A (§5.7) is a second group, with one White break (Kxb4).""")

# 5. Downgraded bullet
edit('7 downgraded dud bullet tail',
"""and the cylinder and other boards are open.)""",
"""and see §5.7 for the cylinder and other boards: in P Z_B and Z_C work on cyl:8×6 (K26; revised after K26, 2026-10-27).)""")

# 6. §8 item 2
edit('8 item 2 question',
"""2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist? Both
   need wider searches. (After K14""",
"""2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist?
   **Answered in part by K26 (P model; revised after K26, 2026-10-27).** Dud groups: yes. Z_B (§5.7) and a new passer-free group Z_C (Pa2 Pc4 / pa3 pc5, kings
   c2/c3 and a4/a5, every pawn blocked) have every non-shuttle move losing at once at all 8 roots on the cylinder: Z_B on cyl:7×6 and cyl:8×6 (and on every
   six-rank board tried), Z_C on cyl:8×6 and cyl:9×6. CHECKED-2 for the roots and move lists (kpp and ref3m); the exhaustive search of F_Z = {a, b, c} with at most
   2 + 2 pawns is CHECKED-2 on flat 7×6, flat 8×6, cyl:7×6 and cyl:8×6 (second enumerator, second solver), and COMPUTED-1 for 3 + 2, 2 + 3 and flat 7×7 (no exact
   dud there; minimum leak count 1). No hand proof on the cylinder. Z_B equals dud_D in all %s + %s + %s contexts of at most 3 pawns tried; Z_C does not (%s of %s).
   Over groups: no exact over or under (Definition 4.8) was found in any searched range (Conjecture 4.7). Wider searches: not done (more than 4 files, more than 3 + 2 pawns, F_Z elsewhere on a flat board).
   (After K14""" % (fm(zb_c8), fm(zb_c7), fm(zb_f) if flat_complete else ('%s (unfinished)' % fm(zb_f)), fm(zc_c8_bad), fm(zc_c8)))
edit('8 item 2 tail',
"""CHECKED-2; five are not settled at cap 1, among them Kc3–d2 with bounds (D, L); cap 2 not run), the cylinder, other boards.)""",
"""CHECKED-2; five are not settled at cap 1, among them Kc3–d2 with bounds (D, L); cap 2 not run). Chess on the cylinder and on the other boards is open as well.)""")

# 7. Conjecture 4.7 and the new definition and lemma
nf4txt = ('The search with four files (a–d) and at most 2 + 2 pawns (%s placements; %s pass the king filter and (U1)–(U3) at one root, %s at all four roots) found no exact group' % (format(nf4_cand, ','), format(nf4_A, ','), format(nf4_B, ','))) if (nf4_complete and nf4_groups == 0) else 'four files: not finished'
edit('4.7 conjecture, definition 4.8, lemma 4.9',
"""- **CONJECTURE 4.7:** no over-type group with ≤ 2 + 2 pawns fits on 3 files of the 8×6 cylinder, but over
  is realisable on the cylinder with wider groups. *Scratch evidence:* the first half; a geometric search over
  placements of ≤ 2 + 2 pawns on 3 (or 4) files found none (Appendix A). *To settle:* a wider search, then
  kpsolve. (Revised after review: R1 item 10, R4 item 8: the search described in Appendix A covered ≤ 2 + 2
  pawns, not the ≤ 3 + 2 claimed here; the conjecture is restated for what was actually searched.)""",
"""**Definition 4.8 (exact under and over groups in P; new, K26, 2026-10-27).** Let White's king shuttle on an adjacent pair z (K1 holds) and Black's king stand on one
square b0 with K1 and K2 against both z squares. Call it an *exact under group* if, in P:
- (U1) at both White-to-move roots every non-shuttle White move loses at once (the position after it is a Black win), and the shuttle is legal;
- (U2) at both Black-to-move roots Black has a move that does not lose at once (a *freeze*);
- (U3) after each freeze, a position q, White to move has a legal move and every legal White move loses at once;
- (U4) the same q with Black to move: Black has a legal move and every legal Black move loses at once. So q is a mutual zugzwang, the position 0_D of Definition 4.4.
The colour mirror (ranks flipped, colours swapped) is an *exact over group*. Dropping (U4) gives a *loose* under group: after the freeze only White is in zugzwang.

**Lemma 4.9 (no king freeze). PROVED** (new, K26, 2026-10-27). In an exact under group no freeze is a king move that captures nothing.
*Proof.* Let m be such a freeze, b0 → b1, and q the position after it. In q Black can play b1 → b0: b0 is empty, no White pawn attacks it (K1), and it is not
next to the White king, which has not moved (K2). The result is the root with White to move. By (U2) and (U3) the other Black-to-move root has a freeze to a position of
value L (a White loss), so that root has value L. By (U1) every non-shuttle White move at the first root loses at once, and the shuttle leads to the second root, value L.
So the first root has value L, the move b1 → b0 does not lose at once, and (U4) fails. ∎ So a freeze of an exact group is a pawn move or a king capture of a group pawn.

- **CONJECTURE 4.7 (revised after K26, 2026-10-27; tested in P, COMPUTED-1):** no exact over group (Definition 4.8) with ≤ 2 + 2 pawns fits on 3 files of the 8×6
  cylinder, but over is realisable on the cylinder with wider groups.
  - *First half: supported.* K26 searched with no cut-off: F_Z = {a, b, c}, every placement of the kings and of at most 2 + 2, then 3 + 2 and 2 + 3 pawns
    (`kings/delegate/out/K26/scripts/over2.py` and `over3.py`). It found **no** exact under or over group on cyl:8×6 (631,179 placements for 2 + 2; 1,602,414 for 3 + 2; 1,517,293 for 2 + 3).
    It found none for 2 + 2 on cyl:7×6, flat 7×6 and flat 8×6 either.
  - Placements with (U1), (U2) and value L after every freeze, at all four roots: 144,159 on cyl:8×6 for 2 + 2 (without the king filter).
    Of these, 141,293 fail (U4) and 2,866 have a promotion as the freeze. A promotion is a decisive event, not a group move.
  - *Second half: no support, not refuted.* %s.
    So "realisable with wider groups" is neither supported nor refuted.
  - *Loose* groups are plentiful. With exactly one freeze at every root there are 120 on cyl:8×6 (2 + 2, 3 files), 142 on flat 7×6, 118 on cyl:7×6 and 626 on cyl:8×6 with four files.
    Beside contexts Proposition 4.6 holds in 762 of the 768 premise roots tested. So they are not over_D. The six failures were not diagnosed.
  - The earlier scratch search is replaced by this one (Appendix A). *To settle:* wider groups (more files, more pawns), then kpsolve.""" % nf4txt)

# 8. Appendix A bullet
edit('Appendix A group search bullet',
"""  - no dud and no over group. (This scratch search covered the cylinders only. K14 repeated the dud search on the 7×6""",
"""  - no dud and no over group. (**False for dud groups on the cylinder**: K26 (2026-10-27) found Z_B and Z_C on cyl:8×6 and Z_B on cyl:7×6 (§5.7); the statement "no over group" is
    replaced by Conjecture 4.7 as revised after K26, which refers to exact over groups. This scratch search covered the cylinders only. K14 repeated the dud search on the 7×6""")

# 9. status row C4.7
edit('status table C4.7 row',
"""| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched) | R1 item 10, R4 item 8 |""",
"""| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched); exhaustive search in P by K26 (revised after K26, 2026-10-27): no exact over or under group (Definition 4.8) in ≤ 2 + 2, 3 + 2 and 2 + 3 pawns on 3 files of cyl:8×6 (and in ≤ 2 + 2 on cyl:7×6, flat 7×6 and 8×6), COMPUTED-1; Lemma 4.9 PROVED (no king freeze) | R1 item 10, R4 item 8; K26 |""")

if '--check-only' in sys.argv:
    print('all OLD texts occur exactly once;', len(E), 'edits')
    sys.exit(0)
with open(os.path.join(OUT, 'EDITS.md'), 'w') as f:
    f.write('# K26 proposed edits to kings/theory/LOOPY.md\n\n')
    f.write('Each OLD text occurs exactly once in LOOPY.md as it stood when this file was written (checked by `scripts/build_edits.py --check-only`).\n\n')
    for (label, old, new) in E:
        f.write('### EDIT %s\n<<<<<<< OLD\n%s\n=======\n%s\n>>>>>>> NEW\n\n' % (label, old, new))
print('EDITS.md written;', len(E), 'edits')
