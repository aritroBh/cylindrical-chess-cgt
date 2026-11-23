# K49: a hand proof for the ON class of K+P v K on the cylinder (LOOPY §8 item 5)

K40 computed that under normal play, on cylinders of 3 and 5–8 files, every K+P v K position x has one of three
signatures: DEC (White wins against every test), ON (the signature of on) or DUD (draw against every test). DEC = P_L
is proved (Proposition 4 of `kings/delegate/out/K40/PROOF.md`); for the ON class there is no hand proof: "White needs no
spare tempo, and no number of Black spares helps Black" is computed for integers up to ±12 only.

1. Characterise the ON class by a rule a person can check (king distances, the pawn's file and rank, the side to
   move), and test the rule against K40's tables (`kings/delegate/out/K40/data/`) on every board: 0 exceptions, or list them.
2. Prove by hand that a position satisfying the rule has the ON signature against every test game T, not only the
   integers up to 12: White has a strategy that never needs a move in T, and Black's moves in T never help.
   State exactly which properties of T you use.
3. Do the same for DUD on 3, 6 and 8 files ("Black can force Kxp against a White who may pass at will"), and explain the
   odd-width fortress exceptions if you can.
4. Light computation only (seconds, no heavy runs). Output findings.txt, PROOF.md, EDITS.md for LOOPY §8 item 5.
