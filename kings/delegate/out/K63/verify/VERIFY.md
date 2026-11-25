# K63 referee report

Referee of `kings/delegate/out/K63/` (brief `kings/delegate/briefs/K63_brief.md`), 2026-11-24. Paths are relative to
`kings/delegate/out/K63/verify/` unless they start with `kings/`. Values are in White's view: W White wins, L Black
wins, D draw.

## Verdict

- **Chess (settled by the tablebase, KNOWN).** F1 and F2 lose the structure of Definition 4.8 in chess. Black to move
  at the c4 root is a draw: every Black move draws, the shuttle included. The q after b2–b3, Black to move, is a draw,
  so it is not a mutual zugzwang. The c5 root with White to move is a draw: b2–b3, Ka3 and Kb3 all draw. Only the c4
  root keeps its structure: b2–b4 is White's only non-losing move, and its q is a mutual zugzwang.
  F3 and F4 keep the c5 (e5) root: the freeze b2–b3 (f2–f3) is White's only non-losing move and wins, and its q is a
  mutual zugzwang. Their other q (after b2–b4, f2–f4) is a draw with Black to move.
  No category other than win, draw or loss occurs, so the 50-move rule changes nothing.
  The investigator's cap-1 tables are right everywhere they decide: 111 exact values agree, and all 47 open bound
  pairs contain the tablebase value. 0 disagreements.
- **P contexts on file h: CONFIRMED.** The P results, the predictions and the counts are confirmed: 271/283, 12
  failures, 40 positions all in Black's favour, and 22 further contexts with a blocked pair that agree. I used my own
  predictor and my own P solver, which agree with the investigator on all 283 predictions and all 2,264 P values.
  The mechanism sentence needs a correction: see B4.
- Flat 8×8 against 8×7, the mirror, and the touching-file recounts: CONFIRMED (B5, C1, C2).
- Two small corrections:
  - Definition 2.1 asks F_Z to be an arc, so on the flat board d and e are group files, not buffer files.
  - The partial 2 + 2 g,h count should not go into the note.
- The investigator's EDITS.md is replaced by `EDITS.md` here.

## Claims

| # | Claim (investigator) | Verdict | Method | Label |
|---|---|---|---|---|
| A1 | Every chess value that cap 1 calls exact (F1–F4, 8 positions each, every move) | CONFIRMED: 111 of 111 equal the tablebase | Syzygy via Lichess API, `src/tb_probe.py`, `src/tb_compare.py`, `logs/tb_compare.txt` | KNOWN |
| A2 | The open cap-1 pairs (W,L), (W,D), (D,L) | CONFIRMED as bounds: all 47 contain the tablebase value; the open values are filled in below | same | KNOWN |
| A3 | "Whether F2 is exact in chess is OPEN" | SETTLED: F2 (and F1) is **not** exact in chess. Root A with Black to move is D; qB with Black to move is D; root B with White to move is D (b2–b3, Ka3, Kb3 draw; b2–b4 loses). Root A with White to move is W, b2–b4 is the only non-losing move, and qA is a mutual zugzwang. | tablebase | KNOWN |
| A4 | F3, F4: "the other freeze and its q are exact in chess" | CONFIRMED and completed. At root B (Black king c5 / e5), White to move: W, with b2–b3 (f2–f3) the only non-losing move; qB is a mutual zugzwang. At root B, Black to move: D, and the shuttle is Black's **only** non-losing move (the others lose). At root A, Black to move: W, and every move loses, the shuttle included. At root A, White to move: D, and the freeze b2–b4 (f2–f4) is the only non-losing move. qA: White to move L; Black to move D (…K×b4, …K×b5 in F3; …K×f4, …K×f5 in F4). | tablebase | KNOWN |
| A5 | "Every move value that cap 1 decides agrees with P" | CONFIRMED. Where cap 1 was open, the chess value often differs from P: for example, qB of F2 with Black to move is D in chess and W in P. | tablebase, P values from section 1 of findings | KNOWN / CHECKED-2 |
| A6 | 50-move rule "not checked" | Settled: no cursed-win, blessed-loss, maybe-win or maybe-loss anywhere in the 40 records (positions and all moves), so every result is the same with and without the rule | tablebase | KNOWN |
| A7 | Mirror `Kc5/Kc4 ka5 Pb3 Pf3 pb7 pf4` has F2's chess values with colours exchanged | CONFIRMED by the tablebase directly (8 positions, all moves; DTM values match too) | tablebase | KNOWN |
| B1 | Prediction r(ω ⊞ X) (roots), r(X) (q's) for the 283 h contexts | CONFIRMED: my predictor (`src/dpred_h.py`, written from Definitions 1.1–1.3 and Proposition 4.6) equals the investigator's prediction column in all 283 contexts | own program | CHECKED-2 (with the investigator's two) |
| B2 | Convention for r(X) | CONFIRMED: it is K47's (context pawns as a D-game of pawn moves only, a promotion a terminal win, e.p. on, a side with no move loses, infinite play a draw; `kings/delegate/out/K47/findings.txt` §3) and Lemma 4.15's (q ⊞ X has the results of 0_D ⊞ X = X). On one file there are no captures and no e.p., so X is very simple here. | reading | — |
| B3 | P values of F2 + X for all 283 h contexts (8 positions each) | CONFIRMED: my own solver (`src/pk.cpp`, which shares no code with ref3m, `kp_p` or kref) gives the same value at all 2,264 positions | own solver, `logs/h22_pk.out`, `logs/h22_referee.out` | CHECKED-2 (now three programs) |
| B4 | 271 agree, 12 differ, 40 positions, all for Black; failures exactly the contexts with Ph2 blocked by ph3, or by ph4 with h3 empty; 22 such contexts agree; qA never affected; qB 8, root B 20, root A 12; 6 draws | CONFIRMED, every count. The 22 agreeing pairs: in 16 the prediction and P are W at all 8 positions, in 5 L at all 8, and in 1 a win for the side to move. | own counts, `logs/h22_referee.out` | CHECKED-2 |
| B4' | "the Black king leaves the shuttle and wins the h2 pawn" | CORRECTED. The h2 walk is what qB (Black to move) and root B (Black to move) are won by (…Kd4–e3–f2–g1×h2, then …h3–h2–h1). At the other positions the difference comes from that: the freeze b2–b3 at root B now loses, so root B with White to move is lost (White's other moves already lose in P alone), and root A with Black to move is lost through the shuttle. The optimal lines there go through …K×f5 and the f-pawn, not h2 (lines 3 and 5 below). | hand replay | CHECKED-2 |
| B5 | Replay of the lines | CONFIRMED. Five lines of `logs/lines_h22.out` (nos. 4, 2, 3, 5, 22) were replayed move by move with `realchess.movegen` (`src/replay_lines.py`, `logs/replay_lines.out`): every move is legal and each ends with a Black promotion. My solver gives L at all 113 positions on the five lines (`logs/replay_pk.out`). The Black king takes h2 in lines 4, 2 and 22, and f5 in lines 3 and 5. | hand + own solver | CHECKED-2 |
| B6 | Touching files: gh11 125/157 (32 differ, 99 positions: 68 Black, 31 White); de11 95/157 (62, 250: 230 Black, 20 White; 24 contexts with an illegal position); gh22a partial 969/1,146 (177, 654: 289 Black, 365 White) | CONFIRMED by recount from the tables (`src/recount.py`, `logs/recount.txt`). Seven contexts (56 positions, 25 of them disagreements) were re-solved with my solver: pg6, Pg2 pg3, Pg2 pg7, pe6, Pd2 pd5, Pe2 pe7 and Pg2 Pg6 ph6 ph7. All 56 values agree, including contexts with e.p. chances next to f5. | recount + own solver | CHECKED-2 |
| B7 | "only file h is separated" (Definition 2.1) | CONFIRMED, with a wording correction. F_Z is an arc of files, here a–f; the buffer is g; h is the only context file. So d and e are group files, not buffer files (the investigator called them buffer files). Either way, no context on d, e or g is separated. | reading | — |
| B8 | gh22 partial (1,146 of 4,579 contexts, the first chunks) | Not rerun. **Recommendation: leave it out of the note.** It is not a sample, its contexts are not separated, and the 1 + 1 touching-file counts already show the effect. findings.txt keeps it. | — | — |
| C1 | Flat 8×8 against 8×7: only root-level difference is the lost double step …b6–b4 (9 non-shuttle Black root moves, not 11), and no common root or q move changes P value | CONFIRMED. The move lists agree with the rules: on 8×7 rank 6 is Black's second rank, and the q after b2–b4 has b4 occupied, so no …b4 there. My solver reproduces every 8×8 root and q move value of findings §1. Equal values on common moves follow from Definition 4.8 holding on both boards with the same freezes (K59 for 8×7). | reading + own solver (8×8) | CHECKED-2 |
| C2 | 39,859 of 883,243 common positions change value | NOT CHECKED (kept COMPUTED-1) | — | COMPUTED-1 |
| C3 | Mirror is the colour flip of F2, with the stated freezes | CONFIRMED by hand. The map r ↦ 9 − r with colours swapped sends Ka4→ka5, Pb2→pb7, Pf5→pf4, kc4→Kc5, kc5→Kc4, pb6→Pb3, pf6→Pf3; it sends b2–b4 at c4 to …b7–b5 at Kc5, and b2–b3 at c5 to …b7–b6 at Kc4. | hand | — |
| C4 | F2 exact with (B1) on flat 8×8 | Read only (K59 twice). My solver agrees with findings §1 on every root and q move value. | own solver | CHECKED-2 |

## Tablebase tables (Syzygy via the Lichess tablebase API, queried 2026-11-24 23:45–23:46 UTC; KNOWN)

Each position is given with its category for the side to move, then every legal move with the value after it (White's
view). The full FENs, board diagrams, DTZ and DTM values are in `logs/tb_probe.out`. Every FEN was built twice, once
from the piece list and once typed by hand, and the two were checked equal. The API's move list was checked equal to
`realchess.movegen`'s legal moves. No castling rights, no e.p. square (no e.p. capture is legal in any of these
positions).

```
F2  rootA Ka4 kc4 Pb2 Pf5 pb6 pf6      w: win  = W | b4 W, Ka3 L, b3+ L
F2  rootA Ka4 kc4 Pb2 Pf5 pb6 pf6      b: draw = D | b5+ D, Kd3 D, Kd4 D, Kc5 D, Kd5 D
F2  rootB Ka4 kc5 Pb2 Pf5 pb6 pf6      w: draw = D | b3 D, Ka3 D, Kb3 D, b4+ L
F2  rootB Ka4 kc5 Pb2 Pf5 pb6 pf6      b: draw = D | Kd4 D, Kd5 D, Kc6 D, Kd6 D, b5+ W, Kc4 W
F2  qA    Ka4 kc4 Pb4 Pf5 pb6 pf6      w: loss = L | Ka3 L, b5 L
F2  qA    Ka4 kc4 Pb4 Pf5 pb6 pf6      b: loss = W | Kc3 W, Kd3 W, Kd4 W, b5+ W, Kd5 W
F2  qB    Ka4 kc5 Pb3 Pf5 pb6 pf6      w: loss = L | Ka3 L, b4+ L
F2  qB    Ka4 kc5 Pb3 Pf5 pb6 pf6      b: draw = D | Kd4 D, Kd5 D, Kc6 D, Kd6 D, b5+ W
F1  rootA Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6  w: win  = W | b4 W, Ka3 L, b3+ L
F1  rootA Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6  b: draw = D | b5+ D, Kd3 D, Kd4 D, Kc5 D
F1  rootB Ka4 kc5 Pb2 Pe4 Pe5 pb6 pe6  w: draw = D | b3 D, Ka3 D, Kb3 D, b4+ L
F1  rootB Ka4 kc5 Pb2 Pe4 Pe5 pb6 pe6  b: draw = D | Kd4 D, Kc6 W, Kc4 W, b5+ W
F1  qA    Ka4 kc4 Pb4 Pe4 Pe5 pb6 pe6  w: loss = L | Ka3 L, b5 L
F1  qA    Ka4 kc4 Pb4 Pe4 Pe5 pb6 pe6  b: loss = W | Kc3 W, Kd3 W, Kd4 W, b5+ W
F1  qB    Ka4 kc5 Pb3 Pe4 Pe5 pb6 pe6  w: loss = L | Ka3 L, b4+ L
F1  qB    Ka4 kc5 Pb3 Pe4 Pe5 pb6 pe6  b: draw = D | Kd4 D, Kc6 W, b5+ W
F3  rootA Ke4 kc4 Pb2 Pb5 Pf5 pb6 pf6  w: draw = D | b4 D, Ke3 L, Kf3 L, Kf4 L, b3+ L
F3  rootA Ke4 kc4 Pb2 Pb5 Pf5 pb6 pf6  b: loss = W | Kb4 W, Kb3 W, Kc5 W, Kxb5 W
F3  rootB Ke4 kc5 Pb2 Pb5 Pf5 pb6 pf6  w: win  = W | b3 W, Ke3 L, Kf3 L, Kd3 L, Kf4 L, b4+ L
F3  rootB Ke4 kc5 Pb2 Pb5 Pf5 pb6 pf6  b: draw = D | Kc4 D, Kb4 W, Kd6 W, Kxb5 W
F3  qA    Ke4 kc4 Pb4 Pb5 Pf5 pb6 pf6  w: loss = L | Ke3 L, Kf3 L, Kf4 L
F3  qA    Ke4 kc4 Pb4 Pb5 Pf5 pb6 pf6  b: draw = D | Kxb4 D, Kxb5 D, Kb3 W, Kc3 W
F3  qB    Ke4 kc5 Pb3 Pb5 Pf5 pb6 pf6  w: loss = L | Ke3 L, Kf3 L, Kd3 L, Kf4 L, b4+ L
F3  qB    Ke4 kc5 Pb3 Pb5 Pf5 pb6 pf6  b: loss = W | Kd6 W, Kb4 W, Kxb5 W
F4  rootA Kc4 ke4 Pb5 Pf2 Pf5 pb6 pf6  w: draw = D | f4 D, Kb3 L, Kc3 L, Kb4 L, f3+ L
F4  rootA Kc4 ke4 Pb5 Pf2 Pf5 pb6 pf6  b: loss = W | Kf4 W, Kf3 W, Ke5 W, Kxf5 W
F4  rootB Kc4 ke5 Pb5 Pf2 Pf5 pb6 pf6  w: win  = W | f3 W, Kb3 L, Kc3 L, Kd3 L, Kb4 L, f4+ L
F4  rootB Kc4 ke5 Pb5 Pf2 Pf5 pb6 pf6  b: draw = D | Ke4 D, Kf4 W, Kd6 W, Kxf5 W
F4  qA    Kc4 ke4 Pb5 Pf4 Pf5 pb6 pf6  w: loss = L | Kc3 L, Kb3 L, Kb4 L
F4  qA    Kc4 ke4 Pb5 Pf4 Pf5 pb6 pf6  b: draw = D | Kxf4 D, Kxf5 D, Ke3 W, Kf3 W
F4  qB    Kc4 ke5 Pb5 Pf3 Pf5 pb6 pf6  w: loss = L | Kb3 L, Kc3 L, Kd3 L, Kb4 L, f4+ L
F4  qB    Kc4 ke5 Pb5 Pf3 Pf5 pb6 pf6  b: loss = W | Kd6 W, Kf4 W, Kxf5 W
mirror Kc5 ka5 Pb3 Pf3 pb7 pf4         w: draw = D | b4+ D, Kc4 D, Kd4 D, Kd5 D, Kd6 D
mirror Kc5 ka5 Pb3 Pf3 pb7 pf4         b: win  = L | b5 L, Ka6 W, b6+ W
mirror Kc4 ka5 Pb3 Pf3 pb7 pf4         w: draw = D | Kc3 D, Kd3 D, Kd4 D, Kd5 D, b4+ L, Kc5 L
mirror Kc4 ka5 Pb3 Pf3 pb7 pf4         b: draw = D | b6 D, Ka6 D, Kb6 D, b5+ W
mirror Kc5 ka5 Pb3 Pf3 pb5 pf4         w: loss = L | Kd5 L, Kc6 L, Kd6 L, b4+ L, Kd4 L
mirror Kc5 ka5 Pb3 Pf3 pb5 pf4         b: loss = W | Ka6 W, b4 W
mirror Kc4 ka5 Pb3 Pf3 pb6 pf4         w: draw = D | Kc3 D, Kd3 D, Kd4 D, Kd5 D, b4+ L
mirror Kc4 ka5 Pb3 Pf3 pb6 pf4         b: loss = W | Ka6 W, b5+ W
```

Questions of the brief, in chess (with and without the 50-move rule; no special categories):

| | shuttle Black's only non-losing root move? | freeze White's only non-losing root move? | q mutual zugzwang? | roots (A b, A w, B b, B w) |
|---|---|---|---|---|
| F1, F2 | no: at A every move draws; at B Kd4 (F2 also Kd5, Kc6, Kd6) draws | at A yes (b2–b4 wins); at B no (b2–b3, Ka3, Kb3 draw) | qA yes; qB no (Black to move draws) | D, W, D, D |
| F3, F4 | at B yes (the shuttle draws, the rest lose); at A every move loses | yes at both (at A the freeze only draws) | qB yes; qA no (Black to move draws by a king capture) | W, D, D, W |

A drawing line from F2's qB with Black to move (`src/tb_walk.py`, `logs/tb_walk.out`, 20 requests; both sides pick
among drawing moves, preferring promotions, captures and pawn moves): 1…Kd4 2.Kb4 Kd3 3.Ka4 Ke3 4.b4 Ke4 5.Kb5 Kxf5
6.Kxb6 Ke4 7.b5 f5 8.Ka5 f4 9.b6 f3 10.b7 f2 11.b8=Q f1=Q, queen against queen, a draw. In P, White's promotion would
end the game.

## Not checked

- The 39,859 changed positions between flat 8×7 and 8×8 (COMPUTED-1 as reported). My solver is 8×8 only.
- The 2 + 2 g,h contexts (partial run). Not rerun, as instructed.
- Touching-file contexts beyond the seven re-solved. The rest rest on ref3m and `kp_p` (CHECKED-2 by the investigator).
- The direct D-sums r(F2 ⊞ X) with vgsum59 (COMPUTED-1) and F2's (B1) were not rerun (K59 has them CHECKED-2).
- Mechanism labels of the touching-file lines (`src/classify_lines.py`). Not checked.

## Programs, runs, budget

- `src/tb_probe.py`, `src/tb_walk.py`: `realchess.probe.Prober(cap=150)` used read-only with its own ledger
  (`tb_ledger.jsonl`) and cache (packed as `logs/tbcache.tar.xz`). **60 HTTP requests** in all (40 positions + 20 on
  the drawing line), no errors, no other network use.
- `src/tb_compare.py`: the comparison with the cap-1 tables (no network).
- `src/dpred_h.py`: the D-sum predictor.
- `src/pk.cpp`: my P solver (flat 8×8). It splits positions by pawn configuration, solves the configurations in an
  order where pawn moves are irreversible, and does a retrograde count of the king moves inside each configuration;
  e.p. is evaluated by one ply. It was built in the scratch directory only; no binary is left here.
- `src/run_h22.py`, `src/replay_lines.py`, `src/recount.py`: drivers and recounts.
- `src/hrun.sh`: every solver run goes through `kings/delegate/heavy.sh` under `/usr/bin/time -l`, with a watchdog that
  kills only its recorded solver PID above 2.2 GB. It never fired. PIDs are in `pids.log`.
- Peak memory (maximum resident set size):
  - h contexts: 0.21 GB (29 min)
  - lines: 0.19 GB
  - spot checks: **1.61 GB**, the largest. The 2 + 2 g,h context has 192,368 pawn configurations at 8 KB each.
- I made one direct test run of pk on F2 alone (8 positions, 0.3 s) outside heavy.sh before I wrote hrun.sh.
  The first spot-check wrapper was killed by me while it was still waiting for a slot, because its watchdog had picked
  the slot-wait `sleep`. hrun.sh was fixed and the run repeated (see pids.log).
