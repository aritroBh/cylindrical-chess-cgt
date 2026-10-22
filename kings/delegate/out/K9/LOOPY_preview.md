# A8 theory: when is "pawn components + a frozen king group" chess?

*Draft of 2026-10-16 by Claude (Opus 5.5) for plan item A8 ([RESEARCH_PLAN.md](../../RESEARCH_PLAN.md) §3,
Track A). The explicit solver that tests this note is `kings/kpsolve.c` (rules: [kings/SPEC.md](../SPEC.md)).
It builds on [notes/lemmas.md](../../notes/lemmas.md) (L2.1, L3.x) but re-proves everything it uses.*
*Revised on 2026-10-21 in answer to four adversarial reviews ([REVIEWS.md](REVIEWS.md), cited as R1–R4 with
their item numbers) and to the kpsolve results in [kings/results/PREDICTIONS.md](../results/PREDICTIONS.md).
The revision was delegated to three external models: kilo minimax-m3.1-flash for §1 and Theorem 2.4,
opencode nemotron-3-ultra for §2, and opencode best-free for §§3–6 (`kings/delegate/out/K1a..K1c/`). Their
64 edits were applied by script and integrated by Claude, which read the repaired proofs once.*

## Status after review (2026-10-21, amended 2026-10-22)

Every numbered result, its final label, and the review item behind any change. "PROVED after repair" means
the statement or its proof was changed and the complete repaired proof is now in the note. **Caveat:** every
repaired proof was written by a free external model and read once by the integrator. Each was then checked
independently by a fourth model (task K3, opencode beam-free, `kings/delegate/out/K3/REPORT.md`): 13 of the
17 are SOUND, and 4 are downgraded to GAP (the sharp form of 1.14, Theorem 2.7, P11, P12). No repaired proof
was found false. All checkers are AI models; no human has re-derived these proofs. The fixes marked "T30
proof audit" (2026-10-22) answer the main project's audit (`notes/proof_audit2/REPORT.md`). The kings/ side session
wrote them. Two AI reviewers (Sonnet) read the first draft, which led to the correction of the audit's
reading of P2.10(a). Two more read the revised text, and their remaining wording points were applied. K3 did
not see any of them, and K3's SOUND verdicts on T1.11(b) and P2.10(a) predate them. "FALSE as
originally stated → …" gives the corrected statement and its label. Each change in the text is marked
"(revised after review: Rk item n)".

| Result | Final label | Note |
|---|---|---|
| (A_Q), §1.2 | FALSE as a general statement → per-position hypothesis (A_Q)(X), checked by kpsolve; no longer a conjecture | R1 item 6, R2 item 8: `Ke2 Pb5 ka5 w` (cyl:7x6) and `Kd1 Pb3 ka3 w` (flat:4x4) are P-wins and chess draws |
| L1.6 | PROVED | R2: sound |
| L1.7 | PROVED | R2: sound |
| R1.8 | PROVED (by §5.4) | unchanged |
| T1.9 | PROVED; the remark after it is corrected | R2 item 2: the remark was false for cylcgt, which re-splits components |
| T1.11(a) | PROVED | R2: sound |
| T1.11(b) | FALSE as originally stated → τ counts moves into ⊕/⊖ by **either** player, M is summed over coordinates: PROVED after repair | R1 item 1, R2 items 1 and 9; T30 audit: a move count one short and the canonical form of 0 corrected in (b) and (c), conclusions unchanged |
| T1.11(c) | PROVED after repair (new in the revision): the hereditary version for cylcgt's re-splitting value | R2 item 2; T30 audit: a move count corrected |
| P1.12 | PROVED | R2: sound |
| P1.13 | FALSE as originally stated → A′ = { \| ⊖}, translation −B−1 (and a {∅ \| ⊖} variant): PROVED after repair | R1 item 2, R2 item 3 |
| T1.14(i) | PROVED | R2: sound |
| T1.14(ii) | GAP → PROVED after repair: (V4) is stated hereditarily on the re-split components of the context, Z deleted, with the corrected τ | R2 items 2 and 5 |
| T1.14(iii) | PROVED after repair, but a tautology: (A_Q) is now a per-position hypothesis | R2 item 8 |
| T1.14, sharp form | PROVED after repair (K9, 2026-10-22): along one D-winning strategy of the D-winner; (V2) at terminals reached, (V3) strong at loser's nodes, (V1a) split, (V1b) at loser's nodes; conclusion is a strategy win in P (revised after K9, 2026-10-22) | R2 item 6 |
| §1.5 "each hypothesis is needed" | (V1b), (V2), (V3), (V4): counterexamples given. (V1a): none given, so "needed" is a CONJECTURE | R1 item 4, R2 item 7 |
| L2.2 | PROVED | unchanged |
| T2.3 | PROVED (also KNOWN), for every integer B ≥ 1 | its direct proof, overwritten by a misanchored edit in the 2026-10-21 revision, was restored after the T30 audit |
| T2.4 | FALSE as originally stated (the "P-game of the context" option) → G under normal play (no draws), plus a strategy-transfer form (c) for games with draws: PROVED after repair | R2 item 4 |
| D2.6, (L3′) | withdrawn: it never applies to a 3-file group, and it does not give (L3) | R1 item 8, R3 item 2 |
| T2.7 | GAP → GAP (proof incomplete): (L1) is required only for k = ∞, (L3) covers stalemate, the local rules are stated, and μ counts context pawns only (revised after K3 check). K3's objection: a context passer within the window is not ruled out by (L2). Integrator's note: in the promotion model P only a promotion ends the game, which (L2) does exclude, so the objection may conflate P with the D-model. Unresolved until a further check. T30 recheck: Definition 2.6 (L2) counts s's king and pawns, Z-pawns included, while this row's "μ counts context pawns only" follows the proof, which leaves s's Z-pawns to (L1); the two are not yet reconciled | R1 item 3, R3 items 2 and 3; K3 |
| C2.8 | PROVED (wording corrected) | R3 item 7 |
| L2.9 | GAP → PROVED after repair (added hypothesis: s has no pawn on f ± 1). Without that hypothesis: CONJECTURE | R1 item 9, R3 item 4 |
| P2.10(a) | FALSE as originally stated (H = 4) → H ≥ 5: PROVED after repair, under both the textbook and the e.p.-aware passed test, for chess-legal contexts and s's context pawns; s's Z-pawns are a separate check. T30 audit: the proof lacked a step for en passant (now added). The stronger claim that no pawn of *either* colour stands one move from promotion needs H ≥ 6 under the e.p.-aware test | R1 item 7, R3 item 1; T30 audit and recheck |
| P2.10(b) | PROVED (the example; it needs width ≥ \|F_Z\| + 4). "The zero is context-dependent" is the CONJECTURE that follows it, now supported in C by P4 | R3 item 5 |
| R2.11 | GAP → heuristic only. No certificate for passers is claimed | R3 item 6 |
| P3.2 | PROVED; chess bridge PROVED after repair (adds (V1a)) | R4 item 7 |
| T3.3(a) | PROVED (also KNOWN) | R4: sound |
| T3.3(b) | FALSE as originally stated (with ∅ the dead position the pair is (W, L)) → { \| ⊖} ⊞ on_D is (L, L): PROVED after repair | R1 item 2 |
| T3.4 | PROVED | R4: sound |
| C3.5 | PROVED | R4: sound |
| §3, shuttles on both sides | CONJECTURE: needs a two-sided Proposition 3.2 | R4 item 6 |
| T4.2(a) | PROVED after repair (through the corrected T1.11(b)) | R4 item 3 |
| T4.2(b) | PROVED after repair (needs B > ℓ; the D-model equivalence is now proved) | R4 item 4 |
| T4.2(c) | PROVED after repair (negative integers; reachable cycle; "acyclic", not "non-reversible") | R4 item 5 |
| P4.3 | FALSE as originally stated (a king in check) → s not in check on u, reply not a promotion: PROVED after repair. The dichotomy "0 or ∞" is narrowed to steps inside F_Z with the opponent frozen at both ends | R4 items 1 and 2, R1 item 11 |
| D4.4 (over) | the numbering gap is filled | R1 item 11 |
| P4.5, P4.6 | PROVED | R4: sound |
| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched) | R1 item 10, R4 item 8 |
| §5.1, frozen | PROVED by enumeration, now written out | R1 item 11, R4 item 9 |
| §5.1, (L1) | CONJECTURE (scratch, k ≤ 4 and k = ∞ only; (L3) not checked) | R1 items 3 and 10, R4 item 9 |
| §5.2, White's sorties | the certificate fails: PROVED (L2.9). "Not punished": CONJECTURE (scratch); in C, kpsolve confirms the 6-rank analogue (P5) | R4 item 9 |
| §5.5 | CONJECTURE (scratch); Kd3 added | R1 items 10 and 11, R4 item 9 |
| §5.6 | μ_W = 5: PROVED by count. T = 5 and "(L2) fails by one tempo": CONJECTURE (scratch; R4 re-derived both) | R1 item 11 |
| P1a, P1b (§6) | PROVED; kpsolve (D, D) | PREDICTIONS.md, as for every P-row |
| P2, P3 | PROVED in P; kpsolve agrees in C on all 10 positions; literal cylcgt also gets them right | R1 item 5 |
| P4 | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\*, H\*2, H0) | PREDICTIONS.md, theory_P4_cap2_moves.txt |
| P5 | PROVED in P (b entries, + Hp1); bare w-entry CONJECTURE; kpsolve agrees on all four entries | — |
| P6, P7 | CONJECTURE, and partly PROVED in P. kpsolve (exact, 8×8): P6 = (L, W) on the cylinder, also confirmed by the main session's `atlas/cylinder/kpk`; P7 = (D, W) on the cylinder and the flat board, confirmed on the flat board by the Lichess tablebase | `kings/results/king_groups_8x8.txt`, `king_groups_lichess.txt` |
| P8 | PROVED in P. kpsolve (W, W) on the 6-rank analogue and on 8×8, cylinder and flat; the flat 8×8 result is confirmed by Lichess | `kings/results/king_groups_8x8.txt`, `king_groups_lichess.txt` |
| P9 | PROVED in P; kpsolve (W, L) | — |
| P10 | PROVED in P; kpsolve (W, W) for k = 0, 1, 2 on the 8×6 cylinder | PREDICTIONS.md |
| P11 | GAP (proof incomplete): W(X) and HSS defined; (V1b) checked from the layout (revised after K3 check) | R1 item 11 |
| P12 | GAP (proof incomplete): restricted to nodes where `--frozen` reports a win (revised after K3 check) | knock-on of R2 item 4 |

Not answered by a change in the mathematics: R1 item 12 (missing A8 content: CGSuite, opposition, Gafni),
which is recorded as open in §8.6.

---

**Labels.** Every claim has exactly one label.

- **PROVED**: the full proof is in this note. One model wrote it, and no second model or human has re-derived
  it yet (RESEARCH_PLAN §4, rule 3).
- **CONJECTURE**: not proved. The text names the evidence that would settle it. "Scratch evidence" means a
  throwaway script run once in the session scratchpad (geometry plus a small retrograde solver, Appendix A):
  not kpsolve, not saved in the project, not independently checked.
- **KNOWN**: from the literature, with a citation.

kpsolve results (§6) are data, not proofs: a claim that only a kpsolve run supports keeps the label
CONJECTURE, with "kpsolve agrees" (revised after review: R1 item 6).

Several results are PROVED *in the promotion model P* (Definition 1.5). They become statements about chess
only at positions where the hypothesis (A_Q) of §1.2 holds. (A_Q) is false in general, so it is checked
position by position by kpsolve (revised after review: R1 item 6, R2 item 8).

---

## 0. Summary

**The question.** The convention scores a passed pawn as ±BIG (BIG = 256), sums pawn components, and treats
the king group Z (the trébuchet) as the game 0. When does this give the chess result?

**The answer, in one paragraph.** The convention gives the chess result when four conditions hold, together
with the per-position hypothesis (A_Q)(X) that a won promotion race is a won game (Theorem 1.14; (A_Q) is
false as a general statement, so it is checked position by position by kpsolve; revised after review: R1 item
6, R2 item 8):
- (V1) the king group never interacts with the components, nobody is ever stalemated, and en passant obeys
  condition (E) of L1.6 in `notes/lemmas.md`;
- (V2) every "decisive event" really decides the game;
- (V3) every move inside Z is decisively punished;
- (V4) no two components carry threats of opposite sign, and BIG exceeds every tempo count. The check is
  hereditary, on the components of every reachable position, and a threat is a move into a terminal by either
  player (revised after review: R1 item 1, R2 items 1 and 2).

Only (V4) concerns BIG. Without it, +BIG and −BIG cancel and no value of BIG helps (Proposition 1.12).
The other three are chess facts.
- For a king move, (V2)+(V3) reduce to a local certificate: the punisher promotes within T moves against a
  defender who may pass, and the defender cannot promote within T moves elsewhere (Theorem 2.7, whose proof
  has a gap). The
  counter-promotion half of the certificate holds in every chess-legal non-terminal context when T = 1, on
  boards with at least 5 ranks, provided the defender has no Z-pawn one move from promotion (Proposition
  2.10(a)). For T ≥ 2 it fails in some context on boards at least |F_Z| + 4 files wide (Proposition 2.10(b)),
  so a slower punishment's zero is not certified in every context; that it is context-dependent is a
  CONJECTURE, supported by P4.
- When a king has a safe square to shuttle to, Z is not 0 but the loopy game `on`/`off` (or `dud`). On that
  side BIG is meaningless, because `on` exceeds every number. The correct rule replaces ±BIG by
  game-ending outcomes (Theorem 3.4):
  - **if only White can pass,** Black wins iff Black can force a decisive event against a White who may
    pass at any time; otherwise White wins;
  - **if both sides can pass,** a side wins iff it can force a decisive event against a passing opponent;
    otherwise the game is drawn.

**Results** (section number, label, one line each):

| # | Statement | Label |
|---|---|---|
| L1.6 | Adding options for a player never lowers that player's result | PROVED |
| L1.7 | Under normal play a move to the opponent's win can be deleted; under chess rules it cannot, because "no move" is stalemate | PROVED |
| T1.9 | One component: o(A^B) is the decisive-event outcome for every B ≥ 1 | PROVED |
| T1.11 | Sums: o(S) = decisive-event outcome under first-event dominance; sufficient: no opposite-sign threats in different components (a threat is a move into a terminal by either player), and B > every tempo count. (c) is the re-splitting version | PROVED (a); (b) and (c) PROVED after repair |
| P1.12 | {⊕ \| ∅} ⊞ {∅ \| ⊖} is 𝓝 in chess semantics, but its BIG translation is 0 (𝓟) for every B | PROVED |
| P1.13 | B must be at least the tempo count: with n tempi against the threat { \| ⊖}, the BIG outcome is right iff n ≤ B | PROVED after repair |
| T1.14 | Validity: (V1)–(V3) give P = D (no draws), (V4) gives o(S) = P, and (A_Q)(X) gives C = P | (i) PROVED; (ii), (iii) PROVED after repair; the sharp form is PROVED after repair (K9, 2026-10-22). The C part is the per-position hypothesis (A_Q)(X) |
| T2.3 | {−B \| B} = 0 for every integer B ≥ 1 | PROVED (and KNOWN: simplicity theorem) |
| T2.4 | Freeze theorem: if Z-moves are punished at every position where the mover is losing, then G + Z has the result of G, for a G scored under normal play (no draws) | PROVED after repair |
| T2.7 | Local certificate LC_T (local forced promotion against a passing defender, no faster counter-promotion, no stalemate) ⇒ decisive punishment | GAP (proof incomplete; see the status table) |
| C2.8 | Square-rule form: d(defender's king, promotion square) ≥ D + 2 suffices for the local part | PROVED |
| L2.9 | Blockade: a defender who may pass and whose king stands in front of the pawn is never beaten | PROVED after repair, with the added hypothesis that s has no pawn on f ± 1 (CONJECTURE without it) |
| P2.10 | For one-move punishments (T = 1) the counter-promotion condition holds in every chess-legal non-terminal context, on boards with at least 5 ranks, if the defender has no Z-pawn one move from promotion; for T ≥ 2 it fails in some (width ≥ \|F_Z\| + 4) | (a) PROVED after repair; (b) PROVED |
| T3.3 | G + `on` is 𝓛 for every short G, ±BIG included, so BIG plus a shuttle predicts "White always wins" | (a) PROVED (on > numbers: KNOWN); (b) PROVED after repair |
| T3.4 | Outcome rules for G ⊞ on, G ⊞ off, G ⊞ dud with game-ending decisive events | PROVED |
| C3.5 | Monotone chain: White wins with dud ⇒ with off ⇒ with nothing ⇒ with on | PROVED |
| T4.2 | n spare moves forming an acyclic graph = the integer n; a reachable cycle is `on`, never an integer | PROVED after repair |
| P4.3 | In an isolated K+P group, a king's spare tempo from safe steps inside F_Z (opponent frozen at both ends, mover not in check) is 0 or ∞, never a finite n ≥ 1 | PROVED after repair (hypotheses added) |
| P4.5–4.6 | 0 < over < x for every number x > 0; White wins G ⊞ over whenever White wins G moving second | PROVED (over: KNOWN) |
| §5 | 5.1 is a frozen trébuchet whose local certificate holds with T ≤ 7 (scratch); 7.2 is frozen for Black only (T = 1) and White escapes by blockade; 7.3 is not a zugzwang (f7–f8=Q at once). New groups realise `on`, `off` and a stalemate trap | per item, as in the status table: 5.1 frozen PROVED, its certificate (L1) a CONJECTURE (scratch); 7.2 and 7.3 PROVED in P where stated |

The testable predictions are in §6.

---

## 1. Chess semantics versus CGT semantics

### 1.1 Notation

- **Board.** W files × H ranks, flat or cylinder, with the rules of `kings/SPEC.md`. d(x, y) is the king
  distance: max(file distance, rank distance), with cyclic file distance on a cylinder.
- **Players.** White = Left, Black = Right.
- **Result pairs.** (r_w, r_b) lists the result with White to move, then with Black to move. Each entry is
  W, D or L **from White's point of view**, as kpsolve prints them.
- **Outcome classes** of a short CGT game (KNOWN; *Winning Ways* [WW] ch. 1, Siegel [S] ch. I–II):
  - 𝓛 = (W, W);
  - 𝓡 = (L, L);
  - 𝓝 = (W, L): the first player wins;
  - 𝓟 = (L, W): the second player wins.

  Short games have no draws.

### 1.2 Games with decisive terminals, and four models

**Definition 1.1 (D-game).** A *D-game* is a finite set X of positions with, for each x ∈ X, finite option
sets L(x) and R(x) contained in X ∪ {⊕, ⊖}.
- ⊕ is the terminal "White has won". ⊖ is the terminal "Black has won".
- The D-game is *short* if the directed graph of moves on X is acyclic, and *loopy* otherwise.
- ∅ denotes a position with no options.

**Definition 1.2 (play and results).**
- Play alternates from (x, s), where s is the player to move.
- A move to ⊕ or ⊖ ends the play with that result.
- A player with no option loses (*normal play*).
- Infinite play is a draw.
- r(x, s) = W if White can force a White win in finitely many moves, L if Black can, and D otherwise.

KNOWN: on a finite game graph these values are the least fixed point computed by retrograde analysis
([S] ch. VI; this is also what kpsolve computes). A short D-game has no draws (Zermelo).

**Definition 1.3 (sum with chess semantics).** For D-games A₁, …, A_k, the sum A₁ ⊞ … ⊞ A_k works as follows.
- Its positions are tuples.
- A move is a move in one coordinate.
- A move to ⊕ or ⊖ in *any* coordinate ends the *whole* play. This is "the first decisive event ends the
  game".
- A player with no option in any coordinate loses.

**Definition 1.4 (BIG translation).** For a short D-game A and an integer B ≥ 1, A^B is the short CGT game
obtained by replacing ⊕ with the integer B and ⊖ with −B. For a sum, (A₁ ⊞ … ⊞ A_k)^B := A₁^B + … + A_k^B
(the disjunctive CGT sum). In this sum a ±B summand does **not** end play: the other components continue.

**Definition 1.5 (four models of a king-and-pawn position X).**
- **C(X), chess.** The rules of `kings/SPEC.md`: checkmate wins, stalemate is a draw, infinite play is a draw.
- **P(X), the promotion model.** Chess, except that the first promotion ends the game as a win for the
  promoter. Stalemate and infinite play are still draws.
  - `kpsolve --frozen` computes P with frozen kings: a king move loses at once.
- **D(X), the decisive-event model.** A D-game. Its positions are the positions before the first decisive
  event. Its terminals are the decisive events:
  - a passer appears (as in `cylcgt`), with races scored by a race rule;
  - a punished move in the king group (§2). Under (V3) of Theorem 1.14 *every* move inside Z is a punished
    move, so the king group then contributes only suicides and is deleted by Lemma 1.7; the setup of
    Theorem 1.14 and this definition agree under (V3) (revised after review: R2 item 10).
- **S(X), the BIG convention.** The BIG value of X: at every node of the game tree the position is split
  into its components (files separated by an empty file, and an empty file stays empty), each component is
  translated separately, and the translations are summed; a component with a passer is worth ±BIG, races being
  scored by the race rule. This is the value `cylcgt.pawns.value` computes (COMPUTED-1, `cylcgt/pawns.py`).
  - *What S(X) is not* (revised after review: R2 item 2): it is not the BIG translation D(X)^B of the D-game of
    §1.2, in which the components are those of the root and the first decisive event ends the whole play.
    `cylcgt` re-splits at every node, and a passer freezes only its own component, so the two differ as soon
    as a component splits. Example: flat 7×6, e.p. on, count rule, `W: b2 d3 f2 / B: c4 c5 e5 g5` is one
    component at the root, yet o(S) = 𝓝 while the decisive-event result is 𝓡 (COMPUTED-1, `lemmas/common.py`:
    o(S) = N, o(W) = R).
  - The re-splitting is why (V4) of Theorem 1.14 has to be checked hereditarily; see Theorem 1.11(c).

The models are connected by bridges, each with its own hypotheses:

*Notation.* o(G) is the outcome class of a CGT game G (𝓛, 𝓡, 𝓝, 𝓟); W(X) is the whole-board convention game
of a pawn position X, in which the first passer ends the game (`notes/lemmas.md`); S(X) is the BIG value of
§1.5; and HSS, hereditary sum-safety, is the hypothesis (HSS) of Theorem 1.11(c). (Revised after review:
R1 item 11: §6 used o(W(X)) and "hereditarily sum-safe" without defining them.)

```
S  --Thm 1.11(c) (V4)-->  D  --Thm 1.14 (V1-V3)-->  P  --(A_Q)(X)-->  C
```

**Axiom (A_Q)(X) (per-position hypothesis, checked by kpsolve).** For a fixed position X: if X is a P-win
for σ, then X is a C-win for σ.
- **FALSE as a general statement (revised after review: R1 item 6, R2 item 8).** cyl:7×6 `Ke2 Pb5 ka5 w -` is
  a P-win (b6=Q at once; `kpsolve --frozen` gives W W) and a chess draw (exact D D: every White move draws);
  flat:4×4 `Kd1 Pb3 ka3 w -` is the same (b4=Q is met by Kxb4). So (A_Q) is not an axiom: it is a hypothesis
  to be checked at each position, and every "PROVED in P" claim below is a chess claim only where it holds.
- *Evidence for:* the cylinder KQK tables agree in two independent solvers ([RESULTS.md](../../RESULTS.md) §2:
  KQK is 100% won on the 8×8 cylinder).
- *Evidence against, in general:* L4.4 of `notes/lemmas.md` is a promotion race lost to a promotion with check.
- *Settled by:* kpsolve with `--cap 1` computes C exactly whenever its bounds agree (A = B), and `--frozen`
  computes P; the two runs decide (A_Q)(X) for that X.

### 1.3 Two lemmas about options

**Lemma 1.6 (option monotonicity). PROVED.** Let A′ be obtained from a D-game A by adding Left options or
deleting Right options at some positions. Then r_{A′}(x, s) ≥ r_A(x, s) for all x and s, in the order
L < D < W.

*Proof.*
- Every White strategy in A is a White strategy in A′, because White has at least the same options there.
- Every Black reply in A′ is also available in A, because Black's options there are a subset.
- So a strategy that forces a win in A forces it in A′, and a strategy that avoids losing in A avoids losing
  in A′. ∎

**Lemma 1.7 (suicide deletion, normal play only). PROVED.** Deleting a Left option equal to ⊖ (a "suicide")
does not change any result. The same holds for Right options equal to ⊕.

*Proof.* r(x, Left) is the best result over Left's options, and a move to ⊖ yields L, the worst.
- If Left has another option, the maximum is unchanged.
- If ⊖ was Left's only option, deleting it leaves Left with no option. Under normal play Left then loses:
  the result is L again. ∎

**Remark 1.8 (what the trébuchet is for).** In chess the second case of Lemma 1.7 fails: a side with no
legal move is **stalemated**, which is a draw.
- The convention's normal-play rule "a side with no pawn move loses" is therefore correct in chess only
  because the king group always offers that side a legal move, and that move is a suicide.
- The trébuchet's real job is to turn stalemate into a loss.
- §5.4 gives a position where a context pawn takes away the only suicide square. The convention says
  "White wins" and the truth is a draw.

### 1.4 What BIG can and cannot do

**Theorem 1.9 (one component). PROVED.** For a short D-game A and every B ≥ 1, the outcome class of A^B at
x equals the D-result pair of A at x.

*Proof.* Induction on the height of x.
- The integer B ≥ 1 is in 𝓛. Moving first, Left moves to B − 1 ≥ 0, where Right has no move. Moving second,
  Right has no move at all.
- Likewise −B is in 𝓡.
- So an option to ⊕ (resp. ⊖) in A corresponds to an option in 𝓛 (resp. 𝓡) in A^B. That is exactly
  "White wins (resp. loses) from it whoever moves next".
- An option to a non-terminal y has matching classes by induction.
- "Left wins moving first" holds iff some Left option is won by Left with Right to move, in both games.
  The same holds for Right.
- A player with no option loses in both games. ∎

In one component of the D-model the convention cannot go wrong: after the first ±B nothing else happens.
Trouble needs at least two components (compare L2.3 of `notes/lemmas.md`). That is *not* true of the
re-splitting model S of §1.5 (revised after review: R2 item 2): there a single component can still fail, because
a passer in one sub-part does not end its sibling, so trouble needs a later split, not two components. Example:
flat 7×6, e.p. on, count rule, `W: b2 d3 f2 / B: c4 c5 e5 g5` is one component at the root, yet o(S) = 𝓝 while
the decisive-event result is 𝓡 (COMPUTED-1, `lemmas/common.py`).

**Definition 1.10 (tempo counts, threats, dominance).** Let Y = (y₁, …, y_k) be a position of a sum of short
D-games.
- **Tempo counts.** M_L(y) is the largest number of Left moves in any sequence of moves from y (moves by
  both sides, in any order, not necessarily alternating), counting a final move into a terminal. M_R(y) is
  defined the same way for Right. Both are monotone: M(y′) ≤ M(y) whenever y′ is reachable from y.
  - For a sum, M_L(Y) is the sum of the M_L of the coordinates: the coordinates are played independently, so a
    longest sequence of Left moves in the sum is the concatenation of longest sequences in the coordinates.
    (The other reading — stop counting at the first terminal of the whole sum — gives a smaller number, so a
    hypothesis stated with it would be weaker; the proofs below use this component reading, and the count of
    the opponent's moves in the proof of Theorem 1.11(b) is exactly this one. Revised after review: R2 item 9.)
  - In the pawn game every White move advances a White pawn by at least one rank, so
    M_W ≤ Σ_white pawns (H − rank) ≤ (H − 2)p for p legal White pawns. That is ≤ 6p, so ≤ 48 on 8 ranks when
    p ≤ 8, and ≤ 6p in general; BIG = 256 exceeds 6p whenever p ≤ 42. The count ignores a final Z-move, so
    add 1 where a move inside the king group is possible (revised after review: R2 item 9).
- **Threats.** τ(y) ⊆ {+, −} contains + iff some position reachable from y without passing a terminal has an
  option ⊕ **by either player**; it contains − iff some such position has an option ⊖ by either player. So a
  move into the opponent's terminal is a threat for the opponent, and a suicide counts for the side that
  gains from it. Like M, τ is monotone: τ(y′) ⊆ τ(y) whenever y′ is reachable from y.
  - This is the τ of `notes/lemmas.md` (Definition 2.0) and of `lemmas/common.py: threats`, which count a
    passer created by either side's move. The earlier version of this note counted only Left options to ⊕ and
    Right options to ⊖, and was therefore blind to suicides (revised after review: R1 item 1, R2 item 1).
- **First-event dominance.** Y is *first-event dominant for B* if the following holds for every Y′ reachable
  from Y without passing a terminal, and every option y′_j → σ (σ ∈ {⊕, ⊖}, by either player):
  - the CGT position σB + Σ_{i≠j} (y′_i)^B is won by σ's player whoever moves first;
  - here σB means +B if σ = ⊕ and −B if σ = ⊖.

**Theorem 1.11 (sums). PROVED for (a); (b) PROVED after repair (revised after review: R1 item 1, R2 item
1); (c) PROVED after repair (R2 item 2).**
- **(a)** If Y is first-event dominant for B, then the outcome class of Σ y_i^B equals the D-result pair of
  ⊞ y_i.
- **(b)** Y is first-event dominant for B if both of the following hold:
  - *pairwise safety:* no reachable Y′ has two different coordinates with + ∈ τ(y′_i) and − ∈ τ(y′_j), with
    the τ of Definition 1.10 (an option to ⊕ or ⊖ counts whoever makes it);
  - *the bound:* B > max(M_L(Y), M_R(Y)).

*Proof.*
- **(a)** Induction on the total height.
  - At a reachable non-terminal Y′, each option of the CGT sum is one of two kinds.
    - A move in some y′_j to a non-terminal position. The induction hypothesis applies to it.
    - A move to the integer σB in coordinate j, giving σB + Σ_{i≠j} (y′_i)^B. By dominance this is in 𝓛 if
      σ = ⊕ and in 𝓡 if σ = ⊖. That is exactly the status of the D-option "σ wins now".
  - No other options exist, because no integer summand is present yet.
  - So the options correspond one to one with the D-options of Y′, with the same "won by Left with Right to
    move" status. The same holds on the Right side.
  - A player with no option loses in both.
- **(b)** Take σ = ⊕; the case σ = ⊖ is symmetric.
  - Let Y′ be reachable from Y without passing a terminal, and let y′_j → ⊕ be the option, made by either
    player. Since the option exists, + ∈ τ(y′_j) (Definition 1.10, corrected: an option counts whoever makes
    it). By pairwise safety no other coordinate has − ∈ τ(y′_i); by monotonicity of τ no other coordinate can
    ever reach ⊖, so no option of the sum Σ_{i≠j}(y′_i)^B is −B. This is the step that failed for the earlier
    τ, which was blind to a ⊕ entered by Right (revised after review: R1 item 1, R2 item 1).
  - The frontier position is B + Σ_{i≠j}(y′_i)^B, and the positive integer B has canonical form {B−1 | } (a
    Left-only stack of B moves, [WW] ch. 2), so Right has no move in it.
  - Left's strategy: on every turn, play in a positive integer summand (the B created by the event, or a +B
    created later), and never in a component.
  - Right's moves are all moves in the components, and there are at most M_R(Y) of them: the moves in one
    coordinate form a sequence of moves in that coordinate, so the total is at most Σ_{i≠j} M_R(y′_i) ≤ M_R(Y)
    (M is monotone, and for a sum M is the sum over the coordinates). A Right move into a terminal can only
    create another +B, because −B is unreachable.
  - Left needs at most M_R(Y) + 1 moves: one reply to each Right move, plus one more if Left moves first at
    the frontier. The first stack has B ≥ M_R(Y) + 1 moves, so Left has a move at every turn of its own.
    The stack can reach 0 = { | } only with Left's last move: reaching 0 takes B ≥ M_R(Y) + 1 Left turns, so
    by then Right has made M_R(Y) moves, the most it can make, and Right, to move, has no move. Right runs
    out of moves first and loses, whoever started. (Revised after the T30 proof audit,
    `notes/proof_audit2/REPORT.md`, 2026-10-22: the count was M_R(Y), one short when Left starts, and 0 was
    given the canonical form {−1 | 1}; neither changes the conclusion.) ∎

**(c) The re-splitting version. PROVED after repair (R2 item 2).** Let X be a pawn position, let S(X) be its
BIG value computed with re-splitting (§1.5), and let D(X) be the decisive-event game of X, in which the
position is split into its components at every node, a move is a move in one component, and the first decisive
event ends the play. Suppose:
- **(HSS)** at every position Y reachable from X before the first decisive event, the components of Y are
  pairwise safe (Definition 1.10, corrected τ: an option to ⊕ or ⊖ counts whoever makes it); and
- **(B)** BIG exceeds every tempo count of every such Y.

Then the outcome class of S(X) is the outcome class of the D-result pair of D(X).

*Proof.* Unfold S(X) as a game form F whose positions are pairs (Y, N), where Y is a pawn position (the live
components) and N is a finite multiset of frozen integers ±B. A move is either a move in an integer summand or
a pawn move in a live component Z; if that move creates a passer (or a race) in Z, then Z leaves Y and ±B joins
N; otherwise Z is replaced by its new components. This is `cylcgt.pawns.value` unfolded.
- **Frontier.** Let (Y, {σB}) be a position of F in which no live component has a (−σ)-threat and
  B > M_{−σ}(Y), where M_{−σ} is the tempo count of the opponent of σ (M_L for White, M_R for Black). Then σ
  wins F(Y, {σB}) whoever moves first. Take σ = +; the case σ = − is symmetric. σ's strategy is to move in the
  positive integer summand on every turn, which is possible while it has a move left; the opponent cannot move
  in a positive integer (its canonical form is {B−1 | }), and every integer frozen later is +B, because a −B
  would need a − threat and a race needs both threats. So every opponent move is a pawn move in a live
  component, and the opponent has at most M_{−σ}(Y) moves in all. σ needs at most M_{−σ}(Y) + 1 moves (one
  reply to each opponent move, plus one if σ moves first), and the first stack has B ≥ M_{−σ}(Y) + 1, so σ
  has a move at every turn of its own and the opponent runs out of moves first. The stack can reach
  0 = { | } only with σ's last move: that takes B ≥ M_{−σ}(Y) + 1 turns of σ, so by then the opponent has made
  all M_{−σ}(Y) of its moves. (Revised after the T30 proof audit, `notes/proof_audit2/REPORT.md`,
  2026-10-22.)
- **Induction.** o(F(Y, ∅)) = o(D(Y)) for every non-terminal Y reachable from X, by induction on the total
  number of pawn moves Φ(Y). Take a move of Y, made in component Z.
  - If the child is non-terminal, both models give the child and the induction hypothesis applies.
  - If the move creates a σ-passer, or a race scored σ, then D gives the terminal σ, which σ wins whoever
    starts. F gives (Y″, {σB}), where Y″ consists of the other components of Y. Here σ ∈ τ(Z): Z reaches the
    passer in one move, and for a race both signs are in τ(Z). Y is pairwise safe by (HSS), so no other live
    component has a (−σ)-threat, and the frontier step applies because M_{−σ}(Y″) ≤ M_{−σ}(Y) ≤ M_{−σ}(X) < B.
    So σ wins this option too.
  - Race scores agree: before the move Y had no passer, a move changes one component only, and passedness is
    local, so all passers of the child lie in Z and the promotion distances are the same in both models.
Outcomes are determined by the outcomes of the options, so o(F(Y, ∅)) = o(D(Y)). ∎

Re-splitting does not change the D-result: it only re-groups the same positions and options, and the D-result
of Definition 1.2 depends on the game graph and the terminals, not on the grouping. So the D-result pair of
the re-splitting D(X) is the one used in Theorem 1.14(i).

The remark that followed Theorem 1.11 is corrected here (revised after review: R1 item 1, R2 items 1 and 2).
Theorem 1.11(b) is the fixed-sum version of L2.1: its coordinates are the components of the root and never
split. The re-splitting version is (c) above, and the test "hereditarily sum-safe" of `notes/lemmas.md` is
(HSS), not pairwise safety at the root: it re-checks the re-split components at every reachable position, and it
uses the either-player τ.

**Proposition 1.12 (opposite threats cancel for every B). PROVED.** Let A = {⊕ | ∅} and A′ = {∅ | ⊖}.
- **In chess semantics,** A ⊞ A′ is 𝓝: whoever moves wins at once.
- **In the BIG translation,** A^B + A′^B = {B | 0} + {0 | −B} = 0, which is 𝓟, for every B ≥ 1.

*Proof of the BIG part.*
- Left moving first has two choices.
  - Left goes to B + {0 | −B}. Right answers −B, the total is B − B = 0, and Left is to move and loses.
  - Left goes to {B | 0} + 0. Right answers 0, and Left loses again.
- Right moving first loses by symmetry. So the sum is a 𝓟-position, and a 𝓟-position equals 0 (KNOWN:
  [WW] ch. 1, [S] ch. II). ∎

The 10 multi-component disagreements in `crosscheck/` and the counterexamples to `sum_safe` in L2.2 of
`notes/lemmas.md` are pawn-game instances of this mechanism.

**Proposition 1.13 (BIG must be at least the tempo count; sharp). PROVED after repair (R1 item 2, R2 item 3).**
Let A′ = { | ⊖} be a Black threat (no Left option at all) and R_n be n consecutive one-shot White moves with
no terminals (the integer n).
- **In chess semantics,** A′ ⊞ R_n is 𝓡 for every n ≥ 1: White can only spend tempi, and Black plays ⊖ when
  on move. (For n = 0 White has no move at all; the D-model scores that as a loss for White, while chess
  scores it as a stalemate, a draw.)
- **In the BIG translation,** A′^B = { | −B} = −B − 1 (KNOWN: {| x} = x − 1 for a number x, [WW] ch. 1), so
  { | −B} + n has three regimes:
  - 𝓡 if n ≤ B;
  - 𝓟 if n = B + 1;
  - 𝓛 if n ≥ B + 2.
- **The other reading of ∅.** With A′ = {∅ | ⊖}, where ∅ is the dead position of Definition 1.1, the
  translation is {0 | −B} and the regimes are different: {0 | −B} + n is 𝓝 for n ≤ B and 𝓛 for n ≥ B + 1
  (COMPUTED-1, `cylcgt.cgt`, B = 4: N, N, N, N, N, L, L, L for n = 0..7). The earlier version of this
  proposition mixed the two readings, and with them the claim was false as stated (revised after review: R1
  item 2, R2 item 3).

*Proof of the BIG part.* { | −B} + n is the integer n − B − 1, and the outcome class of an integer m is 𝓛 if
m ≥ 1, 𝓟 if m = 0 and 𝓡 if m ≤ −1.
- Right moving first goes to n − B. Left, to move, wins iff n − B ≥ 1.
- Left moving first goes to n − 1 + { | −B}. Right answers n − 1 − B. Left, to move, wins iff
  n − 1 − B ≥ 1. ∎

So BIG must be large compared with the tempo counts. In Proposition 1.13 the BIG outcome is right exactly when
n ≤ B, and Theorem 1.11(b) asks for B > M, so that the owner of the stack wins even when it must move first.
With BIG = 256 and pawns only, B > M holds as long as p ≤ 42, since M ≤ 6p (and M ≤ 48 on 8 ranks when
p ≤ 8). With a shuttling king the tempo count is infinite, and no BIG works (§3) (revised after review: R2
item 9; wording corrected after the T30 recheck, which found "exactly … exceeds" off by one).

### 1.5 The exact validity statement

Fix a K+P chess position X, cut into pawn components G₁, …, G_k and a king group Z with a buffer (Definition
2.1). Fix the D-model of §1.2: its decisive events are passers in the components (races by a race rule) and
the moves inside Z.

**Theorem 1.14 (validity of the convention). PROVED for (i); (ii) and (iii) PROVED after repair (revised
after review: R2 items 2, 5 and 8).** Assume:
- **(V1) non-interaction and no stalemate.** At every chess position Y reachable from X before the first
  decisive event:
  - (a) the legal chess moves of the side to move are exactly its D-options, with the same resulting
    positions. This includes en passant obeying condition (E) of L1.6 in `notes/lemmas.md`, and no checks;
  - (b) the side to move has at least one legal move.
- **(V2) decisiveness.** Every decisive event reached by a move from such a Y leads to a position that is a
  P-win for the event's beneficiary.
- **(V3) frozen Z.** Every legal move inside Z, by either side, is a decisive event for the opponent: a
  suicide.
- **(V4) hereditary sum-safety.** At every position Y reachable from X before the first decisive event:
  - the pawn components of Y, re-split as the files split (an empty file stays empty, so a component may split
    into two), with the king group Z deleted, are pairwise safe: no two different components carry + ∈ τ and
    − ∈ τ, where τ counts options to ⊕ or ⊖ by **either** player (Definition 1.10);
  - BIG exceeds every tempo count of Y.

Then, with either side to move:
- **(i)** P(X) = D(X). There are no draws, and the result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z
  deleted).
- **(ii)** If (V4) holds, the outcome class of S(X) — the BIG value of the pawn components, with the king
  group Z deleted — equals the outcome class of the D-result pair of P(X).
- **(iii)** Under (A_Q)(X) (the per-position hypothesis of §1.2, checked by kpsolve), C(X) = P(X). This is now
  a tautology: (A_Q)(X) says exactly this (revised after review: R2 item 8).

*Proof.*
- **(i)** By (V3), Z contributes only suicides to D, so by Lemma 1.7 D(X) is the D-result of ⊞ G_i. D is
  short, so it has no draws.
  - Let σ be the D-winner (for the given side to move). σ plays a D-winning strategy. That strategy never
    plays a Z-move, because Z-moves are σ's suicides.
  - By (V1a), every chess move of the loser σ̄ is a D-option.
  - Under a winning strategy, the loser never has an option to its own terminal: at a loser-to-move position
    every option leads to a σ-win. So the play can end only in a σ-terminal, made by σ, or by σ̄ as a
    suicide (a Z-move, or a pawn move that gives σ a passer).
  - The play does end. The components are short, and (V1b) excludes "no move".
  - By (V2) the terminal position is a P-win for σ, so σ wins P.
- **(ii)** By (i), the D-result pair of X is the D-result pair of D(X), and re-splitting does not change
  that pair (it re-groups the same positions and options). By Theorem 1.11(c), with (V4) supplying (HSS) and
  the bound, the outcome class of S(X) is the outcome class of that D-result pair.
- **(iii)** Definition of (A_Q)(X). ∎

**Sharp form (PROVED after repair (K9, 2026-10-22)).** (revised after K3 check; (revised after K9, 2026-10-22))
- Let σ be the D-winner of D(X) with a D-winning strategy Σ. Assume that along every play consistent with Σ:
  - (V2') every terminal reached is a P-win for σ;
  - (V3') at every loser-to-move node of Σ, every legal Z-move of σ̄ is a P-loss for σ̄;
  - (V1a'-i) every move prescribed by Σ is a legal chess move;
  - (V1a'-ii) at every loser-to-move node of Σ, every legal chess move of σ̄ is a D-option of D(X);
  - (V1b') at every loser-to-move node of Σ that is not a terminal, σ̄ has a legal chess move.
- Then σ wins P(X) by following Σ. The conclusion is a strategy win, not a normal-play result: the claim "the
  result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z deleted)" belongs to (i), not to the sharp form.
- (V3') must hold for *all* legal Z-moves at the node, not just those played: an unpunished loser Z-move is
  not a terminal in the P-relevant sense, the D-to-P mapping collapses, and σ̄ could loop in Z, defeating the
  finite-time win. Lemma 1.7 (suicide deletion) is therefore not used; Z is not deleted and the conclusion is
  not the normal-play result. Lemma 1.6 is used to ignore σ's extra legal chess moves. (revised after K9,
  2026-10-22)

Theorem 2.4 is the version of this statement for Z.

**Why "exact" does not mean "iff".** (V1)–(V4) are sufficient, and none can be dropped, except that for
(V1a) this is a CONJECTURE (table below). But no condition on local data can be *necessary*: the convention is
sometimes right by accident.
- In §5.4, literal pawn-only scoring gets Z_onT1 + context right because it calls c5 passed. It gets the
  stalemate trap wrong for the same reason.
- So the exact answer to "when does the convention hold?" is: whenever (V1)–(V4) hold, plus accidents. The
  accidents are not detectable without solving the position.

**Each hypothesis is needed — except that for (V1a) this is a CONJECTURE (revised after review: R1 item 4,
R2 item 7).** Each can fail and change the result.

| Hypothesis | Counterexample (where in this note or the project) |
|---|---|
| (V1b) no stalemate | §5.4: the only suicide square is covered, and the position is a draw instead of a win (PROVED). The isolated failure needs (V3) to hold, so use the frozen model, where (V3) holds by fiat: `--frozen` gives `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` as (D, D), with every king move L, while the convention reads Z as 0 and the context as +1, i.e. (W, W) (COMPUTED-1, `kings/kpsolve --frozen`). With real kings the same position also violates (V3): Ka6 and Kg4–g6 are legal Z-moves that are not suicides |
| (V1a) non-interaction | No isolated counterexample is known: the king sorties that reach the component (41 of 449 tablebase king moves draw and 7 win, `engine/suite/`, RESULTS §1) are *unpunished Z-moves*, i.e. (V2)/(V3) failures, not (V1a) failures. That (V1a) is needed at all is therefore a **CONJECTURE** (revised after review: R1 item 4, R2 item 7) |
| (V2) decisiveness | Races: L4.1 of `notes/lemmas.md` (forced wins, modulo KQK). A dropped pawn that does not lose: §5.5 |
| (V3) frozen Z | 7.3: f7–f8=Q is available at once (§5.3) |
| (V4) dominance | Proposition 1.12 (cancellation, for every B) and Proposition 1.13 (tempo above B) |

---

## 2. Frozen king groups

**Definition 2.1 (king group, buffer).** A *king group* Z consists of:
- a set F_Z of files (an arc on a cylinder);
- both kings and some pawns, the Z-pawns, all on F_Z.

All other pawns, the *context*, stand on files at distance ≥ 2 from F_Z. The files at distance exactly 1
are pawn-free; they are the *buffer*. A *Z-move* is a move of a king or of a Z-pawn.
- On the 7×6 cylinder with F_Z = {a, b, c}, the buffer is {d, g} and the context lies on {e, f}.

**Lemma 2.2 (buffer invariance). PROVED.** Before the first promotion:
- no pawn ever stands on a buffer file;
- context pawns stay on context files, and Z-pawns stay on F_Z;
- hence a king standing on F_Z is never attacked by a context pawn, and a context pawn never attacks a
  square of F_Z.

*Proof.*
- A pawn changes file only by capturing on an adjacent file, landing on the square of an enemy pawn or
  officer. A king cannot be captured.
- For en passant, the capturer lands on the file of the captured pawn.
- There are no officers before the first promotion.
- So a pawn can enter a buffer file only by capturing an enemy pawn already on it. Buffer files start
  pawn-free, so by induction on the number of moves none ever holds a pawn.
- Pawns attack only the two adjacent files. ∎

**Theorem 2.3 ({−B | B} = 0 for every integer B ≥ 1). PROVED**
(also KNOWN: the simplicity theorem, [WW] ch. 2, [S] ch. II, since 0
is the simplest number strictly between −B and B).

*Direct proof.* (Restored after the T30 proof audit, `notes/proof_audit2/REPORT.md`, 2026-10-22. In the 2026-10-21
revision, edit 24 of `kings/delegate/out/K1a/EDITS.md`, meant for the tempo-bound paragraph after Proposition
1.13, was anchored here by mistake and replaced this proof; it now stands in §1.4.) The proof uses B ≥ 1: for
B = 0 the game is {0 | 0} = \*.
- Left moving first goes to −B. Right, to move, moves to −(B − 1), and Left then has no move in a
  non-positive integer and loses.
- Right moving first loses by symmetry.
- A 𝓟-position equals 0 (KNOWN, [WW] ch. 1). ∎

So "every White Z-move gives Black a passer and vice versa" makes Z = {−BIG | +BIG} = 0 in the convention.
The real content is in what "gives a passer" must mean in chess.

**Theorem 2.4 (freeze theorem). PROVED after repair (R2 item 4).** Let G be a short game scored under normal
play, so that G has no draws, and let Z be a king group, possibly loopy. The sum G ⊞ Z is the game on positions
(Y, z): a move is a G-move in the context or a Z-move (a move of a king or of a Z-pawn inside the group); a
G-position with no G-move left is a loss for the side to move, while in the sum the side to move may still have
Z-moves. Assume Z's state changes only through Z-moves.
- **(a)** Suppose every Z-move, in every state of Z and in every context reachable from the root, leads to a
  position won by the opponent of the mover. Then r(G ⊞ Z) = r(G) at every reachable (Y, s).
- **(b)** It is enough that this holds at the positions (Y, s) reached under some winning strategy of the
  G-winner σ at which the loser σ̄ is to move.
- **(c) (strategy transfer, for a G that may draw.)** Let G be a game that may draw, and let σ be a side with a
  strategy in G that never loses (it wins every line except those that draw). Suppose that, at every position
  reached under that strategy, every Z-move of the opponent σ̄ is decisively punished (Definition 2.5) and that
  σ never needs to move in Z. Then σ does not lose G ⊞ Z; and if σ's strategy in G wins every line, then σ wins
  G ⊞ Z.

In chess, assume also (V1b): the side to move always has a legal move.

*The P-game of the context is **not** covered, and the earlier version of this theorem was false for it
(revised after review: R2 item 4).* The P-model keeps stalemate as a draw, so "G has no draws" fails there and
the step "since G has no draws the results agree" was unjustified. Counterexample: cyl:7×6,
`Ka4 Pb3 Pe3 kc3 pb4 pe4` (Z_T + H0). The context G = {Pe3, pe4} has no move for either side, so it is (D, D)
under P; `kpsolve --frozen` gives (L, W), and there the hypothesis of (a) holds by fiat (king moves lose and
the Z-pawns have no moves); with real kings, White to move is L (exact) (COMPUTED-1, `kings/kpsolve`).

*Proof of (b).*
- σ plays its winning strategy in G and never moves in Z, so Z stays in its initial state.
- Whenever σ̄ is to move, the G-position is lost for σ̄. If σ̄ moves in Z, σ wins by hypothesis.
- G-play is finite, so one of three things happens:
  - a σ-terminal is reached, and σ wins;
  - σ̄ has no G-move and must move in Z, and σ wins;
  - σ̄ has no move at all, and σ̄ loses by normal play.
- In chess the last case is stalemate, which (V1b) excludes.
- So the G-winner wins G ⊞ Z, and since G has no draws the results agree. (a) is a special case. ∎

*Proof of (c).* σ plays its strategy of G, read in the sum, and never moves in Z, so Z stays in its initial
state. Whenever σ̄ moves in G, σ answers as in G. Whenever σ̄ moves in Z, σ wins by the hypothesis, since that
Z-move is decisively punished. The G-play is finite, since G is short. If σ̄ never moves in Z, the play is a
line of G under σ's strategy: it ends in a σ-win, or in a draw of G, so σ does not lose. If σ̄ does move in Z, σ
wins. ∎

**Definition 2.5 (decisive punishment, in chess terms).** A Z-move m of side s, made at a chess position Y
(context plus Z), is *decisively punished* if the opponent s̄ has a forced win in P (or in C) from the
position after m. The win must hold against every defence of s:
- s's moves in the context, including creating passers, starting races and capturing en passant;
- s's king going anywhere, back into Z or into the context;
- s promoting;
- s steering for stalemate.

"Whatever the other components contain" means: for every context in the class one claims the zero for.
Theorem 2.4(b) needs this only at positions where s is losing the context.

**Definition 2.6 (local certificate LC_T).** Let m be a Z-move of s, and r the punishing reply of s̄ (a
king capture of a Z-pawn). Let Q be the position after m and r, with s to move. Let Q_Z be Q with every
context pawn deleted: only the kings and the remaining Z-pawns are left, on the whole board. LC_T(m) holds
at Y if:

- **(L1) local forced promotion against a passing defender.** s̄ wins the following game in Q_Z within T of its
  own moves against a defender s who may pass **arbitrarily many times** (k = ∞):
  - s may pass at any turn, but not while in check;
  - s with no legal move and no pass left is stalemated, which counts as a failure for s̄;
  - s̄ wins by promoting to a queen that s cannot capture at once;
  - s̄'s king never leaves F_Z.

  The unlimited budget models the fact that s's spare moves in the context are not known in advance; the real
  defender's options are a subset of the k = ∞ game's, and its only gain from having fewer options is
  stalemate, which (L3) excludes. The earlier phrasing "for every k" and the remark that "every k is needed"
  are withdrawn (revised after review: R1 item 3, R3 items 2 and 3).
- **(L2) no faster counter-promotion.** Let μ_s be the least number of s-moves (king and pawns) in which s
  could promote in Q if s̄ never moved, s̄'s Z-pieces were removed and s̄'s context pawns stood fixed.
  Then μ_s ≥ T + 1.
  - **(L2⁺)**, the recommended margin before invoking (A_Q), is μ_s ≥ T + 2. With μ_s = T + 1, s's pawn
    reaches its seventh rank just as s̄ queens, and queen-against-seventh-rank-pawn endings can be drawn.
- **(L3) no stalemate in the window.** At every s-turn during the window, s has a legal move in the real
  position.
  - (L1) already excludes stalemate in Q_Z. The extra danger is context pieces taking away king squares that
    are free in Q_Z.
  - Sufficient (L3′): every square within distance T + 1 of s's king (after m) lies on F_Z. Then s's king has
    the same legal moves as in Q_Z. **This condition can never apply for T ≥ 2 on a 3-file group, because the
    ball of radius T+1 spans at least 5 files while |F_Z| = 3.** (revised after review: R1 item 8)
  - For T = 1, (L3) is a single check: after r, s has a legal move.

**Theorem 2.7 (sufficiency of the certificate). GAP (proof incomplete) (in P).** If LC_T(m) holds at Y, then the (revised after K3 check)
Z-move m is decisively punished in P.

*Proof.* s̄ plays r and then follows its local winning strategy σ_Z (which exists by (L1) with k = ∞), using
only Z-moves. It ignores the context. Check that the strategy survives in the full position, for t ≤ T.

- **s's moves map onto the k = ∞ local game.** A king move of s is the same king move in Q_Z. In Q_Z there
  are fewer pieces, so it is still legal there, and a capture of a context pawn becomes a plain move to the
  same square. A context move of s is a pass in Q_Z. It is never made while s is in check (the only checks
  during the window come from s̄'s Z-pieces, which are present in Q_Z), so the pass is allowed in the k = ∞
  game. The real defender's options are a subset of the k = ∞ game's options; its only possible gain from
  having fewer options is stalemate, which (L3) excludes (revised after review: R1 item 3, R3 items 2 and 3).
- **s̄'s prescribed moves are legal.** s̄'s king stays on F_Z, so by Lemma 2.2 no context pawn attacks it,
  occupies its squares or gives it check. s̄'s pawn moves stay on F_Z. Without sliders there are no pins.
- **s does not promote first.** After r, s moves first. Before s̄'s T-th move, s has made T moves, and by
  (L2) it needs at least T + 1. The removed Z-pieces of s̄ could only slow s down **except that s̄'s
  Z-pawns are capture targets for s; the theorem survives only if (L1)'s local game counts an s-promotion as
  a failure for s̄, which it does by "s̄ wins by promoting… s cannot capture at once"**. s's own Z-pawns are
  part of Q_Z, and σ_Z wins against them. (revised after review: R3 item 3b)
- **No other way out.**
  - (L3) excludes stalemate of s in the real position. (L1) at k = ∞ excludes it in Q_Z.
  - s cannot checkmate s̄. s has no officers; s's Z-pawns do attack F_Z, but σ_Z has a legal move on F_Z at
    every turn, and s̄'s real moves include its local ones, so s̄ is never forced to skip a move (revised
    after review: R3 item 3c).
  - The new queen stands on F_Z, out of reach of context pawns (Lemma 2.2).

So s̄ promotes within T moves, which is a P-win. ∎

**Corollary 2.8 (square-rule form of (L1)). PROVED.** Suppose:
- Q_Z consists of the two kings and one s̄-pawn p, and s̄'s king is not on p's path;
- the plan is "push p every move", with D = number of ranks to the promotion square q_D;
- d(k_s, q_D) ≥ D + 2, where k_s is s's king square after m.

Then s̄ wins the local game of (L1) within T ≤ D moves:
- for k = ∞;
- for every finite k, provided s's king always has a legal move in Q_Z. This is the stalemate proviso: a
  king boxed in at a rank edge, with no pass left, would be stalemated.

*Proof.*
- **Distances to every path square.** Let q_j be the path square j ranks ahead, with q₀ = p's square. The
  triangle inequality gives d(k_s, q_j) ≥ d(k_s, q_D) − (D − j) ≥ j + 2.
- **Timing.** p reaches q_j at s̄'s move number t_j ≤ j; a double step only makes it earlier. Up to that
  moment s has made t_j moves.
- **The king can neither block nor capture.** To block q_j, s's king must be there within t_j ≤ j moves.
  To capture p on q_j, it must arrive by move t_j + 1 ≤ j + 1. Both are impossible.
- **The pawn cannot be stopped otherwise.** Q_Z holds no s-pawn, and the buffer keeps context pawns away.
- **The queen is safe.** For j = D the same bound keeps the new queen out of reach.
- **Budgets.** A pass changes nothing on the board, so the timing argument covers every pattern of passes.
  The only remaining defence is a stalemate, which the proviso excludes. ∎

The bound is the classical "rule of the square" with a two-square margin: with the defender to move,
d(k_s, q_D) ≥ D + 2 is exactly the classical rule of the square, not a margin on top of it (revised after
review: R3 item 7). Corollary 2.8 is rarely enough for trébuchets, because the defending king starts next to
the action. (L1) must then be checked by a small search (Appendix A).

**Lemma 2.9 (blockade). PROVED after repair (added hypothesis).** In Q_Z, suppose s̄'s only Z-pawns are on
one file f, and s's king stands on a square of f in front of s̄'s front pawn there. **Assume further that s
has no pawn on f ± 1 that an s̄ pawn could capture.** If s may pass (k = ∞), s̄ never promotes.

*Proof.*
- s passes forever. That is legal: s is never in check, because s̄'s pawns on f attack only files f ± 1, and
  a king never gives check.
- No s̄ pawn leaves file f: a capture needs an s-piece on f ± 1. By hypothesis s has no such pawn, and its
  king cannot be captured.
- So every s̄ pawn on f must pass the king's square, which never empties. ∎

**Without the added hypothesis the statement is a CONJECTURE** (an s-pawn on f ± 1 could be captured,
letting an s̄ pawn leave f). The uses in §5.2 and P5 are unaffected because s has no pawns there (revised
after review: R1 item 9, R3 item 4).

**Proposition 2.10 (which punishments are universal). (a) PROVED after repair; (b) PROVED.**
- **(a)** If T = 1 and **H ≥ 5**, then in every chess-legal non-terminal context (every context without a
  passer) no s context pawn can promote in one move, under both the textbook and the e.p.-aware passed test.
  Hence (L2) holds whenever, in addition, no s Z-pawn is one move from promotion in Q. *Proof:* an s-pawn that
  can promote in one move stands on its penultimate rank (the seventh on 8 ranks).
  - No enemy pawn can stand ahead of it, since no pawn stands on the last rank.
  - It cannot be taken en passant. Only a pawn that has just made a double step can be. In a chess position
    the last move before Y was s̄'s, and r, the last move before Q, is not a double step: it is a king capture,
    or the promotion in §5.3.
  - So it is passed under either test, and the context would be terminal. (This step was missing; added after
    the T30 proof audit, `notes/proof_audit2/REPORT.md`, 2026-10-22.) The argument needs chess-legal
    contexts: cylcgt's component model can keep a stale right in a component after its owner has moved
    elsewhere.
  - The king's help does not change this: removing a blocker takes a move of its own.
  - *Z-pawns.* In the uses in §5.2–5.4, P3, P5 and P7, the s Z-pawn is captured by r. In §5.3 and P8 it
    survives; it is Black's and at least 2 moves from promotion in Q. So μ_s ≥ 2 = T + 1, which is enough for
    (L2), though not always for the margin (L2⁺).

  *A stronger statement needs six ranks.* "In a non-terminal context no pawn of *either* colour is one move
  from promotion" is false on 5 ranks under the e.p.-aware test. In `W a2 / B a3 b2` with White to move just
  after ...b4–b2, White may capture en passant on b3, so nothing is passed; yet b2 is one move from promotion.
  - The pawn belongs to the side *not* to move, so (L2) is unaffected.
  - A search of flat 4-file boards with at most 2 pawns a side finds 156 such (position, e.p. right) pairs on 5
    ranks and none on 6 or 7 ranks (`notes/proof_audit2/checks/prop6_check.out`). The audit's verifier
    reports 120 when the double-step origin must be empty, and none on 8 ranks. Those two results are recorded
    only in the verifier section of `notes/proof_audit2/REPORT.md`, without a saved script.
  - On H ≥ 6 a double step lands H − 4 ≥ 2 moves from promotion, so the stronger statement holds. The paper's
    proof argues this stronger form, hence its six ranks; its statement concerns the defender only.

  *Four ranks.* For H = 4, a pawn on its second rank promotes by a double step onto the last rank in one move
  and need not be passed, so (L2) can fail with μ_s = 1 (revised after review: R1 item 7, R3 item 1).

  So, by Theorem 2.7, whose proof has a gap, a group whose punishments satisfy (L1) with T = 1 is decisively
  punished in every chess-legal non-terminal context on boards with H ≥ 5, provided (L3) holds and no s
  Z-pawn is one move from promotion in Q. For T = 1, (L3) asks only that s has a legal move at its single turn.
- **(b)** For every T ≥ 2 there is a non-terminal context with μ_s = 2 (this requires board width ≥ |F_Z| + 4).
  - *Example (White):* W (f, H−2); B (f, H−1) and (f+1, H−1). No pawn is passed. White captures to
    (f+1, H−1) and promotes next move.
  - So (L2) fails there, and a punishment with T ≥ 2 is never certified for all contexts. **The statement
    "The zero of such a group is context-dependent" is a CONJECTURE** (it is exactly the conjecture stated in
    the next bullet; §0 repeated it as fact). CONJECTURE: for each frozen group with T ≥ 2 there is a
    context, with the defender in zugzwang there, where the freeze actually fails in P. *To settle:* kpsolve
    on Z_T (§5.1) plus 2-file contexts with fast White pawns.

**Remark 2.11 (the certificate is not special to kings). GAP.** A passer created in a component is a decisive
event too, and (V2) asks the same question about it. The certificate of Definition 2.6 **cannot apply as
written** to a passer (revised after review: R3 item 6):
- Q_Z deletes "every context pawn", which deletes the passer itself.
- The punishing reply r is not a king capture of a Z-pawn.
- The passer's owner may need its king off F_Z, where the legality step via Lemma 2.2 no longer covers it.
- The pawns of the passer's own component are not addressed.
The claim "which this certificate rules out" is therefore unproved. P11 in §6 relies on this remark under a
PROVED label; that label must be revised when the certificate is extended.

---

## 3. Spare tempo moves as loopy games

**Definition 3.1 (pass reservoirs).** Each reservoir is a D-game with a single position ω.
- **on_D:** L(ω) = {ω}, R(ω) = ∅. White can pass forever; Black has no move.
- **off_D:** the mirror image.
- **dud_D:** L(ω) = R(ω) = {ω}.

Their CGT analogues are on = {on | }, off = { | off} and dud = {dud | dud} (KNOWN: [WW] ch. 11 "Games
Infinite and Indefinite"; [S] ch. VI). Also KNOWN [S, ch. VI]:
- on exceeds every number;
- on, off and over are stoppers, while dud is not;
- G + dud is a draw for every G in which only running out of moves decides the game.

**Proposition 3.2 (a shuttling king is a pass). PROVED.** Let Z be a king group and z ↔ z′ two non-capturing
White king moves inside F_Z, with:
- in both z and z′, every Black Z-move a suicide in the D-model;
- the two shuttle moves legal in every context, which Lemma 2.2 guarantees, since they stay on F_Z.

Then, in the D-model and for a short context G, r(G ⊞ Z) ≥ r(G ⊞ on_D), with equality if White has no other
Z-moves.

*Proof.*
- The relation {(z, ω), (z′, ω)} is a bisimulation. In each of z and z′, White can move to the other, and
  Black's Z-options are all suicides. So the 2-cycle has the same results as the 1-cycle ω.
- Black's suicides can be deleted (Lemma 1.7). This is valid in chess only under (V1b): Black must always
  have the legal suicide.
- Any further White Z-moves only help White (Lemma 1.6). ∎

**Chess bridge** (PROVED after repair, by the proof of Theorem 1.14 with (V1a) added).
Suppose r(G ⊞ on_D) = W, White plays that strategy (shuttling for its passes), and along it:
- (V1a) every legal chess move of the side to move is one of the D-options of the D-model, and leads to the
  matching position;
- every Black Z-move is decisively punished in P;
- every decisive event of G that is reached is a P-win for its beneficiary;
- Black always has a legal move.

Then White wins in P. *Proof:* the proof of Theorem 1.14(i), with (V1a) among the hypotheses — (V1a) makes
the D-play a chess play, the shuttling strategy supplies White's passes, and the last two bullets make every
deviation decisive for Black. The mirror statement holds for Black wins.
(Revised after review: R4 item 7: the bridge needs (V1a). It fails in P2 + H\* if White plays e3–e4, which
stalemates Black, so the bridge may only be used along a strategy that avoids that move; kpsolve gives (W, W)
for P2 + H\*.)

**Theorem 3.3 (BIG fails with a shuttle). (a) PROVED; (b) PROVED after repair.**
- **(a)** For every short CGT game G, including games with ±B terminals, G + on is in 𝓛.
  *Proof:* Left always has the move on → on, and Right never has a move in on. Right's moves in G are
  finitely many in any play, so Right runs out and loses, whoever starts.
  - In particular on + (−B) is in 𝓛 for every B. (KNOWN as "on exceeds every number", [S] ch. VI.)
- **(b)** In chess semantics, { | ⊖} ⊞ on_D is (L, L): Black plays ⊖ when on move, and White can only pass.
  (With the other reading of ∅, A′ = {∅ | ⊖}, the pair is (W, L) in the D-model: White plays A′ → ∅ and
  leaves Black with no move at all, which the D-model scores as a loss for Black and chess as a stalemate. The
  statement above uses the same A′ = { | ⊖} as Proposition 1.13; revised after review: R1 item 2.)

So once a White shuttle is modelled as on, the BIG convention predicts "White wins" for every position. That
is false whenever Black has a forced decisive event.
- The reason is that BIG encodes "decisive" as "many spare moves". An infinite tempo supply outlasts any
  finite BIG; the tempo-count condition of Proposition 1.13 fails for every B.
- The fix is to make decisive events terminal (game-ending), which the D-model does. This is the setting
  that *affine normal play* formalises (Larsson–Nowakowski–Santos, GONC 6, 2025, per
  [notes/lit_cgt_chess.md](../../notes/lit_cgt_chess.md)). Nothing below depends on that paper.

**Theorem 3.4 (outcome rules with passes). PROVED.** Let G be a short D-game under normal play, and write x
for its positions.

- **(a) Both sides may pass (G ⊞ dud_D).** Define predicates by induction over G's acyclic order:
  - Λ_L(x) ⟺ some Left option of x is ⊕, or is a position x^L with Λ_R(x^L);
  - Λ_R(x) ⟺ Λ_L(x), and every Right option x^R of x is ⊕ or satisfies Λ_L(x^R).

  Then r(x, s) = W iff Λ_s(x). Define Ρ_R and Ρ_L symmetrically for Black; r(x, s) = L iff Ρ_s(x).
  Otherwise r(x, s) = D. Consequences:
  - having the move never hurts: Λ_R ⇒ Λ_L, so there is no zugzwang;
  - if G has no terminals, every position is drawn;
  - in words, **a side wins iff it can force a decisive event against an opponent who may pass at any time;
    otherwise the game is drawn.**
- **(b) Only White may pass (G ⊞ on_D).** There are no draws. Define:
  - Ρ′_R(x) ⟺ some Right option of x is ⊖, or is a position x^R with Ρ′_L(x^R);
  - Ρ′_L(x) ⟺ Ρ′_R(x), and every Left option x^L of x is ⊖ or satisfies Ρ′_R(x^L).

  Then r(x, s) = L iff Ρ′_s(x), and r(x, s) = W otherwise. In words, **Black wins iff Black can force a
  decisive event against a White who may pass at any time.** Black cannot pass, so it loses whenever it runs
  out of moves. White can never be in zugzwang.
- **(c) Only Black may pass (G ⊞ off_D).** The mirror image of (b).

*Proof.*
- **(a)** States are pairs (x, s); a pass moves (x, s) to (x, s̄). Use the least fixed point of
  Definition 1.2.
  - Suppose Left first wins (x, L) at stage n by passing. Then Left won (x, R) at an earlier stage. But
    Right's pass from (x, R) leads back to (x, L), so (x, L) was won at a stage earlier still, a
    contradiction.
  - So Left's winning moves are always G-moves. Left wins (x, R) iff every Right option, Right's pass
    included, leads to a Left win.
  - That is the recursion above. It is well-founded: Λ_L(x) uses Λ_R only at G-successors of x, and Λ_R(x)
    uses Λ_L at x and at its successors. Compute it in reverse topological order.
  - If G has no terminals, Λ_L fails at the sinks and therefore everywhere.
- **(b)** The only non-G move is White's pass (x, L) → (x, R), and from (x, R) every move is a G-move.
  - Black makes finitely many moves in any play, since G is finite and acyclic, and plays alternate. So every
    play is finite, the game is determined (Zermelo, KNOWN), and there are no draws.
  - Black's wins satisfy the stated recursion: Black needs a winning G-option, since it has no pass, and
    every White option, including the pass, must lead to a Black win.
  - If Black has no option at all, Black loses: the "some" over an empty set fails. ∎

**Corollary 3.5 (monotone chain). PROVED.** For every x and s:

  W in G ⊞ dud_D ⇒ W in G ⊞ off_D ⇒ W in G ⇒ W in G ⊞ on_D,

and the mirror chain holds for L.

*Proof.*
- **First step.** By (a), a winning White strategy in G ⊞ dud_D uses no passes and beats every Black
  behaviour, passes included. So it wins G ⊞ off_D.
- **Second step.** G has fewer Black options (Lemma 1.6). A Black player without moves now simply loses.
- **Third step.** on_D adds White options (Lemma 1.6). ∎

**What loopy kings do to the convention.**
- **With a White shuttle (PROVED by Theorem 3.4(b)):** the components' values (numbers, infinitesimals, nimbers)
  are irrelevant except for Black's forcing threats. White cannot be zugzwanged, and Black loses as soon as its
  context tempo runs out.
- **With shuttles on both sides (CONJECTURE):** all tempo content should disappear. Positions without threats
  should be draws, even where the convention predicts a clear winner. The 7.3 group would be of this type if
  its pawn could not promote (§5.3). *To settle:* a two-sided Proposition 3.2 — a bisimulation on the four
  combined king states, in each of which each side's shuttle is legal and each side is frozen — followed by
  Theorem 3.4(a). (Revised after review: R4 item 6: Theorem 3.4 is stated for one reservoir, so this bullet
  was not proved by it.)

**Literature (KNOWN, as summarised in [notes/lit_cgt_chess.md](../../notes/lit_cgt_chess.md)).**
- Mäser (MGONC 2002) models *promotion* as on/off. That is a different use: there `on` is the new queen's
  inexhaustible tempo.
- Elkies (GONC 1996; arXiv 1999) lists loopy values (tis/tisn, over, on/off, dud) among chess positions.
- Siegel ("Coping with cycles", GONC 3, 2009) gives chess positions of value on and upon.
- Gafni (thesis 2011) computes loopy K+P vs K values on 3×3 and 3×4 boards.

None of these treats loopy kings inside sums with game-ending decisive events.

---

## 4. Finite tempo

**Definition 4.1 (reservoir).** R_n^W has positions ρ_n, …, ρ₀ with:
- L(ρ_i) = {ρ_{i−1}} for i ≥ 1, and L(ρ₀) = ∅;
- no Black options, or only suicides.

As a CGT game it is the integer n (KNOWN: n = {n−1 | }, [WW] ch. 2).

**Theorem 4.2 (finite versus loopy tempo). PROVED after repair** (each part is proved
below).
- **(a)** Let G be short, and let R_n^W have no Black options (Black's suicides are deleted first; see (b)).
  Then G ⊞ R_n^W behaves as "White has n one-shot passes", and its BIG translation G^B + n gives the right
  outcome when G ⊞ R_n^W is first-event dominant. A sufficient condition is pairwise safety in G ⊞ R_n^W
  together with B > n + max(M_L(G), M_R(G)), with the threats counted by the corrected τ of Definition 1.10
  (revised: τ counts moves into ⊕ or ⊖ by *either* player).
  *Proof:* Theorem 1.11(a) and (b), with the corrected τ. R_n has no Black options, so it carries no threat at
  all, τ(R_n) = ∅, and pairwise safety in G ⊞ R_n^W follows from pairwise safety in G. Its n Left moves
  enter M_L, so max(M_L(G ⊞ R_n^W), M_R(G ⊞ R_n^W)) ≤ max(M_L(G), M_R(G)) + n < B, which is the bound (b)
  needs, and Theorem 1.11(b) then gives first-event dominance. (Revised after review: R4 item 3: Definition
  4.1 allowed Black suicides inside R_n, and then the stated hypothesis does *not* give first-event
  dominance — take a context whose only option is Black's move to ⊖, whose translation is −B−1, with n = 1 and
  a Black suicide at ρ₁: the frontier is B + (−B−1) = −1 ∈ 𝓡, so dominance fails for every B. The corrected
  τ counts that suicide, so the hypothesis correctly fails there; with no Black options the proof above is
  complete.)
- **(b)** If White's safe Z-moves form an acyclic graph and all Black Z-moves are suicides, then
  Z, with Black's suicides deleted, is equivalent in the D-model to R_ℓ^W, where ℓ is the length of the
  longest path of safe White moves; and in CGT, for B > ℓ, its BIG translation is the integer ℓ.
  *Proof:* induction on the number of White options, using {m₁, …, m_k | } = max m_i + 1: the value of a
  White-only option set is 1 plus the maximum of the values of its options, and dominated options can be
  deleted (KNOWN, [WW] ch. 2, [S] ch. II). In the D-model the deletion of Black's suicides is Lemma 1.7, a
  statement about results; the CGT statement needs the extra hypothesis B > ℓ, because {i−1 | B} = i holds
  only for B > i. (Revised after review: R4 item 4: Lemma 1.7 alone does not give the CGT equality, and the
  D-model equivalence to R_ℓ was not proved; both are now proved, and the CGT form carries B > ℓ.)
- **(c)** A reservoir with a White 2-cycle is on_D and equals no integer. *Proof:* take G = R_{n+1}^B, n + 1
  Black tempi with no threats.
  - G ⊞ R_n^W with White to move is L: the tempi run out on White first.
  - G ⊞ on_D with White to move is W: Black runs out.
  - on_D is not a number at all, so it differs from every integer, negative ones included.
  - The identification needs the hypotheses of Proposition 3.2 — the cycle must be reachable, and in each of
    its two states every Black Z-move must be a suicide — not merely the existence of a cycle.
  (Revised after review: R4 item 5: separating on_D from the integers has to cover the negative integers as
  well, and "is on_D" needs Proposition 3.2's hypotheses.)

So a group's tempo is *finite* (a stopper equal to an integer) exactly when its safe spare moves form an
**acyclic** graph, and *unbounded* (on or off) when they contain a cycle. The word is "acyclic", not
"non-reversible": a 3-cycle has no immediately reversible move and is still unbounded.
(Revised after review: R4 item 5: the old sentence conflated acyclicity with the absence of a 2-cycle.)

**Proposition 4.3 (no finite king tempo in isolated K+P groups). FALSE as originally stated →
PROVED after repair.** Let Z be a king group in a position without officers, with a buffer. Suppose side s plays a
non-capturing king move u → v inside F_Z, and the opponent replies outside Z. **As stated this is false:** the
step back fails if s was in check on u, or if the reply promotes. The repaired statement adds two hypotheses:
- (H1) s is not in check on u;
- (H2) the reply is not a promotion, and does not attack u.

Then v → u is legal at s's next turn and restores Z exactly.
**Consequences, with the scope narrowed (revised after review: R4 item 2, R1 item 11).** Call a king step
u → v inside F_Z *safe* if (H1) and (H2) hold and the opponent is frozen — all its Z-moves are suicides — at
both u and v. Then one safe step gives s an unlimited supply of passes: s returns to u on its next turn, the
Z-state is exactly as before, and the step can be repeated. So, among king steps *inside* F_Z, the tempo of a
pure reservoir is 0 (the opponent is frozen and s has no safe step) or ∞ (s has a safe step); it is never a
finite n ≥ 1. Three caveats, which the original wording hid:
- the dichotomy covers king steps inside F_Z only. A step onto a buffer file can be taken away later by a
  context pawn (Lemma 2.2 lets context pawns attack buffer squares), so such a supply depends on the context
  and is neither 0 nor ∞;
- a king move can be neither a suicide nor a pass: it can unfreeze the opponent without losing (§5.5 shows
  this), so the dichotomy is about pure reservoirs only;
- "safe" is not "any legal step": the opponent must be frozen at the new state v as well as at u.

*Proof.*
- u is empty, since s's king just left it and the opponent did not move in Z.
- u is not adjacent to the opponent's king: by (H1) the opponent's king was not adjacent to u when s's king
  stood there (kings may never be adjacent), and by (H2) the reply did not move it next to u.
- u is not attacked by an opponent Z-pawn, since none has moved (by (H2) the reply is not a promotion), and by
  (H1) none attacked u before. It is not attacked by a context pawn either: context pawns attack only context
  and buffer squares (Lemma 2.2), and u ∈ F_Z.
- With no sliders, the move exposes nothing. ∎

*Counterexample to the original statement (revised after review: R4 item 1).* `Kb2 Pc2 kc4 pc3`, White to
move, on flat:4x4: White is in check from pc3 and plays Kb2–a1; when Black then moves outside Z, Kb2 is
illegal, because pc3 still attacks it. The position is hand-checkable; kpsolve confirms the move lists:
only Ka1a2 and Ka1b1 are legal for `Ka1 Pc2 kc4 pc3 w -`. The step back fails because u was attacked, not
because the opponent moved.
  - Reproduce: `printf 'Kb2 Pc2 kc4 pc3 w -\nKa1 Pc2 kc4 pc3 w -\n'
    | kings/kpsolve --board flat:4x4 --ep on --promote QRBN --cap 1 --moves`.

**What this means for the "n safe spare moves" picture.** In king-and-pawn chess, a king with exactly n safe
spare moves cannot occur in an isolated group *for steps inside F_Z*: one safe step and the step back already
give infinitely many (Proposition 4.3, repaired). Steps out of F_Z are the exception, and their supply depends
on the context. (Revised after review: R4 item 2, R1 item 11: the original sentence claimed more than
Proposition 4.3 proves.)
- Finite tempo comes from **pawn** moves. That is Elkies' integers, spare pawn moves that end blocked
  (KNOWN, Elkies 1996).
- It can also come from genuine king-against-king fights, where the opponent *replies inside Z*: opposition
  and shouldering. Those are not reservoirs, and they can have any value.

**Definition 4.4 (over).** over = {0 | over} (KNOWN, [WW] ch. 11, [S] ch. VI). Right can pass forever
(over → over), and Left has one move, to 0, that ends Right's passing. (Revised after review: R1 item 11: the
note had no item 4.4, so the numbering jumped from 4.3 to 4.5; this paragraph is now Definition 4.4.)

**Proposition 4.5. PROVED.** 0 < over < x for every number x > 0.

*Proof.*
- **over > 0.** Left moving first plays to 0 and wins. Right moving first can only pass, and then Left plays
  to 0.
- **over − x < 0.** Right moving first passes. Left must then either play over → 0, leaving −x (negative, so
  Right wins), or move in −x, which Left can do only finitely often, Right passing in between. Either way
  Right wins. Left moving first faces the same two choices. ∎

**Proposition 4.6 (over with decisive terminals). PROVED.** Let over_D have positions ω and 0_D, with
L(ω) = {0_D} and R(ω) = {ω}. If White wins G moving second, then White wins G ⊞ over_D with either side to
move.

*Proof.* White's strategy:
- if White moves first, play ω → 0_D at once, leaving G with Black to move;
- if Black passes, answer ω → 0_D;
- if Black moves in G, answer with White's second-player strategy in G.

If Black never passes, it runs out of moves in G and must then pass, which White answers by freezing. After
the freeze Black is to move in a G-position lost for Black. ∎

**Chess reading of over.**
- Black has a safe king shuttle (endless passes), and White has exactly one move that takes away a shuttle
  square and leaves a mutual zugzwang. That move is typically a pawn move, but not by Proposition 4.3:
  Proposition 4.3 assumes a frozen opponent that replies outside Z, and in an over-group the opponent
  shuttles inside Z. (Revised after review: R4 item 8.)
- Elkies 1996 reports `over` in a study by Behting (1929), according to our literature notes. We have not
  re-checked it.
- **CONJECTURE 4.7:** no over-type group with ≤ 2 + 2 pawns fits on 3 files of the 8×6 cylinder, but over
  is realisable on the cylinder with wider groups. *Scratch evidence:* the first half; a geometric search over
  placements of ≤ 2 + 2 pawns on 3 (or 4) files found none (Appendix A). *To settle:* a wider search, then
  kpsolve. (Revised after review: R1 item 10, R4 item 8: the search described in Appendix A covered ≤ 2 + 2
  pawns, not the ≤ 3 + 2 claimed here; the conjecture is restated for what was actually searched.)

---

## 5. Applications

Patterns are named by the placement of the kings (WK, BK) and pawns (WP, BP) relative to a file X. All
move lists below were enumerated by hand. A scratch script reproduced them, and its lists for 5.1, 7.2 and
7.3 agree with [notes/diagram_audit.md](../../notes/diagram_audit.md) §C.3.

### 5.1 Position 5.1 (8×8 cylinder: Kh5 Pa4 / Kb4 Pa5) — the frozen trébuchet

- **Pattern A** (the *A-trébuchet*): WK (X−1, r+1), WP (X, r), BK (X+1, r), BP (X, r+1). Here X = a, r = 4.
  - The L3 trébuchet of `notes/lemmas.md` (flat 8×8: Kf5 Pg4 / Kh4 Pg5) is the same pattern with X = g.
  - On a cylinder all placements X are equivalent by rotation, so "5.1 relies on the seam" (lemmas.md
    Prop. 3.6) says that on a *flat* board the pattern needs both files X ± 1.
- **Self-dual. PROVED.** Swapping colours (rank r ↦ 9 − r) and reflecting the files about a maps 5.1 to
  itself. So Black's sorties mirror White's.
- **Frozen in the convention. PROVED by enumeration** (revised after review: R1 item 11, R4 item 9: the
  proof is written out here, instead of being left to the diagram audit). The group is WK h5, WP a4, BK b4,
  BP a5 on the 8-file cylinder. WK's five legal moves are Kg4, Kg5, Kg6, Kh6 and Ka6; each of them abandons
  WP a4, which Black's king then captures on a4, giving Black a passer. BK's five legal moves are Ka3, Kc3,
  Kc4, Kc5 and Kb5; the first four abandon BP a5, which White's king then captures on a5, giving White a
  passer, and the fifth (Kb5) puts Black's king on the square that guards both a4 and a5, so that White is in
  zugzwang with only pawn-blocked moves left. So every king move in the group is decisively punished, and the
  group is frozen. The enumeration agrees with `notes/diagram_audit.md` §C.3.
- **Certificate.**
  - Corollary 2.8 fails for every sortie. After ...Kxa4 the punisher's king stands on its own pawn's path,
    so it needs a king step plus 4 pushes, and the defending king is within distance 5 of a1.
  - (L1) holds for all five White sorties with T ≤ 7 (5 to 7, depending on the sortie and the budget), for
    pass budgets **k ≤ 4 and k = ∞**, with the punisher's king confined to {h, a, b}. Budgets k = 5, 6 were
    not checked; they differ from ∞ when T ≥ 6. This is scratch evidence (Appendix A) (revised after review:
    R1 item 10, R4 item 9).
  - With (L1), Theorem 2.7 makes the freeze valid in P for every context in which (L2) holds with
    μ ≥ 8 at the zugzwang nodes, and (L3) holds.
  - On 8 ranks a single free White pawn on rank 2 has μ = 5. So the certificate covers only locked or slow
    contexts. Next to fast pawns the zero has to be checked case by case (Proposition 2.10b).
- **Prediction.** The bare 5.1 is a real mutual zugzwang, (L, W) (P6 in §6). In the bare position the local
  game is the whole game, so the scratch run is a full P-model computation. It is still one throwaway
  implementation, hence a CONJECTURE.

### 5.2 Position 7.2 (Ke6 Pd7 / Kd8 Pe7) — frozen for Black only

- **Pattern B** (the *crossed blockade*): WK (X+1, H−2), WP (X, H−1), BK (X, H), BP (X+1, H−1), with X = d.
  Each king blockades the enemy pawn and guards its own.
  - The 6-rank analogue is Z_72 = Kc4 Pb5 / kb6 pc5.
- **Black's only move inside the group, Kc7, is punished with T = 1. PROVED.**
  - Kxe7 follows. Then d8=Q comes next move, guarded by Ke7.
  - Black cannot stop it: c8 and e8 are attacked by d7, and d6 and d8 are adjacent to e7.
  - In the bare group Black then has legal moves (b6, b7, b8, c6), so (L3) holds. In a context, (L3) is the
    one-square check of whether a context pawn covers all of them.
  - By Proposition 2.10(a), Black's punishment holds in **every** non-terminal context, subject to (L3) and
    (A_Q).
- **White's sorties: the certificate fails. PROVED by Lemma 2.9.** (The heading "White's sorties are not
  punished" stated as fact what is proved only as the failure of the certificate.)
  - Ke5 already stands on the e-pawn's path. Kd5 and Kf5 reach e5 next move: after ...Kxd7, e5 is not
    adjacent to d7 and not attacked by e7.
  - By Lemma 2.9, (L1) fails for these three sorties. PROVED.
  - That the three sorties are *not punished* in P (no forced promotion for Black) rests on scratch evidence
    only, and is a CONJECTURE (revised after review: R4 item 9, R1 item 11): even without passes, Black cannot
    force promotion after Kd5, Ke5 or Kf5. Only Kf7 loses, in 10 moves. In chess, kpsolve gives (D, W) for the
    6-rank analogue Z_72 bare, so White to move draws (P5).
- **Theory for 7.2 + H** (H the {a,b,h} component). Theorem 2.4(b) needs the freeze only for the loser.
  - **If White wins H** (convention, V1–V2 assumed): White wins 7.2 + H. The loser is Black, and Black's
    Z-moves are universally punished. PROVED, modulo (A_Q), (V1) and (V2) for H's own events.
  - **If Black wins H:** the convention's "Black wins" is **not certified**. At the end White, in zugzwang,
    sorties with Ke5 and blockades. The outcome is then whatever the free Black king can achieve against H.
- **The paper's 7.2.** The {a,b,h} part has outcome 𝓝 with e.p. on (audit).
  - White to move: White wins, consistent with the paper.
  - Black to move: open (CONJECTURE: it may be a draw).
- **Predictions.** The bare 7.2 is (D, W), not the mutual zugzwang (L, W) (P7). The same holds for the 6-rank
  analogue (P5).

### 5.3 Position 7.3 (Kg8 Pf7 / Kf6 Pg7) — not a zugzwang at all

- **Pattern C:** WK (X+1, H), WP (X, H−1), BK (X, H−2), BP (X+1, H−1), with X = f.
- **Both kings can shuttle.** Kg8–f8 and Kf6–g6 are safe (audit; PROVED by enumeration: every one of the
  four king placements is legal and keeps both pawns guarded).
- **But f7–f8=Q is available.** With the king on g8, the queen on f8 cannot be taken: the black king is two
  ranks away, or on e7 next to f8, which g8 guards.
- **Black cannot parry it. PROVED.** All 8 Black moves (Kf5, Kg5, Ke5, Ke6, Ke7, Kg6, g6, g5) leave f7–f8=Q
  available and safe.
- So Z₇.₃ is a White win **with either side to move**, in every non-terminal context, in P (P8):
  - the decisive event has T = 0 with White to move and T = 1 with Black to move;
  - Proposition 2.10(a) gives (L2), because Black cannot promote in one move from a non-terminal context;
  - (A_Q) is still needed for C.
- **Why the paper's "trébuchet = 0" is wrong here.** Z is not even a tempo game. It is also an instance of
  "a zugzwang where the other side's decisive event elsewhere is too slow": a Black passer created elsewhere
  is a ⊖ in the D-model but loses to f8=Q in P. So (V2) fails for Black's passers, and the D-model is wrong.
- **Without the pawn break. CONJECTURE** (revised after review: R4 item 6): if f8 were unavailable, the
  group would be a both-sides shuttle (dud-type), and Theorem 3.4(a) would make every threat-free sum a draw —
  but that needs a two-sided Proposition 3.2, which is not proved: the bisimulation must hold on the four
  combined king states, in each of which each side's shuttle is legal and each side is frozen.
  - *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. dud may not occur in small K+P groups (CONJECTURE).

### 5.4 New groups: `on` and `off` realised, and a stalemate trap

A geometric search on the 8×6 and 7×6 cylinders (scratch) found the following. Every move list is
hand-checkable.

**Z_onT1 = Ka5 Pb4 Pc5 / kc6 pb5** (7×6 or 8×6 cylinder; F_Z = {a, b, c}).
- **Structure.**
  - Black's king blockades the white pawn c5, which stands on the 5th rank and promotes on c6. The king also
    guards b5.
  - White's b4 guards c5.
  - White's king attacks b5 from a5 or a6, and **shuttles a5 ↔ a6**.
- **Black's only legal move inside the group is Kd5. PROVED.**
  - On c6 the king stands on the top rank. Its neighbours are b5, b6, c5, d5 and d6.
  - b5 is Black's own pawn, blocked by b4, with nothing to capture.
  - b6 and d6 are attacked by c5, and b6 is also adjacent to the white king.
  - c5 is guarded by b4.
- **Kd5 is punished with T = 1. PROVED.** Kxb5 follows, and then c6=Q, guarded by b5.
  - Black cannot stop it: c4 and c6 are adjacent to b5, and d6 is attacked by c5.
  - Black is not stalemated after Kxb5: e6 is free in every context of §6.
- **So Z_onT1 realises `on`. PROVED in P** (revised after review: R1 item 11: the claim carried no label).
  By Proposition 3.2, its chess bridge and Proposition 2.10(a), Theorem 3.4(b) applies in every non-terminal
  context that leaves d5 legal and leaves Black a legal move after Kxb5. Black loses unless it has a forced
  decisive event against a passing White. Predictions P2 and P10; in chess the conclusion needs (A_Q), which
  is checked position by position (kpsolve: (W, W) for all ten P2 and P10 positions).
- **Literal pawn-only scoring.** It calls c5 passed (+BIG), and here that agrees with the truth, for the
  wrong reason: it also says "White wins" in the trap below, which is a draw.
- **Z_offT1 = Kc1 Pb2 / ka2 pb3 pc2** is the colour-reversed group. White's only move is Kd2; Black's king
  shuttles a1 ↔ a2. (P3)

**The stalemate trap. PROVED** (by enumerating every legal move; P1). On the 7×6 cylinder, take
Ka5 Pb4 Pc5 Pe2 Pe4 / kc6 pb5 pe5.
- e4 attacks d5, so Black's king has no legal move. Black's b5 and e5 are blocked.
- **Black to move:** Black is stalemated.
- **White to move:** all five White moves (Ka6, Kg4, Kg5, Kg6, e2–e3) leave Black stalemated.
- So the result is (D, D). The convention says (W, W), whether Z is read as 0 with H = +1 or as on.
- (V1b) fails.
- The mirror position Kc1 Pb2 Pe2 / ka2 pb3 pc2 pe3 pe5 is (D, D) as well. There White is the side
  stalemated: e3 covers d2.

### 5.5 A dropped pawn that does not lose

Z_on = Ka4 Pb2 / kc4 pb3 (8×6 cylinder).
- **It passes the convention's test. PROVED by enumeration.** Every Black king move drops b3, after which
  White has a passer and Black none, and White's king shuttles a3 ↔ a4.
- **But Black has an escape. CONJECTURE (scratch evidence; kpsolve agrees).** After the sortie Kc5 and Kxb3,
  White cannot force promotion even without passes; after Kd4 and Kd5, White wins only if Black has no spare
  move. Black's legal moves in the group are Kc5, Kd4, Kd5 and Kd3 (revised after review: R1 item 10 — Kd3
  was missing from the original list; Kc3 is illegal because White's pawn b2 attacks c3), and kpsolve confirms
  that the escape is exactly Kc5: `Ka4 Pb2 kc5 pb3 w -` is (D, D) — a draw, with or without the passes — while
  `Ka4 Pb2 kd3 pb3 w -`, `Ka4 Pb2 kd4 pb3 w -` and `Ka4 Pb2 kd5 pb3 w -` are (W, W).
  - Reproduce: `printf 'Ka4 Pb2 kc5 pb3 w -\nKa4 Pb2 kd3 pb3 w -\nKa4 Pb2 kd4 pb3 w -\nKa4 Pb2 kd5 pb3 w -\n'
    | kings/kpsolve --board cyl:8x6 --ep on --promote QRBN --cap 1 --moves`.
- So "drops a pawn" is not "loses". (V2) fails, and the group is not an `on`-group.
- Z_onT1 above is the repaired version: the punishment there is one move deep.

### 5.6 The engine-suite observation, explained

RESULTS §1 reports that 41 of 449 trébuchet king moves draw and 7 win in the tablebase. Those positions are
on the flat 8×8 board, with the component on a–d and only the e-file between.
- The White king's sortie squares e4–e6 lie on the buffer file, next to the component. Their counter-play is
  correspondingly fast.
- *Example:* the documented draw `8/8/3p4/5Kp1/6Pk/2P5/8/8 w`, with Ke6! Kxg4 Kxd6 (engine/suite README).
  - Our count gives μ_W = 5: the c-pawn walks c4–c8 while Black is busy. **PROVED by count** (revised after
    review: R1 item 11: this chain carried no labels).
  - Black's local win after Ke6 Kxg4 takes T = 5 (scratch). **CONJECTURE** (scratch evidence).
  - So μ = T, and (L2) fails by one tempo. **CONJECTURE** (scratch evidence; Review 4 re-derived both
    numbers independently: μ = 5 = T, so (L2) does fail by one tempo — R4 item 10).
- PROVED: by Theorem 2.7 (contrapositive), every king move that does not lose in P violates (L1), (L2) or
  (L3). A move that loses in P but not in C is an (A_Q) failure.
- CONJECTURE: every one of the 48 non-losing king moves has μ ≤ T + 1 at its node: an (L2) failure, or an
  (A_Q) failure with margin one. *To settle:* compute μ and T at those 48 nodes from `engine/suite/results.json`.

---

## 6. Testable predictions

kpsolve options: `--ep on --promote QRBN --cap 1`, and `--cap 2` for the three P4 rows whose cap-1 bounds
differed. Positions use the format of `kings/SPEC.md`; append ` w -` or ` b -`. Each row gives:
- the predicted result pair (w, b), W/D/L from White's view;
- the Z = 0 convention pair (king group read as 0, H valued by `cylcgt` on its strip);
- the pair kpsolve computes in chess (C), from `kings/results/PREDICTIONS.md`;
- the theorem behind the prediction, and its label.

Reproduce the kpsolve column with `kings/kpsolve --board cyl:7x6 --ep on --promote QRBN --cap 1` on the
positions of the rows (and `--board cyl:8x6` for P10, `--cap 2` for the three P4 rows); the raw runs are in
`kings/results/theory_predictions_raw.txt` and `kings/results/theory_P4_cap2.txt`.

Context components on the e-file of the 7×6 cylinder, with values computed by `cylcgt` on a 1-file strip of
6 ranks:
- Hm1 = Pe2 / pe3 pe5 = −1;
- Hp1 = Pe2 Pe4 / pe5 = +1;
- H* = Pe3 / pe5 = \*;
- H\*2 = Pe2 / pe5 = \*2;
- H0 = Pe3 / pe4 = 0.

Each is a single file with no possible capture, so pure tempo.

| # | Board | Position family | Predicted (w, b) | Z = 0 convention | kpsolve (C) | Basis | Label |
|---|---|---|---|---|---|---|---|
| P1a | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` | (D, D) | (W, W) | (D, D) | (V1b) fails: stalemate (§5.4) | PROVED; kpsolve agrees |
| P1b | cyl:7x6 | `Kc1 Pb2 Pe2 ka2 pb3 pc2 pe3 pe5` | (D, D) | (L, L) | (D, D) | mirror of P1a | PROVED; kpsolve agrees |
| P2 | cyl:7x6 | Z_onT1 `Ka5 Pb4 Pc5 kc6 pb5` + each of {nothing, Hm1, H\*, H\*2, H0} | (W, W) in all five | (L,W), (L,L), (W,L), (W,L), (L,W) | (W, W) in all five | Thm 3.4(b) + Prop 3.2 + Prop 2.10(a) | PROVED in P; C modulo (A_Q); kpsolve agrees on all ten |
| P3 | cyl:7x6 | Z_offT1 `Kc1 Pb2 ka2 pb3 pc2` + each of {nothing, Hp1, H\*, H\*2, H0} | (L, L) in all five | (L,W), (W,W), (W,L), (W,L), (L,W) | (L, L) in all five | mirror of P2 | PROVED in P; C modulo (A_Q); kpsolve agrees on all ten |
| P4 | cyl:7x6 | Z_T `Ka4 Pb3 kc3 pb4` + each of {nothing, Hm1, Hp1, H\*, H\*2, H0} | equal to the convention: (L,W), (L,L), (W,W), (W,L), (W,L), (L,W) | same | (L,W), (L,L), (W,W), (D,L), (D,L), (L,D) | Thm 2.4(b) + Thm 2.7. (L1) holds: scratch, T ≤ 5, all budgets, confined king. (L2) holds at every loser-to-move node: scratch. (L3) not checked | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\*, H\*2, H0) |
| P5 | cyl:7x6 | Z_72 `Kc4 Pb5 kb6 pc5`, bare; and + Hp1 | bare (D, W); + Hp1 (W, W) | bare (L, W); (W, W) | bare (D, W); + Hp1 (W, W) | Black side: Prop 2.10(a) with T = 1 (PROVED in P). White side: Lemma 2.9 (escape by blockade) | all entries PROVED in P except the bare w-entry, which is a CONJECTURE (scratch: no forced promotion); kpsolve agrees on all four entries |
| P6 | cyl:8x8 | 5.1 `Kh5 Pa4 kb4 pa5` | (L, W): a real mutual zugzwang | (L, W) | (L, W) (kpsolve, exact) | Thm 2.4 + Thm 2.7 ((L1) scratch, T ≤ 7) + self-duality | CONJECTURE; kpsolve agrees |
| P7 | cyl:8x8 and flat:8x8 | 7.2 group `Ke6 Pd7 kd8 pe7` | (D, W) | (L, W) | (D, W) on both boards (kpsolve; Lichess on flat) | Prop 2.10(a) for Black; Lemma 2.9 for White | b PROVED in P; w CONJECTURE; kpsolve and Lichess agree |
| P8 | cyl:8x8; cyl:7x6 | 7.3 group `Kg8 Pf7 kf6 pg7`; 6-rank analogue `Kc6 Pb5 kb4 pc5` | (W, W) | (L, W) (read as 0) | (W, W) on 8×8 (kpsolve; Lichess on flat) and on the 6-rank analogue | unparriable safe promotion (§5.3) | PROVED in P |
| P9 | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 kc6 pb5 pf3` | (W, L): class 𝓝 | BIG with Z as `on`: (W, W) | (W, L) | Thm 3.3 versus Thm 3.4(b). Black: fxe2 and e1=Q; White: exf3, then zugzwang (Kd5 forced) | PROVED in P; kpsolve agrees |
| P10 | cyl:8x6 | Z_onT1 + k Black tempo units: k = 0 nothing; k = 1 `Pe2 pe3 pe5`; k = 2 also `Pg2 pg3 pg5` | (W, W) for k = 0, 1, 2 | (L,W), (L,L), (L,L) | (W, W) for k = 0, 1, 2 | Prop 4.3 + Thm 3.4(b): the result does not depend on k, and there is no integer threshold | PROVED in P; kpsolve agrees for k = 0, 1, 2 |
| P11 | cyl:8x6, `--frozen` | Kings parked on the a-file (`Ka1 ka6`, b- and h-files empty); pawn components on c–g; every passer and race node speed-certified (Remark 2.11 with frozen kings); condition (E). Here W(X) is the D-game of X with its own winning side, and "hereditarily sum-safe" (HSS) means that every component of X is itself sum-safe in the sense of Theorem 1.14(ii) | kpsolve `--frozen` = o(W(X)); also = o(S(X)) when hereditarily sum-safe. Where o(S) ≠ o(W) (opposite threats, Prop 1.12), `--frozen` sides with W | — | — (a harness check, not one position) | Thm 1.11 + Thm 1.14 (frozen kings satisfy V1 and V3 by fiat) | GAP (proof incomplete): the harness checks the hypotheses (revised after K3 check) |
| P12 | cyl:7x6 | Z_T + any context on e–f | Every disagreement between kpsolve (real) and `kpsolve --frozen` is witnessed, at some loser-to-move node, by a king move that violates (L1), (L2) or (L3), or by an (A_Q) or (V2) failure | — | — (a harness check, not one position) | Thm 2.4(b) + Thm 2.7 (contrapositive) | GAP (proof incomplete), restricted to the nodes where `--frozen` reports a win (revised after K3 check) |

**Notes on the table.**
- **What P2, P3 and P10 prove.** The derivations use only enumerated move lists (§5.4) and Theorem 3.4(b).
  The one-move punishment holds in every context listed, except where a context pawn covers the king's escape
  square d5 (respectively d2) — and that happens only after the *winning* side has moved its own pawn there:
  - In H\*, White's single step e3–e4 covers d5 and **stalemates Black**: kpsolve scores it a draw, so White
    must avoid it and play the shuttle (Ka6). (Revised after review: R4 item 7: the old sentence "none of them
    puts a pawn on e4 … that would cover d5" was wrong for H\*, where the pawn moves there during the window.)
  - In H\*2, White's double step e2–e4 *would* stalemate Black. In P3's H\*2, Black's double step e5–e3 would
    stalemate White. The winner simply never plays it.
- **Scratch confirmation in P.** A scratch P-model solver (no e.p.; queen safety required — a stricter P
  than Definition 1.5's, which counts any promotion as a win) reproduced every P-level entry of P1, P2, P3,
  P5, P9 and P10 that it finished:
  - P1a and P1b: (D, D);
  - all five P2 positions: (W, W);
  - all five P3 positions: (L, L);
  - Z_72 bare: (D, W);
  - Z_72 + Hp1: (W, W);
  - P9: (W, L);
  - P10 with k = 0 and k = 1: (W, W). The k = 2 run did not finish.

  This is a check of the reasoning, not a substitute for kpsolve: it computes P, not C.
- **What separates the theory from the conventions (revised after review: R1 item 5).** The old headline — "P2,
  P3 and P10 are the decisive tests of the loopy theory" — did not say which baseline it used. Against the
  note's own "Z = 0" reading (king group = 0, the context valued by cylcgt on its strip) it is right: that
  reading gets 17 of the 26 P2/P3/P10 entries wrong, and at least one of the two results in every one of the
  13 positions. Against the *literal* convention it is not: on the actual pawn sets, `cylcgt.pawns.value`
  returns +BIG for every P2 and P10 position and −BIG for every P3 position, so literal cylcgt gets all 26
  entries right and does **not** separate the theory from cylcgt. The positions that do separate them are P1
  (the stalemate trap: both readings say (W, W) and (L, L), the truth is (D, D)), P5 and P7 (the literal
  reading has no answer — it scores a race at move 0 on the 6-rank analogue — while kpsolve settles P5 bare as
  (D, W)), P9 (both readings predict (W, W), the truth is (W, L)) and P4 (below). Over the 25 exactly
  determined predictions of `kings/results/PREDICTIONS.md`, the theory holds in 22 and literal cylcgt in 16;
  the three positions literal cylcgt scores as a race (P5 bare, P5 + Hp1, P8 6-rank) have no answer from it
  at all.
- **What P4 tests, and how it failed.** P4 was the positive control: the theory predicts that the convention
  is *right* there. kpsolve refutes it in 3 of the 6 contexts.
  - H\* and H\*2 with White to move are draws, not (W, L). In H\* every White king move loses (Ka5, Kb5, Kg3,
    Kg4, Kg5) and White's only drawing move is e3–e4; in H\*2 the position is a draw as well.
  - H0 with Black to move is a draw, not (L, W): Black's king draws by Kd3 or Kd2.
  - The mechanism: the defending king walks to the locked context pawns and attacks the stuck pawn there
    (…Kd3, …Kd2, …Kd4). In H0 after …Kd3 the white king is confined to the a- and b-files: Kg4, Kg5 and Kg3
    all lose, while Ka5, Kb4 and Kb5 draw. This is what Proposition 2.10(b) predicts — the zero of the group is
    context-dependent, a CONJECTURE after Proposition 2.10(b), now supported in C by P4 — and the (L2) margin
    the theory assumed does not survive the context.
  - The same three contexts are exactly the ones in which the Z = 0 convention and literal cylcgt are wrong
    too, so the refutation is a fact about the positions, not about the convention.
- **P11 and P12** turn Theorems 1.11, 1.14 and 2.7 into checks of the solver.

---

## 7. Trying to break the proofs

Each item is a counterexample type the task named, or one found while writing.

1. **A zugzwang where the mover can make a decisive threat elsewhere first.**
   - In the D-model a mover with a decisive option is not in zugzwang, so nothing breaks there.
   - In P the threat may be too slow. In 7.3, a Black passer elsewhere loses to f8=Q.
   - That is a (V2) failure for the passer, not a gap in Theorems 1.14 or 2.4, which assume (V2). The
     certificate of Remark 2.11 detects it through (L2).
2. **Double threats.**
   - They are just Λ-positions in Theorem 3.4: every reply leaves a threat. No proof uses "one threat at a
     time".
   - Theorem 1.11 needs pairwise safety only *between* components. Several threats inside one component are
     allowed.
3. **Stalemate.**
   - It broke the naive argument: Lemma 1.7 is false under chess rules.
   - Hence (V1b) in Theorem 1.14, (L3) in Definition 2.6, the "every budget" clause in (L1), and the traps
     of §5.4.
   - Remaining gap: (L3) is not checked for P4.
4. **En passant.**
   - Lemma 2.2: an en passant capture lands on the captured pawn's file, so it never crosses the buffer.
   - Inside components, the sum needs condition (E) (L1.6–1.7 of `notes/lemmas.md`). Theorem 1.14(V1a)
     assumes it.
   - The scratch solver ignores en passant. In every local game it was used on, the defender had no pawns,
     so no en passant capture exists (PROVED: it needs a pawn of the capturing side).
   - In the full positions of §6 no double step lands beside an enemy pawn on the same rank, so no en passant
     right ever arises.
5. **A king that leaves Z and catches a passer.**
   - That is a Z-move made while a context passer exists, so the D-model has already ended. The failure is
     (V2) for the passer.
   - Remark 2.11 requires the passer's local game to contain both kings.
   - The engine-suite escapes (§5.6) are this type. Theorem 2.7 explains them only as certificate failures;
     it does not claim to predict which ones draw.
6. **Checks.**
   - Context pawns never attack F_Z (Lemma 2.2).
   - Inside Z, checks are part of Z's own move lists. The scratch geometry includes legality under check.
7. **Extra moves of the winner.**
   - Z_onT1 gives White king moves to g4–g6 that are not shuttle moves. Lemma 1.6 and the sharp form of
     Theorem 1.14 cover the winner.
   - When Black is the winner (P9, Black to move), Black's forced line was checked against *all* White moves.
     Black promotes on e1 at its second move, and no White king square is within reach of e1.
8. **Is the 2-cycle really equivalent to a self-loop?**
   - The bisimulation in Proposition 3.2 needs *both* shuttle states to have identical properties.
   - In Z_on (§5.5) one state allowed a non-losing Black sortie, so it is not an `on`-group. That is why
     Z_onT1 is used instead.
9. **Theorem 3.4(a) with no terminals.** It reproduces the known fact that G + dud is drawn, which is a
   consistency check.
10. **Over-claiming from the scratch solver.**
    - It found the 7.2 escapes and confirmed Prop. 3.5 of `notes/lemmas.md`: Black wins in 6 moves after
      Kf5–e4 Kxg4, the same length as the 14-ply line quoted there. That is a cross-check of sorts.
    - But it is one implementation, written today. So every claim resting on it is a CONJECTURE.
11. **(A_Q) on 6-rank boards.**
    - KQK on the 7×6 and 8×6 cylinders has not been checked. Every "PROVED in P" becomes a chess claim only
      after kpsolve confirms it.
    - A reason for caution: on short boards a lone king is closer to the queen.

Downgraded while writing:
- "The trébuchet zero is universal": now Proposition 2.10(b) plus a CONJECTURE.
- "A dud group exists in small K+P positions": now a CONJECTURE.
- "The bare 5.1 / 7.2 / Z_72 results": CONJECTURES with scratch evidence.

---

## 8. Open questions

1. **Tempo matching** (CONJECTURE). Suppose a group's punishment wins only in the plain local game, not
   against passes. Is it still decisive in contexts that are second-player wins for the punisher, with each
   defender tempo answered by a punisher tempo?
   - The question is untested. Every trébuchet placement checked on the 7×6 cylinder satisfied (L1) for every
     budget.
   - The only plain-but-not-passing wins found are Z_on's sorties Kd4 and Kd5 (§5.5). Z_on also has an
     outright escape, Kc5, so it cannot test the question.
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist? Both
   need wider searches.
3. King-against-king fights inside Z (opposition, shouldering) are genuine short or loopy games. What values
   occur? This is where finite king tempo can live, by Proposition 4.3.
4. A version of Theorem 1.11 for loopy components: the D-semantics analogue of Siegel's stopper sums.
5. Gafni's K+P vs K values without edges (plan item A8): the cylinder KPK table in `atlas/cylinder/kpk` is the
   starting point.

---

## Appendix A. The scratch computations

These are throwaway Python scripts in the session scratchpad. They are not in the project and were run once.
Re-implement them before relying on any number.

- **Geometry.**
  - Legal king and pawn moves on a W×H board, flat or cylinder, following `kings/SPEC.md` without en passant
    rights. Kings may not be adjacent; a move may not leave one's own king attacked by a pawn.
  - "Drops a pawn" means the opponent's king can then legally capture an undefended pawn.
  - It reproduces the move lists of `notes/diagram_audit.md` §C.3 for 5.1, 7.2 and 7.3.
- **Group search.** On the 8×6 and 7×6 cylinders: all placements of the kings and of ≤ 2 + 2 pawns on 3 (or 4)
  files, with no passer at the root. Each placement was classified as frozen, on, off, dud or over by one-ply
  tests. It found: (revised after review: R1 item 10, R4 item 8: the search covered ≤ 2 + 2 pawns, so every
  claim that depends on it is stated for ≤ 2 + 2 — Conjecture 4.7's "≤ 3 + 2" was wrong. The "no passer at the
  root" test is the note's own, not cylcgt's: cylcgt's passed test calls Z_onT1's c5 passed, so the search
  would have rejected Z_onT1.)
  - the A-trébuchet placements;
  - Z_onT1 and its mirror;
  - Z_on (§5.5);
  - no dud and no over group.
- **Local promotion game.** Retrograde least fixed point over (position, side to move, pass budget k ≤ 4 or
  ∞), with only Z's pieces on the board.
  - The attacker wins by promoting to a queen that cannot be captured at once.
  - Stalemate, a defender promotion and infinite play are attacker failures.
  - Option: confine the attacker's king to F_Z.
  - The reported T is the number of attacker moves under best play.
- **μ.** A breadth-first search over the defender's moves alone (king and pawns), with the other side's
  context pawns fixed and its king absent. It covers every context position reachable inside the e-file
  context.
- **Full P-model check.** The local promotion game run on the full positions of §6, with no budget (k = 0).

---

## References

- **[WW]** E. R. Berlekamp, J. H. Conway, R. K. Guy, *Winning Ways for your Mathematical Plays*, 2nd ed.,
  A K Peters, 2001–2004.
  - Vol. 1, ch. 1–2: outcome classes, G = 0 iff second-player win, integers, simplicity, dominated options.
  - Vol. 2, ch. 11 ("Games Infinite and Indefinite"): on, off, over, dud, stoppers.
- **[S]** A. N. Siegel, *Combinatorial Game Theory*, Graduate Studies in Mathematics 146, AMS, 2013.
  - Ch. I–II: short games, outcome classes, numbers, the simplicity theorem.
  - Ch. VI: loopy games, stoppers, on/off/over/dud, least-fixed-point outcomes.
- **[E]** N. D. Elkies, "On numbers and endgames: combinatorial game theory in chess endgames", in *Games of
  No Chance*, MSRI Publ. 29 (1996), 135–150; arXiv math/9905198 (1999).
  - Mutual zugzwang = 0; spare pawn tempi = integers; loopy values in chess.
- **Cited only as summarised in `notes/lit_cgt_chess.md`, not re-read for this note:**
  - Mäser (MGONC 2002);
  - Siegel, "Coping with cycles" (GONC 3, 2009);
  - Gafni (thesis, 2011);
  - Larsson–Nowakowski–Santos, "Affine normal play" (GONC 6, 2025).
