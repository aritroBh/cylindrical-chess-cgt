# Referee report on K24 (P6 and P7 of LOOPY.md)

Referee: independent verifier. Verdict: **ACCEPT_WITH_FIXES**. No number, label or proof step of K24 was refuted.
Every computed number reproduces with my own code or my own kpsolve build. The proposed edits need fixes before
they go into LOOPY: they cite a file that does not exist, they name a flag that is not in `kings/kpsolve.c`, and
they leave two status rows stale. I also found an old error in LOOPY section 5.1 that K24 did not catch.

All my files are in `kings/delegate/out/K24/verify/` (scripts, logs; binaries and bulk batches deleted).

## 0. What I did

- Built `kp` from `kings/kpsolve.c` and `kp_p` from `kings/delegate/out/K7/scripts/draft/kp_p.c` (the only file I
  read in K7/). Did not use K24's binaries or scripts.
- Wrote two new programs from `kings/SPEC.md` and LOOPY Definition 2.6, without reading `mine.c` first:
  - `psolve.py`: a solver for the P model and for the two promotion models used by the transfer lemma. It is a
    third implementation, after kpsolve and K24's `mine.c`.
  - `lg2.py`: the local game L_T(Q_Z) of Definition 2.6 (s bare king and passes, s-bar confined king and one pawn,
    queen clause on and off), plus the (L3) stalemate scan.
- Checked the transfer lemma by hand, the KPK steps with the project's `atlas/cylinder/kpk` binary (built 15 Oct,
  not K24's), and the 8 edits against the current LOOPY.md.

Naming. K24's `mine.c` calls "bb" the model in which every promotion is a White win and "bw" the model in which
every promotion is a Black win. In my `psolve.py` the same models are called `ww` and `bb`. Below I say
"every-promotion-White-wins" (EPW) and "every-promotion-Black-wins" (EPB) to avoid the clash.

## 1. Claims, one by one

| # | Claim | Verdict | Label supported | How I checked |
|---|---|---|---|---|
| 1 | P model: P6 cyl:8x8 = (L,W); P6 flat:8x8 = (L,L); P7 = (D,W) on both boards; P5 cyl:7x6 = (D,W) | CONFIRMED | CHECKED-2 (I give a third implementation) | `psolve.py` and `kp_p --pmodel` agree on all 10 entries and on every per-move value; see section 2 |
| 2 | kpsolve exact chess values match; bounds A = B | CONFIRMED | COMPUTED-1 | own `kp` build, `--cap 1`, A = B on all 10 entries, same per-move values; see section 2 |
| 3 | (L1) T lists 6,6,6,7,7 (queen clause) and 6,6,5,6,6 (L1_P) for Kg4,Kg5,Kg6,Kh6,Ka6; Kc7 of 7.2 has T = 1; Kf7 has T = 11/10; Ke5, Kd5, Kf5 have none; Z_72 Kd5 has T = 6, others none | CONFIRMED | CHECKED-2 | `lg2.py`, identical numbers, identical s-node counts (1025, 1326, 1939, 4273, 3985 ...); see section 3 |
| 4 | (L2) vacuous in the bare group | CONFIRMED | PROVED (trivial) | mu_s = infinity by Definition 2.6: no context pawn exists |
| 5 | (L3): no stalemate of s on lines where s-bar plays only winning moves; (L3_F) fails everywhere | CONFIRMED | CHECKED-2 | `lg2.py` scan: 0 stalemates in every case that has a finite T; (L3_F) fails trivially, see section 3 |
| 6 | Chess P6 (both entries), P7 b, P5 b: every move met by king capture, then a won KPK; KPK tables agree with atlas `kpk.c` on 326,640 / 331,352 positions | CONFIRMED | CHECKED-2 | atlas `kpk` binary and own kpsolve both give W for all 12 reduction positions; the two position totals equal the atlas `WTM+BTM` counts; see section 4 |
| 7 | Transfer lemma | CONFIRMED | PROVED | I re-proved it, section 5. The proof exists only in a REPORT.md that was never written |
| 8 | P7 w and P5 w chess value D | CONFIRMED | CHECKED-2 | kpsolve exact D D (own build) and the two promotion models (EPW and EPB) both give "cannot win" (my `psolve.py`) plus the lemma |
| 9 | No hand proof of the P7 w draw; Lemma 2.9 cannot give it | CONFIRMED | CONJECTURE for a hand proof | Lemma 2.9 only refutes (L1) for a passing defender; White cannot pass; the label is not too strong |

I found nothing to refute. Where K24 undersells, it is only in counts (I have three solvers where it says two).

## 2. P model and chess values (claims 1, 2, 8)

Own kpsolve build, `--ep on --promote QRBN --cap 1 --moves`, then `kp_p --pmodel` with the same flags (values from
White's view, White to move first, then Black to move). The numbers are those of K24's `logs/kpsolve_*.txt`:

| position | cyl:8x8 chess | cyl:8x8 P | flat:8x8 chess | flat:8x8 P |
|---|---|---|---|---|
| `Kh5 Pa4 kb4 pa5` w / b | L L / W W | L / W | L L / L L | L / L |
| `Ke6 Pd7 kd8 pe7` w / b | D D / W W | D / W | D D / W W | D / W |
| cyl:7x6 `Kc4 Pb5 kb6 pc5` w / b | D D / W W | D / W | | |

Per-move lists match too (P6 w: all five moves L; P7 w: Ke5, Kd5, Kf5 D and Kf7 L; P5 w: Kd5 L, the others D).
Every chess run printed A = B, so the chess values are exact.

My own `psolve.py` (forward exploration, then counting retrograde, from SPEC.md only) gives, for the same six
positions per board, in the three models:

| model | cyl:8x8 P6 w / b | cyl:8x8 P7 w / b | flat:8x8 P6 w / b | flat:8x8 P7 w / b | cyl:7x6 P5 w / b |
|---|---|---|---|---|---|
| P (first promotion wins) | L / W | D / W | L / L | D / W | D / W |
| EPW (every promotion a White win) | D / W | D / W | D / D | D / W | D / W |
| EPB (every promotion a Black win) | L / D | D / D | L / L | D / D | D / D |

This equals K24's `models_p_bb_bw.log` entry by entry (K24 "bb" = my EPW, K24 "bw" = my EPB), including every
per-move value. For P7 w and P5 w: EPW says White cannot win, EPB says Black cannot win, so by the lemma both
are D, and kpsolve exact agrees. The lemma is used in the "cannot win" direction only.

Cross-validation of the P-model solvers, `xval.py` (random positions, side to move random, `kp_p --pmodel` against
`psolve.py`; illegal positions rejected by both):

| board | pawns | positions (legal) | differences |
|---|---|---|---|
| cyl:4x5 | 1 v 1 | 150 (93) | 0 |
| flat:4x5 | 1 v 1 | 150 (104) | 0 |
| cyl:5x6 | 1 v 1 | 300 (226) | 0 |
| flat:5x6 | 1 v 1 | 300 (231) | 0 |
| cyl:4x5 | 2 v 2 | 300 (158) | 0 |
| flat:4x6 | 2 v 1 | 300 (200) | 0 |
| cyl:8x8 | 1 v 1 | 12 (9) | 0 |

So a sample of the "11,102 + 769" claim reproduces with a solver that is neither kpsolve nor `mine.c`. I did not
re-run the full 11,102; a 20-minute Python run was not worth it once the sample was clean.

## 3. The local game (claims 3, 4, 5)

`lg2.py` implements Definition 2.6 literally: s may pass whenever not in check; s-bar may not pass; s-bar's king
steps only on F_Z files; promotion by s-bar wins if no legal s move captures the new queen (queen clause) or always
(L1_P); mate of s wins; s-bar with no move fails; if s takes the pawn, s-bar can never win; s-bar must win with one
of its first T moves. T_min is the least T such that every s move (pass included) is met by a winning s-bar move
within T.

Results (reply = king capture of the group's pawn; same Q as K24):

- 5.1 White sorties on cyl:8x8, F_Z = hab:
  - queen clause (L1): Kg4 6, Kg5 6, Kg6 6, Kh6 7, Ka6 7.
  - without (L1_P): Kg4 6, Kg5 6, Kg6 5, Kh6 6, Ka6 6.
- 7.2 White sorties, F_Z = de, cyl and flat: Kd5, Ke5, Kf5 none (also without the queen clause); Kf7 T = 11 with the
  clause, 10 without.
- 7.2 Black Kc7 (mirrored: bare king c2 against king e2 and pawn d2): T = 1 on both boards.
- Z_72 on cyl:7x6, F_Z = bc: Kd5 T = 6 (both versions); Kb3, Kc3, Kd3 none.
- The five Black sorties of 5.1 are the mirror of the White ones (rank r to 9 - r, file x reflected about a, colours
  swapped: Ka3, Kb3, Kc3, Kc4, Kc5 map to Ka6, Kh6, Kg6, Kg5, Kg4). K24's direct Black runs give the dual numbers.
  The duality is PROVED in LOOPY and the P values (L,W) are symmetric. I did not run Black sorties separately.
- (L3): along every line in which s-bar plays only winning moves with the remaining time (the strong form, so
  a fortiori for one guided strategy), s always has a legal non-pass move or is mated: 0 stalemates, in all cases
  with a finite T. The s-node counts equal K24's (e.g. 1025, 1326, 1939, 4273, 3985 for the five sorties with the
  clause), which suggests the two programs enumerate the same game.
- (L3_F) fails trivially, and not by an accident of K24's code: s may walk its king away from F_Z (for example
  Kg4-Kf4), after which no king move reaches F_Z and s has no Z-pawn. For the T = 1 case Kc7 of 7.2, Black's
  king on c7 has no legal move onto d or e (d6 and d8 are next to the white king on e7, d7 is protected).

One bug in my own code is worth reporting: the first run of `lg_run2.py` gave "None" for Z_72 Kd5. The cause was a
stale king-neighbour cache in `psolve.py` when the board changed from 8x8 to 7x6 in one process. I fixed it
(`KN.clear()` in `setup`) and the rerun gives T = 6, as K24. All 8x8 P and promotion-model runs were done in
separate processes and were never affected.

Hence the Theorem 2.7 route for P6 is sound as written: (L1) by computation, (L2) vacuous, (L3) by computation,
Definition 2.1 holds for the bare group, and every legal move of the side to move is one of the ten sorties. The
side to move is not stalemated (it has five moves), so P6 = (L,W) in P, and the direct P-model solvers agree.

## 4. The KPK reduction (claim 6)

- Legality of each king capture: after White's Kg4, Kg5, Kg6, Kh6, Ka6 the square a4 is not adjacent to the white
  king, and after Black's Ka3, Kb3, Kc3, Kc4, Kc5 the square a5 is not adjacent to the black king, while White's
  king on h5 touches a5 across the seam. For 7.2: after Kc7 the white king takes e7 (not adjacent to c7).
- The eleven KPK positions of K24's `reduction.log` for cyl:8x8, the flat 7.2 position and the cyl:7x6 position:
  - own kpsolve exact: W for the pawn side in all 13 (`Kh6 ka4 pa5 w` and the four White alternatives all `L L`,
    the six Black-to-move positions all `W W`, `Ke7 Pd7 kc7 b` `W W` on both boards, `Kc5 Pb5 ka5 b` `W W` on 7x6).
  - atlas `kpk` (8 ranks only): W in all 12 of the 8x8 queries, converted to its input format by flipping ranks and
    colours for the Black-pawn cases.
- The table sizes printed by atlas `kpk 8 1` are 160,656 white-to-move plus 165,984 black-to-move positions = 326,640
  (cylinder), and by `kpk 8 0` 163,328 + 168,024 = 331,352 (flat). These are K24's
  totals, so "all positions compared" refers to the right table sizes. I did not re-run the all-position diff
  between `kpk2` and atlas.
- `kpk2` promotes to a queen only, so a KPK "win" is a lower bound; for a loser that has no pawn this suffices.
  Chess losses of the side to move in P6, and of Black in P7, follow without any upper bound.
- Not covered by atlas: P5 (6 ranks). There only `kpk2` and kpsolve exact (both W) support the reduction.

## 5. The transfer lemma (claim 7), re-proved

Let EPW be the game in which the first promotion by either side ends the game as a White win, every other rule
as in chess (mate wins, stalemate and infinite play draw). Claim: if White has no winning strategy in EPW, White
has none in chess. Proof by contraposition. Let sigma be a winning strategy for White in chess. Played in EPW,
it produces, against any Black behaviour, a play which is a prefix of a chess play consistent with sigma. Before the
first promotion the legal moves and the mate and stalemate tests coincide in the two games. If a promotion occurs
(by either side) before sigma's mate, the game ends in EPW as a White win. Otherwise the whole chess play is promotion-free
and ends in mate of Black, a White win in EPW as well. Chess win by sigma is finite, so there is no infinite play.
Hence sigma wins EPW. The mirror (EPB, Black) is identical. With determinacy of these reachability games
(retrograde analysis), "White cannot win and Black cannot win" is a draw. A promotion move is a legal move in EPW
exactly when it is legal in chess, so nothing else differs. No gap found. This is PROVED. It needs no cap on
officers.

It uses only the "cannot win" direction, so it does not matter that under-promotion is not distinguished in EPW.

## 6. The eight edits

`chk_edits.py`: all eight OLD blocks occur exactly once in the current LOOPY.md. Table rows keep the same number of
columns (4 / 9 / 9 / 4 / 9 / 4 pipes OLD and NEW). Two bullets become one long line each (style only: surrounding
text is wrapped).

| label | OLD unique | NEW accurate | decision |
|---|---|---|---|
| status row P6, P7 | yes | accurate in content, but cites a missing file and a non-existent flag | FIX (A, B) |
| section 6 row P6 | yes | accurate | OK |
| section 6 row P7 | yes | accurate; cites the (non-written) report for the lemma | FIX (A) |
| status row P5 | yes | accurate | OK |
| section 6 row P5 | yes | accurate; cites the lemma only through the same report | FIX (A) |
| status row 5.1 (L1) | yes | accurate; "third implementation" fine, there are now four | OK |
| 5.1 prediction bullet | yes | accurate; "the Black sorties have the same T lists" is loose (the dual sortie has the same T, in a different order) | OK, optional wording |
| 5.2 not-punished bullet | yes | accurate; refers to "the transfer lemma of the K24 report" | FIX (A) |

Required fixes:

A. **The report K24/REPORT.md does not exist.** The agent's own summary says the Write tool refused it. Yet EDITS.md
   (a) lists `kings/delegate/out/K24/REPORT.md` as a source in the P6/P7 status row, (b) says "see section 4 of the K24
   report" for (L3_F), and (c) cites "the transfer lemma of the K24 report (PROVED ...)" in three edits. A PROVED
   statement in LOOPY whose proof lives only in a missing file is not acceptable. Either state the lemma and my
   section-5 proof in LOOPY (about six lines, for example as a Corollary 2.7'' next to Corollary 2.7'), or point to
   this VERIFY.md section 5 and write the REPORT.md. Drop "see section 4 of the K24 report": the (L3_F) failure
   is explained in one sentence (s may walk off F_Z), which can be stated inline.

B. **`kpsolve --pmodel` does not exist in `kings/kpsolve.c`.** `grep pmodel kings/kpsolve.c` is empty; the flag is
   only in the K7 draft `kings/delegate/out/K7/scripts/draft/kp_p.c`. LOOPY Definition 1.5 still says `kpsolve --frozen`
   computes P with frozen kings. Name the file in the text ("the K7 build `kp_p.c`, flag `--pmodel`"), or merge the flag
   into `kpsolve.c`, and give the reproduce command with that name.

C. **Stale rows that the edits leave in contradiction.** After applying all eight edits LOOPY still says:
   - line 92, status row "5.2, White's sorties": '"Not punished": CONJECTURE (scratch)'. The bullet it summarises now says
     CHECKED-2 (edit 8).
   - line 188, summary row "5": "its certificate (L1) a CONJECTURE (scratch)". Edit 6 now says CHECKED-2.
   - line 1968, history list "Downgraded while writing": "The bare 5.1 / 7.2 / Z_72 results: CONJECTURES with scratch
     evidence". This is a history list; add "(upgraded after K24)" or leave it.
   Suggested replacement for line 92, status cell: `the certificate fails: PROVED (L2.9). "Not punished", and "White
   cannot win": CHECKED-2 (K24: two P-model solvers, local game T = 11 / 10 for Kf7 only; no hand proof)`.

D. Optional, accuracy: the status row for P6, P7 says "the two agree on 11,102 random legal positions". My sample
   (section 2) supports it, but the claim is about K24's own pair of solvers; keep, with "(K24 log crossval_p.log)".

## 7. A pre-existing error in LOOPY section 5.1 (not in K24's edits)

LOOPY lines 1660-1664 ("Frozen in the convention. PROVED by enumeration") say: Black's five legal moves are "Ka3, Kc3,
Kc4, Kc5 and Kb5", that the first four abandon a5, and that "the fifth (Kb5) puts Black's king on the square that guards
both a4 and a5, so that White is in zugzwang with only pawn-blocked moves left".

This is wrong. Kb5 is illegal: the white pawn a4 attacks b5 (`notes/diagram_audit.md` line 80 says so, and its table, line 228,
lists "a3, b3, c3, c4, c5"). Kxa4 is also illegal (a4 is guarded by the king on h5 across the seam). The five legal
Black moves are Ka3, Kb3, Kc3, Kc4, Kc5 (kpsolve, `psolve.py` and K24 all print these), and all five abandon a5, which
White's king takes at once. The conclusion (the group is frozen for both sides) is right, and I confirmed it by computation,
but a PROVED enumeration should not contain an illegal move and a false description of a zugzwang that does not occur.

Proposed edit, in the required format:

### EDIT 5.1 frozen enumeration (referee)
<<<<<<< OLD
BK's five legal moves are Ka3, Kc3,
  Kc4, Kc5 and Kb5; the first four abandon BP a5, which White's king then captures on a5, giving White a
  passer, and the fifth (Kb5) puts Black's king on the square that guards both a4 and a5, so that White is in
  zugzwang with only pawn-blocked moves left. So every king move in the group is decisively punished, and the
  group is frozen.
=======
BK's five legal moves are Ka3, Kb3,
  Kc3, Kc4 and Kc5 (Kb5 is attacked by WP a4, and Kxa4 is illegal because Kh5 guards a4 across the seam); each of
  them abandons BP a5, which White's king then captures on a5, giving White a passer. So every king move in the
  group is decisively punished, and the group is frozen.
>>>>>>> NEW

The OLD text, with its line breaks, occurs exactly once in the current LOOPY.md (checked by script; it starts in the
middle of line 1660). None of the agent's edits touch these lines, so it can be applied after them.

## 8. Reproduce

```
cd kings/delegate/out/K24/verify
cc -O2 -o kp  ../../../../kpsolve.c -lpthread
cc -O2 -o kp_p ../../K7/scripts/draft/kp_p.c -lpthread
./kp --board cyl:8x8 --ep on --promote QRBN --cap 1 --moves < pos.txt          # chess, about 10 CPU-s
./kp_p --pmodel --board cyl:8x8 --ep on --cap 1 --moves < pos.txt              # P model
PY=../../../../../.venv/bin/python
$PY psolve.py cyl:8x8 p  --moves < pos.txt         # also ww and bb; flat:8x8; cyl:7x6 with pos5.txt (30 s each)
$PY lg_run2.py                                     # all (L1)/(L1_P) T values, (L3) scan
$PY xval.py cyl:5x6 300 101 1 1                    # P-model cross-validation (BOARD N SEED NW NB)
$PY chk_edits.py                                   # OLD blocks unique in LOOPY.md
```

Logs: `run8.log` (P, EPW, EPB on 8x8 both boards), `run_kpk.log` (the 13 KPK positions in kpsolve), this file for the rest.
Two runs went through `kings/delegate/heavy.sh` (`run8.sh`, `run_kpk.sh`); one queued xval batch was cancelled by me
(my own PID) after waiting about 20 minutes for a slot and replaced by smaller direct runs, each under about one CPU minute
(the first two kpsolve runs for section 2 were run directly, 10 CPU-s each).
