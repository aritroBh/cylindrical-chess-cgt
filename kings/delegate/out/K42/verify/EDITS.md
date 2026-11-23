# K42 edits for kings/theory/LOOPY.md (§8 open question 1, and a status-table row), revised by the K42 referee
# (replacement set for kings/delegate/out/K42/EDITS.md; labels updated after verification, see kings/delegate/out/K42/VERIFY.md)

### EDIT 1 heading of open question 1 (K42, 2026-11-22)
<<<<<<< OLD
1. **Tempo matching** (false as worded in P; a promotion-free form is a CONJECTURE; revised after K18, 2026-10-27, see the verdict
   below).
=======
1. **Tempo matching** (false as worded in P; the promotion-free form is false too (K42, 2026-11-22), and every failure found uses
   the sortie king; a proved form for promotion-free contexts is Proposition 8.1′; revised after K18, 2026-10-27, and after K42,
   2026-11-22, see the verdict and the K42 item below).
>>>>>>> NEW

### EDIT 2 verdict (b) (K42, 2026-11-22)
<<<<<<< OLD
(b) **It held in every promotion-free test that was run** (contexts with no pawn race or capture sequence that
       promotes, as defined above):
=======
(b) **It held in every promotion-free test that K18 ran, and it is false in general (K42, 2026-11-22: counterexamples
       in every promotion-free context class tested, K18's family included; CHECKED-2, three P solvers; see the K42 item below)** (contexts with no
       pawn race or capture sequence that promotes, as defined above). K18's tests:
>>>>>>> NEW

### EDIT 3 the promotion-free bullet (K42, 2026-11-22)
<<<<<<< OLD
       - **Promotion-free matched contexts: no counterexample (CONJECTURE; 123 of 292 cases CHECKED-2, the rest COMPUTED-1).** Of the
=======
       - **Promotion-free matched contexts: no counterexample in K18's 292 cases (123 of them CHECKED-2, the rest COMPUTED-1); the
         promotion-free form is nevertheless false (K42, 2026-11-22, below): K18's sorties were 31 plain-only king sorties of
         small groups, and none of them fails against these contexts.** Of the
>>>>>>> NEW

### EDIT 4 the K42 item, after Proposition 8.1 (K42, 2026-11-22)
<<<<<<< OLD
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder?
=======
   - **K42: the promotion-free form settled (2026-11-22; `kings/delegate/out/K42/`: `findings.txt`, `PROOF.md`, code in `src/`,
     logs in `logs/`; referee report `kings/delegate/out/K42/VERIFY.md`, with the referee's own code in `verify/`; AI work, no human
     re-derivation).**
     - *Statement tested (PF-TM).* Root Y as in K18 (group on F_Z = {a, b, c}, s = White to move, no e.p. right); m a legal
       non-promoting Z-move after which s̄ has no immediate promotion, plain-only in the sense of K18 ((L1_P) form; the queen-clause
       form recorded too); G a promotion-free context (K18's definition: pawn moves of G alone, any order) of at most 2 + 2 pawns on
       the context files in which s to move loses the pawn game (normal play, e.p. included; for a promotion-free G this is the zero
       or negative class of `--frozen`). Claim: Y·m + G, s̄ to move, is an s̄ win in P. The reading of "each defender tempo answered by
       a punisher tempo": s̄ answers a context move of s by a context move inside the lost-for-s positions, and a local move by σ.
     - *Result: PF-TM is FALSE (CHECKED-2).* K42's own solver (`src/k42.cpp`, written from `kings/SPEC.md` and Definition 2.6) tested
       every plain-only sortie of every root with at most 2 + 2 Z-pawns (cyl:7×6 91,548; cyl:8×6 91,622; cyl:9×6 91,640; no root filter,
       pawn sorties included) against every mirror class of promotion-free contexts with s to move losing: cyl:7×6 all 13 classes (26
       contexts), cyl:8×6 all 36 (56 contexts), cyl:9×6 19 of the 53 (all 16 with at most 3 pawns and 3 of K18's family). Of 6,033,423
       legal pairs 68,395 are not punished (cyl:7×6 15,700 of 1,135,472; cyl:8×6 39,673 of 3,195,699; cyl:9×6 13,022 of 1,702,252;
       draws 11,431, White wins 56,964), and every one of the 68 context classes has failures. K18's family (both sides have a context
       move): cyl:8×6, 4 classes (K18's 5 contexts), 117 draws and 5,407 White wins in 351,502 pairs; cyl:9×6, 3 classes, 87 and 3,163 in
       264,874. At sorties that K18's search lists as plain-only at a group with no outright escape (cyl:8×6): 1,182 failures, 185 in
       K18's family. Groups with 5 or 6 Z-pawns (a 1% sample of the roots of cyl:8×6, 3,162 plain-only sorties, against the 12 classes
       with at most 3 context pawns): 216 failures in 37,362 legal pairs. Checks: K23's independent P-solver `ref3` gives the same value
       on 50 sampled failures and 50 random pairs of cyl:8×6, on 8 failures of the 5–6-pawn sample and on the examples below; K18's
       `lg.cpp` gives the same plain-only sorties on every root it lists (cyl:7×6, 8×6, 9×6, both variants, about 51,000 root lines in the P variant and 46,000 in the Q
       variant). The referee's own solver (written from `kings/SPEC.md` and Definition 2.6) gives the same plain-only sortie lists with
       the same four flags on all three boards (91,548, 91,622, 91,640; 0 differing lines), the same promotion-free contexts and classes
       (26, 56, 100; 13, 36, 53 mirror classes), and the same legal / Black-win / draw / White-win counts and the same failure set, pair by
       pair, for four contexts run in full: `Pe2 pe3` on cyl:8×6 (87,564; 664 W, 833 D) and cyl:7×6 (87,490; 741 W, 605 D),
       `Pe2 Pg2 pe4 pg4` on cyl:8×6 (85,748; 1,268 W, 52 D) and `Pe2 pe3 pe5` on cyl:9×6 (86,347; 24 W, 345 D). These lists and the four
       context rows are CHECKED-2; the other totals are COMPUTED-1 (K42's solver).
     - *Examples (cyl:8×6, CHECKED-2: K42's solver, `ref3` and the referee's solver agree on every value below, bare and with G).* G = `Pe2 Pg2 pe4 pg4` (K18's family, * + * = 0):
       (i) Y = `Kb1 Pb2 ka4 pa2`, m = Kb1–a1 (bare: only 1...Kb3 wins, plain T = 1). With G it is a draw: 1...Kb3 2.e3, and Black's only
       context reply 2...g3 attacks h2 and stalemates White. (ii) Y = `Ka3 Pb3 ka1 pb4`, m = Ka3–h4 (plain T = 6): White wins with G,
       1...Kb2 2.Kxg4 (the only winning move); with the capture the g-pawn promotes within 5 moves, so (L2) fails. (iii) The same kind
       at a group of K18's no-escape list: Y = `Kc3 Pa2 kc1 pa4 pa5`, m = Kc3–d4 (plain-only in both variants): White wins with G.
       (iv) G = `Pe2 Pg2 pe5 pg5`, Y = `Ka4 Pb3 kb6 pb4 pa5`, m = Ka4–h5: a draw without a race or a stalemate (bare, only 1...Kb5 wins;
       with G it loses to 2.g4, and 1...g5–g3 is Black's only drawing move).
     - *Mechanism (COMPUTED-1, exhaustive over the failures of the three boards).* Each failure was re-solved with a stalemate of s
       scored as a loss for s (m1), with s's king kept off the context files (m2), and with both (m3). No failure survives m3. cyl:8×6:
       33,459 White wins are removed by m2 alone (king raids), 143 only by m3; of the 6,071 draws 3,973 are removed by m1 alone
       (a context pawn's attack takes a buffer square and stalemates s), 437 by m2 alone (the king blocks, captures or threatens a context
       pawn), 1,661 by either. cyl:7×6 and cyl:9×6 are alike (0 survivors; `findings.txt` §5–6). So every failure uses the sortie king. The referee re-ran the
       three variants with its own solver on the 1,497 failures of `Pe2 pe3` on cyl:8×6 and on examples (i), (ii), (iv): the same
       classification, failure by failure (0 survivors of m3).
     - **Proposition 8.1′ (tempo pairing for promotion-free contexts). PROVED (K42, 2026-11-22; `kings/delegate/out/K42/PROOF.md`;
       re-derived step by step by the K42 referee, same model family, `kings/delegate/out/K42/VERIFY.md`; no human re-derivation).** Let Q (s to move, no e.p. right) and σ be as in Proposition 8.1, with (P1) and (P1e). Assume (PF): the context G
       of Q is promotion-free and s to move loses its pawn game. Fix a set 𝒢 of positions of that game with s to move that contains G,
       consists of losses for s and is closed under pairing (for example all such positions reachable from G); let X be the squares
       holding a context pawn in a position of 𝒢 or one move of s after one, E the squares passed over by a double step in that play,
       and A the squares attacked by an s̄ context pawn in those positions. Assume (P3′): the set R of (P3) contains no square of
       X ∪ E ∪ A. Then s̄ wins P from Q. Under (PF), (P2) holds automatically (Lemma A of `PROOF.md`), and X ∪ E ∪ A lies inside X and
       its king-neighbourhood, so Proposition 8.1′ contains Proposition 8.1 for promotion-free contexts and weakens (P3): the sortie
       king may stand next to or behind a context pawn, but not where a context pawn stands or moves, nor where an s̄ context pawn
       attacks. The proof is that of Proposition 8.1 with each use of the king-neighbourhood replaced by X, E or A. Example (i) shows
       that A cannot be dropped: there R = {a1, h2} avoids X ∪ E, and h2 lies in A. A certificate check (s̄ wins the plain local game in which a step of s's king onto
       X ∪ E ∪ A and an e.p.-only node of s are failures; COMPUTED-1, not re-run by the referee) certifies 1,213,383 of the 6,033,423 pairs (Proposition 8.1's
       form 967,308), and none of the 68,395 failures.
     - *Open.* A form that lets the sortie king into the context (it would need at least an (L2)-type count with the king's captures
       and an (L3)-type no-stalemate hypothesis), the lapse-game form without (P1e), chess, and larger contexts and groups.
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder?
>>>>>>> NEW

### EDIT 5 status-table row for open question 1 (K42, 2026-11-22)
<<<<<<< OLD
re-derived by the K38 referee, `kings/delegate/out/K38/VERIFY.md`) | K24; `kings/delegate/out/K24/VERIFY.md` |

Not answered by a change in the mathematics: R1 item 12
=======
re-derived by the K38 referee, `kings/delegate/out/K38/VERIFY.md`) | K24; `kings/delegate/out/K24/VERIFY.md` |
| §8 Q1, P8.1′ | Tempo matching (open question 1): FALSE as worded in P (CHECKED-2, K18); the promotion-free form, a CONJECTURE after K18, is FALSE (CHECKED-2, K42, 2026-11-22: 68,395 failures in 6,033,423 sortie–context pairs on cyl:7×6, 8×6, 9×6, K18's context family included; every failure uses the sortie king). Proposition 8.1 PROVED after repair (K18, re-derived by a second referee). Proposition 8.1′ (promotion-free contexts: (P2) automatic, (P3) weakened to X ∪ E ∪ A) PROVED (K42; re-derived by the K42 referee, same model family; no human re-derivation) | K18; K42 (`kings/delegate/out/K42/findings.txt`, `PROOF.md`, `VERIFY.md`) |

Not answered by a change in the mathematics: R1 item 12
>>>>>>> NEW
