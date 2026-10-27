### EDIT P2.10(b): split the conjecture; the example
<<<<<<< OLD
  - So (L2) fails there, and a punishment with T ≥ 2 is never certified for all contexts. **The statement
    "The zero of such a group is context-dependent" is a CONJECTURE** (it is exactly the conjecture stated in
    the next bullet; §0 repeated it as fact). CONJECTURE: for each frozen group with T ≥ 2 there is a
    context, with the defender in zugzwang there, where the freeze actually fails in P. *To settle:* kpsolve
    on Z_T (§5.1) plus 2-file contexts with fast White pawns.
=======
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
      White to move wins by Kg5; and G1′ = {Pf3, pf4} behaves as G1.
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
      referee did not re-run the 81). So in every failing context of this sample a context pawn stands within a step
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
>>>>>>> NEW

### EDIT results table: P2.10 row
<<<<<<< OLD
for T ≥ 2 it fails in some (width ≥ \|F_Z\| + 4) | (a) PROVED after repair; (b) PROVED |
=======
for T ≥ 2 it fails in some (width ≥ \|F_Z\| + 4) | (a) PROVED after repair; (b) PROVED (the example). That the zero of Z_T is context-dependent in P is CHECKED-2 (three implementations agree, P13); for every frozen group with T ≥ 2 it is a CONJECTURE (revised after K23, 2026-10-27) |
>>>>>>> NEW

### EDIT status table: P2.10(b) row
<<<<<<< OLD
| P2.10(b) | PROVED (the example; it needs width ≥ \|F_Z\| + 4). "The zero is context-dependent" is the CONJECTURE that follows it, now supported in C by P4 | R3 item 5 |
=======
| P2.10(b) | PROVED (the example; it needs width ≥ \|F_Z\| + 4). "The zero is context-dependent": CHECKED-2 for Z_T in P (revised after K23, 2026-10-27: Z_T acts as 0 beside {Pe3, pe4} and not beside {Pe2, pe3} on cyl:7×6, and the same for the group of §5.1 on cyl:8×8; three implementations agree; no hand proof, so not PROVED). For every frozen group with T ≥ 2 it is a CONJECTURE. P4 does not show it in P: its six rows equal the convention there | R3 item 5; K23 |
>>>>>>> NEW

### EDIT status table: P4 row
<<<<<<< OLD
| P4 | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\*, H\*2, H0) | PREDICTIONS.md, theory_P4_cap2_moves.txt |
=======
| P4 | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\*, H\*2, H0), in C (revised after K23, 2026-10-27). In P all six rows equal the convention (CHECKED-2, three implementations agree), so the C refutations are chess-only effects, not P effects; their cause was not examined | PREDICTIONS.md, theory_P4_cap2_moves.txt; K23 |
>>>>>>> NEW

### EDIT section 0: the conjecture sentence
<<<<<<< OLD
  so a slower punishment's zero is not certified in every context; that it is context-dependent is a
  CONJECTURE, supported by P4.
=======
  so a slower punishment's zero is not certified in every context. That it is context-dependent is CHECKED-2 for
  Z_T in P (Z_T beside {Pe3, pe4} and {Pe2, pe3}, three implementations agree, no hand proof, P13); for every
  frozen group with T ≥ 2 it is a CONJECTURE (revised after K23, 2026-10-27).
>>>>>>> NEW

### EDIT section 7, (S2): P4 with H0
<<<<<<< OLD
  and White's Ka6 is not a P-loss; reading (b) is the one that applies (Proposition 3.2). P4 with H0, Black to
  move: Black's king sorties Kd3 and Kd2 are legal Z-moves of the loser that do not lose (a king-context
  interaction; kpsolve with cap 2 gives a draw instead of the predicted (L, W); COMPUTED-1 in C, and P was not
  run).
=======
  and White's Ka6 is not a P-loss; reading (b) is the one that applies (Proposition 3.2). P4 with H0 was listed
  here before K23 and is not an instance of (S2) in P (revised after K23, 2026-10-27): H0 is G1 of P13, Black to
  move is lost in P, so Black's sorties Kd3 and Kd2 are P-losses and the position is (L, W) as predicted (CHECKED-2,
  three implementations agree). In C, kpsolve with cap 2 gives a draw instead of (L, W), so there the sorties do not
  lose (COMPUTED-1 in C). That is a chess-only effect, outside this list; its cause was not examined.
>>>>>>> NEW

### EDIT section 5.1: the case-by-case sentence
<<<<<<< OLD
    contexts. Next to fast pawns the zero has to be checked case by case (Proposition 2.10b).
=======
    contexts. Next to fast pawns the zero has to be checked case by case (Proposition 2.10b). For this group on
    cyl:8×8 it fails beside {Pe2, pe3} in P: (L, L) instead of (L, W), CHECKED-2 (three implementations agree; P13;
    revised after K23, 2026-10-27).
>>>>>>> NEW

### EDIT section 6: P4 row, label
<<<<<<< OLD
(revised after K7, 2026-10-22) | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\*, H\*2, H0) |
=======
(revised after K7, 2026-10-22) | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\*, H\*2, H0), in C. In P all six rows equal the convention: CHECKED-2 (three implementations agree; revised after K23, 2026-10-27), so the refutation is a chess-only effect and its cause was not examined |
>>>>>>> NEW

### EDIT section 6: P6 row
<<<<<<< OLD
+ self-duality (also checked numerically by K19) | CHECKED-2 (K19, 2026-10-27: (L, W) in P from two solvers); kpsolve agrees |
=======
+ self-duality (also checked numerically by K19) | CHECKED-2 (K19, 2026-10-27: (L, W) in P from two solvers); kpsolve agrees. The K23 referee's own solver (a third implementation) also gives (L, W) in P for the bare group (revised after K23, 2026-10-27). Beside contexts the zero of this group can fail: P13 |
>>>>>>> NEW

### EDIT section 6: new row P13
<<<<<<< OLD
the chess form needs (A_Q) (revised after K7, 2026-10-22) |

**Notes on the table.**
=======
the chess form needs (A_Q) (revised after K7, 2026-10-22) |
| P13 | cyl:7x6; cyl:8x8 | Z_T `Ka4 Pb3 kc3 pb4` beside G1 = `Pe3 pe4` and G2 = `Pe2 pe3`; on cyl:8x8 the group of §5.1 `Kh5 Pa4 kb4 pa5` beside the same pairs | none made in advance. For Z_T, Theorem 2.7 would give (L, W) for G1 if (L3) holds ((L1) with T = 4 and (L2) with μ_s = 5: COMPUTED-1, K23 referee), and says nothing for G2 ((L2) fails by one tempo, μ_s = 4 = T) | G1 and G2 both (L, W) | P (exact, not C): G1 (L, W), G2 (L, L) on both boards; C not run (cap 2 is too large on cyl:7×6) | Prop 2.10(b) + Thm 2.7 for Z_T (race count in §2 after Proposition 2.10(b)); the mechanism was analysed for Z_T only, not for the group of §5.1 on cyl:8x8 | CHECKED-2 (K23, 2026-10-27: three implementations agree on every number; no hand proof): the zero fails in P beside G2, not beside G1. T = 4 and μ_s = 4, 5 are COMPUTED-1 (one implementation). The general statement for every frozen group is a CONJECTURE |

**Notes on the table.**
>>>>>>> NEW

### EDIT section 6 notes: what P4 tests
<<<<<<< OLD
- **What P4 tests, and how it failed.** P4 was the positive control: the theory predicts that the convention
  is *right* there. kpsolve refutes it in 3 of the 6 contexts.
=======
- **What P4 tests, and how it failed.** P4 was the positive control: the theory predicts that the convention
  is *right* there. kpsolve refutes it in 3 of the 6 contexts, in C. In P all six rows equal the convention
  (CHECKED-2, three implementations agree, K23: `kings/delegate/out/K23/logs/key_digest.txt`), so the three
  refutations are chess-only effects (not P effects), and their cause was not examined in K23. P4 does not show a
  context-dependent zero in P; P13 does (revised after K23, 2026-10-27).
>>>>>>> NEW

### EDIT section 6 notes: P4 mechanism sentence
<<<<<<< OLD
    (…Kd3, …Kd2, …Kd4). In H0 after …Kd3 the white king is confined to the a- and b-files: Kg4, Kg5 and Kg3
    all lose, while Ka5, Kb4 and Kb5 draw. This is what Proposition 2.10(b) predicts — the zero of the group is
    context-dependent, a CONJECTURE after Proposition 2.10(b), now supported in C by P4 — and the (L2) margin
    the theory assumed does not survive the context.
=======
    (…Kd3, …Kd2, …Kd4). In H0 after …Kd3 the white king is confined to the a- and b-files: Kg4, Kg5 and Kg3
    all lose, while Ka5, Kb4 and Kb5 draw. In C the sorties draw; K23 did not run C. In P the same sorties lose
    (H0 is G1 of P13, where (L2) holds with μ_s = T + 1 = 5), so the C result is not a P effect, and it was not
    shown to be an (L2) failure. By the note's own text a margin μ_s = T + 1 does not give a chess win (queen against
    queen, (L2⁺)), so (A_Q) or this margin may be the cause; that is a guess and was not tested. The zero of Z_T
    is context-dependent in P for a different reason (P13: a timing tie of one tempo in G2, Proposition 2.10(b);
    revised after K23, 2026-10-27).
>>>>>>> NEW

### EDIT section 7: stale "trébuchet zero is universal"
<<<<<<< OLD
- "The trébuchet zero is universal": now Proposition 2.10(b) plus a CONJECTURE.
=======
- "The trébuchet zero is universal": downgraded then to Proposition 2.10(b) plus a CONJECTURE. After K23 it is false
  for Z_T in P: Z_T does not act as 0 beside {Pe2, pe3} on cyl:7×6 (CHECKED-2, three implementations agree, P13). That
  the zero of every frozen group with T ≥ 2 is context-dependent is still a CONJECTURE (revised after K23,
  2026-10-27).
>>>>>>> NEW

### EDIT section 8: open question 6
<<<<<<< OLD
5. Gafni's K+P vs K values without edges (plan item A8): the cylinder KPK table in `atlas/cylinder/kpk` is the
   starting point.
=======
5. Gafni's K+P vs K values without edges (plan item A8): the cylinder KPK table in `atlas/cylinder/kpk` is the
   starting point.
6. **Universal zeros** (CONJECTURE, after Proposition 2.10(b); revised after K23, 2026-10-27). The zero of Z_T is
   context-dependent in P (P13, CHECKED-2). Is there a frozen group with T ≥ 2 that acts as 0 beside every context,
   for instance one whose sortie king cannot reach the buffer before the punisher wins? Solving candidates
   exhaustively on contexts of at most two pawns a side, as K23 did for Z_T (`kings/delegate/out/K23/scripts/` and
   `kings/delegate/out/K23/verify/`), is feasible in P.
>>>>>>> NEW
