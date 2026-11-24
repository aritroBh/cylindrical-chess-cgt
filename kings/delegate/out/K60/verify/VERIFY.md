# K60 referee report: an exact test for "has the results of over"

Referee: one AI agent (not the investigator), 2026-11-23. No human re-derivation. I tried to break the hand proofs line
by line, wrote my own toy solvers (`src/r60lib.py`, `src/r60run.py`; nothing taken from `K60/src` or K57's code), and
re-ran the real-group failure on a second move generator.

## Verdicts

| Claim | Verdict | Basis |
|---|---|---|
| Proposition A0 (q's = 0_D; roots ≤ ω, any exact group) | CONFIRMED | re-derived from K57 §3 (E1, E2 never use (B1); b = 0 throughout); toys: 0 violations |
| Theorem A, necessity | CONFIRMED | re-derived (one line: m is a Black option) |
| Theorem A, sufficiency | CONFIRMED | re-derived; it also holds game by game (see A.2); toys: 0 violations game by game |
| Proposition A1 | CONFIRMED | re-derived; toys: 0 violations |
| Proposition A2 (C_W not necessary; G2) | CONFIRMED | G2 checked by hand and by my code (exact, (B1), results of ω on my battery, C_W fails) |
| Theorem B, (2) ⇒ (1) | CONFIRMED, two cosmetic wording slips | re-derived case by case (A.3) |
| Theorem B, (1) ⇒ (3), (3) ⇒ (4) | CONFIRMED | re-derived |
| Theorem B, (4) ⇒ (2) | CONFIRMED | re-derived; positional Büchi determinacy applies (A.4) |
| Corollary B2 ((B1) = Aux without passing) | CONFIRMED | re-derived; toys: (B1) ⇒ Aux, 0 violations |
| Corollary B3 (one test game T_K) | CONFIRMED | re-derived; toys: B3's root test agrees with the battery in every group |
| Remark "draw part alone" | CONFIRMED | re-derived; toys: Aux-with-draws ⇔ D-half of (C) on the battery, 0 violations |
| Example G1 | CONFIRMED | by hand and by my code |
| K58's witness fails (C) | CONFIRMED | by hand and by my code |
| Real groups: Z_O fails (C) exactly at 1…e5–e4 | CONFIRMED, upgraded to CHECKED-2 | pr57 (K56's generator) agrees with vgsum (K56 referee's generator) on T_0…T_6, −1, under |
| Real groups: H10 Aux won at all ten moves | CONFIRMED as a consequence of (B1) (CHECKED-2) and Corollary B2; aux60's direct Aux result stays COMPUTED-1 | pr57: H10's ten x_m are W beside T_0…T_6 and −1 (consistency only; T_N with N ≤ 6 is not a proof of Aux) |
| K60's EDITS.md | applies cleanly (2 of 2), but REPLACED | numbering collides with K59's Corollary 4.17; stale passages left; label must say refereed |

Nothing refuted. No step needed a repair of substance.

## A. The hand proofs, line by line

### A.1 Proposition A0 and Theorem A

- **A0.** In K57 §3, (B1) enters only in Case E3 (Black's bad move at a root, Y = White) and through the budget b = 1
  that E3 creates; b = 1 is also the only state in which S_cur may ask White for ω → 0_D in phase 2. Y = Black
  (transferring Black's wins and non-losses): phase 1, Case E1 (bad White move at a root or at a q), Proposition 4.14
  replacing ω by 0_D, phase 2 with b = 0. No (B1). Y = White starting at a q: o = 0_D throughout, every Black move at
  a q enters through E2 with b = 0. No (B1). So (i) and (ii) hold for every exact group. The q with Black to move
  without the right of a double-step freeze is covered too: removing the right removes Black options only (K57's (P2)),
  and if Black then has no board move, Black must move in T, as at 0_D.
- **Necessity.** At (ρ, t, Black to move) the move m is a board move, legal whether or not Black is in check (Black is
  not, at a root), leading to (x_m, t, White to move) with White's right if m is a double step. Black picks the minimum
  over its options in the least fixed point, so r(ρ ⊞ t, B) ≤ r(x_m ⊞ t, W) in all three values. With the results of ω
  this is (C). Correct with draws: a D at the root forces ≥ D after every Black option.
- **Sufficiency.** Y = White, X = Black. In phase 1 the real and virtual T-positions and sides coincide (K57's
  invariant M). At Black's bad move m the virtual state (ω, t, Black to move) is S-consistent (no replacement S → S′
  happens for Y = White), so r(ω ⊞ t, B) = W (resp. ≥ D). (C) at the same t gives r(x_m ⊞ t, W) ≥ that. Switching to an
  optimal strategy from the real state is legitimate; the prefix is S-consistent and bounded by S's bound when S wins
  (finitely many possible switch states), so wins stay bounded (K-a), and non-losses stay non-losses (K-b). Roots carry
  no e.p. right in phase 1 (reached only by the shuttle or at the start). Real Black is never stuck at a root (the
  shuttle) or at a q ((O3)).
- **Game by game (a strengthening the investigator does not state).** Both directions use (C) only for the T under
  consideration: necessity derives (C) for T from the results of ω beside T; sufficiency uses r(x_m ⊞ t, W) for the
  same T. So, for each fixed T: G has the results of ω beside T iff (C) holds for T (at every bad move of either root).
  My toy run tests exactly this per T (0 violations), and I put it into the edits.
- **Side to move, no-move-loses, checks, e.p.** All comparisons are between sum positions; P's stalemate draw enters
  only through Definition 4.8. In (C) the left side has White to move with White's right after a double step; the
  right side Black to move. These are the states the proof produces. Correct.
- **A2.** G2 checked by hand: q is a mutual zugzwang (q, B: only q → qb, then White promotes; q, W: only q → qw, then
  Black promotes); x, White to move: x → w, Black's only move w → w2, White promotes; (B1): Black's token at w is
  answered by w → ⊕. t0: r(ω ⊞ t0, W) = W (t0 → t1, Black must pass, t1 → ⊕); r(x ⊞ t0, W) = L (x → w is met by t0 → ⊖,
  t0 → t1 by x → ⊖); r(ω ⊞ t0, B) = L. Correct.

### A.2 Theorem B, (2) ⇒ (1)

I re-ran every case of the double simulation (V1 = Aux play on the real board, V2 = over ⊞ T on the real T):

- Invariants (I1)–(I4) hold after each complete exchange (real White to move: V1 White to move, V2 Black to move; real
  Black to move: both Black to move). Transient states with V2 White to move occur only inside an exchange.
- Every real White move is legal: σ's board moves are legal in V1, whose board equals the real board and whose White
  e.p. options are a subset of the real ones; S's T-moves are played only when White is not in check (White can be in
  check only right after a Black board move, and then σ must answer on the board, because a pass in check is illegal in
  Aux exactly as a move elsewhere is in a D-sum).
- The mirror freeze ω̄ → 0̄ in V1 is legal: it happens when V1 has Black to move and the board's last change was Black's
  own move, x itself, or after a real Black move in T; in all three Black is not in check. ω̄ is present because ω is
  (I2), and both components lose their pass/freeze together.
- Ends: a Black promotion or a stuck White would be a Black win of the σ-consistent V1; ⊖ in T a Black win of the
  S-consistent V2; real Black stuck loses. When S wins, V2 is finite, so finitely many T-moves and finitely many White
  passes in V1 (each pass is mirrored by a Black pass in V2); an infinite real play would then give an infinite
  σ-consistent Aux play with finitely many passes, a Black win of Aux: impossible. König's lemma bounds the wins.
- *Wording slips (cosmetic, no effect on the proof).* (1) The e.p. bullet says "White's right is the same in V1 and
  real"; after a σ-pass answered by S's ω → 0_D, V1 has lost White's right while the real game still has it until
  White's board move. Harmless: σ then chooses a move legal in V1, hence legal in the real game. (2) "4·|boards|
  states" counts each board together with its e.p. right; with boards counted without the right it is up to 8 per
  board.

### A.3 Theorem B, (1) ⇒ (3) ⇒ (4) ⇒ (2), B2, B3

- (1) ⇒ (3): ω ⊞ u_0, Black to move, is a White win in T_N (Black's pass is answered by u_i → u_{i+1}, at u_N White
  plays ⊕; Black's u_i → z by ω → 0_D, after which Black has no move). Correct; T_N is short, so (C) restricted to the
  short games T_N already implies Aux, hence (C) for all loopy T. (So Theorem B does not need loopy T; I note this in
  the edits as "results of ω beside short D-games give them beside loopy ones", via B3.)
- (4) ⇒ (2): see A.4. The identification φ maps x ⊞ T_N bijectively onto Aux's options while fewer than N passes have
  been made (same check rule, same clearing of the right, same no-move rule; at z, as at 0̄, White has no move
  elsewhere), so β transfers; u_N is never reached because a β-consistent play has at most K/2 < N passes (passes start
  at distinct White-to-move ω̄-states). Infinite β-consistent plays are draws in T_N, finite ones Black wins. So
  r ≠ W. Correct.
- B2: Aux with White never passing is exactly x ⊞ (−1) (Black's freeze is the one Black move elsewhere, under the same
  rules). A White win there is bounded, hence has no infinite plays, hence is a Büchi win. Correct.
- B3: ⇒ by (1) ⇒ (3) at the roots; ⇐: m is a Black option at ρ, so r(x_m ⊞ u_0, W) ≥ r(ρ ⊞ u_0, B) = W in T_K, then
  (4) ⇒ (2) ⇒ (1) and Theorem A. K is a bound for every x_m's Aux (Aux from x_m lives on the boards reachable from x_m,
  a subset of the group's component). Correct.
- *Internal inconsistency in PROOF.md (cosmetic).* After B3 it says "the smallest N that works is 0, 1 or 2 (§6)", while
  §6 reports N up to 5.

### A.4 Determinacy and the Büchi encoding

Aux is a finite arena. Finite plays must be encoded: a promotion or a stuck Black goes to a White sink with an accepting
self-loop, a stuck White or a Black promotion to a Black sink with a non-accepting self-loop; the acceptance sits on
pass edges, made into vertices by subdividing each pass edge (the subdivision vertex has one successor, so positional
strategies on the subdivided arena are positional on Aux). Büchi games on finite arenas are determined and both players
have positional winning strategies (a parity game with two priorities; Zielonka 1998; Grädel–Thomas–Wilke, LNCS 2500).
The argument "no pass edge on a cycle of H" is correct: in H every Black vertex has only its β-edge, so any cycle of H
reachable from the start is a β-consistent play White can force and repeat; cycles contain no sink. Hence passes cross
between strongly connected components of a DAG order and never repeat their source state.

Draws: in Aux an infinite play with finitely many White passes is a Black win. That is the reading under which the
theorem is proved; it is the right one for (C) because (2) ⇒ (1) delivers both the W- and the D-part of (C), and
(1) ⇒ (3) ⇒ (4) ⇒ (2) uses only the W-part beside T_N. Consequence worth stating: the W-part of (C) implies the D-part.

## B. Own brute force (COMPUTED-1, `src/r60run.py`, seeds 101, 102, 103)

Model (own code): abstract boards with check flags per colour (no move into one's own check; a side in check may not
move elsewhere, pass or freeze), double steps that give the opponent an e.p. right for one turn, e.p.-only moves,
promotions as terminals, P alone with mate a loss and stalemate a draw, sums with no-move-loses. Groups are random
(three families: random, adversarial with dense checks and back edges into the roots and q's, "tempo" with sparse
moves and many promotions), filtered to Definition 4.8 by my own exactness test. Battery per group: 292 finite D-games
(23 named, among them over, under, on, off, dud, ±1, threats with terminals for either side, a White-pass-forever game
with a Black threat, suicides, K60's t0; 12 sums of two named games; 250 random games of 1–6 positions, loopy, terminals
for both sides, with White and Black options; T_N for N = 0, 1, 2, 3, 4, 6 and N = K = 4·boards). Two Büchi solvers
(nested attractor fixpoint, and Zielonka's recursive algorithm on a parity encoding) are compared at every bad move.

| | seed 101 | seed 102 | seed 103 | total |
|---|---|---|---|---|
| exact groups (incl. 4 hand groups) | 3,004 | 3,004 | 3,004 | 9,012 |
| groups with a check | 1,778 | 1,757 | 1,729 | 5,264 |
| results compared | 22,078,212 | 20,625,570 | 20,903,320 | 63,607,102 |
| bad Black root moves | 7,514 | 7,593 | 7,574 | 22,681 |
| … double steps / giving check | 2,349 / 691 | 2,436 / 727 | 2,335 / 767 | 7,120 / 2,185 |
| Aux won / lost | 7,212 / 302 | 7,277 / 316 | 7,251 / 323 | 21,740 / 941 |
| Aux won without (B1) | 307 | 371 | 344 | 1,022 |
| groups with the results of ω on the battery | 2,802 | 2,795 | 2,790 | 8,387 |
| … of them without (B1) / failing C_W | 213 / 291 | 239 / 307 | 225 / 277 | 677 / 875 |
| groups differing from ω on the battery | 202 | 209 | 214 | 625 |
| Aux losses separated only by some T_N | 1 | 0 | 1 | 2 |
| **violations** | **0** | **0** | **0** | **0** |

Checked, all with 0 violations: A0(i) at every q-state (with and without the right) and A0(ii) at both roots, both
sides; A1; Theorem A game by game (results of ω beside T ⇔ (C) beside T); Aux won ⇒ (C) on the whole battery; Aux lost
⇒ (C) fails on the battery; Aux ⇔ x_m ⊞ u_0 White win in T_K; Aux won ⇒ W in every T_N tried; (B1) ⇒ Aux; Aux with
draws (r ≠ L) ⇔ D-half of (C) on the battery; Corollary B3's root test ⇔ results of ω on the battery; the two Büchi
solvers agree.

What I looked for specifically:
- *Aux won but the group differs from ω on some T:* none (0 of 21,740 Aux wins).
- *Aux lost but nothing in the battery separates:* never once T_N is in the battery. Twice (adv10375 in seed 101,
  tempo15797 in seed 103; both printed in full in the logs) the 285 non-T_N games do not separate, and T_2 (and every
  larger T_N tried, including T_K) does, as the proof of (4) ⇒ (2) says: Black's positional Aux strategy carries over to
  x_m ⊞ T_N.
- Hand groups: G1 (exact, (B1) fails at both bad moves, Aux won, results of ω on the battery, x_m ⊞ T_N W for every N
  tried); G2 (exact, (B1), C_W fails, results of ω); K58's witness (Aux lost, differs from ω, x_m ⊞ T_N W only for
  N = 0); R1, my own check/e.p. probe (Black's bad move is a double step that gives check, White's only answer is the
  e.p. capture, after which White has no board move: Aux lost because White cannot pass in check and is stuck after
  Black's freeze; the group differs from ω).
- Peak memory 43 MB, 75–79 s per seed.

## C. Real groups on a second move generator

`run_real.sh`: K57's `pr57` (K56's pass-game program with a D-sum mode; K56's own move generator, which shares no code
with the K56 referee's generator under vgsum and aux60), compiled in the session scratchpad, beside T_0 … T_6, under_D
and −1, probes = the four roots and every x_m. Logs `logs/pr57_ZO.*`, `logs/pr57_H10.*`.

- **Z_O (cyl:8×6, 5,501,308 nodes in pr57's keying):** x after 1…e5–e4 at the d4 root, White to move: W beside T_0,
  T_1, **L beside T_2 … T_6**, L beside −1 and under. The other ten x_m: W beside every T_N, −1 and under. Roots: d4 root,
  Black to move, L beside T_2 … T_6; d5 root, Black to move, W beside T_0 … T_2 and L beside T_3 … T_6. All identical to
  K60's vgsum run. Since ω ⊞ u_0, Black to move, is a White win in every T_N (PROVED), (C) fails at 1…e5–e4:
  **CHECKED-2** (two programs on two move generators). (B1) at the other ten: CHECKED-2 (vgsum and pr57), so (C)
  holds there by Corollary B2. Hence "Z_O fails (C) exactly at 1…e5–e4" is CHECKED-2 together with Theorem B. Peak
  1.19 GB.
- **H10 (cyl:10×6, 3,778,695 nodes):** all ten x_m are W beside T_0 … T_6 and beside −1; the roots equal ω beside every
  test (W beside T_N, D beside under, L beside −1). This is consistent with Aux won, not a proof of it (N ≤ 6 < K);
  the proof is (B1) (CHECKED-2, Corollary 4.16) with Corollary B2. Peak 0.79 GB.
- Probe note: for the double step e5–e3 there is no White pawn beside e3, so pr57 stores no e.p. target (aux60 writes
  `e4`); the positions are the same.

## D. Edits

- K60's `EDITS.md` applies to the current LOOPY.md (2 applied, 0 rejected), but numbers the new statements 4.17/4.18
  (K59 is adding Corollary 4.17), says "not yet refereed", and leaves stale: the opening paragraph of Conjecture 4.7
  ("With one Black token … it does force the results of over"), the K47 bullet's closing parenthesis ("while Z_O fails
  (B1) at 1…e5–e4"), and §8 item 2. "Is the Black-side" does not occur in LOOPY.md; the only "sufficient, not
  necessary" about (B1) is in Lemma 4.15.
- My replacement `verify/EDITS.md`: 5 edits, all applied to a scratch copy (5 applied, 0 rejected): Lemma 4.15
  pointer; Conjecture 4.7 opening; K47 bullet; §8 item 2; new **Theorem 4.18** and **Corollary 4.19**, inserted before
  "*Computable test (K43).*", i.e. after Corollary 4.16's paragraph and after K59's Corollary 4.17 if that lands at the
  end of 4.16's paragraph. None of my OLD blocks touches Corollary 4.16, the C4.7 status row, or the "To settle" line.
  Labels: PROVED (one AI proof, re-derived by the K60 referee; no human re-derivation; Theorem 4.18(c) uses KNOWN Büchi
  determinacy); COMPUTED-1 for the toy runs and aux60; CHECKED-2 for Z_O's failure at 1…e5–e4. No table rows edited.

## E. Blind packet

`K61_packet_draft.md`: definitions only (D-games, play, D-sums, r, over_D, 0_D, under_D, T_N, the abstract group with
check, e.p. right and promotions, the sum's rules, exact over groups (O0)–(O4), bad moves, Aux), statements A0, A, B, B3
without proof or hint, seven readings (side to move, stalemate vs no-move-loses, checks, e.p., draws, class of T, the
abstract model). Modelled on the K58 brief.

## What I did not check

- No human re-derivation; mine is a second AI reading.
- aux60's Büchi result on the real groups was not reproduced by a second Aux program; for H10 the conclusion rests on
  (B1) instead, for Z_O on the T_N sums. Z_O's flat translates, the cyl:8×7 groups and K59's flat groups were not run.
- The open question of a fixed finite test family independent of the group (K60 §4) was not examined.
- Toy groups are abstract; they model checks and e.p. rights as flags, not chess geometry.
- Nothing about P contexts or chess.

## Files

`src/r60lib.py` (solvers: least fixed point, D-sums, P alone, Aux as a Büchi game, Zielonka cross-check, T_N, test
games), `src/r60run.py` (generator, exactness test, battery, checks), `run_toys.sh`, `run_real.sh`, `logs/`
(`toys_10[123].*`, `pr57_*.*`, `TN_pr57.txt`, probe lists), `pids.log`, `EDITS.md`, `K61_packet_draft.md`.
Reproduce: `zsh kings/delegate/out/K60/verify/run_toys.sh 101 102 103`;
`zsh kings/delegate/out/K60/verify/run_real.sh <dir with pr57 built from kings/delegate/out/K57/src/pr57.cpp>`.
