# K22 referee report (Lemma 2.9 without its added hypothesis)

Verdict: ACCEPT WITH FIXES. The refutation and the repaired lemma (B1) hold up under my own code and a step-by-step proof check.
Three small fixes are needed in EDITS.md. One of the agent's claims (the Python/C++ agreement on 92 roots) I did not re-run.
My verification code is in `verify/`: `mylocal.py` (my own solver of the local game), `myenum.py`, `mysample.py`, `chk_edits.py`.

## What I built and ran
- `verify/mylocal.py`: a new solver of the local game of Definition 2.6 (k = infinity, White = s-bar with king confined to F_Z,
  Black = s may pass when not in check, P semantics, queen clause switchable). I wrote it from the definition only, without K22's scripts.
  Pieces are kings and pawns; it has pushes, double steps, captures and e.p. It needs H >= 5.
- `kpsolve` and `kp_p` (the P model with real kings), both private builds from the sources named in the task.
- `verify/mysample.py`: time-boxed random sampling of roots of the family in the lemma.
  The family: all s-bar pawns on one file f, the s king on f above them, s to move, s pawns anywhere on F_Z, s-bar king anywhere on F_Z.
- `verify/chk_edits.py`: checks each EDITS.md OLD block against the current LOOPY.md.
- The heavy runs I queued (a 2+2 exhaustive on flat:4x5, cyl:7x6 and cyl:5x5, and a kpsolve cap-2 run on E1) never got a slot on `heavy.sh`.
  Both slots stayed taken by other jobs for 11 minutes. I cancelled them; PIDs are in `verify/run_pids.txt`.
  So I have no exhaustive run of my own; the exhaustive claim rests on the agent's run plus my samples.

## Claim by claim

1. **E1, flat:4x5 `Kd4 kb5 Pb2 Pb3 pc3 pc4`, Black to move, is a local win for White, T = 3.** CONFIRMED.
   My solver: minT = 3 with and without the queen clause. All six Black moves (Kb4, Ka5, c3-c2, c3xb2, c4xb3, pass) lose within 3 White moves.
   `verify/mylocal_counterexamples.log`. Third implementation, so CHECKED-2 is not overstated. I also replayed the lines by hand, as the proposed text gives them.
   Both lines are correct: after a pass, 2.bxc4+ and c5=Q with c5 guarded by Kd4. After 1...cxb3 2.bxc3 and the pawn run c3-c4+.
2. **E2 cyl:7x6 F_Z = a..c `Ka5 kc6 Pc3 Pc4 pb4 pb5`, and E4 `Kc5 ka6 Pa3 Pa4 pb4 pb5` (f = a, wraps), White wins in 3.** CONFIRMED.
   My solver gives minT = 3 for both, with and without the queen clause, and all five or six Black replies lose.
   The 5x6 flat version (E3) also gives minT = 3 in my solver.
3. **E1 to E4 are P-model White wins with real kings.** CONFIRMED for E1, E2, E3 and E4 (my own build of `kp_p`).
   E1 flat:4x5: `W W`, all five Black moves `:W`. E2 cyl:7x6: `W W`, all five `:W`. E4: `W W`, all five `:W`. E3 flat:5x6: `W W`, all five `:W`.
   The control `Ka1 kb5 Pb2 Pb3 pc3 pc4 b -` gives `L L` in P, with only Ka5 losing for Black. My local solver finds no White win for it up to T = 10.
   Outputs: `verify/p_flat4x5.out`, `verify/p_cyl7x6.out`.
   Note that the P model has no passes, so it is a different game from the local game. It supports the position, not Lemma 2.9 directly. The text says this correctly.
4. **Repaired Lemma 2.9 under (B1): PROVED.** I checked the proof step by step against Definition 2.6 and found no gap.
   - Root: s's king is on f above all s-bar pawns, and s-bar pawns attack only files f +- 1, so s is not in check. The pass is legal. A capture is legal (no sliders, no pins).
   - (B1) leaves at most one attacked pawn at the root. The capture makes (J2) true at s-bar's first turn. A capture by s cannot be a promotion, because s-bar pawns stand on rank >= 2.
   - Inductive step. Pushes and double steps are blocked by the king's square, so no s-bar pawn reaches rank k, let alone the last rank (k <= H).
     That also holds for a double step on H = 4. A capture by s-bar needs an attack, and (J2) says there is none. E.p. needs a double step by s, and s never double-steps.
     Only the moved pawn can be newly attacked, so at most one pawn is attacked at s's turn. The capture then restores (J2).
   - The capturing pawn Q lands on f. It attacks files f +- 1 only, where there is no s-bar pawn. Before the capture it attacked only P among s-bar's pawns.
   - Removing an s pawn never creates an attack, so s-bar's king captures cannot break (J2).
   - The sufficient conditions for (B1) are right. Single pawn: trivial. No s pawn on f +- 1: trivial. H = 4: two attacked pawns need ranks x1 < x2 with x2 >= 3,
     so the attacker is on rank >= 4, which is s's first rank; so H >= 5 is needed.
   - The optional e.p. capture at the root is not forced, so the strategy may ignore it. The proof's use of "an e.p. right in Q_Z was created by s-bar" is right.
   - My own machine check of the strategy (`myenum.py ... strat`, which explores all White replies to "capture the attacked pawn, else pass"):
     flat:3x5 (f = 1, 2+2 pawns, 1,507 roots with <= 1 attacked pawn; and 3+3 pawns, 3,027 roots): 0 violations.
     That is only a small check; the proof does not depend on it.
5. **Exhaustive search, 74,469,430 roots, 0 wins with <= 1 attacked, all 22,456 wins have >= 2 attacked.** NOT_CHECKED directly (my exhaustive runs never got a lock slot).
   Partial support from my random sampling, with my own solver and with Tmax = 6 or 7 (a win is only looked for within T moves):
   | board | roots with 0 / 1 / 2+ attacked | White wins with 0 / 1 / 2+ attacked |
   |---|---|---|
   | flat:4x5, 3+3 pawns | 4596 / 1297 / 139 | 0 / 0 / 7 |
   | cyl:7x6 F_Z a..c, 3+3 | 256 / 85 / 12 | 0 / 0 / 1 |
   | flat:4x6, 3+3 | 308 / 81 / 6 | 0 / 0 / 0 |
   | cyl:5x5, 3+3 | 274 / 98 / 9 | 0 / 0 / 0 |
   | flat:3x5, 3+3 | 132,178 / 45,317 / 7,212 | 0 / 0 / 424 |
   (`verify/sample_log.txt`; the flat:4x5 and cyl:7x6 rows were printed to the terminal and are not in the log.)
   Also a full enumeration of flat:3x5 f = 1 with 2+2 and 3+3 pawns: no wins at all (0 / 0 / 0), consistent but uninformative.
   So the pattern "wins only with >= 2 attacked" reproduces, but a bounded-T sample cannot show "no win at any T". The proof does that.
   The label COMPUTED-1 is right for the exhaustive number; it should say it is one implementation (C++), with a Python spot check.
6. **Python agrees with C++ on 92 sampled roots.** NOT_CHECKED (I did not re-run `compare.py`).
   Replaced by something stronger for the named positions: my own third solver agrees with the agent's counterexamples (claims 1 and 2).
7. **(B1) is sufficient, not necessary; about 1.0% of roots with >= 2 attacked are lost.** CONFIRMED in kind.
   22,456 / 2,233,320 = 1.005%, an arithmetic match. The control position `Ka1 ...` is not lost, in my solver and in `kp_p`. My samples give 5% to 8% on flat:4x5 and cyl:7x6,
   but those are biased by small boards and capped pawn counts, so they are not a contradiction; the 1.0% belongs to the agent's full enumeration, which I did not reproduce.
8. **Chess (A_Q) not established.** CONFIRMED as stated. My own `kp --board flat:4x5 --cap 1 --moves` on E1 gives `W L`
   ("capped promotions met (two bounds)"), as the agent reports. The cap-2 run did not get a slot for me either. Label CONJECTURE is right.

## Proposed EDITS
`verify/chk_edits.py`: OLD occurs exactly once in the current LOOPY.md for all three blocks (status row, summary row, Lemma 2.9 statement and proof).

- **EDIT L2.9 status row: ok.** One accuracy point: "CHECKED-2 and a P-model run" is fine, but "no exception to (B1) in 74,469,430 roots (COMPUTED-1 ...)" overstates what a bounded search shows.
  Suggest "no White win with at most one attacked pawn among 74,469,430 roots, within the search bound (COMPUTED-1) and proved separately by (B1)". Fix needed, small.
- **EDIT L2.9 summary row: ok.**
- **EDIT Lemma 2.9 statement and proof: ok, with two small fixes (items 1 and 3 below).**
  1. The last bullet of the Remark says "The uses in §5.2, P5 and P7 are unaffected: there s has no pawn at all (and s-bar has one Z-pawn)".
     In the starting positions s does have a pawn (7.2 `Pd7`, P5 `Pb5`); it is only gone in Q_Z because the standard reply r captures it (Kxd7, Kxb5).
     Say "in Q_Z, after the reply r, s has no pawn (and s-bar has one Z-pawn, so (B1) holds anyway)".
  2. (Withdrawn.) I first thought the quoted R3 item 4 repair had no source. It does: `kings/theory/REVIEWS.md` line 241 has "pass, but capture any s̄ pawn that
     attacks an s-pawn", plus an induction. The EDIT's quotation is accurate up to the hyphen in "s-pawn". That review line also says "s has no pawns there", the same
     imprecision as fix 1, which is where the wording of the new bullet comes from.
  3. Minor: "The smallest board is 5 ranks" should read "the smallest number of ranks is 5"; the width of the smallest counterexample is not established (flat:4x5 is the smallest found, not shown minimal).
- Not covered by EDITS.md but now stale: nothing else says "CONJECTURE without the hypothesis" apart from the three places edited. Lines 1699, 1703, 1846 and 1848 cite
  Lemma 2.9 for single-pawn cases, where (B1) is automatic, so they stay valid.

## Limits of this referee check
- Bounded-T searches only (T <= 6 or 7 on samples). Nothing here shows a White win does not exist beyond that bound; the proof does that.
- No e.p. roots in my samples (the agent's `--ep` scan was not re-run). H = 4 boards are not covered by my solver (it needs H >= 5); the H = 4 case rests on the argument above.
- No exhaustive reproduction of the 74.5M roots (no lock slot).
