# K38: hand proof for P5 (LOOPY §8 item 7, the 6-rank analogue of 7.2)

Output: `kings/delegate/out/K38/` (write only there; no git; do not edit LOOPY.md or REPORT.md).

K30 proved by hand that White cannot win P7 (position 7.2) with White to move, in P and in chess, on cyl:8×8 and flat:8×8
(`kings/delegate/out/K30/PROOF.md`, referee `VERIFY.md`): every White move is met by ...Kxd7, and after Ke5, Kd5 or Kf5
White holds by a blockade rule with an invariant set checked by an own move generator. LOOPY §8 item 7 says the same proof
for P5 (the 6-rank analogue; find its definition in LOOPY §5 and its computed values in the P5 rows) is open and nothing was run.

1. Compute P5's values in P (kp_p `--pmodel`, kings/delegate/out/K7/scripts/draft/kp_p.c) and in chess (kpsolve, cap 2) on
   the boards LOOPY lists for P5, and with ref3/ref3m (`kings/delegate/out/K23/verify`; board spelled `cyl7x6`, `pln7x6`).
2. Write `PROOF.md`: a hand proof of whatever the computed value says (adapting K30's method), with every case. Where the proof
   uses an invariant set, check it with your own move generator written from `kings/SPEC.md`, and report the set size.
3. If the K30 method does not carry over, say exactly where it breaks and give the smallest counterexample line.
4. `EDITS.md` for LOOPY (§8 item 7, the P5 status row(s)), each OLD occurring exactly once.
Labels: PROVED only for the hand proof; solver results COMPUTED-1 / CHECKED-2.
