# K17 final edits (fix round, 2026-10-27)

Integrator notes.
- Six blocks, all rebased onto the current `kings/theory/LOOPY.md` (it now also holds the K14, K16, K19, K20-K24 and K27 edits; commits 432907a and bbb8356). Apply them in the order given; each OLD occurs exactly once in the current file, and no block's OLD overlaps another's.
- Referee fixes implemented: (1) the counterexample to the clause "no checks" of (V1a) is labelled CHECKED-2 (three solvers: kp_p, refp.py, ref3m), never PROVED; (2) the count 1,128 is replaced by 752 (a genuine e.p. capture); the old figure appears only as a withdrawn, looser count; (3) the (S1) CONJECTURE sentence (LOOPY line 660) is replaced by referee block B1, with the label and the revision tag added and the wording made exact (Σ's step e3-e2 is illegal, and no Z-move is a D-move or a P-win for Black); (4) the proof of Proposition 1.15(a) now says "every square a context pawn can capture on is at distance >= 1 from F_Z", and "(V1a) fails at some Y iff ..."; (5) the deeper example `Kb6 kb3 Pa2 pa3 Pd2 Pe3 pe5 b -` is CHECKED-2 (kp_p and ref3m agree; D = N in the referee's own D and in cylcgt), not COMPUTED-1; (6) the statistics are CHECKED-2 as counts (the referee reproduced each with its own generator).
- Second fix round (2026-10-27), three changes. (1) In the table row (V1a), the claims that (V4) holds at X and that D_fix and D_whole give the D = N value at X are now labelled COMPUTED-1 and cite K17's `scripts/check2.py` and `logs/check2_A.json` (second entry: `V4_X_hss_exact`, `V4_strong`, `tempo_ok` true, `D_fix` = `D_whole` = (W, L), `E_violated` none); the referee verified V1b, V2, V3 and D = N (own D, cylcgt) at X, and V1-V4 only for the twin. (2) Proposition 1.15(b): the 39,600 roots of the flat:8x6 run are said to violate (E) through the persisting e.p. right, and the text says this is compatible with 0 differences on the HSS roots. (3) Proposition 1.15(b): the flat:6x6 <= 4+4 partial run now states the 5,017 E-violating roots from `summary.json` (also `logs/B2_f66_4.log`: "60000 t=577 diffs 0 E-violating 5017"). Blocks, labels and everything else are unchanged from EDITS_FINAL.md.
- Kept as a negative result: no isolated counterexample for clause (E), with its exact search boundary written into Proposition 1.15(b) (ranks 2..H-1, <= 3 context files (4 for the E search), pawn bounds per run, one locked Z pair, E search on flat:8x6 with a gap file and the right at the root only; cyl:7x6 and flat:6x6 <= 4+4 not completed). The generalisation "(E) can be dropped under (V4)" stays a CONJECTURE; the text now says that only (HSS), the first half of (V4), was tested.
- Small additions of mine, all within what the referee reported: (i) Proposition 1.15(a) is stated for the moves outside Z, because in D the Z-moves are the suicides of (V3) and not D-moves of the pawn game; (ii) one sentence in the proof of (a) says that an e.p. capture lands on the victim's file (Lemma 2.2), so it cannot capture a Z-pawn on F_Z; (iii) the table row says that retrograde legality of X was not examined (the referee's remark); (iv) the "D = N" claims name the models that were checked (the referee's own D and cylcgt), not "all three D models"; (v) a status-table row for P1.15 is added inside the first block.
- No referee point was judged wrong. Referee amendment A3(ii), as worded by the referee (1,128 roots, 752 of them genuine), is not used verbatim, because the integrator instruction is to use 752; the text states 752 and mentions 1,128 only as the withdrawn looser figure.
- Not changed: LOOPY line 2725 ("Theorem 1.14(V1a) assumes it") and the text of Theorem 1.14(V1a) itself are still correct; the referee asked for no change there.

### EDIT status row (V1a) and new row P1.15
<<<<<<< OLD
| §1.5 "each hypothesis is needed" | (V1b), (V2), (V3), (V4): counterexamples given. (V1a): none given, so "needed" is a CONJECTURE | R1 item 4, R2 item 7 |
=======
| §1.5 "each hypothesis is needed" | (V1b), (V2), (V3), (V4): counterexamples given. (V1a), clause "no checks": needed, CHECKED-2, by an isolated counterexample (cyl:6×6 `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`, a Z-pawn check; P with real kings, three independent solvers agree; revised after K17 and its referee, 2026-10-27). (V1a), clause (E) (e.p. across components): no isolated counterexample in a bounded search, so "(E) is needed" stays a CONJECTURE. In the structured class of Definition 2.1 these two clauses are the only ways (V1a) can fail (Proposition 1.15(a), PROVED) | R1 item 4, R2 item 7, K17 |
| P1.15 | (a) PROVED (hand proof, checked against Definition 2.1 and Lemma 2.2 by the K17 referee). (b) the search counts are CHECKED-2 as counts (reproduced by the referee's own generator, own D and an independent solver); "(E) can be dropped when (HSS) holds" is a CONJECTURE, bounded by the search (revised after K17 and its referee, 2026-10-27) | K17 and its referee |
>>>>>>> NEW

### EDIT heading
<<<<<<< OLD
**Each hypothesis is needed — except that for (V1a) this is a CONJECTURE (revised after review: R1 item 4,
R2 item 7).** Each can fail and change the result.
=======
**Each hypothesis is needed (revised after K17 and its referee, 2026-10-27: for (V1a) the clause "no checks" is needed, CHECKED-2, by an isolated counterexample; for its clause (E) "needed" is still a CONJECTURE; earlier: R1 item 4, R2 item 7).** Each can fail and change the result.
>>>>>>> NEW

### EDIT why exact
<<<<<<< OLD
(V1)–(V4) are sufficient, and none can be dropped, except that for
(V1a) this is a CONJECTURE (table below).
=======
(V1)–(V4) are sufficient, and none can be dropped (table below; for the clause (E) of (V1a) this is
a CONJECTURE; revised after K17 and its referee, 2026-10-27).
>>>>>>> NEW

### EDIT table row (V1a)
<<<<<<< OLD
| (V1a) non-interaction | No isolated counterexample is known: the king sorties that reach the component (41 of 449 tablebase king moves draw and 7 win, `engine/suite/`, RESULTS §1) are *unpunished Z-moves*, i.e. (V2)/(V3) failures, not (V1a) failures. That (V1a) is needed at all is therefore a **CONJECTURE** (revised after review: R1 item 4, R2 item 7) |
=======
| (V1a) non-interaction | **The clause "no checks": needed, CHECKED-2 (revised after K17 and its referee, 2026-10-27; the position is small enough that a hand proof of P = White wins is possible, but none is given).** cyl:6×6 `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`. Z = Ka2, kb4 and the locked pair Pa3/pa4 on F_Z = {a, b}; context Pd2/pe3 on d, e; buffer c, f. The Z-pawn a3 checks kb4, so Black's only legal moves are the four king moves Kb5, Kc5, Kc4, Ka5 (Z-moves), and every one loses in P with real kings: P(X) = White wins (CHECKED-2, in fact three solvers agree: `kp_p --pmodel`, K17's `scripts/refp.py`, and K23's `ref3m`, written from SPEC.md only). D, with Z deleted, lets Black play e3–e2 or e3×d2, a passer at once, so D(X) = Black wins with Black to move (and White wins with White to move: outcome class N; CHECKED-2: the referee's own D and `cylcgt` o(S) both give N). K17's own D_whole and D_fix give the same pair at X, White to move White wins and Black to move Black wins, so they agree with the value N (COMPUTED-1: K17's `scripts/check2.py`, record `logs/check2_A.json`, second entry, which also shows no (E) violation at X; the referee reproduced N with its own D and `cylcgt` but did not run D_fix or D_whole at X). So P(X) ≠ D(X). Here (V1b) holds (4 legal moves), (V2) and (V3) hold at every chess-reachable position (X alone, because every legal move is a Z-move, and all four lead to P-wins for White), and (V4) holds at X in K17's own test (COMPUTED-1: `v4_hss_exact`, `v4_strong` and `tempo_ok` of K17's `scripts/check2.py` are all true at X, record `logs/check2_A.json`, second entry; the referee did not re-run this test for X, only for the twin below, which has the same context). The twin with kb5 (no check) satisfies (V1)–(V4) at every chess-reachable position (checked by the referee's own V-checker) and P = D for both sides to move (White to move: White wins, Black to move: Black wins), so the check is the only cause. Whether X is retrograde-legal (the last White move must have been a capture onto a3, such as Pb2×a3) was not examined; Theorem 1.14 speaks of a K+P chess position and all solvers treat X as legal. A deeper context, `Kb6 kb3 Pa2 pa3 Pd2 Pe3 pe5 b -` (twin kb2; 4 chess-reachable positions with Black to move and 6 with White to move), behaves the same (CHECKED-2: kp_p and ref3m agree: X = White wins; twin, White to move: White wins, Black to move: Black wins; D = N in the referee's own D and in `cylcgt`). With frozen kings (V3 by fiat) `Ka1 kb4 Pa3 pa4 Pd2 pe3 b -` behaves the same (CHECKED-2: `kpsolve --frozen` and `ref3m --frozen`: White wins; twin kb5: Black wins with Black to move). Statistics of the search in `kings/delegate/out/K17/` (CHECKED-2 as counts: the referee reproduced every figure below with its own generator, own D and `ref3m`): frozen, 514/514 (flat:6×6 and cyl:7×6, ≤ 2+2 pawns on 3 context files), 411/411 (cyl:6×6, ≤ 3+3 pawns on 2 files) and 6/6 (cyl:5×6, one context file) contexts where Black wins D moving first give P ≠ D at the checked root; real kings, 781 (cyl:6×6), 3780 (flat:6×6), 3657 (cyl:7×6) layouts (≤ 2+2 pawns) with P = White wins ≠ D = Black wins, of which 257, 1362 and 1210 have a twin that satisfies all of (V1)–(V4) with real kings (cyl:5×6, one context file, ≤ 3+3: 0 hits). The king sorties found earlier (41 of 449 tablebase king moves draw and 7 win, `engine/suite/`, RESULTS §1) remain (V2)/(V3) failures. The clause **(E)**: no isolated counterexample, see Proposition 1.15(b) (CONJECTURE that (E) is not needed when (HSS) holds, in the searched boundary only) |
>>>>>>> NEW

### EDIT proposition 1.15
<<<<<<< OLD
| (V4) dominance | Proposition 1.12 (cancellation, for every B) and Proposition 1.13 (tempo above B) |
=======
| (V4) dominance | Proposition 1.12 (cancellation, for every B) and Proposition 1.13 (tempo above B) |

**Proposition 1.15 (what (V1a) can mean in the structured class; K17; revised after K17 and its referee, 2026-10-27). (a) PROVED by hand. (b) The counts are CHECKED-2 as counts; the generalisation is a bounded CONJECTURE.**
Let X be as in Definition 2.1 (kings and Z-pawns on F_Z, context on files at distance ≥ 2, buffer empty, no officer) and let
Y be a chess position reachable from X by legal moves in which no Z-move has been made.
- **(a)** Then the legal chess moves of the side s to move that are not Z-moves are exactly its context pawn moves (with
  the global e.p. right) if s is not in check at Y, and there are none if s is in check at Y. Whether a given side is in
  check is the same at every such Y: it is decided at X. In particular there are no pins (no slider exists before the first
  promotion), no checks arise after the root (context pawns never attack F_Z by Lemma 2.2, and kings and Z-pawns have
  not moved), and a king never blocks or captures a context pawn in one move. Read for the moves outside Z (the Z-moves are
  the suicides of (V3), not D-moves of the pawn game; Lemma 1.7), (V1a) therefore fails at some Y iff **(check)** the side
  to move at some Y is in check from a Z-pawn, or **(E)** fails (the persisting local right of a component is the only other
  difference between chess moves and D-options). *Proof.* A context pawn move is illegal only if it leaves the mover's king
  attacked. With no sliders the only attackers are pawns. Context pawns attack only buffer and context squares
  (Lemma 2.2), so after a context move the attackers of the king are the same Z-pawns as before. If s is in check, a
  context move would have to capture the checking Z-pawn, which lies on F_Z, while every square a context pawn can capture
  on is at distance ≥ 1 from F_Z, or block, which a pawn check cannot be. En passant is also a context move: the capturer
  lands on the victim's file (Lemma 2.2), so it cannot capture a Z-pawn either. The remaining difference between
  D-options and chess moves is the right that persists in a component of the sum while another component is played: that
  is (E). ∎ (The check status of a given side is the same at every Y, so "fails at some Y" is "fails at X" for (check).)
- **(check) is needed: CHECKED-2.** Example in the table row of §1.5 (`Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`, cyl:6×6; three
  independent solvers agree on P, the referee's own D gives N). The side in check has only Z-moves, so under (V3) it loses
  in P, while D lets it play in the context. This is a solver result, not a hand proof.
- **(b) (E): a negative result with its exact search boundary.** In the structured class a chess position with a pending
  right at the root, or one reached later, and ≥ 2 components, violates (E). Boundary of the K17 searches (reproduced by the
  referee with its own generator and its own D): contexts on ranks 2 to H−1 only; at most 3 context files (4 in the (E) search);
  ≤ 2, 3, 4 or 5 pawns per side as stated; Z = one locked pair Pa(r)/pa(r+1), Black king on b(r+1), White king on a or b; the
  search with a right at the root is on flat:8×6 with a gap file and the right in the root only.
  - Roots with a fresh e.p. right for the side to move: contexts on files c, d, f, g of flat:8×6 (F_Z = {a}, buffer b),
    ≤ 5 + 5 pawns: 313,476 contexts, 39,696 roots, 39,600 with ≥ 2 components. At each of these 39,600 roots the persisting e.p. right violates (E), because a right that stays pending in one component while another is played is not a D-option. This does not contradict the 0 differences on the HSS roots below: the two readings (chess e.p. and the sum with persisting rights) can differ only where (E) fails, and on the HSS roots they still agree (revised after the K17 referee check, 2026-10-27). Contexts on c to f of
    flat:6×6, ≤ 3 + 3 pawns: 3,036 roots, 192 with ≥ 2 components, no difference.
  - Roots without a right: contexts on c to f of flat:6×6, ≤ 3 + 3 pawns, 20,102 contexts: 752 roots in which (E) is violated
    (some reachable position has ≥ 2 components and a genuine e.p. capture), and D_fix = D_whole at all of them. (The first
    K17 count, 1,128, also counted a later ordinary capture of a just-double-stepped pawn; that count is withdrawn.) Not
    completed: cyl:7×6 ≤ 3 + 3, and flat:6×6 ≤ 4 + 4 (stopped after about 60,000 contexts, no difference seen; K17's `summary.json` records 5,017 E-violating roots in that partial run, and the 0 differences are over those 5,017 roots; revised after the K17 referee check, 2026-10-27).
  - Result: the whole-board D (chess e.p.) and the sum D with persisting rights differ in 48 roots of the ≤ 5 + 5 run (16
    in the ≤ 4 + 4 run), all in flat:8×6, none of them hereditarily sum-safe (HSS false: opposite threats in different
    components); `kp --frozen` gives P = D_whole in 32 of the 48 and P = D_fix in 16, which says nothing about (V1a) under (V4)
    because HSS fails in all 48. Among the 5,584 HSS roots of the ≤ 5 + 5 run there is no difference (o(S) = D_whole in all of
    them), and none among the 2,560 HSS multi-component roots of the ≤ 4 + 4 run. So no isolated counterexample for (E) was
    found, and when (HSS) holds the sum reading and the chess reading agreed on every searched root. CONJECTURE that (E) can be
    dropped under (V4), in this boundary only; the second half of (V4), "BIG exceeds every tempo count", was not part of
    the test.
>>>>>>> NEW

### EDIT B1 (S1 no longer a bare conjecture)
<<<<<<< OLD
the natural D(X) no isolated counterexample is known, so "(S1) is needed" is a CONJECTURE, as for (V1a).
=======
the natural D(X), K17's `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -` (cyl:6×6; CHECKED-2, §1.5; revised after K17 and its referee, 2026-10-27) is an isolated counterexample: σ = Black is the D-winner and is in check, its only legal moves are the four king moves (Z-moves), none of them is a D-move and none is a P-win for Black, and Σ's step (e3–e2, a context move) is illegal, so (S1) fails and P(X) is a White win. That is the same failure as the clause "no checks" of (V1a). A failure of (S1) with no check at the root is not known.
>>>>>>> NEW
