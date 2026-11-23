### EDIT 8.5a The ON class: the hand reduction to one computed fact (K49, 2026-11-23; revised by the K49 referee)
<<<<<<< OLD
   - **What is computed only.** That an ON position needs no spare tempo and is not hurt by up to 12 Black spares.
     No number and no infinitesimal occurs, so Gafni's on\* and {on | 0} do not appear, and neither does 1\* (against a
     second-hand summary; the source was not located). A tie of on with on + \* cannot be split by these tests.
=======
   - No number and no infinitesimal occurs, so Gafni's on\* and {on | 0} do not appear, and neither does 1\* (against a
     second-hand summary; the source was not located). A tie of on with on + \* cannot be split by these tests.
   - **The ON claims, reduced to one computed fact** (new, K49, 2026-11-23; `kings/delegate/out/K49/PROOF.md`; every hand
     step re-derived by one referee of the same model family, `kings/delegate/out/K49/VERIFY.md`). Under (N), with W ≠ 4,
     write W_N for White's wins in the bare game x ⊞ 0.
     - **Lemma P (no reciprocal zugzwang):** for every placement with Black not in check, if White wins with Black to move
       then White wins with White to move. CHECKED-2 on K40's twelve boards (it is the −1 column of K40's tables) and on
       cyl:3×10, 5×10, 9×8 and 10×10 (K49's `scripts/kn.c` and the referee's own solver `verify/vk.c`); COMPUTED-1 (kn.c)
       on the other cyl:W×H with W ∈ {3, 5, …, 10}, 4 ≤ H ≤ 10. False on cyl:4×H for H = 4, …, 10 (8, 8, 12, 16, 20, 24 and
       28 violations, CHECKED-2; in every one White to move draws), so there a single Black spare turns some wins into draws,
       one source of the 4-file tempo thresholds; the 4-file Black wins have another cause (White stalemated, K40 Lemma 2). PROVED by hand for the pawn on rank H−1, so everything
       below is PROVED outright for the pawn on rank H−1.
     - **Given Lemma P, PROVED by hand:** (i) r(x ⊞ n) = r(x ⊞ 0) for **every** integer n, not only |n| ≤ 12. Black's spares
       never help: White plays her W_N strategy and answers a Black spare from a W_N position via Lemma P; the pair (spares
       left, stage) decreases. White needs none: outside W_N, a White pass (by Lemma P) and every White move stay outside
       W_N, and Black always has a move that stays outside W_N or takes the pawn, so White never wins x ⊞ on. (ii) A lower
       bound for every terminal-free T: a W_N position with Black to move wins x ⊞ T whenever Left wins on ⊞ T with Right
       to move (White's x-moves play the role of Left's passes); this gives W against every T with no infinite run of Right
       moves (all integers, \*, ↑, ↓, ±1, under, on, on + \*), and against over without Lemma P. (iii) The trichotomy: P_L
       is DEC, W_N ∖ P_L is ON, and the complement of W_N is DUD (D against every T: White never wins x ⊞ on, as in (i),
       and Theorem 3.11). So the rule for the ON class is "White wins the bare normal-play game but not against a Black who
       may pass", and K40's two-bit description follows from Lemma P. On the boards where Lemma P is CHECKED-2 or
       COMPUTED-1, (i)–(iii) carry that label, not PROVED.
     - **PROVED without Lemma P:** if the T-position lies in a set S closed under Left moves in which Right always has a
       move into S (off, dud), every position outside P_L draws.
     - **The pawn on rank H−1, PROVED** (W = 3 or W ≥ 5, H ≥ 4): with White to move it is DEC unless Black's king is on the
       promotion square q; then ON if White's king is within one step of the three squares Π below the pawn, DUD otherwise.
       With Black to move: Kxp available gives DUD; bk on q (wk in Π) is ON (the bind: every Black king move loses at once,
       White waits inside Π); a Black king that can step to q (then wk is in Π) is ON as well; anything else is DEC. 0
       exceptions on all 463,616 such positions of cyl:W×H, W ∈ {3, 5, …, 9}, H ∈ {6, 7, 8} (COMPUTED-1, kn.c); the referee's
       solver confirms the rule and the types on cyl:3×6, 5×6, 7×7, 8×8 and 9×8 (166,710 positions). Two ranks down ON has
       103 and 135 relative configurations with White and with Black to move (W ≥ 7); no short rule was found there.
     - **ON is not one game.** On the 8×8 cylinder, `Kc6 Pa7 ka8` (White to move) and `Kb6 Pa7 kb8` (Black to move, in check)
       are both ON, but against {0 | off} the first draws although on wins with Left to move, and the second wins although on
       draws with Right to move (PROVED; both solvers agree). For the pawn on rank H−1 every ON position behaves exactly like
       on with Left to move or exactly like on with Right to move, against every T (PROVED); on random test games the same
       holds for every ON position on nine boards (COMPUTED-1, CONJECTURE in general). K40's tests do not separate the two
       movers of on.
   - **What is computed only.** Lemma P for the pawn below rank H−1.
>>>>>>> NEW

### EDIT 8.5b DUD and the fortresses (K49, 2026-11-23; revised by the K49 referee)
<<<<<<< OLD
     count and the geometry).
=======
     count and the geometry).
     - (K49, 2026-11-23.) PROVED: if Black can force Kxp against a White who may pass, x ⊞ T is D for every terminal-free T
       (step (1) of Theorem 3.11 with the colours exchanged). The converse is the absence of fortresses, which is COMPUTED only.
       The fortress geometry is sharper than stated above: with White to move the two kings are on the same back file, with
       Black to move on different back files (except 10 positions on 5×7 and 20 on 5×8, same file, rank distance 5), always at
       rank distance ≥ 2. cyl:9×8 has 522 fortress positions; cyl:7×6, 9×6 and 9×7 have none, so on 7 and 9 files the
       fortress needs more ranks than on 5 (CHECKED-2: K49's kn.c and the referee's own solver give the same counts and
       geometry). A heuristic for odd widths: only they have two adjacent back files, which may let Black's king mirror White's
       king round the cylinder (3 files, where the back files are the pawn's neighbours, have no fortress). This is an
       explanation, not a proof (`kings/delegate/out/K49/logs/fortress.log`).
>>>>>>> NEW

### EDIT 8.5c Open problems after K49 (K49, 2026-11-23)
<<<<<<< OLD
   - **Open:** a hand proof of the ON claims (no tempo needed under (N)); a rule for the parity classes beyond the
=======
   - **Open:** a hand proof of Lemma P (no reciprocal zugzwang under (N)) for the pawn below rank H−1, which would complete
     the hand proof of the ON claims (K49); the two-type conjecture for ON below rank H−1 (K49); a hand proof of the
     odd-width fortresses; a rule for the parity classes beyond the
>>>>>>> NEW
