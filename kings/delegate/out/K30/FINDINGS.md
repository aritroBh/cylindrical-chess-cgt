# K30 FINDINGS: a hand proof that White cannot win from P7 w (LOOPY section 8, open question 7)

1. P7 w (`Ke6 Pd7 kd8 pe7`, White to move) is a draw. PROVED by hand on cyl:8x8 and flat:8x8, in P, EPW, EPB and in chess directly (Lemma 2.7a is not needed). Mechanically checked. The proof is `PROOF.md`.
2. White cannot win: its four legal moves (Ke5, Kd5, Kf5, Kf7; Kd6, Kf6, Kxe7 are illegal) all leave d7 unprotected, Black plays ...Kxd7, and a lone king can neither promote nor mate. In EPW Black adds a rule that never promotes (a king always has a move, Lemma K).
3. Black cannot win after Ke5, Kd5 or Kf5: White follows an explicit blockade rule rho that moves every turn (no pass), with an invariant S of 918 positions per board (Lemma D). The other Black replies (...Kc7, ...e6, ...e5) are met by Ke6 or by taking the pawn. This is the content of open question 7: the objection "White cannot pass" does not apply.
4. Kf7 loses in P (PROVED): ...e5 and the pawn runs with the king on d8; the White king is too far by the rule of the square (Black promotes after four more pushes, 10 plies from X). Not claimed for chess, and not needed.
5. The strategies are coded as finite rules and checked with my own move generator (written from SPEC.md): S is closed over all 6,777 (cyl) and 5,985 (flat) Black moves; my values agree with K24's `mine.c` (P, EPW, EPB) and K7's `kp_p --pmodel` (P) on 15,536 and 15,695 positions, 0 differences. Not covered: the 6-rank analogue P5, other board sizes. Referee K30 (`VERIFY.md`): ACCEPT_WITH_FIXES, every count reproduced with independent code. `EDITS.md` has 11 edits (referee wording).

## What was proved (outline; every step is in PROOF.md)

- **Statement 0.** At X White has exactly Ke5, Kd5, Kf5, Kf7. The pawn d7 cannot move (d8 is occupied).
- **A (White cannot win).** After any of the four moves, ...Kxd7 is legal (d7 is two or more steps from the White king).
  White then has a king only. In P, EPB and chess nothing more is needed. In EPW Black must not promote: rule tau,
  "never move the pawn, move the king to a free non-corner neighbour"; Lemma K (a king whose neighbours are not all
  attacked or blocked: at most 3 are attacked by a king two steps away, at most 1 is blocked by the own pawn) shows
  Black always has such a move.
- **B (Black cannot win after a sortie).** Black's replies after a sortie are Kxd7, Kc7, e6 and (after Kd5 or Kf5) e5.
  - ...Kxd7: king and Black pawn e7 against king. Lemma D. The invariant S (Black to move, pawn on e_r): the White king
    on one of F = e_{r-1}, M = e_{r-2}, L = d_{r-2}, R = f_{r-2}, with b unrestricted for F and M, b outside the zone
    {f,g} x [r-3, r] for L (mirror for R), plus exact lists for r = 3 and r = 2. The rule rho: capture the pawn if
    possible; from F go to M; from M go to F, else to the opposition square on the black king's file; from L or R go
    to M, else F; after a pawn check go to the square below the pawn. Lemma D: every Black move is answered inside S, by
    capturing the pawn, or by a stalemate; Black never has a promotion and White is never mated.
  - ...Kc7: Ke6. Then ...Kd8 is X again (the play repeats: a draw); otherwise Kxe7.
  - ...e6 or ...e5: Kxe6 or Kxe5.
  - After the pawn is gone ("free mode") White plays king moves only, never the pawn; Lemma K says it always has one.
- **C.** Kf7 e5: Black pushes every turn with the king on d8. White's king is on rank at least 8 - k before its k-th
  move, so it can neither capture nor block the pawn.

## Results of the checks

All runs are under about one CPU-minute (the longest, `compare.py`; the referee measured about 12 s of CPU for its own longest run), run at `nice -n 15`, under 300 MB RSS.
No `heavy.sh` call was needed. Logs are in `logs/`.

| Check | cyl:8x8 | flat:8x8 |
|---|---|---|
| `check_kpk.py`: positions of S (r = 7,6,5,4: 201 each; r = 3: 112; r = 2: 2) | 918 | 918 |
| (position, Black move) pairs, rule reply legal and inside S / capture / White stalemate | 6,777 (4,308 / 2,467 / 2) | 5,985 (3,736 / 2,247 / 2) |
| distinct White-to-move positions arising | 1,488 | 1,488 |
| reached from the three starts: Black-to-move / White-to-move | 151 / 348 | 151 / 348 |
| `check_A.py`: White's moves at X | Ke5 Kd5 Kf5 Kf7 | same |
| Black's rule tau (EPW): White-to-move / Black-to-move states | 3,348 / 3,348 | 3,164 / 3,164 |
| Kf7 e5 line: White-to-move states; promotion at depth 4 in all lines | 52 | 47 |
| `check_B.py`: White-to-move states for Ke5 / Kd5 / Kf5 (free mode: 3,341 cyl, 3,385 flat) | 3,694 / 3,696 / 3,696 | 3,738 / 3,740 / 3,740 |
| `compare.py`: positions valued; differences own vs `mine.c` (P, EPW, EPB) and vs `kp_p --pmodel` (P) | 15,536; 0 | 15,695; 0 |
| all positions of S and their successors are D (P, EPB); no sigma position is L; no tau position is W (EPW) | yes | yes |

Value sets from the own solver on those positions: cyl P {W 6,333; D 4,983; L 4,220}, EPW {W 6,363; D 9,173},
EPB {D 11,316; L 4,220}; flat P {W 6,421; D 5,030; L 4,244}, EPW {W 6,451; D 9,244}, EPB {D 11,451; L 4,244}.
The three solvers were written from `kings/SPEC.md`: `kpm.py` (this task; no code of the others was read), `mine.c` (K24),
`kp_p.c` (K7, shares source with kpsolve). `mutation_tests.py` shows the closure check rejects a damaged S.

The strategies are not read from solver tables: `k30lib.py` codes S, rho, sigma and tau exactly as written in PROOF.md,
and the generator only supplies the legal moves.

## Labels

| Claim | Label |
|---|---|
| Statement 0 (four moves, three illegal) | PROVED, confirmed by the generator |
| A: White cannot win (P, EPW, EPB, chess) | PROVED, with a mechanical check |
| B: Black cannot win after Ke5, Kd5, Kf5 (P, EPW, EPB, chess) | PROVED (Lemmas D and K), with a mechanical check of all of S and of sigma, both boards |
| C: Kf7 loses in P | PROVED, with a mechanical check; chess not claimed |
| X = D in chess, both boards | PROVED directly; agrees with K24 (Lemma 2.7a) and kpsolve exact |
| Same values from three programs on 15.5k positions per board | CHECKED-2 |
| P5 (Z_72 on cyl:7x6) and other board sizes | not covered (the method should carry over; nothing was run) |

The proof was re-derived by a referee (VERIFY.md, ACCEPT_WITH_FIXES; fixes applied). The mechanical check is of the rules, not a replacement for reading Lemma D.

## What I did not do, and the boundary of the negative results

- I did not run kpsolve on chess (cap 1) again; the chess value of X is K24's (CHECKED-2) and now also PROVED here.
- I did not extend the proof to P5 or to boards other than 8x8.
- The invariant S is not the largest set of drawn positions. The exact drawn set is larger (for example, with the pawn on
  e7 and the black king on d7 and Black to move, the White king also draws from d3 and e3, by the distant opposition). S
  is only what the proof needs. For r = 3 and 2 the lists are exact for the rule, not for the game.

## Exact commands

    cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K30/scripts
    export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
    PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
    # private builds (deleted at the end; rebuild to rerun compare.py)
    mkdir -p ../bin
    cc -O2 -o ../bin/kpp  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread
    cc -O2 -o ../bin/mine /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K24/scripts/mine.c
    for b in cyl:8x8 flat:8x8; do
      nice -n 15 $PY check_kpk.py $b     # Lemma D: closure of S, 918 positions, both boards
      nice -n 15 $PY check_A.py   $b     # statement 0, part A (tau, EPW), part C (Kf7)
      nice -n 15 $PY check_B.py   $b     # sigma for Ke5, Kd5, Kf5
      nice -n 15 $PY compare.py   $b     # own solver vs mine.c (p, bb, bw) vs kp_p --pmodel
    done
    nice -n 15 $PY mutation_tests.py cyl:8x8
    python3 build_edits.py               # rewrites ../EDITS.md from the current LOOPY.md (each OLD must occur once)
    python3 /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/apply_edits.py \
        /Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md /tmp/x.md ../EDITS.md   # dry run, writes only /tmp/x.md

## Files

- `PROOF.md`: the proof. `EDITS.md`: 11 edits (checked against the LOOPY.md of 2026-10-28 01:48-ish; all applied in a dry run). `summary.json`.
- `scripts/`: `kpm.py` (own generator and solver), `k30lib.py` (rules), `check_kpk.py`, `check_A.py`, `check_B.py`,
  `compare.py`, `mutation_tests.py`, `build_edits.py`; `scripts/explore/` holds earlier exploratory scripts (not part of the proof).
- `logs/`: one log per check and board, `compare_positions_*.txt` (the positions compared). `pids.log`: processes I started.
