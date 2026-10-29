## 4. Exact on and off groups (class c)

Search: White shuttles on z, Black's king on one square (K1, K2), at most n_W + n_B pawns, four roots; `on_strong` = exact on as defined in section 1(c); `on_weak` = only the Black half; the loose under/over column is the one used in section 3.
Black-shuttler versions (exact off) are the colour mirror: the exact off groups for (n_W, n_B) are the exact on groups for (n_B, n_W) with colours swapped.
Fresh runs (`logs/k26f_*_t1_*`):

@@T1@@

Exact on / loose under groups for 2 + 3 and 3 + 2 pawns: cyl:7×6 4 / 167 and 6 / 216 (fresh run, identical to the earlier attempt); cyl:8×6 6 / 175 and 4 / 198 and flat 7×6 28 / 334 and 34 / 228 (reused from `logs/merged.json`, not re-run).

- **Exact on groups exist on every board searched**: 4 on cyl:7×6 and cyl:8×6 for 2 + 2, up to 34 on flat 7×6 (3 + 2). The union over all pawn limits is 103 exact on groups on the five boards (`logs/exact_groups_all.json`, reused list, re-confirmed fresh by ref3m: section 6),
  of which 78 have no textbook passer. Together with the 10 exact duds that makes the 113 groups of the ref3m confirmation (2 of the 10 duds, Z_C and its mirror, are passer-free).
  The smallest example is `Ka5 Ka6 | kc6 | Pb4 | pb5` on flat 7×6 (White's king shuttles on a5/a6, Black's king on c6, one blocked pair on file b: every Black move loses at once).
- **Beside contexts** (section 6) the P-result equals the D-model prediction for on_D / off_D (Theorem 3.4(b), (c)) at every root on flat 7×6 (260 roots of the on group, 28 of its mirror) and, on the cylinders, at all roots but 9 roots in 3 of 258 sampled on-contexts (fresh sample: 8 roots in 2 contexts on cyl:7×6, 1 root in 1 context on cyl:8×6; the earlier attempt's sample had 12 roots in 5 contexts).
  Examples (`logs/ctx_phase2.json`, earlier sample): P = W where the D-model says L (White's extra king moves help, the direction of Proposition 3.2's inequality) and P = L where the D-model says W (a Black king move that loses alone does not lose beside that context, so (Pun) fails for the frozen king).
  The mismatching contexts have pawns on files f, g (cyl:8×6) or e, f (cyl:7×6), next to the wrap square. They were not diagnosed further.
