# K47: the K45 over group: hand proof of exactness, and its value in sums

K45 found the exact over group Z_O = `Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5` on cyl:8×6 (Black's king shuttles d4–d5; White's
freeze is e2–e4 at d4, e2–e3 at d5), exact in the sense of Definition 4.8 in plain P (CHECKED-2). Read LOOPY Definition
4.8, Conjecture 4.7, Lemmas 4.9–4.11, the K45 bullet, and kings/delegate/out/K45 (findings.txt, VERIFY.md).

1. Hand proof that Z_O is exact on cyl:8×6: every move at both roots and after each freeze loses at once (K45 says so),
   so a short case list should do. Give it move by move, and say which widths the same argument covers.
2. Value in sums. Test whether Z_O equals over = {0 | pass} as a D-model component: compare r(Z_O ⊞ T) with r(over ⊞ T) for
   test games T (integers −6..6, on, off, dud, *, ↑, ↓, ±1, over, under, and sums of two of them), both sides to move, with
   your own sum solver from SPEC.md and Definitions 1.2, 1.3, 1.5; a second implementation must agree. Report every
   disagreement.
3. Beside P contexts on files f–h at distance ≥ 2 (with buffer files c and… check the buffer for this F_Z), sample contexts of at
   most 2 + 2 pawns with kp_p --pmodel and ref3m (board `cyl:8x6`): does Z_O shift outcomes like over?
4. Output findings.txt, PROOF.md, EDITS.md for LOOPY (Conjecture 4.7 status row, the K45 bullet, §8 item 2).
