# K57 review (2026-11-23)

Question: is the 2 + 3 group H10 = `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` of cyl:10×6 over in sums?

Investigator: an Opus agent (`findings.txt`, `PROOF.md`, `EDITS.md`, `src/`). Referee: a second Opus agent that
re-derived the proofs step by step, tested the lemma by brute force with its own code and recomputed the condition
for H10 with code that is not the investigator's (`VERIFY.md`, `verify/`). A blind proof of the two general
statements by Codex (model gpt-6.2-astra) is in `kings/delegate/out/K58/`. AI work, no human re-derivation.

## Verdict

- **Proposition 4.14 (over ≥ 0 in D-sums): PROVED.** White does at least as well beside over as beside zero, for every
  finite D-game, loopy or short, with or without terminals.
- **Lemma 4.15: PROVED.** An exact over group of Definition 4.8, as the P game of its own pieces, has the results of
  over beside every finite D-game provided (B1): after every non-shuttle Black move at a root, White still wins when
  Black may once move elsewhere (the sum's rule: a side with no move loses). Nothing beyond Definition 4.8 is needed
  on White's side or at the q's. Weakest step: the bookkeeping after a deviation (staying safe while both sides move
  elsewhere, and the termination count); the referee found it correct as written.
- **Corollary 4.16: PROVED given CHECKED-2 computations.** H10 has the results of over beside every finite D-game. The
  two computed facts: Definition 4.8 for H10 (K45) and (B1) for its ten non-shuttle Black root moves (the referee's
  own computation under the sum's rule, with the e.p. right kept for the two double steps; the K56 referee's pass-game
  solver; the investigator's solver; K55's two solvers).
- **What is not claimed:** equality with over as a game (the note defines none for loopy D-games), behaviour beside P
  contexts, chess.
- **Brute force (COMPUTED-1, referee's code):** 12,000 abstract exact groups with (B1), including adversarial ones,
  beside 224 finite D-games each: 0 differences from over in 63,349,928 results; 1,225 of 12,000 exact groups without
  (B1) differ. Proposition 4.14: 0 violations in 150,796 comparisons.
- **The 3 + 3 group** fails (B1) exactly at 1…e5–e4, the move K47 found.
- **The four groups of cyl:8×7** meet (B1) by one program only, so the conclusion for them is conditional.

## Integration

The referee's replacement set `verify/EDITS.md` was applied to `kings/theory/LOOPY.md`: 9 applied, 0 rejected, table
cell counts unchanged. It replaces the investigator's "over is realised in D-sums" by "has the results of over beside
every finite D-game" and brings six passages that still said "open" into line. Two sentences were added by hand after
applying: the Codex blind proof (K58) in the headers of Proposition 4.14 and Lemma 4.15, and K58's abstract example
that (B1) cannot simply be dropped.

A correction to K56's findings noted by the investigator: condition (T2) holds in 5 of the 9 groups, not 6 (the 3 + 3
family is four groups). LOOPY's wording ("all but Z_O and its translates") was already right.

## Process notes

Peak memory: investigator 1.08 GB, referee 1.29 GB. No pattern kills; binaries removed.

## Open

A second program for (B1) on the cyl:8×7 groups; necessity of (B1); H10 beside P contexts and in chess; the value of
the 3 + 3 group.
