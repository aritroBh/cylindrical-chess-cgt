#!/usr/bin/env python3
"""build_edits.py -- K30: writes ../EDITS.md; every OLD is taken from the CURRENT kings/theory/LOOPY.md and must occur exactly once."""
import sys, re
LOOPY = '/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md'
t = open(LOOPY).read()
P = '`kings/delegate/out/K30/PROOF.md`'
edits = []
def add(label, old, new):
    n = t.count(old)
    assert n == 1, (label, n)
    edits.append((label, old, new))

add('status row 5.2 sorties: not punished',
    '"Not punished": CHECKED-2 (revised after K19, 2026-10-27): after Kd5, Ke5 or Kf5 Black has no forced promotion.',
    '"Not punished": PROVED by hand (revised after K30, 2026-10-27; K30 has not been re-derived by a referee; the computations of K19 and K24 agree): after Kd5, Ke5 or Kf5 Black has no forced promotion.')

add('status row 5.2 sorties: White cannot win chess',
    'That White cannot win chess either, so that the bare group is D in C, is CHECKED-2 by Lemma 2.7a (EPW and EPB computed by two implementations) and kpsolve exact. There is no hand proof of it: Lemma 2.9 refutes (L1) for a defender who may pass, and White cannot pass (open question 7) | R4 item 9; K19; K24 |',
    'That White cannot win chess either, so that the bare group is D in C, is PROVED by hand (revised after K30, 2026-10-27; ' + P + '; not yet re-derived by a referee), on cyl:8×8 and flat:8×8, in chess directly, so Lemma 2.7a is not needed. Part A, White cannot win: after any of its four moves Black plays ...Kxd7, and a lone king can neither promote nor mate. Part B, White does not lose: after Ke5, Kd5 or Kf5 White follows a blockade rule that makes a move every turn, with an invariant of 918 positions per board (Lemma D of the proof), and the other Black replies (...Kc7, ...e6, ...e5) are met by Ke6 or by taking the pawn. An own move generator checked all 918 positions, every Black move and the rule\'s reply, and three implementations agree on about 15.5k positions. The earlier evidence agrees: Lemma 2.7a with EPW and EPB (two implementations) and kpsolve exact | R4 item 9; K19; K24; K30 |')

add('status row P6, P7: hand proof of P7 w',
    'No hand proof of the P7 w draw exists: Lemma 2.9 refutes (L1) for Ke5, Kd5, Kf5, but (L1) lets White pass, so that failure does not make the sorties safe (open question 7) |',
    'Revised after K30, 2026-10-27: the P7 w draw is PROVED by hand, in P and in chess, on both boards (K30, not yet re-derived by a referee; ' + P + ', mechanically checked). White cannot win: after any of its four moves Black plays ...Kxd7, and a lone king can neither promote nor mate. Black cannot win after Ke5, Kd5 or Kf5: White follows a blockade rule that makes a move every turn (Lemma D of the proof), and the other Black replies are met by Ke6 or by taking the pawn. Kf7 loses in P: PROVED (...e5 and the pawn runs, and the White king is too far by the rule of the square). Lemma 2.9 refutes (L1) for Ke5, Kd5, Kf5, but (L1) lets White pass; the K30 rule never passes |')

add('section 5.2: not punished',
    'is **CHECKED-2** (revised after\n    K19, 2026-10-27): even without passes, Black cannot force promotion after Kd5, Ke5 or Kf5.',
    'is **PROVED** (revised after K30, 2026-10-27; hand proof in ' + P + ', part B, with the K19 and K24 computations agreeing; K19\'s revision of 2026-10-27 follows): even without passes, Black cannot force promotion after Kd5, Ke5 or Kf5.')

add('section 5.2: White cannot win chess',
    'That **White cannot win chess either**\n    is **CHECKED-2** by Lemma 2.7a: with every promotion a White win, White cannot win, and with every promotion a Black\n    win, Black cannot win (two implementations of both models), so the chess value is D, and kpsolve exact agrees (the\n    Lichess tablebase also, on the flat board). There is no hand proof of this draw. Lemma 2.9 says only that (L1) fails\n    for a defender who may pass, and White cannot pass (open question 7).',
    'That **White cannot win chess either**\n    is **PROVED** by hand (revised after K30, 2026-10-27; ' + P + '; K30 has not been re-derived by a referee), so the chess value is D, on both 8×8 boards.\n    - White cannot win: every White move leaves d7 unprotected, Black plays ...Kxd7, and a lone king can neither promote nor mate.\n    - Black cannot win after Ke5, Kd5 or Kf5: White follows an explicit blockade rule with an invariant (Lemma D of the proof), and it never has to pass. ...Kc7 is met by Ke6, and ...e6 and ...e5 by taking the pawn.\n    - Kf7 loses in P: ...e5, and the White king is too far by the rule of the square.\n    The earlier evidence agrees: Lemma 2.7a with EPW and EPB (two implementations of both models), kpsolve exact, and the Lichess tablebase on the flat board. The proof does not use Lemma 2.7a. Lemma 2.9 says only that (L1) fails for a defender who may pass; the K30 rule is a blockade that makes a move every turn.')

add('section 5 summary row',
    '7.2 is (D, W) with the w-entry by Lemma 2.7a; there is no hand proof of the 7.2 draw (open question 7) |',
    '7.2 is (D, W), and the w-entry is PROVED by hand (new, K30, 2026-10-27; ' + P + '; not yet re-derived by a referee), with Lemma 2.7a and the solvers as agreeing checks |')

add('section 5.2 predictions',
    '- **Predictions.** The bare 7.2 is (D, W), not the mutual zugzwang (L, W) (P7): CHECKED-2 in P and in C on both boards (revised after K24, 2026-10-27). The same holds for the 6-rank\n  analogue (P5).',
    '- **Predictions.** The bare 7.2 is (D, W), not the mutual zugzwang (L, W) (P7). The w-entry D is PROVED by hand in P and in C on both boards (new, K30, 2026-10-27); the b-entry is PROVED in P and CHECKED-2 in C (revised after K24, 2026-10-27). The same values hold for the 6-rank\n  analogue (P5), CHECKED-2 (K30\'s proof does not cover it).')

add('section 6 row P7: w-entry in C',
    'In C the w-entry is D by Lemma 2.7a (EPW and EPB both D for White to move, two implementations) and kpsolve exact, CHECKED-2, with no hand proof (Lemma 2.9 only refutes (L1) for a passing defender; open question 7).',
    'In C the w-entry is D: PROVED by hand (new, K30, 2026-10-27; ' + P + '; directly in chess, so Lemma 2.7a is not needed; K30 has not been re-derived by a referee). The computations agree: Lemma 2.7a with EPW and EPB both D for White to move (two implementations), kpsolve exact, and K30\'s own solver, `mine.c` and `kp_p --pmodel` on about 15.5k positions per board with 0 differences.')

add('status row L2.7a',
    'The values it is applied to (P5 w, P7 w) are CHECKED-2 |',
    'The values it is applied to (P5 w, P7 w) are CHECKED-2 (revised after K30, 2026-10-27: the P7 w value is also PROVED by hand directly in chess, so for P7 w the lemma is not needed) |')

i = t.index('7. **A hand proof that White cannot win in 7.2**')
j = t.index('without).', i) + len('without).')
add('section 8 item 7',
    t[i:j],
    '7. **A hand proof that White cannot win in 7.2** (PROVED for 7.2, new, K30, 2026-10-27; not yet re-derived by a referee; still open for P5). The w-entry of P7 is D in P and\n   in C on cyl:8×8 and flat:8×8, with the proof in ' + P + '. White cannot win: after any of its four moves Black plays ...Kxd7. Black cannot win after Ke5, Kd5 or Kf5: White follows a blockade rule that makes a move every turn, with an invariant of 918 positions per board, checked by an own move generator. Kf7 loses in P (...e5 and the pawn runs). Still open: the same proof for the 6-rank analogue P5 (the method should carry over; nothing was run), and for other board sizes.')

add('appendix A: K30 bullet',
    '  `kp_p.c` and `atlas/cylinder/kpk`.\n- **K18 re-computation (2026-10-27;',
    '  `kp_p.c` and `atlas/cylinder/kpk`.\n- **K30 hand proof of the P7 w draw (2026-10-27; ' + P + ', scripts and logs in `kings/delegate/out/K30/`; no referee yet).** One new implementation, `scripts/kpm.py`, an own move generator and solver of P, EPW and EPB written from `kings/SPEC.md` only (no solver code was read), and `scripts/k30lib.py`, which codes the strategies of the proof as finite rules.\n  - `check_kpk.py`: the invariant S of Lemma D (918 positions per board) is closed under every Black move and the rule. `check_A.py`: the four White moves, ...Kxd7, Black\'s rule for EPW, the Kf7 line. `check_B.py`: White\'s strategy against every Black move for each sortie (about 3,700 White-to-move states each).\n  - `compare.py`: 15,536 (cyl:8×8) and 15,695 (flat:8×8) positions visited by the checks, valued by the own solver, `mine.c` (P, EPW, EPB) and `kp_p --pmodel` (P): 0 differences. `mutation_tests.py`: damaged invariants are rejected.\n  Results: the P7 w draw is PROVED in P, EPW, EPB and chess; Kf7 loses in P (PROVED).\n- **K18 re-computation (2026-10-27;')

out = ['# EDITS for kings/theory/LOOPY.md (K30). Each OLD occurs exactly once in the LOOPY.md of the time of writing; `python3 kings/delegate/apply_edits.py kings/theory/LOOPY.md /tmp/out.md kings/delegate/out/K30/EDITS.md` checks it.\n']
for label, old, new in edits:
    out.append('### EDIT %s\n<<<<<<< OLD\n%s\n=======\n%s\n>>>>>>> NEW\n' % (label, old, new))
open('../EDITS.md', 'w').write('\n'.join(out))
print(len(edits), 'edits written')
