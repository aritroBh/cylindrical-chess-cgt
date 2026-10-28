# K16 final edits (fix round, 2026-10-27)

Integrator notes (read first).

- Base: every OLD block below was rebased onto the CURRENT `kings/theory/LOOPY.md` (latest commit 44d1e72), which has changed a lot since K16 wrote its EDITS.md: the K19, K23, K14, K22, K24, K11b and K12 edits are in. Each OLD text was taken from the current file and occurs exactly once.
- The R2.11 status row (line 76) now ends with the K11b sentence ("a blind re-derivation outside the Sonnet family exists since K11b ... Proposition 2.11"), then "Real kings: nothing proved, ...". The block below replaces only that last sentence and the reference column, so all K10, K10v, K10 second-round and K11b text in the row stays.
- The P11 status row (line 103) is a frozen-model statement (`--frozen`) and contains no claim about real kings, so it needs no change and has no block. The K12 root-clause sweep and the K11b scope note stay as they are. One new block adds a sentence to the P11 bullet at the end of Remark 2.11 to say that Theorem 2.11K is not used by P11.
- The text around Proposition 2.11 (lines 1307-1415) is untouched: the proposition, its proof and Corollaries 2.11a and 2.11b are frozen-king results and stay as they are. Only Remark 2.11 changes. The new theorem quotes "Step 2 of Proposition 2.11"; in the current file Step 2 is the invariant (J_β), (J_ω), (I1), as the theorem says.
- Referee fixes applied (K16v, `kings/delegate/out/K16/VERIFY.md`, section 4):
  (1) CONJECTURE' count is 172 instances in the exhaustive sweeps and 565 in total (172 + 393), not 180 and 573: the flat:6x6 <= 2+2 sweep (8) is nested in the <= 3+3 one (134), so 134 + 36 + 2 = 172.
  (2) the line "Checked, not proved: ... (H3K) implies (NS)" is now a "Computational counterpart (COMPUTED-1)" of the proved implication.
  (3) the KV = 2 parenthetical no longer asserts a mechanism the data do not record: it says omega promotes first and gives the referee's simplest mechanism (the king steps off its own pawn's path), with the example cyl:6x6 `Ka1 ke1 Pc2 pe2 w -`.
  (4) Step 2 of the proof says "by induction on the plies of the play", and the status line says "one AI proof, read step by step by the referee K16v".
- Labels used (as instructed): counterexamples CHECKED-2 (kp_p, the referee's own P solver, K16's `pyp.py`); the small exhaustive sweeps the referee reproduced exactly (flat 6x6 and 7x6 up to 1+1, flat 6x6 up to 2+0, cyl:6x6 up to 2+2) CHECKED-2; the large sweeps, the KV = 2 numbers, the flip check, the pycert check and the hunts COMPUTED-1; the real-king square rule as stated is FALSE; Theorem 2.11K is PROVED (one AI proof, read by the referee). The referee's random samples (16,500) are reported as COMPUTED-1 evidence, not as a label for the theorem.
- No other place in LOOPY.md mentions the old conjecture or says that nothing is proved about real kings (the referee's grep, repeated on the current file: lines 76, 1525, 1529, 2407, 2430-2431). Line 2429 ("Proposition 2.11 is proved only with frozen kings") would have become misleading next to Theorem 2.11K, so it is in the R3 item 5 block.

### EDIT R2.11 table row
<<<<<<< OLD
Real kings: nothing proved, the square rule is a CONJECTURE (scratch evidence) | R3 item 6; K10 |
=======
Real kings (revised after K16, 2026-10-27): the square-rule CONJECTURE of Remark 2.11 is FALSE as stated (ω can be stalemated; counterexamples CHECKED-2: kp_p, the referee's own P solver and K16's `pyp.py` agree); the same rule with a no-stalemate clause, Theorem 2.11K, is PROVED in P (one AI proof, read step by step by the referee K16v, who found no gap; not re-derived by a second model), and its checks are CHECKED-2 on the small exhaustive sweeps and COMPUTED-1 on the large ones | R3 item 6; K10; K16 |
>>>>>>> NEW

### EDIT Remark 2.11, proved about real kings
<<<<<<< OLD
- **Proved about real kings: nothing.** Every step above uses (F2). The hypotheses are not enough with real kings:
=======
- **Proved about real kings: Theorem 2.11K below, a square rule with a no-stalemate clause (PROVED in P, one AI proof; revised after K16, 2026-10-27). Before K16: nothing.** Every step of Proposition 2.11 uses (F2). The hypotheses (H1)–(H5) are not enough with real kings:
>>>>>>> NEW

### EDIT Remark 2.11, square-rule conjecture replaced by the K16 outcome
<<<<<<< OLD
- **CONJECTURE (real-king square rule, label kept).** Let β's king be sheltered as in (H2) and the pawn data satisfy
  (H1), (H4), and (H5) with ω's king allowed to move and to capture β's other pawns in G_ω. Let q₀, …, q_d be the
  squares p occupies before its first push and after each push, and n_j = j if s = ω, j − 1 if s = β, the number of
  ω moves before the j-th push. If d(k_ω, q_j) ≥ n_j + 2 for every j (for j = 0 only if s = ω), then β wins P with
  real kings. This follows from d(k_ω, q_d) ≥ d + 2 (s = ω) or d + 1 (s = β) by the triangle inequality. The
  sketch is the proof above with Step 1 replaced by the rule of the square (no capture and no block), but ω could
  steer into a stalemate or a draw by king-and-pawn play, which the sketch does not exclude. Scratch evidence
  only: β = White, `Ka1`, ≤ 2 + 2 pawns, `--pmodel`: cyl:6×6 30,847 legal instances and cyl:7×6 158,840, 0
  violations. The chess form needs (A_Q) at the resulting position (§1.2) and is not claimed.
=======
- **Real-king square rule: the first statement is FALSE (CHECKED-2); with a no-stalemate clause it is PROVED in P (revised after K16, 2026-10-27).**
  - *The former CONJECTURE is false.* It said: let β's king be sheltered as in (H2), let the pawn data satisfy (H1), (H4) and (H5) with
    ω's king allowed to move and to capture β's other pawns in G_ω, let q₀, …, q_d be the squares p occupies before its first push and
    after each push, and n_j = j if s = ω, j − 1 if s = β; if d(k_ω, q_j) ≥ n_j + 2 for every j (j = 0 only if s = ω), then β wins P with real kings.
    It drops (H3) of Proposition 2.11, and with real kings ω can be stalemated, or can walk into a stalemate, which is a draw in P (the Remark's own
    caveat). CHECKED-2 (kp_p `--pmodel`, the referee K16v's own P solver and the pure-Python solver `kings/delegate/out/K16/scripts/pyp.py` agree; the referee's own
    certificate accepts the named pawn in each case): cyl:6×6 `Ka4 ka6 Pa5 Pd5 b -` (β = White, p = d5, Black has no legal move at y itself), flat:6×6
    `Kc1 ka1 Pc2 pa2 w -` (one pawn each, ω's king is shut in by its own pawn and β's king), `Kc1 ka1 Pc2 pa3 w -` (ω steers into the stalemate: c3 pa2 c4) and
    `Kd2 kf1 Pa2 Pf3 pf2 pd3 w -` (stalemate after the first push) are (D, D) although every hypothesis holds. The earlier scratch evidence (`Ka1` only, ≤ 2 + 2 pawns) cannot meet such nets.
    K16's own two implementations of the certificate agree on 15,000 random positions (COMPUTED-1, not re-run by the referee).
  - *Counts (β = White; the flip of ranks and colours gives β = Black, checked on 175,454 positions, COMPUTED-1).* Exhaustive over all kings, both sides to move, e.p. rights,
    COMPUTED-1 (K16's own code; the referee did not re-run these): certified positions and the violating ones (kp_p value not a β win): cyl:6×6 ≤ 4 + 4 pawns 142,434,153 certified, **496 violating**; cyl:6×6 ≤ 3 + 3 19,373,221, 32;
    cyl:7×6 ≤ 3 + 3 117,348,760, 101 (≤ 3 + 2: 26,083,399, 93; ≤ 2 + 2: 3,740,009, 2); cyl:8×6 ≤ 2 + 2 10,378,374, 4; flat:6×6 ≤ 3 + 3 299,322,340, **54,452** (≤ 2 + 2: 11,838,544, 5,490); flat:7×6 ≤ 2 + 2 40,233,315, 9,662.
    The small sweeps were reproduced exactly by the referee with his own enumeration, his own certificate and kp_p (CHECKED-2): flat:6×6 ≤ 1 + 1 156,528 certified, 208 violating (all (D, D)); flat:7×6 ≤ 1 + 1 357,542, 276; flat:6×6 ≤ 2 + 0 171,334, 36;
    cyl:6×6 ≤ 2 + 2 1,072,469, 1 (`Ka4 ka6 Pa5 Pd5 b -`). One pawn in all (1 + 0) never violates (CHECKED-2 on flat:6×6, flat:7×6 and cyl:6×6); 1 + 1 violates on flat boards only (flat:6×6 208, flat:7×6 276 positions, kp_p on every position;
    CHECKED-2), on cylinders from 2 pawns (cyl:6×6 ≤ 2 + 0 has 1; CHECKED-2).
    A strategy simulation (own move generator, checked against `pyp.py`) plays "β pushes p every turn" against all ω lines on every certified instance: its only failures are ω stalemates
    (at y or later) — no capture of p, no block, no earlier ω promotion in any sweep — so a violation can only sit where the simulation shows a stalemate line, and kp_p was run on all of those (COMPUTED-1 for the large sweeps; the referee's own simulation
    reports a stalemate as the only failure on the small ones, CHECKED-2).
    "ω not stalemated at y" is not enough (22 violating instances of the cyl:6×6 ≤ 4 + 4 sweep and 45,566 of the flat:6×6 ≤ 3 + 3 sweep remain; COMPUTED-1).
    The control without king moves in G_ω (variant KV = 2) fails on 153,582 instances of cyl:6×6 ≤ 3 + 3 (ω promotes first; COMPUTED-1, K16's number). The simplest mechanism is that the king steps off its own pawn's path
    and its pawn then promotes: cyl:6×6 `Ka1 ke1 Pc2 pe2 w -` passes every hypothesis under KV = 2 (the king is frozen, so the pawn on e2 never moves) and is (L, L) in P, since Black plays Kd1 and e1=Q before c6 can be reached
    (kp_p, and the referee's certificate accepts it under KV = 2; COMPUTED-1). So (H5) must use the king.
  - ***Theorem 2.11K.* PROVED in P (one AI proof, K16; read step by step by the referee K16v, who found no gap and no counterexample in about 1.1 million exhaustive and 16,500 random checks; not re-derived by a second model; Step 2 is Step 2 of Proposition 2.11, whose proof it quotes).** Notation of Proposition 2.11; Π is "β pushes p at every
    turn (the double step first if ρ(p) = 2)". Assume (H1) (path free of pawns and kings), (H4), (H2) (no pawn of either colour on a file adjacent to β's king's file),
    (H5K) μ^K_ω(y; p) ≥ e + 1, where μ^K_ω is μ_ω in G^K_ω, which is G_ω with ω's king allowed one step per move onto a square that is not an ω pawn, not β's king and not adjacent to it,
    capturing β's other pawns (the variant that also forbids squares attacked by a remaining β pawn is covered too), (SQ) d(k_ω, q_j) ≥ n_j + 2 for j = 0, …, d (j = 0 only if s = ω), and
    (NS) in no play of Π is ω stalemated at one of its turns (a search of depth ≤ e over ω's replies); (NS) follows from (H3K): every square x with d(x, k_ω) ≤ e − 1 has a king-neighbour t with
    d(t, k_β) ≥ 2 and no pawn of either colour on the files of t, t − 1, t + 1. Then β wins P from (y, s) by Π.
    *Proof.* (F1) a pawn changes file only by a capture, landing on the captured pawn's square (e.p.: on the captured pawn's file); a king capture only removes a pawn; so a pawn enters a file only by
    capturing a pawn on it and a file without pawns never gets one. (F2) the first promotion ends P with a win for its maker. (F3) under Π only p moves.
    *Step 1.* By (H2) and (F1) no pawn ever stands on a file adjacent to β's king, so no ω pawn attacks it, and ω's king is never adjacent to it: β is never in check and no push exposes β's king.
    *Step 2.* Exactly Step 2 of Proposition 2.11, proved by induction on the plies of the play (Steps 2 and 3 use each other: Step 2 assumes that p is still on the board, Step 3 shows that ω's king never takes it; the induction runs over the plies, and at each ply both statements hold for the earlier plies):
    (J_β) at β's turns every ω pawn in the strip f − 1, f, f + 1 has ρ ≤ ρ_p + 1; (J_ω) at ω's turns it has ρ ≤ ρ_p and p cannot be taken e.p.; (I1) no pawn stands ahead of p on its file.
    The proof uses only pawn moves, (H1), (H4) and (F1)–(F3); king captures remove β pawns and add none, so every bound on a landing rank can only drop. Hence no ω pawn captures p or lands ahead of it.
    *Step 3.* After β's j-th push p stands on q_j and ω has made n_j moves, its king at distance ≤ n_j from k_ω; to capture p it needs distance ≤ 1, i.e. d(k_ω, q_j) ≤ n_j + 1, against (SQ) (for j = 0, s = ω, no move has been made and d(k_ω, q₀) ≥ 2).
    Before the (j + 1)-th push ω has made n_{j+1} moves, so its king is on q_{j+1} only if d(k_ω, q_{j+1}) ≤ n_{j+1}, against (SQ); the square skipped by the double step is adjacent to q₁ and at distance ≥ n₁ + 1. β's king is not on the path (H1).
    With Step 2 every push of Π is legal.
    *Step 4.* β always has the push; by (NS) ω has a legal move (or is mated, a win for β) at each turn.
    *Step 5.* Every ω move before β's promoting push is a move of G^K_ω from y (pawn moves: the squares empty in the play are empty in G_ω, where p is deleted, captured pawns are β pawns other than p, the only e.p. capture is the one offered at y;
    king moves: a legal king step goes to a square that is not an ω pawn, not β's king, not adjacent to it, and captures a β pawn other than p). Before β's d-th push ω has made exactly e moves, and (H5K) says that none of the e-move plays of G^K_ω puts an ω pawn on its last rank.
    So ω does not promote first, and the d-th push promotes: β wins by (F2).
    *(H3K) ⟹ (NS).* At ω's m-th turn (m ≤ e) its king stands on some x with d(x, k_ω) ≤ m − 1 ≤ e − 1. For the t of (H3K), the three files around t hold no pawn, hence (F1) never do: t is never occupied by or attacked by a pawn, t is not β's king and not adjacent to it, so the step x → t is legal even in check. ∎
    Computational counterpart (COMPUTED-1): on every certified instance of every sweep (H3K) implies (NS) (0 exceptions among about 7.6 · 10⁸ instances, the five top sweeps; the nested sweeps are not added), and (NS) leaves 0 violations, kp_p and the simulation agreeing on all instances solved by both.
    These are checks of the proved implication and of the theorem, not part of the proof. The referee's own samples agree (COMPUTED-1: 16,500 random positions on six boards, and all 1,072,467 certified positions of cyl:6×6 ≤ 2 + 2 without a stalemate line are (W, W) in kp_p; 0 exceptions).
  - *CONJECTURE′ (evidence only).* Replace (NS) by (H3) of Proposition 2.11 at ω's own king: k_ω has a neighbouring square t, not adjacent to β's king, with no pawn on the files of t, t − 1, t + 1. 0 violations in all sweeps and hunts, but in 565
    cases (172 instances in the exhaustive sweeps, 393 positions in random hunts; COMPUTED-1) ω has a line that stalemates Π and β still wins by another move (kp_p), so Theorem 2.11K does not cover them and a proof needs another strategy for β.
    The 172 are 134 (flat:6×6 ≤ 3 + 3) + 36 (flat:7×6 ≤ 2 + 2) + 2 (cyl:8×6 ≤ 2 + 2); the flat:6×6 ≤ 2 + 2 sweep (8 instances) is nested in the ≤ 3 + 3 one and is not added again (revised after K16v, 2026-10-27).
  - The chess form needs (A_Q) at the resulting position (§1.2) and is not claimed. Data, scripts and counts: `kings/delegate/out/K16/` (`logs/`, `scripts/`).
>>>>>>> NEW

### EDIT Remark 2.11, P11 bullet
<<<<<<< OLD
- P11 in §6 relies on Proposition 2.11 in the sense given there (revised after K10, 2026-10-22).
=======
- P11 in §6 relies on Proposition 2.11 in the sense given there (revised after K10, 2026-10-22). P11 is a frozen-model statement (`--frozen`); it does not use Theorem 2.11K, which is about P with real kings, and Theorem 2.11K does not change P11 (revised after K16, 2026-10-27).
>>>>>>> NEW

### EDIT R3 item 1, certificate with real kings
<<<<<<< OLD
     with real kings only the square-rule CONJECTURE of Remark 2.11 applies (revised after K10, 2026-10-22).
=======
     with real kings the square-rule conjecture of Remark 2.11 is FALSE as stated (ω can be stalemated; CHECKED-2), and Theorem 2.11K (PROVED in P: the same rule with a no-stalemate clause) applies where its hypotheses hold (revised after K16, 2026-10-27).
>>>>>>> NEW

### EDIT R3 item 5, king that catches a passer
<<<<<<< OLD
   - Proposition 2.11 is proved only with frozen kings. With real kings the defender's king may catch the
     passer (`Ka1 ka6 Pc2 w -` is (W, W) frozen and (D, D) with real kings); the real-king form is the square-rule
     CONJECTURE of Remark 2.11 (revised after K10, 2026-10-22).
=======
   - Proposition 2.11 is proved only with frozen kings. With real kings the defender's king may catch the
     passer (`Ka1 ka6 Pc2 w -` is (W, W) frozen and (D, D) with real kings); the real-king form is Theorem 2.11K of
     Remark 2.11 (the square rule with a no-stalemate clause, PROVED in P; without the clause the rule is FALSE, CHECKED-2, K16) (revised after K16, 2026-10-27).
>>>>>>> NEW
