# K33 blind proofs

## Fixed-point convention

For any finite game graph, use states `(position, mover)`. Let `W` be the least fixed point for a finite White win and `L` the least fixed point for a finite Black win. At a White-to-move state, membership in `W` means that some move is an immediate White terminal or reaches `W`; at a Black-to-move state it means that there are no moves, or every move is an immediate White terminal or reaches `W`. The rules for `L` are the color mirror. The stage at which a state first enters one of these fixed points is its finite-win rank. The two least fixed points are disjoint. A state in neither is a draw: in particular, an infinite play is a draw, not a win for either side.

All inductions below are on these least-fixed-point stages/ranks, never on the game graph being acyclic. In a sum with decisive terminals, every option to either terminal is an event and the first event ends the whole sum. An option to the opponent's terminal is a suicide for the mover, but still an event with the opponent's terminal sign. This includes suicides in both the bridge and the sandwich arguments.

## Theorem 3.7 — loopy bridge — PROVED

Fix a reachable tuple and compare corresponding states before an event, with the same mover. A nonterminal move changes the same coordinate to the same node in the D-sum and translated sum. A D-option to terminal sign `σ` ends the whole D-sum at that first event; the corresponding translated move reaches frontier `σB + Σ(i ≠ j) (y'_i)^B`, with the other player to move. By first-event dominance, that frontier is a finite `σ` win whichever player moves next. Thus event edges have the terminal's winner in the translated sum, including a suicide into the opponent's terminal.

For each sign `σ`, prove both inclusions on tuple states. First induct on the D-attractor stage. At a `σ`-to-move state, a winning terminal option translates to a frontier in `W_σ`; a winning nonterminal option translates to the same successor, which is in `W_σ` by induction. At a `σ̄`-to-move state in `W_σ`, there is no `σ̄`-terminal option, since that mover could take it and win; every other option is either a `σ` terminal (a `σ` frontier) or a nonterminal successor in the preceding D-stage. The translated state therefore enters `W_σ` too. A no-option `σ̄` state is also no-option in the translation, since available component options correspond.

For the reverse inclusion, induct on the translated-sum attractor stage, restricted to tuple states. At a `σ`-to-move tuple state in `W_σ`, choose a translated winning option. If it is a frontier, its sign must be `σ`: a `σ̄` frontier is a `σ̄` win by dominance, disjoint from `W_σ`; hence the D-sum has the matching `σ` terminal option. If it is nonterminal, it is the same D-option and the tuple successor is in `W_σ` by induction. At a `σ̄`-to-move state, every translated option is in `W_σ`. No frontier option can have sign `σ̄`, again by dominance and disjointness, so each D-option is a `σ` terminal or a nonterminal successor in `W_σ`; if there are no options, the mover loses in both graphs. Thus the D-state is in `W_σ`.

The two inductions apply to `σ = White` and `σ = Black`, at every reachable tuple and either mover. A play that loops forever without an event is outside both least fixed points and is a draw in both models; finite exhaustion with no move has the same normal-play loss. No acyclicity of a component was used.

## Lemma 3.8a — reserve subadditivity and monotonicity — PROVED

First prove the stated Left claims. Suppose Left wins `G_i + n_i` with Right to move, for `i=1,2`. In the sum, keep a conceptual allocation of the `n_1+n_2` Left tokens into `n_1` tokens assigned to `G_1` and `n_2` assigned to `G_2`; the tokens are indistinguishable in play, but this accounting lets us follow the two individual strategies.

Maintain the invariant that each local position, including its allocated remaining tokens, is in `W` with Right to move. When Right moves in component `i`, this is a legal Right move in that component's individual game. Since its local state is in `W` with Right to move, the successor is still in `W` with Left to move. Left then follows the individual finite-win strategy in that component. Its reply is either a move in `G_i` or a spend of one of that component's allocated tokens, and reaches `W` with Right to move again. The other component was unchanged. Thus each Right/Left pair preserves the invariant and strictly decreases the finite-win rank of the selected component. The sum of the two local ranks strictly decreases on every pair, so the strategy cannot permit infinite play. If Right has no move in either component, Right loses. Therefore Left wins `G_1+G_2+(n_1+n_2)` with Right to move. The same rank argument works for any finite number of summands.

If Left wins `G+n` with Right to move and `m ≥ n`, she follows that strategy in `G+m` while designating only `n` of the available tokens for it. Extra Left tokens are ignored; Right's moves are unchanged. The same finite win follows. Swapping Left and Right proves both claims for Right tokens, so the reserve of a sum is at most the sum of the reserves for `λ` and for `ρ`.

The proof covers arbitrary finite loopy normal-play games. A draw is not treated as a win: each invoked component strategy has a finite rank, and the sum of ranks rules out a play that evades the forced finite win forever.

## Theorem 3.8 — reserve criterion — PROVED

Fix a reachable tuple and an event of sign `+` in component `j`. For each other component let `λ_i = λ_B(y'_i)`, and let `N = Σ(i ≠ j) λ_i`. Since `λ_i ≤ Λ_B(G_i)`, the hypothesis gives `N ≤ B−1`. By Lemma 3.8a, Left wins

`H + N`, where `H = Σ(i ≠ j) (y'_i)^B`,

with Right to move (if there are no other components, this is the immediate win from `0` with Right to move). Monotonicity gives a Left win in `H + (B−1)` with Right to move. From the frontier `+B + H`, if Left moves first she spends one of the `B` Left tokens, leaving `H+(B−1)` with Right to move. If Right moves first, Left already wins second by monotonicity, since `B ≥ B−1`. Thus every such `+` frontier is a finite White win whoever moves first.

For an event of sign `−`, put `ρ_i = ρ_B(y'_i)` and `N = Σ(i ≠ j) ρ_i ≤ B−1`. The mirror of Lemma 3.8a says Right wins `H−N` with Left to move; monotonicity gives the same result with `B−1` Right tokens. In the frontier `−B+H`, if Right moves first, spend one Right token and leave `H−(B−1)` with Left to move; if Left moves first, Right wins second directly. So every `−` frontier is a finite Black win whoever moves first.

These are exactly all frontier positions required by first-event dominance. The event coordinate is absent from a frontier, so no bound on its own reserve is needed. By Theorem 3.7, the D-sum result and translated CGT outcome agree at every reachable tuple. Loops in the other components are covered because the reserve strategies used above are finite-rank wins; infinite play remains a draw.

## Theorem 3.11 — sandwich — PROVED

Use finite-win ranks in the relevant sum as the induction measure. In each simulation below, a target move is either mirrored as a source move, or corresponds to a source reservoir pass. That source transition decreases the rank. If a target gives the opponent fewer moves than the source, every target reply is among the source replies already covered by the source winning strategy; if the target side to move has no moves, it loses immediately. Consequently the simulated strategy still forces a finite win.

### White-win chain

`W(K ⊞ off) ⇒ W(K ⊞ S)`: Follow the source winning strategy in the shadow `K ⊞ off` game and make its `K` move in the real game. On a White turn, the shadow cannot choose an `off` move, so its winning strategy must choose `K`. If Black moves in real `S` to a nonterminal, record the corresponding Black `off` pass in the shadow. If Black moves in `S` to `⊕`, White wins at once; Black's option to `⊖` is excluded by the condition on `S`. A missing real move by Black is also an immediate Black loss. All other moves are the same `K` moves. The source rank decreases on each simulated transition, giving a finite White win.

`W(K ⊞ S) ⇒ W(K ⊞ on)`: Keep a shadow `S` position and follow a finite White strategy in the source. Mirror source `K` moves. A source White move in `S` used by a winning strategy cannot be to `⊖` (that loses immediately), and cannot be to `⊕` by the hypothesis on `S`; hence it is nonterminal. Replace it by White's `on` pass and update the shadow `S` position. In the target, Black can only move in `K`; each such move is one of the source's Black replies. If Black has no target move, Black loses. The target moves therefore follow rank-decreasing source transitions, so White still wins finitely.

### Black-win chain

`L(K ⊞ on) ⇒ L(K ⊞ S)`: Follow a finite Black strategy from the source `K ⊞ on`. A source Black move must be in `K`, since `on` gives Black no move. Mirror it in the target. If White moves in real `S` to a nonterminal, record White's `on` pass in the shadow; if White moves to `⊖`, Black wins immediately. White's option to `⊕` is excluded. Other White moves in `K` are mirrored. Every target reply is covered by the source strategy, whose rank decreases, so Black wins finitely.

`L(K ⊞ S) ⇒ L(K ⊞ off)`: Follow a finite Black strategy in the source. Mirror `K` moves. A winning Black strategy cannot select an `S` move to `⊕` (that would lose at once), and cannot select `⊖` because Right options to `⊖` are excluded; any selected `S` move is nonterminal. Replace it by Right's `off` pass and update the shadow `S` position. White has fewer `S` moves in the target; every remaining White reply is a source reply covered by the strategy, and a White node with no target move loses immediately. Rank descent gives the finite Black win.

The event checks in these four simulations include suicides: a Left option to `⊖` and a Right option to `⊕` end the whole sum for Black and White respectively. The restrictions on `S` exclude only same-mover winning terminals, exactly the options that could invalidate the pass substitutions.

### Equalities

For `W(K ⊞ off) ⊆ W(K ⊞ dud)`, White uses the same `K` strategy; Right's options in `off` and `dud` are identical, and White can ignore her extra `dud` pass.

Conversely, at a White-to-move state in `W(K ⊞ dud)`, some option must reach a lower-rank `W` state. That option cannot be only White's `dud` pass: if the pass reached a lower-rank Right-to-move `W` state, Right's own `dud` pass back would have to reach a still lower-rank `W` state, namely the original White-to-move state, a contradiction. Hence there is a winning `K` option. Use it in `off`; at Right-to-move states, Right's options (including the pass) are the same in both games. Induction on rank gives `W(K ⊞ dud) ⊆ W(K ⊞ off)`. Thus `W(K ⊞ off)=W(K ⊞ dud)`.

The Black-win equality is the mirror. In `L(K ⊞ on)`, Right can ignore the extra `dud` pass, giving `L(K ⊞ on) ⊆ L(K ⊞ dud)`. At a Right-to-move state in `L(K ⊞ dud)`, Right's winning option cannot be only his `dud` pass: after that pass, Left's `dud` pass back would force a still lower Black-win rank at the original state. A winning `K` option therefore exists and works in `on`; Left's options are the same in both games. This gives `L(K ⊞ dud) ⊆ L(K ⊞ on)`, so `L(K ⊞ on)=L(K ⊞ dud)`.

All statements hold at every listed node and either mover. No stopper or shortness assumption was used; finite wins are certified by rank, while non-winning infinite-play possibilities remain draws.

## Blind random checks — COMPUTED-1

Reproduce from the project root with:

```sh
PYTHONPATH=. .venv/bin/python kings/delegate/out/K33/random_tests.py
```

The script uses seed `330027`. For each random graph, each possible directed node edge is independently included with probability `0.22`; each allowed terminal edge is independently included with probability `0.14`; roots are node `0`; component sizes are uniform on `1..4`. For Theorems 3.7 and 3.8, it samples `B` uniformly from `1..4`, with `2` or `3` components. It runs 180 unrestricted random component tuples and 60 signal cases; each signal case has both signs forced at node `0` of one random component and the remaining components are zero games. For Lemma 3.8a, it generates 500 pairs of terminal-free loopy games and token counts uniformly from `0..4`. For Theorem 3.11, it generates 300 `(K,S)` pairs, with `S` restricted so Left has no `⊕` option and Right has no `⊖` option.

The run checked 233 Left and 232 Right subadditivity premises, 364 Left and 356 Right monotonicity premises, and all 1,185 applicable reserve implications. Among 240 Theorem 3.7 instances, 131 satisfied first-event dominance; all 564 reachable tuple/mover positions in those cases agreed. The Theorem 3.8 criterion held in 129 of 240 cases; all 528 required frontiers were dominant and all 546 reachable tuple/mover positions agreed. Theorem 3.11 checked all six inclusions/equalities at 3,584 node-pair/mover positions (21,504 Boolean assertions). No counterexample was found.

These are `COMPUTED-1` checks of the written results, not substitutes for the proofs above. The reserve test records `B` as a sentinel for any reserve greater than `B−1`; this is exact for deciding the stated criterion, which only asks whether the sum is at most `B−1`.
