# Recheck of the star2_frontier discrepancy (job 2)

Source of the question: `research/star2_frontier/REPORT.md:69-71`. Two flat five-file positions are *2 in the C mask scan under the opponent race rule with the e.p.-aware passed test, but `cylcgt` gives a non-nimber.

Positions: P1 = `W: a3 b3 c2 e2 / B: a6 c5 d5 e3`, P2 = `W: a6 b4 c4 e3 / B: a7 c7 d6 e6`. Board: 5 files, 8 ranks, flat, e.p. on.

## Reproduction of both sides

- C side (`frontier_copy.c`, a copy of `frontier.c`, `--eval`): opponent/epon/aware gives `N,2` for P1 and for P2 (`logs/c_eval.tsv`).
- cylcgt (`verify_disagreement.py`, unchanged): P1 is `⇑`, P2 is `⇓`. Reproduced.

## Third route

`sumtest/sumsolver.py` (from-scratch brute-force solver, shares no code with cylcgt or the C scan), opponent race rule, e.p.-aware, outcome of G + each reference game (`logs/sumsolver_runs.txt`):
- `--mode whole` (first passed pawn on the board ends the game): for P1 and for P2 the outcome vector is exactly that of *2 (G+*2 is P, G+0, G+*, G+*3 are N, G+up is L, and so on).
- `--mode comp` (components re-split after every move, each component with a passer becomes the integer +-BIG, and the integers add): P1 gives L against every nimber and P2 gives R against every nimber. That is the signature of `⇑` and `⇓`.
- With the count rule both modes give the *2 vector for both positions.

`nosplit.py` (cylcgt with `pawns.components` replaced by "one component = whole board", `logs/nosplit.log`): under opponent/aware, P1 and P2 become `*2` (nim=2). With splitting on they are `⇑` and `⇓`. Under count/aware all three five-file positions, with or without splitting, are `*2`. Under mover/aware none is *2 in either model, as the C table says.

## Verdict

The C scan is right for the whole-board game. cylcgt is right for the sum model S, not for the whole-board game W. The two programs have different models, and neither has a bug here.

Why they differ: the sum model replaces a component with a passed pawn by +-BIG and keeps playing in the other components, so a +BIG can be cancelled by a -BIG. In the whole-board game the first passed pawn ends the game. Smallest witness found in a descendant of P1 (`find_witness.py`, `logs/find_witness.log`): `W: a3 e2 / B: b4 d3 e3`. White plays axb4 and has the only passed pawn, so White wins at once on the whole board. As a sum, the pawns split into {a3,b4} and {e2,d3,e3}, and Black answers d3xe2 for -BIG, which cancels. cylcgt calls the position `{* | -W*}`, a Black win, while the whole-board solver says first player wins. In total 106 of 2,107 e.p.-free descendants of each root have a different outcome in the two models. `cylcgt.pawns.sum_safe()` says True for both roots, but `lemmas.common.hereditarily_safe` says False for both. So the roots are not hereditarily sum-safe and the equality theorem does not apply.

Candidates I ruled out: a different race rule (same rule, set the same way in both), different e.p. handling (e.p. is aware in both; the component e.p. scope is the same), board width or embedding (same Board(5,8)), a bug in the C mask (the independent whole-board solver agrees with it).

## Do any claims depend on the wrong side?

No claim in the paper or RESULTS.md relies on the sum value of these two positions under the opponent rule. The paper already states the discrepancy for P1:
- `paper/ieee/sections/05_sums.tex:137-142`: "under the opponent rule with the e.p.-aware test, W a3 b3 c2 e2 / B a6 c5 d5 e3 ... is ⇑ as a sum but *2 on the whole board". This matches my result. It does not mention P2, which behaves the same (`⇓` as a sum).
- `paper/ieee/sections/08_star2.tex:119-125`: the three five-file positions are *2 "in both models" in the default setting (count, e.p.-aware). Confirmed: cylcgt gives *2 for all three with and without splitting.
- `paper/ieee/sections/08_star2.tex:121`: "as sums, 15 keep the value" was not rechecked here.

One wording risk, not a wrong number: `RESULTS.md:26` says "Sum model vs whole-board game | equal: the tree never splits into components before a passer (Theorem 2.3) | proved". It sits in the table for the four-file candidate `W a2 c2 / B b7 d7`, where it is about that position only. As a general statement it is false (it needs HSS), and P1 and P2 are examples. A reader could take it as general.

Suggested edits (not made): add P2 to the sentence at `05_sums.tex:141`; add "for this position" to `RESULTS.md:26`.

## Not done

- I did not rerun the 21 five-file positions or the 179 *2 scope hits. Only the two disputed positions and the third one in the same table were checked.
- The "two programs" for the whole-board value of P1 and P2 are the C scan and `sumsolver.py` (plus cylcgt with splitting off). `crosscheck/minimax.py` only has the count rule, so it was not used.
