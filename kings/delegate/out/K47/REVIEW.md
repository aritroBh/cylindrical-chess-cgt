# K47 review (2026-11-23)

Question: is the exact over group of K45 on cyl:8×6, Z_O = `Kf5 kd4/kd5 Pb2 Pb4 Pe2 pa4 pb5 pe5`, equal to over in
sums, and can its exactness be proved by hand?

Investigator: an Opus agent (`findings.txt`, `PROOF.md`, `EDITS.md`, `src/`). Referee: a second Opus agent that wrote
its own solver before reading the investigator's (`VERIFY.md`, `verify/`). AI work, no human re-derivation.

## Verdict

- **Z_O is not equal to over in D-sums (CHECKED-2).** As the P game of its own pieces it differs from over at 38 of
  1,100 results (275 test games, two roots, two sides to move), always in Black's favour, from T = \*, ↓, under and
  sums containing them. Two investigator implementations agree on all 1,100; the referee's third solver agrees on the
  108 results it ran, which include every kind of difference.
- **Orientation and model checked first.** The comparison with over (not under) is the right one. The reading "Z_O as
  the P game of its pieces, its moves real moves" is the only non-trivial one: in the D-model of Definition 1.5 the
  group is over_D by construction.
- **Hand proof: q_A is a mutual zugzwang of P on every cyl:W×6, W ≥ 8 (PROVED).** The investigator's Proposition 2 had
  a gap (White's king can take e5 when it stands on d6, e6 or f6); the referee repaired it (Kc2, Kxb2 and the a-pawn)
  by hand and confirmed the line with its solver. The rest of exactness ((O1), the d5 root) stays CHECKED-2.
- **Candidate values (COMPUTED-1, signatures on the battery only):** the d4 root has the results of tiny-2, the d5 root
  those of ⇑\* = {0 | ↑\*} + \*.
- **P contexts (CHECKED-2 for the P values):** P follows r(over ⊞ C) in 262 of 263 contexts; the exception
  `Ph2 pi3 pi5` (cyl:10×6) is confirmed by ref3m and kp_p.

## Integration

The referee's replacement set `verify/EDITS.md` was applied to `kings/theory/LOOPY.md`: 6 applied, 0 rejected, table
cell counts unchanged. Two corrections by hand after applying: a nested bold marker in the C4.7 status row, and the
name of the d5-root candidate (the referee wrote "↑²\*" for {0 | ↑\*} + \*, which is ⇑\*).

Corrections the referee made to the investigator's edits: the Kxe5 case in the hand proof; the placement count
(2,853,540 reachable placements; 3,914,687 is the node count with every e.p. target kept); a sentence on the model
reading; the third solver and the candidate signatures; a more precise \* example.

## Process notes

- The referee's ref3m run on 84 cyl:10×6 positions peaked at 4.75 GB, over the 3 GB limit; it stopped its own run
  (recorded PIDs) and finished with kp_p under a 2.9 GB cap. The investigator's ref3m run on the same board very
  probably exceeded 3 GB too. Later briefs must measure ref3m's memory on cyl:10×6 before a batch.
- No pattern kills; only recorded own PIDs were stopped. Binaries removed.

## Open

The value of Z_O; whether any exact group of Definition 4.8 has the value over; a hand proof of (O1) and of the d5 root.
