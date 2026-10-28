## 1. Claims, labels and reproduce commands

Notation: `R=/Users/aritro/Downloads/Research/Chessendgames`, `K=$R/kings/delegate/out/K27`, `PY=$R/.venv/bin/python`, `export PYTHONPATH=$R`.
Binaries (private builds, deleted at the end): `cc -O2 -o $K/work/kp $R/kings/kpsolve.c -lpthread`,
`cc -O2 -o $K/work/kpp $R/kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread`,
`c++ -O2 -std=c++17 -o $K/work/ref3 $R/kings/delegate/out/K23/verify/ref3.cpp`, same for `ref3m.cpp`. Input files are in `logs/`
(`roots16.txt`: the 8 roots of Z_B then the 8 of the mirror; `children52.txt`: the 52 non-shuttle children).

| # | claim | label | reproduce |
|---|---|---|---|
| 1 | the 8 roots of Z_B and the 8 of its mirror have P-value D | CHECKED-2 (kpp, ref3; pm.py a third time, no forced win within 25 plies) | `kpp --board flat:7x6 --ep on --promote QRBN --cap 1 --pmodel --moves < logs/roots16.txt`; `ref3 --board flat7x6 < logs/roots16.txt`; `PY scripts/pm_roots.py logs/roots16.txt` (log: `logs/pm_roots.log`) |
| 2 | the move lists at the 16 roots: 26 non-shuttle moves per group (15 White, 11 Black), the shuttle is the only move valued D | CHECKED-2 (kpp, ref3m; pm.py a third time) | `logs/roots_kpp.log`, `logs/roots_ref3m.log`, `PY scripts/t1.py logs/roots16.txt 21` |
| 3 | shuttle legal and safe in both directions at all 8 roots (K1, K2, Lemma S) | PROVED (hand, `PROOF.md` section 3) | by hand; also in claim 2 |
| 4 | each of the 26 non-shuttle moves loses by force in P, at most 11 plies after the move | PROVED (hand-checkable certificates, 286 entries, `PROOF.md` section 6); every cited position and every reply independently valued by kpp and ref3m | `PY scripts/verify_certs.py logs/children52.txt $K/work/kpp $K/work/ref3m` (log `logs/verify_certs.log`: 409 opponent positions, 2,642 reply values, 626 leaves, 0 problems) |
| 5 | **Z_B alone is exactly two-shuttle in P**: (D, D) at all 8 roots, neither side can win against a shuttling opponent | **PROVED** | `PROOF.md` section 7 (from claims 3, 4) |
| 6 | the mirror group is tau(Z_B), tau = rank flip + colour swap + side swap, a symmetry of the P model and of chess; hence claims 1-5 hold for the mirror | PROVED (symmetry); machine check of the 8 roots and of equivariance of the legal moves on 22,818 positions | `PY scripts/tau_check.py logs/roots16.txt` (log `logs/tau_check.log`); certificates for all 52 children verified in claim 4 |
| 7 | in P no en passant arises in Z_B play | PROVED (no pawn ever stands on its second rank) | `PROOF.md` section 1 |
| 8 | K14's count of "27 non-shuttle moves" is wrong: 26 per group (4+1+4+4+4+2+3+4) | CHECKED-2 | lists in claim 2 |

## 2. What the hand proof is

`PROOF.md` section 4 lists every legal move at the 8 roots with the reasons the other moves are illegal. Section 6 gives, for
each of the 26 deviations, the opponent's winning strategy as a list of entries: the position, the winner's move, the complete
list of replies (with the reason every other king move or pawn move is illegal), and for each reply either a further entry or
an immediate promotion. The mechanisms are three: (a) a *runner* (b3-b2 or c4-c3 and the White king is too far, 3 plies: Kc3 to d2, d4, xc4 and
Black's Kxa3 / White's b4-b5); (b) the *pair* b3+c3 (or the White pair a4+b4 with check on a5/b5) against a king on the first rank (or a Black king on
the sixth rank), which is the bulk of the king-retreat cases; (c) a *pawn push that is captured* (b4-b5, a3-a4, c4-c3, b3-b2), after
which the side that won the pawn wins the remaining race, sometimes after a waiting move of the shuttle (a zugzwang). The longest
certificates are b4-b5 from (b2, a4) (37 entries) and b3-b2 from (c3, b5) (36 entries).
Termination is by the number `d` (plies to the promotion), which falls by at least 2 along every arrow. Nothing in the proof depends on the
solvers, which were used to find the lines and to check every position cited.

All 26 lines are PROVED; none was kept at CHECKED-2 for being too long.

## 3. Chess status (no P rule: the first promotion does not end the game)

| code | root | deviation | evidence (kpsolve, `--board flat:7x6 --cap 1`, chess) | chess verdict |
|---|---|---|---|---|
| C04 | Z1 (b2,a4) White | b4-b5 | capture Kxb5: `Kb2 Pa3 / kb5 pb3 pc4`, White to move: (L, L) exact | loses for White: **COMPUTED-1** |
| C05 | Z2 (b2,a4) Black | c4-c3 | capture Kxc3: `Kc3 Pa3 Pb4 / ka4 pb3`, Black to move: (W, L) | open |
| C09 | Z3 (b2,b5) White | a3-a4+ | capture Kxb4: `Kb2 Pa4 / kb4 pb3 pc4`, White to move: (L, L) | loses for White: **COMPUTED-1** |
| C13 | Z4 (b2,b5) Black | c4-c3 | capture Kxb3: `Kb3 Pa3 Pb4 / kb5 pc3`, Black to move: (W, W) | loses for Black: **COMPUTED-1** |
| C14 | Z5 (c3,a4) White | Kxc4 | child `Kc4 Pa3 Pb4 / ka4 pb3`, Black to move: (W, L), 7.7 CPU-s, 93 MB, 19.75 M states, 187 layers | open |
| C17 | Z5 (c3,a4) White | b4-b5 | capture Kxb5: `Kc3 Pa3 / kb5 pb3 pc4`, White to move: (L, L) | loses for White: **COMPUTED-1** |
| C18 | Z6 (c3,a4) Black | Kxa3 | child `Kc3 Pb4 / ka3 pb3 pc4`, White to move: (W, L), 8.0 CPU-s, 99 MB, 20.96 M states, 201 layers | open |
| C19 | Z6 (c3,a4) Black | b3-b2 | capture Kxb2: `Kb2 Pa3 Pb4 / ka4 pc4`, Black to move: (W, W) | loses for Black: **COMPUTED-1** |
| C22 | Z7 (c3,b5) White | a3-a4+ | capture Kxa4: `Kc3 Pb4 / ka4 pb3 pc4`, White to move: (W, L) | open |
| C26 | Z8 (c3,b5) Black | b3-b2 | capture Kxb2: `Kb2 Pa3 Pb4 / kb5 pc4`, Black to move: (W, W) | loses for Black: **COMPUTED-1** |
| the other 16 | king moves (C01-C03, C06-C08, C10-C12, C15, C16, C20, C21, C23-C25) | | children have 4 pawns: more than one CPU-minute each at cap 1; the batch of the 24 four-pawn children (`work/ch_ZB.txt`) was queued under `heavy.sh` and never got a slot | not computed (open) |

A capture position that is exact at cap 1 (A = B) and a win for the capturer shows that the child, with the capturer to move, is a win for the capturer: the capturer plays that capture.
Values are from White's point of view, "(A, B)" being the two bounds of SPEC.md. Reproduce (each under one CPU-minute, `nice -n 15`):
`echo "<position>" | $K/work/kp --board flat:7x6 --cap 1`; all eight capture positions: `scripts/cap1_each.sh $K/work/capt8.txt out` (log `logs/chess_cap1_capture_positions.log`; the two children: `logs/chess_cap1_kxc4_child.log`, `logs/chess_cap1_kxa3_child.log`).
Only kpsolve was used for chess (no second chess implementation was run), so these are COMPUTED-1.

### Cap 2

The one-position probe was run as asked: the Kxc4 child `Kc4 Pa3 Pb4 ka4 pb3 b -` (3 pawns), `kp --board flat:7x6 --cap 2 --threads 2`,
under `heavy.sh` and `scripts/watch.sh` (kills its own recorded PID if RSS passes 3 GB). It did **not finish**: after 20 minutes wall
(618 CPU-s user, 15 s sys) I killed my own PID 374. Polled peak RSS 147 MB, `getrusage` maximum resident set 151 MB (log
`logs/cap2_probe.err.txt`). So memory was not exceeded, but kpsolve prints nothing until the end and the run was nowhere near done, so
this is no measurement of the final requirement. **Extrapolation** (`scripts/layers_estimate.py`, `logs/layers_estimate.log`), which
over-approximates the layers (white pawns, black pawns, officer multiset) visited and counts 2 * 42^(2+k) states for k officers: at cap 1 it gives
33.6 M states for the Kxc4 child against 19.75 M measured (ratio 0.59), and 51.6 M for the Kxa3 child against 20.96 M measured (ratio 0.41). At cap 2 it
gives 1.04 G states for the Kxc4 child (about 0.4-0.6 G real, at the measured 4.7 bytes per state about 2-3 GB, with a CPU time of the order of
hours), 1.36 G for the Kxa3 child, and **10.2-10.8 G for the 4-pawn children (about 4-6 G real states, over 20 GB)**. Cap 2 is therefore not run for any
of the 26 children: it needs more than 3 GB for the 4-pawn children, and for the 3-pawn ones it is at the limit in memory and far beyond 20 minutes in time.

### Hand arguments (labelled, none is a proof)

* HA1 (mechanism; one line checked by hand, no proof). In P the certificates end when a pawn promotes, whatever happens to the new piece. In chess the new
  queen can be captured at once by the king: after the deviation 1.Kc3-d2 (C15) b3-b2 2.Kc2 Black may not play b1=Q because of Kxb1, so the 3-ply P certificate does not carry
  over. What carries over is the pair: 2...c4-c3! (b2 is now protected; 3.Kxc3? b1=Q wins since Kc3 is not next to b1) 3.Kb1 c3-c2+ 4.Ka2 b2-b1=Q#
  (the queen is protected by the pawn on c2 and the king on a2 has no square). That is one line against one defence; I did not complete a chess proof of any 4-pawn child.
* HA2 (CONJECTURE). In the Kxc4 and Kxa3 children (3 pawns) cap 1 gives (W, L): the bounds differ only because both sides can promote
  (e.g. Kxc4 child: b3-b2, b4-b5, b2-b1=Q, b5-b6=Q is a capped second promotion; there Black's queen on b1 attacks b6 along the open b-file and
  wins the new queen by Qxb6+). This suggests that the first queen wins in chess here, but that is not a proof.
* So: 6 of 26 deviations are shown to lose in chess (COMPUTED-1); 4 have bounds (W, L) at cap 1; 16 are not computed. Z_B being (D, D) in chess would need all 26.

## 4. State of Z_B (what to write)

* **(i) Z_B is exactly two-shuttle in P: PROVED** (and CHECKED-2). Also for the mirror group (tau).
* **(ii) Z_B in chess: undecided.** cap 1 gives (W, L) at the roots (K14 referee); of the 26 deviations 6 are shown to lose in chess (COMPUTED-1), 4 are open at cap 1, 16 not computed; cap 2 is not feasible within the limits.
  CONJECTURE that it holds.
* **Open:** chess (cap 2); the per-context conjecture (P-results of G + Z_B equal those of G + dud_D in every context; 225 of 885 contexts untested by the
  K14 referee, not touched here); the cylinder and other boards; whether a chess-specific group exists whose deviations are punished also in chess.

## 5. Proposed LOOPY edits

`EDITS.md` (OLD texts checked to occur exactly once in the current `kings/theory/LOOPY.md`, which already contains K14's edits).

## 6. Housekeeping and disclosures

* Everything was written inside `kings/delegate/out/K27/`; no git; no existing file edited.
* Heavy runs: the cap-2 probe ran under `heavy.sh` (slot waited about 16 minutes, then got it) with `watch.sh`. The cap-1 batch of the 24 four-pawn children
  (`work/ch_ZB.txt`, `heavy.sh ... kp --cap 1 --threads 2`, wrapper PIDs 35063/35066) was queued at 16:12 and had not obtained a slot after about 70 minutes of waiting (the two slots were held by other jobs and re-taken by other waiters); I killed the waiting wrapper (own PIDs) at the end, so there is no output. The cap-1 bounds of the 16 king-move children are therefore not available.
* Runs outside the lock, each under one CPU-minute and `nice -n 15`: the two 3-pawn cap-1 runs (7.7 and 8.0 CPU-s), the small calibration runs, and all pm.py / verify scripts.
* My own mistakes, disclosed: (1) my very first cap-1 batch of 52 children was started without the lock; it was over a CPU-minute, I killed it (own PID 29149) after about 2 minutes, nothing was kept. (2) I then started a sequential unlocked loop of single runs (`cap1_each.sh`, CPU limit 58 s each); the first 4-pawn position exceeded the limit, so I killed it (own PIDs) and kept only the 3-pawn positions. (3) A calibration `kp --cap 2` run (pid 99894) had no memory guard (`ulimit -v` is not supported on this macOS); I killed it at once at about 25 CPU-s and 13 MB, and relied on the watchdog-guarded probe instead. All PIDs are recorded in `logs/pids.log`. No pkill, killall or pattern kill was used.
* Bulk inputs, outputs and binaries (`work/`) were deleted at the end; no file over 50 MB was ever created.
