# T78 referee report · One-sided extension of Corollary 3.8b

## Five-line summary

- **PROVED — CORRECT AS STATED** under the note’s reach convention. For `on`, no follower of any short component may offer ⊖ to either player. For `off`, exclude ⊕ in the same way.
- **PROVED** — To satisfy Theorem 3.8, `on` needs only the bound `B ≥ 1 + M_R(K)`. For `off` use `B ≥ 1 + M_L(K)`. Pairwise safety follows from the sign exclusion.
- **PROVED** — Under the same sign exclusion, first-event dominance and outcome equality hold for every integer `B ≥ 1`. The componentwise reserve criterion itself can fail at small *B*.
- **COMPUTED-1** — Of 94,456 reservoir/multiset pairs enumerated exhaustively, 25,296 met the published hypotheses. All passed the criterion, dominance, and outcome comparison at every follower tuple for both movers.
- **PROVED** — Absence of an adverse option only at the root allows even the root winner to reverse. Two option edges suffice. Absence along all alternating plays from the root protects the root outcome but can still miss a losing follower.

## Statement and reach convention

**PROVED.** The following wording makes the existing quantifier explicit. “Let `K_1,…,K_m` be short. For `S=on`, assume `−∉τ(K_i)` for every *i*. For `S=off`, assume `+∉τ(K_i)` for every *i*. Then the criterion of Theorem 3.8 holds at the published bound, and its conclusion holds for both movers at every reachable tuple.” Here `τ(K_i)` is evaluated at the root of the component but already inspects all its followers. A node’s *immediate* event set is a different test. [Definition 1.10 and its threat sets](../../../kings/theory/LOOPY.md#14-what-big-can-and-cannot-do)

**PROVED.** Section 3 takes the product of the component reach sets to define reachable tuples. Follow nonterminal option edges of either colour in each component, then take the product. An event is an option at the resulting node “by either player”, including a suicide. Reaching the event’s source and having the right mover to take it on an actual play are distinct conditions. The note uses the former and checks both movers. The supplement has the same quantifier in Theorem 3.8 and the same qualification after Corollary 3.8b. [Theory note, §3](../../../kings/theory/LOOPY.md#3-spare-tempo-moves-as-loopy-games) · [Supplement S12, Theorem 3.8 and following](../../../dist/tog/supp_src/s12_kings.md)

## Proof audit

1. **PROVED — Which inequalities apply.** Theorem 3.8 assumes “B ≥ 1” and quantifies “for every j and every σ for which some reachable node of G_j has an event of sign σ.” Take `Y=(S,K_1,…,K_m)`. The reservoir has no terminal options. With `S=on`, the sign assumption rules out every minus index/sign pair in that quantifier. It also implies pairwise safety because no coordinate has a minus threat. If no component has either sign, the criterion and dominance are vacuous. The body of Corollary 3.8b requires finite reserves on both sides and cannot itself be invoked for this step.

2. **PROVED — The plus inequality.** For each remaining event coordinate *j*, the exact hypothesis is “Σ_{i≠j} Λ_B(G_i) ≤ B − 1 (σ = +).” Proposition 3.9 gives `Λ_B(on)=0` because Right has no move when starting there. For another short coordinate `K_i`, take any follower *y*. There is no reachable ⊖, so the translated game `y^B` can introduce only a Left-only integer chain. Right can make at most `M_R(y)` moves in that coordinate, counting a final Right move into `+B`. With `M_R(y)` extra Left tokens, Left can answer each Right move with a token until Right runs out. Thus `λ_B(y)≤M_R(y)≤M_R(K_i)`, using exactly the short-component estimate in 3.8(a). Maximizing over followers gives the same bound on `Λ_B(K_i)`. The required sum is bounded by `Σ_{i≠j} M_R(K_i)≤M_R(K)≤B-1`. The definition of `M_R(K)` is the sum of the root coordinate counts, allowing either colour of edge in any order and counting terminal edges. The published maximum of the two tempo counts suffices. In fact the event coordinate can be omitted separately for each *j*.

3. **PROVED — At the event, for both movers.** The proof of 3.8 starts “Let (Y′, j, +) be an event”. Let *R* be the translated rest, including `on`. The sum of its *local* Left reserves is at most the sum of the maxima just bounded. Lemma 3.8a adds these reserves and allows surplus tokens, so Left wins `R+(B-1)` and `R+B` moving second. With Right to move at the frontier `B+R`, the latter result applies. With Left to move, she spends one token in *B* and uses the former result. Every existing frontier is therefore a win for its beneficiary for both movers. No step needs `ρ_B(on)`.

4. **PROVED — Nothing reintroduces the missing sign.** After a move inside `K_i` to *y*, every follower of *y* was already a follower of `K_i`, so `τ(y)⊆τ(K_i)`. A pass leaves all component nodes fixed. Theorem 3.7 requires only “If Y is first-event dominant for B”. Its two inductions compare ordinary moves with the corresponding pre-event successor and terminal moves with their certified frontier. In the reverse induction the proof excludes a *present* frontier of the opposite sign as a winning option for the wrong side. With no minus edges there is no minus frontier to inspect. A plus frontier never supplies a winning option for Black. Subsequent moves *after* translation of an event are already accounted for by the frontier win in step 3. The bridge yields equality for every tuple and both movers.

5. **PROVED — The mirror.** With `S=off` and no reachable ⊕, only “Σ_{i≠j} P_B(G_i) ≤ B − 1 (σ = −)” applies. `P_B(off)=0`. From any other short coordinate, Left has at most `M_L(K_i)` moves, including entry into a Right-only chain `-B`. Right can answer with that many Right tokens, so `P_B(K_i)≤M_L(K_i)`. With `B≥1+M_L(K)`, the frontier `-B+R` is a Right win moving second. Moving first, Right spends one token and uses the second-player strategy with `B-1` tokens. The same bridge applies. No step uses `λ_B(off)`.

[Definitions 1.1–1.4](../../../kings/theory/LOOPY.md#12-games-with-decisive-terminals-and-four-models) · [Definition 1.10](../../../kings/theory/LOOPY.md#14-what-big-can-and-cannot-do) · [Theorems 3.7–3.8, Lemma 3.8a and Proposition 3.9](../../../kings/theory/LOOPY.md#3-spare-tempo-moves-as-loopy-games)

### How small can B be?

**PROVED.** For `on`, Left can always pass. In the pre-event D-game every Black move consumes an edge of the finite short sum or awards White the win. Under the sign exclusion, White therefore wins from either start. In the translated sum, and at every plus frontier, everything beside `on` is short. Left can keep passing and Black runs out of moves. This proves equality and dominance for every permitted `B≥1`, independently of the numerical criterion. For `off` the same argument gives Black the win. Conversely, one structurally reachable adverse event always destroys dominance here. Its translated frontier still contains the reservoir and only short games, so the reservoir owner wins regardless of the event’s sign.

**PROVED.** The one-sided tempo bound can be sharp for the *criterion*. Beside `on`, take `K_1={⊕|}` and let `K_2=-n` be a terminal-free Right-only chain, `n≥1`. At a plus event of `K_1`, `Λ_B(K_2)=n`. Right starts in `-n+C`, and Left must answer each of the *n* moves. The criterion is exactly `n≤B-1`, with `M_R(K)=n`, even though Left wins at every frontier for `B=1`. Conjugating gives the sharp family for `off`. The script also checks both families for `1≤n≤5`.

## Independent exhaustive check

**COMPUTED-1.** From the project root, this command generates the universe, solves the games, prints the counts and smallest mismatches, and checks the concrete reserve examples. It reproduces all numerical results below. A result pair is ordered (Left starts, Right starts). The program prints 0 for a White win and 1 for a Black win.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python delegate/out/T78/referee.py
```

**PROVED (enumeration scope).** An instance consists of one of the two reservoirs and an unordered multiset of one, two, or three short component forms, with at most five option edges in total after unfolding. Each mover-labelled edge costs one, including a terminal edge. A nonterminal target adds the cost of its own form. Each side has a set of distinct targets chosen from ⊕, ⊖ and smaller forms, with empty sets allowed. Left and Right can both have the same target. To generate cost *e*, the script enumerates all subsets of (mover, target) with total cost *e*. All possible targets have already been generated. Induction on *e* gives completeness within this bound. Identical option trees share storage. The enumeration retains distinct forms that happen to have the same CGT value, permits repeated components and zero components, and counts each multiset once. The bound concerns unfolded edges, so a DAG with shared followers can have a small vertex count and still fall outside it.

**COMPUTED-1 (method).** The solver explicitly builds the reachable graph on (tuple, mover) with a reservoir pass as an edge. In D, a move to a signed terminal labels the winner immediately. For CGT the translator replaces each signed terminal by a chain of the appropriate length and owner, leaving the other coordinates active. A fixed-point search on each graph propagates wins and losses from signed terminals and players with no move. Unresolved states draw. The code also solves every frontier, and computes both second-player reserve tests by trying token budgets from zero through `B-1`. Larger and infinite reserves can be grouped because either exceeds the allowance. For each multiset it checks both movers at the full product of follower sets. The alternating-play filter separately traverses legal pre-event moves from both root starts, including passes and suboptimal moves. It imports only the standard library. [Runnable solver](referee.py)

**COMPUTED-1.** The number of component forms at unfolded edge costs 0 through 5 was respectively 1, 6, 27, 146, 877 and 5,606. The table gives counts **per reservoir**. The program enumerated each colour separately. “With event” excludes vacuous sign-free instances from the preceding column. Every hypothesis column retains pairwise safety.

| Short components | All multisets | Published hypotheses | Of these, with event | Root-only absence | Alternating-play absence |
|---:|---:|---:|---:|---:|---:|
| 1 | 6,663 | 2,082 | 1,724 | 4,982 | 2,905 |
| 2 | 17,304 | 4,673 | 4,029 | 8,741 | 5,652 |
| 3 | 23,261 | 5,893 | 5,146 | 10,159 | 6,888 |

**COMPUTED-1.** At `B=1+max(M_L(K),M_R(K))`, the following counts apply separately to each reservoir. An instance counts once in a failure column if it fails anywhere in that column’s scope. The last column includes root failures.

| Reading of “no adverse event”, with safety retained | Accepted | Criterion fails | Dominance fails | Outcome differs at root | Outcome differs at some theorem tuple |
|---|---:|---:|---:|---:|---:|
| All component followers, either mover | 12,648 | 0 | 0 | 0 | 0 |
| Immediate root options only, either mover | 23,882 | 11,234 | 11,234 | 1,667 | 6,365 |
| All actual alternating plays from either root start | 15,445 | 2,797 | 2,797 | 0 | 654 |
| All component followers, only edges taken by the adverse event’s beneficiary | 20,831 | 8,183 | 8,183 | 0 | 0 |

**COMPUTED-1.** Every published-hypothesis instance also passed the criterion at the one-sided tempo bound. At `B=1`, 3,460 instances per reservoir failed the criterion, yet every such instance, and every other published-hypothesis instance, passed dominance and the outcome comparison.

## Smallest counterexamples to weaker readings

**PROVED — Ignoring suicide edges costs one edge.** Let `S=on`, `K={⊖|}`. Left can pass and win in D, but the ⊖ frontier `on-B` is won by White. Thus dominance and the criterion already fail. More generally, if Black has no move to ⊖ at any follower, Left can decline all her own suicides by passing, so outcome equality survives throughout. For `off`, exchange colours and use `K={|⊕}`. An event requires at least one edge.

**PROVED — Inspecting root options only costs two edges, and reverses both winners.** For `on`, let `V={|⊖}`, `K={|V}`. The only root edge is an ordinary Right move. Right plays to *V* and then to ⊖. Left can only pass. Hence D gives (Black, Black). The published bound starts at `B=3`, but every finite translation gives (White, White). A one-component sum is pairwise safe. For `off`, take `V={⊕|}`, `K={V|}`. D gives (White, White), the translation (Black, Black). A hidden event needs at least one ordinary edge to its source plus the terminal edge itself. At the same size the root can also conceal failure at a follower while remaining correct itself. Use `on` with `K={V|}`, `V={|⊖}`. Left passes at the root and Black has no root move.

**PROVED — Alternating-play absence can miss a theorem tuple.** With `on`, take `V={|⊖}`, `U={V|}`, `K={U|}`. Black has no move at the root or at *U*. To reach *V* requires two successive Left moves in *K*, which no alternating play from either root start can realize. The root is a White win in both games. But *V* belongs to the component reach set, and there D gives (Black, Black) against (White, White) in the translation, including at `B=3`. The `off` mirror uses `V={⊕|}`, `U={|V}`, `K={|U}` and reverses the colours. Absence on all actual root plays always suffices for the *root* outcome because the reservoir owner can pass and the other side exhausts its finite options. **COMPUTED-1.** Three edges is the first outcome mismatch under this filter in the enumeration. Dominance alone can already fail with two edges, for example `on` beside `{{⊖|}|}`. The hidden suicide is structurally present and cannot be taken on an alternating root play.

## Scope of the verdict

**PROVED** applies to the abstract D-games and their normal-play BIG translations under the note’s definitions. **COMPUTED-1** identifies counts from this independent program. The earlier random sample was not rerun or matched instance by instance. The finite enumeration covers the stated edge budget and component counts. It does not test chess realizability, race rules, either passed-pawn test, or en passant. No human or proof-assistant verification is claimed.
