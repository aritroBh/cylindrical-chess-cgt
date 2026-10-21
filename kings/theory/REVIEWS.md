# Adversarial reviews of LOOPY.md

Four independent referees (Claude models) were asked to refute this note. Their reports follow verbatim.
The revision of LOOPY.md answers every numbered item.

## Review 1: general theory review (pipeline reviewer)

I ran the reference tests and tried 7 new positions, and found no solver bug. The theory note has real defects: one theorem marked PROVED is false as stated, one proposition marked PROVED is wrong under the note's own notation, and the main certificate theorem has a broken proof step that can be repaired. None of them overturns a prediction that has been computed.

**Checks run**
- `.venv/bin/python -m pytest -q kings/ref/test_ref.py`: 56 passed (344 s).
- I solved 7 positions by hand and ran each through both `kings.ref.solve` and `kings/kpsolve` (QRBN, cap 1, ep on). Both solvers match my hand analysis on all 7. Position files are in `/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/rev/`.
  - flat:4x4 `Kb2 Pa3 ka4`: b → D D (stalemate); w → D D (every White move either stalemates Black or drops a3).
  - flat:4x4 `Kb2 Pc2 ka4 w -` → W W (c2–c4=Q is mate; this exercises the 4-rank double-step promotion).
  - flat:4x4 `Kc2 Pb3 kb4 pc3`, the 7.2 pattern on 4 ranks: b → W W (1...Ka3 2.Kxc3 Ka2 3.b4=Q Ka1 4.Qb2#); w → D D (1.Kc1 blockade holds, and White cannot win because every White move drops b3). Also `Kc1 Pb3 kb4 pc3 b -` → D D.
  - cyl:6x4 `Ka3 Pb2 Pc3 Pe2 kc4 pb3 pe3`, a stalemate trap like P1a: w and b → D D.
  - cyl:6x4 `Ka3 Pb2 Pc3 kc4 pb3`, a small version of the shuttle group Z_onT1: w and b → W W.
- kpsolve cyl:8x6 on P10 with k=0 gives W W.
- `kings/results/theory_predictions_raw.txt` matches every prediction P1–P9. The only inexact entries are P4 H*, H*2 and H0, which give W/D bounds; those are consistent with the predictions.

**Defects, most severe first** (all in `/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md` unless stated)

1. **Theorem 1.11(b) (PROVED) is false as stated.**
   - The threat set τ (Def 1.10) only counts Left moves to ⊕ and Right moves to ⊖. First-event dominance must also hold after suicides, but the proof's step "coordinate j had a + threat" fails when the event is a Right move to ⊕.
   - Counterexample: y1 has only a Right option ⊕; y2 has only a Right option ⊖. Then τ(y1)=∅ and τ(y2)={−}, so the position is pairwise safe; M_L=0, M_R=1, B≥2. After Right's suicide the position is B + { | −B} = −1, which is an 𝓡-position, so dominance fails. `cylcgt.cgt` with B=4 gives R.
   - The note calls this "L2.1 of notes/lemmas.md, restated", but lemmas.md's τ counts a passer created by either side's move. The restatement weakened the hypothesis.
   - Affected: the "sufficient" clause of Theorem 1.14(ii), Theorem 4.2(a), and the (V4) wording in §0 and `kings/REPORT.md`.
   - Fix: define τ by moves into ⊕/⊖ by either player.

2. **Proposition 1.13 (PROVED) and Theorem 3.3(b) contradict the note's own notation.** Def 1.1 says ∅ is a position with no options, and Propositions 1.12–1.13 translate it as 0. So A′ = {∅ | ⊖} gives White a move that kills the threat:
   - In chess semantics, A′ ⊞ R_n is 𝓝, not 𝓡.
   - In the BIG translation, {0 | −B} + n is 𝓝 for n ≤ B and 𝓛 for n ≥ B+1, never 𝓡 or 𝓟. The proof ignores Left's move to 0.
   - Theorem 3.3(b) should give (W, L), not (L, L).
   - The claimed regimes only hold for A′ = { | ⊖}, whose translation is { | −B} = −(B+1), not {0 | −B}.
   - Reproduce with `cylcgt.cgt`, B=4: `total([make([0],[-4]), n])` for n = 0..7 gives N,N,N,N,N,L,L,L. With `make([],[-4])` it gives R,R,R,R,R,P,L,L.

3. **Theorem 2.7 / Def 2.6: the pass-budget step is invalid, and its justification is wrong.**
   - The proof says "the number of such passes is some k, which (L1) covers". But the punisher's local strategy depends on k, it has to move before k is settled, and the defender can change its remaining budget mid-window. Example with the H*2 context Pe2/pe5: e2–e3 then e3–e4 gives two passes, while e2–e4 gives one pass and then none.
   - The theorem can be rescued another way. Play the k=∞ strategy: the real defender's options are a subset of the ∞-game's, and its only gain from having fewer options is stalemate, which (L3) excludes.
   - So the finite-k clauses of (L1) add nothing once (L3) holds, the remark "'every k' is needed" is wrong, and the scratch "all budgets" checks do not stand in for (L3).
   - (L3) is not checked for P4, P6, P12 or §5.1.

4. **The (V1a) row of the "each hypothesis is needed" table (§1.5) cites the wrong failure.** The engine-suite king sorties (41 of 449 draw, 7 win) are unpunished king-group moves, i.e. (V2)/(V3) failures; §5.6 itself treats them as certificate failures. No real (V1a) counterexample is given (an en passant / condition (E) failure would be one), so "none can be dropped" is unsupported for (V1a).

5. **Def 1.5's "S(X) is `cylcgt.pawns.value`" is false for these groups, and the §6 "naive convention" headline is against a strawman.**
   - Z_onT1, Z_offT1, Z_72 and 7.3 contain pawns that cylcgt's test calls passed. On the actual pawn sets, `cylcgt.pawns.value` returns +BIG (𝓛) for every P2 and P10 position, −BIG (𝓡) for P3, and RaceError for P5 and P8.
   - So the literal convention gets all 26 P2/P3/P10 entries right. "The naive convention gets 17 of the 26 entries wrong" and "decisive tests of the loopy theory" hold only for the ad-hoc reading "king group = 0, cylcgt on the context strip". These tests cannot tell the loopy theory apart from literal cylcgt.
   - Appendix A's search "with no passer at the root" cannot have used cylcgt's test, or it would have rejected Z_onT1.
   - Reproduce: `pawns.value(Board(7,6,True,True), Pos.parse('W: b4 c5 e2 / B: b5 e3 e5'))` gives outcome L. The truth is (W, W); the note's naive column says (L, L).

6. **(A_Q) is labelled CONJECTURE but is false in general.**
   - The promotion model P scores any promotion as a win, even one where the queen is captured at once.
   - flat:4x4 `Kd1 Pb3 ka3 w -`: `kpsolve --frozen` gives W W, while chess (both solvers) gives D D, because b4=Q is met by Kxb4.
   - It is a per-position hypothesis, not a conjecture. Also, the "scratch confirmation in P" and (L1) use a queen-safety model, not Def 1.5's P.

7. **Proposition 2.10(a) fails on 4-rank boards, which SPEC allows (H from 4 to 8).** A pawn that is not passed can promote in one move by a double step. cyl:7x4 with context W f2 / B e3 f3: `cylcgt.passed` is False for both sides, but ...e3–e1=Q takes one move, so μ_B = 1 < T+1. The proposition needs H ≥ 5.

8. **(L3′) can never apply.** The ball of radius T+1 around a king spans at least 5 files, but the king group's file set has 3. So no claim with T ≥ 2 has a usable (L3) certificate.

9. **Lemma 2.9's proof assumes "s has only its king", which is not in the hypotheses.** In the local game the defender may have pawns on the neighbouring files that the attacker's pawns can capture, which takes them off file f. The uses in 7.2 and Z_72 are unaffected (the defender has no pawns there).

10. **Evidence does not match claims.**
    - Conjecture 4.7 cites a search over ≤ 3+2 pawns; Appendix A describes ≤ 2+2.
    - §5.1 claims (L1) for every budget with T up to 7, but the scratch run covers only k ≤ 4 or ∞; k = 5 and 6 differ from ∞ when T ≥ 6.
    - §5.5 omits Black's fourth legal king move, Kd3.

11. **Labels and definitions.**
    - Claims with no label: all of §5.5, the §5.6 chain (μ_W = 5, T = 5, "(L2) fails by one tempo"), and "So Z_onT1 realises on".
    - §5.2's heading "White's sorties are not punished" states as fact what is only proved as "(L1) fails".
    - "Frozen in the convention. PROVED (diagram audit)" has no proof in the note, against its own rule for PROVED.
    - P11 uses `o(W(X))` and "hereditarily sum-safe" without defining them.
    - There is no item 4.4.
    - Proposition 4.3's corollary ("king tempo is 0 or ∞") is broader than what it proves, which only covers king steps inside the group's files.

12. **Content required by `RESEARCH_PLAN.md` item A8 is missing.** There is no CGSuite modelling, opposition is only deferred (§8.3), and the re-examination of Gafni's K+P vs K values is only deferred (§8.5).

**Verdict:** no solver defect. The one-move-punishment results (P1, P2, P3, P5 Black-to-move, P7 Black-to-move, P8, P9, P10) look sound, and kpsolve confirms them wherever it was run. The note is not ready under its current labels: items 1–3 need fixing before the theory sections can be called PROVED, item 5's headline should be restated, and items 6–12 are labelling, scope and wording fixes.

## Review 2: refuter (one theorem cluster)

# Referee report: LOOPY.md, Section 1 and Theorem 2.4

I found three false statements (Theorem 1.11(b), Proposition 1.13 as written, Theorem 2.4(a) for its "P-game of the context" option), one false identification (S(X) = cylcgt) that leaves a gap in Theorem 1.14(ii), and several minor problems. Theorem 1.14(i) holds as stated.

**Tools used.** All solver runs used `--board cyl:7x6 --ep on --promote QRBN --cap 1`. The binary was a private temp build, since deleted. Abstract D-game checks were brute-forced with throwaway scripts in `/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/ref/dg*.py`. Below, e means a position with no options.

## Problems, most severe first

**1. Theorem 1.11(b) and the threat set τ of Definition 1.10. Fatal.**
- **What is wrong:** τ counts only Left options to ⊕ and Right options to ⊖. It does not see suicides (a Right move to ⊕, a Left move to ⊖).
- **Where the proof breaks:** the step "coordinate j had a + threat" fails when ⊕ is entered by Right.
- **Counterexample:** y₁ = {e | ⊕}, y₂ = {e | ⊖}.
  - τ(y₁) = ∅ and τ(y₂) = {−}, so the pair is pairwise safe.
  - M_L = M_R = 2.
  - For every B ≥ 3 (checked at B = 3, 10, 100), the frontier after Right plays y₁ → ⊕ is B + {0 | −B}. That is 𝓝, not 𝓛: Right moving first plays −B, and Left loses at 0.
  - So the pair is not first-event dominant, although (b) says it is.
- **How common:** 1,488 of 3,641 random sums that pass this pairwise-safety test fail dominance at the root.
- **What survives:** the final outcome claim, o(Σ y^B) = D-result, did not fail in about 22,000 random sums where the two definitions of τ differ. It may be true, but it is unproved.
- **Citation:** the claim that this is "L2.1 of `notes/lemmas.md`, restated" is inaccurate. In lemmas.md (Definition 2.0, and `common.threats`), τ counts passers created by either side.
- **Fix:** τ ∋ + iff some reachable position has a ⊕ option for either player, and likewise for −.
- **Why it matters here:** Z itself is suicide-only. Under this τ, τ(Z) = ∅.

**2. Definition 1.5 ("S = D(X)^B … This is `cylcgt.pawns.value`"), the remark after Theorem 1.9, and Theorem 1.14(ii). Fatal for the identification; gap for 1.14(ii).**
- **What is wrong:** cylcgt splits components again at every node (`_child` → `value` → `components`). A passer in one sub-part therefore does not end its sibling. Definition 1.4's translation of a single D-game does end it.
- **Counterexample:** flat 7×6, e.p. on, count rule, `W: b2 d3 f2 / B: c4 c5 e5 g5`.
  - It is one component.
  - Re-run via `lemmas.common`: o(S) = 𝓝 and o(W) = 𝓡.
  - By Theorem 1.9, o(D^B) = o(D) = o(W) = 𝓡. So S ≠ D^B.
- **Consequences:**
  - "In one component the convention cannot go wrong" is false for cylcgt. Trouble needs a later split (L2.3), not two components.
  - (V4), as stated on the fixed top-level tuple, holds trivially for any single-component X, yet o(S) ≠ o(D) there. So 1.14(ii) does not follow from 1.11(a) for cylcgt.
  - "The test 'hereditarily sum-safe' there is pairwise safety" is wrong in two ways: HSS re-checks the re-split components, and it uses the either-player τ.
- **Fix:** require (V4) hereditarily, on the re-split components of every reachable position (HSS), with the corrected τ.

**3. Proposition 1.13. Fatal as written; a one-symbol fix repairs it.**
- **The notation:** Definition 1.1 makes ∅ a position with no options. That is why A′ = {∅ | ⊖} is translated as {0 | −B}.
- **Chess semantics, under that reading:** White plays A′ → ∅ and Black has no move. So A′ ⊞ R_n is 𝓝 for every n, not 𝓡.
- **BIG translation:** the proof omits Left's option to 0 in {0 | −B}. Computed at B = 3, {0 | −B} + n is 𝓝 for n ≤ B and 𝓛 for n ≥ B + 1, not 𝓡/𝓟/𝓛.
- **What is true:** the stated regimes hold for A′ = { | ⊖}, whose translation is { | −B} = −B − 1.
- **Knock-on:** Proposition 1.12 uses Definition 1.1's reading and is correct. So 1.12 and 1.13 read ∅ differently.

**4. Theorem 2.4(a) with G = "the P-game of the context". Fatal for that alternative.**
- **The unjustified step:** "since G has no draws". The P-model keeps stalemate as a draw. A context in which the side to move has no pawn move is therefore drawn alone, but inside G ⊞ Z that side must make a punished Z-move.
- **Counterexample:** cyl:7x6, `Ka4 Pb3 Pe3 kc3 pb4 pe4` (Z_T + H0).
  - G = {Pe3, pe4} has no move for either side, so it is (D, D) under P's rules.
  - `--frozen` gives (L, W). There the hypothesis of (a) holds by fiat: king moves lose, and the Z-pawns have no moves.
  - With real kings, White to move is L (exact).
- **Fix:** restrict G to normal-play scoring, or to games with no draws.
- **Minor wording:**
  - "At every reachable (Y, s)" is false literally at positions reached after a Z-move (Z in another state).
  - G ⊞ Z is not defined when G is a D-game and Z is a chess group.

**5. Theorem 1.14(ii), (V4). Gap.**
- **What is wrong:** it is not said whether Z is a coordinate of X.
  - **If it is:** after a Black Z-suicide, dominance needs +B + Σ G_i^B ∈ 𝓛. This fails whenever Black, moving first, can reach −B in some component.
  - **With the note's τ:** τ(Z) = ∅, so pairwise safety cannot see this.
  - **With the corrected τ:** τ(Z) = {+, −}, so pairwise safety fails as soon as any component has a threat.
- **Fix:** state (V4) for ⊞ G_i with Z deleted. S scores Z as 0, and Z^B = {−B | B} = 0.
- **Proof citation:** the proof should cite (i) as well as 1.11(a).

**6. Theorem 1.14, sharp form. Gap (wording).**
- **What is wrong:** "(V3) needed only for terminals reached". A loser's Z-move that is not punished is not a terminal, so, read literally, nothing is required of it. Then the Lemma 1.7 reduction and "D is short" both fail.
- **Example of a loser with no G-move whose Z-move is not a suicide:** `Ka5 Pb4 Pc5 Pe3 kc6 pb5 pe4`.
  - kpsolve gives (W, W), exact.
  - ⊞ G_i = H0 = 0 says White to move loses.
  - White's legal Z-move Ka6 is not a suicide; White wins.
- **Fix:**
  - Require that every legal Z-move of the loser, at every loser-to-move node of the strategy, is a P-loss for the loser.
  - Drop "Z deleted" and "no draws" from the sharp conclusion.

**7. The "Each hypothesis is needed" table. Minor.**
- **(V1b) row:** the witness P1a also violates (V3) with real kings. Ka6 and Kg4–g6 are legal Z-moves that are not suicides.
  - The isolated (V1b) failure does exist in the frozen model. `--frozen` gives `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` as (D, D), with every king move L, while normal-play +1 says (W, W).
- **(V1a) row:** king sorties are really a (V2)/(V3) failure.

**8. (A_Q) and the P-model of Definition 1.5. Minor.**
- **(A_Q) as phrased universally is false:** `Ke2 Pb5 ka5 w -` is a P-win (b6=Q at once; `--frozen` gives W) but a chess draw (exact D; every move draws). So 1.14(iii) is only a per-position tautology.
- **Two different P-models:** Definition 1.5's P counts any promotion as a win. The scratch solver ("queen safety required") and (L1) use a stricter P.

**9. Definition 1.10. Minor.**
- M_L of a sum is ambiguous (stop at the first terminal, or add up the components). The bound argument works either way.
- "≤ 6p ≤ 48" assumes p ≤ 8 and ignores a final Z-move.

**10. Definition 1.5 versus the setup of 1.14. Minor.**
- Definition 1.5 makes "a punished move in the king group" the Z-terminal. The setup of 1.14 makes every move inside Z one.
- In (V1a), "same resulting positions" is ill-typed for terminals.

## Checked with no defect found
- **Lemmas 1.6 and 1.7:** the strategy and fixed-point arguments hold, for loopy D-games too.
- **Theorem 1.9.**
- **Theorem 1.11(a).**
- **Proposition 1.12:** correct under either reading of ∅.
- **The D-model on en passant and checks:**
  - Under (V1a), condition (E) carries over to the D-sum: rights are local, and unusable stale rights do not change any options.
  - No check can arise before the first decisive event: Z is static, and context pawns never attack F_Z.
- **Theorem 1.14(i):**
  - A loser with no G-move has a legal move by (V1b). That move is a Z-move, which (V3) makes decisive and (V2) makes a P-win for σ.
  - D is short, so draws are excluded.

## Verdicts
- Definitions 1.1–1.5: GAP (the S = cylcgt identification is false; ∅ is used two ways; P counts unsafe promotions)
- Lemma 1.6: SOUND
- Lemma 1.7: SOUND
- Theorem 1.9: SOUND (the remark after it is false for cylcgt)
- Theorem 1.11: FALSE ((b) fails: suicide-blind τ; (a) is sound)
- Proposition 1.12: SOUND
- Proposition 1.13: FALSE as written (true with A′ = { | ⊖})
- Theorem 1.14: GAP ((i) sound; (ii) gap from items 1, 2 and 5; (iii) tautological)
- Theorem 1.14, sharp form: GAP (wording lets non-suicide loser Z-moves through)
- Theorem 2.4: FALSE as stated for the P-game alternative (draws); sound for normal-play G with no draws

## Review 3: refuter (one theorem cluster)

**Referee report: LOOPY.md §2, Definition 2.5 to Remark 2.11**

**1. Prop 2.10(a): FATAL (the statement is false on 4-rank boards)**
- **What is wrong.** The step "an s-pawn that can promote in one move stands on its seventh rank" fails when H = 4. SPEC §3 allows 4 ranks, and there a pawn on its 2nd rank promotes by a double step onto the last rank. Such a pawn need not be passed, and the note never assumes H ≥ 5.
- **Counterexample (cyl:7x4).**
  - Layout: F_Z = {a,b,c}, buffer {d,g}. The context on {e,f} is Pf2 / pe3 pf3. cylcgt `passed()` is false for all three pawns, so the context is non-terminal.
  - Group: Kb4 Pb3 / kc2 pc3, Black to move. The Z-move is m = ...Kc1, and the punishing reply is r = Kxc3.
  - Q_Z = Kc3 Pb3 / kc1 (Black to move). Black has only Kb1 or Kd1, then b4=Q follows, guarded by c3. So (L1) holds with T = 1 for every k, and (L3) holds.
  - But μ_Black = 1. After Kxc3, Black plays e3–e1; after fxe3, Black plays f3–f1. White cannot promote at once, because its own king stands on b4. So in P, Kc1 is not punished.
  - Solver check, kpsolve cyl:7x4 --promote Q --cap 2 (bounds agree, so exact). Input file: `/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/ref_sec2/h74.txt`.

    | Position | Result |
    |---|---|
    | `Kb4 Pb3 Pf2 kc1 pc3 pe3 pf3 w -` (after m) | L L |
    | `Kc3 Pb3 Pf2 kc1 pe3 pf3 b -` (Q) | L L |
    | `Kc3 Pb3 kc1 b -` (Q_Z) | W W |

  - With the default QRBN set at cap 1 the bounds disagree, so C is open there; P is decided by inspection.
- **Fix.** Assume H ≥ 5, or exclude pawns on their 2nd rank with a free double step. For H ≥ 5 the argument is right for context pawns: they cannot promote by capture, and rank H can hold no enemy pawn.
- **Minor.** μ_s in (L2) also counts s's Z-pawns, but the proof only discusses context pawns. If s has a Z-pawn on its 7th rank whose promotion square m or r vacates, then μ_s = 1 in every context. Such a punishment also fails (L1), but only if the local game counts an s-promotion as a failure for s̄ (see 3b).

**2. Definition 2.6, (L3′): GAP**
- (L3′) does make s's king moves the same in the real position as in Q_Z. It does not give (L3).
- (L1) "for every k" gives a separate strategy σ_k for each budget. In reality the budget is not fixed: s decides as it goes how many context moves it makes and how fast the supply runs out (single step versus double step, captures).
- Under the k = ∞ strategy, s can be steered into positions where its king has no move and only passes remain, while the real context has none left. Deriving (L3) from (L3′) needs one strategy that wins against every way the passes can run out, and (L1) as written does not provide it.
- For T = 1, (L3′) together with (L1) at k = 0 does imply (L3).
- **Also minor:**
  - (L1) does not say what an s-promotion, a checkmate of either side, or en passant means in the local game. Only Appendix A says a defender promotion is an attacker failure.
  - "Every k is needed" is false for Thm 2.7, which needs only k = ∞ plus (L3) (see 3a).

**3. Thm 2.7: GAP** (the statement looks true, but the written proof has holes)
- **(a) Quantifier order.** "(L1) at the actual budget" assumes the budget is fixed in advance, which it is not. Repair: use σ_∞. Every real move of s maps to a legal local move with unlimited passes, and (L3) excludes real stalemate. With that repair the finite-k clauses are never used.
- **(b) The μ_s lower bound is false.** "The removed Z-pieces of s̄ could only slow s down" fails because s̄'s Z-pawns are capture targets.
  - Example on 6 ranks, s = White to move in Q: Kc5 Pc4 / pd5.
  - With s̄'s pieces removed, μ = 3 (king off c5, then c5, c6). In reality cxd5 and d6=Q take 2 moves.
  - The theorem survives only if (L1)'s game ends as an s̄ failure when s promotes, which Definition 2.6 does not state.
- **(c) Checkmate.** "s cannot checkmate s̄ … its context pawns never attack F_Z" ignores s's Z-pawns, which do attack F_Z. The correct reason: σ_Z has a legal move on F_Z at every turn, and s̄'s real moves include its local ones. This also needs the unstated local rules.
- **(d) Passes when s is in check (minor).** The clause "unless it answers a check given by a context pawn" is vacuous: s̄'s context pawns never move during the window, s's king cannot step into their attack, and s is not in check at Q. Passes do model context moves correctly: when s is in check, the checker is a Z-pawn on F_Z, which no context pawn can capture.
- **Deleting context pawns (asked) is sound.**
  - Every real king move of s is legal in Q_Z, so deletion only adds options for s.
  - s̄'s context pawns are fixed and σ_Z never uses them.
  - s's context pawns never stand on or attack F_Z, so they cannot block or check s̄'s confined king.
  - The only way deletion favours s̄ is by removing a real stalemate, and that is (L3)'s job.

**4. Lemma 2.9: GAP (hidden hypothesis)**
- The proof uses "s has only its king", but the hypotheses restrict only s̄'s pawns. If s has a pawn on f±1, then "pass forever" lets an s̄ pawn capture and leave f. Example: Kc1 Pb3 / pc4; White passes, then ...cxb3.
- I found no counterexample to the statement itself. An exhaustive local search on the 7×6 cylinder (scratch, my own code, defender passing freely, punisher's king unconfined) covered: 1–2 s̄ pawns on the c-file at ranks 2–4, s's king on c in front, and s with either 1 pawn on ranks 3–5 or 2 pawns on the b/d files. It found 0 forced promotions. Code: `.../ref_sec2/blockade.py`, `blockade2.py`.
- A plausible repair: "pass, but capture any s̄ pawn that attacks an s-pawn", plus an induction. The §5.2 and P5 applications are unaffected, because s has no pawns there.

**5. Prop 2.10(b): SOUND, minor mislabel**
- The example is correct: no passer, and μ = 2 via fxg(H−1) then promotion.
- "The zero of such a group is context-dependent" is not proved. It is exactly the CONJECTURE stated in the next bullet, and §0 repeats it as fact.
- The construction also needs room: board width ≥ |F_Z| + 4.

**6. Remark 2.11: GAP**
- It carries no label, against the note's "every claim has exactly one label", and gives no proof.
- Definition 2.6 cannot apply as written:
  - Q_Z deletes "every context pawn", which deletes the passer itself.
  - r is not a king capture.
  - The passer's owner may need its king off F_Z, where the legality step via Lemma 2.2 no longer covers it.
  - The pawns of the passer's own component are not addressed.
- "Which this certificate rules out" is therefore unproved, and P11 in §6 relies on it under a PROVED label.

**7. Cor 2.8: SOUND**
- The timing, double-step, queen-safety and pass arguments are correct, and the strategy is the same for every budget.
- Minor: with the defender to move, d ≥ D + 2 is exactly the classical rule of the square, not a "two-square margin" on top of it.

**Verdicts**
- Def 2.6: GAP ((L3′) does not imply (L3) for T ≥ 2; local-game outcomes unspecified)
- Thm 2.7: GAP
- Cor 2.8: SOUND
- Lemma 2.9: GAP
- Prop 2.10(a): FALSE (H = 4); sound for context pawns when H ≥ 5
- Prop 2.10(b): SOUND (minor mislabel)
- Remark 2.11: GAP

Other test inputs are in the same folder (`h4.txt`, `h4b.txt`, `h4c.txt`, `h4d.txt`); the temp solver build is `ref_sec2/kp`. No project files were changed.

## Review 4: refuter (one theorem cluster)

**Referee report: LOOPY.md, Sections 3–5 (Theorems 3.3, 3.4, Corollary 3.5, Theorem 4.2, Propositions 4.3, 4.5–4.6, applications 5.1–5.6)**

Every position I could test came out exactly as claimed. The only false statement is the first sentence of Proposition 4.3. Theorem 4.2 has real proof gaps; the rest are minor.

**How I checked.** I built the solver at `/tmp/kp_check_12161` from `kpsolve.c` and ran it with `--board cyl:7x6 --ep on --promote QRBN --cap 1 --moves`. All results were exact (bound A = bound B). The run files are in `/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/ref/` (`z.out`, `b1.out`, `b2.out`).

- I first started one batch that included the two 6-pawn stalemate positions, which is over the 5-pawn limit. I killed it before it produced output.
- So the 6-pawn trap P1a was checked by hand plus a 5-pawn variant. The 8×6 and 8×8 claims were checked by hand only.

| Position | Solver result | Agrees with note |
|---|---|---|
| Z_onT1 `Ka5 Pb4 Pc5 kc6 pb5`, also with `Ka6` | (W,W) in both shuttle states. Black's only move is Kd5. White's moves are Ka6 (or Ka5) and Kg4/g5/g6 | yes |
| Z_offT1 `Kc1 Pb2 ka2 pb3 pc2` | (L,L). White's only move is Kd2. Black has Ka1 and Kg1/g2/g3 | yes |
| P2 + H*, + H\*2, + H0 | (W,W) in all three | yes |
| Trap without Pe2 (`Ka5 Pb4 Pc5 Pe4 kc6 pb5 pe5`) | (D,D). Black has no legal move; all four White moves draw | yes (P1a mechanism) |
| P9 | (W,L). White wins only by exf3; Black wins by fxe2 or f2 | yes |
| Z_72 bare | (D,W). Kd5 is the only losing White sortie, the analogue of 7.2's Kf7 | yes |
| P8, 6-rank 7.3 analogue | (W,W). b6=Q wins at once | yes |
| Z_T bare | (L,W) | yes |

**Problems found**

1. **Proposition 4.3, first sentence — FALSE as stated (fatal for that sentence, easy to repair).**
   - The claim: after s plays a non-capturing king move u → v inside F_Z and the opponent replies outside Z, the move v → u is legal.
   - This fails when s was in check on u. The proof step "u is not attacked by an opponent Z-pawn, since none has moved" does not follow. What it needs is "u was not attacked while s's king stood there", which is exactly the missing hypothesis that s was not in check.
   - Counterexample: `Kb2 Pc2 kc4 pc3`, White to move and in check from c3. White plays Kb2–a1, Black moves outside Z, and Kb2 is now illegal. The solver confirms that `Ka1 Pc2 kc4 pc3 w -` lists only Ka2, Kb1, Kg1, Kg2.
   - A second missing condition: the opponent's reply could be a promotion. Lemma 2.2 only holds before the first promotion, and a new officer can attack u or give check.
   - The "frozen opponent" consequence needs the no-check condition at the root as well.

2. **Proposition 4.3, the dichotomy "king tempo is 0 or ∞, never finite n ≥ 1" — gap.**
   - **Steps out of F_Z are not covered.** The proof handles steps inside F_Z only, but the conclusion says "any one safe king step". A step onto a buffer file (for example Z_onT1's Kg4, Kg5, Kg6) can later be taken away by a context pawn, because Lemma 2.2 lets context pawns attack buffer squares. Such a supply of passes depends on the context and is neither a fixed 0 nor ∞.
   - **"Safe" is not defined.** It has to mean that the opponent is still frozen at the new Z-state v. §5.5 shows this can fail: in Z_on with the White king on a3, Black gains Kb5.
   - **A third case exists.** A king move can be neither a suicide nor a pass: it unfreezes the opponent without losing. The dichotomy only holds among pure reservoirs.

3. **Theorem 4.2(a) — gap.**
   - Definition 4.1 allows R_n to contain Black suicides. In that case "pairwise safety in G plus B > n + max M" does not give first-event dominance.
   - Example: G = {∅ | ⊖}, n = 1, with Black suicides at ρ₁ and ρ₀. At the frontier, B + G^B = B + (−B−1) = −1, which is in 𝓡, so dominance fails for every B.
   - The cause is inherited from Theorem 1.11(b), which is outside my cluster. Its proof assumes the coordinate that produces ⊕ carries a + threat. That is false when the ⊕ comes from a Right suicide, because τ only counts Left options to ⊕.
   - The outcome still comes out right in this example, and {n−1 | B} = n whenever B > n. So the conclusion is probably true, but the proof route does not work. With suicides, the BIG translation is also not literally "n".

4. **Theorem 4.2(b) — minor gap.**
   - It deletes Black's suicides using Lemma 1.7, which is a statement about D-results, but then concludes a CGT equality. In CGT, {i−1 | B} = i only when B > i.
   - It also never proves, in D-semantics, that a branching Left-only acyclic group is equivalent to R_ℓ. It cites CGT dominated-option deletion instead.

5. **Theorem 4.2(c) and the closing sentence of §4 — minor.**
   - The proof separates on_D from the integers n ≥ 0 only. Negative integers need a separate (trivial) test.
   - "Is on_D" needs Proposition 3.2's bisimulation hypotheses and needs the cycle to be reachable.
   - "Finite exactly when non-reversible" mixes up "acyclic" with "non-reversible": a 3-cycle has no immediately reversible move.

6. **Two-sided shuttles — minor gap.** The §3 paragraph "With shuttles on both sides…" is labelled PROVED by Theorem 3.4, and §5.3 says the group "would be dud-type". Both rely on a two-sided version of Proposition 3.2 that is never proved. Two shuttles behave as dud only if each side's shuttle stays legal, and each side stays frozen, in all four combined king states.

7. **Proposition 3.2, chess bridge — minor.** It leaves out condition (V1a): Black's legal chess moves in the context must be exactly G's D-options. The solver shows this matters. In P2 + H*, White's single step e3–e4 draws (it stalemates Black). The §6 notes mention only H\*2's double step, and their sentence "none of them puts a pawn on e4" is inaccurate for H*. The prediction itself survives, because the winner simply avoids that move.

8. **§4 commentary — minor.**
   - "Typically a pawn move by Proposition 4.3" does not follow. Proposition 4.3 assumes a frozen opponent that replies outside Z, but in an over-group the opponent shuttles inside Z.
   - Conjecture 4.7 cites a search over "≤ 3 + 2 pawns", but Appendix A describes a search over "≤ 2 + 2 pawns".

9. **§5 labels and wording — minor.**
   - **5.1:** "Frozen… PROVED (diagram audit)" puts the proof outside the note, which breaks the note's own label rule. My hand enumeration agrees: each king has five moves and each drops its pawn, and self-duality checks out. Separately, "(L1) for every pass budget" is broader than the scratch run, which covered budgets k ≤ 4 and ∞ only. With T up to 7, budgets 5 and 6 are unchecked; k ≥ 7 is equivalent to ∞ inside a 7-move window.
   - **5.2:** Lemma 2.9 only proves that the certificate fails for the reply Kxd7. "Sorties not punished" in full rests on scratch evidence. Also, in 7.2 + H, Black's only Z-move Kc7 lands on the buffer file c, where an H-pawn on b6 would cover it and risk stalemate. That is covered by "modulo (V1)".
   - **5.5:** "(V2) fails; not an on-group" rests on scratch evidence but carries no CONJECTURE label.

10. **Citations.** The claims sourced to `notes/lit_cgt_chess.md`, `notes/diagram_audit.md` §C.3, RESULTS §1 ("41 of 449 king moves draw and 7 win") and the engine-suite README (Ke6! Kxg4 Kxd6) all say what the note claims. In §5.6, μ = 5 = T is right, so (L2) does fail by one tempo.

**What holds up.**
- **Theorem 3.4:** the stage argument shows a winning first move is never a pass. The recursion is well-founded and determines the least fixed point, so draws are properly handled rather than asserted. Play in (b) is finite, with every two plies strictly decreasing.
- **Theorem 3.3, Corollary 3.5, Propositions 4.5 and 4.6:** I found no flaw.

**Verdicts**
- T3.3: SOUND
- T3.4: SOUND
- C3.5: SOUND
- T4.2: GAP
- P4.3: FALSE as stated (check counterexample); still a GAP even after the no-check repair
- P4.5: SOUND
- P4.6: SOUND
- §5.1: SOUND (label misuse only)
- §5.2: SOUND for the PROVED parts
- §5.3: SOUND
- §5.4: SOUND (move lists and results confirmed by the solver)
- §5.5: label gap only
- §5.6: SOUND
