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
repaired proof, except those of T2.7, P12 and the sharp form of 1.14 (see the K7 and K9 caveats below), was written by a free external model and
read once by the integrator. Each was then checked
independently by a fourth model (task K3, opencode beam-free, `kings/delegate/out/K3/REPORT.md`): 13 of the
17 are SOUND, and 4 are downgraded to GAP (the sharp form of 1.14, Theorem 2.7, P11, P12). No repaired proof
was found false. Theorem 2.7 and P12 were repaired afterwards (task K7, 2026-10-22): they are PROVED after
repair in P (revised after K7, 2026-10-22). K3's objection to Theorem 2.7 read it as a statement about the
D-model; it is a statement about P (Remark after Theorem 2.7). **Caveat for the K7 repair:** it is one
AI-written proof. Three AI reviewers read its first draft and found one real error, in the window form (b),
which was false when Q carried an en passant right with its target off F_Z; the text now accounts for that
right (revised after K7, 2026-10-22). Three more AI reviewers (logic, chess, consistency) then read the
final text, with the e.p. clause. They found no counterexample and no false step in the proof, only wording and
bookkeeping errors, which were corrected in the same pass (revised after K7, 2026-10-22). The corrected text has
not been read again. K3 did not see the repair, and no human has re-derived it. **Caveat for the K9 repair (sharp
form of Theorem 1.14):** a free model drafted it; two AI reviewers found real errors (the draft claimed that the
D-winner never moves in Z, and never fixed what D(X) is on Z); a Sonnet agent rewrote it as a simulation lemma
(an induction on the rank of the D-win), and the integrator read the rewrite. It has not been re-checked by
another reviewer (revised after K9, 2026-10-22). **Caveat for K10 (Proposition 2.11, P11):** a free model drafted a
passer certificate; two Sonnet reviewers found it FALSE (a capture of a β pawn on a neighbouring file lets an ω pawn
stop the passer, and checks, kings, one move order, races and en passant were mishandled). A Sonnet agent rebuilt the statement and
proof, and the integrator read it step by step and re-ran its examples. K10v (opencode beam-free; Codex was out of quota) wrote an independent checker of (H1)–(H5) without reading K10's files and found 0 violations
against `kpsolve --frozen` (the computation is CHECKED-2); its verdict "Steps 0–5 SOUND" came without a written derivation,
so it was no re-derivation (revised after K10v, 2026-10-22). In a second round two fresh Sonnet reviewers found no error in the proof and 0 violations in 5.7 million certified positions; they found that P11 must also certify a root that already has a passer, which is now part of P11. No model outside the Sonnet family has re-derived the proof (revised after the K10 second round, 2026-10-22). With Proposition 2.11,
P11 is PROVED in P in a conditional form: the passer and race terminals must be certified, and a root that already has a passer must itself satisfy Proposition 2.11 (revised after K10,
2026-10-22). So none of K3's four GAP downgrades remains GAP. The scripts behind the checks
of Appendix A are copied to `kings/delegate/out/K7/scripts/` (their paths point at the old scratchpad), and their raw
output is in the local, untracked archive `kings/delegate/out/K7/k7_k9_scratch.tar.zst`. All checkers are AI models; no human has re-derived these proofs. The fixes marked "T30
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
| T1.14, sharp form | GAP → PROVED after repair: simulation form on a σ-certified set N of P-positions, with (S1) the winner's step, (S2) the loser's step (a D-move or a P-loss) and (S3) no stalemate; proof by induction on the D-rank. The winner may move in Z. Not yet independently re-checked (revised after K9, 2026-10-22) | R2 item 6; K3, K9 |
| §1.5 "each hypothesis is needed" | (V1b), (V2), (V3), (V4): counterexamples given. (V1a): none given, so "needed" is a CONJECTURE | R1 item 4, R2 item 7 |
| L2.2 | PROVED | unchanged |
| T2.3 | PROVED (also KNOWN), for every integer B ≥ 1 | its direct proof, overwritten by a misanchored edit in the 2026-10-21 revision, was restored after the T30 audit |
| T2.4 | FALSE as originally stated (the "P-game of the context" option) → G under normal play (no draws), plus a strategy-transfer form (c) for games with draws: PROVED after repair | R2 item 4 |
| D2.6, (L3′) | withdrawn: it never applies to a 3-file group, and it does not give (L3) | R1 item 8, R3 item 2 |
| T2.7 | GAP → PROVED after repair, in P (revised after K7, 2026-10-22). K7 made the local game of (L1) explicit (the first promotion ends it, a promotion by s is a failure for s̄, s̄'s king stays on F_Z, no pass in check, a mate of s is a win for s̄, a stalemate of s̄ is a failure; s cannot be stalemated in the local game because it may pass). K7 also fixed the choice that K3 and the T30 recheck left open: (L2) counts s's king and **context** pawns only, and s's Z-pawns are covered by (L1); (L3) is stated over the real play of a guided strategy, in which s̄ makes Z-moves only. K3's objection (a context passer within the window ends the game in s's favour) assumes that a passer is terminal. That holds in the D-model and not in P: in P only a promotion is terminal, and (L2) bounds it. Whether a passer is decisive in D is (V2), a hypothesis of Theorem 1.14, which Theorem 2.7 does not claim. The window form (b) of the first K7 draft was FALSE when Q carried an e.p. right with its target off F_Z (counterexample in the text); (L2) now counts that right. The theorem gives a P-win only. The bound μ_s ≥ T + 1 is sharp in P, and in chess no margin of μ_s replaces (A_Q) (examples in the text). A second review round found no false step | R1 item 3, R3 items 2 and 3; K3; K7 |
| C2.7′ | PROVED in P (revised after K7, 2026-10-22): the contrapositive of Theorem 2.7(a), the content of P12. If `--frozen` reports a win for σ and every king move of σ̄ at the nodes of σ's winning strategy is a P-loss, then σ wins P. The chess form adds (A_Q) | K7 |
| C2.8 | PROVED (wording corrected). The finite-k clause was made a side remark after K7 (revised after K7, 2026-10-22). A reviewer found no counterexample in 9566 placements on 4 boards (scratch) | R3 item 7; K7 |
| L2.9 | GAP → PROVED after repair, now under the weaker hypothesis (B1): at most one s̄ pawn is attacked by an s pawn (it holds if s has no pawn on f ± 1, if s̄ has a single Z-pawn, and automatically on boards with 4 ranks) (revised after K22, 2026-10-27). **The statement without any hypothesis is FALSE** (revised after K22, 2026-10-27): with two attacked s̄ pawns s can lose, for example cyl:7×6 `Ka5 kc6 Pc3 Pc4 pb4 pb5` with Black (s) to move, F_Z = {a, b, c}: White (s̄) forces a promotion within 3 moves against a defender who may pass (CHECKED-2: K22's C++ and Python solvers and the referee's own solver agree). The flat:4×5 version `Kd4 kb5 Pb2 Pb3 pc3 pc4` is also hand-verified, and a flat:3×5 version `Kc4 ka5 Pa2 Pa3 pb3 pb4` is CHECKED-2. The cylinder position is also a White win in P with real kings (COMPUTED-1: one run of `kp_p --pmodel`, K7's P-model build of kpsolve). Bounded search (K22: up to 3 + 3 pawns, and 4 + 4 on some small boards): no White win with at most one attacked s̄ pawn among 74,469,430 roots, within the boards and pawn counts searched (COMPUTED-1: one C++ solver, with a Python spot check on 92 roots; the proof of (B1) is separate and does not use this search) | R1 item 9, R3 item 4; K22 |
| P2.10(a) | FALSE as originally stated (H = 4) → H ≥ 5: PROVED after repair, under both the textbook and the e.p.-aware passed test, for chess-legal contexts and s's context pawns. (L2) counts context pawns only, so there is no Z-pawn proviso: s's Z-pawns are covered by (L1), whatever their distance from promotion (revised after K7, 2026-10-22). T30 audit: the proof lacked a step for en passant (now added). The stronger claim that no pawn of *either* colour stands one move from promotion needs H ≥ 6 under the e.p.-aware test | R1 item 7, R3 item 1; T30 audit and recheck |
| P2.10(b) | PROVED (the example; it needs width ≥ \|F_Z\| + 4). "The zero is context-dependent": CHECKED-2 for Z_T in P (revised after K23, 2026-10-27: Z_T acts as 0 beside {Pe3, pe4} and not beside {Pe2, pe3} on cyl:7×6, and the same for the group of §5.1 on cyl:8×8; three implementations agree; no hand proof, so not PROVED). For every frozen group with T ≥ 2 it is a CONJECTURE. P4 does not show it in P: its six rows equal the convention there | R3 item 5; K23 |
| R2.11 | GAP → PROVED in P (frozen), as a sufficient condition (revised after K10, 2026-10-22): Proposition 2.11 and Corollary 2.11a give (V2) at a passer or race terminal under (H1)–(H5): a clear path for pawns and kings of both colours, no check, no stalemate, no interference of an ω pawn that captures a β pawn on a neighbouring file, and the timing bound for both move orders over all ω pawns. K10's first draft was FALSE (it ignored all of these); the statement and proof were rebuilt by a Sonnet agent and read step by step by the integrator. One AI proof, checked on 954,392 parked and 60,000 random-king positions with side to move against `kpsolve --frozen` (0 violations; scripts in `kings/delegate/out/K10/scripts/`). Computation CHECKED-2 by K10v (independent code, opencode beam-free): 0 violations in 146,328 certified instances (an instance is a position, side to move, β and p; 119,654 distinct positions with side to move) and 5,716 with an e.p. right; its proof verdict SOUND has no written derivation, so the proof is not re-derived by a second model (revised after K10v, 2026-10-22). Second round: two fresh Sonnet reviewers read the proof and found no error, and their own code found 0 violations in 5,730,596 certified positions with side to move (6,783,482 instances) on cylinders, plus 434,429 positions on flat boards, also 0 violations; no model outside the Sonnet family has re-derived it (revised after the K10 second round, 2026-10-22). Real kings: nothing proved, the square rule is a CONJECTURE (scratch evidence) | R3 item 6; K10 |
| P3.2 | PROVED; chess bridge PROVED after repair (adds (V1a)) | R4 item 7 |
| T3.3(a) | PROVED (also KNOWN) | R4: sound |
| T3.3(b) | FALSE as originally stated (with ∅ the dead position the pair is (W, L)) → { \| ⊖} ⊞ on_D is (L, L): PROVED after repair | R1 item 2 |
| T3.4 | PROVED | R4: sound |
| C3.5 | PROVED | R4: sound |
| P3.2′ (two shuttling kings are a dud) | D-model: PROVED (new, K14; revised after the K14 referee, 2026-10-27): a p-morphism onto dud_D on the four combined king states, for every D-game G; inequalities when one side has further Z-moves; a win needs only the half of the states in which the winner's king stands still; all eight shuttle arrows are needed (counterexamples). The proof was re-checked by one referee (same model family) and the statements by two brute-force implementations, on short and loopy G, 0 violations (COMPUTED-1 for the data). Chess bridge (Theorem 3.2‴): PROVED in P, conditional on (V1a-ctx), (V2-ctx) and the per-group hypothesis (Pun) that every non-shuttle Z-move is decisively punished; stalemate is excluded automatically. (Pun) is the only gap of the bridge; the chess statement also needs (A_Q). Existence (revised after the K14 referee, 2026-10-27): Z_B (§5.7; flat 7×6; White king b2/c3, Black king a4/b5, pawns Pa3 Pb4 pb3 pc4) has every non-shuttle move losing at once, and Z_B alone is (D, D) at all 8 roots in P: CHECKED-2 (kp_p and the independent solver ref3). Beside every context tested the P-result of G ⊞ Z_B equals r(G ⊞ dud_D): COMPUTED-1 (68 contexts, 12 contexts on files e–g, and the first 660 of 885 contexts of ≤ 2 + 2 pawns on f, g; 225 contexts untested). In chess with cap 1 the bounds at the 8 roots are (W, L): undecided. Open: chess (cap 2), the cylinder, other boards. Z_A (§5.7) is a second group, with one White break (Kxb4). K14's first search found no frozen group only because of a move-count cut-off (18) that excluded Z_B | R4 item 6; K14 and its referee |
| T4.2(a) | PROVED after repair (through the corrected T1.11(b)) | R4 item 3 |
| T4.2(b) | PROVED after repair (needs B > ℓ; the D-model equivalence is now proved) | R4 item 4 |
| T4.2(c) | PROVED after repair (negative integers; reachable cycle; "acyclic", not "non-reversible") | R4 item 5 |
| P4.3 | FALSE as originally stated (a king in check) → s not in check on u, reply not a promotion: PROVED after repair. The dichotomy "0 or ∞" is narrowed to steps inside F_Z with the opponent frozen at both ends | R4 items 1 and 2, R1 item 11 |
| D4.4 (over) | the numbering gap is filled | R1 item 11 |
| P4.5, P4.6 | PROVED | R4: sound |
| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched) | R1 item 10, R4 item 8 |
| §5.1, frozen | PROVED by enumeration, now written out | R1 item 11, R4 item 9 |
| §5.1, (L1) | CHECKED-2 (revised after K19, 2026-10-27). K19 wrote the local game again from Definition 2.6 and agrees with the K7 numbers: after the reply Kxa4, with k = ∞ and the king confined to {h, a, b}, T = 6, 6, 6, 7, 7 with the queen clause and T = 6, 6, 5, 6, 6 for (L1_P) (Kg4, Kg5, Kg6, Kh6, Ka6). With the pre-K7 rules the least T is 5 to 7 for each budget k = 0, …, 8 and k = ∞: the scratch run covered k ≤ 4 and k = ∞, and K19 and the referee also cover k = 5, 6, 8, which equal k = ∞. Every k ≥ 7 equals k = ∞, because the window holds at most T ≤ 7 moves of s. The five Black sorties give the mirrored numbers. (L3): CHECKED-2 (K19 and the referee's own code, each written from the definition): in the bare group it holds for all ten sorties (five White, five Black) at T, T + 1 and T + 2, with and without the queen clause. K24 adds two further implementations of the local game, written from Definition 2.6 (the K24 agent's `kings/delegate/out/K24/scripts/lg.py` and the K24 referee's `kings/delegate/out/K24/verify/lg2.py`): the lists are the same, T = 6, 6, 6, 7, 7 with the queen clause and 6, 6, 5, 6, 6 for (L1_P) (Kg4, Kg5, Kg6, Kh6, Ka6), with the same numbers of s-nodes (1025, 1326, 1939, 4273, 3985 with the queen clause). K24 ran the five Black sorties directly: Ka3, Kb3, Kc3, Kc4, Kc5 give T = 7, 7, 6, 6, 6 with the queen clause and 6, 6, 5, 6, 6 without, the mirror of the White lists (the referee did not run the Black sorties separately). The strict sufficient form (L3_F) fails in every case, because s may walk its king off F_Z (for example Kg4–Kf4), after which no king step reaches F_Z; this does not touch the (L3) above, which holds in the bare group with 0 stalemates of s on any line on which s̄ plays only winning moves, in K24's code and in the referee's (revised after K24, 2026-10-27) | R1 items 3 and 10, R4 item 9; K7; K19; K24 |
| §5.2, White's sorties | the certificate fails: PROVED (L2.9). "Not punished": CHECKED-2 (revised after K19, 2026-10-27): after Kd5, Ke5 or Kf5 Black has no forced promotion. In the local game after ...Kxd7 (with or without passes, confined or not) there is no win up to T = 13 (K19 and the referee; K19's least fixed point finds none at any T, COMPUTED-1), and in the exact P-model after the sortie the result is D against every Black reply (two solvers). Only Kf7 loses, with T = 10 (11 with the queen clause and unlimited passes). In C, kpsolve agrees on both boards and on the 6-rank analogue (P5). Revised after K24, 2026-10-27: two more implementations of the local game (`kings/delegate/out/K24/scripts/lg.py`, the referee's `verify/lg2.py`) reproduce this on both boards: no T for Ke5, Kd5, Kf5 (with or without the queen clause), T = 11 with the queen clause and 10 without for Kf7, and T = 1 for Black's Kc7. That White cannot win chess either, so that the bare group is D in C, is CHECKED-2 by Lemma 2.7a (EPW and EPB computed by two implementations) and kpsolve exact. There is no hand proof of it: Lemma 2.9 refutes (L1) for a defender who may pass, and White cannot pass (open question 7) | R4 item 9; K19; K24 |
| §5.5 | CHECKED-2 (revised after K19, 2026-10-27), with one correction. Confirmed: Black's moves are exactly Kc5, Kd3, Kd4, Kd5; after Kc5 Kxb3 White has no win for any budget k = 0, …, 6, 8 or ∞, up to T = 20 with the confinement and T = 12 without it (K19 and the referee; K19's least fixed point finds none at any T, COMPUTED-1); after Kd3 White wins with T = 5 for each budget k = 0, …, 6, 8 and ∞. Corrected: after Kd4 and Kd5 White wins the local game against each finite budget checked (T = 6 + k with the queen clause for k = 0, …, 6 and 8; without it T = 6 for k = 0 and T = 5 + k for k ≥ 1) and not against unlimited passes (no win up to the same bounds), so "only if Black has no spare move" holds for an unlimited supply only. kpsolve and the P-model agree on all four sorties | R1 items 10 and 11, R4 item 9; K19 |
| §5.6 | μ_W = 5: PROVED by count (K19's breadth-first search agrees). T = 5 and "(L2) fails by one tempo": CHECKED-2 (revised after K19, 2026-10-27: T = 5 for each budget k = 0, …, 4 and k = ∞, with or without the queen clause and the confinement; μ_W = 5 < T + 1 = 6; the scratch run, R4 and K19 agree) | R1 item 11; K19 |
| P1a, P1b (§6) | PROVED; kpsolve (D, D) | PREDICTIONS.md, as for every P-row |
| P2, P3 | PROVED in P; kpsolve agrees in C on all 10 positions; literal cylcgt also gets them right | R1 item 5 |
| P4 | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\*, H\*2, H0), in C (revised after K23, 2026-10-27). In P all six rows equal the convention (CHECKED-2, three implementations agree), so the C refutations are chess-only effects, not P effects; their cause was not examined | PREDICTIONS.md, theory_P4_cap2_moves.txt; K23 |
| P5 | PROVED in P (b entries, + Hp1); bare w-entry CHECKED-2 (revised after K19 and K24, 2026-10-27: the P-value D from K19's solver and `kp_p --pmodel` (K7's P-model build of kpsolve), and from K24's `mine.c` and the referee's `psolve.py`, each written from `kings/SPEC.md`; D in C by Lemma 2.7a, with EPW and EPB both D for White to move in two implementations, and by kpsolve exact; no hand proof); kpsolve agrees on all four entries | K19; K24 |
| P6, P7 | CHECKED-2 (revised after K19 and K24, 2026-10-27), and partly PROVED in P. **In P:** P6 = (L, W) on cyl:8×8 and (L, L) on flat:8×8 (no zugzwang there); P7 = (D, W) on both boards; in P7 w, Ke5, Kd5 and Kf5 draw and Kf7 loses. The solvers are K19's, the K7 build `kings/delegate/out/K7/scripts/draft/kp_p.c` (its flag is `--pmodel`; `kings/kpsolve.c` has no such flag), K24's `kings/delegate/out/K24/scripts/mine.c`, and the K24 referee's `kings/delegate/out/K24/verify/psolve.py`, the last two written from `kings/SPEC.md`. They agree on every entry and every per-move value (`kings/delegate/out/K24/logs/pmodel_kp_p_8x8.log`, `logs/models_p_bb_bw.log`, `verify/run8.log`). K24 compared `kp_p.c` with `mine.c` on random positions with 0 differences: 11,102 legal positions (cyl:5×6, flat:5×6, cyl:6×6, cyl:7×6) and 769 legal one-pawn positions of the 8×8 boards (`logs/crossval_p.log`; the referee did not repeat these runs). The referee compared `psolve.py` with `kp_p.c` on 1,512 random positions (1,021 legal, seven board and pawn settings) with 0 differences (`verify/xval.py`, `verify/run_xval.log`). **Theorem route for P6, CHECKED-2:** (L1) for the ten sorties with T = 6, 6, 6, 7, 7 (queen clause) and 6, 6, 5, 6, 6 (L1_P) (§5.1); (L2) is vacuous, since the bare group has no context pawn (μ_s = ∞); (L3) holds in the bare group (0 stalemates of s on any line on which s̄ plays only winning moves). The strict form (L3_F) fails in every case, because s may walk its king off F_Z, so the route uses the (L3) of Definition 2.6 only. **In chess:** P6 = (L, W), CHECKED-2 by reduction to KPK: each of the five moves of the side to move is met by the other king capturing the group's pawn (legal in every case; the referee checked this), and the KPK position is won for the capturer in kpsolve exact, in K24's queen-only solver `scripts/kpk2.c` and in `atlas/cylinder/kpk` (the referee re-ran the 12 queries with the atlas binary and with its own kpsolve build). K24 also reports that `kpk2` and atlas agree on all 326,640 cylinder and 331,352 flat KPK positions (the referee checked the table sizes, not the full comparison). P7 b = W in C the same way (Kc7, then Kxe7), on both boards. P7 w = D in C: Lemma 2.7a with EPW and EPB both D for White to move (two implementations), and kpsolve exact agrees; on flat:8×8 the Lichess tablebase agrees too. No hand proof of the P7 w draw exists: Lemma 2.9 refutes (L1) for Ke5, Kd5, Kf5, but (L1) lets White pass, so that failure does not make the sorties safe (open question 7) | `kings/results/king_groups_8x8.txt`, `king_groups_lichess.txt`; K24 (`kings/delegate/out/K24/summary.json`, `logs/`, `VERIFY.md`) |
| P8 | PROVED in P. kpsolve (W, W) on the 6-rank analogue and on 8×8, cylinder and flat; the flat 8×8 result is confirmed by Lichess | `kings/results/king_groups_8x8.txt`, `king_groups_lichess.txt` |
| P9 | PROVED in P; kpsolve (W, L) | — |
| P10 | PROVED in P; kpsolve (W, W) for k = 0, 1, 2 on the 8×6 cylinder | PREDICTIONS.md |
| P11 | PROVED in P, in conditional form (revised after K10, 2026-10-22): `--frozen` = o(W(X)) for every X of the layout whose passer and race terminals are all certified: by Corollary 2.11a at every node reached by a move and, if X already has a passer (then W(X) ends at the root), by Proposition 2.11 at X itself, with s the side to move and β the side that W(X) credits. Without the root clause the claim is false: `Ka1 ka6 Pc2 Pd4 pd3 b -` is a White win in W(X) and (L, L) in `--frozen` (revised after the K10 second round). The chain is Theorem 1.14(i) with (V1) from the layout (no check is possible, and a king move is always legal) and condition (E) of L1.6 in `notes/lemmas.md`, (V3) by fiat, and (V2) by fiat at king moves, by Corollary 2.11a at every passer and race terminal reached by a move, and by Proposition 2.11 at a root that already has a passer; the o(S) clause adds HSS with Theorem 1.11(c) and Theorem 1.14(ii). Without the certificate the equality is FALSE (`Ka1 ka6 Pc2 Pc3 pd3 pd4 w -`: o(W) is a White win, `--frozen` is (L, L)). The root clause is swept (revised after K12, 2026-10-27): on the layout (Ka1, Black's king at the top of the a-file, pawns on files c to W − 2, both sides to move, legal e.p. rights included) of cyl:6×6 and cyl:7×6 with ≤ 3 pawns a side and cyl:8×6 with ≤ 2, there are 716,962 roots with a passer; no certified root disagrees with `--frozen`, and the 20,376 roots where W(X) is wrong are all uncertified, so the clause is what excludes them (COMPUTED-1, `kings/delegate/out/K12/`). On cyl:6×6 (≤ 3 a side) and cyl:8×6 (≤ 2 a side) without e.p. rights the integrator re-ran the sweep with separate code (its own root generator, credit from `cylcgt`, `kpsolve --frozen`, and the K10r2 hypothesis checker): the same 76,744 and 68,036 roots, 0 certified disagreements (CHECKED-2 there; `kings/delegate/out/K12/REVIEW.md`). Controls: dropping (H4) gives 48 certified violations, weakening (H5) 15,868. Not yet done: P11's own harness does not test (H4) and (H5) (the K10 end-to-end script `kings/delegate/out/K10/scripts/e2e.py` does, on the roots listed under Proposition 2.11), and no model outside the Sonnet family has re-derived Proposition 2.11 (in the K10 second round two fresh Sonnet reviewers found no error) | R1 item 11; K10 |
| P12 | GAP → PROVED after repair in P (Corollary 2.7′, from the repaired Theorem 2.7), restricted to nodes where `--frozen` reports a win. The chess form adds (A_Q) at the root; the earlier alternative "(V2) failure" is not needed (revised after K7, 2026-10-22) | knock-on of R2 item 4; K3; K7 |
| L2.7a | New in K24 (2026-10-27): the transfer lemma from the two promotion models EPW and EPB to chess. PROVED; the proof is in the lemma, and the K24 referee re-derived it. The values it is applied to (P5 w, P7 w) are CHECKED-2 | K24; `kings/delegate/out/K24/VERIFY.md` |

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
- **COMPUTED-1** and **CHECKED-2** (revised after K19, 2026-10-27): labels for a finite computation, never for a
  theorem. COMPUTED-1: one implementation produced the numbers. CHECKED-2: two independently written
  implementations agree on the exact numbers (for example the scratch run and a second program, or two solvers).
  Neither label is a proof, and neither replaces PROVED for a statement over all contexts.

kpsolve results (§6) are data, not proofs: a claim that only a kpsolve run supports keeps the label
CONJECTURE (for a statement over all contexts) or COMPUTED-1 (for the finite computation itself), with
"kpsolve agrees" (revised after review: R1 item 6; after K19, 2026-10-27: CHECKED-2 needs a second, independently
written implementation, and a second run of the same code or of a build derived from it does not count).

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
  defender who may pass, and the defender cannot promote within T moves elsewhere (Theorem 2.7: PROVED after
  repair, in P; it gives a P-win, not a C-win; revised after K7, 2026-10-22). The counter-promotion half
  counts the defender's king and context pawns only: its Z-pawns are covered by the local game. That half holds
  in every chess-legal non-terminal context when T = 1, on boards with at least 5 ranks (Proposition 2.10(a)).
  For T ≥ 2 it fails in some context on boards at least |F_Z| + 4 files wide (Proposition 2.10(b)),
  so a slower punishment's zero is not certified in every context. That it is context-dependent is CHECKED-2 for
  Z_T in P (Z_T beside {Pe3, pe4} and {Pe2, pe3}, three implementations agree, no hand proof, P13); for every
  frozen group with T ≥ 2 it is a CONJECTURE (revised after K23, 2026-10-27).
- When a king has a safe square to shuttle to, Z is not 0 but the loopy game `on`/`off` (or `dud`). On that
  side BIG is meaningless, because `on` exceeds every number. The correct rule replaces ±BIG by
  game-ending outcomes (Theorem 3.4):
  - **if only White can pass,** Black wins iff Black can force a decisive event against a White who may
    pass at any time; otherwise White wins;
  - **if both sides can pass,** a side wins iff it can force a decisive event against a passing opponent;
    otherwise the game is drawn. For a king group with two frozen shuttles this is Proposition 3.2′ together with
    Theorem 3.4(a), in the D-model; in chess it also needs (Pun) and (A_Q), Theorem 3.2‴ (revised after K14,
    2026-10-27).

**Results** (section number, label, one line each):

| # | Statement | Label |
|---|---|---|
| L1.6 | Adding options for a player never lowers that player's result | PROVED |
| L1.7 | Under normal play a move to the opponent's win can be deleted; under chess rules it cannot, because "no move" is stalemate | PROVED |
| T1.9 | One component: o(A^B) is the decisive-event outcome for every B ≥ 1 | PROVED |
| T1.11 | Sums: o(S) = decisive-event outcome under first-event dominance; sufficient: no opposite-sign threats in different components (a threat is a move into a terminal by either player), and B > every tempo count. (c) is the re-splitting version | PROVED (a); (b) and (c) PROVED after repair |
| P1.12 | {⊕ \| ∅} ⊞ {∅ \| ⊖} is 𝓝 in chess semantics, but its BIG translation is 0 (𝓟) for every B | PROVED |
| P1.13 | B must be at least the tempo count: with n tempi against the threat { \| ⊖}, the BIG outcome is right iff n ≤ B | PROVED after repair |
| T1.14 | Validity: (V1)–(V3) give P = D (no draws), (V4) gives o(S) = P, and (A_Q)(X) gives C = P | (i) PROVED; (ii), (iii) PROVED after repair; the sharp form is PROVED after repair (simulation form on a certified set; revised after K9, 2026-10-22). The C part is the per-position hypothesis (A_Q)(X) |
| T2.3 | {−B \| B} = 0 for every integer B ≥ 1 | PROVED (and KNOWN: simplicity theorem) |
| T2.4 | Freeze theorem: if Z-moves are punished at every position where the mover is losing, then G + Z has the result of G, for a G scored under normal play (no draws) | PROVED after repair |
| T2.7 | Local certificate LC_T (local forced promotion against a passing defender, no faster counter-promotion by a context pawn, no stalemate of s) ⇒ decisive punishment in P; μ_s ≥ T + 1 is sharp | PROVED after repair (revised after K7, 2026-10-22) |
| C2.7′ | If `--frozen` reports a win for σ and every king move of σ̄ on the nodes of its winning strategy is a P-loss, σ wins P (content of P12) | PROVED in P (revised after K7, 2026-10-22) |
| L2.7a | If White cannot win when every promotion is a White win (EPW), White cannot win chess; the mirror for Black; both together give a chess draw | PROVED (revised after K24, 2026-10-27). The proof is written out in the lemma, and the K24 referee re-derived it independently (`kings/delegate/out/K24/VERIFY.md`, section 5) |
| C2.8 | Square-rule form: d(defender's king, promotion square) ≥ D + 2 suffices for the local part | PROVED |
| L2.9 | Blockade: a defender who may pass and whose king stands in front of the pawn is never beaten, provided at most one s̄ pawn is attacked by an s pawn (B1) | PROVED after repair under (B1) (revised after K22, 2026-10-27); (B1) covers "s has no pawn on f ± 1" and "s̄ has one Z-pawn". Without (B1) the statement is FALSE: counterexamples with two attacked s̄ pawns, hand-verified for one and CHECKED-2 for the others |
| P2.10 | For one-move punishments (T = 1) the counter-promotion condition holds in every chess-legal non-terminal context, on boards with at least 5 ranks (the defender's Z-pawns are covered by (L1), not by (L2)); for T ≥ 2 it fails in some (width ≥ \|F_Z\| + 4) | (a) PROVED after repair; (b) PROVED (the example). That the zero of Z_T is context-dependent in P is CHECKED-2 (three implementations agree, P13); for every frozen group with T ≥ 2 it is a CONJECTURE (revised after K23, 2026-10-27) |
| T3.3 | G + `on` is 𝓛 for every short G, ±BIG included, so BIG plus a shuttle predicts "White always wins" | (a) PROVED (on > numbers: KNOWN); (b) PROVED after repair |
| T3.4 | Outcome rules for G ⊞ on, G ⊞ off, G ⊞ dud with game-ending decisive events | PROVED |
| C3.5 | Monotone chain: White wins with dud ⇒ with off ⇒ with nothing ⇒ with on | PROVED |
| P3.2′ | Two shuttling kings are a dud: a component with four combined shuttle states, each side's shuttle an option and every other option a suicide, has r(G ⊞ Z) = r(G ⊞ dud_D) for every G; inequalities with further Z-moves; the chess bridge has no stalemate hypothesis | D-model PROVED; chess bridge PROVED in P, conditional on (Pun); in chess it also needs (A_Q) (new, K14, 2026-10-27) |
| T4.2 | n spare moves forming an acyclic graph = the integer n; a reachable cycle is `on`, never an integer | PROVED after repair |
| P4.3 | In an isolated K+P group, a king's spare tempo from safe steps inside F_Z (opponent frozen at both ends, mover not in check) is 0 or ∞, never a finite n ≥ 1 | PROVED after repair (hypotheses added) |
| P4.5–4.6 | 0 < over < x for every number x > 0; White wins G ⊞ over whenever White wins G moving second | PROVED (over: KNOWN) |
| §5 | 5.1 is a frozen trébuchet whose local certificate holds with T ≤ 7 (CHECKED-2, K19 and K24); 7.2 is frozen for Black only (T = 1) and White escapes by blockade; 7.3 is not a zugzwang (f7–f8=Q at once). New groups realise `on`, `off` and a stalemate trap | per item, as in the status table: 5.1 frozen PROVED, its certificate (L1) and (L3) CHECKED-2 (K19, 2026-10-27, and K24, 2026-10-27); 7.2 and 7.3 PROVED in P where stated. The bare values in chess are CHECKED-2 (revised after K24, 2026-10-27): 5.1 is (L, W) by the reduction to KPK, 7.2 is (D, W) with the w-entry by Lemma 2.7a; there is no hand proof of the 7.2 draw (open question 7) |

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
  - `kpsolve --frozen` computes the frozen-king model F of Corollary 2.7′ (a king move loses at once for the mover), not P. P itself, with free kings, is computed by K7's build `kings/delegate/out/K7/scripts/draft/kp_p.c` (its flag is `--pmodel`; `kings/kpsolve.c` has no such flag) and by the independent solvers of K19 and K24 (revised after K24, 2026-10-27: this line used to say that `--frozen` computes P).
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

**Sharp form (PROVED after repair; revised after K9, 2026-10-22).** (revised after K3 check; statement and proof
rewritten as a simulation lemma, revised after K9, 2026-10-22)

*Setting.*
- A *P-position* is a chess position before the first promotion, with the side to move. σ is one side and σ̄ the
  other. A *P-win for σ* is a forced win in finitely many moves (the least fixed point, as in Definition 1.2):
  a promotion by σ or a checkmate of σ̄. Stalemate and infinite play are not wins. The defining clauses are:
  - with σ to move, a position is a P-win if σ has a legal move that promotes or leads to a P-win;
  - with σ̄ to move, a position is a P-win if σ̄ is not stalemated (it has a legal move, or it is in check) and
    every legal move of σ̄ leads to a P-win (so none of them promotes).
- Fix a D-game D (Definition 1.1, possibly loopy) and a map π from P-positions to the positions of D that keeps
  the side to move. For D(X) of Definition 1.5, π is the identity. D(X) can be fixed in two ways, and the theorem
  below holds for both and for any other D:
  - (a) every Z-move is a terminal for the opponent of the mover, as under (V3);
  - (b) Z is a loopy component. Its terminals are the P-punished Z-moves (Definition 1.5), and its other
    Z-moves are ordinary options: the shuttle of Z_onT1 is `on_D`.

  For the chess bridge after Proposition 3.2, D = G ⊞ on_D and π sends both shuttle states to ω. For the two-sided
  bridge (Theorem 3.2‴), D = G ⊞ dud_D and π sends all four combined king states to ω.
- A legal chess move y → y′ is a *D-move* if it does not promote and π(y′) is a D-option of π(y). Legal chess
  moves that are not D-moves may exist, and so may D-options that are not legal chess moves (the move Kd5 of
  §5.4 when e4 covers d5). Both are allowed.
- W_σ is the set of D-positions (x, s) from which σ forces a D-win in finitely many moves: the least fixed
  point of "(x, σ) ∈ W_σ if some option is the σ-terminal or lies in W_σ; (x, σ̄) ∈ W_σ if every option is the
  σ-terminal or lies in W_σ" (with no option, σ̄ loses by normal play). ρ(x, s) is the stage at which (x, s)
  enters, and ρ = ∞ outside W_σ. So every option of a σ̄-node of W_σ is the σ-terminal or lies in W_σ with
  smaller ρ, and every σ-node of W_σ has such an option. Write ρ(y) for ρ(π(y), side to move at y).

*Statement.* A legal move is *closing* if it promotes with σ or leads to a P-win for σ. A set N of P-positions is
*σ-certified* if ρ(y) < ∞ for every y ∈ N and, for every y ∈ N:
- **(S1)** (σ to move) σ has a legal move that is closing, or is a D-move to some y′ ∈ N with ρ(y′) < ρ(y);
- **(S2)** (σ̄ to move) every legal move of σ̄ is closing, or is a D-move to some y′ ∈ N;
- **(S3)** (σ̄ to move) σ̄ is not stalemated.

**Theorem 1.14, sharp form.** If a σ-certified set N contains X, then X is a P-win for σ.

*Proof.* We show by induction on ρ(y) that every y ∈ N is a P-win for σ. Let y ∈ N, and assume the claim for all
members of N of smaller ρ.
- *σ to move.* Take the move of (S1). If it is closing, y is a P-win by the clause above. Otherwise it leads to
  y′ ∈ N with ρ(y′) < ρ(y), a P-win by the induction hypothesis, so y is a P-win.
- *σ̄ to move.* By (S3), σ̄ has a legal move or is in check. Consider any legal move of σ̄. By (S2) it is
  closing, so it does not promote and leads to a P-win; or it is a D-move to some y′ ∈ N. In the second case π(y′)
  is a D-option of the σ̄-node π(y) of W_σ, and it is a position of D, not a terminal, so ρ(y′) < ρ(y) by the
  definition of ρ, and y′ is a P-win by the induction hypothesis. So σ̄ is not stalemated
  and every legal move of σ̄ leads to a P-win: y is a P-win. (If σ̄ has no legal move, it is checkmated and the
  condition is vacuous.)

ρ takes values in the natural numbers, so the induction covers N. ∎ The proof is also a strategy: σ plays
rank-lowering D-moves until a closing move, and then plays a winning strategy of the P-position reached. Every
move lowers ρ or ends the D-phase, so the win takes finitely many moves.

*Reading in the vocabulary of Theorem 1.14.* Take a D-winning strategy Σ of σ that lowers ρ at every σ-move,
and let N be the P-positions that occur when σ plays Σ as legal chess moves and σ̄ plays any legal D-move.
- (S1) is (V1a) for the winner, along Σ only: Σ's move is a legal chess move **and the resulting position is the
  prescribed D-successor** (this is what "the same resulting positions" means; it excludes a king move that
  captures a context pawn or steps onto a buffer file). If Σ prescribes a σ-terminal, the move must be a P-win:
  this is (V2) at the winner's terminals. The winner may move in Z: the shuttle of Z_onT1 is a Z-move that is an
  ordinary D-option, legal in every context by Lemma 2.2 (Proposition 3.2). The claim "σ never plays a Z-move"
  belongs to the proof of (i), where (V3) makes every Z-move a suicide, and is not used here. The winner's other
  legal moves are never played and need no hypothesis.
- (S2) is (V1a) for the loser, together with (V2) and (V3): every legal move of σ̄ at a node of N is a D-move
  or a P-loss for σ̄. In reading (a) every Z-move of σ̄ is a σ-terminal, so (S2) says that **every legal Z-move
  of σ̄ is a P-loss**: this is the strong form of (V3) found by the K3 check, for all legal Z-moves and not only
  those played, because σ̄ chooses. In reading (b) an unpunished Z-move of σ̄ (a loser that owns a shuttle) is a
  D-move and needs no punishment: this is the loser's shuttle in Theorem 3.2‴, and with it the loser's stalemate
  (S3) cannot occur. A decisive event that σ̄ makes for σ is a closing move, which is (V2).
- (S3) is (V1b) restricted to the loser's nodes of N. Checkmate of σ̄ is a P-win, so only stalemate must be
  excluded. The normal-play rule of D, "no option loses", is never used.
- Checks need no separate hypothesis: the loser's moves are legal chess moves, and the winner's are legal by (S1).
- Existence is what is needed: N depends on the choice of Σ. In P2 + H\* White's e3–e4 stalemates Black (§6),
  so N has to be built from the shuttle Ka6.

The conclusion is a strategy win in P, not a normal-play result; the claim "the result is the normal-play result
of G₁ ⊞ … ⊞ G_k (Z deleted)" belongs to (i). Lemmas 1.6 and 1.7 are not used: Z is not deleted, and the winner's
extra legal moves are simply not played. Exhibiting N at a concrete position is a separate check, which this
paragraph does not do for any position of §6 beyond what the text says there. The chess bridge after Proposition
3.2 is the instance D = G ⊞ on_D; its proof cites the proof of (i), whose "σ never moves in Z" step does not cover
White's shuttle, so the sharp form is the right citation for it.

*Sharpness of (S1)–(S3)* (examples already in the note; revised after K9, 2026-10-22).
- **(S3).** P1a with real kings, `Ka5 Pb4 Pc5 Pe2 Pe4 / kc6 pb5 pe5` (§5.4; PROVED by enumeration, kpsolve
  (D, D)). The convention reads it as (W, W), and so does D, where Black's only option is
  the suicide Kd5. In chess Kd5 is illegal, Black has no legal move and is not in check, so (S2) holds vacuously
  and (S1) holds (the shuttle Ka6), yet the position is a draw. Only (S3) fails.
- **(S2), a legal Z-move of the loser that is not a P-loss.** 7.3 (§5.3), P8 `Kc6 Pb5 kb4 pc5` (kpsolve (W, W),
  PROVED in P): the convention (reading (a)) gives (L, W), but White's Z-move b5–b6=Q (f7–f8=Q on 8×8) is a legal
  move of the loser that wins. P2 + H0, `Ka5 Pb4 Pc5 kc6 pb5 Pe3 pe4` (kpsolve (W, W)): reading (a) gives (L, W)
  and White's Ka6 is not a P-loss; reading (b) is the one that applies (Proposition 3.2). P4 with H0 was listed
  here before K23 and is not an instance of (S2) in P (revised after K23, 2026-10-27): H0 is G1 of P13, Black to
  move is lost in P, so Black's sorties Kd3 and Kd2 are P-losses and the position is (L, W) as predicted (CHECKED-2,
  three implementations agree). In C, kpsolve with cap 2 gives a draw instead of (L, W), so there the sorties do not
  lose (COMPUTED-1 in C). That is a chess-only effect, outside this list; its cause was not examined.
- **(S2), a decisive event that is not a P-win (V2).** Races (L4.1 of `notes/lemmas.md`, modulo KQK) and §5.5,
  `Ka4 Pb2 kc5 pb3 w -` = (D, D): Black's Kc5 is scored as a White passer in D but is not a P-win (CONJECTURE,
  scratch evidence, kpsolve agrees). For the winner, the same failure removes closing moves: in 7.3 a Black
  passer is a ⊖ in D and loses to f8=Q in P.
- **(S1).** For an abstract D the need is trivial: with no legal move realising Σ's step, nothing transfers. For
  the natural D(X) no isolated counterexample is known, so "(S1) is needed" is a CONJECTURE, as for (V1a).

*Relation to Theorem 2.4.* Theorem 2.4 is a statement inside D (G short and under normal play, Z a king group, σ
never moving in Z). The sharp form compares P with D and lets σ move in Z. Neither is a special case of the
other. Both say that a winning strategy of a model transfers to the real game when every real move of the loser
is a model move or loses on the spot.

*Label.* PROVED after repair: the proof above is complete for the abstract statement. It has not yet been
independently re-checked, because K3 saw only the earlier draft.

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

**Definition 2.6 (local certificate LC_T). (revised after K7, 2026-10-22)**

*Data.*
- Y is a position as in Definition 2.1 with s to move: both kings on F_Z, the Z-pawns on F_Z, the context on files
  at distance ≥ 2 from F_Z, the buffer empty, no officer, no promotion yet. An e.p. right carried by Y is cleared by m. The proof of (a) does not
  use that Y is chess-legal: it uses that m and r are legal moves (see (b)).
- m is a legal Z-move of s that is not a promotion. It may take s's king off F_Z.
- r is a legal reply of s̄ to m that is not a promotion, is a Z-move, and leaves s̄'s king on F_Z. The standard r
  is a king capture of a Z-pawn of s. (If s̄ can promote at once there is nothing to certify: that is a P-win.)
- Q is the position after m and r, with s to move. T ≥ 1 is an integer.
- The *window* is the sequence s, s̄, s, s̄, … from Q. So s̄'s t-th move after r comes after s's t-th move, and
  s̄ must have won by its T-th move.
- The *projection* π(R) of a position R is R with every pawn deleted that stands off F_Z, of both colours. The
  kings (wherever they stand), the Z-pawns, the side to move, and an e.p. right whose target square is on F_Z
  are kept. Put Q_Z = π(Q). (Earlier text: "Q with every context pawn deleted". The e.p. right and the place of
  s's king were not said.)
- In (a), r is a Z-move, so an e.p. right carried by Q has its target on F_Z. In the window form (b) the
  target may be anywhere, and (L2) accounts for it (revised after K7, 2026-10-22).

LC_T(m) holds at Y if some such reply r satisfies (L1), (L2) and (L3).

- **(L1) local forced promotion against a passing defender.** The *local game* L_T(Q_Z) is played on the same
  board (same files and ranks, flat or cylinder) from Q_Z with s to move, by the rules of chess, with these
  changes:
  1. *Promotion (P semantics).* The first promotion by either side ends the game. A promotion by s is a win for
     s, whatever happens to the new piece: it is a **failure** for s̄. A promotion by s̄ is a win for s̄ if the
     new queen cannot be captured at once, that is, if no legal move of s captures it. An unsafe
     promotion ends the game as a failure for s̄.
  2. *Passes.* s may pass at any turn in which it is not in check, as often as it likes (k = ∞). s̄ may not
     pass. A pass changes only the side to move and clears the e.p. right.
  3. *Confinement.* s̄'s king may only step onto squares of F_Z. s̄'s pawn moves are not restricted; by Lemma 2.2
     they stay on F_Z.
  4. *Mate and stalemate.* If s is in check and has no legal move, s is mated and s̄ wins. With unlimited
     passes s can never be stalemated in the local game. If s̄ has no permitted move at its turn (checkmate,
     stalemate, or only king moves that leave F_Z), that is a failure for s̄.
  5. *Time.* s̄ must win with one of its first T moves, by a promotion as in 1 or by a move that mates s.
     Anything else is a failure.

  (L1) holds if s̄ has a strategy that wins L_T(Q_Z) against every behaviour of s, passes included.
  **(L1_P)** is the weaker condition in which every promotion by s̄ is a win (no queen clause). Theorem 2.7 holds
  with (L1_P) in place of (L1); the queen clause is for the chess statement (A_Q).
  - The unlimited budget models the fact that s's spare moves in the context are not known in advance; the real
    defender's options are a subset of the k = ∞ game's, and its only gain from having fewer options is
    stalemate, which (L3) excludes. The earlier phrasing "for every k" and the remark that "every k is needed"
    are withdrawn (revised after review: R1 item 3, R3 items 2 and 3).
  - The earlier clause "s with no legal move and no pass left is stalemated, which counts as a failure for s̄"
    has no content for k = ∞. Stalemate enters in two places only: a stalemate of s̄ is a failure (rule 4),
    and a stalemate of the *real* s is excluded by (L3).
- **(L2) no faster counter-promotion by a context pawn.** Let Q° be Q with s̄'s king and all Z-pawns of both
  colours deleted. s's king and the context pawns of both colours stay. Let μ_s be the least number of
  consecutive s-moves (s̄ never moves) after which a context pawn of s promotes in Q°, and ∞ if none can. The
  moves are chess moves: a king may not step onto a square attacked by a pawn of s̄, an s̄ context pawn stays
  where it is unless s captures it, and no e.p. right exists except the one described next. If Q carries an
  e.p. right whose target square is **off F_Z**, Q° keeps it: s may use it at its first move, and only then
  (the capture lands on the target and removes the s̄ pawn that has just double-stepped). A right whose target
  is on F_Z concerns Z-pawns only, which Q° has deleted, so it is dropped. In (a) Q carries no right of the first
  kind. Then **μ_s ≥ T + 1**.
  - μ_s is a breadth-first search over s's king and context pawns. A king move that captures an s̄ context
    blocker is one of the moves, so the king's help is counted, and so is the e.p. capture just described.
  - **Which s-pawns are counted.** Only the context pawns. s's Z-pawns are not counted by (L2): their
    promotions belong to the local game, where s̄'s Z-pieces stay on the board and a promotion by s is a failure
    for s̄. This replaces the earlier text, in which μ_s counted s's king and all pawns, Z-pawns included, with
    s̄'s Z-pieces removed. Reasons:
    - The proof needs (L2) only for the promotions that (L1) cannot see, and what (L1) deletes is the context.
    - The earlier count was not a lower bound for a Z-pawn: deleting s̄'s Z-pieces can raise or lower it (R3
      item 3b: 3 moves against the real 2).
    - As a hypothesis it was stronger than needed. `Ke6 ka1 Pc4 pb3 pc5`, White to move (cyl:7×6), is a Black
      win in P. Black's local win has T = 2 (b2, b1=Q), no White context pawn exists, but the old count gave
      μ_s = 2 for White's Z-pawn c4 once Black's c5 was deleted, although c5 locks it. (L1), (L2), (L3) as now
      stated all hold; the old (L2) failed.
    - With context pawns only, Proposition 2.10(a) needs no Z-pawn proviso: s's Z-pawns are covered by (L1),
      whatever their distance from promotion (a promotion by s is a failure for s̄ in the local game).
    - Anyone who wants the stronger hypothesis may assume both; the theorem holds a fortiori.
  - **μ_s ≥ T + 1 is the exact bound for P.** Step 4 shows that s promotes no earlier than its (T + 1)-th turn, and
    s̄ queens on its T-th move, which follows s's T-th turn. With μ_s = T, s promotes first (example below).
  - **(L2⁺)**, μ_s ≥ T + 2, is only a margin, and it does not give a chess win. With μ_s = T + 1, s promotes at once
    after s̄ queens (queen against queen, not against a pawn on its seventh rank). With μ_s = T + 2, s̄ has one move
    with its new queen, and a draw can still follow. No margin of μ_s replaces (A_Q) at the position (examples in
    "What Theorem 2.7 does not give"). The earlier wording, "queen-against-seventh-rank-pawn endings can be
    drawn", described the T + 1 case wrongly (revised after K7, 2026-10-22).
- **(L3) no stalemate of s in the window.** A *guided strategy* of s̄ is a strategy in the real game that at each
  of its turns plays a Z-move (a king step onto a square of F_Z, a move of a Z-pawn, or a promotion) whose
  projection is a winning move of L_T(Q_Z) at the projected position, with the remaining time. s̄ never moves a
  context pawn. (A winning strategy of the local game, read in the real game, is guided.) (L3) asks for a
  guided strategy such that, in every real play from Q in which s̄ follows it and s plays legal moves as it
  likes, s is never stalemated at one of its turns in the window. A mate of s ends the play in s̄'s favour and
  is not excluded.
  - (L1) cannot see (L3): it lets s pass, while the real s has only the context moves that exist. The danger is
    a context pawn taking away king squares that are free in Q_Z, or the context running out of moves.
  - **Sufficient local condition (L3_F).** In every line of L_T(Q_Z) in which s̄ plays only winning moves, s has
    at each of its turns before s̄'s win a legal Z-pawn move or a legal king move onto a square of F_Z. By
    Lemma 2.2 nothing off F_Z occupies or attacks a square of F_Z, so that move is legal in every real position
    reached as well.
  - The earlier sufficient condition (L3′) (every square within distance T + 1 of s's king lies on F_Z) can never
    apply for T ≥ 2 on a 3-file group, because the ball of radius T + 1 spans at least 5 files while
    |F_Z| = 3 (revised after review: R1 item 8).
  - For T = 1, (L3) is a single check: s is not stalemated at Q.

**Theorem 2.7 (sufficiency of the certificate). PROVED after repair (in P). (revised after K7, 2026-10-22)**
(The first K7 draft of (b) had no e.p. clause in (L2) and was FALSE; see the example in the list "The conditions
cannot be dropped" below.)
- **(a)** If LC_T(m) holds at Y, with reply r, then s̄ has a forced win in P after m: it plays r and then wins
  with one of its next T moves. So m is decisively punished in P.
- **(b) Window form.** The proof does not use how Q arose. Let Q be a position with s to move which is
  chess-legal, or which arises from a position Y of Definition 2.1 by legal moves m and r as in (a), and in which
  every pawn is a Z-pawn on F_Z or a context pawn on a context file, the buffer is empty, there is no officer,
  s̄'s king stands on F_Z, and no s̄ context pawn attacks s's king (automatic if s's king is on F_Z). Q may
  carry an e.p. right with its target anywhere: (L2) counts a right whose target is off F_Z, and π keeps a
  right whose target is on F_Z. If (L1),
  (L2) and (L3) hold at Q, s̄ has a forced win in P from Q. This is the form used in §5.3 and P8, with Q = Y.
  The window form does not cover a legal position in which s is in check from an s̄ context pawn that has just
  moved (s's king on a context or buffer file): there (I4) fails, and the theorem says nothing.

*Proof.* Fix a guided strategy ρ of s̄ with the property (L3). s̄ plays r and then ρ. Only Z-moves are made
by s̄, and its king stays on F_Z. Consider any real play from Q in which s plays legal moves, and write R for
the real positions in it.

- **Step 0: invariants.**
  - (I1) Every pawn is a Z-pawn on F_Z or a context pawn on a context file; the buffer is empty. This is Lemma
    2.2, applied from Q (from Y in (a)); it holds for every legal play before the first promotion.
  - (I2) No context pawn of either colour attacks a square of F_Z. A pawn attacks only adjacent files, and a
    context file is at distance ≥ 2 from F_Z. Also, a Z-pawn can capture only on F_Z or on the buffer, which is
    empty, so its captures take Z-pawns (or e.p.).
  - (I3) s̄'s king stands on F_Z.
  - (I4) s̄'s context pawns never move and are only removed (by s). No s̄ context pawn ever attacks s's king:
    none does at Q (m was legal, r changes no context pawn; in (b) this is a hypothesis), the set of squares
    they attack only shrinks, and a king never steps onto an attacked square. So s is in check at R iff an s̄
    Z-pawn attacks its king, iff s is in check in π(R).
  - (I5) *E.p. rights.* A right created by s̄ comes from a Z-pawn double step, since s̄ plays Z-moves only, so its
    target is on F_Z, and only Z-pawns of s can use it (a context pawn is not adjacent to F_Z). A right created by
    s concerns an s pawn, so it is of no use to an s context pawn. If its target is on F_Z, s̄'s Z-pawns may use it,
    and the local game accounts for this (π keeps such a right). If its target is off F_Z, no s̄ pawn that s̄
    moves can use it, and π drops it. So the only e.p. capture that an s context pawn can ever make is the
    one of the right carried by Q, if its target is off F_Z, and it can be made at s's first turn only.
- **Step 1: s's moves are local moves.** Let R have s to move. π(R) is a position of L_T(Q_Z) reached with s̄
  playing winning moves only (by induction on the play). A legal real move of s is one of three kinds.
  - *A king move* to d. Legal in R: d is not occupied by an own pawn, not adjacent to s̄'s king, not attacked by
    an s̄ pawn after the capture (if any), and if s is in check the move removes the check. Every condition
    holds in π(R): the kings are the same, the pawns present are a subset, and the checkers are Z-pawns by (I4).
    A capture of a context pawn becomes a plain king move in π(R). So the move is legal in π(R) and the
    projection of the result is the local result.
  - *A Z-pawn move* (step, double step, capture of an s̄ Z-pawn, e.p. capture of an s̄ Z-pawn, promotion). The
    squares involved lie on F_Z or on the empty buffer, and F_Z holds the same pieces in R and π(R) by (I1). King
    safety is as in the previous case. So it is legal in π(R) with the same result. In particular a promotion of
    a Z-pawn of s is a promotion by s in the local game.
  - *A context-pawn move.* It changes only context pawns, so π(R) is unchanged except for the side to move; an
    e.p. right it creates has a target off F_Z and is dropped by π, as a pass does. The e.p. capture of the right
    of Q (target off F_Z, I5) is such a move too: it moves an s context pawn and removes an s̄ context pawn. A
    context move is legal only if s is not
    in check: the checkers are s̄ Z-pawns (I4), and a context pawn can neither capture on F_Z (I2) nor block a
    pawn check. So s is not in check in π(R) and the pass is allowed. (A context promotion is treated in Step 4.)
  So the projection of the play is a play of L_T(Q_Z) in which context moves are passes. Real s-turns and local
  s-turns correspond one to one, as do s̄'s moves.
- **Step 2: s̄'s permitted local moves are legal real moves.** Let R′ have s̄ to move, and let μ̃ be a permitted
  move of s̄ at π(R′): a king step onto a square of F_Z, a Z-pawn move, or a promotion. Then μ̃ is legal in R′.
  - F_Z holds the same pieces in R′ and π(R′), and so does the e.p. right on F_Z (it comes from a Z-pawn double
    step, and only Z-pawns can capture it, because the squares next to F_Z are F_Z and the empty buffer).
  - s̄'s king ends on F_Z. The only pieces that could attack it are s's pawns and king. s's context pawns do not
    attack F_Z (I2); the rest is the same in π(R′). The kings are not adjacent, as in π(R′).
  - There are no sliders, so there are no pins.
  So guided strategies exist, and a winning strategy of the local game, read in the real game, is one.
- **Step 3: s̄ is never stuck.** A winning move of the local game exists whenever s̄ is to move before its win,
  and by Step 2 it is a legal real move. So s̄ always has a legal real move, and is never mated or stalemated before
  winning.
- **Step 4: s does not win first.** By Step 1 the projection of the play so far is a play of L_T(Q_Z) in which
  s̄ plays winning moves only, and such a play is over by s̄'s T-th move. So s has at most T turns, and the
  turn j at which s might promote has j ≤ T.
  - *A Z-pawn.* By Step 1 this is a promotion by s in a line of L_T(Q_Z) in which s̄ played winning moves only.
    That contradicts rule 1 (a promotion by s is a failure).
  - *A context pawn.* **Claim M:** μ_s ≤ j. Delete from the real play s̄'s moves and s's Z-pawn moves. What is
    left is a sequence of at most j moves of s, each a king move or a context-pawn move, ending with the
    promotion. It is a legal sequence in Q° (the position of (L2)). Indeed, s's king and the context pawns of
    both colours stand on the same squares in the real play and in the sequence, because s̄'s context pawns
    do not move and only s moves them (captures included). A king move is legal in Q°: its destination is not
    occupied by an own context pawn, it is not attacked by an s̄ context pawn (the same attackers), and Q°
    has fewer other pieces (no s̄ king, no Z-pawn), so no condition is added. A context-pawn move is legal
    in Q°: its target squares are on context files, where the real occupants are context pawns and possibly
    s's king (same in Q°); s̄'s king and all Z-pawns are on F_Z (I1, I3); the own king is not attacked
    (I4); and the only e.p. right that can be used is the one of Q (I5), at s's first turn. If it is used, it is
    the first move of the sequence, and Q° keeps exactly that right for its first move. So μ_s ≤ j ≤ T, which
    contradicts (L2). This is where the king's help in removing blockers is counted: it uses moves of s.
  - A context *passer* that exists but has not promoted in the window does nothing: in P only a promotion ends
    the game.
- **Step 5: no other ending.**
  - s cannot mate s̄: s̄ is never mated before winning (Step 3). In particular s's Z-pawns and king, which do
    attack F_Z, cannot take s̄'s last move away, because the prescribed local move is legal in the real
    position (Step 2).
  - s̄ is not stalemated (Step 3). s is not stalemated by (L3). There is no infinite play: the window has at
    most T moves of s̄.
- **Step 6: s̄ wins in time.** The projection is a play of the winning local game, so it ends within s̄'s first T
  moves with a promotion by s̄ or a mate of s. A promotion by s̄ is a legal real move (Step 2) and ends the real
  game in s̄'s favour in P. A mate of s in π(R) is a mate in R: s is in check in R (I4), and every legal real
  move of s is a local move or a pass (Step 1), and no pass exists in check, so s has no legal move in R either.
  Since s moves first after r, s̄'s t-th move comes after s's t-th, and the count is the one used in Step 4. ∎

*Part (b)* is the same proof with Q as the starting point: only (I1)–(I5) at Q were used, that s̄'s king is not
attacked at Q, and that an e.p. right is that of a pawn standing where the right says. These are the hypotheses of
(b) (they hold for a chess-legal Q, and for the Q of (a) because m and r are legal), together with Lemma 2.2.
*Part (a)* is part (b) applied to Q: m and r are Z-moves, so
every pawn is still a Z-pawn on F_Z or a context pawn on a context file and the buffer is empty (Lemma 2.2);
s̄'s king is on F_Z by the Data; no s̄ context pawn attacks s's king, because m was legal and r moves no context
pawn; and the only e.p. right Q can carry is one created by r, with its target on F_Z.

**Remark (K3's objection, answered).** K3 wrote that (L2) counts promotions only and that a context passer within
T ends the game in s's favour. In the D-model a passer is a terminal. Whether it is decisive is (V2), a hypothesis
of Theorem 1.14 (Proposition 2.11, P11; revised after K10, 2026-10-22), and Theorem 2.7 does not claim it. Theorem 2.7 is a statement about P. In P a
context passer of s is not terminal. Only a promotion ends the game, and (L2) bounds the first promotion of every
context pawn of s, passer or not, by T + 1 moves of s. A passer that stands at the end of the window has not
promoted, and s̄ has. So the objection does not apply to Theorem 2.7: it reads a P-statement as a D-statement.

**What Theorem 2.7 does not give.**
- *No C-win, and no margin of μ_s gives one.* In P a promotion wins at once. In chess the new queen must survive
  and the ending must be won. (L1) asks for a queen that s cannot capture at once, which is not enough: that s̄ wins
  chess after the promotion is the per-position hypothesis (A_Q), checked by kpsolve (§1.2). (L2⁺) is only a margin.
  The examples below are kpsolve results (`--promote QRBN --cap 2`, both bounds equal; the P values come from the
  private `--pmodel` copy of Appendix A). By the Labels rule they are data and keep the label CONJECTURE. In each,
  s̄ is Black, and (L1) with the queen clause, (L2) with the e.p. clause and (L3) hold (revised after K7, 2026-10-22).
  - μ_s = T + 1, window form with Q = the position: cyl:7×6 `Ka4 ka6 Pf4 pb2`, White to move. T = 1 (b1=Q), and the
    White pawn f4 has μ_s = 2. Black wins P. **White wins chess**, and 1.f5 is the only winning move.
  - μ_s = T + 1, form (a): cyl:7×6, Y = `Kc5 ka3 Pe2 pc4`, White to move, m = Kc5–d5, r = c4–c3,
    Q = `Kd5 ka3 Pe2 pc3`, T = 2 (c2, c1=Q), μ_s = 3. Corollary 2.8 applies (d(Kd5, c1) = 4 = D + 2). After m, Black
    wins P and **White wins chess**.
  - μ_s = T + 1, form (a): cyl:7×6, Y = `Kb4 ka1 Pe4 pa2`, White to move, m = Kb4–c5, r = Ka1–b1,
    Q = `Kc5 kb1 Pe4 pa2`, T = 1, μ_s = 2. After m, Black wins P and chess is **drawn**.
  - μ_s = T + 2: flat:6×6 `Ke6 kb1 Pf2 pc2`, White to move. T = 1, μ_s = 3 (f4, f5, f6=Q). Black wins P and chess
    is **drawn**.
  - In a sampled enumeration of one Black Z-pawn and one White context pawn, a reviewer found draws still present at
    μ_s ≥ T + 3 on flat:6×6 (4 of 659), and none at μ_s ≥ T + 2 on cyl:7×6 (scratch).
  - Hence a chess form of (V3) does not follow from any horizon condition. The paper's Conjecture `conj:cert`
    (`paper/ieee/sections/04_kings.tex`, "a certificate of horizon h implies (V3)") and the matching sentence of
    `kings/REPORT.md` are refuted as worded by the second and third example. Theorem 2.7 supports the P-version only.
- *No D-model statement.* For Theorem 1.14 the theorem supplies (V2) for the terminal "a Z-move is punished",
  at one Z-move and only in contexts where LC_T holds. It says nothing about (V2) for the passer terminals,
  nothing about (V3) for the other Z-moves, and nothing about (V1) or (V4).
- *No converse.* LC_T is sufficient only. A Z-move can be punished in P although (L1), (L2) or (L3) fails for
  every reply, for example by a different reply that the certificate does not use.
- *One Z-move at one position.* Theorem 2.4 needs every Z-move of the loser at every loser-to-move node, each with
  its own certificate. (L2) is context-dependent: for T = 1 it holds in every chess-legal non-terminal context
  when H ≥ 5, and for T ≥ 2 it fails in some context (Proposition 2.10).
- *The conditions cannot be dropped.* All examples are in cyl:7×6. The P values are kpsolve results from the private
  `--pmodel` copy of Appendix A (source: `kings/delegate/out/K7/scripts/draft/kp_p.c`). By the Labels rule they are data, and the claim that
  the conditions cannot be dropped keeps the label CONJECTURE; the races can be checked by hand.
  - (L3): `Kb5 kd5 Pb4 Pc5 Pe3 Pf3 Pf4 Pf5`, Black to move, is a draw in P. (L1) holds with T = 1 (c6=Q), Black
    has no pawn, and the White pawns on e3, f3, f4, f5 cover d4, e4, e5, e6, so Black is stalemated. This is
    the position after `Kd5 Kxb5` in `Ka5 kc6 Pb4 Pc5 pb5` with that context. In that start position Kd5 is
    still punished in P, by a different reply, so this is also an example of the missing converse.
  - (L2): `Kd6 kc2 pa3 Pe4 pe5 pf5`, White to move, is a White win in P. Black's local win has T = 2 (a2, a1=Q),
    the context is non-terminal, but μ_s = 2: exf5 and f6=Q (Proposition 2.10(b)). For T = 1 the same happens
    with a passer: `Kb5 kd5 Pb4 Pc5 pe2`, Black to move, is a Black win.
  - (L2), the e.p. clause: `Kd6 kc4 Pe3 pa4 pe4 pf3`, White to move, e.p. right on f4 (Black has just played
    f5–f3). Black (s̄) has a local win with T = 3 (a3, a2, a1=Q), (L3) holds, and without the clause μ_s = 6, so
    (L1), (L2) and (L3) would all hold. Yet White wins in P: exf4 e.p., f5, f6=Q, and its third move promotes
    before Black's third. With the clause μ_s = 3 < T + 1 = 4, as it should. The same position without the right
    is a Black win in P. This is why the first K7 draft of (b) was false. Part (a) cannot meet this case.
  - (L2), sharpness of μ_s ≥ T + 1: `Kf5 kc6 Pe4 pb3`, White to move, has T = 2 (b2, b1=Q) and μ_s = 2, and White wins
    P (1.e5 b2 2.e6=Q). With the pawn on e3 instead, μ_s = 3 and Black wins P (1.e4 b2 2.e5 b1=Q). The example
    `Kd6 kc2 pa3 Pe4 pe5 pf5` above also has μ_s = T = 2.
  - (L1) is the substance: with no local win there is nothing to transfer.

**Corollary 2.7′ (the contrapositive; the content of P12). PROVED in P (revised after K7, 2026-10-22).** Let X
have the structure of Definition 2.1 (kings and Z-pawns on F_Z, context on context files), let F be the
`--frozen` model (a king move loses at once for the mover, a promotion wins at once, stalemate and infinite play
are draws), and suppose σ has a winning strategy S in F from X. If at every node of S with σ̄ to move every
legal king move of σ̄ is a P-loss for σ̄, then σ wins P from X. Hence, if σ wins F but not P, then for every
winning strategy S of σ in F some node of S with σ̄ to move has a legal king move m of σ̄ that is not a
P-loss, and for that m, every admissible reply r (Definition 2.6, with s = σ̄ and s̄ = σ: a non-promoting Z-move
of σ that leaves σ's king on F_Z) and every T ≥ 1, (L1), (L2) or (L3) fails. A promoting reply by σ would make m a
P-loss for σ̄, so it does not occur for a move that is not a P-loss; replies that are not admissible are outside
LC_T.
- *Proof.* In P, σ plays S. S uses no king move of σ, since in F a king move is a loss for its maker, so the
  kings stand where they did at X, and the nodes of S keep the structure (a pawn move preserves it by Lemma
  2.2; a promotion ends the game). Every legal pawn move of σ̄ is the same move in F and in P, and S answers
  it. Every king move of σ̄ is a P-loss by hypothesis. Stalemates are draws in both
  models and do not occur in S. Terminals of S are promotions by σ, a P-win, and mates, equal in both. So the
  play is finite and σ wins P. The second statement is the contrapositive. Its last clause is the contrapositive
  of Theorem 2.7(a): a king move m with a reply r and T such that LC_T holds would be punished. ∎
- In chess: if `--frozen` reports a win for σ at X and the chess result at X is not a σ-win, then either P(X) is
  not a σ-win (the statement above) or (A_Q) fails at X. The comparison is one-directional: σ may win real chess
  by king moves that F forbids.

**Lemma 2.7a (transfer from a promotion model to chess). PROVED (new, revised after K24, 2026-10-27).** For a
king-and-pawn position X let EPW(X) be chess in which the first promotion by either side ends the game as a White win,
and EPB(X) the same with a Black win. Everything else is as in chess: a mate wins, stalemate and infinite play are
draws. A promotion move is legal in EPW and EPB exactly when it is legal in chess.
- (a) If White has no winning strategy in EPW(X), White has none in C(X).
- (b) If Black has no winning strategy in EPB(X), Black has none in C(X).
- (c) If both hold, C(X) is a draw.
- *Proof.* (a) By contraposition. Let σ be a winning strategy of White in C(X). Every play consistent with σ is
  finite and ends in a mate of Black. Play σ in EPW(X), against any behaviour of Black. Until the first promotion the
  legal moves, the mate test and the stalemate test are the same in the two games, so the play so far is a prefix of
  a chess play consistent with σ. If a promotion (by either side) occurs before σ's mate, the play ends in EPW as a
  White win. If none occurs, the whole play is a chess play consistent with σ and ends in the mate of Black, which
  is a White win in EPW as well. No play is infinite. So σ wins EPW(X). (b) is the same with the colours exchanged.
  (c) EPW, EPB and C are finite-state reachability games, so "neither side can force a win" is exactly the value D.
  ∎
- The lemma is used only in the direction "cannot win". The converse is not claimed (White may win EPW by a
  promotion that chess does not reward). EPW and EPB do not distinguish the piece promoted to, and the proof needs
  no cap on officers.
- *Application (CHECKED-2: two implementations of the models, K24's `mine.c`, where EPW is `bb` and EPB is `bw`, and the
  referee's `verify/psolve.py`, where EPW is `ww` and EPB is `bb`; logs `kings/delegate/out/K24/logs/models_p_bb_bw.log`
  and `kings/delegate/out/K24/verify/run8.log`).* With White to move, EPW = D and EPB = D for P7 (`Ke6 Pd7 kd8 pe7`, on
  cyl:8×8 and on flat:8×8) and for P5 (`Kc4 Pb5 kb6 pc5`, on cyl:7×6). By the lemma, White cannot win chess and Black
  cannot win chess there, so the chess value of the w-entry is D. kpsolve exact (lower and upper bound equal) gives D
  as well, and the Lichess tablebase agrees on flat:8×8. The lemma gives a chess draw, not a draw in P and not a hand
  proof of the draw in P. For P6 the values are different (EPW = D and EPB = L with White to move on cyl:8×8): the lemma
  is not used there, the chess value comes from the reduction to KPK (§6, P6).
- *Consistency test, not part of the proof.* K24 checked on 423 legal positions of cyl:5×6 (`kings/delegate/out/K24/logs/soundness_bbbw.log`)
  that no position has "White cannot win in EPW" while kpsolve gives a White win in chess, and no mirror case: 0 violations.

**Corollary 2.8 (square-rule form of (L1)). PROVED.** Suppose:
- Q_Z consists of the two kings and one s̄-pawn p, and s̄'s king is not on p's path;
- the plan is "push p every move", with D = number of ranks to the promotion square q_D;
- d(k_s, q_D) ≥ D + 2, where k_s is s's king square after m.

Then s̄ wins the local game of (L1) within T ≤ D moves:
- for k = ∞;
- for every finite k, provided s's king always has a legal move in Q_Z. This is the stalemate proviso: a
  king boxed in at a rank edge, with no pass left, would be stalemated.

The finite-k clause is a side remark (revised after K7, 2026-10-22). The local game of Definition 2.6 has k = ∞
only, and Theorem 2.7 uses nothing else. The first clause gives (L1) of Definition 2.6 for this Q_Z: p promotes
by pushes with s̄'s king never moving, s has no pawn to promote, and s cannot be stalemated because it may pass.

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

**Lemma 2.9 (blockade). PROVED after repair, under the hypothesis (B1) (revised after K22, 2026-10-27).** In Q_Z, suppose:
- all of s̄'s Z-pawns stand on one file f, and s's king stands on a square of f in front of s̄'s front pawn, so above every s̄ pawn;
- **(B1)** at most one s̄ pawn is *attacked by an s pawn*. An s̄ pawn on (f, x) is attacked iff an s pawn stands on the square
  diagonally in front of it (on file f ± 1, one rank on in s̄'s direction). The relation is symmetric: the two pawns attack each
  other, and the one that is to move may capture. (B1) holds if s has no pawn on f ± 1 (the earlier hypothesis), whenever s̄ has
  exactly one Z-pawn, and on every 4-rank board (counted from s̄'s side, s̄ pawns stand on rank 2 or higher, so two attacked s̄ pawns
  need an s̄ pawn on rank 3 or higher, attacked by an s pawn on rank 4 = s̄'s last rank, where no s pawn stands; so H ≥ 5 is needed);
- s is to move and may pass (k = ∞). An e.p. right carried by Q_Z was therefore created by s̄.

Then s has a strategy against which no s̄ pawn ever promotes and s is never mated. So s̄ wins L_T(Q_Z) for no T, in the reading
(L1) and in the reading (L1_P).

*Proof.* The strategy of s: if some s̄ pawn is attacked by an s pawn, capture it with an s pawn that attacks it; otherwise pass.
The king of s never moves. Let k be its rank. Write "attacked" for "attacked by an s pawn". Claim (J): at every turn of s̄, (J1) every
s̄ pawn stands on file f, below the king of s; (J2) no s̄ pawn is attacked. At the root, (J1) is the hypothesis. (J2) is not yet true
there, but at s's first turn (B1) leaves at most one attacked pawn, and the strategy captures it, so (J2) holds at s̄'s first turn.
Then the induction:
- *s̄ moves; (J1) and (J2) hold before its move.* A king move changes no pawn of either side except that it may capture an s pawn,
  and removing pawns attacks nothing new. A pawn move on f stays on f and below the king: a push needs an empty target and a double
  step needs two empty squares, and the king's square is occupied; so no s̄ pawn reaches a rank above k − 1, in particular none
  reaches its last rank (k ≤ H), and **no promotion is possible** by a pawn on f. A pawn capture needs an s pawn diagonally in front,
  which is exactly an attack, and by (J2) there is none; an e.p. capture needs an e.p. right created by a double step of s, and s
  never double-steps (it captures or passes), while a right present in Q_Z was created by s̄. So no s̄ pawn leaves f, and (J1) holds
  after the move. Only the moved pawn can be newly attacked, because the attack relation is a pairing of an s̄ pawn's square with an
  s pawn's square, and no other pawn moved. So at s's turn **at most one s̄ pawn is attacked**.
- *s moves.* s is not in check: its king stands on f, and s̄'s pawns stand on f and attack files f ± 1 only (on a cylinder of width
  2 the file f ± 1 is the other file, still not f); a king gives no check. So the pass is legal, and so is a capture (no sliders, no
  pins; the king stands where it was). A capture by s is never a promotion: it lands on the square of an s̄ pawn, and s̄ pawns stand
  on rank 2 or higher from s̄'s side, so that square is not on s's last rank. If an s̄ pawn P is attacked, the capture removes P. The
  capturing pawn Q came from file f ± 1 and lands on f, so it attacks no square of file f; and Q attacked only P among s̄'s pawns (it
  attacks two squares, both on files at distance 1 from Q's file, and at most one of them is on f, apart from the width-2 cylinder
  where both squares coincide). The other pairs are untouched. So after s's move (J2) holds, and (J1) holds, since P was the only pawn
  removed.
By induction, no s̄ pawn promotes, and none ever leaves f; s is never in check at its turns, so it is never mated. s̄ cannot win L_T for
any T. ∎ (The proof does not use that s̄'s king is confined to F_Z, nor the move count.)

**Remark (K22: the hypothesis (B1) is needed, and it is not necessary; revised after K22, 2026-10-27).**
- *Without (B1) the lemma is FALSE.* The earlier proof ("s passes forever") fails when an s̄ pawn can capture an s pawn. The repair
  suggested in review R3 item 4 ("pass, but capture any s̄ pawn that attacks an s-pawn") fails too, as soon as two s̄ pawns are
  attacked: s captures one and s̄ captures with the other, and the pawn that has left f is no longer blockaded. Counterexamples, all
  with Black = s to move, in the local game of Definition 2.6 with k = ∞, with and without the queen clause. For each, White (s̄)
  wins within T = 3 moves, against every Black move, the pass included. CHECKED-2 for each: at least two independently written
  solvers agree (K22's C++ solver, K22's Python solver, the referee's own solver written from the definition; see each line).
  - cyl:7×6, F_Z = {a, b, c}: `Ka5 kc6 Pc3 Pc4 pb4 pb5`. s̄ = White has two Z-pawns on c, s has b4, b5 (b4 attacks c3, b5 attacks c4).
    After 1…bxc4 White plays 2.cxb4, and the pawn runs to b6, which Ka5 guards; the black king cannot step to b5 or b6. Every Black move
    loses, the pass included (3 White moves at most). The same position is a White win in P with real kings (`kp_p --pmodel`;
    COMPUTED-1, because the referee's run used the same code as K22's); each of Black's five legal moves loses.
  - flat:4×5, F_Z = {a, b, c, d}: `Kd4 kb5 Pb2 Pb3 pc3 pc4`: each Black move, the pass included, loses within 3 White moves. After
    a pass, 2.bxc4+ and 3.c5=Q (c4 and c5 are guarded by Kd4); after 1…cxb3 2.bxc3, a black pawn run is too slow because c3–c4 gives
    check to the king on b5. Hand-verified (by K22 and again by the referee), and CHECKED-2 as above.
  - flat:3×5, F_Z = {a, b, c}, f = a: `Kc4 ka5 Pa2 Pa3 pb3 pb4`. s̄ = White has two Z-pawns on a, s has b3, b4 (b3 attacks a2, b4
    attacks a3), and the black king stands on a5, above both. CHECKED-2 (K22's Python solver and the referee's solver; the
    integrator re-ran both); not hand-verified.
  - *Size.* A counterexample needs at least 5 ranks, because (B1) is automatic on 4 ranks (PROVED, in the statement above), and 5
    ranks suffice (the flat:4×5 and flat:3×5 examples). Any violation of (B1) needs two s̄ pawns on f and two s pawns. The width is
    not established as minimal: 3 files is the narrowest board with a counterexample found, and boards with fewer than 3 files were
    not searched.
- *(B1) is sufficient and not necessary.* In K22's bounded enumeration (the boards and pawn counts of the search), s̄ wins 22,456 of
  the 2,233,320 roots with two or more attacked s̄ pawns (about 1.0%); the positions of the kings decide. COMPUTED-1: one C++
  implementation, a Python solver agreeing on a spot check of 92 sampled roots, and the referee did not reproduce the counts. The
  referee's own random samples (its solver, win searched within T ≤ 6 or 7) show the same pattern, no White win with at most one
  attacked pawn and wins only with two or more; they give 5% to 8% lost on flat:4×5 and cyl:7×6, a higher share than 1.0%
  because of the small boards and capped pawn counts, so the 1.0% describes K22's enumeration and is not a general rate.
- *Checks of the proof.* The referee re-derived the proof step by step against Definition 2.6 and found no gap (an AI check; no
  human has re-derived it). The strategy was also run on small boards: 0 violations in K22's 31,355 sampled roots with at most one
  attacked pawn, over 14 board and file settings (flat 3×4 to 5×6, cyl:4×6, cyl:5×5, cyl:7×6;
  `kings/delegate/out/K22/logs/strategy_check.txt`), and in the referee's 4,534 roots on flat:3×5 (COMPUTED-1 each; not part of the proof).
- The uses in §5.2, P5 and P7 are unaffected. In the starting positions s may have a pawn (7.2 `Pd7`, P5 `Pb5`), but in Q_Z, after
  the reply r, s has no pawn (r captures it: Kxd7, Kxb5), and s̄ has one Z-pawn, so (B1) holds anyway.

**Proposition 2.10 (which punishments are universal). (a) PROVED after repair; (b) PROVED.**
- **(a)** If T = 1 and **H ≥ 5**, then in every chess-legal non-terminal context (every context without a
  passer) no s context pawn can promote in one move, under both the textbook and the e.p.-aware passed test.
  Hence (L2), which counts context pawns only, holds (revised after K7, 2026-10-22). *Proof:* an s-pawn that
  can promote in one move stands on its penultimate rank (the seventh on 8 ranks).
  - No enemy pawn can stand ahead of it, since no pawn stands on the last rank.
  - It cannot be taken en passant. Only a pawn that has just made a double step can be. In a chess position
    the last move before Y was s̄'s, and so was the last move before Q (r, or in the window form the move that led
    to Q), so no pawn of s has just double-stepped. In §5.3 the window Q is Y itself (revised after K7, 2026-10-22).
  - So it is passed under either test, and the context would be terminal. (This step was missing; added after
    the T30 proof audit, `notes/proof_audit2/REPORT.md`, 2026-10-22.) The argument needs chess-legal
    contexts: cylcgt's component model can keep a stale right in a component after its owner has moved
    elsewhere.
  - The king's help does not change this: removing a blocker takes a move of its own.
  - *Z-pawns* (revised after K7, 2026-10-22). (L2) no longer counts them. They are covered by (L1), whatever their
    distance from promotion: a promotion by s is a failure for s̄ in the local game, and Step 4 of Theorem 2.7 uses
    exactly that. (If s can promote at its first turn, (L1) fails. If an s Z-pawn stands on its penultimate rank but s
    is in check at Q and cannot promote at once, (L1) may hold, and then the theorem applies.) In the uses in §5.2–5.4, P3, P5 and
    P7 the s Z-pawn is captured by r. In §5.3 and P8 it survives; it is far from promotion.
  - *The e.p. clause of (L2)* (revised after K7, 2026-10-22). In the window form (b), Q may carry an e.p. right with
    its target off F_Z, and Q° then lets s use it at its first move. It does not change the T = 1 argument: the
    capture lands on the target square, which is on the third rank of s̄'s side and so is never s's last rank, and a
    pawn that promotes at once still has to stand on its penultimate rank.

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

  So, by Theorem 2.7 (PROVED after repair, in P), a group whose punishments satisfy (L1) with T = 1 is decisively
  punished in P in every chess-legal non-terminal context on boards with H ≥ 5, provided (L3) holds. No Z-pawn
  proviso is needed. For T = 1, (L3) asks only that s is not stalemated at its single turn (revised after K7, 2026-10-22).
- **(b)** For every T ≥ 2 there is a non-terminal context with μ_s = 2 (this requires board width ≥ |F_Z| + 4).
  - *Example (White):* W (f, H−2); B (f, H−1) and (f+1, H−1). No pawn is passed. White captures to
    (f+1, H−1) and promotes next move.
  - So (L2) fails there, and a punishment with T ≥ 2 is never certified for all contexts. That statement is PROVED
    (the example above). Whether the freeze itself fails in P is a different statement. It is split below into a
    checked example and a CONJECTURE (revised after K23, 2026-10-27).
  - *Three implementations (K23).* Every number below is exact, in P with real kings, and every one was produced by
    three codes: the kpsolve family (`kpsolve --frozen` and the private `--pmodel` build `kp_p.c`, which share one
    source), the independent solver `kings/delegate/out/K23/scripts/pk2.c` (written by the K23 agent), and the
    referee's solver `kings/delegate/out/K23/verify/ref3.cpp` (written by the K23 referee from `kings/SPEC.md`
    alone). "CHECKED-2 (three implementations agree)" below means that they agree on every position of the
    computation. It is a finite computation, not a proof.
  - *Definition (the zero beside a context, in P).* For a group Z and a context G (Definition 2.1) let Φ(G ⊞ Z) be the
    pair (w, b) of P results, White to move and Black to move, from White's view. Let Ψ(G ⊞ Z) be the same pair in the
    frozen model `--frozen` (a king move loses at once, a promotion wins at once, stalemate draws). Ψ plays the role of
    "the result of G": on the sample below it does not depend on the kings (cyl:7×6, contexts on e–f with at most two
    pawns of each colour on ranks 2–5, 1,770 positions: Z_T replaced by two parked kings `Ka1 ka6` gives the same
    Ψ, 0 differences; CHECKED-2, the referee's solver and the kpsolve family). That this holds for every G is not
    shown here (a CONJECTURE; the reason one expects it is that kings on F_Z are never attacked by context pawns and
    never block them, Lemma 2.2). **Z acts as 0 beside G (in P)** if Φ(G ⊞ Z) = Ψ(G ⊞ Z).
  - **CHECKED-2 (three implementations agree; no hand proof is given): the zero of a frozen group depends on the
    context, in P.** Z_T = `Ka4 Pb3 kc3 pb4` on cyl:7×6 (the trébuchet of P4, Pattern A of §5.1 with r = 3), and two
    locked context pairs, each a single file with no passer and no move, so each has the value 0 and Ψ = (L, W):
    - G1 = {Pe3, pe4}: Φ = (L, W) = Ψ(G1). Z_T acts as 0 beside G1.
    - G2 = {Pe2, pe3}: Φ = (L, L) ≠ (L, W) = Ψ(G2). Black to move wins by the sortie 1...Kd2, the only winning move
      (Kc2, Kb2 and Kd4 lose; Kd3 is illegal, the pawn e2 covers it; Kc4 and Kxb3 are illegal as well). Z_T does not act as 0
      beside G2.
    - The mirror (colours swapped, ranks reversed, files reflected about b) is G2′ = {Pf4, pf5}: Φ = (W, W) ≠ (L, W),
      White to move wins by Kg5; and G1′ = {Pf3, pf4} behaves as G1 (Φ = Ψ = (L, W); the agent's run and `ref3`).
    - Same on the group of §5.1 on cyl:8×8 (`Kh5 Pa4 kb4 pa5`, contexts on d–f, ranks 2–7): {Pe3, pe4} gives (L, W)
      and {Pe2, pe3} gives (L, L); {Pe6, pe7} gives (W, W). The referee's solver also finds {Pd2, pd3} and
      {Pd3, pd4} different with Black to move, and {Pf5, pf6} and {Pf6, pf7} different with White to move. The
      mechanism was analysed for Z_T only, not for this group.
    - *Mechanism for Z_T: a timing tie, decided by one tempo.* 1...Kd2 steps onto the buffer file next to the context.
      If White punishes the sortie with 2.Kxb4, the b-pawn is free but its own king stands in front of it: it needs a
      step aside and three pushes, four moves, with White to move after Black's capture. Black replies 2...Kxe2 in G2
      and 2...Kxe3 in G1, which makes the black context pawn a passer. In G2 that pawn needs three more moves (king
      steps off, e2, e1=Q), in G1 four (king steps off, e3, e2, e1=Q). White moves first, so White's fourth move
      is before Black's fourth but after Black's third. The two race positions confirm it: `Kb4 Pb3 ke2 pe3`, White to
      move, is lost for White; `Kb4 Pb3 ke3 pe4`, White to move, is won (three implementations). In P a promotion ends
      the game, so no queen is ever captured. In G2 every other White reply to 1...Kd2 loses as well (by the
      solvers); in G1 White wins after 1...Kd2, so the sortie is punished there.
    - *The numbers of Theorem 2.7 (COMPUTED-1, the K23 referee's own code, one implementation).* The local game of
      Definition 2.6 after m = 1...Kd2 and r = 2.Kxb4 (Black may pass, White's king confined to the a–c files) has T = 4,
      both for (L1_P) and for (L1) with the queen clause (T = 3 fails). The breadth-first search for μ_s of (L2) gives
      μ_s = 4 in G2 and μ_s = 5 in G1. So (L2) holds in G1 (μ_s = T + 1) and fails in G2 (μ_s = T) by exactly one tempo.
      (L3) was not checked. The sortie is punished only if no context pawn becomes a passer that is at most as slow as
      the punisher.
    - *Distance.* On cyl:8×6 (Z_T on a–c, buffer d and h, context on e–g) the same pair {Pe2, pe3} fails, and moved one
      file away, {Pf2, pf3} and {Pg2, pg3}, it holds (and so do all rank shifts on f and g, except the mirror image
      {Pg4, pg5} of G2). Over all 4,579 contexts on e–g with at most two pawns of each colour on ranks 2–5, 152 have
      Φ ≠ Ψ (47 with a passer, 105 without), and every one has a pawn on e or g, the files next to the buffer. None of
      the 62 non-empty contexts confined to f differs (63 with the empty context), and neither does any of the 81
      single-file contexts on f with up to four pawns of each colour (CHECKED-2: the kpsolve family and `pk2.c`; the
      integrator re-ran the 81 with `ref3`: 0 differ). So in every failing context of this sample a context pawn stands within a step
      of the buffer file the sortie king enters. Whether that is necessary in general is not shown.
    - *The six P4 contexts do not show it in P.* In P all six rows of P4 equal the convention (CHECKED-2, three
      implementations agree), including H*, H*2 and H0 (H0 is G1). The draws that kpsolve finds there in C are
      therefore chess-only effects, not P effects. K23 did not examine their cause.
    - *Scope.* Z_T on cyl:7×6, contexts on e–f with at most two pawns of each colour on ranks 2–5 (885 contexts):
      838 have Φ = Ψ and 47 do not (43 of the 47 have no passer; CHECKED-2, three implementations). In the 23
      passer-free contexts with Ψ = (L, W) that differ, the side to move loses in Ψ and not in P in 26 (context, side to
      move) pairs, and in all 26 a king step to the buffer file (Kd2 or Kd3 for Black; Kg3, Kg4 or Kg5 for White) is
      among its moves that do not lose. With at most three pawns of each colour (3,237 contexts, the same files and
      ranks) 99 differ: 4 with a passer and 95 without; 39 of the passer-free ones have frozen (L, W); in 44 (context,
      side to move) pairs the frozen mover loses and does not lose in P; no position was left unresolved. This
      ≤ 3 count is CHECKED-2 (the K23 agent's `pk2.c` and kpsolve family, re-run by the integrator with the referee's
      generator and solver `ref3`, boards `cyl:7x6`, with and without `--frozen`). Among these positions are cases of
      Corollary 2.7′: `--frozen` reports a win for σ and σ does not win P (G2 with Black to move: `--frozen` is a
      White win, P is a Black win).
  - **CONJECTURE (what remains): the general statement.** For each frozen group with T ≥ 2 there is a context, with
    the defender in zugzwang there, where the freeze fails in P. **A proof is not available as stated, and the
    obstacle is not technical.** T belongs to a certificate, not to a group. A failure needs three things at once for
    one sortie m: (i) the sortie king can reach a buffer square next to a context pawn it can capture (here Kd2, Kg4,
    Kg5), which depends on where the kings stand in Z; (ii) the counter-passer that results is no slower than the
    punisher's *exact* P-win, not the bound T of (L1); (iii) s has no other loss on the way. A converse of Theorem
    2.7 (μ_s ≤ T implies that m is not punished) is false in general (see "No converse"), because s̄ may win faster
    than T or by another reply. So the statement can be settled only group by group, by solving. What is checked
    (CHECKED-2, not a proof): Z_T on cyl:7×6, cyl:8×6 and the group of §5.1 on cyl:8×8, each by an example of a
    context. What is open: groups in which no sortie king can reach the buffer in time (they might be universal zeros
    even with T ≥ 2), and every group other than these two.

**Proposition 2.11 (frozen-king passer certificate). PROVED in P (frozen), as a sufficient condition (revised after
K10, 2026-10-22).** *Caveat.* K10's first draft (a free model) was FALSE: it said that a passed pawn stays passed, and
that fails when an ω pawn captures a β pawn on a neighbouring file. Two AI reviewers found that error and five more
(checks, kings on the path, one move order only, races, en passant). The statement and proof below were rebuilt by
a Sonnet agent (the K10 fixer), which also ran the enumerations listed after the proof. The integrator read the
proof step by step, re-ran every example on a separate kpsolve build, and corrected one example (P1a, which also
fails (H1)). It is one AI proof. In the K10 second round two further Sonnet reviewers, in fresh contexts and without K10's files (they shared a scratch directory with each other for part of the run), read it step by step and found no error; no human and no model outside the Sonnet family has re-derived it. The computation is CHECKED-2: K10v
(opencode beam-free) wrote its own checker without reading K10's files and found 0 violations (see the checks below;
revised after K10v, 2026-10-22).

*Setting.* F is the frozen promotion model, `kpsolve --frozen`: a promotion wins at once for the promoter; a legal
king move ends the play at once in favour of the opponent of its maker; a side with no legal move at all (king
moves count as moves) that is not in check draws, and one in check loses; infinite play is a draw. The board is
a cylinder with W files and H ≥ 5 ranks (files mod W). On a flat board the same proof works with the neighbouring
files that exist (not separately written out); a second-round reviewer ran flat 5×6, 6×6, 7×6 and 6×7 (434,429 certified positions with side to move, 0 violations; see the checks).

*Notation.* Fix a legal position y (kings not adjacent, the side not to move not in check) before any promotion, the side s to move, a side β (the beneficiary) and ω, the
other side. For a pawn q of either colour let ρ(q) be its rank counted from β's side: ρ(q) = rank(q) if β is
White, and ρ(q) = H + 1 − rank(q) if β is Black, whatever the colour of q (revised after the K10 second round). β's pawns advance towards larger ρ, ω's towards smaller ρ; "ahead of p" means larger ρ.
β's start rank is ρ = 2 and ω's is ρ = H − 1. For a pawn p of β put d = H − ρ(p) − [ρ(p) = 2] (the number of β
moves p needs to promote; this is cylcgt's `promote_distance`), and
- e = d if s = ω (ω makes e moves before β's promoting push),
- e = d − 1 if s = β.

*The ω-only game G_ω(y; p).* Delete p. Only ω moves, one move after another. β's other pawns stay where they are
and can be captured. Both kings stay and block squares; nobody captures a king. ω's pawns move as in chess:
push, double step from the start rank over an empty square, capture, and the e.p. capture that y offers (only
as the first move, and only if s = ω). μ_ω(y; p) is the least number of moves after which some ω pawn stands on
its last rank (the promoting move included), or ∞. It is a minimum over **all** ω pawns, passers or not,
with captures allowed. An ω king move ends F at once, so it never occurs in G_ω.

*Hypotheses.*
- **(H1) clear path.** p is a pawn of β that is passed at y in cylcgt's e.p.-aware sense (`passed` with
  `PASSED_RESPECTS_EP = True`: no ω pawn on files f − 1, f, f + 1 with ρ > ρ(p), and p cannot be taken en passant at
  y), and every square of p's file ahead of p, the promotion square included, is empty. So p is the front pawn
  of its file, and **no pawn and no king of either colour** stands on the path.
- **(H2) no check.** No pawn of either colour stands on a file adjacent to the file of β's king.
- **(H3) no stalemate.** ω's king has a neighbouring square t that is not adjacent to β's king, such that no
  pawn of either colour stands on the file of t or on a file adjacent to it. "Not adjacent" means king distance ≥ 2.
- **(H4) no interference.** Every pawn of β other than p that stands on a file adjacent to p's file has
  ρ ≤ ρ(p) + 1.
- **(H5) timing.** μ_ω(y; p) ≥ e + 1.

**Statement.** Under (H1)–(H5), β wins F from (y, s) by pushing p at every turn (the double step first if
ρ(p) = 2).

*Proof.* Write f for p's file and ρ₀ for ρ(p) at y.

*Step 0, three facts about F.*
- (F1) A pawn changes file only by a capture, and lands on the square of the captured piece (an e.p. capture lands
  on the file of the captured pawn). There are no officers before the first promotion, and a king is never
  captured. So a pawn enters a file only by capturing a pawn that stands on it, and a file without pawns never
  gets one.
- (F2) A king move ends F at once. So in any play in which its maker has not lost, no king moves, and both kings
  stand where they stand at y.
- (F3) A promotion ends F with a win for the promoter.

*Step 1, safety of the kings.*
- By (H2) and (F1), no pawn ever stands on a file adjacent to β's king, so no ω pawn ever attacks it. ω's king
  gives no check. So β is never in check, and no push of p is ruled out by king safety.
- By (H3) and (F1), the three files around t never hold a pawn. So t is never occupied, never attacked by a
  β pawn (p included), and is not adjacent to β's king: a move of ω's king to t is always legal, even if ω is
  in check. So ω always has a legal move: it is never stalemated, and F has no draw by stalemate in the play below.

*Step 2, the invariant.* Consider plays in which β follows the strategy Π (push p) and ω moves arbitrarily. Let
ρ_p be the current value of ρ(p) and call the files f − 1, f, f + 1 the *strip*. We show:
- (J_β) at every node with β to move, every ω pawn in the strip has ρ ≤ ρ_p + 1;
- (J_ω) at every node with ω to move, every ω pawn in the strip has ρ ≤ ρ_p, and p cannot be taken en passant;
- (I1) at every node, every square of file f ahead of p is empty.

At y: (J_β) or (J_ω), according to s, is (H1) (passed, aware), and (I1) is (H1). In the following, β's other pawns
and both kings never move, by Π and (F2).
- *β moves.* p goes from ρ_p to ρ′ ∈ {ρ_p + 1, ρ_p + 2}; the squares are empty by (I1), and the move is legal by
  Step 1. By (J_β), the ω pawns in the strip have ρ ≤ ρ_p + 1 ≤ ρ′. A double step (ρ′ = ρ_p + 2) leaves every ω
  pawn in the strip strictly below ρ′, and an e.p. capturer stands on the rank of p, so none exists. A single step
  gives no e.p. right. So (J_ω) holds, and (I1) still holds.
- *ω moves a pawn.* (a) A push or double step lowers ρ. It cannot enter p's square or a square ahead of p on file
  f, because the pawn stands at ρ ≤ ρ_p. (b) A capture lands on the square of a captured β pawn q (or on an e.p.
  target). It captures p never: (J_ω) leaves no ω pawn at ρ_p + 1 next to p, and p is not e.p.-capturable. So
  q ≠ p. If q is on file f, then q stands behind p (nothing of β stands ahead of p by (H1)), and the landing
  rank is below ρ_p. If q is on file f ± 1, then ρ(q) ≤ ρ₀ + 1 ≤ ρ_p + 1 by (H4), and the landing rank is ρ(q). An
  e.p. capture is possible only with the right offered by y when s = ω (Π double-steps only p, and p is not
  capturable): the victim q′ is a β pawn that just double-stepped, the landing square is the skipped square, one
  rank below q′. If q′ is on f ± 1, then ρ(q′) ≤ ρ₀ + 1 by (H4); if on f, it is behind p. Either way the landing
  rank is at most ρ_p + 1. (c) So every ω pawn in the strip after the move has ρ ≤ ρ_p + 1, which is (J_β),
  and nothing lands on file f ahead of p, which is (I1). Captures that land outside the strip change nothing.
  (The tempting one-line argument "ω pawns move away from p's promotion side, so none can ever stand beside its landing
  square" is false: a capture of a β pawn on a neighbouring file puts an ω pawn there. (H4) is what bounds the landing rank.)

*Step 3, consequences.* At every ω turn no ω pawn stands at ρ_p + 1 next to p, and p cannot be taken e.p., so p is
never captured; nothing stands ahead of p on file f ((I1)), so p is never blocked. At every β turn the push is
legal. So Π can be played to the end.

*Step 4, ω's moves are moves of G_ω.* In a play consistent with Π, each ω pawn move is a move of G_ω(y; p): the
squares and the captured pawns are the same, p never takes part (Step 3), β's other pawns stay (Π), the kings
stay (F2), and the only e.p. capture is the one offered at y. (G_ω has fewer obstacles, since p is deleted; this
only enlarges its move set.) So if ω promotes after k of its moves in the real play, then k ≥ μ_ω(y; p). An ω king
move loses at once (F2).

*Step 5, timing.* Under Π, β promotes with its d-th push. Before that push ω has made exactly e moves. By (H5),
e < μ_ω(y; p), so by Step 4 none of those moves promotes, and by Step 1 ω has a legal move each time, so the
play is not a draw. ω's only other moves are king moves, which lose at once. β's d-th push is legal (Step 3)
and promotes, and by (F3) β wins. ∎

**Corollary 2.11a ((V2) at a passer or race terminal of the D-model).** Let y′ be the node reached by a move of M
(N to move), and let cylcgt credit it to b ∈ {M, N}:
- only M has a passed pawn: b = M;
- only N has a passed pawn: b = N;
- both have one (a race, scored by the count rule): b = N if dp(N) ≤ dp(M), else b = M, where dp is
  `promote_distance`.

Then (V2) holds at y′ if (H1)–(H5) hold at (y′, s = N, β = b) for some pawn p of b. Then e = d if b = M (the
opponent moves first) and e = d − 1 if b = N (the beneficiary moves first). This covers the terminal's beneficiary
in both move orders, and a race won by the side to move. The corollary is the proposition at y′. It is
sufficient only (slack example below).

**Corollary 2.11b (the layout of P11).** On cyl:8×6 with `Ka1 ka6` and every pawn on c–g (the a-, b- and h-files
empty), the pawns stay on c–g (F1). Then for either colour as β: (H2) holds (the neighbours of the a-file are b and h);
(H3) holds with t = a5 for ω = Black and t = a2 for ω = White (king distance d(a5, a1) = d(a2, a6) = 4 ≥ 2); and no king stands
on p's file. So at a terminal of such a position only the passed front pawn, (H4) and (H5) have to be checked. A pawn on the a-file breaks (H3): in `Ka1 ka6 Pa3 Pc2 w -` no neighbour of a6 has three pawn-free files (revised after the K10 second round).

**Remark (the count rule is not a (V2) certificate).** In the count rule's test, β wins iff dp(ω) ≥ e + 1. This is
(H5) with μ_ω replaced by ω's fastest **passer** distance dp(ω), and dp(ω) ≥ μ_ω whenever no king stands on the
path of that passer (always so in P11's layout). The two agree only if no non-passer of ω is as fast. Without a passer of ω the count rule credits β whatever ω's pawns do, and it sees neither captures
(H4) nor kings (H1, H2) nor stalemate (H3).

**What the hypotheses do (every example is a `kpsolve --frozen --cap 1` result; the integrator re-ran each on a
separate build).** A pair such as (L, L) is kpsolve's printed line `A B` for the side to move given: the two cap
bounds, equal in `--frozen`, from White's point of view. It is not the pair (r_w, r_b) of §1.1. Unless a
board is named, it is cyl:8×6; β is White (p = Pc4 or Pc2) unless said otherwise.
- *(H5), both move orders.* ω to move (e = d = 2): `Ka1 ka6 Pc4 pe3 b -` (μ = 2) gives (L, L), so ω wins the tie;
  `Ka1 ka6 Pc4 pe4 b -` (μ = 3) gives (W, W). β to move (e = d − 1): `Ka1 ka6 Pc4 pe3 w -` (e = 1, μ = 2) gives (W, W);
  `Ka1 ka6 Pc3 pe3 w -` (d = 3, e = 2, μ = 2) gives (L, L). With Black as β: `Ka1 ka6 pc3 Pe4 w -` (ω to move,
  μ = 2) gives (W, W) and `Ka1 ka6 pc3 Pe3 w -` (μ = 3) gives (L, L).
- *(H5), non-passers count.* `Ka1 ka6 Pc2 Pd4 pd3 b -`: p = Pd4 is a passer (d = 2) and the only Black pawn is not
  one, but d3xc2 and c1=Q take ω two moves. (L, L), although cylcgt credits White. This is the position
  after c3xd4 in `Ka1 ka6 Pc2 Pc3 pd3 pd4 w -`, whose D-result is a White win and whose `--frozen` result is (L, L):
  the D-result and `--frozen` differ at this root. Race: `Ka1 ka6 Pc4 Pd2 pe3 pf4 b -` is (L, L); the count rule
  credits White (dp = 2 against dp(Black) = 3 for the passer f4), but Black's non-passer e3 takes d2 and promotes in two.
- *(H5) is not necessary.* cyl:7×6 `Ka1 ka6 Pc2 Pd3 Pf2 pe4 b -` has μ = e = 3 and is (W, W): the proposition says
  nothing there.
- *(H4), and the threshold ρ(p) + 1 is exact.* `Ka1 ka6 Pc2 Pd4 Pe2 pe5 b -` is (L, L): p = c2, Pd4 stands at
  ρ = ρ(p) + 2, and e5xd4 followed by d3, d2, d1 takes ω four moves (μ = 4 ≥ e + 1 = 4, so (H5) holds); the
  pawn on d4 then attacks c3 and the double step is met by dxc3 e.p. `Ka1 ka6 Pc2 Pd3 Pe2 pe5 b -`
  (Pd3 at ρ(p) + 1) is (W, W). The failure arises inside the D-model: `Ka1 ka6 Pc2 Pe2 Pe3 pd4 pe4 pe5 w -` has D-result
  "White wins" (e3xd4 makes c2 a passer, a terminal credited to White) and is (L, L) in F.
  With the bound ρ(p) + 2 in place of ρ(p) + 1, the end-to-end run below refutes 8 certified wins (9,852 roots, cyl:6×6); so does
  dropping (H4) (16 of 80 positions with side to move on cyl:6×6).
- *(H2).* `Ke2 ka6 Pc4 pf4 b -` is (L, L) (f4-f3+ forces a king move or no reply), `Ka1 ka6 Pc4 pf4 b -` is (W, W);
  in both p = c4, d = 2 and μ = 3 = e + 1.
- *(H1), kings.* `Ka1 kc5 Pc4 pf4 b -`, `Kc5 ka6 Pc4 pf4 b -`, `Kc6 ka6 Pc4 pf4 b -` and `Ka1 kc6 Pc4 pf4 b -`
  (a king of either colour on the path, or on the promotion square) are all (L, L).
- *(H1), e.p.* `Ka1 ka6 Pe4 pd4 b e3` (e4 has just been played, e.p. right on e3) is (L, L); the same position
  without the right, `... b -`, is (W, W). The textbook passed test calls e4 passed at once, the aware test does not.
  Another: `Ka1 ka6 Pc3 Pd4 Pf2 pc4 b d3` is (L, L) and `... b -` is (W, W): the right is the only reason that
  μ = 3 ≤ e = 3 (the e.p. capture is the first move of G_ω).
- *(H3).* `Ke1 ka6 Pa4 Pc5 Pg5 pa5 b -` is (D, D): p = c5 (d = 1), (H1), (H2), (H4) and (H5) hold (μ = ∞: a5 is
  blocked and has nothing to capture), but Black has no legal move: a4 covers b5 and h5 across the seam, c5
  covers b6 and g5 covers h6. Without Pg5 the king can step to h6 (and lose), and the position is (W, W). Also
  flat:7×6 `Kb1 ka6 Pa4 Pc2 Pc5 pa5 b -` is (D, D); there the static (H2) fails, but no check can occur.
  (P1a of §5.4, cyl:7×6 `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5 b -`, is (D, D) too, but it is not an example for (H3):
  the black king stands on c6, the promotion square of c5, so (H1) fails as well.)

**Checks (K10 fixer, 2026-10-22; kpsolve built privately from `kings/kpsolve.c`; data, not proof).** The
scripts (`cert.py` decides (H1)–(H5) with its own move generator, and only `passed` and `promote_distance` are cylcgt's;
`direct.py`, `direct2.py`, `e2e.py`) and their logs are copied to `kings/delegate/out/K10/scripts/`; their paths point
at the old scratchpad.
- *Proposition against `--frozen`, kings parked* (`Ka1` and a Black king on the top rank of the a-file, the b-file and the
  last file empty, pawns on files c to W − 2, ≤ 3 per side except where noted; both colours as β, both sides to move; the
  unit is a position with its side to move, certified for one β by some p): cyl:6×6 74,410
  positions, cyl:8×6 (≤ 2 per side) 64,954, cyl:6×7 306,020, cyl:6×5 12,160, cyl:7×6 496,848: **0 violations in
  954,392**. With (H4) dropped: 16 of 80 (6×6), 56 of 456 (6×7), 32 of 368 (7×6) violate.
- *Independent check (K10v, opencode beam-free, own code; `kings/delegate/out/K10v/`; revised after K10v,
  2026-10-22).* An instance is a position, a side to move, a beneficiary β and a pawn p. Its checker decides (H1)–(H5) with its own move generator and a search for μ_ω, and agrees with
  cylcgt's `passed` on 2,000 random positions. Certified instances, all of them β wins in `--frozen`: cyl:6×6 parked,
  ≤ 3 a side, 91,074 (74,410 positions with side to move, the same count as above); cyl:7×6 parked, ≤ 2 a side, 29,140,
  and 20,000 random positions with 3 a side, 23,363; cyl:8×6 with random kings, 2,751; cyl:6×6 with an e.p. right, 5,716
  (2,356 of them with another β pawn capturable e.p. and ω to move): **0 violations**. Dropping (H4) gives 80, 24 and
  23 violations on the parked boards; dropping (H2) or (H3) gives 3,277 and 2,086 with random kings.
- *Kings anywhere* (random placements, so that (H2), (H3) and the king clause of (H1) are tested as stated): cyl:7×6,
  cyl:8×6 and cyl:6×7, 20,000 positions with side to move each, ≤ 3 pawns a side: 0 violations in 60,000. With one hypothesis dropped,
  the violations are: (H2) 1,744, 1,853 and 1,394 of 20,000; (H3) 8 of 19,033, 8 of 16,599 and 5 of 20,000; the king
  clause of (H1) 563 of 1,315, 469 of 1,020 and 556 of 1,783; (H4) 0 of 4 and 0 of 9 (too few) and 2 of 11.
- *Chain D → P, end to end* (kings parked; no passer at the root; both sides to move): cyl:6×6 files c–e, ≤ 3 pawns a
  side, 9,852 roots; cyl:7×6 files c–f, ≤ 3 a side, 40,204 roots; cyl:8×6 ≤ 2 a side, 5,384 roots; cyl:6×6 ≤ 2, 1,432
  roots; 56,872 in all. The conservative D-game in which a side's own terminals, and the opponent's moves into
  terminals credited to it, must be certified by Corollary 2.11a gives a win only if `--frozen` agrees: 48,000
  certified wins, 0 violations. When **every** terminal of the D-game is certified (26,014 roots), `--frozen` equals
  the D-result (o(W)): 0 violations. Without (H4) in the certificate: 8 violations (cyl:6×6). `--frozen` differs from
  o(W) at 3,194 of the 56,872 roots, all of them with some uncertified terminal.
- *Second round (two Sonnet reviewers in fresh contexts, own code, without reading K10's or K10v's files;
  scripts and result JSONs in `kings/delegate/out/K10r2/`; 2026-10-22).* An instance is (position, side to move, β, p).
  - Exhaustive with kings parked on the a-file (all legal a-file king pairs): cyl:5×6 files c–d ≤ 3 a side, cyl:6×6
    c–e ≤ 3, cyl:7×6 c–f ≤ 2, cyl:8×6 c–g ≤ 2, cyl:6×7 c–e ≤ 2. Exhaustive with free kings: cyl:5×6 c–d ≤ 3, cyl:4×6.
    Random scenes built for the tight cases (cyl:5×6 to 8×6, 6×7, 6×5) and uniform random positions (cyl:5×6 to 8×6,
    6×7). On these cylinders, in all,
    5,730,596 certified positions with side to move (6,783,482 instances): **0 violations**, and no position is
    certified for both colours. Flat 5×6, 6×6, 7×6 and 6×7: 434,429 positions (516,823 instances), 0 violations.
  - The tight cases occur among the cylinder instances: (H5) with μ = e + 1 (3,306,911 instances), another β pawn at ρ(p) + 1 on an
    adjacent file (242,044), an ω pawn entering the strip by a capture (307,127), an ω e.p. right against another
    β pawn (333,474), ω in check at y (48,190), races (4,642,279).
  - Controls: on cyl:6×6 parked (all legal a-file king pairs, so a larger sample than the 16 of 80 above), dropping (H4) gives 24 of 940 failures, and the same 24 fail with the bound
    ρ(p) + 2 (`Ka1 ka6 Pe2 pc5 pd3 pe5 w -`); (H5) weakened to μ ≥ e gives 6,891 of 7,855; dropping the e.p. clause
    of (H1) gives 272 of 692. With random kings, dropping (H2) or the king clause of (H1) gives hundreds of failures
    per board, dropping (H3) 1 to 12.
  - Reproduced exactly: every parked count above that was re-run (74,410; 64,954; 306,020; 12,160;
    496,848; K10v's 91,074 and 29,140), the end-to-end figures (48,000 conservative wins, 26,014 fully certified
    roots, 3,194 differences, 8 violations without (H4)), and every example above. On cyl:8×6 with pawns on c–g
    (≤ 2 a side), (H2), (H3) and the king clause of (H1) held in all 371,250 instances (Corollary 2.11b), and
    dp(ω) ≥ μ_ω held in all 378,407 instances with no king on the fastest passer's path (the count-rule remark).
  - Both reviewers read Steps 0–5 and Corollaries 2.11a and 2.11b against `cylcgt/pawns.py` and `kings/kpsolve.c`
    and found no error. Their findings were the root case of P11, the legality of y, and the wording fixed here.

**Remark 2.11 (the certificate is not special to kings; real kings).** The same (V2) question arises for passer
terminals. The certificate of Definition 2.6 (king moves) does not apply to a passer as written (Q_Z deletes the
passer, r is not a king capture, the owner's king may leave F_Z, the component's own pawns are unaddressed).
Proposition 2.11 supplies the missing certificate for passer and race terminals **in the frozen model**, and
Corollary 2.11a states it for the D-model.
- **Proved about real kings: nothing.** Every step above uses (F2). The hypotheses are not enough with real kings:
  `Ka1 ka6 Pc2 w -` (cyl:8×6) satisfies (H1)–(H5) with μ = ∞ and is (W, W) in F, but P with real kings (a private
  `--pmodel` build, `kings/delegate/out/K7/scripts/draft/kp_p.c`) and chess (kpsolve exact) both give (D, D).
- **Corollary 2.8** is the real-king statement for one pawn: a single-pawn local game with a king beyond reach.
- **CONJECTURE (real-king square rule, label kept).** Let β's king be sheltered as in (H2) and the pawn data satisfy
  (H1), (H4), and (H5) with ω's king allowed to move and to capture β's other pawns in G_ω. Let q₀, …, q_d be the
  squares p occupies before its first push and after each push, and n_j = j if s = ω, j − 1 if s = β, the number of
  ω moves before the j-th push. If d(k_ω, q_j) ≥ n_j + 2 for every j (for j = 0 only if s = ω), then β wins P with
  real kings. This follows from d(k_ω, q_d) ≥ d + 2 (s = ω) or d + 1 (s = β) by the triangle inequality. The
  sketch is the proof above with Step 1 replaced by the rule of the square (no capture and no block), but ω could
  steer into a stalemate or a draw by king-and-pawn play, which the sketch does not exclude. Scratch evidence
  only: β = White, `Ka1`, ≤ 2 + 2 pawns, `--pmodel`: cyl:6×6 30,847 legal instances and cyl:7×6 158,840, 0
  violations. The chess form needs (A_Q) at the resulting position (§1.2) and is not claimed.
- P11 in §6 relies on Proposition 2.11 in the sense given there (revised after K10, 2026-10-22).

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
Z-moves. (Two shuttles, one for each king: Proposition 3.2′ below.)

*Proof.*
- The relation {(z, ω), (z′, ω)} is a bisimulation. In each of z and z′, White can move to the other, and
  Black's Z-options are all suicides. So the 2-cycle has the same results as the 1-cycle ω.
- Black's suicides can be deleted (Lemma 1.7). This is valid in chess only under (V1b): Black must always
  have the legal suicide.
- Any further White Z-moves only help White (Lemma 1.6). ∎

**Chess bridge** (PROVED after repair, by the sharp form of Theorem 1.14 with D = G ⊞ on_D; revised after K9,
2026-10-22: the earlier citation, the proof of Theorem 1.14(i), assumes that σ never moves in Z, which White's
shuttle violates).
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
- **With shuttles on both sides (PROVED in the D-model by Proposition 3.2′; revised after K14 and its referee, 2026-10-27):** for a
  component with four combined king states, each side's shuttle an option and every other option a suicide, all tempo
  content disappears. A position in which neither side can force a decisive event against a passing opponent is a
  draw even where the convention predicts a clear winner, and a side wins iff it can (Theorem 3.4(a), through
  Proposition 3.2′). The chess bridge is Theorem 3.2‴. It needs, per group and context, that every non-shuttle Z-move
  is decisively punished; a win needs this only for the loser and only in the two states in which the winner's king
  stands still. The 7.3 group is **not** of this type: f7–f8=Q is a White Z-move that is no suicide (§5.3). A group of this type
  exists in P on the flat 7×6 board: Z_B of §5.7 has every non-shuttle move losing at once at all 8 roots (CHECKED-2),
  and beside every context tested its P-result equals r(G ⊞ dud_D) (COMPUTED-1; 225 of 885 contexts untested);
  CONJECTURE that this holds in every context. Whether Z_B is exactly two-shuttle in chess is undecided (cap 1 gives
  the bounds (W, L)); open: chess (cap 2), the cylinder, other boards (§8, item 2). Z_A (§5.7) has one White break.

**Proposition 3.2′ (two shuttling kings are a dud). PROVED (new, K14, 2026-10-27; revised after the K14 referee,
2026-10-27: the D-model part was re-checked by one referee (same model family) and by two brute-force implementations,
on short and loopy G).**

*Two-shuttle component.* Let Z be a D-game with four distinct positions (a, b), a ∈ {z, z′}, b ∈ {w, w′}. Write ā for
the other of z, z′ and b̄ for the other of w, w′. In chess z, z′ and w, w′ are the two shuttle squares of the White and
the Black king, and the four positions are the four combined king states. In each of the four positions:
- **(T1)** (ā, b) is a Left option (White's shuttle);
- **(T2)** (a, b̄) is a Right option (Black's shuttle);
- **(T3)** every other Left option is ⊖ (a suicide);
- **(T4)** every other Right option is ⊕ (a suicide).

Z may have further positions. Let G be any D-game (short or not) and x a position of G.
- **(a) Equality.** Under (T1)–(T4), for all four states (a, b) and both sides to move, r(G ⊞ Z) at (x, (a, b)) equals
  r(G ⊞ dud_D) at (x, ω). For short G the value is given by Theorem 3.4(a): a side wins iff it can force a decisive
  event against an opponent who may pass at any time, and otherwise the game is drawn. There is no zugzwang
  (Λ_R ⇒ Λ_L), and a G without terminals is a draw.
- **(b) Further Z-moves.** Under (T1), (T2), (T4) (White may have further Z-moves, of any kind, even to new positions),
  r(G ⊞ Z) ≥ r(G ⊞ dud_D) in the order L < D < W. Under (T1), (T2), (T3), r(G ⊞ Z) ≤ r(G ⊞ dud_D). If both sides have
  further moves there is no comparison in general. The inequalities can be strict (a further White option ⊕ at
  (z, w) makes G = 0 a White win, against D for dud_D).
- **(c) Half-slice.** Suppose only (T2) and (T4) hold, and only at (z, w) and (z, w′), and everything else in Z is
  arbitrary. If r(G ⊞ dud_D) = W at (x, ω) for a side to move s, then r(G ⊞ Z) = W at (x, (z, w)) and at (x, (z, w′))
  for the same s. Mirror: (T1), (T3) at (z, w) and (z′, w) transfer a Black win. So *a win needs only the half of the
  four states in which the winner's king stands still*; the draws, and the exact equality (a), need all four.
- **(d) Each shuttle arrow is needed.** Take G = 0 (one position, no options), where r(G ⊞ dud_D) = (D, D).
  - *Opposition.* Delete the diagonal state (z′, w′) (the kings would touch). Then (z′, w) has no Black shuttle and
    (z, w′) has no White shuttle; their only options are suicides. At (z, w) the pair is (W, L): White to move goes to
    (z′, w) and Black must suicide, Black to move goes to (z, w′) and White must suicide. The first player wins.
  - *One arrow.* Delete Black's shuttle at (z′, w) only: the pair at (z, w) is (W, D).
  - *Every arrow.* Deleting any one of the eight shuttle arrows from an otherwise exact Z changes the result in a
    positive fraction of random instances, and at G = 0 it changes the result at all four states (the referee's table of
    all eight deletions; COMPUTED-1).

*Proof.* Two lemmas, then the parts.

**Lemma A (p-morphism).** Let A, B be D-games and φ a map from the positions of A to those of B (identity on terminals)
such that, for every position u of A and each player s, (i) φ maps every s-option of u to an s-option of φ(u), and
(ii) every s-option of φ(u) is φ of some s-option of u. Then r_A(u, s) = r_B(φ(u), s) for all u, s. A and B may be loopy.
*Proof.* Let U_n^σ be the stage sets of Definition 1.2 (U_0 = ∅; (u, σ) enters at stage n+1 if some σ-option is a
σ-terminal or a position t with (t, σ̄) in U_n^σ; (u, σ̄) enters if every option is a σ-terminal or a t with (t, σ) in
U_n^σ, a position without options entering at stage 1). By induction on n, (u, s) is in U_n^σ(A) iff (φ(u), s) is in
U_n^σ(B). For s = σ, an option of u that is good at stage n maps by (i) to a good option of φ(u), and a good option
of φ(u) is φ of an option of u by (ii), which is good by induction. For s = σ̄, every option of φ(u) is φ of an option
of u by (ii), and every option t of u maps to an option of φ(u) by (i). The union over n is the least fixed point. ∎

**Lemma B (the winner of G ⊞ dud_D never passes).** Let (x, ω, σ) be in W^σ of G ⊞ dud_D, entering at stage n. Then
some option that makes it enter at stage n is a G-move (a σ-terminal of G or a position (x′, ω) with σ̄ to move and
stage ≤ n − 1). *Proof.* If the only such option were the pass, to (x, ω, σ̄) at stage m ≤ n − 1, then every option of
(x, ω, σ̄), the pass back included, has stage ≤ m − 1, so (x, ω, σ) would enter at stage ≤ m < n. ∎
This is the content of the proof of Theorem 3.4(a), "Left's winning moves are always G-moves".

*(a)* Let A = G ⊞ Z and A⁰ = G ⊞ Z⁰, where Z⁰ keeps only the four shuttle options at the four states.
- The stage sets of A and A⁰ coincide. A deleted option is a Left option ⊖ or a Right option ⊕. For the player to move
  it never makes a position enter (it is a terminal for the opponent). For the opponent it is a terminal that is always
  fine, so a position all of whose remaining options are fine, or that has none, enters at the same stage in A⁰ and A.
  (This is Lemma 1.7; its proof does not use shortness.)
- φ(x′, (a, b)) = (x′, ω) maps A⁰ onto G ⊞ dud_D. The Left options of (x′, (a, b)) are the terminals of G, the
  positions (x′^L, (a, b)) and (x′, (ā, b)); their images are the Left options of (x′, ω): the terminals of G, the
  positions (x′^L, ω) and (x′, ω), the pass. So (i) and (ii) hold for Left, and for Right with (x′, (a, b̄)). By
  Lemma A the results agree. ∎

*(b)* Delete White's further options (they can be added back as unreachable positions of the smaller game): (a) applies,
and by option monotonicity (Lemma 1.6) the larger game is at least as good for White, since Black's options are
unchanged. The second inequality is its mirror.

*(c)* Take σ = White. By induction on n, (x′, ω, s) in U_n^White(G ⊞ dud_D) implies (x′, (z, b), s) in U_n^White(G ⊞ Z)
for both b. For s = White, Lemma B gives a G-move making it enter, and the same move exists in G ⊞ Z. For s = Black,
every option of (x′, ω, Black) is good: a G-option, or the pass. At (x′, (z, b)) Black has the same G-options, the
shuttle to (x′, (z, b̄)) by (T2) (it corresponds to the pass), and otherwise only ⊕ options by (T4). All are good. ∎

*(Remark on e.p.; revised after the K14 referee, 2026-10-27.)* The sum of Definition 1.3 leaves G alone under a Z-move,
and in chess an e.p. right expires under a king move. Model the flag as a coordinate of G that every Z-move resets, and
the pass of dud_D likewise. Lemma A goes through unchanged (φ forgets only the Z-state, and both games reset the flag at
corresponding moves). Lemma B needs one more line. The pass from (x, f, ω, σ) leads to (x, none, ω, σ̄), and the pass
back leads to the flag-free state (x, none, ω, σ), which is not (x, f, ω, σ) when the flag f is set. The flag belongs
to the side to move, so (x, f, σ) has all the options of (x, none, σ) and possibly an e.p. capture more. By option
monotonicity (Lemma 1.6) its stage is at most the stage of (x, none, σ). So (x, f, σ) enters at stage ≤ m < n: the same
contradiction. The conclusion of Lemma B also holds on all 4,579 pawn contexts of the checks below (155,400 winning
nodes, 0 violations; the referee's `vpawn.py`; COMPUTED-1). The chess statements below use this reading.

**Remark 3.2′a (what it says about the conjecture).** A two-shuttle component realises dud_D, so the "shuttles on both
sides" bullet above is PROVED in the D-model for every component that satisfies (T1)–(T4). Whether a chess king group
does is a separate question, answered by the hypotheses of Theorem 3.2‴ below and, for a concrete group, by a search
(§5.7: Z_B in P).

**Lemma 3.2″ (four-state geometry; PROVED).** Let z ≠ z′ and w ≠ w′ be empty squares of F_Z, z, z′ adjacent and w, w′
adjacent, such that (K1) no Black Z-pawn attacks z or z′ and no White Z-pawn attacks w or w′, and (K2) the king distance
d(a, b) ≥ 2 for all four (a, b) (the kings never touch). Then, in every context (files at distance ≥ 2 from F_Z), with
the Z-pawns unmoved and the kings on {z, z′} and {w, w′}: neither king is in check, both shuttle moves are legal
(whatever the other king's square), and each side has a legal move, so nobody is stalemated.
*Proof.* A king is attacked only by an enemy pawn or the enemy king. By Lemma 2.2 no context pawn attacks a square of
F_Z and no pawn stands on a buffer file; the Z-pawns do not attack the four squares by (K1), and the kings do not attack
each other by (K2). So there is no check, and a shuttle move is legal: its target is empty, not attacked, and not
adjacent to the enemy king. Each side has its shuttle as a legal move. ∎

**Theorem 3.2‴ (chess bridge for two shuttles; PROVED in P, conditional on the stated hypotheses; the chess statement adds
(A_Q)(X) as always).** Let X be a K+P position
with a king group Z satisfying (K1), (K2), the kings on {z, z′} and {w, w′}, and a context with D-model G (the pawn-only
game of Definition 1.5, with the e.p. flag as in the Remark). Let D = G ⊞ dud_D, with π sending a chess position to
(x, ω) and keeping the side to move. A *regular* position is one reachable from X by D-moves (matching context moves and
the two shuttles). Assume, at every regular position:
- **(V1a-ctx)** the legal context moves of the side to move are exactly G's options for that side, with the same
  resulting positions (e.p. through condition (E)); the shuttle is the pass;
- **(V2-ctx)** every decisive event of G leads to a P-win for its beneficiary (automatic for a pawn-only G scored by
  promotions);
and write **(Pun_s)** for: *every legal move of s that is neither a context move nor s's shuttle (a king move off the
shuttle, a Z-pawn move or capture) is decisively punished (Definition 2.5): the position after it is a P-win for s̄.*
- **(a) Win transfer.** Suppose r_D(x, ω, s) = W. Let Σ be a rank-lowering White strategy in D (by Lemma B it never
  passes) and N the set of chess positions arising when White plays Σ as chess moves and Black plays any legal D-move.
  If (Pun_Black) holds at the nodes of N with Black to move, then White wins X in P. White's king stays on its square, so
  only the two states (a, w), (a, w′) occur; White's shuttle and the square z′ are not used. The mirror statement for a
  Black win needs (Pun_White) at the nodes of N with White to move.
- **(b) Exactness.** If (Pun_White) and (Pun_Black) hold at all regular positions, the P-result of every regular
  position equals r_D(π(y)), draws included. In particular, if G has no decisive event, X is a draw in P.

*Proof.* (a) By the sharp form of Theorem 1.14 it is enough to exhibit a White-certified set; take N.
- (S1): at a White node of N, Σ prescribes a G-move or a ⊕. By (V1a-ctx) the move is legal and leads to the prescribed
  D-position; a promotion wins in P by (V2-ctx). The rank is lowered.
- (S2): at a Black node of N every legal move is one of: a context move, a D-move by (V1a-ctx) to a position of N (a
  decisive event of G for White is closing by (V2-ctx); a promotion by Black would be a ⊖ option of a Black node of
  W^White, and there is none); Black's shuttle, a D-move (legal by Lemma 3.2″) whose rank is lower because the pass is
  an option of a Black node of W^White; any other move, closing by (Pun_Black).
- (S3): Black's shuttle is a legal move, so Black is not stalemated (Lemma 3.2″).
The sharp form gives a P-win. ∎(a)

(b) *D-win ⇒ P-win:* by (a) at every regular position, as (Pun) holds everywhere. *P-win ⇒ D-win:* by induction on the
stage of the P-win, a regular position y that is a P-win for σ has π(y) in W^σ. Suppose π(y) = (x, ω) with side s and
(x, ω, s) not in W^σ.
- s = σ: σ has a legal move that promotes or leads to a P-win of smaller stage. A promotion is a σ-terminal option of D
  by (V1a-ctx), which would put (x, ω, σ) in W^σ. A context move or a shuttle is a D-move to a regular y′ of smaller
  stage, and by induction π(y′) is in W^σ, again a contradiction. Any other move is decisively punished (Pun_σ), a P-win
  for σ̄, not for σ.
- s = σ̄: being a P-win, y has every legal move of σ̄ leading to a P-win for σ, and σ̄ is not stalemated. As (x, ω, σ̄)
  is not in W^σ and σ̄ has the pass, some option of it is neither a σ-terminal nor in W^σ. By (V1a-ctx) and Lemma 3.2″ it
  is realised by a legal move of σ̄ (a promotion, or a context or shuttle move to a regular y′ with π(y′) the option).
  By induction that move is not a P-win for σ. Contradiction.
So the P-win sets of both sides are π^{-1}(W^σ). ∎

**Which hypotheses hold (revised after K14).**
- (K1), (K2) are a finite test on Z alone, and by Lemma 3.2″ they give legality of both shuttles, no check and no
  stalemate in **every** context. (V1b) is therefore no hypothesis here: it is automatic, unlike in the one-sided bridge.
- A win needs no hypothesis on the winner's shuttle (Lemma B): only (Pun) for the loser, in the two states in which the
  winner's king stands still. Draws and the exact statement need (Pun) for both sides in all four states.
- (V1a-ctx), (V2-ctx) are per-context facts, as in the one-sided bridge.
- (Pun) is a per-group, per-context fact. It does not follow from the geometry of Z, and it fails when a counter-chance
  is faster than the punishment (Proposition 2.10(b)). It is the only gap of the bridge (the chess statement needs (A_Q)(X) as
  always, and (Pun) is stated for P): no theorem here gives it for a concrete group in all contexts. Theorem 2.7 and Proposition 2.10(a) give it in P for punishments of depth
  T = 1 under their side conditions.

**Checks of Proposition 3.2′ and Theorem 3.2‴ (K14 and its referee; data, not proofs; revised after the K14 referee,
2026-10-27).**
- *D-model, brute force, K14* (`kings/delegate/out/K14/scripts/prop_check.py 400`): 400 random short D-games G (3 to 6
  positions, random options including ⊕, ⊖), each with random components Z of the kinds "exact (T1)–(T4) with extra
  suicides", "(T1), (T2), (T4) plus random further White options", the mirror, and (c)'s half-slice, solved by least fixed
  point on the explicit sum. (a): 44,208 of 44,208 instances agree. (b): 44,208 of 44,208 for each of the two
  inequalities. (c): 4,980 of 4,980. COMPUTED-1: the solver is new and one implementation; the statements are PROVED
  above.
- *D-model, brute force, the referee's own implementation* (`kings/delegate/out/K14/verify/vdmodel.py 400 777`,
  counter-based retrograde on the explicit sum): 400 random games of 2 to 6 positions, half of them loopy, 0 to 2 extra
  Z-positions. (a): 38,544 of 38,544 short and 37,200 of 37,200 loopy. (b): 75,744 of 75,744 for each inequality. (c):
  6,492 of 6,492 (White version) and 6,060 of 6,060 (Black version). 0 violations. COMPUTED-1 for the data; the
  statements are PROVED above, for loopy G as well.
- *Predictions for pawn-only contexts:* the least-fixed-point solver `scripts/dmodel.py`, the closed recursion of
  Theorem 3.4(a) (`scripts/closed_form.py`, a pass resets the e.p. flag) and the referee's third implementation
  (`verify/vpawn.py`, own pawn generator and own retrograde) agree on all 4,579 contexts of ≤ 2 + 2 pawns on files e–g
  of the flat 7×6 board: CHECKED-2. All three solve Theorem 3.4(a) on one pawn-game model, so this checks Theorem 3.4(a)
  with e.p. resets, not chess.
- *Chess, concrete groups:* §5.7. Counts are root instances of Theorem 3.2‴ under the referee's convention: (Pun) for the
  loser holds on all regular positions reachable from the root and the D-result is W or L, for (a); both (Pun) hold, for
  (b). Z_A: (a) 208 instances, (b) 48 instances, 0 failures. Z_B: (a) 160 instances, (b) 56 instances, 0 failures.
  COMPUTED-1 in P.

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
  WP a4, which Black's king then captures on a4, giving Black a passer. BK's five legal moves are Ka3, Kb3,
  Kc3, Kc4 and Kc5 (Kb5 is illegal: the pawn a4 attacks b5); each of them abandons BP a5, which White's king
  then captures on a5, giving White a passer. (They are the mirror images of the White list: g4 ↔ c5, g5 ↔ c4,
  g6 ↔ c3, h6 ↔ b3, a6 ↔ a3.) So every king move in the group is decisively punished, and the group is frozen.
  (Corrected after K19, 2026-10-27: the earlier list had Kb5 in place of Kb3, and a zugzwang argument for a move
  that is not legal. This was a transcription slip in this section: `notes/diagram_audit.md` §C.3 and the scratch
  list of Appendix A both give the correct list a3, b3, c3, c4, c5. The conclusion stands. K19's move generator,
  checked against `kpsolve --moves`, gives the list above, and so does the referee's.)
- **Certificate.**
  - Corollary 2.8 fails for every sortie. After ...Kxa4 the punisher's king stands on its own pawn's path,
    so it needs a king step plus 4 pushes, and the defending king is within distance 5 of a1.
  - (L1) holds for all five White sorties with T ≤ 7 (5 to 7, depending on the sortie and the budget), for
    every pass budget **k = 0, 1, …, 8 and k = ∞**, with the punisher's king confined to {h, a, b}: **CHECKED-2**
    (revised after K19, 2026-10-27: for k ≤ 4 and k = ∞ the scratch run and K19's code agree. The budgets k = 5, 6, 8 were
    never run before: K19's code and the referee's own code (K19/VERIFY.md) agree that they equal k = ∞. Every
    k ≥ 7 equals k = ∞ for a reason: the window contains at most T ≤ 7 moves of s, so no budget is used up.)
    (L3) holds in the bare group for these five sorties and for the five Black ones: **CHECKED-2** (K19's code and the
    referee's own code; Appendix A).
    - These runs used the local game as it was before K7 (finite budgets, optional confinement). K7 re-ran the local
      game of Definition 2.6 (k = ∞, king confined to {h, a, b}, a mate of s a win) on the five sorties, after the
      reply Kxa4, with a second scratch implementation. (L1_P), which has no queen clause, holds with
      T = 6, 6, 5, 6, 6 for Kg4, Kg5, Kg6, Kh6, Ka6. (L1), with the queen clause, holds with T = 6, 6, 6, 7, 7.
      A reviewer's independent implementation gave the same two lists. So in P the freeze needs μ_s ≥ 7 at the
      zugzwang nodes (Theorem 2.7 holds with (L1_P)), and μ_s ≥ 8 with the queen clause, which is the value used
      above. K19's code reproduces both lists, so this is now CHECKED-2 (revised after K19, 2026-10-27). The K24 agent's local-game code and the K24 referee's (each written from Definition 2.6) give the same lists and the same s-node counts, and K24 ran the five Black sorties directly: T = 7, 7, 6, 6, 6 for Ka3, Kb3, Kc3, Kc4, Kc5 with the queen clause and 6, 6, 5, 6, 6 without, the mirror of the White lists (revised after K24, 2026-10-27). The strict form (L3_F) fails in every case, because s may walk its king off F_Z (for example Kg4–Kf4), after which no king step reaches F_Z; the claim above rests on (L3) of Definition 2.6, which holds in the bare group (0 stalemates of s on any line on which s̄ plays only winning moves, in K24's code and the referee's).
  - With (L1), Theorem 2.7 makes the freeze valid in P for every context in which (L2) holds with
    μ ≥ 8 at the zugzwang nodes, and (L3) holds.
  - On 8 ranks a single free White pawn on rank 2 has μ = 5. So the certificate covers only locked or slow
    contexts. Next to fast pawns the zero has to be checked case by case (Proposition 2.10b). For this group on
    cyl:8×8 it fails beside {Pe2, pe3} in P: (L, L) instead of (L, W), CHECKED-2 (three implementations agree; P13;
    revised after K23, 2026-10-27).
- **Prediction.** The bare 5.1 is a real mutual zugzwang, (L, W) (P6 in §6). **CHECKED-2** (revised after K19,
  2026-10-27): K19's own P-model solver and the P-model build of kpsolve both give (L, W) in P, and kpsolve gives
  (L, W) in C. After each of the five White sorties (Black to move) White is lost in P, and after each of the five
  Black sorties (White to move) Black is lost, in P and in C. Revised after K24, 2026-10-27: two more P-model implementations (K24's `mine.c` and the referee's `psolve.py`) give (L, W) in P as well, and in C the value follows from the reduction to KPK, **CHECKED-2**: each of White's five moves is met by Black's king capturing on a4, and each of Black's five moves by White's king capturing on a5, and the KPK position is won for the capturer (kpsolve exact, K24's `kpk2.c`, `atlas/cylinder/kpk`). On flat:8×8 the bare group is (L, L), in P and in C (kpsolve exact and the P-model solvers); there is no zugzwang there.

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
  - By Lemma 2.9, (L1) fails for these three sorties. PROVED. For Ke5 the lemma applies at once. For Kd5 and Kf5,
    s plays Ke5 at its first turn; at s̄'s next turn (J1) and (J2) of the proof hold (s has no pawn, and s̄'s only
    Z-pawn is e7, below the king), and the induction of the proof runs from there (revised after K22, 2026-10-27:
    the lemma as stated needs s's king on f at Q_Z, so this step was implicit).
  - That the three sorties are *not punished* in P (no forced promotion for Black) is **CHECKED-2** (revised after
    K19, 2026-10-27): even without passes, Black cannot force promotion after Kd5, Ke5 or Kf5. K19: in the local
    game after ...Kxd7 Black has no win up to T = 13 (K19 and the referee; K19's least fixed point finds none at any
    T, COMPUTED-1), with or without passes, with the king confined to {d, e, f} or not; in the exact P-model after the sortie, against every Black reply, the result is a draw (own solver and the
    P build of kpsolve), and kpsolve gives a draw in C on the cylinder and on the flat board. Only Kf7 loses, in 10
    moves (T = 10 in the local game without the queen clause, with or without passes; with the queen clause T = 10
    without passes and 11 with unlimited passes). In chess, kpsolve gives (D, W) for the 6-rank analogue Z_72 bare,
    so White to move draws (P5). In the analogue Kb3, Kc3 and Kd3 are not punished and Kd5 loses (T = 6).
  - Revised after K24, 2026-10-27: K24 and its referee find the same with two more implementations of the local game and of
    the P model: no T for Ke5, Kd5, Kf5, with or without the queen clause, on both boards; Kf7 has T = 11 with the queen
    clause and 10 without; in the analogue Kd5 has T = 6 and Kb3, Kc3, Kd3 have none. That **White cannot win chess either**
    is **CHECKED-2** by Lemma 2.7a: with every promotion a White win, White cannot win, and with every promotion a Black
    win, Black cannot win (two implementations of both models), so the chess value is D, and kpsolve exact agrees (the
    Lichess tablebase also, on the flat board). There is no hand proof of this draw. Lemma 2.9 says only that (L1) fails
    for a defender who may pass, and White cannot pass (open question 7).
- **Theory for 7.2 + H** (H the {a,b,h} component). Theorem 2.4(b) needs the freeze only for the loser.
  - **If White wins H** (convention, V1–V2 assumed): White wins 7.2 + H. The loser is Black, and Black's
    Z-moves are universally punished. PROVED, modulo (A_Q), (V1) and (V2) for H's own events.
  - **If Black wins H:** the convention's "Black wins" is **not certified**. At the end White, in zugzwang,
    sorties with Ke5 and blockades. The outcome is then whatever the free Black king can achieve against H.
- **The paper's 7.2.** The {a,b,h} part has outcome 𝓝 with e.p. on (audit).
  - White to move: White wins, consistent with the paper.
  - Black to move: open (CONJECTURE: it may be a draw).
- **Predictions.** The bare 7.2 is (D, W), not the mutual zugzwang (L, W) (P7): CHECKED-2 in P and in C on both boards (revised after K24, 2026-10-27). The same holds for the 6-rank
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
  - Proposition 2.10(a) gives (L2), because Black cannot promote in one move from a non-terminal context; for Black to move this is Theorem 2.7(b), the window form, with Q = the position itself, and (L3) is the one-turn check that Black is not stalemated: its Z-pawn g7 has the moves g6 and g5 in every context; if Y carries an e.p. right, (L2) counts it, and it cannot promote at once (revised after K7, 2026-10-22);
  - (A_Q) is still needed for C.
- **Why the paper's "trébuchet = 0" is wrong here.** Z is not even a tempo game. It is also an instance of
  "a zugzwang where the other side's decisive event elsewhere is too slow": a Black passer created elsewhere
  is a ⊖ in the D-model but loses to f8=Q in P. So (V2) fails for Black's passers, and the D-model is wrong.
- **Without the pawn break (revised after K14 and its referee, 2026-10-27).** Z₇.₃ itself is not a two-shuttle
  component: f7–f8=Q is a White Z-move that is no suicide, so (T3) of Proposition 3.2′ fails and part (b) gives only
  r(G ⊞ Z₇.₃) ≥ r(G ⊞ dud_D), the trivial bound here. (At the two states with Kf8 the pawn f7 is blocked, so f8=Q exists
  in only two of the four states; (T3) fails all the same.) The four combined king states are legal (the kings keep
  distance ≥ 2 in all four; K1 holds: Black's g7 attacks f6 and h6, White's f7 attacks e8 and g8, so neither pawn attacks
  a shuttle square of the other king), so the geometry of Lemma 3.2″ holds. "If f8 were unavailable" does not define a group. The earlier sentence "would be dud-type" is
  withdrawn as unproved. The two-sided proposition it needed is now Proposition 3.2′ (PROVED in the D-model). A group of
  this type exists elsewhere on the flat 7×6 board: Z_B of §5.7 (every non-shuttle move loses at once in P, CHECKED-2),
  and Z_A of §5.7 is two-shuttle up to one White break.
  - *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. This is the earlier scratch search on the cylinders only, with
    one-ply tests, not re-run; it says nothing about flat boards, where Z_B exists (§5.7). "dud may not occur in small
    K+P groups" remains a CONJECTURE for chess and for the cylinder.

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
- **But Black has an escape. CHECKED-2 (revised after K19, 2026-10-27; kpsolve agrees).** After the sortie Kc5
  and Kxb3, White cannot force promotion even without passes, and not with unlimited passes either (no win up to T = 20
  confined and T = 12 unconfined, for each budget k = 0, …, 6, 8 and ∞, K19 and the referee; K19's least fixed
  point finds none at any T, COMPUTED-1). After Kd4 and Kd5, White wins the local game against each finite budget
  of Black's passes that was checked (T = 6 + k with the queen clause, k = 0, …, 6 and 8; for larger k the formula
  is a CONJECTURE) and does not win against unlimited passes (no win up to the same bounds): "wins only if Black
  has no spare move" is right for an unlimited supply of passes and was too strong as written for a finite one.
  After Kd3 White wins with T = 5 for each budget k = 0, …, 6, 8 and ∞. So (L1) holds for Kd3 and fails
  at k = ∞ for Kd4 and Kd5, which are nevertheless punished in P and in C in the bare group, where Black has no spare move
  (k = 0, T = 6). A context with k spare moves costs k tempi (T = 6 + k), and (L2) then asks for μ ≥ 7 + k.
  Black's legal moves in the group are Kc5, Kd4, Kd5 and Kd3 (revised after review: R1 item 10 — Kd3
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
  - Black's local win after Ke6 Kxg4 takes T = 5. **CHECKED-2** (revised after K19, 2026-10-27: the scratch run and
    K19's code agree. T = 5 for every pass budget 0, …, 4 and ∞, with or without the queen clause and the
    confinement to {f, g, h}. Here Q_Z = `Ke6 kg4 pg5`: the context pawns c3 and d6 are deleted.)
  - So μ = T, and (L2) fails by one tempo. **CHECKED-2** (Review 4 re-derived both numbers, and K19's breadth-first
    search gives μ_W = 5 with the same Q°, so μ_W = 5 < T + 1 = 6). The sortie nevertheless loses in P: the P build
    of kpsolve gives Black the win after Ke6 (`Ke6 Pg4 Pc3 kh4 pg5 pd6 b -` is L from White's side;
    COMPUTED-1, K19), so the documented draw is an (A_Q) failure, not a failure in P.
- PROVED: by Theorem 2.7 (contrapositive), for every admissible reply r (Definition 2.6) and every T ≥ 1, every king
  move that does not lose in P violates (L1), (L2) or (L3) (revised after K7, 2026-10-22). A move that loses in P but not in C is an (A_Q) failure.
- CONJECTURE: every one of the 48 non-losing king moves has μ ≤ T + 1 at its node: an (L2) failure, or an
  (A_Q) failure with margin one. *To settle:* compute μ and T at those 48 nodes from `engine/suite/results.json`.

---

### 5.7 Two-shuttle groups (K14, 2026-10-27; revised after the K14 referee, 2026-10-27)

Two groups on the flat 7×6 board (F_Z = {a, b, c}, buffer d, context on e–g): Z_A, found first, has one White break,
and Z_B (below, after Z_A) has none. Everything below is a statement in the P model unless chess is named.

**Z_A = Ka5, Ka6 (shuttle) / kc5, kc6 (shuttle) / Pb3 pb4 pb5**, on the flat 7×6 board (F_Z = {a, b, c}, buffer d, context
on e–g). Kings at (a, c) ∈ {a5, a6} × {c5, c6}.
- **Geometry. PROVED by enumeration.** The four states satisfy (K1) and (K2): pb4 and pb5 attack a3, c3, a4, c4, and Pb3
  attacks a4, c4, none of the four shuttle squares; d(a, c) = 2 in all four. The Z-pawns are blocked (b3–b4–b5) and cannot
  move. White's legal moves other than the shuttle: **Kxb4 at (a5, c6) only** (b4 is then undefended); at every other
  state White has no other move (a4 is attacked by b5, b5 is guarded by the Black king, b6 is next to the Black king).
  Black's legal moves other than the shuttle are the sorties c5–d4, d5, d6 and c6–d5, d6 (c4 is attacked by b3, b6 is next
  to the White king).
- **Z alone is (D, D) at all 8 roots** (4 states × 2 sides to move; `kp_p --pmodel`, the P model with real kings, exact: COMPUTED-1). Every
  Black sortie loses at once (the position after it is a White win). White's Kxb4 draws: it is a non-suicidal further White
  Z-move, so (T3) fails at (a5, c6) and Z_A is a two-shuttle component *up to one White break*. Reproduce: the 8 roots
  (e.g. `Ka5 kc6 Pb3 pb4 pb5 w -`) piped into `kpp --board flat:7x6 --ep on --promote QRBN --cap 1 --pmodel --moves`,
  where `kpp` is a private build of `kings/delegate/out/K7/scripts/draft/kp_p.c`.
- **What Proposition 3.2′ gives for Z_A.** (T1), (T2), (T4) hold at all four states (T4 in the Z-alone sense above), so part
  (b) gives r(G ⊞ Z_A) ≥ r(G ⊞ dud_D) in the D-model, part (c) transfers a White win from any state, and a Black win from
  the two states with the Black king on c5 (there White has no move but the shuttle).
- **Contexts. COMPUTED-1 (P model), prediction CHECKED-2.** 68 pawn-only contexts of ≤ 3 pawns on the files f and g (all six
  outcome pairs of G ⊞ dud_D occur: (D,D), (D,L), (L,L), (W,D), (W,L), (W,W)), each with the four king states and both
  sides to move (544 roots). In **53 contexts** the exact P-result of G ⊞ Z_A equals the prediction r(G ⊞ dud_D) at all 8
  roots. Examples (White's, Black's pawns; prediction): none; f3 / f4 (D,D) blocked; f2 / — (W,W); — / f3 (L,L); f3 / g4
  (W,L); f2 f4 / g5 (W,D); f2 / f5 g3 (D,L). In the **15 other contexts** (40 roots) the result differs, in every case at
  a context in which (Pun) fails somewhere on the regular positions. In all 40 mismatching roots the prediction is D and the result is decisive: Black
  wins in 10 contexts (a sortie beats the context race), White in 4 (White's break Kxb4 turns Black's shuttle into a
  zugzwang), both in 1. Predicted W or L was never contradicted in this f/g sample. Example f2 / f3 (blocked, so G has no move): the prediction is (D, D), but Black to move at (a5, c5) must
  shuttle to c6, and Kxb4 then wins; four of the eight roots are W. With the context on files e–g (closer to the sortie
  squares) 5 of 12 representative contexts fail (24 of 96 roots), and with White e2, Black g4 (prediction (W, L)) the
  result is (L, L) at all 8 roots: a predicted White win is contradicted there, so "never contradicted" holds only in
  the f/g sample. In the larger sample of all 885 contexts with ≤ 2 + 2 pawns on files f, g (7,080 roots), 58 contexts
  (156 roots) differ from r(G ⊞ dud_D), all with prediction D and a decisive result, and again no predicted W or L is
  contradicted (the referee's kpp run, COMPUTED-1; the rates 58 of 885 and 15 of 68 are not comparable, the samples
  differ).
- **Chess (C) for Z_A. Mostly not done.** In chess (`kpsolve --board flat:7x6 --ep on --promote QRBN --cap 1`) Z_A alone
  is (D, D) at all 8 roots, exact (COMPUTED-1, 1.4 CPU-s). The chess results with contexts were not computed. So (A_Q) is not checked for any context, and every context result above is a statement in P.
- **The bridge on Z_A. COMPUTED-1.** `scripts/bridge_check.py` enumerates the regular positions of each context (8 to
  about 330) and classifies every legal move as context move, shuttle or other. (Pun_White) holds at all regular positions
  in 14 of the 68 contexts, (Pun_Black) in 17, both in 2 (the referee's own generator of the 2,304 regular positions
  agrees, and finds exactly one shuttle for the side to move at each). Theorem 3.2‴(a): at the 208 roots where (Pun) for
  the loser holds on the regular positions reachable from the root and r_D = W (resp. L) for the winner, P agrees: 0
  failures. Theorem 3.2‴(b): 48 roots with both (Pun)'s, 0 failures. (Counts under the referee's convention; K14's own
  convention gave 200 and 16, also with 0 failures.) All 15 mismatching contexts have a (Pun) failure: 0 contexts where the hypotheses hold and the conclusion
  fails. (Pun) is sufficient, not necessary: many of the 53 matching contexts have a (Pun) failure at some regular position
  that the winner's play never uses.
- **An exactly frozen two-shuttle group: Z_B (revised after the K14 referee, 2026-10-27). Z_B alone: CHECKED-2 in P; the
  search and the contexts: COMPUTED-1.** K14's first search (next bullet) found none, because it cut the candidates by an
  approximate count of other moves (at most 18, and 12 for 3 + 3 pawns). The referee searched flat 7×6 with F_Z = {a, b, c}
  and at most 2 White and 2 Black pawns on ranks 2 to 5, **with no cut-off**: 817,270 placements in which the four
  combined king states are legal (K1, K2). At the two roots (z, w), White and Black to move, 535 placements have no
  non-shuttle move that fails to lose at once. At all 8 roots **2 placements have none (mirror images of each other)**
  and 12 have exactly one (Z_A type).
  - **Z_B:** White king b2, c3 (shuttle), Black king a4, b5 (shuttle), pawns Pa3 Pb4 pb3 pc4. Its mirror (a ↔ c) is
    Ka3, Kb2 / kb5, kc4 / Pb4 Pc3 pa4 pb3. Roots are written like `Kb2 ka4 Pa3 Pb4 pb3 pc4 w -`.
  - *Geometry. PROVED by enumeration.* (K1): pb3 attacks a2, c2; pc4 attacks b3, d3; Pa3 attacks b4; Pb4 attacks a5, c5;
    none of b2, c3, a4, b5. (K2): d(b2, a4) = 2, d(b2, b5) = 3, d(c3, a4) = 2, d(c3, b5) = 2.
  - *Move lists at the 8 roots (P model).* The value is that of the position after the move, from White's point of view
    (L = White has lost, W = White has won, D = draw). White to move | Black to move:
    - (b2, a4): Kb1 L, Kc1 L, Ka1 L, b4–b5 L, shuttle D | shuttle D, c4–c3 W
    - (b2, b5): Kb1 L, Kc1 L, Ka1 L, a3–a4 L, shuttle D | Kb6 W, Kc6 W, Ka6 W, c4–c3 W, shuttle D
    - (c3, a4): Kc4 L, Kd4 L, Kd2 L, b4–b5 L, shuttle D | Kxa3 W, b3–b2 W, shuttle D
    - (c3, b5): Kd4 L, Kd2 L, a3–a4 L, shuttle D | Kb6 W, Kc6 W, Ka6 W, b3–b2 W, shuttle D
  - **Z_B alone is (D, D) at all 8 roots in P, and every non-shuttle move loses at once** (every non-shuttle move is a loss for the
    mover; the shuttle draws). So (Pun) holds for Z_B alone at all 8 roots, in both colours. **CHECKED-2:**
    the referee's build of kp_p (the K7 P-model solver) and the K23 referee's solver ref3
    (`kings/delegate/out/K23/verify/ref3.cpp`, which shares no code with kpsolve or kp_p; for flat boards pass
    `--board flat7x6`, a parsing quirk) give the same 8 root values and the same move lists, as re-run by the integrator.
  - *Contexts. COMPUTED-1 (the referee's kpp run), prediction CHECKED-2.* The P-result of G ⊞ Z_B equals the prediction
    r(G ⊞ dud_D) at every root, all outcome pairs included, in: the 68 contexts with ≤ 3 pawns on files f, g (544 roots),
    the 12 representative contexts on files e–g (96 roots), and the first 660 of the 885 contexts with ≤ 2 + 2 pawns on
    files f, g (5,280 roots): 0 contexts and 0 roots differ. 225 of the 885 contexts are untested. Z_A on the same 885
    contexts differs in 58.
  - *The bridge on Z_B. COMPUTED-1* (the referee's `vbridge2.py`, 68 f/g contexts). (Pun_White) holds at all regular
    positions in 19 contexts, (Pun_Black) in 15, both in 7; no context has a mismatch. Theorem 3.2‴(a): 160 instances, (b):
    56 instances, 0 failures.
  - *Chess. Undecided.* In chess with cap 1 the bounds at the 8 roots of Z_B alone are (W, L): the capped promotions are
    met and cap 1 does not decide. Whether Z_B is exactly two-shuttle in chess is open (cap 2 not run, memory), and so is
    every chess result beside contexts.
  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact, and 225
    of the 885 contexts are untested. It is open on the cylinder and on other boards.
- **K14's first search (superseded by Z_B). A record of what the script printed, not reproduced by the referee, and not a
  negative result.**
  `scripts/search_groups.py` lists every placement of the kings and of pawns on F_Z in which the four combined king states
  are legal (K1, K2: kings with two adjacent safe squares each, never touching) and the number of other legal moves in the
  four states is at most 18 (12 for ≤ 3 + 3 pawns on three files). It listed 6,674 groups (flat 7×6, flat 7×7, cylinder
  7×6), 1,147 of them (D, D) at all 8 roots with Z alone, and found none with every non-shuttle move losing at once. **The
  cut-off excluded Z_B:** with the cut-off raised to 40 the script lists Z_B, which has score 26. The statement "no exactly
  frozen group in this family" is therefore false for flat 7×6. The script's statements for the 7×7 board and the 7×6
  cylinder (including "the minimum is 12" and "none comes close") depend on the same cut-off, were not repeated without
  it, and are not claimed.

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
| P4 | cyl:7x6 | Z_T `Ka4 Pb3 kc3 pb4` + each of {nothing, Hm1, Hp1, H\*, H\*2, H0} | equal to the convention: (L,W), (L,L), (W,W), (W,L), (W,L), (L,W) | same | (L,W), (L,L), (W,W), (D,L), (D,L), (L,D) | Thm 2.4(b) + Thm 2.7. (L1) holds: scratch, T ≤ 5, all budgets, confined king. (L2) holds at every loser-to-move node: scratch. (L3) not checked. These checks used the local game and the μ before K7: the old μ counted the king and all pawns, and Definition 2.6 now counts the king and context pawns, with the e.p. clause (revised after K7, 2026-10-22) | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\*, H\*2, H0), in C. In P all six rows equal the convention: CHECKED-2 (three implementations agree; revised after K23, 2026-10-27), so the refutation is a chess-only effect and its cause was not examined |
| P5 | cyl:7x6 | Z_72 `Kc4 Pb5 kb6 pc5`, bare; and + Hp1 | bare (D, W); + Hp1 (W, W) | bare (L, W); (W, W) | bare (D, W); + Hp1 (W, W) | Black side: Prop 2.10(a) with T = 1 (PROVED in P). White side: Lemma 2.9 (escape by blockade) | all entries PROVED in P except the bare w-entry, which is CHECKED-2 (K19, 2026-10-27: the P-value D from an own solver and from `kp_p --pmodel` (K7's P-model build of kpsolve), and D in C from kpsolve; K24, 2026-10-27: the P-value D also from `mine.c` and the referee's `psolve.py`, and D in C by Lemma 2.7a with EPW = EPB = D for White to move, which agrees with kpsolve exact; no hand proof) (revised after K24, 2026-10-27); kpsolve agrees on all four entries |
| P6 | cyl:8x8 | 5.1 `Kh5 Pa4 kb4 pa5` | (L, W): a real mutual zugzwang | (L, W) | (L, W) (kpsolve, exact) | Thm 2.4 + Thm 2.7 ((L1): CHECKED-2, T ≤ 7; (L2) holds trivially in the bare group, which has no context pawn; (L3): CHECKED-2) + self-duality (also checked numerically by K19) | CHECKED-2 (K19, 2026-10-27: (L, W) in P from two solvers); kpsolve agrees. Revised after K24, 2026-10-27: K24's `mine.c` and the referee's `psolve.py` (two more implementations, written from `kings/SPEC.md`) give (L, W) in P as well, and the Theorem 2.7 route is run for all ten sorties ((L1) T = 6, 6, 6, 7, 7 with the queen clause and 6, 6, 5, 6, 6 without; (L2) vacuous; (L3) 0 stalemates). In C, (L, W) is CHECKED-2 by the reduction to KPK: every move is met by the capture of the group's pawn, and the resulting KPK is won in kpsolve exact, K24's `kpk2.c` and `atlas/cylinder/kpk`. On flat:8×8 the entry is (L, L), in P and in C. The K23 referee's own solver (a third implementation) also gives (L, W) in P for the bare group (revised after K23, 2026-10-27). Beside contexts the zero of this group can fail: P13 |
| P7 | cyl:8x8 and flat:8x8 | 7.2 group `Ke6 Pd7 kd8 pe7` | (D, W) | (L, W) | (D, W) on both boards (kpsolve; Lichess on flat) | Prop 2.10(a) for Black; Lemma 2.9 for White | b PROVED in P; w CHECKED-2 (K19, 2026-10-27: D in P from two solvers, on both boards); kpsolve and Lichess agree. Revised after K24, 2026-10-27: the w-entry is also D in P from `mine.c` and the referee's `psolve.py`. In C the w-entry is D by Lemma 2.7a (EPW and EPB both D for White to move, two implementations) and kpsolve exact, CHECKED-2, with no hand proof (Lemma 2.9 only refutes (L1) for a passing defender; open question 7). In C the b-entry is W by the reduction to KPK (after Kc7 White's king takes e7, and `Ke7 Pd7 kc7` with Black to move is won, on both boards: kpsolve exact, `kpk2.c`, `atlas/cylinder/kpk`), CHECKED-2 |
| P8 | cyl:8x8; cyl:7x6 | 7.3 group `Kg8 Pf7 kf6 pg7`; 6-rank analogue `Kc6 Pb5 kb4 pc5` | (W, W) | (L, W) (read as 0) | (W, W) on 8×8 (kpsolve; Lichess on flat) and on the 6-rank analogue | unparriable safe promotion (§5.3) | PROVED in P |
| P9 | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 kc6 pb5 pf3` | (W, L): class 𝓝 | BIG with Z as `on`: (W, W) | (W, L) | Thm 3.3 versus Thm 3.4(b). Black: fxe2 and e1=Q; White: exf3, then zugzwang (Kd5 forced) | PROVED in P; kpsolve agrees |
| P10 | cyl:8x6 | Z_onT1 + k Black tempo units: k = 0 nothing; k = 1 `Pe2 pe3 pe5`; k = 2 also `Pg2 pg3 pg5` | (W, W) for k = 0, 1, 2 | (L,W), (L,L), (L,L) | (W, W) for k = 0, 1, 2 | Prop 4.3 + Thm 3.4(b): the result does not depend on k, and there is no integer threshold | PROVED in P; kpsolve agrees for k = 0, 1, 2 |
| P11 | cyl:8x6, `--frozen` | Kings parked on the a-file (`Ka1 ka6`, b- and h-files empty); pawn components on c–g; every passer and race terminal of the D-game of X certified by Corollary 2.11a, and, if X already has a passer, X itself certified by Proposition 2.11 (s the side to move, β the side W(X) credits) (for the beneficiary's passed front pawn: (H4) and (H5); in this layout (H2), (H3) and the king clause of (H1) hold by Corollary 2.11b); condition (E). Here W(X) is the D-game of X with its own winning side, and "hereditarily sum-safe" (HSS) means (HSS) and (B) of Theorem 1.11(c), that is (V4) of Theorem 1.14: at every position reachable before the first decisive event, the re-split components are pairwise safe and BIG exceeds every tempo count | kpsolve `--frozen` = o(W(X)); also = o(S(X)) when hereditarily sum-safe. Where o(S) ≠ o(W) (opposite threats, Prop 1.12), `--frozen` sides with W | — | — (a harness check, not one position) | Thm 1.11 + Thm 1.14 ((V3), and (V2) at king moves, hold by fiat; (V1) holds in the layout by Corollary 2.11b: no check, and a2 or a5 is always a legal king move) + Proposition 2.11 / Corollary 2.11a for (V2) at passer and race terminals | PROVED in P, conditional on the certificate (revised after K10, 2026-10-22). False without it: `Ka1 ka6 Pc2 Pc3 pd3 pd4 w -` is a White win in W(X) and (L, L) in `--frozen`; checked end to end on 56,872 roots (a root is a position with its side to move, here without a passer) of cyl:6×6, cyl:7×6 and cyl:8×6 (0 violations when every terminal is certified; 3,194 roots differ otherwise); roots with a passer: 716,962 swept by K12 with 0 certified violations (COMPUTED-1; CHECKED-2 on the 6×6 and 8×6 roots without e.p. rights, revised after K12, 2026-10-27) |
| P12 | cyl:7x6 | Z_T + any context on e–f | If `--frozen` reports a win for σ at X, then either σ wins in P, or, for every `--frozen` winning strategy of σ, some node of it with σ̄ to move has a king move of σ̄ that is not a P-loss. For that move, and for every admissible reply r (Definition 2.6) and every T ≥ 1, (L1), (L2) or (L3) fails. In chess, add (A_Q) at X | — | — (a harness check, not one position) | Thm 2.7 (contrapositive) + the transfer argument of Corollary 2.7′ | PROVED after repair, in P, for the nodes where `--frozen` reports a win; the chess form needs (A_Q) (revised after K7, 2026-10-22) |
| P13 | cyl:7x6; cyl:8x8 | Z_T `Ka4 Pb3 kc3 pb4` beside G1 = `Pe3 pe4` and G2 = `Pe2 pe3`; on cyl:8x8 the group of §5.1 `Kh5 Pa4 kb4 pa5` beside the same pairs | none made in advance. For Z_T, Theorem 2.7 would give (L, W) for G1 if (L3) holds ((L1) with T = 4 and (L2) with μ_s = 5: COMPUTED-1, K23 referee), and says nothing for G2 ((L2) fails by one tempo, μ_s = 4 = T) | G1 and G2 both (L, W) | P (exact, not C): G1 (L, W), G2 (L, L) on both boards; C not run (cap 2 is too large on cyl:7×6) | Prop 2.10(b) + Thm 2.7 for Z_T (race count in §2 after Proposition 2.10(b)); the mechanism was analysed for Z_T only, not for the group of §5.1 on cyl:8x8 | CHECKED-2 (K23, 2026-10-27: three implementations agree on every number; no hand proof): the zero fails in P beside G2, not beside G1. T = 4 and μ_s = 4, 5 are COMPUTED-1 (one implementation). The general statement for every frozen group is a CONJECTURE |

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
  is *right* there. kpsolve refutes it in 3 of the 6 contexts, in C. In P all six rows equal the convention
  (CHECKED-2, three implementations agree, K23: `kings/delegate/out/K23/logs/key_digest.txt`), so the three
  refutations are chess-only effects (not P effects), and their cause was not examined in K23. P4 does not show a
  context-dependent zero in P; P13 does (revised after K23, 2026-10-27).
  - H\* and H\*2 with White to move are draws, not (W, L). In H\* every White king move loses (Ka5, Kb5, Kg3,
    Kg4, Kg5) and White's only drawing move is e3–e4; in H\*2 the position is a draw as well.
  - H0 with Black to move is a draw, not (L, W): Black's king draws by Kd3 or Kd2.
  - The mechanism: the defending king walks to the locked context pawns and attacks the stuck pawn there
    (…Kd3, …Kd2, …Kd4). In H0 after …Kd3 the white king is confined to the a- and b-files: Kg4, Kg5 and Kg3
    all lose, while Ka5, Kb4 and Kb5 draw. In C the sorties draw; K23 did not run C. In P the same sorties lose
    (H0 is G1 of P13, where (L2) holds with μ_s = T + 1 = 5), so the C result is not a P effect, and it was not
    shown to be an (L2) failure. By the note's own text a margin μ_s = T + 1 does not give a chess win (queen against
    queen, (L2⁺)), so (A_Q) or this margin may be the cause; that is a guess and was not tested. The zero of Z_T
    is context-dependent in P for a different reason (P13: a timing tie of one tempo in G2, Proposition 2.10(b);
    revised after K23, 2026-10-27).
  - The same three contexts are exactly the ones in which the Z = 0 convention and literal cylcgt are wrong
    too, so the refutation is a fact about the positions, not about the convention.
- **P11 and P12** turn Theorems 1.11, 1.14 and 2.7 into checks of the solver.

---

## 7. Trying to break the proofs

Each item is a counterexample type the task named, or one found while writing.

1. **A zugzwang where the mover can make a decisive threat elsewhere first.**
   - In the D-model a mover with a decisive option is not in zugzwang, so nothing breaks there.
   - In P the threat may be too slow. In 7.3, a Black passer elsewhere loses to f8=Q.
   - That is a (V2) failure for the passer, not a gap in Theorems 1.14 or 2.4, which assume (V2). With
     frozen kings, the certificate of Proposition 2.11 fails there at (H5), the timing bound over all of the opponent's pawns (a failed
     certificate does not by itself prove a (V2) failure: 2.11 is sufficient only);
     with real kings only the square-rule CONJECTURE of Remark 2.11 applies (revised after K10, 2026-10-22).
2. **Double threats.**
   - They are just Λ-positions in Theorem 3.4: every reply leaves a threat. No proof uses "one threat at a
     time".
   - Theorem 1.11 needs pairwise safety only *between* components. Several threats inside one component are
     allowed.
3. **Stalemate.**
   - It broke the naive argument: Lemma 1.7 is false under chess rules.
   - Hence (V1b) in Theorem 1.14, (L3) in Definition 2.6, the unlimited-pass clause in (L1) (the earlier "every budget" phrasing is withdrawn; revised after K7, 2026-10-22), and the traps
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
   - Proposition 2.11 is proved only with frozen kings. With real kings the defender's king may catch the
     passer (`Ka1 ka6 Pc2 w -` is (W, W) frozen and (D, D) with real kings); the real-king form is the square-rule
     CONJECTURE of Remark 2.11 (revised after K10, 2026-10-22).
   - The engine-suite escapes (§5.6) are this type. Theorem 2.7 explains them only as certificate failures;
     it does not claim to predict which ones draw.
6. **Checks.**
   - Context pawns never attack F_Z (Lemma 2.2).
   - Inside Z, checks are part of Z's own move lists. The scratch geometry includes legality under check.
7. **Extra moves of the winner.**
   - Z_onT1 gives White king moves to g4–g6 that are not shuttle moves. The sharp form of Theorem 1.14 covers
     the winner: those moves are simply not played, and Lemma 1.6 is not needed (revised after K9, 2026-10-22).
   - When Black is the winner (P9, Black to move), Black's forced line was checked against *all* White moves.
     Black promotes on e1 at its second move, and no White king square is within reach of e1.
8. **Is the 2-cycle really equivalent to a self-loop?**
   - The bisimulation in Proposition 3.2 needs *both* shuttle states to have identical properties. For two shuttles
     (Proposition 3.2′) it needs all four combined states, with both shuttles legal in each; deleting any one of the
     eight arrows changes the result (Proposition 3.2′(d)), and the kings' opposition, a missing diagonal state, gives
     (W, L) instead of (D, D).
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
- "The trébuchet zero is universal": downgraded then to Proposition 2.10(b) plus a CONJECTURE. After K23 it is false
  for Z_T in P: Z_T does not act as 0 beside {Pe2, pe3} on cyl:7×6 (CHECKED-2, three implementations agree, P13). That
  the zero of every frozen group with T ≥ 2 is context-dependent is still a CONJECTURE (revised after K23,
  2026-10-27).
- "A dud group exists in small K+P positions": now a CONJECTURE. (After K14 and its referee, 2026-10-27: Z_B of §5.7
  has every non-shuttle move losing at once in P, CHECKED-2, and equals dud_D beside every context tested, COMPUTED-1;
  Z_A is dud-type up to one White break. Chess (cap 2), the cylinder and other boards are open.)
- "The bare 5.1 / 7.2 / Z_72 results": CONJECTURES with scratch evidence (raised to CHECKED-2 after K19,
  2026-10-27; see the status table).

---

## 8. Open questions

1. **Tempo matching** (CONJECTURE). Suppose a group's punishment wins only in the plain local game, not
   against passes. Is it still decisive in contexts that are second-player wins for the punisher, with each
   defender tempo answered by a punisher tempo?
   - The question is untested. Every trébuchet placement checked on the 7×6 cylinder satisfied (L1) for every
     budget k ≤ 4 and for k = ∞ (the local game before K7; Definition 2.6 now has k = ∞ only; revised after K7,
     2026-10-22).
   - The only plain-but-not-passing wins found are Z_on's sorties Kd4 and Kd5 (§5.5). Z_on also has an
     outright escape, Kc5, so it cannot test the question.
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist? Both
   need wider searches. (After K14 and its referee, 2026-10-27: on the flat 7×6 board Z_B of §5.7 has every non-shuttle
   move losing at once in P, CHECKED-2; a search of flat 7×6 (F_Z = {a, b, c}, ≤ 2 + 2 pawns, no cut-off) found exactly
   two such placements, mirror images, among 817,270, COMPUTED-1. Beside every context tested its P-result equals that of
   dud_D (COMPUTED-1; 225 of 885 contexts untested). K14's own search had a move-count cut-off (18), which excluded Z_B,
   so its negative statements are withdrawn. Open: chess (cap 2; cap 1 gives bounds (W, L)), the cylinder, other
   boards.)
3. King-against-king fights inside Z (opposition, shouldering) are genuine short or loopy games. What values
   occur? This is where finite king tempo can live, by Proposition 4.3.
4. A version of Theorem 1.11 for loopy components: the D-semantics analogue of Siegel's stopper sums.
5. Gafni's K+P vs K values without edges (plan item A8): the cylinder KPK table in `atlas/cylinder/kpk` is the
   starting point.
6. **Universal zeros** (CONJECTURE, after Proposition 2.10(b); revised after K23, 2026-10-27). The zero of Z_T is
   context-dependent in P (P13, CHECKED-2). Is there a frozen group with T ≥ 2 that acts as 0 beside every context,
   for instance one whose sortie king cannot reach the buffer before the punisher wins? Solving candidates
   exhaustively on contexts of at most two pawns a side, as K23 did for Z_T (`kings/delegate/out/K23/scripts/` and
   `kings/delegate/out/K23/verify/`), is feasible in P.
7. **A hand proof that White cannot win in 7.2** (CONJECTURE; revised after K24, 2026-10-27). The w-entry of P7 is D in P and
   in C, and so is the w-entry of P5, each CHECKED-2 by computation (Lemma 2.7a for C). No proof by hand exists. Lemma 2.9
   only refutes (L1) for a defender who may pass, and White cannot pass. A proof would have to show that after Ke5, Kd5
   or Kf5 Black has no forced promotion and no forced mate against any White play (for instance by an explicit drawing
   strategy built from the blockade), and that Kf7 is the only losing sortie (T = 11 with the queen clause and 10
   without).

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
  - no dud and no over group. (This scratch search covered the cylinders only. K14 repeated the dud search on the 7×6
    cylinder and the flat 7×6 and 7×7 boards with kpsolve as the filter, with a move-count cut-off (18), which excluded
    Z_B (§5.7); its negative result is withdrawn. A search of flat 7×6 without the cut-off found Z_B.)
- **Local promotion game.** Retrograde least fixed point over (position, side to move, pass budget k ≤ 4 or
  ∞), with only Z's pieces on the board. (This is the game as it was before K7. Definition 2.6 now has k = ∞
  only, counts a mate of s as a win for s̄, and always confines s̄'s king to F_Z. The K7 checks below use the new
  game; revised after K7, 2026-10-22.)
  - The attacker wins by promoting to a queen that cannot be captured at once.
  - Stalemate, a defender promotion and infinite play are attacker failures.
  - Option: confine the attacker's king to F_Z.
  - The reported T is the number of attacker moves under best play.
- **μ.** A breadth-first search over the defender's moves alone (king and pawns), with the other side's
  context pawns fixed and its king absent. It covers every context position reachable inside the e-file
  context. (This is the μ_s before K7. Definition 2.6 now counts the defender's king and the context pawns only,
  with s̄'s king and all Z-pawns deleted and the e.p. clause. The K7 checks below use the new count; revised after
  K7, 2026-10-22.)
- **Full P-model check.** The local promotion game run on the full positions of §6, with no budget (k = 0).
- **K7 checks of Theorem 2.7 (2026-10-22; scripts copied to `kings/delegate/out/K7/scripts/`, raw output in the local
  archive `kings/delegate/out/K7/k7_k9_scratch.tar.zst`).** They test the
  statement, not the proof, on random positions with at most 3 pawns a side (revised after K7, 2026-10-22):
  - a Python move generator, which agrees with `kpsolve --moves` on 1200 random positions (cyl:7×6, cyl:6×5,
    flat:5×4) and on 600 positions with an e.p. right (cyl:7×6, flat:6×6);
  - a solver of the local game of (L1) (passes, confined king, mate of s a win, promotion by s a failure, T ≤ 5),
    a search for μ_s (context pawns only, and the old count with Z-pawns), and a search of the real window game
    for (L3). In that search s is free, and s̄ plays any move whose projection is a winning local move, except
    king moves off F_Z. It did **not** exclude context moves of s̄, so its strategies are wider than the guided
    strategies of Definition 2.6 as now worded (Z-moves only). The runs are therefore not an exact test of the
    stated (L3); a reviewer's corrected harness (below) restricts s̄ to Z-moves;
  - the exact P value from a private copy of `kings/kpsolve.c` with one added switch, `--pmodel` (a promotion wins at
    once for the promoter, kings move normally). The project file is unchanged. The whole patch is three lines:
    `PMODEL = 0` added to the static flags next to `FROZEN`; the test `if (FROZEN) emit(..., 'P', ...)` at the
    promotion move generator changed to `if (FROZEN || PMODEL) emit(..., 'P', ...)`; and
    `else if (!strcmp(argv[i], "--pmodel")) PMODEL = 1;` in the option parser.
  - All K7 runs of the drafter used F_Z = {a, b, c}.
  - **Run 1 (first draft; no e.p. right at Q).** Window positions (Theorem 2.7(b); Z-group on files a–c): 9300
    positions on cyl:7×6, 7×5, 7×7, 8×6 and flat:6×6; (L1) holds in 2221, and LC_T (with (L2) on context pawns and
    (L3)) in 1379. In all 1379 s̄ wins P. Random Y, Z-move m, reply r (any non-promoting Z-move reply keeping s̄'s king
    on F_Z), cyl:7×6: 3787 triples, LC_T in 508, again all P-wins. The generator set no e.p. right at Q, so this run
    could not meet the case that broke the first draft of (b). Its (L3) routine also rejected any real promotion
    by s, which cannot happen under (L1) and (L2), so it tested a subset of the stated hypotheses.
  - **Run 2 (after the review of the first draft; e.p. right at Q).** Each position has an e.p. right: an s̄ pawn has
    just double-stepped, and an s pawn stands beside it in 85% of the cases. The target is off F_Z, except in one
    cyl:7×6 run where half of the positions have it on F_Z (934 positions with LC_T in that run, 522 of them with the target on F_Z). 34000 random positions
    on cyl:7×6 (twice), 8×6, 7×5, 7×7 and flat:6×6, T ≤ 4 (T ≤ 3 on 7×5), with (L3) as stated (stalemate of s only). (L1) holds in 7559.
    LC_T with the e.p. clause of (L2) holds in 4998, and **in all 4998 s̄ wins P: no counterexample**. LC_T read
    without the e.p. clause (the first draft) holds in 5128, and in 70 of them s̄ does not win P, which are
    counterexamples to the first draft of (b).
  - Where hypotheses fail (run 1): (L1) holds and (L2) fails in 709 non-wins; (L3) fails in 3 of the window positions
    and in 3 of the triples (all draws by stalemate of s); the old Z-pawn count would have rejected 105 window
    positions that are P-wins; in 221 the queen clause of (L1) fails while (L1_P) holds and s̄ wins P.
  - Examples: `Kb5 kd5 Pb4 Pc5 Pe3 Pf3 Pf4 Pf5` (b), `Kd6 kc2 pa3 Pe4 pe5 pf5` (w), `Ke6 ka1 Pc4 pb3 pc5` (w),
    `Kd6 kc4 Pe3 pa4 pe4 pf3` with e.p. right f4 (w) (cyl:7×6). The last one, found by the reviewers, is a White
    win in P and a Black win in P without the right (private patched copy of `kpsolve.c`).
  - **Independent re-check by a reviewer (2026-10-22; scripts in `kings/delegate/out/K7/scripts/review2/`).** A second implementation,
    written without the drafter's code, using kpsolve only for P values. Numbers as reported by the reviewer, not
    re-run by me, except where stated:
    - its move generator agrees with `kpsolve --moves` on 1600 random positions; it reproduces the (L1) values of
      §5.1 (below); Corollary 2.8 holds on 9566 placements on 4 boards, with the queen clause;
    - window form (b), random Q with 1 to 3 pawns a side, about 45000 pairs satisfying (L1) to (L3) on cyl:7×6
      (F_Z = a–c, b–d, a–b, a–d), cyl:7×5, cyl:6×6, flat:6×6 and flat:7×6 (middle group): no non-win. A structured
      e.p. family (an s pawn blocked by an s̄ pawn beside one that has just double-stepped): 19525 pairs with the
      e.p. clause, no non-win. The same positions without the clause: 53210 pairs, 8387 of them P non-wins. So the
      harness has power, and the clause cures the first draft's error. A stalemate-focused family: 40308 pairs, no
      non-win. When (L1) and (L2) hold and (L3) fails, 109 of 139 are P non-wins, so (L3) is needed;
    - form (a): 117232 triples (random Y, every Z-move m, every admissible r), and in all of them both Y·m and Q are
      P-wins for s̄. The quantitative claim, that a guided strategy of s̄ wins within T moves against every legal real
      play of s, had no failure in about 70000 pairs. With μ_s = T instead of T + 1, about 23 percent of the LC
      positions are non-wins;
    - sharpness examples of the text above: I re-ran them myself with the private builds, and they agree.
- **K19 re-computation (2026-10-27; scripts, logs and `summary.json` in `kings/delegate/out/K19/`).** One new
  implementation, written from Definition 2.6 and `kings/SPEC.md` without reading `kings/ref/` or the K7 scripts:
  - a move generator (kings, pawns, e.p., promotion), which agrees with `kpsolve --moves` on 980 random
    positions (4802 moves, 6 boards, with e.p. rights);
  - the local game of Definition 2.6: bounded recursion with a pass budget k (0, …, 8, ∞), the queen clause and the
    mate rule as switches, so that the pre-K7 and the K7 versions both run; the unbounded least fixed point; (L3) as
    a search over guided strategies against a real s without passes; and μ_s as a breadth-first search;
  - a full-board solver of the model P, which agrees with the P-model build of kpsolve on 350 random positions;
  - the local game with no passes, no confinement and no queen clause is exactly P, and agrees with the P build of
    kpsolve on 110 random positions (38 of them won by the attacker; bounded recursion and fixed point agree).
  Results: §5.1 (L1) and (L3) (five White and five Black sorties), §5.2 (not punished), §5.5, §5.6, P5, P6, P7 as
  recorded in the status table and in those sections. Every kpsolve run used a private build
  (`cc -O2 -o kp kings/kpsolve.c -lpthread`; the P build is K7's `kp_p.c`).
- **K24 re-computation (2026-10-27; scripts and logs in `kings/delegate/out/K24/`, the referee's code and logs in `kings/delegate/out/K24/verify/`, the
  referee's report in `kings/delegate/out/K24/VERIFY.md`).** K24 wrote no report file; the proof of Lemma 2.7a is in §2 of
  this note, and the referee's re-derivation is in VERIFY.md, section 5. New in K24 (revised after K24, 2026-10-27):
  - two further independent solvers of the promotion models, both written from `kings/SPEC.md`: `scripts/mine.c`
    (models P, EPW, EPB; it calls EPW `bb` and EPB `bw`) and the referee's `verify/psolve.py` (the same models, where
    EPW is `ww` and EPB is `bb`: the two programs use the name `bb` for different models);
  - the local game of Definition 2.6 and the (L3) and (L3_F) checks, `scripts/lg.py` and the referee's `verify/lg2.py`;
  - the reduction of P6 and P7 b to KPK: `scripts/reduction.py`, with the queen-only solver `scripts/kpk2.c`, compared by
    K24 with `atlas/cylinder/kpk` (`logs/reduction.log`);
  - Lemma 2.7a, and its application to P5 w and P7 w (`logs/models_p_bb_bw.log`).
  Results: P5, P6, P7 and §5.1, §5.2 as recorded in the status table, in those sections and in §6. No earlier number
  changed. The referee reproduced every number with code of its own and with its own builds of `kings/kpsolve.c`,
  `kp_p.c` and `atlas/cylinder/kpk`.

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
