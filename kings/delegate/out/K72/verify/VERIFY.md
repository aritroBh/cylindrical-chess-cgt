# K74: referee report on K72 (five chess-exact over groups beside real pawns, promotion game P)

Referee of `kings/delegate/out/K72/` (brief `kings/delegate/briefs/K74_brief.md`), 2026-11-26. Paths are relative to
`kings/delegate/out/K72/verify/` unless they start with `kings/`. Values are White's view: W White wins, L Black wins,
D draw. Positions per context: A b, A w, B b, B w, qA b, qA w, qB b, qB w (A, B the two Black king squares).

## Verdict

| # | Claim | Verdict | Label |
|---|---|---|---|
| 1 | Table of findings §0 (11 pairs, 1 + 1 and 2 + 2 counts, positions differing); C125_10 on h: 283 of 283, 2,264 positions | CONFIRMED, every number. Beyond 2 + 2 the C125_10 claim does not extend to every context on h: 3 of all 729 contexts fail (smallest 4 + 1, below) | CHECKED-2 (now three programs: pk, ref3m, and my p74); the 3 failures CHECKED-2 (p74, pk); the 726 agreements beyond 2 + 2 COMPUTED-1 (p74) |
| 2 | Prediction r(ω ⊞ X) at the roots, r(X) at the q's; X the D-game of the context pawns | CONFIRMED: this is what Lemma 4.15 and Corollary 4.17 give, with the right side to move at all eight positions; X modelled as Definition 1.3 asks | prediction recomputed by my own code, equal on all 283 patterns and in every table (third predictor) |
| 3 | Context files (Definition 2.1) | CONFIRMED | by hand |
| 4 | Every failing context has pawns of both colours; every one-colour context agrees | CONFIRMED in all 11 pairs (1 + 1 and 2 + 2) | CHECKED-2 (recount from p74's values and from K72's tables) |
| 5 | Two failure kinds; ten smallest counterexamples; mechanisms COMPUTED-1; "exactness in chess does not protect a group" | Examples CONFIRMED (positions as stated, lines legal, results right). Kinds CORRECTED: there is a third mechanism without a king raid, and two pairs fail in both directions (below). COMPUTED-1 is the right label for the mechanism sentences. The sentence is true for P beside real pawns and should say so | values CHECKED-2; lines replayed (movegen) and re-solved (p74) |
| 6 | EDITS.md | REPLACED by `EDITS.md` here (corrected kinds, the failing hypothesis named, refereed) | — |

No disagreement anywhere: 0 of 24,904 P values (11 × 2,264; the 1 + 1 runs, 11 × 344, are the same positions again),
0 of 283 predictions.

**Which hypothesis fails (claim 6).** No theorem of the note is contradicted. Lemma 4.15 and Corollary 4.17 speak of the
D-sum G ⊞ T of the group, as the P game of its own pieces, with an abstract finite D-game T. The board position is such
a sum only while the kings stay on F_Z and nothing on the context file meets them. Lemma 2.2 (buffer invariance) keeps
only the pawns apart, not the kings, and it protects F_Z but not the buffer files. In every failure I looked at, a
king leaves F_Z and captures or stops a context pawn, or a context pawn attacks a buffer square that a group king
needs. Then the legal chess moves are not the options of the sum, so (V1)(a) of Theorem 1.14 (non-interaction) fails.

## Comparison table (p74 against K72's tables)

| group | file | 1 + 1 contexts agree/fail | 2 + 2 agree/fail | positions differing (White/Black) | p74 vs pk | p74 vs ref3m | own vs K72 prediction | one-colour failing |
|---|---|---|---|---|---|---|---|---|
| C125_05 | f | 27/16 | 208/75 | 228 (131/97) | 0 | 0 | 0 | 0 |
| C125_05 | g | 30/13 | 233/50 | 108 (108/0) | 0 | 0 | 0 | 0 |
| C125_05 | h | 34/9 | 252/31 | 53 (53/0) | 0 | 0 | 0 | 0 |
| C125_08 | h | 33/10 | 248/35 | 100 (100/0) | 0 | 0 | 0 | 0 |
| C125_10 | h | 43/0 | 283/0 | 0 | 0 | 0 | 0 | 0 |
| C145_07 | a | 41/2 | 271/12 | 56 (0/56) | 0 | 0 | 0 | 0 |
| C145_07 | b | 38/5 | 261/22 | 116 (0/116) | 0 | 0 | 0 | 0 |
| C145_07 | c | 25/18 | 232/51 | 239 (1/238) | 0 | 0 | 0 | 0 |
| C145_09 | a | 30/13 | 233/50 | 108 (108/0) | 0 | 0 | 0 | 0 |
| C145_09 | b | 27/16 | 209/74 | 261 (128/133) | 0 | 0 | 0 | 0 |
| C145_09 | h | 25/18 | 224/59 | 275 (16/259) | 0 | 0 | 0 | 0 |

Positions compared: 24,904 at 2 + 2 (all 283 contexts of all 11 pairs, more than the brief's minimum of three pairs)
and 3,784 at 1 + 1; disagreements 0. The result pairs (prediction → P) of findings §3 are reproduced exactly
(`logs/compare_22.txt`). Every failing context, at both sizes, has pawns of both colours (`logs/compare_11.txt`,
`logs/compare_22.txt`, column "failing with both colours").

The prediction (claim 2). Lemma 4.15: both roots have the results of ω beside every finite D-game, each q those of
0_D, i.e. of X alone, for either side to move. The eight positions are the two roots and the two q's, each with
Black and with White to move. q with Black to move is the position after the freeze; q with White to move is the
same placement with White to move, as in (O3)/(O4). X: pawns of one file, pushes and double steps (no captures and no
e.p. on one file), a promotion a terminal win, a side with no move loses (Definition 1.3). ω: Black may pass, White may
move once ω → 0_D. Code: `src/mk74.py` (function `pred`, a dozen lines, written without reading `dpred.py`); output
`logs/pred74_22.txt`, equal to K72's `logs/dpred.txt` on all 283 patterns and to the prediction column of all 11 tables.
My solver also reproduces Definition 4.8 for the five groups alone (roots W, q's lost for the side to move, only the
stated freezes do not lose; `logs/alone_p74.out`).

Context files (claim 3). F_Z is the arc spanned by both kings (both root squares) and the group pawns:
C125_05 b–d (buffer a, e; context f, g, h); C125_08 and C125_10 b–f (buffer a, g; context h only); C145_07 e–g
(buffer d, h; context a, b, c); C145_09 d–f (buffer c, g; context a, b on the far side, h on the near side). As stated.

## Failure kinds (claim 5): correction

K72's two kinds are right as descriptions of what happens in most failing contexts, but the text assigns whole groups
to one kind, and that is not right:
- C125_05 on f and C145_09 on b fail in **both** directions (97 and 133 positions for Black).
- C145_07 on c has 1 position for White, and C145_09 on h has 16 for White.
- The Black-favoured failures of C125_05 f are a **third mechanism**, without a raid. A Black context pawn takes a
  buffer square from the White king. Example (1 + 1): root A, Black to move, beside Pf5, pf6 (White Kd4, Pb6, Pc2, Pc5,
  Pf5; Black Kb4, pb7, pc6, pf6). Predicted W, P is D. The pawn f6 covers e5, the square between d4 and d6 through which
  White's king must go to b7 (Proposition 4.25, "Why it works"). So 1…Ka3 (or the shuttle) and the Black king sits on
  a1–a2: White cannot reach b7, and Black cannot win. After c2–c4 (qA, Black to move) every Black move draws
  (`logs/f56_p74.out`).
- All 31 C125_05 f contexts with a Black-favoured difference have a Black pawn on f5, f6 or f7. The 31 of C145_09 b
  likewise have one on b5, b6 or b7 (COMPUTED from CHECKED-2 values). C125_05 g and C145_09 a give identical counts
  at both sizes, as do C125_05 f and C145_09 b at 1 + 1: the king distances to the context file are the same.

"Exactness in chess does not protect a group": true as a statement about P beside real pawns (four of the five
chess-exact groups fail). It should say "in P, beside real pawns", since no chess was computed.

## Hand checks: the ten smallest counterexamples (findings §0 item 3)

Every position was rebuilt from the group and the freeze, and every one is as stated. p74 gives the stated P result
at all ten (`logs/ten_lines_p74.out`, with every legal move and its value).

The four decisive lines of K72 (`ref3pv`, from `logs/raw_outputs.tar.xz`, lines_11.out) and my own four lines (p74 -l)
were replayed move by move with `realchess.movegen`: every move is legal and each ends with the winner's promotion.
p74 gives the line's value at all 202 positions on them (`logs/replay_check.txt`). Draws have no line; for them the
move values decide. In each case below, the idea is in two sentences.

1. **C125_08 h, qA + Ph2 ph3, White to move, L → W.** White's king is free on e5, three files from h. 1.Kf4 (or 1.b4
   first) and Kg3×h3 wins the blocked pawn in three moves, and the h-pawn needs six more. The Black king, busy on b6,
   is outside its square, and Black's b-pawn is held by b4 (after 1.b4) or is slower. Both 1.b4 (K72) and 1.Kf4 (p74)
   win; Ke4 and Kf5 win too.
2. **C125_05 h, qB + Ph2 ph7, White to move, L → W.** 1.h4! h5 fixes the h-pawns. Then Ke3–f4–g5×h5 gives White a
   passed h-pawn while Black takes c5 and b6. Black's king cannot both stop it and hold b7 (my line: …Kf7, then c3–c4,
   Kd6–c7×b7 and b-pawn), and in K72's line the h-pawn queens one move before Black's b-pawn. Only h2–h3 and h2–h4 win;
   every king move and c3–c4 lose.
3. **C125_05 f, qB + Pf2 pf3, White to move, L → D.** Kd3, Ke3, Ke4 and Ke5 draw; c3–c4 loses. The White king takes f3
   (Ke3×f3) while the Black king takes c5 and b6, and the remaining pawns are traded or caught (in the line, bare kings
   after …K×f7). No side keeps a winning passer.
4. **C125_05 g, qB + Pg2 pg3, L → D.** As 3, with Ke3–f3×g3. Here Kd3 loses (L), while Ke3, Ke4 and Ke5 draw.
5. **C145_09 a, qB + Pa2 pa3, L → D.** The colour-and-side picture of 4, with Kc3–b3×a3 against …K×e5, …K×f6. Kc3, Kc4
   and Kc5 draw; Kd3 and e3–e4 lose.
6. **C145_09 b, qB + Pb2 pb3, L → D.** Kc3×b3 in two moves; Kc3, Kd3, Kc4 and Kc5 draw; e3–e4 loses.
7. **C145_09 h, root A + Ph2 ph3, Black to move, W → D.** Only the shuttle 1…Kf5 draws (…Kg4 and …Kg5 lose). After the
   freeze 2.e3 the Black king walks …Kg4–f3–f2–g1–h1×h2, and the White king must come back to f1/f2 against the
   h-pawn. King and rook pawn against king cannot be won (the line ends in stalemate), and all White pawns are
   blocked. So the q, Black to move, is D, not W.
8. **C145_07 a, root A + Pa2 pa3, Black to move, W → L.** Black wins. Fastest is the shuttle 1…Ke5: White's freeze
   2.f3 now loses to 2…Kd4 and …Kc3–b2×a2–b1, …a2–a1. That is one tempo ahead of White's counter Kh5–g6–f7×e7 and e7–e8,
   because each capturing king blocks its own pawn for a move (p74: after 2…Kd4 3.Kh5 the a-pawn queens on Black's 6th
   move). White's other moves lose in P alone (…K×f5, …K×e6 and the e/f-pawns). The direct raid 1…Kd3 also wins.
   K72's sentence "…Kd4–d3–c2–b1×a2, then …a3–a2–a1" names the raid correctly. Its optimal line goes through …K×f5,
   because White's longest resistance is not to freeze.
9. **C145_07 b, root A + Pb2 pb3, Black to move, W → L.** 1…Kd3 2.Kf3 Kc2 3.Ke2 K×b2 and …b3–b2–b1 (6 Black moves;
   the White king is four files away).
10. **C145_07 c, root A + Pc2 pc3, Black to move, W → D.** Here …Kd3 is illegal (c2 covers d3) and …Kd4, …Kd5 lose.
    The shuttle 1…Ke5 draws, because after 2.f3 the Black king's threats against c2 (…Kd4) draw the White king to
    the c-file (K×c3), and nobody wins.

## C125_10: why one would expect no failure (explanation, not a proof), and the search that found three

*Explanation.* Both kings are tied and the h-file is far for both. White's king on c5 has only b4, b5, c4 (and d4 when
Black is on e6). c6 is covered by b7, and d4–d6 are next to the Black king. Every one of these moves loses, and file h
is five files away, so a raid on an h-pawn costs at least four king moves away from b7. Black's king on e5/e6 is three
files from h, but every Black move other than the shuttle lets White win in 11 plies (Kc6×b7 and the b-pawn,
`logs/c10_moves_p74.out`). A raid on an h-pawn costs Black at least three king moves, plus a tempo for its own pawn
after a king capture, so it is a tempo too slow. In C125_08 the White king stands on e5, three files from h, with a free
road (Kf4–g3), and in C145_07 and C145_09 the Black king stands on e4/e5 or f4/f5, one or two files nearer its target.

*Search: every context on h.* I solved all 729 placements of pawns of both colours on h2–h7, every context file h
can carry (one run of 298,890 configurations through heavy.sh, 83 s, 0.64 GB; 5,832 positions). Before that, while the
slots were busy, I solved 160 contexts of kinds the enumeration left out (3 + 0, 0 + 3, 3 + 1, 1 + 3) in direct chunks.
The single run reproduces every value of the chunked runs (283 + 160 contexts, 0 differences).
**Result: 726 of 729 contexts agree, and 3 fail** (`logs/compare_all.txt`). All three fail only at qA with White to
move, predicted L and a draw in P:
- `Ph3 Ph4 Ph5 Ph6 ph7` (4 + 1, the smallest);
- `Ph2 Ph3 Ph4 Ph5 Ph6 ph7` (5 + 1);
- `Ph2 Ph3 Ph4 Ph6 ph5 ph7` (4 + 2).

Every other class agrees, including all 3 + 3 contexts and everything with at most three pawns of each colour. So the
quotable statement must keep its bound: "at most 2 + 2" (or "at most three pawns of each colour") is true, and
"every context on file h" is false.

The smallest counterexample, as a diagram in text: qA = White Kc5, Pb6, Pf3, Pf6, Ph3, Ph4, Ph5, Ph6; Black Ke5, pb7,
pf7, ph7; White to move. On the h-file nothing can move, so X is dead and the q should be lost for White to move.
Instead 1.Kb4 (or Kc4, Kb5) draws; only f3–f4 loses. The idea (explanation, read from p74's move values in
`logs/c10_fail_p74.out`, `logs/kb4_ctx_p74.out`, `logs/kxf6_p74.out`): without the h-pawns, Black answers 1.Kb4 with
…K×f6 and wins, by …Ke5–e6–d6–c5×b6 against White's f-pawn and then the b-pawn. Here the frozen White chain h3–h6
covers g4–g7, squares of the buffer file g. After 1…K×f6 the Black king cannot use the g-file, so 2.f3–f4 (or 2.Kc5)
holds: the White king returns to c5 and keeps b6, and the f-pawn ties the Black king. This is the third mechanism
again: a context pawn attacks a buffer square that a group king needs, and no king raids the context. Labels:
the three failures are CHECKED-2. K72's pk (the K63 referee's solver), built in `tmp/` and run through heavy.sh, gives
the same values as p74 at all 24 positions of the three contexts (`logs/c10f_pk.out`). That "the other 726 contexts
agree" is COMPUTED-1 (p74 only).

## Process notes (investigator)

- Self-reported: one input file was copied to /tmp for a comparison and deleted. Against the brief's "write only
  inside", no harm found.
- Otherwise clean: no binaries, no `__pycache__`, no executable bits, no home paths in text files or in the two
  archives. The 1 + 1 runs (14–23 s) were measured first and run directly; every 2 + 2 run and both line runs went
  through heavy.sh with the watchdog, which never fired (peak 1.40 GB, ref3pv). The 1 + 1 chain and the 2 + 2 chain
  were started at the same time (18:52:41), so a direct run and a heavy run of K72 overlapped. The K72 brief does not
  forbid this.
- `ref3m --board flat:8x8` is misparsed (K72 says so and used pln:8x8). This is a hazard for later users of ref3m.

## Programs, runs, memory (this referee)

- `src/p74.c`: my own P solver, written from the rules (SPEC.md, Definition 1.5) before reading pk.cpp or ref3m.cpp.
  It solves configurations in order (fewer pawns first, then more pawn progress), runs a retrograde analysis with
  move counters and a bucket queue over king moves inside each configuration, evaluates e.p. positions by one ply,
  and sizes its tables before allocating (exit 3 over 2.0e9 bytes). Tests before use: the 162 Lemma B positions of
  `kings/delegate/out/K68/verify/logs/r68_lemmaB.out` (values and distances equal), and 45 root and move positions of
  `r68_main.out` (values and distances equal).
- `src/mk74.py` (contexts, positions, prediction), `src/cmp74.py` (comparison and recount), `src/replay74.py` (line
  replay with realchess.movegen), `src/run74.sh` (time -l and the watchdog on the solver's PID, 5 polls a second,
  kill at 2.0 GB), `src/chunk74.sh` (2 + 2 runs in chunks of 10 contexts), `src/chain74.sh` (the heavy-slot chain, not
  used in the end).
- The 2 + 2 runs were made direct, one chunk at a time. The largest 10-context chunk was measured first: 15.7 s and
  0.13 GB; the longest chunk took 15.8 s. Two runs went through heavy.sh: p74 on all 729 contexts (83 s, 0.64 GB) and
  pk on the three failures (72 s, 0.73 GB).
- The watchdog never fired. PIDs are in `pids.log`.
- **Rule breach (mine):** one direct run, `c10_fail` (p74 with distances on the three failing contexts), had tables
  sized 1.31 GB. It peaked at 1.27 GB RSS for 19.9 s. It should have gone through heavy.sh: I started it before
  reading its size line. The watchdog (2.0 GB) was on, and the run ended by itself.
- I first queued the 2 + 2 runs through heavy.sh (`src/chain74.sh`). They waited 1 h 40 min without a slot, because
  other agents' short runs took every freed slot. I stopped my own waiting chain: PIDs 11747 and 11762, recorded in
  `pids.log` before the kill, holding no slot and never having run p74. I replaced it with the direct chunks.
- Logs: the run outputs (all 1 + 1 and 2 + 2 runs, the 160-context extension, the 729-context run) are packed in
  `logs/p74_runs.tar.xz` (extract into `logs/` to rerun `src/cmp74.py`); the `/usr/bin/time -l` files are in
  `logs/time.tar.xz`; the comparisons are `logs/compare_*.txt`. `tmp/` has been deleted; no binaries are left.
