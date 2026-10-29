import re, json, glob
TAG = "revised after the K26 referee, 2026-10-27"
E = open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/EDITS.md').read()
blocks = re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW', E, re.S)
B = {lab: (old, new) for lab, old, new in blocks}
def tot(pat):
    t = {}
    n = 0
    for f in glob.glob(pat):
        d = json.load(open(f)); n += 1
        for k, v in d.items():
            if k != 'exact': t[k] = t.get(k, 0) + v
            else: t.setdefault('exact', []).extend(v)
    return n, t
n32, t32 = tot('logs/under_cyl8x6_32_f3_*of24.json')
n23, t23 = tot('logs/under_cyl8x6_23_f3_*of24.json')
full32 = n32 == 24 and t32.get('placements') == 1602414
full23 = n23 == 24 and t23.get('placements') == 1517293
print("3+2:", n32, t32.get('placements'), t32.get('U1_U2_U3'), len(t32.get('exact', [])), "| 2+3:", n23, t23.get('placements'), t23.get('U1_U2_U3'), len(t23.get('exact', [])))
def sub(new, a, b):
    assert new.count(a) == 1, (a[:70], new.count(a))
    return new.replace(a, b)
out = []
# ---------- EDIT 5.7
old, new = B['5.7 Z_B on other boards, Z_C, contexts (new, K26)']
new = sub(new, "The searches COMPUTED-1, the 8 roots and their move lists CHECKED-2 (kpp and ref3m).**",
 "The searches CHECKED-2 for at most 2 + 2 pawns and for 3 + 2 and 2 + 3 on flat 7×6, cyl:7×6 and cyl:8×6 (%s), the 8 roots and their move lists CHECKED-2 (kpp and ref3m).**" % TAG)
new = sub(new, "and on every six-rank board that was tried: flat width 5, 7, 8, 9, 10, 12 and cylinder width 5 to 12 (width 9 and more: ref3m only,\n    COMPUTED-1).",
 "and on every six-rank board that was tried: flat width 5, 7, 8, 9, 10 and cylinder width 5 to 10 (widths 9 and 10: ref3m only, COMPUTED-1; kpp stops at width 8).\n    Widths 11 and 12 (66 and 72 squares) were also run, but ref3m keeps its pawn sets in 64-bit masks, so they are not claimed (%s)." % TAG)
new = sub(new, "finds exactly Z_B and its mirror on flat 7×6, flat 8×6 and cyl:7×6. For 2 + 2 this is CHECKED-2: a second\n    enumerator and a second solver (ref3m) agree on 2.4 to 2.8 million root move lists per board, 0 differences.",
 "finds exactly Z_B and its mirror on flat 7×6, flat 8×6 (at most 2 + 2 pawns only) and cyl:7×6 (all three pawn limits; 3 + 2 and 2 + 3 were also searched on flat 7×6 and cyl:8×6). For 2 + 2 this is CHECKED-2: a second\n    enumerator and a second solver (ref3m) agree on 2.4 to 2.8 million root move lists per board, 0 differences. The K26 referee's own enumerator (`kings/delegate/out/K26/verify/scripts/ref_enum.py`, ref3m only) reproduces the counts of total leaks 0, 1, 2 on all four boards and for 3 + 2 and 2 + 3 on flat 7×6, cyl:7×6 and cyl:8×6 (%s)." % TAG)
new = sub(new, "On flat 7×7 no placement has\n    leak count 0 (the minimum is 1; COMPUTED-1).",
 "On flat 7×7 (at most 2 + 2 pawns only) no placement has\n    leak count 0 (the minimum is 1, with 12 placements; CHECKED-2: the referee's own enumerator gives the same counts; %s)." % TAG)
new = sub(new, "It is exact alone only on cyl:8×6 and cyl:9×6: it has 8 leaks on cyl:6×6, 7×6, 10×6, 11×6 and 12×6, 12 on cyl:5×6\n    and 16 on every flat board of six ranks and on flat 7×7.",
 "Among the boards tried it is exact alone only on cyl:8×6 and cyl:9×6: it has 8 leaks on cyl:6×6, 7×6 and 10×6, 12 on cyl:5×6\n    and 16 on every flat board of six ranks tried (width 5 to 10) and on flat 7×7 (its mirror has 6 there).")
new = sub(new, "131 of 2,049 contexts give\n    a P-result different from r(G ⊞ dud_D).",
 "131 of 2,049 contexts (35 of the 264 with two pawns, 96 of the 1,760 with three, none with fewer; 754 of 16,392 roots) give\n    a P-result different from r(G ⊞ dud_D) (CHECKED-2: K26's kpp and `dmodel.py`, and the referee's ref3m and its own predictor `verify/scripts/dud_ctx.py`, give the same counts; %s)." % TAG)
new = sub(new, "- **Contexts beside Z_B (new, K26, 2026-10-27). COMPUTED-1** (kpp; the sampled runs were partly re-solved with ref3, 0 mismatches).",
 "- **Contexts beside Z_B (new, K26, 2026-10-27). CHECKED-2** (K26: kpp against its own D-model predictor `dmodel.py`; the K26 referee: ref3m against its own implementation of Theorem 3.4(a) with the e.p. flag, `verify/scripts/dud_ctx.py`; same result; %s)." % TAG)
new = sub(new, "beside a pawn that its king can reach (COMPUTED-1).", "beside a pawn that its king can reach (CHECKED-2; %s)." % TAG)
new = sub(new, "flat 7×6, files e–g: 2,049 contexts: 0 differ. (Each context at 8 roots.)",
 "flat 7×6, files e–g: 2,049 contexts: 0 differ. (Each context at 8 roots.) Files d and h (next to F_Z) were not tried.")
out.append(("5.7 Z_B on other boards, Z_C, contexts (new, K26)", old, new))
# ---------- status table P3.2' row tail
old, new = B["status table P3.2′ row tail"]
new = sub(new, "and Z_B equals dud_D in every context tried (K26; §5.7; COMPUTED-1; revised after K26, 2026-10-27).",
 "and Z_B equals dud_D in every context tried (K26; §5.7; CHECKED-2 for the exhaustive contexts of at most 3 pawns beside Z_B, COMPUTED-1 for the earlier samples; revised after K26 and its referee, 2026-10-27).")
out.append(("status table P3.2′ row tail", old, new))
# ---------- EDIT 8 item 2 question
old, new = B['8 item 2 question']
new = sub(new, "and COMPUTED-1 for 3 + 2, 2 + 3 and flat 7×7 (no exact\n   dud there; minimum leak count 1).",
 "CHECKED-2 for 3 + 2 and 2 + 3 on flat 7×6, cyl:7×6 and cyl:8×6 (the same groups, no new one), and CHECKED-2 for 2 + 2 on flat 7×7 (no exact dud there; minimum leak count 1) (%s)." % TAG)
new = sub(new, "(second enumerator, second solver), ", "(second enumerator, second solver, and the referee's third), ")
new = sub(new, "Z_B equals dud_D in all 2,049 + 577 + 2,049 contexts of at most 3 pawns tried; Z_C does not (131 of 2,049).",
 "Z_B equals dud_D in all 2,049 + 577 + 2,049 contexts of at most 3 pawns tried (CHECKED-2); Z_C does not (131 of 2,049, CHECKED-2).")
out.append(("8 item 2 question", old, new))
# ---------- EDIT 4.7
old, new = B['4.7 conjecture, definition 4.8, lemma 4.9']
new = sub(new, "- (U2) at both Black-to-move roots Black has a move that does not lose at once (a *freeze*);\n- (U3) after each freeze, a position q, White to move has a legal move and every legal White move loses at once;\n- (U4) the same q with Black to move: Black has a legal move and every legal Black move loses at once. So q is a mutual zugzwang, the position 0_D of Definition 4.4.",
 "- (U2) at both Black-to-move roots Black has a move that does not lose at once (a *freeze*);\n- (U3) after each freeze, a position q (with the e.p. flag if the freeze is a double step), White to move has a legal move and every legal White move loses at once;\n- (U4) the same q with Black to move (no flag): q is a legal position, Black has a legal move and every legal Black move loses at once. So q is a mutual zugzwang, the position 0_D of Definition 4.4. If the freezing pawn gives check, q with Black to move is not legal and (U4) fails.\nA promotion by Black is a decisive event, not a freeze to 0: a group in which some freeze is a promotion is not exact (such placements are counted separately below). (Rules for promotion, e.p. and check added after the K26 referee, 2026-10-27; they are what both searches did.)")
new = sub(new, "  - Placements with (U1), (U2) and value L after every freeze, at all four roots: 144,159 on cyl:8×6 for 2 + 2 (without the king filter).\n    Of these, 141,293 fail (U4) and 2,866 have a promotion as the freeze. A promotion is a decisive event, not a group move.",
 "  - Placements with (U1), (U2) and value L after every freeze (a promotion counts as value L), at all four roots: 144,159 on cyl:8×6 for 2 + 2 (without the king filter), 144,411 on cyl:7×6, 140,389 on flat 7×6; the K26 referee's own enumerator with ref3m counts the same numbers (%s).\n    None is an exact group: each fails (U4) at some freeze or has a promotion as a freeze. The split between these two depends on the order in which the freezes are tried (K26: 141,293 and 2,866; referee: 143,831 and 328 on cyl:8×6); the sum does not. In 5,791 of the (U4) failures on cyl:8×6 the freezing pawn gives check." % TAG)
new = sub(new, "    Beside contexts Proposition 4.6 holds in 762 of the 768 premise roots tested. So they are not over_D. The six failures were not diagnosed.",
 "    Beside contexts Proposition 4.6 holds in 537 of the 552 premise roots of K26's final sample (762 of 768 in an earlier sample); the failures were not diagnosed. Loose groups are not over_D anyway: after the freeze Black still has a move that does not lose.")
if full32 and full23 and not t32['exact'] and not t23['exact']:
    under32 = ("The 3 + 2 and 2 + 3 runs on cyl:8×6 (1,602,414 and 1,517,293 placements) were repeated by the referee without the king filter: no exact group, and the counts of placements with (U1), (U2) and value L after every freeze are %s and %s (%s). The four-file run was not repeated." % (format(t32['U1_U2_U3'], ','), format(t23['U1_U2_U3'], ','), TAG))
else:
    under32 = ("The 3 + 2 and 2 + 3 runs on cyl:8×6 were repeated by the referee only in part (%d of 24 and %d of 24 shards by pawn configuration; no exact group in the shards run; %s). The four-file run was not repeated." % (n32, n23, TAG))
new = sub(new, "    It found none for 2 + 2 on cyl:7×6, flat 7×6 and flat 8×6 either.",
 "    It found none for 2 + 2 on cyl:7×6, flat 7×6 and flat 8×6 either. The K26 referee's own search (`verify/scripts/ref_under.py`, ref3m, no king filter, no use of Lemma 4.9) reproduces the 2 + 2 result on cyl:8×6, cyl:7×6 and flat 7×6 (CHECKED-2; flat 8×6 not repeated). " + under32)

new = sub(new, "value L (a White loss), so that root has value L.", "value L (a White loss; if that freeze is a promotion, the root is a Black win at once), so that root has value L.")
new = sub(new, "In q Black can play b1 → b0: b0 is empty, no White pawn attacks it (K1), and it is not\nnext to the White king, which has not moved (K2).", "In q (with Black to move, a legal position by K1 for the White king's square) Black can play b1 → b0: b0 is empty, no White pawn attacks it (K1, the pawns have not moved), and it is not\nnext to the White king, which has not moved (K2). No e.p. right exists (no pawn moved).")
new = sub(new, "(revised after K26, 2026-10-27; tested in P, COMPUTED-1)", "(revised after K26 and its referee, 2026-10-27; tested in P: CHECKED-2 for the searches on 3 files named below except flat 8×6, COMPUTED-1 for the four-file search)")
new = sub(new, "118 on cyl:7×6 and 626 on cyl:8×6 with four files.", "118 on cyl:7×6 (all three CHECKED-2 by the referee's count) and 626 on cyl:8×6 with four files (reused from K26, not repeated).")
out.append(("4.7 conjecture, definition 4.8, lemma 4.9", old, new))
old, new = B["status table C4.7 row"]
new = sub(new, "on 3 files of cyl:8×6 (and in ≤ 2 + 2 on cyl:7×6, flat 7×6 and 8×6), COMPUTED-1; Lemma 4.9 PROVED (no king freeze)",
          "on 3 files of cyl:8×6 (and in ≤ 2 + 2 on cyl:7×6, flat 7×6 and 8×6), CHECKED-2 for the 3-file searches except flat 8×6 (revised after the K26 referee, 2026-10-27), COMPUTED-1 for the four-file search; Lemma 4.9 PROVED (no king freeze)")
out.append(("status table C4.7 row", old, new))
with open('EDITS.md', 'w') as f:
    f.write("# K26 referee: replacement edits for kings/theory/LOOPY.md\n\nEach OLD occurs exactly once in the current LOOPY.md (checked by `scripts/chk_edits.py EDITS.md`). They replace the blocks of the same label in `../EDITS.md`; the other seven blocks of `../EDITS.md` stand as written (their OLD blocks also occur once, and their NEW texts are accurate).\nThe tag date `2026-10-27` follows the task text.\n\n")
    for lab, o, n in out:
        f.write("### EDIT %s\n<<<<<<< OLD\n%s\n=======\n%s\n>>>>>>> NEW\n\n" % (lab, o, n))
print("written", len(out))
