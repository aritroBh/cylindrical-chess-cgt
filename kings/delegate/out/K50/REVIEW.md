# K50 review: `kings/embed_check.py` (integrated 2026-11-23)

**Outcome: accepted with the referee's fixes.** The referee's patch (`verify/embed_check.patch`, fixes F1 and F2) is
applied to `kings/embed_check.py`.

- The program certifies the frozen-king model for one K+P position by sufficient conditions that LOOPY proves, per
  side to move, and reports CERTIFIED, FAILS or UNDECIDED per clause. CERTIFIED is a result in the promotion game P;
  chess also needs (A_Q)(X), which the program does not check.
- Referee's harness against `kp_p --pmodel` on 6-rank boards: 6,222 strict positions (439 CERTIFIED) and 1,002 with
  `--ctx` (76 CERTIFIED), 0 disagreements; the investigator's 2,080 runs had 193 CERTIFIED, 0 disagreements.
- F1 (crash): `min()` without a default when the other side has no pawn in the terminal's component; fixed.
- F2 (soundness gap, no counterexample found): bounds for the other components ran over non-terminal states only and
  could miss an e.p.-lapse terminal on boards of 7 or more ranks, in the sharp-form route; fixed by including
  terminal states.
- Open minor points: the e.p. square of a FEN is not validated (M2); a FEN whose size does not match `--board` raises
  (M3); `--help` is read as a position. Feed only legal FENs.
- Strict mode certifies none of the trébuchets (Fig. (a), Fig. (b), Z_T): the literal (L3_F) fails, as §5.1 says.
  `--ctx` (off by default) certifies them beside locked or slow contexts. Its argument is the implementer's, judged
  SOUND by the referee, who proposes it as a Lemma 2.6a; it is not yet a LOOPY statement.
- ChessSums with `--group`: all 23 APART positions pass separation; all 14 ADJACENT and all 163 SHARED fail it.
