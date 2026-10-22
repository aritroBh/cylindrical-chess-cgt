> **Erratum (2026-10-22, orchestrator).** The claim below that the P2.10(b) example `W (f,H-2); B (f,H-1),
> (f+1,H-1)` is a terminal context is wrong. For Black, "ahead" means lower ranks, and White's pawn on (f, H-2)
> stands ahead of both black pawns on files f and f+1. `cylcgt.pawns.passed` finds no passed pawn for either side
> at H = 6, 7, 8 (T30 audit, `notes/proof_audit2/REPORT.md`, confirmed by its verifier). P2.10(b) has no gap on
> this point.

# Second-Model Re-Derivation of Proofs

*Task T2 (qwen) — verification of proofs from `notes/lemmas.md` and `kings/theory/LOOPY.md`*

---

## Part I: Statements from `notes/lemmas.md`

---

### L1.6 — Theorem 1.6: Disjunctive Decomposition of the Pure Game Under Condition (E)

#### Precise Restatement

Let X be a pawn position with components X₁, …, Xₖ (k ≥ 2) on a board B = (n, m, κ, ε). Assume **condition (E)**: either en passant is off (ε = off), or no position Y reachable from X that has two or more components carries a *usable* en-passant right (a right is usable iff the entitled side has an en-passant capture available). Then the pure game P(X) equals the disjunctive sum P(X₁) + … + P(Xₖ).

#### Re-Derivation

1. **Components never merge.** By Lemma 1.1 (empty file stays empty), Occ(Y) ⊆ Occ(X) for every move X → Y. A capture removes one pawn but the capturer remains on the target file, so every component retains at least one pawn. Hence every reachable Y has at least k components.

2. **Moves are local to components.** By Lemma 1.2(a), a move of a pawn on file f changes only squares on {f} ∪ N(f). Since the target file of a capture or e.p. capture holds an enemy pawn, it lies in the same component as the capturer. Thus every White move in Y corresponds to a White move in exactly one component Y|Kᵢ, leaving all other components unchanged.

3. **En-passant rights live in their component.** The e.p. right e = (t, c, s) has target t on some file. That file is adjacent to the double-stepping pawn's file, so t and c are in the same component. When a move is made in component Kᵢ ≠ Kⱼ (where the right lives), the global rules delete the right. In the sum model, the right remains inside P(Y|Kⱼ). The difference matters only if the right is *usable* in Y|Kⱼ.

4. **Condition (E) eliminates the difference.** By (E), any right in a multi-component position is not usable. A non-usable right means the entitled side has no e.p. capture available. Since children never inherit rights, Y|Kⱼ with and without the right have exactly the same options. Hence their P-values are equal by induction on Φ(Y).

5. **Induction on Φ.** Base: terminal positions (which have no moves) trivially satisfy the sum. Inductive step: the options of P(Y) and Σᵢ P(Y|Kᵢ) correspond one-to-one with equal values. Therefore P(Y) = Σᵢ P(Y|Kᵢ).

#### Steps Not Fully Justified

- **Step 3 (rights assignment):** "The right goes with the component that contains the file of its target" (Definition 1.3). This is a design choice in `cylcgt`. Could a right straddle components? No: the target file and the captured pawn's file are adjacent, so they are in the same connected component of the occupancy graph.

- **Step 4 (non-usable ⇒ equal values):** The claim "Y|Kⱼ with and without the right have the same options" relies on the fact that only e.p. captures depend on the right. But does the *presence* of a right (even if not immediately usable) affect the opponent's move generation? In `cylcgt.pawns.moves`, the opponent's moves are generated with the right *deleted* (because the right expires when the opponent moves). If the right is not usable, the side that owns it has no e.p. capture now; the opponent's moves are unaffected by whether the right is kept or deleted. So the game trees are identical.

#### Verdict: **VALID**

The proof is sound. The condition (E) is exactly what is needed to make the sum decomposition work for the pure game P. The counterexample in Proposition 1.7 shows (E) is necessary.

---

### L2.1 — Theorem 2.1: Outcome Faithfulness of ±BIG for Hereditarily Sum-Safe (HSS) Positions

#### Precise Restatement

Let X be a non-terminal pawn position that is **hereditarily sum-safe (HSS)** (every reachable position, including X, is pairwise safe: no two different components carry opposite-sign threats). Assume condition (E) from L1.6, and BIG > max(M_W(X), M_B(X)) where M_W, M_B are the maximum move counts for each side. Then the outcome class of the sum model S(X) equals the outcome of the whole-board convention game W(X), which equals the alternating-play winner of the convention game.

#### Re-Derivation

The proof constructs a game form F for S(X):
- Positions of F are pairs (Y, N) where Y is the set of live components and N is a multiset of frozen integers ±BIG.
- A move is either a move in an integer summand, or a pawn move in a live component Z.
- If a pawn move creates a σ-passer (or a race scored σ), Z leaves Y and ±BIG joins N.

**Step 1: Frontier lemma.** If (Y, {σBIG}) has no live component with a (−σ)-threat and BIG > M_{−σ}(Y), then σ wins F(Y, {σBIG}) whoever moves first.
- σ's strategy: move in the integer summand every turn (BIG → BIG−1 → …).
- The opponent cannot move in a positive integer.
- Opponent's moves are all in live components, at most M_{−σ}(Y) of them.
- Since BIG > M_{−σ}(Y), σ has enough "spare moves" to outlast the opponent.

**Step 2: Induction on Φ(Y).** Prove o(F(Y, ∅)) = o(W(Y)) for all reachable Y.
- If a move in component Z leads to a non-terminal child, both models give the child; induction applies.
- If the move creates a σ-passer or a σ-scored race:
  - W gives σBIG (a 𝓛 or 𝓡 game), which σ wins.
  - F gives (Y'', {σBIG}) where Y'' are the other components.
  - Because Y is HSS (pairwise safe), no other component has a (−σ)-threat.
  - Since M(Y'') ≤ M(X) < BIG, Step 1 applies: σ wins this option too.
- Race scores agree because passedness is local (Lemma 1.2(c)) and promotion distances are the same in both models.

**Step 3: Outcomes match.** Since options correspond with same outcomes, o(F(Y,∅)) = o(W(Y)). By Lemma 0.1, o(W) equals the alternating-play winner.

#### Steps Not Fully Justified

- **Step 1 (frontier strategy):** The strategy "move in the integer every turn" assumes σ can always move in an integer summand. But what if all integer summands are exhausted (k = 0)? The lemma assumes {σBIG} is present, so k ≥ 1 initially. σ's moves reduce k by 1 each turn. The opponent makes at most M_{−σ}(Y) moves total. Since BIG ≥ M_{−σ}(Y) + 1, σ will still have k ≥ 1 when the opponent runs out. This holds.

- **Step 2 (no (−σ)-threat in other components):** Pairwise safety says no *reachable* position has opposite threats in different components. But the induction is on positions reachable from X. Since Y is reachable from X and HSS, Y is pairwise safe. The move is in Z, which has σ ∈ τ(Z). Could another component develop a (−σ)-threat *after* the move? The child position Y'' is reachable from Y, so by monotonicity of τ (τ(Y'') ⊆ τ(Y)), it cannot gain a new threat. So no (−σ)-threat appears.

- **Race scoring agreement:** The proof says "before the move Y had no passer, a move changes one component, and passedness is local. So all passers of the child lie in Z." This is correct because a passer requires no enemy pawn on adjacent files ahead. A move in Z can only affect passedness on files in Z ∪ N(Z). Since components are separated by at least one empty file, no other component's passedness changes.

#### Verdict: **VALID**

The proof is rigorous. The HSS condition (pairwise safety at all reachable nodes) is exactly what prevents the +BIG/−BIG cancellation that breaks `sum_safe()` (Counterexample 2.2). The bound BIG > M is mild (BIG = 256, M ≤ 48 for 8×8).

---

### L2.3 — Theorem 2.3: No Split ⇒ S = W as Canonical Games

#### Precise Restatement

Suppose no non-terminal position reachable from X has two or more components. Then S(X) = W(X) as canonical games, for every race rule.

#### Re-Derivation

1. For any such position Y (including X), `pawns.value` takes the single-component branch.
2. In that branch, `_value` and `_child` apply:
   - The same terminal test (passer check)
   - The same race scoring function
   - The same e.p. right stripping (deleting the opponent's right when generating moves)
3. The recursion is identical to the definition of W(Y).
4. By induction on Φ(Y), S(Y) = W(Y) for all reachable Y, hence S(X) = W(X).

#### Steps Not Fully Justified

- **"The same e.p. right stripping":** In W, White's options are generated from X with Black's right deleted. In S's single-component branch, the code does the same. This is a code-level coincidence, not a mathematical necessity. But since both are defined to model the same convention, it holds by construction.

- **No splitter positions:** The hypothesis "no reachable non-terminal position has ≥2 components" is a strong syntactic condition. The proof doesn't explain *why* this holds for the *2 candidate — it just verifies it by enumeration (1,075 positions with e.p. on, none split). This is a computational check, not a structural proof. But the theorem statement is conditional: *if* no split occurs, *then* S=W.

#### Verdict: **VALID**

The proof is trivial by induction once the hypothesis is granted. The hypothesis is verified computationally for the *2 candidate. No logical gap.

---

### L3.3 — Theorem 3.3: Freeze Lemma (Convention)

#### Precise Restatement

For every non-terminal pawn configuration Y:
- (a) o(WF(Y)) = o(W(Y)), where WF adds king-move options −BIG (Left) and +BIG (Right).
- (b) If every non-terminal Y' reachable from Y is *BIG-interior* (−BIG ⧏ W(Y') ⧏ BIG), then WF(Y) = W(Y) as canonical games.

#### Re-Derivation

**(a) Outcome equality.**
- Induction on Φ(Y).
- Extra Left option: −BIG. This is a Right win (𝓡) whoever starts. So it never creates a new Left win.
- If Left has no pawn move, in W Left loses (no move). In WF Left's only move is to −BIG, which is also a loss. So "Left wins moving first" is unchanged.
- Extra Right option +BIG is symmetric (𝓛).
- All other options agree by induction.
- Therefore o(WF(Y)) = o(W(Y)).

**(b) Value equality under BIG-interior.**
- Induction. Terminals agree.
- At non-terminal Y', WF(Y') = {W(Y'ᴸ), −BIG | W(Y'ᴿ), BIG} by induction.
- By Lemma 3.2 (gift-horse principle): {Gᴸ, X | Gᴿ} = G iff X ⧏ G.
- Since −BIG ⧏ W(Y') and W(Y') ⧏ BIG, both −BIG and +BIG are reversible and can be deleted, leaving W(Y').

#### Steps Not Fully Justified

- **Lemma 3.2 (gift-horse) application:** The lemma states {Gᴸ, K_L | Gᴿ, K_R} = G if K_L has Right option −BIG ≤ G' and K_R has Left option +BIG ≥ H. The proof uses reversibility: K_R is reversible in H = {Gᴸ | Gᴿ, K_R} because BIG ≥ H. But this requires H ≤ BIG, which is true since H ≤ G ≤ BIG. Similarly K_L is reversible in G' because −BIG ≤ G'. This chain holds.

- **BIG-interior condition:** The condition is −BIG ⧏ W(Y') ⧏ BIG, i.e., W(Y') is strictly between −BIG and BIG in the Conway order. This is exactly what makes −BIG a "bad" Left option (reversible) and +BIG a "bad" Right option. The proof correctly identifies this.

- **"WF ≠ W in 94 of 400 random positions, all violating BIG-interior":** This is empirical confirmation, not part of the proof. The proof stands independently.

#### Verdict: **VALID**

The proof correctly uses the gift-horse principle (reversibility) from CGT. Part (a) is a simple outcome induction; part (b) adds the value equality under the BIG-interior condition. Both are sound.

---

### L5.1 — Lemma 5.1 & Theorems 5.2–5.3: Dawson Ring Reduction (R_n = mex{G(n−3)})

#### Precise Restatement

**Lemma 5.1 (Macro-move):** On the full 3×n ring R_n (n ≥ 3), every first move (a push on file f) forces a unique 5-ply capture sequence after which:
- Files f−1 and f+1 are empty.
- File f holds a blocked pair (W on rank 2, B on rank 3 if White moved first).
- All other files are untouched.
- The opponent of the first mover has no capture and is to move.

**Theorem 5.2 (Ring opens to strip):** The position after the macro-move is the flat strip D_{n−3} (files f+2 … f−2) plus an inert file, with the opponent to move.

**Theorem 5.3 (Grundy value):** Let G be the Grundy function of octal 0.137 (Dawson's Kayles). Then:
- Alternating play on R_n is a first-player win iff G(n−3) = 0.
- In the macro-move model, R_n has Grundy value mex{G(n−3)} (1 if G(n−3)=0, else 0).

#### Re-Derivation

**Lemma 5.1:**
- After White pushes f1→f2, the only captures available are on (f,2) by Black pawns on f−1 and f+1 (rank 3). Captures are compulsory.
- Ply 2: Black captures with one neighbour, say (f−1,3)×(f,2). Now White pawn on (f,2), Black pawn removed from f−1.
- Ply 3: White must recapture on (f,2) with its remaining neighbour (f+1,1) or (f−1,1) — but f−1 is now empty, so only (f+1,1) works. White captures, landing on (f,2).
- Ply 4: Black captures with its last neighbour (f+1,3)×(f,2).
- Ply 5: White captures with its last neighbour (f−1,1)×(f,2) — wait, (f−1,1) was not used yet? Actually after ply 2, White's pawn on f−1 is still there. Let me trace carefully:

Initial: White on rank 1 all files, Black on rank 3 all files.
White pushes f:1→2.
Black captures: options (f−1,3)×(f,2) or (f+1,3)×(f,2). Say (f−1,3).
Now: White has pawns on all rank 1 except f−1 (capturer moved), plus White on (f,2). Black has pawns on all rank 3 except f−1.
White recaptures: must capture on (f,2). Attackers: White pawns on (f−1,1) and (f+1,1). (f−1,1) is still there! So White can use (f−1,1) or (f+1,1). Say (f−1,1).
Now: White on (f,2) (from f−1), Black on all rank 3 except f−1. White's pawn on f+1,1 still there.
Black captures: only attacker left is (f+1,3). Captures (f+1,3)×(f,2).
Now: Black on (f,2) (from f+1), White on all rank 1 except f−1, f+1. White's original pawn on f,1? No, White pushed from f,1 so f,1 is empty. Wait — White's push was from (f,1) to (f,2). So (f,1) is empty. White's remaining pawns on rank 1: all except f (pushed), f−1 (used to recapture), f+1 (still there? No, f+1,1 hasn't moved yet).

Actually let's track files:
- File f: White pushed 1→2. Then Black (f−1) captured to f,2. Then White (f+1) recaptured to f,2. Then Black (f+1) captured to f,2. Then White (f−1) recaptured to f,2.
- File f−1: White pawn at 1 captured to f,2 (ply 3). Black pawn at 3 captured to f,2 (ply 2). Both gone.
- File f+1: White pawn at 1 captured to f,2 (ply 5? No, ply 3 was f−1. Ply 5 would be f+1). Black pawn at 3 captured to f,2 (ply 4). Both gone.
- Other files: untouched.

After ply 5: File f has White on 2, Black on 3 (blocked pair). Files f−1, f+1 empty. All other files: White on 1, Black on 3.
Black to move. Black's pawns on rank 3 attack only rank 2. Only rank 2 pawn is on file f. Its attackers would be on f−1 and f+1, which are empty. So Black has no capture.

The proof's induction invariant (a)-(c) is correct: before each ply 2-5, rank 2 has exactly one pawn (on f,2) belonging to the side that just moved; all pawns of side to move are on home rank; attackers of (f,2) are exactly the unused neighbours.

**Theorem 5.2:**
- Files f−1, f+1 empty. File f has dead blocked pair (can never move: captures would land on f±1, which stay empty by Lemma 1.1).
- Remaining files form an arc of length n−3 bordered by empty files. By Lemma 1.4 (arc = strip), this is D_{n−3}.

**Theorem 5.3:**
- Flat Dawson's chess: alternating play on D_n is a first-player win iff G(n) ≠ 0 (classical result, checked for n ≤ 22).
- The macro-move model treats each macro-move as a single impartial move reducing the strip by 3 (middle push), 2 (end push), or 1 (isolated file). This is exactly octal 0.137.
- During a macro-move, other strips are quiet (no captures available), so compulsion acts locally.
- R_n has exactly one macro-move, leading to heap n−3. So its Grundy value is mex{G(n−3)}.

#### Steps Not Fully Justified

- **Lemma 5.1 induction base:** "These hold after ply 1." After White's push, rank 2 has White pawn on (f,2); Black pawns all on rank 3; attackers of (f,2) are Black on f−1 and f+1. Correct.
- **Invariant maintenance:** "A pawn on its home rank attacks only squares on rank 2." True in Dawson's chess (no double steps, no promotions). So captures are exactly on (f,2).
- **Distinct neighbours:** n ≥ 3 ensures f−1 ≠ f+1 mod n. On a 3-ring, f−1 = f+1? No, on C₃, f−1 and f+1 are the same file (since 3 files, distance 1 and -1 are the same mod 3). Wait! The proof says "neighbours in (c) exist and are distinct because n ≥ 3, so f−1 ≠ f+1". But on C₃, f−1 ≡ f+1 (mod 3). So for n=3, the two neighbours are the *same file*!
  - On R₃ (3 files), White pushes on file 0. Black's attackers on (0,2) are files 2 and 1 — which are distinct mod 3? 0−1=2, 0+1=1. Yes, distinct! On a 3-cycle, each vertex has two distinct neighbours. f−1 and f+1 are distinct mod n for all n ≥ 3. My confusion: on C₃, the two neighbours of 0 are 2 and 1, which are different. The statement "f−1 ≠ f+1" is true mod n for n ≥ 3 because 2 ≢ 0 (mod n). So it's fine.
- **Global compulsion acts locally:** "During a macro-move the other strips are quiet: they have no captures." This needs justification: in a sum of strips separated by empty files, a capture in one strip doesn't create captures in another. True because captures only happen on rank 2, and the macro-move only populates rank 2 in the active strip. Other strips have no rank-2 pawns, so no captures there. Correct.

#### Verdict: **VALID**

The macro-move analysis is correct. The reduction R_n → D_{n−3} is rigorous. The Grundy value mex{G(n−3)} follows from the classical theory of octal 0.137. The proof is complete for n ≥ 3.

---

## Part II: Statements from `kings/theory/LOOPY.md`

---

### Theorem 1.14(i): Validity of the Convention — P(X) = D(X)

#### Precise Restatement

Assume (V1) non-interaction and no stalemate, (V2) decisiveness, (V3) frozen Z. Then for either side to move, P(X) = D(X). There are no draws, and the result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z deleted).

#### Re-Derivation

1. By (V3), every Z-move is a suicide for the mover (gives opponent a decisive event ⊕/⊖). In the D-model, Z contributes only suicides.
2. By Lemma 1.7 (suicide deletion, normal play), suicides can be deleted without changing results. So D(X) = D(⊞ G_i).
3. D is short (acyclic), so no draws. Let σ be the D-winner for the given side to move.
4. σ plays a D-winning strategy in ⊞ G_i. This strategy never uses Z-moves (they are σ's suicides).
5. By (V1a), every legal chess move of the loser σ̄ is a D-option.
6. Under σ's winning strategy, σ̄ never has an option to its own terminal (every option leads to σ-win).
7. Play ends in a σ-terminal (made by σ) or a σ̄-suicide (Z-move or pawn move giving σ a passer).
8. Play terminates because components are short and (V1b) excludes "no move".
9. By (V2), the terminal is a P-win for σ. So σ wins P(X).

#### Steps Not Fully Justified

- **Step 2 (Lemma 1.7 applies):** Lemma 1.7 is for D-games under *normal play* (no draws). The D-model here has no draws by construction (terminals are ⊕/⊖, no stalemate because (V1b) gives a move). So Lemma 1.7 applies.
- **Step 5 (V1a covers all loser moves):** (V1a) says "legal chess moves = D-options". This includes the condition that en passant obeys (E) and no checks. If a chess move is not a D-option, the strategy might face an unexpected move. (V1a) explicitly assumes this doesn't happen.
- **Step 6 (loser never has own terminal):** In a winning strategy for σ, at every σ̄-to-move position, all options lead to σ-win. So σ̄ cannot move to ⊖ (which would be a σ̄-win). This is the definition of a winning strategy.
- **Step 8 (termination):** The components are short games (Φ decreases). But could the play cycle through Z-moves? No, because σ never plays Z-moves (they're suicides), and σ̄ playing a Z-move ends the game (decisive event for σ). So no cycles.

#### Verdict: **VALID**

The proof correctly reduces the problem to the normal-play sum of components. The assumptions (V1)–(V3) are exactly what's needed. The sharp form noted after the theorem (only one winning strategy needs (V2)/(V3)) is also correct.

---

### Theorem 2.7: Sufficiency of the Local Certificate LC_T

#### Precise Restatement

Let m be a Z-move of side s, r the punishing reply (king capture of a Z-pawn), Q the position after m and r with s to move. If **LC_T(m)** holds at Y:
- (L1) For every pass budget k ∈ {0,1,2,…,∞}, s̄ wins the local game in Q_Z within T of its own moves (s may pass up to k times, not in check; stalemate with no pass = failure; s̄ wins by promoting to uncapturable queen; s̄'s king stays on F_Z).
- (L2) μ_s ≥ T+1, where μ_s is the least s-moves to promote in Q with s̄'s Z-pieces removed, s̄'s context pawns fixed.
- (L3) No stalemate in the window: at every s-turn, s has a legal move in the real position.
Then m is decisively punished in P.

#### Re-Derivation

s̄ plays r, then follows local winning strategy σ_Z in Q_Z (using only Z-moves). We check survival in full position for t ≤ T:

1. **s's moves map to local game:**
   - King moves: same in Q_Z (fewer pieces, so still legal; context pawn capture becomes plain move).
   - Context moves: act as passes in Q_Z. Not made in check (unless answering check by context pawn, which doesn't exist in Q_Z). Number of such passes = k, covered by (L1).

2. **s̄'s moves are legal:** s̄'s king stays on F_Z. By Lemma 2.2 (buffer invariance), no context pawn attacks F_Z, occupies its squares, or gives check. s̄'s pawn moves stay on F_Z. No sliders ⇒ no pins.

3. **s does not promote first:** After r, s moves first. Before s̄'s T-th move, s has made T moves. By (L2), μ_s ≥ T+1. Removed Z-pieces of s̄ could only slow s, so μ_s is a lower bound. s's own Z-pawns are in Q_Z, and σ_Z wins against them.

4. **No other escape:**
   - (L3) excludes stalemate of s in real position. (L1) at actual budget excludes it in Q_Z.
   - s cannot checkmate s̄ (no officers, context pawns don't attack F_Z).
   - New queen on F_Z, out of reach (Lemma 2.2).

Therefore s̄ promotes within T moves → P-win.

#### Steps Not Fully Justified

- **(L1) "every pass budget k":** The proof says "a pass changes nothing on the board, so the timing argument covers every pattern of passes." This is true because the local game's geometry is static — passes don't change piece positions. The only danger is stalemate when k runs out, which the "stalemate proviso" in Corollary 2.8 handles.

- **(L2) μ_s definition:** "Least s-moves in which s could promote if s̄ never moved, s̄'s Z-pieces removed, s̄'s context pawns fixed." This is a lower bound because removing s̄'s Z-pieces and freezing s̄'s context pawns can only help s (fewer obstacles). But what if s̄'s Z-pieces *block* s's promotion path? Then removing them *reduces* μ_s, making the bound tighter (good for the proof). If s̄'s Z-pieces *help* s (e.g., by shielding), removing them could increase μ_s, weakening the bound. But Z-pieces are enemy pieces; they don't help s promote. So μ_s is indeed a lower bound.

- **(L3) sufficiency of (L3′):** "Every square within distance T+1 of s's king lies on F_Z." This ensures s's king has same moves as in Q_Z. But what if a context pawn *gives check* to s's king from outside F_Z? Lemma 2.2 says context pawns attack only context and buffer squares, not F_Z. So no check from context pawns. What about discovered checks from s̄'s pieces? s̄'s pieces stay on F_Z. So (L3′) is sufficient.

- **The "unlimited-pass argument" (referee's gap):** The referees noted a gap fixable by an unlimited-pass argument. The proof uses (L1) for *every* k including ∞. This *is* the unlimited-pass argument: the local strategy must win even if s has infinitely many passes. The proof explicitly requires this ("for every pass budget k ∈ {0,1,2,…,∞}"). So the repair works — the certificate *requires* winning against infinite passes, which is stronger than needed for any finite context.

#### Verdict: **VALID-WITH-REPAIR** (the repair is already incorporated in the statement of (L1) requiring k = ∞)

The theorem as stated includes the unlimited-pass condition (k = ∞ in L1). The proof uses it correctly. The referee's gap was that an earlier version only required k = 0 or finite k; the current version fixes this by requiring all k up to ∞.

---

### Proposition 2.10: Which Punishments Are Universal

#### Precise Restatement

**(a)** If T = 1, (L2) holds in every non-terminal context. A group with T = 1 punishments satisfying (L1) and (L3) is decisively punished in every non-terminal context (modulo (A_Q)).

**(b)** For every T ≥ 2, there exists a non-terminal context with μ_s = 2. So (L2) fails in some context, and such a group's zero is context-dependent.

#### Re-Derivation

**(a) T = 1:**
- An s-pawn that can promote in 1 move stands on rank H−1 (7th rank).
- No enemy pawn can stand ahead of it (on rank H), so it is passed.
- Therefore the context would be terminal (a passer exists).
- In a *non-terminal* context, no pawn is on the 7th rank.
- The king's help doesn't change this: removing a blocker takes a move of its own, so μ_s ≥ 2.
- Thus μ_s ≥ 2 = T+1, so (L2) holds.
- (L3) for T = 1 only asks that s has a legal move at its single turn.

**(b) T ≥ 2:**
- Construct context: White pawn on (f, H−2), Black pawns on (f, H−1) and (f+1, H−1). No pawn passed (White on H−2, Black on H−1 but White pawn blocks f-file; Black on f+1,H−1 has no White pawn ahead on f+1,f+2).
- White captures (f,H−2)×(f+1,H−1) → (f+1,H−1), then promotes next move. So μ_W = 2.
- For any T ≥ 2, μ_W = 2 < T+1, so (L2) fails.
- Hence a T ≥ 2 punishment is not universally certified.

#### Steps Not Fully Justified

- **(a) "The king's help does not change this":** Could the king capture a blocker on the 7th rank in 1 move, enabling promotion? If a blocker is on (f, H), it's on the promotion square — but pawns don't stand on the promotion square (they promote). If a blocker is on (f±1, H−1), the king would need to capture it (1 move), then the pawn promotes (1 move) = 2 moves total. So μ_s ≥ 2 still holds.

- **(b) "No pawn is passed":** White on (f, H−2): Black on (f, H−1) blocks. Black on (f+1, H−1): White has no pawn on f+1 or f+2, so is this Black pawn passed? A Black pawn on (f+1, H−1) is passed if no White pawn on {f+1} ∪ N(f+1) at rank > H−1. Rank H is promotion, no pawns there. White has pawn on (f, H−2), which is on adjacent file f but rank H−2 < H−1. So yes, Black on (f+1, H−1) *is* passed! This means the context is **terminal** (Black has a passer). But the proposition says "non-terminal context".
  - Wait: the definition of passed pawn (notes/lemmas.md L1.2(c)): "no enemy pawn stands on a file of {f} ∪ N(f) at a rank greater than r". For Black on (f+1, H−1), enemy files are {f+1, f, f+2}. White has pawn on (f, H−2). Rank H−2 < H−1, so not greater. So Black pawn *is* passed. The context has a Black passer → B-terminal → terminal context.
  - The counterexample fails because it's a terminal context!
  - However, the proof says "No pawn is passed." This appears to be an error. Let me check: White on (f, H−2), Black on (f, H−1) and (f+1, H−1). Black on (f, H−1): enemy files {f, f−1, f+1}. White on (f, H−2) rank H−2 < H−1 → not greater. So Black on (f, H−1) is also passed! Both Black pawns are passed.
  - So this context is a race (both sides have passers? White has no passer: White on (f, H−2), Black on (f, H−1) blocks file f. White on f+1? No White pawn there. So only Black has passers → B-terminal).
  - The proposition claims this is a "non-terminal context". It is not.

#### Verdict: **GAP**

The counterexample for (b) is a terminal context (Black has passed pawns), not a non-terminal one. The claim "for every T ≥ 2 there is a non-terminal context with μ_s = 2" is not proved by this example. A valid counterexample would need a non-terminal context where μ_s = 2. This may still be true, but the given construction doesn't work.

**Repair idea:** Place White on (f, H−3), Black on (f, H−1) and (f+1, H−2). Then White captures (f,H−3)×(f+1,H−2) → (f+1,H−2), then pushes to (f+1,H−1) and promotes. μ_W = 3? Need μ_s = 2 exactly. Maybe White on (f, H−2), Black on (f+1, H−2) and (f+2, H−1)? Need to check passedness carefully. This requires more work.

---

### Theorem 3.4: Outcome Rules with Passes (G ⊞ on_D, G ⊞ off_D, G ⊞ dud_D)

#### Precise Restatement

Let G be a short D-game (acyclic, terminals ⊕/⊖). Define predicates by induction:

**(a) G ⊞ dud_D (both pass):**
- Λ_L(x) ⟺ ∃ Left option ⊕, or ∃ Left option x^L with Λ_R(x^L)
- Λ_R(x) ⟺ Λ_L(x) ∧ (∀ Right option x^R: x^R = ⊕ ∨ Λ_L(x^R))
- r(x, s) = W iff Λ_s(x); L iff Ρ_s(x) (symmetric); else D.
- Consequences: no zugzwang; if G has no terminals, all drawn; a side wins iff it can force a decisive event against a passing opponent.

**(b) G ⊞ on_D (only White passes):**
- Ρ′_R(x) ⟺ ∃ Right option ⊖, or ∃ Right option x^R with Ρ′_L(x^R)
- Ρ′_L(x) ⟺ Ρ′_R(x) ∧ (∀ Left option x^L: x^L = ⊖ ∨ Ρ′_R(x^L))
- r(x, s) = L iff Ρ′_s(x); else W. No draws.

**(c) G ⊞ off_D (only Black passes):** Mirror of (b).

#### Re-Derivation

The proof uses the least fixed point of Definition 1.2 (retrograde analysis on finite game graph).

**(a) G ⊞ dud_D:**
- States: (x, s) where x ∈ G, s ∈ {L,R}. Pass moves: (x, L) → (x, R), (x, R) → (x, L).
- Terminals: ⊕ (White wins), ⊖ (Black wins).
- Compute winning regions by induction on stages.
- **Claim:** Left cannot win by passing first. Suppose Left wins (x, L) at stage n by passing to (x, R). Then (x, R) was won by Left at stage < n. But Right can pass from (x, R) back to (x, L), so (x, L) would be won at an even earlier stage — contradiction. So Left's winning moves are always G-moves.
- **Left wins (x, R):** Right to move. Right's options: G-moves to x^R, or pass to (x, L). Left wins iff *every* Right option leads to Left win. That is: every x^R is ⊕ or satisfies Λ_L(x^R). And Left must have a winning move from (x, L), i.e., Λ_L(x). So Λ_R(x) ⟺ Λ_L(x) ∧ ∀x^R (⊕ ∨ Λ_L(x^R)).
- **Left wins (x, L):** Left to move. Left wins iff some option wins. Options: G-moves to x^L (need Λ_R(x^L)), or pass to (x, R) (need Λ_R(x)). But we just showed passing first never wins, so only G-moves matter. Thus Λ_L(x) ⟺ ∃x^L (⊕ ∨ Λ_R(x^L)).
- Symmetric for Ρ_L, Ρ_R (Black wins).
- If neither Λ nor Ρ holds, it's a draw (infinite play or stalemate).

**(b) G ⊞ on_D:**
- Only White can pass: (x, L) → (x, R). From (x, R), only G-moves.
- No draws: Black makes finitely many moves (G finite, acyclic), plays alternate → finite play → determined.
- **Black wins (x, R):** Black to move. Black wins iff some Right option is ⊖ or leads to Black win (i.e., Ρ′_L(x^R)). So Ρ′_R(x) ⟺ ∃x^R (⊖ ∨ Ρ′_L(x^R)).
- **Black wins (x, L):** White to move. White's options: G-moves to x^L (need Ρ′_R(x^L)), or pass to (x, R) (need Ρ′_R(x)). White loses (Black wins) iff *every* White option leads to Black win. So Ρ′_L(x) ⟺ Ρ′_R(x) ∧ ∀x^L (⊖ ∨ Ρ′_R(x^L)).
- If Black doesn't win, White wins (no draws).

#### Steps Not Fully Justified

- **"Left cannot win by passing first" in (a):** The argument is: if passing wins at stage n, then (x,R) wins at stage < n, but Right can pass back, so (x,L) wins at stage < n-1, contradiction. This assumes the fixed-point computation is well-founded. Since G is finite and acyclic, and passes only toggle the side to move, the state space is finite (2|G| states). The least fixed point exists and the argument holds.

- **Well-foundedness of Λ_L/Λ_R recursion:** Λ_L(x) uses Λ_R at successors; Λ_R(x) uses Λ_L at x and successors. Since G is acyclic, we can compute in reverse topological order. At sinks (no G-moves), Λ_L = false (no ⊕ option, no successors), Λ_R = false (Λ_L false). This propagates up. Well-founded.

- **No draws in (b):** "Black makes finitely many moves in any play, since G is finite and acyclic, and plays alternate." But White can pass arbitrarily many times! The play could be: White passes, Black moves, White passes, Black moves, … Black's moves are finite, so eventually Black runs out of moves. When Black has no move, Black loses (normal play). So the game is finite. Correct.

#### Verdict: **VALID**

The fixed-point definitions are correct and the derivations are rigorous. The recursive predicates match the least-fixed-point semantics of the loopy game. The "no zugzwang" and "win iff force decisive event against passing opponent" interpretations are accurate.

---

## Summary of Verdicts

| Statement | Verdict | Notes |
|---|---|---|
| L1.6 (Theorem 1.6) | **VALID** | Clean decomposition proof; condition (E) is necessary and sufficient |
| L2.1 (Theorem 2.1) | **VALID** | HSS + BIG bound gives outcome faithfulness; frontier strategy sound |
| L2.3 (Theorem 2.3) | **VALID** | Trivial induction under the no-split hypothesis |
| L3.3 (Theorem 3.3) | **VALID** | Gift-horse principle correctly applied; BIG-interior condition exact |
| L5.1–5.3 (Dawson ring) | **VALID** | Macro-move analysis correct; reduction to octal 0.137 rigorous |
| Theorem 1.14(i) | **VALID** | Reduces to normal-play sum; assumptions (V1)–(V3) are sufficient |
| Theorem 2.7 | **VALID-WITH-REPAIR** | Unlimited-pass condition (k=∞ in L1) is the repair; already in statement |
| Proposition 2.10 | **GAP** | Counterexample for (b) is a terminal context, not non-terminal |
| Theorem 3.4 | **VALID** | Fixed-point derivation correct for all three pass reservoirs |

---

## Reproduce Commands

All computational claims can be checked with:
```bash
cd /Users/aritro/Downloads/Research/Chessendgames
PYTHONPATH=. .venv/bin/python -m pytest lemmas/test_L1_components.py -v
PYTHONPATH=. .venv/bin/python -m pytest lemmas/test_L2_big.py -v
PYTHONPATH=. .venv/bin/python -m pytest lemmas/test_L3_trebuchet.py -v
PYTHONPATH=. .venv/bin/python -m pytest lemmas/test_L5_dawson.py -v  # if exists
```

For LOOPY.md theorems, the predictions in §6 are checked by `kings/kpsolve` (C solver).