## 6. The selected groups: root values, move lists (ref3m too) and small pawn contexts

**Selection (20 groups, `logs/groups_final.json`, chosen by the earlier attempt's `final_select.py`; I audited the choice and kept it):** all 10 exact duds (Z_B and Z_C and their mirrors on the boards where they are exact), 5 exact on groups (passer-free, spread over cyl:7×6, cyl:8×6, flat 7×6),
and 5 *loose* under/over groups (labelled: no exact over group exists, section 3). The first 15 are exact groups. Each group is also tested in its colour-mirror orientation (the mirror of an on group is an off group, of a dud a dud, of a loose under group a loose over group).

**Roots and move lists.** For the 20 groups in both orientations, **240 roots**: `kpp --pmodel --moves` and `ref3m --moves` (fresh builds) agree at every root on the root value and on the complete multiset of (move, value), with promotions normalised: **240 of 240, CHECKED-2**
(`logs/f/confirm/confirm_final.json`; readable lists in `audit/movelists_20groups.txt`; the colour-flip symmetry of the values holds at all of them). The 113 exact groups of the whole search (10 duds and 103 on) were re-verified directly from the definition of the class with ref3m alone:
**113 groups, 492 roots, 0 failures** (`logs/f/confirm/confirm_all.json`); the negative control (Z_A, and Z_B on flat 7×7) fails 9 times as it must.

**Contexts.** A context is a set of White and Black pawns on files at distance 2 or more from F_Z (files f, g on flat 7×6 and cyl:8×6; e, f on cyl:7×6), at most 2 + 2 pawns on ranks 2..H−1, no e.p. right at the root. At every root (king state × side to move)
the P value (`kpp --pmodel`, ref3m for a part) is compared with the D-model prediction r(G ⊞ Z) of `dmodel.py` (an independent implementation of Definitions 3.1 and 4.4 and Theorem 3.4; cross-checked against K14's D solver: 885 contexts, 7,080 roots, 0 differences, `logs/dm_crosscheck.log`):
dud for dud groups (Theorem 3.4(a)), on or off for exact on/off groups (Theorem 3.4(b), (c)), the over/under reservoir for the loose groups (Proposition 4.6 and its mirror: if White wins G moving second then White wins G ⊞ over_D with either side to move).
The sample for the orientation as given is the empty context plus a random sample stratified by the number of context pawns (0 to 2, 3, 4; shares 35, 40, 25 per cent), half drawn uniformly and half among the contexts whose D-prediction is decisive (`--nbase 66`), so at least 60 contexts per group; the colour-flipped orientation gets about 7 (`--nflip 6`; 21 in the earlier runs).

@@CTX_SAMPLED@@

**Exhaustive small contexts (reused from the earlier attempt: its runs `logs/exh/`, kpp, complete; the fresh runs did not get a lock slot).** Every placement of at most 3 context pawns, either colour, on the context files, ranks 2..H−1, each at the 8 roots of the group (unbiased rates):

@@CTX_EXH@@

By number of context pawns (source column: the fresh run if all its shards exist, else the earlier attempt's run):

@@CTX_STATS@@

- **Z_B equals dud_D in every one of these contexts** (cyl:8×6 files e–g, cyl:7×6 files e–f, flat 7×6 files e–g): 0 contexts and 0 roots differ. This is COMPUTED-1 (kpp; the sampled runs were partly re-solved with ref3m, 0 mismatches).
- **Z_C does not**: no context of one pawn differs, but 35 of 264 two-pawn and 96 of 1,760 three-pawn contexts do (131 of 2,049; 754 of 16,392 roots). The differing contexts always have pawns of both colours in the context files (examples: Pe2 pe3, Pe2 pe5, Pe3 pe4, Pf2 pf3). The smallest example is Pe2 pe3 (see section 2).
- Exact on/off groups agree with Theorem 3.4(b)/(c) except in the few contexts discussed in section 4. The loose under/over groups agree with the over_D reading at almost every root; Proposition 4.6's conclusion fails at 15 of 552 premise roots in the fresh sample (6 of 768 in the earlier one), which is why they are not over_D (section 3).
