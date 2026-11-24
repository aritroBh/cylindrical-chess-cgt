# W7: two proofs for the new S12.2 ("Two Further Proofs for Section S2")

Output: `dist/tog/supp_src/s12b_extra.tex` (261 source lines). Test build: `delegate/out/W7_two_proofs/test_s12b.tex`
(preamble of `dist/tog/supplement.tex`, `macros.tex`, `supp/mainlabels.tex`, stub labels for `S-kings` and `thm:loopy`),
compiled with `nice -n 15 tectonic -X compile --only-cached --outdir delegate/out/W7_two_proofs/build`. Compiles with no
error and no undefined reference; the only warnings are hyperref "empty target" for the two stub labels.
**Page count of the part: 4 pages** (the 4th about three-quarters full), heading included.

Macros used: `\lab`, `\cyl` (from macros.tex), plus standard LaTeX/amsmath/unicode-math symbols (`\oplus`, `\ominus`,
`\boxplus`, `\varrho`, `\mathrm`, `\texttt`), `\subsubsection*`, `itemize` with `\item[...]`, `proof`. Item style copies
s12a_core.tex (`\textbf{A.n Kind (name).} \emph{statement}` then `\begin{proof}`).

## Items and the note lines they condense (line numbers of dist/tog/supp_src/s12_kings.md)

| Item | Content | Note lines |
|---|---|---|
| lead-in | names the note (`kings/theory/LOOPY.md`, Thm 3.4, Prop 2.11, Cor 2.11a) once | - |
| A.V definitions (D-games, play, short, Sums, Spare moves, Forcing, Predicates) | Def 1.1-1.3, Def 3.1, predicates of Thm 3.4 | 42-63, 1564-1573, 1639-1652 |
| A.18 Lemma (forcing and blocking) | the two strategy arguments behind Thm 3.4 | 1658-1678 (rewritten) |
| A.18a Theorem (outcomes with spare moves; thm:loopy) | Thm 3.4 (a), (b), (c) | 1636-1678 |
| A.18b Remark | how A.18a gives the S2 wording; the king-shuttle-as-pass hypothesis is not treated | 1575-1617 (only the caveat) |
| A.VI Setting, G_omega, Hypotheses | Prop 2.11 setting, notation, (H1)-(H5) | 1308-1339 |
| A.19 Proposition (frozen-king passer test) | Prop 2.11 statement and proof, Steps 0-5 | 1341-1400 |
| A.19a Corollary ((V2) with frozen kings) | Cor 2.11a, restated in the A.III language | 1402-1412 |
| A.19b Remark | sufficiency; (H5) counts non-passers; F only, not P or chess, with one C1 example | 1306, 1419-1421, 1508-1509 |

Left out: the note's examples for each hypothesis, all sweeps and counts, Cor 2.11b, Remark 2.11, Theorem 2.11K,
Prop 3.2 and its chess bridge, Thm 3.3, Cor 3.5, the loopy-sum theory 3.7 ff.

## Changes, narrowings, repairs relative to the note

Theorem 3.4 (A.18, A.18a):
1. **Proof rewritten with explicit strategies** instead of the note's least-fixed-point stage argument. The note's (a)
   proof argues by "Left first wins at stage n by passing" and then had to concede (its own correction) that a pass can
   be a winning move; the step from "a first-stage win is never by a pass" to the recursion is left implicit there. A.18
   proves both directions directly: a forcing strategy that uses only moves of G (invariant lambda), and a blocking
   strategy with passes (invariant not-lambda), with an explicit bound of 2h+1 moves on plays under the forcing strategy.
   No change of statement.
2. **One predicate pair for Black in both cases.** The note defines Rho (dud case) and Rho' (on case) separately; they
   are literally the same recursion, and A.18 uses one pair (varrho) for both, which makes "Black's winning condition is
   the same whether or not Black can wait" visible.
3. **"Every other move in Z loses" made formal.** The note's Thm 3.4 is about G (+) on_D / dud_D only; the S2 wording also
   has losing moves in Z. A.V models Z as a one-position D-game with passes and suicides; A.18 shows suicides never enter
   the strategies, so the theorem covers S2's wording. (The note did this by deleting suicides via its Lemma 1.7.)
4. **"Force a decisive event against a passing opponent" defined** (A.V, Forcing) and proved equivalent to the predicates,
   so the S2 sentence's words are a theorem, not a gloss. In (b) the definition lets the forcing side be Black while the
   passing opponent is White.
5. **Finiteness in the one-sided case**: the note says "Black makes finitely many moves since G is finite and acyclic";
   A.18a(b) gives the bound (at most h Black moves, at most 2h+1 moves in all) and then Zermelo on the finite tree.
6. **Draw case**: proved by the blocking strategies of both sides (Black needs its pass for this; White's pass is used
   in case (b)).
7. **Caveat added (A.18b), not a change of the theorem**: the pass of Z changes only the side to move and keeps G's
   position, e.p. right included. A real king shuttle ends an e.p. right. The note's chess bridge (lines 1591-1592) says
   "The pass of on_D resets the flag, as White's shuttle does", which does not match Definition 3.1 (the pass is z -> z in
   the on_D coordinate; G's coordinate, with its flag, is untouched). This only affects the chess bridge after Prop 3.2,
   which is not part of the S2 theorem and is not in the new text; flagged here for whoever keeps that bridge.

Proposition 2.11 / Corollary 2.11a (A.19, A.19a):
8. **Statement narrowed in name only, as the note has it**: proved in F (frozen kings), not P with real kings, not chess.
   A.19b says so and gives the note's C1 example (cyl 8x6, White Ka1 Pc2, Black Ka6, White to move: hypotheses hold,
   F-win, P draw).
9. **Flat board**: the note proves the cylinder case and says "on a flat board the same proof works ... (not separately
   written out)". A.19 states both; the proof is phrased with "files at distance 1", which is the same argument on both
   boards (edge files simply have one neighbour). I consider this a correct extension; flagging it as the one place where
   the text states more than the note writes out.
10. **I re-checked every step and found no error.** Points checked specifically:
    - *e.p.*: (J_omega) carries "p cannot be captured e.p."; a double step of p leaves every omega strip pawn strictly
      below p's new rank, so no capturer exists; the only e.p. capture by omega in the whole play is the one offered at y
      (beta double steps only p, which is never capturable), and G_omega allows exactly that one as its first move; an
      e.p. capture of a beta pawn on f+-1 lands at rho(q)-1 <= rho_0.
    - *captures onto the passer's file or path*: a capture lands on the captured beta pawn's file; beta pawns on f stand
      behind p (H1, and none can enter f later since only p moves), so nothing lands ahead of p; captures of beta pawns on
      f+-1 land at rank <= rho_0+1 by (H4), which is what keeps (J_beta).
    - *checks and stalemate*: (H2)+Lemma A.1 keep the files next to beta's king pawn-free for ever, so beta is never in
      check and is never mated; (H3)+A.1 make the king step to t legal at every omega turn, even in check, so omega is
      never stalemated (the step loses in F, which is a beta win).
    - *move count*: d = H - rho for rho >= 3 and H - 3 for rho = 2 (double step then singles; H >= 5 as in A.III);
      omega makes exactly e moves before the d-th push, e = d if omega moves first, d-1 if beta does; (H5) mu >= e+1.
    - *who is to move*: in A.19a, s = N (the side not making the passer move), beta = the side W credits; e = d if the
      credited side made the move, e = d-1 otherwise; this covers races credited to either side.
11. **Small precision added**: A.19a's proof says why y' is before any promotion (no Z-move and no context promotion in
    R(Q), and the passer move itself does not promote, by Lemma A.2(c) as in the proof of A.11). The note left this
    implicit.
12. A.19b(a) states that (H5) counts all omega pawns and all omega move sequences (so a count of passed pawns alone, e.g.
    the count rule, is not the test) - this is the note's lines 1419-1421, without its examples.

## Dependencies

- A.18 Lemma: own definitions only (D-game, play/win/draw, short, Z with passes and suicides, forcing, predicates
  lambda/varrho). No A.n.
- A.18a Theorem: A.18; Sums (own); Zermelo's theorem for finite games (already assumed in the lead-in of S12.1).
- A.18b Remark: A.18a; Theorem thm:loopy of S2 (wording only).
- A.19 Proposition: Lemma A.1 (files); Part A.I (board, pawn moves, e.p. and rights, e.p.-aware test); Part A.III
  (game F); own: rho, d, e, strip, G_omega, mu_omega, (H1)-(H5).
- A.19a Corollary: A.19; Lemma A.2(c); Part A.II (W, adjudication); Part A.III (king group, context, decisive events,
  R(Q), (V2)); proof of Theorem A.11 (no promotion before the first decisive event); Remark A.12(b).
- A.19b Remark: A.19, A.19a, A.12(b); one C1 computation (used nowhere).

## Rewordings S2 needs (dist/tog/supp/s02.tex)

1. Lines 21-23. The sentence claims "a local test is known only if king moves also lose" and "wins the promotion game".
   The proof gives a win in F (the promotion game in which a king move loses), and "known only" is not true even of the
   removed note, which also proves a real-king version (its Theorem 2.11K, in P, with extra square-rule and no-stalemate
   clauses). "every enemy pawn ... needs a move more" is also loose: (H5) is about any sequence of enemy moves (one pawn
   can capture to free another), and with the beneficiary to move the enemy needs only as many moves as the passer.

   Old:
   > For (V2) a local test is known only if king moves also lose \lab{S}: a passed pawn then wins the promotion
   > game if, besides conditions on checks, stalemates and its own nearby pawns, its path is empty and every enemy
   > pawn, passed or not, needs a move more to promote.

   New (slightly shorter):
   > For (V2) we prove a local test only with frozen kings \lab{S}: a passed pawn then wins the frozen-king game
   > if, besides conditions on checks, stalemates and its own nearby pawns, its path is empty and no enemy pawn,
   > passed or not, can promote first.

   (If "frozen-king game" should be explained in S2: "... wins the promotion game in which a king move loses if, ...".)

2. Theorem thm:loopy (lines 51-56): no change needed; A.18a implies it as worded (see A.18b). Optional: the proof
   sketch (lines 58-63) could end with "Full proof: Theorem~A.18a." No change is required.

## Other places that will go stale when the old S12.2 is removed (not edited; outside my write set)

- `dist/tog/supp_src/s12a_core.tex` line 295 (Remark A.12(d): "Theorem 1.14 in the longer treatment") and lines 419-425
  ("Where to find the longer treatment ... In the numbering of the rest of this section: ...") cite the removed note's
  numbering as "the rest of this section".
- `dist/tog/tools/build_supplement.py` lines 346-355 build the old S12.2 (`\subsection{The Longer Treatment}`, NOTE mapping
  Theorem 3.4, the certificate theorem, etc.) and must be changed to input `s12b_extra.tex` under the new title.
- `dist/tog/supp/s16.tex` line 41 and the S12 section title mention "loopy games"; still true with A.18a.
- Main text `sections/04_kings.tex` lines 85-86 say a local test for (V2) "and the loopy games ... are in Section S2" -
  still true.

## Not sure / to check

- Label of the A.19b example: the note says kp_p (P with real kings) and kpsolve exact (chess) both give a draw. These
  compute different games, so I used C1 (for P), not C2.
- Whether the flat-board extension of A.19 (item 9) is wanted; it is a one-word change ("flat or a cylinder") to drop.
- A.18 forcing definition allows the opponent to pass even when it cannot wait in Z (needed so the S2 phrase "against a
  passing opponent" has one meaning in (a) and (b)). This is a definition choice; A.18a(b) then says Black wins iff it
  forces a decisive event against a White who passes, which is exactly S2's wording.
- Page count measured in a test build with the supplement's fonts and margins, not inside the real supplement.
