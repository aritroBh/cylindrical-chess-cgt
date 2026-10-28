# EDITS_FINAL for K18 (fix round, 2026-10-28)

Integrator notes (this prose is outside the EDIT blocks, which are the only part `apply_edits.py` reads).

* Three blocks: the section 8 open question 1 heading, the section 8 body (replacing the two "untested" bullets), and Appendix A.
  All three OLD texts occur exactly once in the current LOOPY.md, which already contains the K14, K16, K19, K20-K24 and K27 edits
  (commits 432907a and bbb8356). The blocks do not overlap. Apply them in any order.
* Referee fixes made: flat 6x6 is an unmerged root count, 1,695 (1,829); "about half" (487 of 953) replaces "usually"; totals
  2,305 legal, 2,263 punished, 42 not punished; the mechanism sentence is gone (nothing is claimed; the king-captures-the-pawn
  guess stays as a CONJECTURE); Proposition 8.1 is repaired in full (new hypothesis (P1e), proof rewritten for the e.p. lapse);
  the counterexample and the budget values k = 1..6 are CHECKED-2; E1 and the 681 un-rerun E3 cases and the chess runs stay
  COMPUTED-1; the answer to open question 1 is "false as worded in P, held in every test where the context cannot be won by a pawn
  race or capture", with the boundary written out.
* Not done here, by rule (only this file is written): `kings/delegate/out/K18/summary.json` still says "punished": 2233; it should
  read 2263 (and 2,305 legal). The note's own text uses the corrected numbers.
* If the integrator prefers not to rely on the repaired proof of Proposition 8.1 (one derivation, not read by a second reviewer),
  change "PROVED after repair" in its heading and in the first block to "CONJECTURE"; the evidence paragraph beside it stands on
  its own.

### EDIT section 8 open question 1 heading (K18)
<<<<<<< OLD
1. **Tempo matching** (CONJECTURE). Suppose a group's punishment wins only in the plain local game, not
=======
1. **Tempo matching** (false as worded in P; a promotion-free form is a CONJECTURE; revised after K18, 2026-10-27, see the verdict
   below). Suppose a group's punishment wins only in the plain local game, not
>>>>>>> NEW

### EDIT section 8 open question 1 (K18)
<<<<<<< OLD
   - The question is untested. Every trébuchet placement checked on the 7×6 cylinder satisfied (L1) for every
     budget k ≤ 4 and for k = ∞ (the local game before K7; Definition 2.6 now has k = ∞ only; revised after K7,
     2026-10-22).
   - The only plain-but-not-passing wins found are Z_on's sorties Kd4 and Kd5 (§5.5). Z_on also has an
     outright escape, Kc5, so it cannot test the question.
=======
   - **K18 tested the question (2026-10-27; scripts, logs and `summary.json` in `kings/delegate/out/K18/`; referee report
     `kings/delegate/out/K18/VERIFY.md`, with the referee's own code and logs in `kings/delegate/out/K18/verify/`; AI work, no human
     re-derivation; revised after K18, 2026-10-27).** Model P (first promotion wins, real kings), `cyl:7×6` and `cyl:8×6`,
     F_Z = {a, b, c}, s = White (Black sorties are colour-flipped), unless stated. *Plain* is the local game of Definition 2.6 with
     no passes for s (a stalemate of s is then a failure for s̄); *pass* is Definition 2.6 as it stands (k = ∞); *budget k* gives s
     at most k passes. A *plain-only sortie* is a White move m at a root Y such that some admissible reply r wins the plain game
     and no admissible reply wins the pass game. An *outright escape* is a White move at Y that neither game punishes and that no
     immediate promotion by s̄ punishes. A context G is *promotion-free* if no sequence of legal pawn moves of the context alone
     (both colours, any order, captures and e.p. captures included) promotes, so the context holds no pawn race. Result: the
     question can be tested; the conjecture is **false as worded** (explicit counterexamples below, CHECKED-2); a promotion-free
     form is supported by every test (no counterexample; CONJECTURE); and a form with extra hypotheses is **PROVED after repair**
     as Proposition 8.1 below (one added hypothesis, (P1e)), but its hypotheses hold in none of the tests.
     - **Groups with a plain-only sortie and no outright escape exist in large numbers (CHECKED-2).** Solver: `scripts/lg.cpp`
       (dense retrograde tables over all pawn configurations with ≤ 2 + 2 or ≤ 3 + 2 pawns on F_Z at ranks 2 to H − 1, all king
       placements, e.p. rights carried exactly; budgets k = 0, …, 6 and ∞; the queen clause as a switch), written from Definition 2.6
       and `kings/SPEC.md`. Second implementation, written separately by K18: `scripts/lg2.py` (explicit reachable graph and fixed
       point) and `scripts/lg2k.py` (budgets). Third implementation, written by the referee from Definition 2.6 and the K18 text
       (`verify/mine/mylg.cpp`, which read `lg.cpp` only for the passer rule and the output format). `lg.cpp` and the referee's
       solver give the same output on every line of the 32,539-line search of `cyl:8×6`, 3 files, ≤ 2 + 2 pawns (every root, every
       sortie class, every T, every escape count; 0 lines on one side only), the same totals for the other searches below, and the
       same budget vectors k = 0, …, 6 for all 941 classes. K18's `lg2.py` and `lg.cpp` agree on 140 random positions (80 on
       `cyl:8×6`, 60 on `cyl:7×6`, 40 of them with an e.p. right, 42 with a finite value; 0 mismatches; the referee did not re-run
       this one), and K18's cross-check of the budget values with `lg2k.py` was cut off by machine load after 1 of 60 values (no
       mismatch). Both K18 solvers give the (L1) list T = 6, 6, 6, 7, 7 and the (L1_P) list 6, 6, 5, 6, 6 of §5.1 after Kxa4, and
       the facts of §5.5 (mirrored to a White sortie: Kd3 and Kd2 are plain-only with T = 6, Kd4 is won in both games with T = 5,
       Kc2 in neither; the referee reproduced these on the root `Kc3 Pb4 ka3 pb5`). The search lists, for every root Y with both kings on F_Z,
       White to move, no passer by the root rule of Appendix A and no immediate promotion for White, every White move and the least
       T over the admissible replies in each game (no sortie of the search has an immediate promotion reply, so the difference
       between the text's definition of plain-only and the code's is empty). Mirror classes of roots with at least one plain-only
       sortie and no outright escape (queen clause; without it): `cyl:8×6`, 3 files, ≤ 2 + 2 pawns: 941 (1257); `cyl:7×6` the same,
       941 (1257); `cyl:8×6`, 4 files: 6602 (6864); `cyl:7×6`, 4 files: 6598 (6860); 3 files, ≤ 3 + 2 pawns: 1075 and 1075 (1391
       and 1390). On a cylinder the reflection of the files a to c is a symmetry, and the referee checked that every candidate root
       has its mirror partner with the same flag. On `flat:6×6`, 3 files, ≤ 2 + 2 pawns, the reflection is not a symmetry (F_Z has
       the board edge on one side and the buffer on the other), so there is no class count: 1,695 (1,829) roots with a plain-only
       sortie and no outright escape, not merged (K18's earlier "960 (1056)" was a merge that is not valid there). On `cyl:8×6` with 3 files
       and the queen clause the 941 groups have 1372 plain-only king sorties (and 492 plain-only pawn sorties); 19 of the groups have
       one pawn a side. So Z_on's escape Kc5 was not essential: the question has non-degenerate test cases. Reproduce:
       `bin/lg --board cyl:8x6 --fz 0:3 --maxw 2 --maxb 2 --kmax 6 --search` (`c++ -O2 -std=c++17 -o bin/lg scripts/lg.cpp`), then
       `scripts/parse_search.py`.
     - **The local game is a lower bound of the real one (CHECKED-2: the local solver and the full-board P solvers agree).** For the
       232,343 distinct positions after a White move at those roots (`cyl:8×6`, 3 files, ≤ 2 + 2): whenever the plain local game is
       won, `kpsolve --pmodel` (K7's `kp_p.c`) says Black wins P: 108,710 of 108,710 (queen-clause version 100,625 of 100,625); for
       the pass game 95,658 of 95,666, and in the 8 exceptions Black does not win in P (all Black moves there are draws in P; White
       being stalemated is the expected cause, not traced; the pass game cannot stalemate s). The referee re-ran all 232,343
       positions with K23's independent P-solver `ref3` and got exactly these numbers. All 4,593 punished White moves of the 941
       groups (1,864 plain-only, 2,726 punished in both games, 3 only with passes: two of them also Black wins in P, one drawn)
       are Black wins in bare P except that one draw (the referee reproduced the four classes exactly). Reproduce:
       `scripts/bare_noesc.py`, `scripts/cmp_bare.py`.
     - **Most plain-only sorties are not tempo-sensitive (CHECKED-2; the budget vectors k = 1, …, 6 come from `lg.cpp` and agree with
       the referee's solver for all 941 classes).** The failure at k = ∞ only says that s can pass forever. Of the 1372 plain-only
       king sorties, 953 are won for every budget k ≤ 6 (in about half of them, 487 of 953, with T_k = T_0 + k: s̄ absorbs each
       pass with one extra move; the others have increments such as 2, 0, 2, 0, 2, 0 or 2, 1, 1, 1, 1, 1); 327 are won only for
       k = 0; 61 are won for a prefix k ≤ 1, …, 4; 27 have a parity pattern (won for even k only, 15, or for k = 0 and odd k,
       12); 4 are other. A real context gives s only finitely many spare moves, so for a sortie of the first kind the budget game
       rather than the k = ∞ game is the relevant one (the point of (L2) with T_k, and of Proposition 8.1 below; that this
       carries over to contexts is not shown here); the other 419 (1372 − 953) are the cases that depend on the budget.
     - **Context experiments (`scripts/ctx_exp2.py`, `kpp --pmodel --cap 0`; labels per item below).** Contexts G: pawns of both
       colours on the context files e, f, g (`cyl:8×6`: all 4160 with at most 2 + 2 pawns and a legal pawn move for each side) or e,
       f (`cyl:7×6`: 716). The class of G is its `kpsolve --frozen` value with the kings on a1 and c6, (White to move, Black to move):
       zero = (L, W), negative = (L, L), positive = (W, W), fuzzy = (W, L). "Second-player win for the punisher" means zero or
       negative. Tempo matching predicts that Y·m + G, Black to move, is a Black win for these classes. A sortie is *illegal*
       beside G if a context pawn attacks its square (such cases are not counted). Tested: (ES) the 25 plain-only king sorties of
       the 19 groups with one pawn a side against 125 contexts (all 123 with one pawn a side, and the two zero contexts with 1 + 2
       and 2 + 1 pawns); (ES7) the same on `cyl:7×6` (25 sorties, 59 contexts); (E3) 6 of 12 planned sorties of the stratified sample
       (the other six were not finished), 2 + 2 and 1 + 2 groups, with k* from 0 to 6, against 159 contexts (all 59 zero, 60
       negative, 20 positive, 20 fuzzy of the `cyl:8×6` family). The 4160 contexts, their classes and their promotion-free subset
       (below) are CHECKED-2: the referee's own enumerator gives 4160 contexts, 1633 fuzzy, 1234 negative, 59 zero, 1234 positive,
       and 716 contexts on `cyl:7×6`. Reproduce: `scripts/contexts.py cyl:8x6 4,5,6 2 2 logs/ctx8x6_efg_22`, `bin/kp --board cyl:8x6
       --frozen --ep on --promote Q --cap 0 < logs/ctx8x6_efg_22_frozen_in.txt`, `scripts/select_k.py`, `scripts/ctx_exp2.py make
       cyl:8x6 <contexts> <sorties.json> <dir>`, `bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 < <dir>/in_i.txt`,
       `scripts/ctx_exp2.py collect …`, `scripts/analyze_E.py <dir> <sorties.json>`.
       - **Counterexamples to the unrestricted conjecture (CHECKED-2, exact: both bounds agree).** In 42 of the 2,305 legal
         sortie–context cases with a zero or negative context in these three runs (ES 1,017, ES7 601, E3 687) the sortie is not
         punished (29, 7 and 6 cases); in the other 2,263 it is (CHECKED-2 for the ES and ES7 cases, COMPUTED-1 for the 681 E3 cases that were not
         re-run). All 42 failures are CHECKED-2: the referee rebuilt the ES and ES7
         tables cell by cell with its own code and its own contexts and sorties (ES, zero contexts: 7 draws, 235 Black wins, 7 White
         wins, 1 illegal; negative: 2, 753, 13 and 32 illegal), and confirmed each of the six E3 failures as a White win in P with
         `ref3`. The other 681 legal E3 cases are as K18 reported (COMPUTED-1: the referee did not re-run them, `ref3` needs more
         than a minute of CPU per sortie there). The smallest counterexample, CHECKED-2: Y = `Ka1 Pa2 kc1 pa3`, m = Ka1–h1
         (plain-only, T = 4), context G = `Pe2 Pg2 pf4` (frozen value zero). `Ka1 kc6 Pe2 Pg2 pf4 w -` is a Black win and `… b -` a
         White win in `--frozen`, but `Kh1 Pa2 kc1 pa3 Pe2 Pg2 pf4 b -` is a White win in P (exact; all six Black moves lose), and
         `Ka1 Pa2 kc1 pa3 Pe2 Pg2 pf4 w -` is a White win in P, so beside this zero the group is not 0 (K7's `kpp` and the independent
         solver `ref3` agree; the bare group `Ka1 Pa2 kc1 pa3 w -` is a Black win). The same for the negative context `Pe2 pg3` (a
         race). Reproduce: `bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 --moves < logs/cx_small.txt` (5.5 s;
         output in `logs/cx_small_out.txt`). **Chess** (COMPUTED-1: `kpsolve --cap 1 --promote Q`, exact bounds A ≥ value ≥ B from
         White's side; `bin/kp --board cyl:8x6 --ep on --promote Q --cap 1 < logs/C2_in.txt`, 586 s; the referee recounted the log
         and did not re-run it): for 29 non-punished sorties of ES the lower bound B is D or W in 20, so Black cannot win chess
         either (this includes the two examples above); in 3 Black wins chess exactly (P and chess differ); 6 are undecided (bounds
         W or D against L). The 12 controls (punished in P): 11 Black wins in chess exactly, 1 undecided. None of the 35 failures of ES and E3 has a
         promotion-free context (the referee checked ES; in E3 each failing context holds a pawn that can walk to promotion, and
         the promotion-free contexts of E3 were all punished); the context sets of the 7 failures of ES7 were not checked for
         this. In the 35 failures checked for it (the 29 of ES and the 6 of E3; the 7 of ES7 were not checked) the sortie
         king stands within 2 steps of a context pawn after m, while T ≥ 4. No mechanism is claimed. A guess is that the king
         captures the pawn that makes G a second-player win (CONJECTURE; not traced move by move).
       - **Promotion-free matched contexts: no counterexample (CONJECTURE; 123 of 292 cases CHECKED-2, the rest COMPUTED-1).** Of the
         4160 contexts only 5 zero and 45 fuzzy ones are promotion-free (shared one-move gaps such as `Pe2 Pg2 pe4 pg4`, whose value
         is * + * = 0); no negative or positive one is. All 153 legal cases with these shared-gap contexts are punished (25 sorties
         of the one-pawn groups against the 5 zero contexts, 123 legal; the 5 contexts against the 6 E3 sorties, 30 legal), and so are
         139 cases with the reservoir contexts described next in which s has no more spare moves than s̄: 292 of 292 in all. The
         referee reproduced the 123 cases of the first kind (125 pairs, 2 illegal, 123 Black wins) with its own code. The 30 E3 cases
         and the 139 reservoir cases are as K18 reported (COMPUTED-1; the referee did not re-run them, and rebuilt none of the
         reservoir runs). The reservoir contexts are the blocked modules `Pe2 Pe4 pe5` (one private spare move for White, file e or g)
         and `Pe2 pe5 pe3` (one for Black), combined on the files e and g so that s has a spare moves and s̄ has b (31 of 32 sorties,
         8 contexts each, 248 pairs of which 18 illegal: Δ = a − b ∈ {−2, −1, 0, 1, 2}). Here the refined prediction is: punished iff
         Δ ≤ 0 or the P-variant local game with Δ passes is won. Δ ≤ 0: 139 of 139 punished. Δ > 0 predicted punished: 60 of 60
         punished. Δ > 0 predicted not punished: 7 not punished (draw or White win, as predicted), 24 punished anyway; these are not
         contradictions, because the local game confines s̄'s king to F_Z and the real s̄ may raid the reservoir. The harness
         therefore has power.
     - **Verdict on open question 1 (revised after K18, 2026-10-27).** (a) **Tempo matching is false as worded in P** (CHECKED-2).
       A context can be a second-player win for the punisher in the frozen convention and a plain-only sortie still wins: 42
       failures in 2,305 legal cases, the smallest above; in chess too for 20 of the 29 cases of ES, where Black cannot win
       (COMPUTED-1). The counterexamples refute the conjecture as worded; they do not refute Theorem 2.7, which needs (L2) and (L3)
       and which the wording of the question does not assume. (b) **It held in every test in which the context contains no pawn race
       or capture sequence that promotes** (promotion-free contexts, as defined above): 0 failures in 292 cases, with or without a
       surplus for s̄ (CONJECTURE; 123 of the 292 cases CHECKED-2). The exact boundary: the 292 cases are the 5 promotion-free zero
       contexts of the 4160 against the 25 + 6 sorties (153 legal cases) and the reservoir contexts (139 cases with Δ ≤ 0); the family
       has no promotion-free negative or positive context, so nothing is tested for those; the sorties are plain-only king sorties of
       the groups above. The 35 failures of ES and E3 have a context in which some sequence of pawn moves promotes (the 7 of ES7 were
       not checked); the converse is not claimed (many contexts that are not promotion-free are punished). The only evidence
       about the sortie king is that in the 35 failures checked it stood within 2 steps of a context pawn after m. (c) With the
       hypotheses of Proposition 8.1 it is a theorem, but those hypotheses are very restrictive: in none of the tested cases does it
       hold. (P3) (called P4 in `scripts/p4_check.py`) fails in all 1,827 matched sortie–context pairs on `cyl:8×6` (ES 1,017, EP
       123, E3 687) and in all 256 pairs of the 32 reservoir-test sorties with the 8 reservoir contexts (legal or not; results exist for 31 of
       the 32 sorties; `scripts/p4_check.py`, with R from
       `scripts/analysis_R.py`; the sortie king can reach the context files within T ≥ 3 moves). There R is the union over the
       fastest winning strategies of s̄. The referee tested the strong form on ES: in the local game in which s's king may never step
       on a square of X or of its king-neighbourhood (X as in (P2): every sequence of pawn moves without promotion), s̄ cannot win at
       all, for any T, in any of the 1,050 zero or negative ES pairs (legal or not), while the same 24 positions after m are won
       with T = 4 to 7 without the restriction. So in ES (P3) fails for every strategy of s̄, not only for the fastest ones
       (CHECKED-2; for EP, E3 and the reservoir pairs only the union form was tested). It is a proved sufficient condition, not the
       explanation of the data. (d) The k = ∞ criterion is too strong for finite contexts: 953 of the 1372 plain-only king sorties
       are won for every budget tried (CHECKED-2).
       Boundary: ≤ 2 + 2 pawns (≤ 3 + 2 in the group search only) on 3 or 4 files of `cyl:7×6` and `cyl:8×6` (and `flat:6×6` for the
       group search, root counts only), contexts of at most 2 + 2 pawns on the context files (at most 3 pawns for the modules), model
       P; chess was run only for the 41 positions above (a promotion in chess is not an immediate win), and not for the
       promotion-free tests. The reservoir (E1) runs, the E3 cases other than the six failures, and the chess runs were not
       re-run by the referee.
     - **Proposition 8.1 (tempo pairing). PROVED after repair (one derivation, K18; the e.p. step was repaired after the K18 referee found a
       gap in the first proof, and the repair has not been read by a second reviewer; revised after K18, 2026-10-27).** Let Q (s to
       move) be as in Theorem 2.7(b), with no e.p. right at Q, context G on the context files. Assume:
       - (P1) s̄ has a winning strategy σ in the plain local game L_T^0(Q_Z) (s may not pass; stalemate of s is a failure for s̄;
         the (L1_P) version is enough for P);
       - (P1e) no s-to-move position of a line of L_T^0(Q_Z) in which s̄ plays σ carries an e.p. right and has only e.p.
         captures as legal moves for s (this holds, for example, when no s-to-move position of the game is of that kind; the
         referee found none with ≤ 2 + 2 pawns on 3 files of `cyl:8×6` and 36 with ≤ 3 + 3 pawns, for example `Kb1 Pc3 kc4 pb2 pa3
         pb3 w b4`; it is a real condition for the larger games, because without it the proof has a gap);
       - (P2) there is a set 𝒢 of context positions with s to move that contains the context of Q, contains no promotion move in
         its play (neither side promotes in any play of 𝒢 under the pairing below), and is closed under pairing: after any legal
         context-pawn move of s from a position of 𝒢 (e.p. captures included) s̄ has a legal context-pawn move to a position of 𝒢.
         (𝒢 = the positions at which s̄ wins the frozen game with s to move, when G is promotion-free.) Let X be the set of squares
         on which a context pawn stands in some position of 𝒢-play;
       - (P3) let R be the set of squares on which s's king can stand in lines of L_T^0(Q_Z) where s̄ plays σ; then R contains no
         square of X or of its king-neighbourhood.
       Then s̄ wins P from Q.
       - *Proof.* A position of 𝒢 may carry an e.p. right (created by s̄'s last pairing move). Adding to 𝒢 the same position without the
         right keeps (P2): the moves of s from it are among the moves of s from the position with the right, the same pairing reply
         works, and no promotion is added. So 𝒢 is closed under deleting a pending context right; assume this. s̄ plays: to a local
         move of s (a king move or a Z-pawn move) the reply of σ, read on the play of L_T^0(Q_Z) obtained by deleting all context
         pairs (a context move of s with its pairing reply); to a context-pawn move of s the pairing reply of (P2). Only one e.p. right
         can be pending at a time. A right created by s̄'s σ-reply lies on F_Z; a right created by a pairing reply lies on a
         context file. s's next move clears it, whichever it is. A right created by s concerns s̄'s reply, which is a σ-move made at once.
         - *The deleted play is a play of L_T^0(Q_Z) in which s̄ follows σ.* A context pair changes only the context and the side
           to move twice. Let s be to move at a real position S, and let P be the position of the deleted play at that point. The
           local part of S is P itself, except that P carries a pending Z-right and S does not when a context pair has come since
           s̄'s last σ-reply; write P° for the local part of S (P° is P, or P without its right). The kings and the Z-pawns are the
           same in S, P and P°. (i) A legal real move of s is a legal move in P°, by the argument of Step 1 of Theorem 2.7 (the
           context pawns of S add restrictions only, and a context pawn never attacks s's king by (P3)); and a legal move in P°
           is a legal move in P, because P has all the moves of P° and possibly an e.p. capture more. So the deleted play is a legal
           play of L_T^0(Q_Z), and s̄ answers by σ. (ii) Conversely, a legal move of s in P that is not an e.p. capture of a missing
           right is a legal real move: a Z-pawn move involves squares of F_Z only, which hold the same pieces in S and P; a king move
           goes to a square of the set R of (P3) (it is a move of s in a line of σ), which is neither occupied nor attacked by a
           context pawn. The result is the same local position. (iii) s̄'s reply by σ is a legal real move: F_Z holds the same pieces
           in the real and the local position, no context pawn attacks F_Z, and a pending right created by s on F_Z is answered at once
           (Steps 2 and 3 of Theorem 2.7).
         - *s is never stalemated, and a mate in the projection is a mate in the real game.* At a real s-turn that follows a σ-reply, S
           is P, and s has a legal move there, because σ wins the plain game, in which a stalemate of s is a failure for s̄; by (ii) the
           move is legal in the real game (it is not an e.p. capture of a missing right, because no right is missing). At a real s-turn
           that follows a pairing reply, s was not in check before its context move (a context move is not allowed in check) and
           no context move gives check, so s is not in check at P°. P has a legal move for s, and by (P1e) one that is not an e.p.
           capture; by (ii) that move is legal in S. So (L3) and (L3_F) do not have to be assumed. A mate in the projection arises right
           after a σ-reply, where S is P; it is a mate in the real game, because a context pawn never attacks s's king (by (P3) the king
           stays outside the king-neighbourhood of X), and the real legal moves of s are local moves or context moves, which are not
           allowed in check.
         - *Pairing replies exist and are legal.* The context pawns move on squares of X, which by (P3) are never occupied by s's king
           (the square passed over in a double step is next to a square of X, so it is not occupied either). s̄'s king stays on F_Z
           (a buffer file separates it from the context), and a context pawn move gives no check to a king on F_Z (Lemma 2.2); s̄'s
           king is not in check when s has just made a context move (s's context move was legal, and no context pawn attacks F_Z). A
           real context move of s is a move of the abstract pawn game (the king stands outside X), so it is covered by (P2). No
           promotion occurs in the context: none in 𝒢-play, and s's king cannot capture or block a context pawn by (P3).
         - *End of the play.* The number of context pairs is finite (pawns only advance or are captured, and none promotes), the
           number of local moves of s before s̄'s win is at most T, so the play ends. The deleted play ends within T moves of s̄ by a
           promotion by s̄ (a legal real move, which wins P) or a mate of s. ∎
       - *What it does not say.* (P3) is a hypothesis on the sortie king; without it the statement is false (the counterexamples
         above). (P2) can be certified by `kpsolve --frozen` (zero or negative) and a search for promotions. (P1e) is a finite check
         on the positions of the winning lines. The referee added the option "s may let a pending e.p. right lapse" to its solver
         (a move of s to the same position without the right, s to move again) and compared the plain game with and without it on every
         e.p.-free state with ≤ 3 + 3 pawns on 3 files of `cyl:8×6` (5,293,277 won states): the won states and every T are identical
         (COMPUTED-1, one implementation). So (P1e) may be unnecessary, but that is not shown here.
       - A finite-budget form (s has at most k more spare moves than s̄, and s̄ wins the local game with k passes) is the natural
         generalisation; it is a CONJECTURE here, supported by the 60 reservoir cases with Δ > 0 that it predicts punished (all
         punished; COMPUTED-1, not re-run by the referee).
>>>>>>> NEW

### EDIT appendix A K18 (K18)
<<<<<<< OLD
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
=======
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
- **K18 re-computation (2026-10-27; scripts, logs and `summary.json` in `kings/delegate/out/K18/`, the referee's code and logs in
  `kings/delegate/out/K18/verify/`, the referee's report in `kings/delegate/out/K18/VERIFY.md`; revised after K18, 2026-10-27).** For open
  question 1. New implementations, written from Definition 2.6 and `kings/SPEC.md`: `scripts/lg.cpp` (the local game of
  Definition 2.6, all pawn configurations of ≤ 2 + 2 or ≤ 3 + 2 pawns on F_Z at once, pass budgets 0 to 6 and ∞, queen clause and
  the mate rule as in K7), `scripts/lg2.py` and `scripts/lg2k.py` (a second, independent solver, with budgets). They agree with §5.1,
  §5.5 and with each other (140 random positions, 0 mismatches). The full-board checks use private builds of `kings/kpsolve.c` and
  of K7's `kp_p.c` (`--pmodel`): the plain local game is a lower bound of bare P at 108,710 of 108,710 positions. The referee wrote
  a third local-game solver (`verify/mine/mylg.cpp`) and reproduced the search outputs line by line, the budget classes, the 232,343
  full-board checks (with K23's `ref3`), the context counts of ES, ES7 and EP, the six E3 failures and the headline counterexample.
  The referee did not re-run the reservoir (E1) runs, the other 681 legal E3 cases or the chess runs. The referee found three
  statements to correct (the `flat:6×6` class count, the total 2,305, the word "usually") and a gap in the first proof of
  Proposition 8.1 (an e.p. right that s lets lapse); all are corrected in §8. The group search, the finite-budget classes, the
  context experiments and Proposition 8.1 are recorded in §8, open question 1.
  One bug found on the way (fixed, all numbers above are after the fix): a configuration in which a White and a Black pawn
  share a square was treated as a root; the bare P check (`X`, illegal) exposed it.
>>>>>>> NEW
