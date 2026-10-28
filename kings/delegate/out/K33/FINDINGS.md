# K33 comparison findings

## Summary

1. **PROVED:** Theorem 3.7, Lemma 3.8a, Theorem 3.8, and Theorem 3.11 survived an independent Codex proof check.
2. Every proof step reviewed in LOOPY for those four results is **SOUND**; I found no gap or counterexample.
3. Theorem 3.8(a)–(c), Corollary 3.8b, and Corollary 3.11a follow with the scopes stated in LOOPY.
4. **COMPUTED-1:** the seeded small-game run passed 1,185 reserve checks, 564 bridge positions, 546 criterion positions, and 3,584 sandwich positions.
5. Keep the theorem labels **PROVED**; keep this run's numerical evidence **COMPUTED-1**, not CHECKED-2.

## Comparison route

The blind proof is in [`PROOF.md`](PROOF.md). It uses the same finite-win rank structure as LOOPY, but expands several steps:

Comparison sources: [`LOOPY.md`](../../../theory/LOOPY.md), lines 1729–1844; [`K21 VERIFY.md`](../K21/VERIFY.md), §1, lines 26–39.

- **Theorem 3.7:** I compare the two arenas by explicit attractor-stage inclusions for each winner. LOOPY uses the same two inductions, writing the directions as D-stage then translated-CGT-stage. Both rely on first-event dominance to classify frontiers and on disjoint `W_L`/`W_R` sets in the reverse direction.
- **Lemma 3.8a:** I keep one local finite-win rank per component and use their sum as the potential. LOOPY names that potential `Φ` and notes its decrease is at least two per Right/Left round. This is the same argument.
- **Theorem 3.8:** The token-spending argument is the same. I spell out both movers for each event sign; LOOPY states the positive case and takes the negative case by symmetry.
- **Theorem 3.11:** I spell out all four implications using a shadow state for `S`, including the terminal cases. LOOPY proves the two White implications and invokes color symmetry for the Black chain. Both remove the extra `dud` pass by a least-stage contradiction.

Infinite play remains a draw throughout. Every strategy called a win has a finite least-fixed-point rank. The first event ends the D-sum; suicides are included by their terminal sign.

## LOOPY proof-step audit

| Result | LOOPY proof step | Verdict | Check |
|---|---|---|---|
| Theorem 3.7 | Corresponding nonterminal options and event-to-frontier options | **SOUND** | A move before an event changes the same coordinate; a terminal option in the D-sum is a translated move to its signed frontier. |
| Theorem 3.7 | D-attractor-stage induction into translated `W_σ` | **SOUND** | A matching frontier is a finite `σ` win by dominance; nonterminal successors follow the induction. At an opponent-to-move state, an own-terminal option for that opponent would contradict membership in `W_σ`. |
| Theorem 3.7 | Translated-attractor-stage induction back to D `W_σ` | **SOUND** | A frontier of the opponent's sign cannot be a winning option for `σ`, since it is in the disjoint opponent win set. Every remaining option is a matching `σ` event or nonterminal D successor. |
| Theorem 3.7 | No-option states and draws | **SOUND** | Before an event, available options correspond. Unresolved cycles are outside both least fixed points and therefore draw. |
| Lemma 3.8a | Start with individual finite-win strategies and answer Right in the same component | **SOUND** | The local state is Right-to-move in `W_L`; each Right move is covered and leaves Left-to-move in `W_L`. Left's finite-rank reply can spend only that component's allocated tokens. |
| Lemma 3.8a | `Φ` drops by at least two per round | **SOUND** | The Right move lowers that component's rank once, and Left's reply lowers it again. Other local ranks stay fixed. |
| Lemma 3.8a | At zero potential, Right has no move; extra tokens are harmless | **SOUND** | All local Right-to-move states are rank-zero wins for Left, hence have no Right option. More tokens can be ignored. The Right reserve statement is the mirror. |
| Theorem 3.8 | Bound the rest's reserves by their maxima and use subadditivity | **SOUND** | The criterion is quantified over all reachable nodes, so each frontier's sum of reserves is at most `B−1`. Repeated application of Lemma 3.8a handles any finite number of rest components. |
| Theorem 3.8 | Positive frontier, Right to move | **SOUND** | Right cannot move in the positive integer stack; the Left-second win with at least `B−1` tokens applies. |
| Theorem 3.8 | Positive frontier, Left to move | **SOUND** | Left spends one token, leaving `B−1` and Right to move. |
| Theorem 3.8 | Negative frontier by symmetry | **SOUND** | The same argument uses Right tokens and `ρ_B`; it covers both movers. |
| Theorem 3.11 | `W(off) ⇒ W(S)` shadow simulation | **SOUND** | A real Right move in `S` maps to an `off` pass; a Right-to-`⊕` suicide wins for White; Right-to-`⊖` is excluded by `S`. A source `W_L` state cannot offer Black a winning terminal. |
| Theorem 3.11 | `W(S) ⇒ W(on)` shadow simulation | **SOUND** | A winning Left `S` move is nonterminal: `⊕` is excluded and `⊖` would lose. It maps to an `on` pass; Right's target moves are a subset of the source replies. |
| Theorem 3.11 | Remove Left's extra `dud` pass for `W(dud) ⊆ W(off)` | **SOUND** | If a lower-rank winning move were only the Left pass, the Right pass would return to the original state and force a contradictory lower rank. A winning `K` move must exist. The reverse inclusion is immediate. |
| Theorem 3.11 | Black chain and `L(on)=L(dud)` by color mirror | **SOUND** | The restrictions on `S` mirror exactly; a Black-winning strategy cannot use a Right suicide to `⊕`. For the equality, a Right `dud` pass cannot be rank-lowering because Left's pass returns to the original state. |

All listed steps are SOUND. No step is marked GAP or FALSE.

## Theorem 3.8 additions in LOOPY

- **(a) Follows.** Pairwise safety makes every other component free of the opposite-sign event at a given event. For a short component with no reachable `⊖` option, answering each Right move with a Left token proves `λ_B(y) ≤ M_R(y)`; the mirror gives `ρ_B(y) ≤ M_L(y)`. Summing over the other components gives the reserve criterion when `B > max(M_L(Y), M_R(Y))`.
- **(b) Follows.** In `A={∣⊕}` and `C={⊖∣}`, each of the four reserves is zero: the player to move either has no move or can choose only a suicide. The criterion applies although their event signs conflict, and their translated sum is zero. The claimed strict strengthening over pairwise safety is sound.
- **(c) Follows as worded.** For a `+` event with one rest component `G`, dominance requires Left to win `G^B+B` with Right to move, hence `λ_B(G)≤B`; an infinite opposite reserve therefore prevents dominance. This is only necessity for dominance, not for equality of D-result and CGT outcome.
- **Corollary 3.8b follows.** Terminal-free `S` has no events and its translation/reserves do not depend on `B`. Events are only in the short, pairwise-safe `K` components; the stated bound gives `Λ(S)+M_R(K)≤B−1` and `P(S)+M_L(K)≤B−1`, so Theorem 3.8 applies.
- **Corollary 3.11a follows immediately.** The two forced-win predicates cannot both hold, since Theorem 3.11 would make one `K⊞S` position both a White and Black finite win. Each predicate forces the same winner for every admissible `S`.

## Random checks

Reproduce from the project root:

```sh
PYTHONPATH=. .venv/bin/python kings/delegate/out/K33/random_tests.py
```

The fixed seed is `330027`. In each component, every possible node edge is included independently with probability `0.22`, and each allowed terminal edge with probability `0.14`; component sizes are uniform on `1..4`. Roots are `0`. Theorem 3.7/3.8 cases use two or three components and `B` uniform on `1..4`: 180 unrestricted tuples plus 60 cases with both event signs forced at node `0` of one random component and zero games elsewhere. Theorem 3.11 uses 300 random `(K,S)` pairs, with `S` generated under the no-Left-`⊕`/no-Right-`⊖` restriction. Lemma 3.8a uses 500 pairs of terminal-free games and token counts uniform on `0..4`.

| Check | Generated cases | Applicable checks | Result |
|---|---:|---:|---|
| Lemma 3.8a, Left subadditivity | 500 game pairs | 233 premises | 233 passed |
| Lemma 3.8a, Right subadditivity | 500 game pairs | 232 premises | 232 passed |
| Lemma 3.8a, token monotonicity | 500 games | 364 Left + 356 Right premises | 720 passed |
| Theorem 3.7 | 240 tuples | 131 dominant; 564 reachable tuple/mover positions | 564 matched |
| Theorem 3.8 | 240 tuples | 129 criteria held; 528 frontiers and 546 reachable tuple/mover positions | all passed |
| Theorem 3.11 | 300 `(K,S)` pairs | 3,584 node-pair/mover positions; 6 assertions each | 21,504 passed |

The random output reports 1,185 applicable reserve implications in total. The reserve checker uses `B` as a sentinel for any reserve greater than `B−1`, which is exact for deciding this criterion. No counterexample was found. These are `COMPUTED-1` checks from one implementation, not `CHECKED-2`.

## Recommended labels

- **PROVED:** Theorem 3.7, Lemma 3.8a, Theorem 3.8, Theorem 3.11, Corollaries 3.8b and 3.11a, and Theorem 3.8(a)–(c) with (c) limited to necessity for dominance. This adds an independent Codex-family proof re-derivation to the Claude-family proof/referee route.
- **COMPUTED-1:** the random counts in this report and the script output. They use one implementation and should not be called CHECKED-2.
- The Research Plan's §3 ground rule also calls for human proof review. This K33 check supplies an independent AI proof, not a human review.
