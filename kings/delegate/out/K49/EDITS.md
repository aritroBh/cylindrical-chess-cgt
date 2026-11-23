### EDIT 8.5a The ON class: the hand reduction to one computed fact (K49, 2026-11-23)
<<<<<<< OLD
   - **What is computed only.** That an ON position needs no spare tempo and is not hurt by up to 12 Black spares.
=======
   - **The ON claims, reduced to one computed fact** (new, K49, 2026-11-23; `kings/delegate/out/K49/PROOF.md`, not refereed).
     Under (N), with W ≠ 4, write W_N for White's wins in the bare game x ⊞ 0.
     - **Lemma P (no reciprocal zugzwang):** for every placement with Black not in check, if White wins with Black to move
       then White wins with White to move. CHECKED-2 on K40's twelve boards (it is the −1 column of K40's tables; K49's own
       solver `scripts/kn.c` reproduces all of K40's tables with 0 differences); COMPUTED-1 (kn.c) on every cyl:W×H with
       W ∈ {3, 5, …, 10}, 4 ≤ H ≤ 10; false on every 4-file cylinder (8–28 violations per board), which is where K40's 4-file
       anomalies come from. PROVED by hand only for the pawn on rank H−1.
     - **Given Lemma P, PROVED by hand:** (i) Black's spares never help and White needs none: r(x ⊞ n) = r(x ⊞ 0) for
       **every** integer n, not only |n| ≤ 12 (strategy: play the W_N strategy; a Black spare is answered via Lemma P; the
       pair (spares left, stage) decreases). (ii) A lower bound for every terminal-free T: a W_N position with Black to move
       wins x ⊞ T whenever Left wins on ⊞ T with Right to move (White's x-moves play the role of Left's passes); this gives W
       against every T with no infinite run of Right moves (all integers, \*, ↑, ↓, ±1, under, on, on + \*), and against over
       without Lemma P. (iii) An upper bound: if the T-position lies in a set S closed under Left moves in which Right always has
       a move into S (off, dud), every position outside P_L draws. (iv) The trichotomy: P_L is DEC, W_N ∖ P_L is ON, and the
       complement of W_N is DUD (D against every T, by Theorem 3.11). So the rule for the ON class is "White wins the bare
       normal-play game but not against a Black who may pass", and K40's two-bit description follows from Lemma P.
     - **The pawn on rank H−1, PROVED** (W = 3 or W ≥ 5): with White to move it is DEC unless Black's king is on the promotion
       square q; then ON if White's king is within one step of the three squares Π below the pawn, DUD otherwise. With Black to
       move: Kxp available gives DUD; bk on q (wk in Π) is ON (the bind: every Black king move loses at once, White waits inside
       Π); a Black king that can step to q gets the class of that White-to-move position; anything else is DEC. Tested on
       463,616 positions (W ∈ {3, 5, …, 9}, H ∈ {6, 7, 8}): 0 exceptions. No comparably short rule exists two ranks down (103
       and 135 relative configurations of ON with White and with Black to move).
     - **ON is not one game.** On the 8×8 cylinder, `Kc6 Pa7 ka8` (White to move) and `Kb6 Pa7 kb8` (Black to move, in check)
       are both ON, but against {0 | off} the first draws although on wins with Left to move, and the second wins although on
       draws with Right to move (PROVED). For the pawn on rank H−1 every ON position behaves exactly like on with Left to move or
       exactly like on with Right to move, against every T (PROVED); on random test games the same holds for every ON position
       on nine boards (COMPUTED-1, CONJECTURE in general). K40's tests do not separate the two movers of on.
   - **What is computed only.** Lemma P below the last rank.
>>>>>>> NEW

### EDIT 8.5b DUD and the fortresses (K49, 2026-11-23)
<<<<<<< OLD
     count and the geometry).
=======
     count and the geometry).
     - (K49, 2026-11-23.) PROVED: if Black can force Kxp against a White who may pass, x ⊞ T is D for every terminal-free T
       (step (1) of Theorem 3.11 with the colours exchanged). The converse is the absence of fortresses, which is COMPUTED only.
       The fortress geometry is sharper than stated above: with White to move the two kings are on the same back file, with
       Black to move on different back files (except 10 positions on 5×7 and 20 on 5×8, same file, rank distance 5), always at
       rank distance ≥ 2. cyl:9×8 has 522 fortress positions; cyl:7×6, 9×6 and 9×7 have none, so the fortress needs height.
       Why odd widths: only they have two adjacent back files, which lets Black's king mirror White's king round the cylinder.
       This is an explanation, not a proof (COMPUTED, `kings/delegate/out/K49/logs/fortress.log`).
>>>>>>> NEW

### EDIT 8.5c Open problems after K49 (K49, 2026-11-23)
<<<<<<< OLD
   - **Open:** a hand proof of the ON claims (no tempo needed under (N)); a rule for the parity classes beyond the
=======
   - **Open:** a hand proof of Lemma P (no reciprocal zugzwang under (N)) below the last rank, which would complete the hand
     proof of the ON claims (K49); the two-type conjecture for ON beyond the last rank (K49); a hand proof of the odd-width
     fortresses; a rule for the parity classes beyond the
>>>>>>> NEW
