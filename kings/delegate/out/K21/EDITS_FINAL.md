## Integrator notes for K21 (fix round; this file supersedes EDITS.md, apply this file only)

- **LOOPY.md has changed since K21 wrote its EDITS** (latest commit 44d1e72; it contains the K19 and later edits of 2026-10-27). Every block is rebased: the OLD text of all four blocks was checked mechanically against the
  current file and occurs exactly once. K21's three original OLD anchors (the C3.5 row of the results table, the heading `**What loopy kings do to the convention.**`, and item 4 of section 8) did not move; the heading is re-emitted at the end
  of its NEW text, so nothing is lost. One block is new (below). Apply in file order (the blocks do not overlap).
- **K21 could not write REPORT.md.** Cite `kings/delegate/out/K21/VERIFY.md` (the referee), `summary.json`, `logs/`, `scripts/` and EDITS.md's own text, as the NEW text does.
  Note: `kings/delegate/out/K21/EDITS.md` on disk was patched in place at 19:13 by `scripts/apply_referee_fixes.py` (a partial application of F1 to F4). This file was built from the original text and carries the complete fixes; do not apply both.
- **Labels used.** PROVED (one AI proof each, re-derived step by step by the referee): Theorem 3.7, Lemma 3.8a, Theorem 3.8, Corollary 3.8b, Propositions 3.9 and 3.10, Theorem 3.11 (Corollary 3.11a is immediate from 3.11; the body of Proposition 3.12 from 3.3 and 3.4).
  CHECKED-2: the brute-force results where two independent solvers agree (K21's `dsum.py` and the referee's `ref.py`: 20,324 states, 0 disagreements; dominance and the criterion on 1,500 instances), the reserve table of Proposition 3.9, the named counterexamples at the root.
  COMPUTED-1: sample counts from one generator (K21's and the referee's), and the whole chess P-model part (the referee did not re-run the oracle: the shared lock was never free; the counts were recounted from K21's files and three predictions re-derived by hand).
- **Referee fixes, all applied.**
  - F1: Proposition 3.12 and its summary-table row now say: right exactly outside P_R (on), outside P_L (off), outside P_L ∪ P_R (dud); wrong exactly on the forced positions of the side the reservoir does not favour (of both sides for dud, where "right" is exactly the tempo regime).
  - F2: "no translation" is narrowed to forcible threats in the Reading paragraph, the first bullet of "What fails" (heading changed) and section 8 item 4; a new bullet gives the unforceable cases, `{⊖∣} ⊞ on` D = CGT = (W, W), `{∣⊕} ⊞ off` (L, L), `{⊖∣} ⊞ dud` and `{∣⊕} ⊞ dud` (D, D); the "no translation" sentence for the pure reservoirs now applies to on, off, dud only.
  - F3: Theorem 3.8(c) is retitled and says it is necessity for dominance only, with the `{⊖∣} ⊞ on` example.
  - F4: "CONJECTURE C1" is replaced by "the guess is refuted".
  - F5: the empty clause of Corollary 3.11a is replaced by: outside T nothing depends on S; the inclusions hold everywhere and are Theorem 3.11 itself.
  - The referee's second small counterexample is added where K21's counterexamples are listed: K = `{⊕, 0 ∣ 0}`, S = `{0 ∣ off}`, Right to move at the root, D = W, translation L (B = 1, 2, 5, 14). I re-checked it, and the four F2 examples and K21's first counterexample, with a small independent solver (`python3`, tiny instances): all as stated.
  - F6 (optional): no change to the content of open item (d); I only added the word CONJECTURE to its "untested".
- **Referee points judged wrong: none.**
- **Further changes beyond the referee list** (each small, none weakens a label):
  - Corollary 3.8b: the sentence "S = on qualifies when ..." said `on` and `off` qualify, but they violate the corollary's finite-reserve hypothesis (ρ(on) = λ(off) = ∞). It now says they satisfy Theorem 3.8 directly under the sign condition (same proof; the referee tested 1,810 such instances, 0 failures).
  - Definition 1.4 and Definition 1.10 are stated in LOOPY for short games; the new Section 3 text says it uses them verbatim and restated for loopy components.
  - The referee's caveat is recorded: the K21 all-states C cross-check (47,896 states) contains no instance with D ≠ CGT and no draw, so it tests only the agreeing regime; the differing regime is covered by the root cross-checks and by the referee's run.
  - Open item (b) no longer says "sum reserve ∞ at an event ⇒ no B" for three or more components (overbroad after F2); it says the three-or-more-components case is open.
  - New block "referee-status table": rows for the new results are added to the status table near the top of LOOPY.md (where the K14 row P3.2′ sits), anchored at the T4.2(a) row.
- **Stale text elsewhere in LOOPY.md**: checked and left alone. Theorem 3.4 and Corollary 3.5 are stated for short G and stay true (Theorem 3.11 generalises them); the "What loopy kings do to the convention" bullets are consistent with Corollary 3.11a;
  line "G + dud is a draw for every G in which only running out of moves decides the game" (KNOWN) is unaffected; the "Results" table and the status table were the only places listing the loopy-sum claims, and both are updated.
- Mechanical check: `python3 kings/delegate/apply_edits.py kings/theory/LOOPY.md <out> kings/delegate/out/K21/EDITS_FINAL.md` reports 4 applied, 0 rejected.

### EDIT summary table: rows for the loopy sum theorems
<<<<<<< OLD
| C3.5 | Monotone chain: White wins with dud ⇒ with off ⇒ with nothing ⇒ with on | PROVED |
=======
| C3.5 | Monotone chain: White wins with dud ⇒ with off ⇒ with nothing ⇒ with on | PROVED |
| T3.7 | Loopy bridge: if the sum is first-event dominant for B (after every decisive event the frontier σB + rest is a forced σ-win whoever moves), the D-result of ⊞ y_i is the outcome, draws included, of the loopy CGT sum Σ y_i^B, at every reachable position; no shortness or stopper hypothesis | PROVED (new, K21, 2026-10-27; the K21 referee re-derived the proof step by step; brute force CHECKED-2 and COMPUTED-1) |
| T3.8 | Reserve criterion, the loopy form of T1.11(b): reserves λ_B, ρ_B (spare tempo needed to win second); if the reserves of the other components add up to ≤ B−1 at every event, the sum is dominant (with Lemma 3.8a, subadditivity, and Corollary 3.8b: one terminal-free component of finite reserves plus short pairwise safe components). Contains T1.11(b), strictly: `{∣⊕} ⊞ {⊖∣}` qualifies although its threats have opposite signs. The criterion is sufficient, not necessary; part (c) is necessity for dominance only, for one rest component | PROVED (new, K21, 2026-10-27; the K21 referee re-derived each proof step by step; revised after the K21 referee, 2026-10-27: (c) is necessity for dominance, not for D = CGT) |
| P3.9–P3.10 | Reserves (λ, ρ): on (0, ∞), off (∞, 0), over (0, 1), under (1, 0), dud (∞, ∞). One loopy stopper plus short components has no draws; dud and other non-stoppers do | PROVED (new, K21, 2026-10-27; re-derived by the K21 referee); the reserve table CHECKED-2 (two solvers), the draw counts COMPUTED-1 |
| T3.11 | Sandwich: for every D-game K and every group S whose terminal options are suicides, W(K⊞off) = W(K⊞dud) ⊆ W(K⊞S) ⊆ W(K⊞on) and L(K⊞on) = L(K⊞dud) ⊆ L(K⊞S) ⊆ L(K⊞off). A side that can force a decisive event against a passing opponent wins K ⊞ S for every such S (Corollary 3.11a) | PROVED (new, K21, 2026-10-27; the K21 referee re-derived the three parts step by step); the sampled states (K21: 142,798; referee: 6,150 instances) COMPUTED-1, 0 violations |
| P3.12 | For S ∈ {on, off, dud} the BIG/CGT translation of K ⊞ S is right exactly outside P_R (on), outside P_L (off), outside P_L ∪ P_R (dud): it is wrong exactly on the forced positions of the side the reservoir does not favour (of both sides for dud, where "right" is exactly the tempo regime). In general it can fail even in the tempo regime (3-node stopper, 2-node K) | PROVED (new, K21, 2026-10-27; revised after the K21 referee, 2026-10-27: the first draft said "right exactly in the tempo regime", which is false for on and off); the last claim CHECKED-2 (two solvers and a hand argument; two examples) |
>>>>>>> NEW

### EDIT sums with loopy components: new Section 3 block
<<<<<<< OLD
**What loopy kings do to the convention.**
=======
**Sums with loopy components (new, K21, 2026-10-27; revised after the K21 referee, 2026-10-27; answers part of §8 item 4).** Everything here is about D-games in the
sense of Definition 1.1, with loopy components allowed, the sum ⊞ of Definition 1.3 (the first decisive event ends the
whole play, infinite play is a draw) and the loopy CGT translation y^B, which is Definition 1.4 used verbatim for loopy components (Definition 1.4 states it for short
ones; ⊕ ↦ the chain +B, ⊖ ↦ −B; the translated components have no terminals, and Σ y_i^B is the ordinary disjunctive sum under normal play, with draws by
infinite play). First-event dominance (below) is Definition 1.10 restated for loopy components.
- *Labels (revised after the K21 referee, 2026-10-27).* The proofs of Theorem 3.7, Lemma 3.8a, Theorem 3.8, Corollary 3.8b, Propositions 3.9 and 3.10 and Theorem 3.11 are PROVED: each is one AI proof
  (K21), and the K21 referee re-derived every step against Definitions 1.1–1.4 and 1.10 and found no gap (`kings/delegate/out/K21/VERIFY.md`, section 1); Corollary 3.11a is immediate from Theorem 3.11 and
  the body of Proposition 3.12 follows from Theorems 3.3 and 3.4 (both PROVED). K21 did not write a REPORT.md; its experiments are in `summary.json`, `logs/` and `scripts/` of the same directory. The brute-force
  results are CHECKED-2 where two independent solvers agree (K21's `dsum.py` and the referee's from-scratch `verify/ref.py`: 20,324 states, 0 disagreements) and COMPUTED-1 otherwise (a count from one
  generator); the chess P-model counts are COMPUTED-1, because the referee could not re-run the oracle.
- *Conventions.* "σ wins at a position" means "σ forces a win in finitely many moves", i.e. the position is in the least
  fixed point W_σ of Definition 1.2; ρ(v) is its stage. W_L ∩ W_R = ∅ (KNOWN). "G + n" is G with n extra Left tokens (the
  integer n; only the number of unused tokens matters, and Right cannot touch them). "Left wins G + n second" means that
  (G + n, Right to move) ∈ W_L. For a component G, reach(G) is the set of nodes reachable from the root without passing a terminal;
  the reachable tuples of a sum are the product of the reach sets, since the coordinates move independently.
- A node has an *event of sign σ* if one of its options (by either player) is the terminal σ (a suicide counts, as in
  Definition 1.10). A *frontier position* of (Y′, j, σ), with Y′ a reachable tuple and an event of sign σ at y′_j, is
  σB + Σ_{i≠j} (y′_i)^B.
- Y is *first-event dominant for B* if every frontier position is a σ-win whoever moves first (for short components this is
  Definition 1.10).
- *Reserves.* For a node y and B ≥ 1: λ_B(y) is the least C ≥ 0 such that Left wins y^B + C second (Right moves first), and ρ_B(y)
  the least C ≥ 0 such that Right wins y^B − C second; ∞ if there is none. Λ_B(G) and P_B(G) are the maxima over reach(G).
- A component is a *stopper* if the graph on (node, mover) with edges (x, L) → (x^L, R), (x, R) → (x^R, L) has no cycle
  (no infinite alternating play from a reachable node). on, off, over, under are stoppers, dud is not.

**Theorem 3.7 (loopy bridge). PROVED** (new, K21, 2026-10-27; re-derived by the K21 referee). If Y is first-event dominant for B, then for every reachable tuple Y′ and both
movers the D-result of ⊞ y′_i equals the outcome of Σ (y′_i)^B (W, D or L). No shortness or stopper hypothesis.

*Proof.* Let 𝒟 be the D-graph on reachable tuples with a mover and 𝒞 the CGT graph. A D-option to a non-terminal is the same
move in 𝒞; a D-option to σ in coordinate j is the 𝒞-option to the frontier position (σB in coordinate j, the other mover to
move); 𝒞 has no other options, and a node has an option in 𝒟 iff it has one in 𝒞.
(⊆) By induction on the 𝒟-stage, W^𝒟_σ ⊆ W^𝒞_σ: a σ̄-node with no option has none in 𝒞. A σ-node with a σ-terminal option has the 𝒞-option
to a frontier position of sign σ, a σ-win by dominance; one with an option in W^𝒟_{σ,n} has the same option in 𝒞, in W^𝒞_σ by induction.
A σ̄-node of W^𝒟_σ has no σ̄-terminal option, and each other option is a σ-terminal (frontier, dominance) or in W^𝒟_σ (induction).
(⊇) By induction on the 𝒞-stage, for nodes of 𝒟. A σ-node with a winning 𝒞-option: if it is a frontier position, its sign is σ,
because a frontier of sign σ̄ is a σ̄-win by dominance and W_L ∩ W_R = ∅; so 𝒟 has the σ-terminal option. A σ̄-node all of whose 𝒞-options are in W^𝒞_σ has no
frontier option of sign σ̄ (same reason), so each 𝒟-option is σ's terminal or a node in W^𝒞_σ, hence in W^𝒟_σ. ∎

**Lemma 3.8a (subadditivity). PROVED** (new, K21, 2026-10-27; re-derived by the K21 referee). If Left wins G_1 + n_1 second and G_2 + n_2 second (any loopy normal-play games), Left wins
G_1 + G_2 + (n_1 + n_2) second; and if Left wins G + n second she wins G + m second for m ≥ n. So the reserve of a sum is at most the
sum of the reserves, for λ and for ρ.

*Proof.* In H_i = G_i + n_i Left follows a stage-lowering strategy of W_L. Let Φ = ρ_1 + ρ_2 at positions with Right to move.
Right moves in one component (not in tokens); Left answers in the same component with a stage-lowering move (a token or a G_i-move).
Φ drops by at least 2 per round, Left always has a reply, and when Φ = 0 Right is to move with no option anywhere and loses.
Extra tokens are never used and never hurt. ∎

**Theorem 3.8 (reserve criterion; the loopy Theorem 1.11(b)). PROVED** (new, K21, 2026-10-27; re-derived by the K21 referee). Let Y = (G_1, …, G_k), B ≥ 1. If for every j and every σ for which
some reachable node of G_j has an event of sign σ,

  Σ_{i≠j} Λ_B(G_i) ≤ B − 1 (σ = +),  Σ_{i≠j} P_B(G_i) ≤ B − 1 (σ = −),

then Y is first-event dominant for B, so by Theorem 3.7 the D-result of ⊞ is the CGT outcome of Σ y_i^B at every reachable position.
Moreover:
- (a) *Theorem 1.11(b) is the special case of short, pairwise safe components with B > max(M_L(Y), M_R(Y)).* For a short y with no
  ⊖ reachable, λ_B(y) ≤ M_R(y): y^B has no −B, Right makes at most M_R(y) moves in it (a move into +B counts as one, and the chain has
  no Right option), and Left answers each with a token. Pairwise safety (Definition 1.10) says that if + is a threat in G_j then no node of any
  other component has an option ⊖, so Σ_{i≠j} Λ_B(G_i) ≤ M_R(Y) ≤ B − 1; σ = − is symmetric.
- (b) *It is strictly stronger.* A = `{ ∣ ⊕}` (Right's only option is the suicide ⊕) and C = `{⊖ ∣ }` have threats of opposite sign
  (Definition 1.10 counts the suicides, so they are not pairwise safe), yet all four reserves are 0: Left has no move in A, so Right, moving
  second, wins A − 0 at once; Right has no move in C. The criterion holds for every B ≥ 1 and the D-result (L, W) is the outcome of `{ ∣ B} + {−B ∣ } = 0`.
- (c) *Necessity of the reserve condition for dominance, for one rest component (revised after the K21 referee, 2026-10-27).* If the rest of an event is a single component G with a reserve ∞
  opposite the event (e.g. `off` beside a ⊕ event), dominance fails for every B: it needs Left to win B + G^B second, i.e. λ_B(G) ≤ B. This is necessity for dominance only, not for D = CGT:
  `{⊖∣} ⊞ on` is not dominant (the event ⊖ has the rest `on`, with ρ = ∞), yet D = CGT = (W, W) for B = 2, 5, 9, because Right can never force the −B (Proposition 3.12). The referee's 9,592 random cases
  with an infinite reserve opposite an event: dominance failed in all (COMPUTED-1).

*Proof.* Let (Y′, j, +) be an event, R = Σ_{i≠j} (y′_i)^B and Λ = Σ_{i≠j} λ_B(y′_i) ≤ B − 1. By Lemma 3.8a Left wins R + Λ second, hence
R + (B − 1) and R + B second. The frontier position is B + R. If Right is to move, it cannot move in the stack B, so this is R + B second, a Left win.
If Left is to move, she plays B → B − 1 and wins R + (B − 1) second. The case σ = − is the mirror image with ρ_B. ∎

*Reading (the "value" of a loopy component). PROVED, from Theorem 3.8.* Under the criterion the D-result of the sum is the outcome of Σ y_i^B, so it is determined by the loopy-CGT class of each y_i^B (its equivalence class under
outcomes in all loopy contexts) and by the reserve data that certify the criterion. If y_i is a stopper, so is y_i^B (the chains are acyclic), and its class is Siegel's simplest form [S, ch. VI] (KNOWN, not re-derived here). For the reservoirs `on`, `off`, `dud`
opposite a threat that the threatening side can force, no B reproduces the D-result on the forced positions (Proposition 3.12); opposite a threat that cannot be forced (a suicide) the translation can
still be right although dominance fails (Theorem 3.8(c)) (revised after the K21 referee, 2026-10-27).

**Corollary 3.8b (one loopy component plus short components). PROVED from Theorem 3.8** (new, K21, 2026-10-27; re-derived by the K21 referee). Let S be a terminal-free component (stopper or not) with finite reserves at every reachable node, Λ(S) = max λ(y) < ∞ and P(S) = max ρ(y) < ∞
(for terminal-free S the reserves do not depend on B), and let K = (K_1, …, K_m) be short and pairwise safe (Definition 1.10). If B ≥ 1 + max(Λ(S), P(S)) + max(M_L(K), M_R(K)), the criterion holds, so the D-result of S ⊞ K is the outcome of S + Σ K_i^B
at every reachable position. *Proof.* All events are in K. For an event of sign + in K_j the rest is S together with the other K_i, and Λ(S) + Σ_{i≠j} Λ_B(K_i) ≤ Λ(S) + M_R(K) ≤ B − 1 by Theorem 3.8(a); σ = − is symmetric. ∎
It is the finite-reserve half of the "one stopper plus short components" case: S = over and S = under qualify (Proposition 3.9) and so does every stopper whose reserves are finite; `on` and `off` are not covered by the corollary as stated (ρ(on) = λ(off) = ∞) but satisfy Theorem 3.8 directly: S = on when K has no ⊖ event
(only the σ = + condition is needed, and Λ(on) = 0), S = off when it has no ⊕ event (the sign condition of Theorem 3.8 is what pairs the reservoir with the threats of the side it favours), with K pairwise safe and
B ≥ 1 + max(M_L(K), M_R(K)) (PROVED by the same proof; tested on 1,810 referee instances, 0 failures, COMPUTED-1). The other pairings are Theorem 3.4 and Proposition 3.12 (revised after the K21 referee, 2026-10-27). Most random stoppers do not qualify: 9,488 of the 12,610 random stopper-plus-safe-short instances had an infinite reserve.

**Proposition 3.9 (reserves of the named games). PROVED** (new, K21, 2026-10-27; re-derived by the K21 referee). (λ, ρ): on (0, ∞), off (∞, 0), over (0, 1), under (1, 0), dud (∞, ∞).

*Proof.* on: Right has no move, so Left wins second at once: λ = 0. Whatever Right's tokens, Left passes forever and Right runs out: Right never wins, ρ = ∞.
off is the mirror image. over: Right moves first (a pass or a token); Left plays ω → 0 and Right has no move: λ = 0. With no Right token Left moving first plays ω → 0
and wins; with one token Left's only move is ω → 0 (tokens are Right's), Right plays the token and Left is stuck: ρ = 1. under is the mirror image.
dud: Right can pass forever, so Left never forces a win; likewise Right: λ = ρ = ∞. ∎ (The same table was computed by K21's solver and by the referee's `ref.py`, B = 4: CHECKED-2. For over and under these are also Λ and P, the node 0 inside them having reserves (0, 0).)

**Proposition 3.10 (no draws beside a stopper). PROVED** (new, K21, 2026-10-27; re-derived by the K21 referee). If all components are short except one stopper S, every play of ⊞ is finite and the D-result is W or L.
*Proof.* A move in a short coordinate descends in a finite acyclic graph, so a play contains finitely many of them; after the last, all moves are in S and the movers
alternate, an infinite alternating play of S, which a stopper does not have. ∎ For dud (a non-stopper) `G ⊞ dud` is a draw when G has no terminal, `on ⊞ off` is a draw,
and a random non-stopper beside random short components has a draw in 1,315 of 3,335 instances (stoppers: 0 draws in 7,932 instances, 116,954 states; COMPUTED-1,
`run_tests.py stopper`; the referee's own generator: 0 draws in 1,277 stopper instances and a draw in 320 of 1,223 non-stopper instances, so the draw rate depends on the generator).

**Theorem 3.11 (sandwich). PROVED** (new, K21, 2026-10-27; re-derived by the K21 referee). Let K be any D-game (loopy allowed) and S a D-game none of whose options is a terminal of its own mover (no Left option ⊕, no Right
option ⊖; suicides are allowed, as for the deleted Z-moves of a frozen group; every terminal-free S qualifies, stopper or not). Then for every k, s and mover:

  (k, mover) ∈ W(K ⊞ off) ⇒ (k, s, mover) ∈ W(K ⊞ S) ⇒ (k, mover) ∈ W(K ⊞ on),
  (k, mover) ∈ L(K ⊞ on) ⇒ (k, s, mover) ∈ L(K ⊞ S) ⇒ (k, mover) ∈ L(K ⊞ off),

and W(K ⊞ off) = W(K ⊞ dud), L(K ⊞ on) = L(K ⊞ dud). Call P_L(K, mover) = "Left wins K ⊞ off" (Left can force a decisive event against a Right who may pass) and
P_R(K, mover) = "Right wins K ⊞ on". For short K these are the predicates Λ and Ρ of Theorem 3.4.

*Proof.* (1) Let σ be a stage-lowering Left strategy at (k, ω, mover) in K ⊞ off. In K ⊞ S Left keeps the virtual position (k, ω) in K ⊞ off. Off has no Left move, so σ prescribes
only K-moves and the terminal ⊕, which she plays for real. A real Right move in K is a virtual Right move; a real Right move in S is treated as the virtual pass ω → ω; a real
Right terminal is a suicide ⊕, or ⊖, which is not an option at a node of W_L. If Right has no real option it loses. The stage drops every round.
(2) Let σ be a stage-lowering Left strategy at (k, s, mover) in K ⊞ S. In K ⊞ on Left keeps a virtual S-position; when σ prescribes an S-move s̃ → s̃′ she passes ω → ω and updates s̃
(σ never prescribes a Left terminal in S, for S has none, nor a suicide). Right's real options are K-moves only, a subset of the virtual ones.
(3) Suppose (k, ω, L) enters W_L(K ⊞ dud) at stage n ≥ 1 through the Left pass to (k, ω, R). Then (k, ω, R) ∈ W_{L,n−1}, so all its options, Right's pass back to (k, ω, L) among them,
lie in W_{L,n−2}, and (k, ω, L) entered earlier: a contradiction. So by induction on the stage the Left pass is never needed, W_L(K ⊞ dud) ⊆ W_L(K ⊞ off), and the reverse inclusion
is clear. The L-statements are the mirror images. ∎

**Corollary 3.11a. PROVED** (new, K21, 2026-10-27; immediate from Theorem 3.11). P_L ∩ P_R = ∅. On P_L the D-result of K ⊞ S is W for every such S and every s, on P_R it is L. So whatever Z is, if one side can force a decisive event
against a passing opponent, that side wins; Theorem 3.4 and Corollary 3.5 are the cases S = on, off, dud. For K short and S a stopper (no draws, Proposition 3.10), S can matter only
in the *tempo regime* T = ¬(P_L ∪ P_R): outside T the result does not depend on S. (The inclusions W(K ⊞ S) ⊆ ¬P_R and L(K ⊞ S) ⊆ ¬P_L hold everywhere and are Theorem 3.11 itself; they say nothing inside T.
Revised after the K21 referee, 2026-10-27.)

**Proposition 3.12 (where the translation is right for the pure reservoirs). PROVED** (new, K21, 2026-10-27; revised after the K21 referee, 2026-10-27). Let K be short.
- K^B + on ∈ 𝓛, so the translation says W at both movers and is right at (K, mover) iff (K, mover) ∉ P_R (Theorem 3.4(b)); on P_L, where Left forces, D = W as well.
- K^B + off ∈ 𝓡, so the translation says L and is right iff ∉ P_L.
- K^B + dud is a draw (Left can pass forever, so Right never wins, and conversely), right iff ∉ P_L ∪ P_R (Theorem 3.4(a)).
So the translation is right exactly outside P_R for `on`, outside P_L for `off` and in the tempo regime T for `dud`; it is wrong exactly on the forced positions of the side that the reservoir
does not favour (of both sides for `dud`). Theorem 3.4, not Theorem 1.11, is the sum theorem for them. *Proof.* Theorem 3.3(a) and its mirror for the first two; for dud, Left can pass forever. ∎
(Revised after the K21 referee, 2026-10-27: the first draft said "right in the tempo regime, wrong on the forced positions of the side the reservoir favours", which is false for `on` and `off`.
Referee check, 53,838 (K, mover, reservoir) cases with the statement as now written: 0 violations, COMPUTED-1.)

**What fails (revised after the K21 referee, 2026-10-27). The named examples are CHECKED-2 at the root (K21's solver and the referee's `ref.py` agree, B = 2, 5, 9 unless stated); the statistics are COMPUTED-1
(`kings/delegate/out/K21/logs/examples.txt`, `kings/delegate/out/K21/VERIFY.md` section 2); results are (Left first, Right first).**
- *An infinite reserve opposite a threat that the threatening side can force kills every B.* `{⊕∣} ⊞ off`: D-result (W, W), CGT outcome (L, L) for B = 2, 5, 9. `{⊕∣} ⊞ dud`: D (W, W), CGT (D, D). `{∣⊖} ⊞ on`: D (L, L),
  CGT (W, W). The favourable pairs are right: `{⊕∣} ⊞ on` and `⊞ over` are (W, W) in both; `{∣⊖} ⊞ off`, `⊞ over`, `⊞ under` are (L, L) in both.
- *A threat that cannot be forced does not.* If the only event is a suicide (Left's own ⊖ in `{⊖∣}`, Right's own ⊕ in `{∣⊕}`), the other side never has to allow it and the translation can be right although
  dominance and the criterion of Theorem 3.8 fail: `{⊖∣} ⊞ on` D = CGT = (W, W); `{∣⊕} ⊞ off` D = CGT = (L, L); `{⊖∣} ⊞ dud` and `{∣⊕} ⊞ dud` D = CGT = (D, D) (B = 2, 5, 9; referee, `verify/ex2.py`). The reserve
  criterion is therefore not necessary for D = CGT (see also the last bullet).
- *Non-stoppers.* Theorem 3.7 holds verbatim, and so does Theorem 3.8 with finite reserves: S = {S, 0 ∣ S} (not a stopper, λ = 0 at both nodes) beside `{⊕∣}` is dominant and D = CGT = (W, W). What is lost is
  Proposition 3.10 (draws) and the compatibility of dud (λ = ρ = ∞) with a threat of either sign.
- *The tempo-regime guess is false for general stoppers (the guess is refuted).* "For K short and S a terminal-free stopper, outside P_L ∪ P_R the translation K^B + S gives the D-result."
  It fails in 60 of the 28,581 sampled tempo-regime states in which the criterion of Theorem 3.8 is violated (S = random stopper 39, short 7, arbitrary loopy 7, under 4, over 3; never for on, off, dud: 8,646 tempo-regime states;
  the failures with a short, over or under S come from a K whose own components violate the criterion), and in none of the 40,380 states (all regimes) in which the criterion holds. Smallest counterexample, 2 + 3 nodes, B = 3, 14, 40 alike: K = `{1 ∣ ⊖, 1}` with node 1 = 0 (Left's only move is to 0; Right may
  play ⊖, a Black win, or move to 0); S has nodes a, b, c with a: Left → c, Right → b, c; b: Right → a, b; c: Left → b, c (c is on-like, b off-like; S is a stopper).
  At (K, a), Left to move, K ⊞ off is lost and K ⊞ on is won for Left, so it is in T. The D-result is **L**: K → 0 lets Right play a → b and Left is stuck; a → c lets Right play ⊖.
  The translation says **W**: after a → c Right's ⊖ becomes −B and Left passes forever in c. (ρ_B(S) = ∞.) CHECKED-2 (K21's solver, the referee's `ref.py` for B = 1, 2, 3, 14, 40, and this hand argument).
  A second, independent counterexample (found by the referee's random search): K = `{⊕, 0 ∣ 0}` (nodes k and 0; Left may play ⊕ or move to 0, Right may only move to 0), S = `{0 ∣ off}` (nodes s, 0 and off, a stopper). At the
  root with Right to move K ⊞ on is (W, W) and K ⊞ off is (W, L), so Right-first is in T; the D-result is **W**, the translation gives **L**, for B = 1, 2, 5, 14. Hand check: Right's K → 0 loses to Left's S → 0 (Right is stuck);
  Right's S → off lets Left play ⊕ at once, a White win in the D-game; in the translation that ⊕ is the stack +B, Right passes forever in `off` and Left runs out of moves. CHECKED-2.
  Statistics (COMPUTED-1): the referee's generator is not K21's and does not reproduce the 60 of 28,581 bit for bit, but it reproduces the content: 1 failure in 6,882 tempo-regime states with the criterion violated and 0 in 3,594
  with it true.
- *The criterion is not necessary.* `{∣⊕, 0}` ⊞ `{⊖, 0 ∣ 0}` (each with a self-loop at its only node; the first is off-like with a Right suicide, the second dud-like with a Left suicide) is dominant at B = 5 and D = CGT = (D, D),
  although the criterion fails: λ_5 of the second component is exactly B = 5 (Left stops Right's passes only by her suicide to −B), and the criterion asks for ≤ B − 1 (22 cases of this kind among the 4,693 dominant
  loopy cases, `run_tests.py bridge`; this example from `search_incomplete.py`; the referee confirms D = CGT = (D, D) for B = 3, 5, 7, dominance true, criterion false, λ_5 of the second component exactly 5; CHECKED-2).

**Computations (revised after the K21 referee, 2026-10-27; COMPUTED-1 for the experiments, CHECKED-2 where two independent solvers agree, as marked).** Code: `kings/delegate/out/K21/scripts/` (`dsum.py`, `run_tests.py`, `sumsolve.c`, `crosscheck.py`, `run_all.sh`, `summarize.py`);
logs and `summary.json` one level up; the referee's independent code and logs are in `kings/delegate/out/K21/verify/` (`ref.py`, `xcheck.py`, `tests1.py`, `exh.py`, `ex.py`, `ex2.py`, `logs_bridge.txt`). Python: `PYTHONPATH=… .venv/bin/python`, `KRICH=1` for the richer generator. Random components: short DAGs (≤ 4 or 5 nodes, ≤ 2 or 3 options per side, both signs of terminal
options), random loopy components with terminals (≤ 3 nodes), on, off, over, under, dud, random stoppers (≤ 4 or 5 nodes); 2 or 3 components.
- *Solver cross-check:* Python (explicit reachable product, counter-based least fixed point) against `sumsolve.c` (dense product, naive iteration, its own translation) on the root tuple, both movers, D-result and CGT outcome:
  0 disagreements on 6,000 instances (`crosscheck.py 6000 801 5`; 3,000 more with seed 7); 1,169 have D ≠ CGT, 1,468 a draw. With `K21_ALL=1` the C program prints the D-result and the CGT outcome at *every* tuple of original nodes and `crosscheck.py` compares them with the Python
  results at every reachable tuple, both movers: 47,896 states (`K21_ALL=1 crosscheck.py 1500 77 5` and `4000 78 5`, KRICH=1 for the second), 0 disagreements. These all-states samples contain no instance with D ≠ CGT and no draw (`summary.json`, `crosscheck`), so they test only the agreeing regime; the differing regime is covered by the root cross-checks (1,169 and 557 instances with D ≠ CGT)
  and by the referee's run. *Referee:* a third, independent solver (`verify/ref.py`, written from the definitions) agrees with `dsum.py` on 1,500 random instances (2 or 3 components of up to 4 nodes, loopy or short, with terminals, B in {1, 2, 4, 6}):
  D-result and CGT outcome at every reachable tuple and both movers, 20,324 states, 0 disagreements, and dominance and the reserve criterion on all 1,500 instances: CHECKED-2. K21's own dominance, reserve and regime statistics use the Python solver only (COMPUTED-1).
- *Theorems 3.7, 3.8:* `run_tests.py bridge 6000 {101,102,103} 5` and `bridge 4000 {111,112} 7`: 26,000 instances, D = CGT compared at all reachable tuples and both movers. 4,693 non-vacuous loopy cases with dominance
  (4,671 with the criterion): 0 violations; criterion ⇒ dominance ⇒ equality, 0 violations; where dominance fails, D ≠ CGT in 6,898 + 1,115 instances (by accident equal in 2,123 + 667).
- *Theorem 3.8(a):* `thm111b 6000 {901,902,903}`: 5,537 pairwise safe (Definition 1.10) short instances with B = max(M_L(Y), M_R(Y)) + 1, 5,127 of them with events: the criterion, dominance and D = CGT at every reachable tuple hold in all, 0 failures.
- *Corollary 3.8b:* `onestopper 6000 {1101,1102,1103}`: 3,122 instances (2,625 with events) with a random terminal-free stopper S of finite reserves (or over, under) beside 1-2 pairwise safe short components, B as in the corollary: the criterion holds and D = CGT at every reachable position in all, 0 failures (9,488 further instances skipped because S had an infinite reserve).
- *Proposition 3.12:* `pure 4000 {1001,1002} (B = 14)`: 189,072 (K, mover, reservoir) checks, translation right exactly as stated: 0 violations.
- *Lemma 3.8a:* `subadd 3000 {501,502} 5`: 5,682 checks, 0 violations.
- *Theorem 3.4 predicates:* `thm34 8000 {601,602}`: 225,312 (position, mover, reservoir) checks, 0 violations. *Proposition 4.6:* `over46 8000 701`: 20,628 checks, 0 violations.
- *Theorem 3.11:* `sandwich 5000 {201,202,203}`: 15,000 instances, 142,798 states (K one or two components, short or loopy with terminals; S named, quiet short, stopper, quiet loopy, loopy with suicide-only terminals, 38,020
  states of the last kind): 0 violations of the four inclusions and of W(off) = W(dud), L(on) = L(dud).
- *The K21 referee's independent runs (own generator, own solver; COMPUTED-1, all 0 violations).* Theorem 3.7 (dominance ⇒ D = CGT at every reachable tuple, both movers; criterion ⇒ dominance): 10,000 random instances (1,778 dominant, 1,646 with the criterion), and exhaustively all
  2,080 pairs of one-node components with options in {self-loop, ⊕, ⊖} (268 non-vacuous dominant, 49 dominant without the criterion), 2 × 3,000 one-node × random two-node, 1,200 random triples of one-node components. Theorem 3.8(a): 641 safe instances. Corollary 3.8b: 721 instances
  (591 with events). Lemma 3.8a: 1,600 checks. Theorem 3.11: 6,150 instances. Proposition 3.12: 53,838 checks. Proposition 3.10: 1,277 stopper instances, no draw.
- *Corollary 3.11a and the translation:* `regime 4000 {401,402,403} 14`: 102,883 states with (K, mover) ∈ P_L ∪ P_R, D-result = forced result in all of them; 40,380 states with the criterion true, D = CGT in all.

**Chess instances with a shuttle beside small contexts (COMPUTED-1, P model; `scripts/chess_pred.py`, `chess/`; the oracle was not re-run by the referee, see the last-but-one bullet).** Z_onT1 = `Ka5 Pb4 Pc5 kc6 pb5` on cyl:7x6 is `on_D` (Proposition 3.2, §5.4); a pawn context on the e and f files is turned
into a D-game (positions = pawn configurations with e.p. as in `cylcgt`, decisive events = a passer, races by the "count" rule, as in `lemmas/common.py`), and the prediction is the solver's D-result of K ⊞ on_D, which is
Theorem 3.4(b) and, for the forced positions, Theorem 3.11. 18 contexts of 1-5 pawns (for each predicted class (W,W), (W,L), (L,L): the four smallest and two mid-size contexts found among 6,000 random placements, plus the P9 context `Pe2 pf3` as a control)
and 6 colour-reversed contexts with Z_offT1 = `Kc1 Pb2 ka2 pb3 pc2` (prediction from the `off_D` model). Oracle: the P-model solver (first promotion wins, real kings) built privately from K7's `kp_p.c`
(`--board cyl:7x6 --pmodel --ep on --promote Q --cap 0`, 24 s for all 48 positions).
- **21 of 24 agree**: 6/6 Z_off contexts; for Z_on, 6/6 in (W,W), 5/6 in (L,L), 4/6 in (W,L); P9 `Pe2 pf3` gives (W, L) as in P9.
- The 3 disagreements are (V1a)/(V2) failures on this narrow board (the seam makes the e-file 2-3 king steps from the a-file), not failures of the sum theory:
  (i) `Pe2 pe3 pf4`, predicted (L,L), P-model (W,L): White's king sortie Ka5-g4 (not a shuttle move) wins, so P is better for White than D, as Proposition 3.2 allows (r(G ⊞ Z) ≥ r(G ⊞ on_D));
  (ii) `Pe4 pf5`, predicted (W,L), P-model (W,W): after Black's capture f5xe4 the new Black passer is caught by Ka5-g4 (`Ka5 Pb4 Pc5 kc6 pb5 pe4 w` is a White win in P), so Black's decisive event is not a P-win ((V2));
  (iii) `Pe2 Pe3 pe4 pf3 pf4`, predicted (W,L), P-model (L,L): every White move loses; White's capture e3xf4 creates a passer that the D-model scores as a win, but Black's f3xe2 and e1=Q is a faster counter-promotion (a race, (V2)).
- **80 further random contexts** (`chess_rand.py gen 80 31337`, 1-4 pawns on e, f; same oracle, 27 s): 64 of 80 agree. Over all 98 Z_on contexts, 79 agree; 13 differ in White's favour (the P-result is at least the prediction, as the inequality
  r(G ⊞ Z) ≥ r(G ⊞ on_D) of Proposition 3.2 allows: White's non-shuttle king moves); 5 are draws where the D-model predicts a decision (the stalemate mechanism, (V1b); `Pe4 pe5` is one: e4 covers d5 and pe5 is blocked, so Black has no legal move;
  the other four were not diagnosed); 1 is worse for White than predicted ((iii) above, a race, (V2)). Direction table: `logs/chess_direction.txt`.
- Reproduce: `scripts/chess_pred.py gen` (writes `chess/positions_all.txt`-compatible files and `chess/pred.json`), then
  `cc -O2 -o bin/kp_p kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread; bin/kp_p --board cyl:7x6 --pmodel --ep on --promote Q --cap 0 < chess/positions_all.txt` and compare with `chess/pred.json`.
- **Referee status (revised after the K21 referee, 2026-10-27).** The P-model oracle was *not re-run*: the referee built `kp_p` and queued a 12-position sample, but both shared heavy-job slots were held by other jobs for 25 minutes and the run was withdrawn. What was checked:
  the counts above were recounted from K21's own result files (`verify/count_chess.py`: 24 base contexts, 21 agree; 80 random contexts, 64 agree; 79 of 98 Z_on contexts agree; 13 + 5 + 1 differences as listed), and the prediction side was re-derived by hand
  for `Pe2 pf3` ((W, L)), `Pe2 pe3` ((W, W)) and `Pe4 pf5` (predicted (W, L), P-model (W, W)), and the `Pe4 pe5` stalemate explanation is right. So the P-model results stay COMPUTED-1 (one run, not re-run); nothing in the chess part is CHECKED-2.
- **kpsolve (C, cap 1): not obtained.** One cap-1 position (`Ka5 Pb4 Pc5 kc6 pb5 Pe2 pf3 w -`) used more than 55 CPU-seconds when run alone outside the lock (killed at the limit), and a batch of 4 contexts (8 positions, `chess/positions_C.txt`) waited in the
  shared heavy-job queue (both slots held by other kings/ jobs for the whole session) and was withdrawn. So the new contexts are P-model results (the Z_on claims of §5.4 are "PROVED in P"; the chess claim needs (A_Q) at each position), and the only kpsolve (C) value
  for a context here is the one already recorded for P9. Reproduce when the lock is free: `kings/delegate/heavy.sh bin/kp --board cyl:7x6 --ep on --promote QRBN --cap 1 --threads 2 < chess/positions_C.txt`.

**What loopy kings do to the convention.**
>>>>>>> NEW

### EDIT section 8 item 4: status
<<<<<<< OLD
4. A version of Theorem 1.11 for loopy components: the D-semantics analogue of Siegel's stopper sums.
=======
4. A version of Theorem 1.11 for loopy components: the D-semantics analogue of Siegel's stopper sums. **Answered in part (K21, §3 after Corollary 3.5; revised after the K21 referee, 2026-10-27).**
   - PROVED (one AI proof each, re-derived step by step by the K21 referee): the bridge to the loopy CGT sum under dominance (Theorem 3.7), a reserve criterion that contains Theorem 1.11(b) and is strictly stronger (Theorem 3.8), the reserves of
     on, off, over, under, dud (Proposition 3.9), no draws beside one stopper (Proposition 3.10), and the sandwich theorem, which makes the forced-event regime independent of the group (Theorem 3.11, Corollary 3.11a).
   - What fails (examples CHECKED-2, statistics COMPUTED-1): an infinite reserve opposite a threat that the threatening side can force (on or off against the wrong sign, dud against both) makes the translation wrong for every B on the forced
     positions (Proposition 3.12); an unforceable threat (a suicide) does not, although dominance still fails (Theorem 3.8(c)); dud and other non-stoppers draw; and the translation can be wrong even in the tempo regime for a stopper with an
     infinite reserve (two examples with 3-node stoppers, §3, "What fails").
   - OPEN: (a) the exact value of a stopper with an infinite reserve in the tempo regime (what replaces the CGT value); (b) a necessary and sufficient form of Theorem 3.8 (the criterion is sufficient, not necessary, and Theorem 3.8(c) is necessity
     for dominance only, for one rest component; for three or more components the sum of the reserves at an event is open); (c) a theorem for two or more loopy stoppers (their sum need not be a stopper: on ⊞ off draws); (d) the relation between (λ, ρ) and
     Siegel's stops (CONJECTURE, untested: λ(S) = ⌈−RS(S)⌉ or one more, for a terminal-free stopper with finite reserve).
>>>>>>> NEW

### EDIT referee-status table: rows for the loopy sum results
<<<<<<< OLD
| T4.2(a) | PROVED after repair (through the corrected T1.11(b)) | R4 item 3 |
=======
| T3.7, L3.8a, T3.8, C3.8b (loopy sums) | PROVED (new, K21, 2026-10-27): one AI proof each; the K21 referee re-derived every step against Definitions 1.1–1.4 and 1.10. T3.8(c) is necessity for dominance only, not for D = CGT (revised after the K21 referee, 2026-10-27). Brute force: CHECKED-2 (two solvers, 20,324 states), the statistics COMPUTED-1 (K21: 26,000 bridge instances; referee: 10,000 random and 2,080 exhaustive pairs, 0 violations) | K21 referee (`kings/delegate/out/K21/VERIFY.md` sections 1 and 3), `kings/delegate/out/K21/summary.json` |
| P3.9, P3.10 | PROVED (new, K21, 2026-10-27; re-derived by the K21 referee); the reserve table CHECKED-2, the draw counts COMPUTED-1 | K21 referee |
| T3.11, C3.11a | PROVED (new, K21, 2026-10-27; the three parts re-derived by the K21 referee); 142,798 + 6,150 sampled instances, 0 violations, COMPUTED-1 | K21 referee |
| P3.12 | Body PROVED (new, K21, 2026-10-27). The first draft's wording, "right exactly in the tempo regime" for on and off, was REFUTED by the K21 referee and is corrected: right exactly outside P_R (on), P_L (off), P_L ∪ P_R (dud). The claim that the translation can fail in the tempo regime: CHECKED-2 (two examples, two solvers, hand-checked). The "no translation" claims were narrowed to forcible threats | K21 referee, fixes F1 to F4 |
| T4.2(a) | PROVED after repair (through the corrected T1.11(b)) | R4 item 3 |
>>>>>>> NEW
