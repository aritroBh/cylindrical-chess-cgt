# K21 referee report (independent verification)

Referee: independent agent, 2026-10-27. Verdict: **ACCEPT WITH FIXES**.
All the mathematics (T3.7, Lemma 3.8a, T3.8, Cor 3.8b, P3.9, P3.10, T3.11, Cor 3.11a) survived: every proof step was
re-derived against the definitions in LOOPY, and none of well over 100,000 independent state or instance checks found a violation.
The refutable content is in the **wording** of three places in EDITS.md (P3.12 and "no translation" claims) plus
one dangling label. Those must be corrected before the EDITS are applied. The chess part is confirmed only by recounting the
agent's own result files and three hand derivations; the P-model oracle could not be re-run (shared lock never freed).

Everything below was done with my own code in `K21/verify/` (`ref.py` is a from-scratch solver; it was not derived from
`K21/scripts/`). Python: `PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames .venv/bin/python`, run from `K21/verify/`.

## 0. How the evidence was produced

* `ref.py`: components are (L, R) option lists with terminals `P` = ⊕, `M` = ⊖; the D-sum, the loopy-CGT translation
  (integer chains +B / −B), least fixed points by counter-based retrograde analysis, dominance, reserves, criterion,
  stopper test. Written from the LOOPY definitions.
* **Solver agreement (third implementation).** `xcheck.py`: my solver against K21's `dsum.py` on 1,500 random instances
  (2-3 components, up to 4 nodes, loopy or short, with terminals, B in {1,2,4,6}): D-result and CGT outcome at every reachable
  tuple, both movers, **20,324 states, 0 disagreements**, plus dominance and the reserve criterion on all 1,500 instances,
  0 disagreements. So the K21 solver label CHECKED-2 is honest (it is now agreed by three code bases).
  Caveat: the K21 all-states C cross-check (`summary.json`, 47,896 states) reports 0 instances with D ≠ CGT and 0 draws, so
  it exercises the agreeing regime only; the differing regime is covered by the root cross-checks (1,169 and 557 instances
  with D ≠ CGT) and by my run.

## 1. Proof review (each step checked against Definitions 1.1-1.4, 1.10 and Theorems 1.11, 3.3, 3.4)

| Claim | Proof check | Verdict |
|---|---|---|
| **T3.7 bridge** | Both directions re-derived. (⊆) by 𝒟-stage: σ-node with a σ-terminal option goes to a σ-frontier, a σ-win by dominance; σ̄-node in W_σ has no σ̄-terminal option, each other option is a σ-frontier or a lower stage. (⊇) by 𝒞-stage: a winning frontier option has sign σ because a σ̄-frontier is a σ̄-win and W_L ∩ W_R = ∅ in 𝒞. Nodes without options correspond. Draws agree (infinite play on both sides). No missing case; no shortness or stopper hypothesis is used. | **PROVED (confirmed)** |
| **Lemma 3.8a** | Stage argument fine: a Right-to-move stage-k node has all options at stage ≤ k−1, a Left-to-move stage-j node has an option at stage ≤ j−1, so Φ drops ≥ 2 per round; Left's reply stays in the component Right moved in and uses only that component's tokens; at Φ = 0 Right has no option. Monotonicity in tokens is clear. | **PROVED (confirmed)** |
| **T3.8** | Frontier B + R: Right to move cannot move in the stack, so it is "R + B second", a Left win since R + Λ is; Left to move plays B → B−1. The case σ = − is the mirror. The quantification is right: any combination of reachable coordinate nodes is a reachable tuple. (a) λ_B(y) ≤ M_R(y) when no ⊖ is reachable: checked by hand and on 12,717 node instances (0 violations). (b) the reserves of {∣⊕}, {⊖∣} are all 0 (recomputed) and the D-result (L,W) is the outcome of 0. (c) correct as a statement about **dominance** (9,592 random cases with an infinite reserve opposite an event: dominance never holds), but see fix F3: it does not say anything about D = CGT. | **PROVED (confirmed)**, with F3 |
| **Cor 3.8b** | Arithmetic checked: events only in K, Λ(S) + Σ Λ_B(K_i) ≤ Λ(S) + M_R(K) ≤ B−1. 721 random instances (591 with events), 0 failures; the on/off remark (S = on when K has no ⊖ event, S = off when no ⊕ event) tested on 1,810 instances, 0 failures. | **PROVED (confirmed)** |
| **P3.9** | All five pairs recomputed by solver (B = 4): on (0,∞), off (∞,0), over (0,1) at its root (the node 0 inside it has (0,0)), under (1,0), dud (∞,∞). Hand proofs check. | **PROVED (confirmed)** |
| **P3.10** | Argument fine (short moves finitely many, the tail alternates in S, a stopper has no such tail). 1,277 random stopper instances, 0 draws; random non-stoppers draw in 320 of 1,223 (the rate depends on the generator; K21 found 1,315 of 3,335). | **PROVED (confirmed)** |
| **T3.11 sandwich** | All three parts re-derived. (1) copy of a K⊞off strategy: off has no Left move, real Right moves in S are virtual passes, S has no Right ⊖; (2) Left's S-moves become passes in `on`, Right's options only shrink; (3) a Left pass entering at stage n gives a contradiction (the Right pass is always available in K⊞dud). The hypothesis "no Left ⊕ / no Right ⊖ in S" is exactly what is used. 6,150 instances (21,134 + 21,226 + 1,014 states; about 1,530 of them with suicide-only S), 0 violations of the four inclusions and of W(off) = W(dud), L(on) = L(dud). | **PROVED (confirmed)** |
| **Cor 3.11a** | Immediate. The closing sentence ("in T, W(K⊞S) ⊆ ¬P_R and L(K⊞S) ⊆ ¬P_L") is vacuous (T ⊆ ¬P_R already); harmless, but it is not content. | confirmed |
| **P3.12** | The body is right: translation of K^B + on is constant 𝓛 (W), + off 𝓡, + dud a draw (27,666 + 26,172 (K, mover, reservoir) checks, B = 14 and 3, **0 violations**; the translation is right iff ∉ P_R (on), ∉ P_L (off), ∉ P_L ∪ P_R (dud)). **The summary-table row and the last sentence of the body are wrong**, see F1. | body PROVED; table row **REFUTED** as worded |

## 2. Counterexamples and numbers re-checked with my own code

All reproduce (script `ex.py`, `ex2.py`; B = 2, 5, 9 unless stated; results are (Left first, Right first)).

* `{⊕∣} ⊞ off`: D (W,W), CGT (L,L). `{⊕∣} ⊞ dud`: D (W,W), CGT (D,D). `{∣⊖} ⊞ on`: D (L,L), CGT (W,W). **Confirmed.**
  The favourable pairs `{⊕∣} ⊞ on / over` (W,W both) and `{∣⊖} ⊞ off / over / under` (L,L both): **confirmed**, dominance and criterion hold.
* `{∣⊕} ⊞ {⊖∣}`: D (L,W) = CGT (L,W) for B = 2, 5, 9, dominance and criterion true. **Confirmed.**
* **Tempo-regime guess refuted** (K = `{1 ∣ ⊖,1}` with 1 = 0; S: a: L→c, R→b,c; b: R→a,b; c: L→b,c). S is a stopper (checked on the
  (node, mover) graph). At (K,a), Left to move: K⊞off is (L,·), K⊞on is (W,·), so it is in the tempo regime; D-result **L**;
  translation **W** for B = 1, 2, 3, 14, 40. The two-line hand argument in EDITS is correct. **Confirmed (CHECKED-2 + hand).**
  Extra: my random search found an independent, equally small failure, K = `{⊕,0 ∣ 0}`, S = `{0 ∣ off}` (a stopper), Right to move at the
  root: D = W, translation = L for B = 1, 2, 5, 14 (K⊞on (W,W), K⊞off (W,L), so Right-first is in T). It could be added as a one-line second example.
* Criterion not necessary: `{∣⊕,0}` ⊞ `{⊖,0∣0}` (self loops): D = CGT = (D,D) for B = 3, 5, 7, dominance true, criterion false, and
  λ_5 of the second component = 5 = B. **Confirmed.**
* Non-stopper `{S,0∣S}` beside `{⊕∣}`: λ = (0, 0) at both nodes, D = CGT = (W,W), dominant. **Confirmed.**
* Counts of K21 (internal consistency of `summary.json`): 60 failures = 39+7+7+4+3; 28,581 tempo states with criterion violated; 40,380 with criterion true;
  8,646 for on/off/dud; 26,000 bridge instances split 4,671 + 22 = 4,693 dominant loopy-with-event cases. All add up. Not individually
  reproducible (other generator); the **qualitative** content reproduces: my own random search gave 0 criterion-true failures
  (3,594 criterion-true tempo states) and 1 failure in 6,882 tempo states with the criterion violated.

## 3. Independent randomised and exhaustive tests of the theorems (my generator, my solver)

All runs below: 0 violations. Generator: 1-5 node components, loopy allowed, both terminal signs on both players' options.

| Check | Instances / checks | Result |
|---|---|---|
| T3.7: dominance ⇒ D = CGT at every reachable tuple, both movers; criterion ⇒ dominance | 10,000 random (2-3 components, B = 1, 2, 4, 6): 1,778 dominant (1,646 with criterion), 0 violations (`tests1.py`, `logs_bridge.txt`) | 0 violations |
| same, exhaustive | all pairs of one-node components with options in {self-loop, ⊕, ⊖} (2,080 pairs, B = 1, 2, 3, 5): 268 non-vacuous dominant, 49 dominant without the criterion (`exh.py pairs`) | 0 violations |
| same, one-node × random two-node | 2 × 3,000 (B = 2, 4), 412 non-vacuous dominant | 0 violations |
| same, random triples of one-node components (1,200 of the 45,760; the exhaustive triple run stayed in the heavy.sh queue and was withdrawn) | 1,200 (B = 2) | 0 violations |
| T3.8(a) (short, pairwise safe, B = max(M_L,M_R)+1) | 641 safe (606 with events) | criterion, dominance, D = CGT all hold |
| Cor 3.8b | 721 (591 with events); 1,103 skipped for an infinite reserve | 0 failures |
| Lemma 3.8a, λ and ρ, B = 1 and 4 | 1,600 checks | 0 violations |
| T3.11 | 6,150 instances | 0 violations |
| P3.12 / T3.3(a) | 53,838 checks | 0 violations |
| P3.10 | 1,277 stopper instances | 0 draws |
| T3.8(c) (infinite reserve opposite an event) | 9,592 cases | dominance fails in all |

## 4. Required fixes (the labels are stronger than the evidence in these places)

**F1 (EDIT 1, row P3.12, and the last sentence of Proposition 3.12).** "the translation is right exactly in the tempo regime ... and wrong on
the forced positions of the side the reservoir favours" is **false** for `on` and `off`. The translation of K^B + on is always W; so it is right
on P_L (Left forces: D = W as well) and on T, and wrong exactly on P_R, the forced positions of the side the reservoir does **not** favour.
In my runs the `on` translation was right on a position of P_L in 2,894 + 2,677 cases and the `off` translation right on a position of P_R in 3,036 + 2,831.
Only for `dud` is "right exactly in T" true. Replacement text for the row:

    | P3.12 | For S ∈ {on, off, dud} the BIG/CGT translation of K ⊞ S is right exactly outside P_R (on), outside P_L (off), outside P_L ∪ P_R (dud): it is wrong exactly on the forced positions of the side the reservoir does not favour (of both sides for dud, where "right" is exactly the tempo regime). In general it can fail even in the tempo regime (3-node stopper, 2-node K) | PROVED; the last claim COMPUTED (and hand-checked) |

and, in the body, replace "So for these three the translation is right in the tempo regime, and wrong on the forced positions of the side that the reservoir favours;"
by "So the translation is right exactly outside P_R for `on`, outside P_L for `off` and in the tempo regime T for `dud` (wrong on the forced positions of the side that the reservoir does not favour);".

**F2 (EDIT 3, section 8 item 4, second bullet; EDIT 2, the last sentence of "Reading").** "an infinite reserve opposite a threat ... has no integer translation (Proposition 3.12)"
and "For a component with an infinite reserve opposite a threat no such value exists (Proposition 3.12)" are overbroad. What is proved is that **dominance** fails
(Theorem 3.8(c)) and that the translation is wrong on the forced positions P_R / P_L / P_L ∪ P_R. If the opposite-sign event cannot be forced the translation is
right although the criterion and dominance fail: `{⊖∣} ⊞ on`: D = CGT = (W,W); `{∣⊕} ⊞ off`: D = CGT = (L,L); `{⊖∣} ⊞ dud` and `{∣⊕} ⊞ dud`: D = CGT = (D,D), all for B = 2, 5, 9
(`ex2.py`). Suggested wording for the bullet: "an infinite reserve opposite a threat that the threatening side can force (on or off against the wrong sign, dud against both)
makes the translation wrong for every B on the forced positions (Proposition 3.12); an unforceable threat (a suicide) does not, although dominance still fails". The first
bullet of "What fails" has the same problem in its italic heading ("kills every B"); its three examples are all forcible threats and are correct.

**F3 (EDIT 2, Theorem 3.8(c)).** Heading it "Necessity" invites the reading "the criterion is necessary for D = CGT". It is necessary for **dominance** for one rest component only; add
"(for dominance, not for D = CGT; Proposition 3.12 and the example `{⊖∣} ⊞ on` show the translation can still be right)".

**F4 (EDIT 2, "What fails" third bullet).** "(CONJECTURE C1 refuted)": there is no conjecture named C1 in LOOPY.md (grep). The quoted sentence is self-contained, so drop the label:
write "(the guess is refuted)".

**F5 (EDIT 2, Corollary 3.11a, last sentence).** Optional: the clause "where W(K⊞S) ⊆ ¬P_R and L(K⊞S) ⊆ ¬P_L" is true but empty in T; either delete it or say that the inclusions
hold everywhere and are exactly Theorem 3.11 (the real content is that outside T nothing depends on S).

**F6 (optional, EDIT 3 OPEN (d)).** The conjecture "λ(S) = ⌈−RS(S)⌉ or one more" is untested and its marking "untested" is honest; it fails as stated for `on` (λ = 0, RS = ∞) but is
restricted to "finite reserve", so no change is needed. I did not test it.

## 5. Check of the three EDIT blocks

| EDIT | OLD occurs exactly once in the current LOOPY.md? | NEW accurate? |
|---|---|---|
| summary table: rows for the loopy sum theorems | yes (my own `chk_edits.py`, also after applying the earlier edits in order; 3 blocks, 3 OLD / NEW markers) | T3.7, T3.8, P3.9-P3.10, T3.11 rows accurate; **P3.12 row needs F1** |
| sums with loopy components: new Section 3 block | yes (the OLD is the heading `**What loopy kings do to the convention.**`, which the NEW text re-emits at its end, so nothing is lost) | accurate apart from F1, F2, F3, F4 (F5 optional). All 21 cross-references (Definition 1.1-1.4, 1.10, Theorems 1.11, 3.3, 3.4, Lemma 3.8a, Cor 3.5, 3.8b, 3.11a, Prop 3.2, 3.9, 3.10, 3.12, 4.6) resolve in the edited file |
| section 8 item 4: status | yes | accurate apart from F2; "OPEN" list is honest |

Applied in order, the three EDITs give a file of 202,492 characters (was 177,931).

## 6. Chess instances (P model)

* **Recount of the agent's own files** (`count_chess.py`, no solver): 24 base contexts, 21 agree (Z_on 15/18, Z_off 6/6); 80 random Z_on contexts, 64 agree; so
  79 of 98 Z_on contexts agree. The 19 differences split as claimed: 13 in White's favour (P result ≥ prediction), 5 draws where D predicts a decision, 1 worse for White
  (`Pe2 Pe3 pe4 pf3 pf4`, (W,L) → (L,L)). **Confirmed by recount.** The direction claims (13 / 5 / 1) are correct from the listed pairs.
* **Prediction side spot-checked by hand** (own derivation of the pawn D-game, not the agent's code): `Pe2 pf3`: White options {e2xf3 → ⊕, e3 → ⊖ (Black races: 2 moves vs 3)},
  Black options {f3xe2 → ⊖, f2 → ⊖ (1 move vs 4)}, so K ⊞ on_D = (W,L), which agrees with P9 and with the file. `Pe2 pe3` (frozen context) gives (W,W) as listed. `Pe4 pf5`:
  White {exf5 → ⊕, e5 → ⊕ (1 vs 4)}, Black {fxe4 → ⊖, f4 → ⊕ (2 vs 3, White to move)}, prediction (W,L) as listed, and the P model differs ((W,W)) as claimed.
  The `Pe4 pe5` stalemate explanation is right (Black king on c6 has no move: b6 and d6 attacked, c5 protected, d5 covered by e4; pb5 is blocked).
* **kpsolve cap 1: not run** by the agent, honestly labelled. I also did not obtain kpsolve results.
* **P-model re-run: NOT CHECKED.** I built `kp_p` from `K7/scripts/draft/kp_p.c` and queued a 12-position sample (6 contexts, both movers, including the three
  disagreements) through `heavy.sh`; both lock slots were held by other kings/ jobs for the whole 25 minutes (holders running 1 h 17 min and 51 min), so the run never
  started and I withdrew it (only my own queued PID was killed). The P-model numbers are therefore **recounted from K21's own result files, not re-solved**. The
  prediction side was re-derived by hand for three contexts (above). Reproduce when the lock is free:
  `kings/delegate/heavy.sh ./kp_p --board cyl:7x6 --pmodel --ep on --promote Q --cap 0 < K21/chess/positions_all.txt`, then `K21/verify/count_chess.py`.

## 7. Label audit

| Claim in the agent's summary | Label given | My verdict |
|---|---|---|
| T3.7 | PROVED | PROVED, confirmed |
| T3.8 | PROVED; COMPUTED-1 | PROVED, confirmed; criterion ⇒ dominance ⇒ equality: my 10,000 + exhaustive: 0 violations |
| Cor 3.8b | PROVED; COMPUTED-1 | confirmed |
| P3.9 / P3.10 | PROVED; counts COMPUTED-1 | confirmed |
| T3.11 | PROVED; COMPUTED-1 | confirmed |
| P3.12 "right exactly in the tempo regime" (as summarised: "for on, off, dud the translation is right exactly in the tempo regime") | PROVED; COMPUTED-1 | **REFUTED as worded** for on and off (right also on the favoured side's forced positions); correct form: right exactly outside P_R / P_L / P_L ∪ P_R. The agent's own `claims` entry for P3.12 states the correct form; the EDIT text and the one-line summary do not |
| "an infinite reserve opposite a threat gives no translation for any B" | PROVED / COMPUTED (CHECKED-2 at roots) | **overbroad**: true for forcible threats (the three examples), false for suicides (F2) |
| tempo-regime guess false | COMPUTED-2, hand-checked | CHECKED-2 + hand: confirmed; the 60 / 28,581 statistic is not reproducible bit-for-bit (my generator found 1 / 6,882) but the qualitative statement reproduces |
| criterion sufficient, not necessary | COMPUTED-1 | confirmed |
| solver Python vs C | CHECKED-2 | confirmed (third implementation agrees on 20,324 states); the all-states sample is thin in the D ≠ CGT regime |
| chess P-model 21 of 24, 79 of 98 | COMPUTED-1 (P model) | recount of the files confirmed; oracle **not re-run** (lock never freed): NOT CHECKED beyond the recount and three hand derivations |
| kpsolve cap 1 | not run | accepted |
