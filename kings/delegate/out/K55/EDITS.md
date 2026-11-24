### EDIT status row C4.7: the 2 + 3 group of cyl:10×6 has the results of over on the whole battery (K55, 2026-11-23)
<<<<<<< OLD
PROVED by hand after a referee repair; see the K47 bullet in Conjecture 4.7)
=======
PROVED by hand after a referee repair; see the K47 bullet in Conjecture 4.7; K55, 2026-11-23, CHECKED-2: the same pawn group on cyl:9×6 and 10×6 gives the same 1,100 results, while the 2 + 3 group of cyl:10×6 has the results of over against all 752 test games tried, a finite battery, not a proof of equality; see the K55 bullet)
>>>>>>> NEW

### EDIT new K55 bullet after the K47 bullet (K55, 2026-11-23)
<<<<<<< OLD
the P context test, unlike the D-sums, hardly separates Z_O from over.
=======
the P context test, unlike the D-sums, hardly separates Z_O from over.
  - *K55 (2026-11-23; `kings/delegate/out/K55/findings.txt`; AI work, no human re-derivation; K47's two solvers `za.cpp` and the referee's `rz.cpp`, widened for cyl:10×6 and checked against K47's outputs byte for byte; every result below CHECKED-2, za = rz everywhere). The other exact groups, and the value of Z_O.*
    - *The other exact groups.* K45's ten groups on cyl:8×6 to 10×6 are five over groups and their colour mirrors; one over group is the reflection of Z_O. The other three, against K47's 275 test games (1,100 results): the pawn group of Z_O on cyl:9×6 and on cyl:10×6 gives exactly Z_O's results (38 differences from over); the 2 + 3 group `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` of cyl:10×6 equals over at all 1,100 results, and at all 3,008 results of 752 test games (the 275 and 477 further games, below). It is the only exact group found with the results of over on the whole battery. This is a finite battery, not a proof that the group is over.
    - *Z_O against an enlarged battery.* 794 test games (3,176 results): K47's 275; tiny-n, miny-n, ⇑, ⇑\*, ↑², ↑\*, the switches {n ∣ −n}, {n ∣ 0}, {0 ∣ −n} and their negatives; sums of up to three atoms of {\*, ↑, ↓, tiny-1, miny-1, tiny-2, miny-2, ±1, 1, −1, over, under}; then tests built from the candidates that survived. Over 3,000 candidate games were scanned (COMPUTED-1, one Python program). No candidate survives at either root. The d4 root has the results of tiny-n against every test without miny-m, m ≥ n, and is below every tiny-n tried (n ≤ 30: Z_O ⊞ miny-n is a Black win with either side to move); the d5 root has those of {0 ∣ tiny-n} except against −{0 ∣ tiny-n}. The loopy candidates {0 ‖ 0 ∣ off}, {0 ∣ {0 ‖ 0 ∣ off}} and the D-games {0 ‖ 0 ∣ ⊖}, {0 ∣ {0 ‖ 0 ∣ ⊖}} each fail only against their own negatives (4 to 8 results). Reading, not a result: Black's threat in Z_O is a promotion, larger than any finite reserve, and the d5 root behaves like {0 ∣ d4 root}.
    - *Order tests.* §3 defines no order on loopy D-games. With the difference test of Proposition 3.9′ and Proposition 4.5 (G ≥ H iff White survives G ⊞ (−H) with Black to move first; draws counted once for each side, which changed nothing here) the d4 root is above 0 and below ↑, ⇑\*, over and every tiny-n tried, and the d5 root is above 0, below ⇑\* and over, and confused with ↑ and tiny-n. These are D-sum outcomes, not an order: Z_O is not a stopper (Kd4–d5, Kf5–f6, Kd5–d4, Kf6–f5 is an alternating cycle; 5,512,994 of its 5,513,626 legal states start infinite alternating play), and for loopy and D-game candidates the test is not even reflexive ({0 ‖ 0 ∣ off} minus itself is a draw; {0 ‖ 0 ∣ ⊖} minus itself is a Black win with Black first). No theorem of §3 turns a finite battery or a difference test into equality: Theorem 3.7 needs first-event dominance, and Siegel's simplest forms (the "Reading" after Theorem 3.8) need stoppers.
>>>>>>> NEW

### EDIT "To settle": the K55 answers (K55, 2026-11-23)
<<<<<<< OLD
the value of the K45 groups in sums (Z_O is not over, K47) and whether some exact group of Definition 4.8 has the value over; a hand proof of (O1) and of the d5 root of Z_O.
=======
the value of Z_O in sums (not over, K47; no candidate of K55's 794-game battery survives); whether the 2 + 3 group of cyl:10×6, which has the results of over against all 752 test games tried (K55), is over, which needs an argument beyond a finite battery (it is not a stopper); the groups of cyl:11×6 and wider in sums; a hand proof of (O1) and of the d5 root of Z_O.
>>>>>>> NEW
