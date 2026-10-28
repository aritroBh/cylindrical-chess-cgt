Referee amendments to K17/EDITS.md (round 2).  Apply EDITS.md first, with the label changes A1-A3 below, then the new edit B1.
OLD of B1 occurs exactly once in the current LOOPY.md (checked 2026-10-27 19:4x).

A1. In EDIT "status row (V1a)", NEW: replace "PROVED by an isolated counterexample (cyl:6×6 `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`, a Z-pawn check; CHECKED-2 in P with real kings, K17)"
    by "CHECKED-2 by an isolated counterexample (cyl:6×6 `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`, a Z-pawn check; P with real kings: three independent solvers agree, K17 and its referees)".
A2. In EDIT "table row (V1a)", NEW: replace "**The clause "no checks": PROVED needed (K17), CHECKED-2.**" by "**The clause "no checks": needed, CHECKED-2 (K17; the position is small enough that a hand proof of P = W is possible but none is given).**".
    Also replace "(COMPUTED-1, kpsolve only: X = W; ..." by "(CHECKED-2: kp_p and ref3m agree: X = W; ...".
A3. In EDIT "proposition 1.15": (i) in the proof of (a) replace "which lies on F_Z, two files from every context pawn's captures, or block" by
    "which lies on F_Z, while every square a context pawn can capture on is at distance >= 1 from F_Z, or block"; (ii) replace "(flat:6×6: 1,128 (E)-violating roots;" by
    "(flat:6×6: 1,128 roots in which some reachable position has a capture of a just-double-stepped pawn, 752 of them with a genuine e.p. capture;"; (iii) replace "So (V1a) fails at X iff (check) ... or (E) fails"
    by "So (V1a) fails at some Y iff (check) ... or (E) fails" (V1a is a hypothesis over every Y, and the check status of a given side is the same at every Y).

### EDIT B1 (S1 is no longer a bare conjecture)
<<<<<<< OLD
the natural D(X) no isolated counterexample is known, so "(S1) is needed" is a CONJECTURE, as for (V1a).
=======
the natural D(X), K17's `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -` (cyl:6×6, CHECKED-2, §1.5) is an isolated counterexample: σ = Black is the D-winner
and in check, its only legal moves are Z-moves, none closing and none a D-move to a position of N, so (S1) fails and P(X) is a White win. That is the same
failure as the clause "no checks" of (V1a); a failure of (S1) with no check at the root is not known.
>>>>>>> NEW
