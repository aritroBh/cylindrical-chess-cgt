# T81L referee report (2026-11-23)

Scope: the 9 edits in `kings/delegate/out/T81L/EDITS.md` to `kings/theory/LOOPY.md`. Read-only except this folder.
Line numbers below are those of the current LOOPY.md (before the edits).

## Overall

The substance of all nine edits is right. Five need a fix in wording or scope (1, 5, 6, 8, 9). The edits also
leave stale or now-false text in seven places (the status table, P11, §7), so I added edits 6b and 10-15.
The full replacement set is `verify/EDITS.md`. Apply check on a copy outside the repo: 16 applied, 0 rejected,
and the `awk -F'|'` cell counts are identical row by row (the original set also gives 9 applied, 0 rejected, with
the same counts).

## Engine facts re-checked (COMPUTED-1, my own script, cylcgt + lemmas/common.py)

- `pawns.value`: tests the whole position at the root; `_child` tests the moved component for a race, then
  `value` tests it for one passer and only then splits. This is test-first for the moved component, as EDIT 3
  says. At a root with passers of both colours it splits, and they cancel: flat 8×8 `W a2 / B h7` gives 0.
- Flat 8×8 `W b2 d6 / B c7`: S = 𝓛, W = 𝓛. Black's options c6, c5 and c7×d6 are all +BIG. c7×d6 is a race:
  count distances W b2 = 5, B d6 = 5, so the tie goes to the non-mover, White. Split-first gives 0 there, so the
  game is 𝓝. Confirmed.
- `moves`: a pawn on its last rank has no moves. `passed`: it is passed. It is never e.p.-capturable, because the
  capturer would have to stand on its own first rank. Flat 4 ranks `W a2 / B b3`: a2–a4 is a race, scored +BIG
  (distances W 0, B 1), and the value is ±+W. Flat 5 ranks `W a2 b2 / B b4`: after a2–a4 nobody is passed, a4–a5
  is +BIG, and the value is {+W | ±+W}, 𝓛 = o(W). Confirmed.
- Sweep re-run (`scripts/sweep.py`, 3.1 s): the same 1,306 roots, 488 of them with a last-rank pawn, and 0
  disagreements. Caveat: roots that raise RaceError are skipped without being counted, so this is not an
  independent engine.

## H ≥ 5 claim (re-derived by hand: PROVED is right)

- A promoting move can be a capture onto rank H, a step from H−1, an e.p. capture or a double step.
  - A capture onto rank H needs an enemy pawn on its own first rank: impossible.
  - An e.p. capture lands on rank H−2: not a promotion.
  - A double step lands on rank 4 < H.
  - So the only promoting move is a step from H−1.
- The mover's pawn on H−1 passes the textbook test, because nothing can stand ahead of it.
- It fails the e.p. clause only if it is the pawn that just double-stepped, with the right belonging to the
  opponent. That is the excluded "stale right" case. Example: on 5 ranks the mover double-stepped to rank 4,
  and the opponent then played in another summand. In `cylcgt` this is reachable in sums: `W a2 b2 f2 / B b4 f4`
  on flat 6×5 has the White option a4–a5 after a Black f-move. The clause in EDIT 1 that the right was made by the
  opponent is exactly what rules it out.
- The argument is the same on a cylinder.
- H = 4 counterexample `W a2 / B b3`: the root is passer-free, and a2–a4 promotes. Confirmed.

The examples of EDIT 6 are re-checked by hand. Kb6 Pc7 / Ka8 Pa5:
- With Black to move: a7 and b7 are covered by Kb6, and b8 by c7. The only move is a5–a4, and then c8=Q is mate:
  the queen covers b8 and b7, the king covers a7, and the queen on c8 cannot be taken. So (V1)–(V3) hold and P = D
  = White wins.
- With White to move: c8=Q is a non-suicidal Z-move, so (V3) fails. The empty sum with Z deleted is a loss for
  the mover, while P is a White win.

## Per edit

1. **ACCEPT WITH FIX.** The content is true and matches `cylcgt`.
   - Fix: the bullet is moved after **Board**, because it used H and the models before the board was defined.
   - Fix: the proof now says that captures onto rank H are impossible; before, it only implied it.
   - "No result of §1 needs a bound on H" is right. The tempo bound Σ(H − rank) of Definition 1.10 still holds
     with a last-rank pawn (0) and with a double step onto it.
2. **ACCEPT.**
3. **ACCEPT.** It matches `value` and `_child`, and the example is verified. The headline sentence of §1.5 still
   reads split-first, but the new sub-bullet settles the order. Optional: reword the headline.
4. **ACCEPT.** It is needed, because (HSS) is vacuous at a root with passers.
   - Knock-on 1: T1.14(ii) cites 1.11(c), so it now needs a passer-free root (EDIT 8).
   - Knock-on 2: P11's o(S) clause runs over roots with passers, where `hereditarily_safe` is vacuously True and
     S can be 0. Fixed by EDITS 13 and 14.
5. **ACCEPT WITH FIX.** The any-order reading is right and is what `common.threats` and `reachable` compute.
   But "Here and throughout" would redefine "reachable" in places that mean chess play:
   - (V1)–(V3) at line 554, and edit 6's "with s moving first";
   - Prop 1.15 at line 722.
   The scope is narrowed to "In this definition and in Theorem 1.11".
6. **ACCEPT WITH FIX.**
   - "D, the empty sum, is lost for White" is replaced by "the normal-play result of the empty sum (Z deleted)":
     with (V3) failing, D's treatment of Z is not fixed by Definition 1.5.
   - New **6b**: the "Assume:" before (V1) is replaced by a sentence that reads (V1)–(V3) per starter. Otherwise
     the hypothesis list still reads as global and clashes with "for each side s such that …".
7. **ACCEPT.**
8. **ACCEPT WITH FIX.**
   - Fix: the passer-free root is added, needed since EDIT 4.
   - Fix: "before the first decisive event" is added. Without it the reach included positions after a passer.
   - Fix: the reach is now that of the pawn part of X with Z deleted.
   - Fix: the D-result pair is now that of G₁ ⊞ … ⊞ G_k (Z deleted), not "D(X)". With (V3) holding for one
     starter only, D(X)'s treatment of Z is undefined.
9. **ACCEPT WITH FIX.** The whole proof bullet is replaced. The old first sentence, "By (i), the D-result pair
   of X is …", used (i) for both starters. The new proof gets the pair from 1.11(c) and only the s-entry from (i).

## Item b: every place that uses the edited items

| Line | Place | After the edits |
|---|---|---|
| 64 | status T1.11(c): "every use goes through T1.14, whose (V1a) contains (E)" | now FALSE (that is the point of edit 9). **EDIT 10** |
| 67 | status T1.14(i) PROVED | correct (proof already per starter) |
| 68 | status T1.14(ii) | stale. **EDIT 11** |
| 70 | status, sharp form | correct: it is stated per P-position with its side to move |
| 115 | status P11: the o(S) clause via 1.11(c)/1.14(ii) | wrong at roots with passers of both colours. **EDIT 13**. Its (E) is that of L1.6 (any-order reach), and (V1)–(V3) hold for both sides in the layout, so the per-starter form is fine |
| 156–166 | §0 summary (V1)–(V4) | informal; still a fair summary; no edit |
| 198 | summary table T1.14 | made per starter. **EDIT 12** (precision) |
| 280–282, 293, 299, 303 | Definition 1.5 D, the HSS note, the bridge diagram | correct |
| 441, 473, 495 | 1.11(c) (HSS) reach, the induction, "the re-splitting D(X) used in 1.14(i)" | correct; the reach is any-order, consistent with EDIT 5 |
| 588–591 | proof of 1.14(ii) | **EDIT 9** |
| 628–697 | sharp form and its reading | correct (per (y, side)); it does not cite (i)/(ii) |
| 702, 707 | "(V1)–(V4) are sufficient" | slightly loose now: (ii) also needs (E) on the any-order reach and a passer-free root. Not false for (i). Left as is (optional) |
| 715 | (V1a) table row, K17 `Ka2 kb4 … b -` | correct: Black to move, hypotheses checked for that starter; the twin "P = D for both sides" has its hypotheses at all chess-reachable positions |
| 1064, 1090 | the Remark after T2.7 | correct |
| 1118 | Corollary 2.7′ | does not cite 1.14; correct |
| 1577 | "Chain D → P" checks (no passer at the root, both sides to move) | empirical; consistent |
| 1697–1715 | chess bridge after P3.2 | uses the sharp form, with π keeping the side; correct |
| 2147–2167 | Theorem 3.2‴ | (a) per s through the sharp form, (b) all regular positions; correct |
| 2568 | §5.3 "with either side to move" | a P8 result, not a 1.14 citation; correct |
| 2916 | §6 P11: "also = o(S(X)) when hereditarily sum-safe" | **EDIT 14** (passer-free root) |
| 2917 | P12 | cites T2.7/C2.7′ only; correct |
| 2972, 2983, 2994 | §6/§7 mentions of 1.14 | correct |
| 2999–3000 | §7 item 4 "Theorem 1.14(V1a) assumes it" | incomplete. **EDIT 15** |

No later statement cites Theorem 1.14 "with either side to move" without both starters' hypotheses.

## Item c: labels

- PROVED is right for the H ≥ 5 statement and for the Kb6 example (both re-derived above).
- COMPUTED-1 is right for every `cylcgt` output: the 8×8 race, the 4- and 5-rank examples, and the sweep.
- The sweep is reproduced, but by the same engine, so COMPUTED-1 stays.
