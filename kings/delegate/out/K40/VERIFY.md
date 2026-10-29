# K40 referee report (Gafni's K+P vs K values without edges)

Referee, 2026-10-29. My files are in `kings/delegate/out/K40/verify/`:
- `src/vsum.c`: my own solver for x ⊞ T. I wrote it from `kings/SPEC.md` and LOOPY Definitions 1.2, 1.3 and 1.5, and I did not read K40's `kpsum.c` or `ksum2.py`.
  - The test graph is the integers −12…12, on, off, dud, over, under, \*, ↑, ↓, ±1 and on + \*.
  - A T-move is illegal in check. `N` and `C` select the no-move convention. `--kxploss` scores Kxp as a Black win.
  - `--atlas` is my own reimplementation of the atlas promotion rule. `--kvk` brute-forces Lemma 1.
- `src/*.py`: comparison and analysis scripts.
- `logs/`: all outputs.
- `data/analysis.json`: per-board counts.
- `EDITS.md`: the replacement edit.

Binaries were built in `verify/bin/` and deleted at the end. Nothing went through heavy.sh, because no run took more than 2 CPU-seconds: the largest was cyl:8×8 with all 35 tests, 1.6 s. I started no background process and killed nothing.

## Claim table

| # | Claim (K40) | My re-run | Verdict | Label |
|---|---|---|---|---|
| 1 | Bare P table (T = 0) on cyl:3–8×6 and cyl:3–8×8: kpsum, kp_p `--pmodel` and ref3m agree, 1,056,504 positions, 0 differences | I built kp_p and ref3m myself and ran them on every legal position. Compared with vsum (C) at T = 0: 1,056,504 positions, 0 differences across the three (`logs/` via `src/cmp_base.py`) | CONFIRMED | CHECKED-2 |
| 2 | ref3m needs `cyl:7x6`; `cyl7x6` returns X | `cyl7x6`: X. `cyl:7x6`: D. ref3m reads W and H from character 4 on. The task's spelling hint is wrong for ref3m | CONFIRMED | KNOWN (code) |
| 3 | Sums: kpsum and ksum2 agree on 38,971,824 results (both K40's) | I did not re-run ksum2. Instead I compared K40's own tables `data/sums_cyl_*.tsv.xz` and `sums_normal_cyl_*.tsv.xz`, position by position, with vsum: 2,113,008 rows × 34 tests = 71,842,272 results, 0 differences, integers ±12 on every board | CONFIRMED (the count 38,971,824 is NOT_CHECKED, and superseded) | CHECKED-2 (was "two implementations, one author") |
| 4 | Per-board table, §2 of findings.txt (normal DEC/ON/DUD/other, P DEC/ON/tempo/DUD, P-W, atlas-W, atlas≠P), all 24 rows | Every number reproduced (`logs/analysis.log`) | CONFIRMED | CHECKED-2 |
| 5 | (N), 3 and 5–8 files: only DEC / ON / DUD. DEC = W(x ⊞ dud). The class is fixed by r(x ⊞ 0) and r(x ⊞ dud) | 0 "other" on every board with W ∈ {3,5,6,7,8} and H ∈ {6,7,8}. DEC = W(dud) = W(off). The two-bit rule holds everywhere | CONFIRMED (also for H = 7, which K40 did not run) | CHECKED-2 for H = 6, 8; COMPUTED-1 for H = 7 |
| 6 | Placement pairs: only DEC/DEC, DEC/ON, DEC/DUD, ON/ON, ON/DUD, DUD/DUD | Confirmed on all 15 boards (`logs/pairs.log`) | CONFIRMED | COMPUTED-1 (my own pairing; it rests on CHECKED-2 tables) |
| 7 | DUD = "Black forces Kxp against a White who may pass" on 3, 6 and 8 files (H = 6, 7, 8) and on 7×6 | vsum N `--kxploss`, T = on: DUD = L and DEC ∪ ON = W, no draw left, on those boards | CONFIRMED | COMPUTED-1 (only K40's kpsum and my run; this is an independent re-run, so CHECKED-2 in effect) |
| 8 | Fortress exceptions 5×6 30, 5×7 100, 5×8 170, 7×7 182, 7×8 378, with both kings at cyclic distance (W−1)/2 from the pawn | Counts reproduced exactly. In every fortress position both kings are at distance (W−1)/2 from the pawn's file. They share a file in 10/50/90/98/182 of them and do not in the rest | CONFIRMED. The EDITS.md wording "both kings on **the** file antipodal to the pawn" is inaccurate: odd W has two such files, and the kings are often on different ones | COMPUTED (two runs) |
| 9 | 4-file cylinders: thresholds n ∈ {−4..1} under (N); 28 Black wins per board; "other" 76+132 (4×6), 212+268 (4×8) | Under (N), thresholds are −2…1 on 4×6, −3…1 on 4×7 and −4…1 on 4×8. There are 8 + 20 = 28 Black wins on 4×6, 4×7 and 4×8. The "other" counts are reproduced | CONFIRMED | CHECKED-2 |
| 10 | (C), 3 and 5–8 files: DEC and DUD are the same sets as under (N); all of ON becomes D on 3 files | Confirmed on all boards with H ∈ {6,7,8} | CONFIRMED | CHECKED-2 (H = 6, 8) |
| 11 | (C): ON splits into P-ON, monotone thresholds θ ∈ {−1,0,1} ("−1 only for H = 8") and parity classes | Confirmed for H = 6 and 8. On H = 7, which K40 did not run, θ = −1 also occurs. So the true statement is "−1 only for H ∈ {7, 8}". On 8×8 there are 5 non-monotone integer patterns, all of them parity patterns (`logs/check2.log`) | CONFIRMED (scope note for H = 7) | CHECKED-2 |
| 12 | Examples on 8×8: `Ka1 Pa2 ka3 w` θ = 1; `Ka2 Pf2 kb4 w` W iff n ≥ −1 or n odd; `Ka3 Pg4 kb5 w` W iff n ≥ −2 or n even; `Ka6 Pa7 ka8 b` W iff n < 0 and n odd | All four reproduced over n = −12…12 | CONFIRMED | CHECKED-2 |
| 13 | 8×8 ON with White to move: 19,504 P wins and 15,528 P draws; 33,176 of 35,032 tempo-sensitive | Reproduced | CONFIRMED | CHECKED-2 |
| 14 | The Prop. 5 pattern is held exactly by the W translates of x_f, on every board run with W ≥ 4 | Exactly W positions on each board with W = 4…8 and H = 6, 7, 8, all of the shape K(f,H−2) P(f,H−1) k(f,H), Black to move | CONFIRMED | COMPUTED by K40 and by me |
| 15 | Under (C), Prop. 4(b) fails on 4×6 at 52 Black-to-move and 40 White-to-move positions; it never fails on 3 and 5–8 files | 2268 − 2216 = 52 and 3496 − 3456 = 40, where W(dud) is the same under both conventions. It does not fail elsewhere | CONFIRMED | CHECKED-2 |
| 16 | Atlas vs P: every difference is P = W, atlas = D; 8×8 3,440 + 4,824; 6×6 504 + 810; 7×6 910 + 1,652; 8×6 1,440 + 2,512 | Checked three ways: the real `atlas/cylinder/kpk.c`, compiled by me (8 ranks); my own copy with R = 6; and my own reimplementation of the atlas rule in vsum. All three agree at every position. The difference sets equal K40's `atlas_disagreements.tsv.xz` (27,490 rows, `comm` gives 0 differences) | CONFIRMED | CHECKED-2 |
| 17 | Cause: Kxq now, or later; stalemate after promotion only on 4 files (8 per board); 8×8 w 784 + 2656, b 4816 + 8 (DEC + ON); 7×6 ON 126 | Reproduced by my own classifier (`logs/atlas_cause.log`) | CONFIRMED | COMPUTED (two runs) |
| 18 | With P's promotion rule put into the atlas code, it reproduces P with 0 differences | My own copy, with `promo_value` returning 1: 0 differences on all 12 boards | CONFIRMED | CHECKED-2 |
| 19 | The disagreements are (A_Q) failures | Chess check: `kpsolve --cap 1` (bounds exact everywhere) on all positions of the 12 boards. Atlas = chess everywhere **except 24 positions per board on cyl:4×6 and cyl:4×8**: there P = W, atlas = D and chess = W, because a rook promotion wins (`--promote R` gives W W, `--promote Q` gives D D). On 3 and 5–8 files every disagreement is an exact chess draw, so it is an (A_Q) failure (`logs/chess_vs_P_atlas.log`, `logs/kpsolve_chess_disagreements.log`) | CONFIRMED on 3 and 5–8 files. REFUTED as stated on 4 files, where 24 per board are atlas errors (underpromotion), not (A_Q) failures | COMPUTED-1 (kpsolve) |
| 20 | EDITS.md: the atlas "differs from P at 1.4–3.0% of positions" | The actual range over the 12 boards is 0.75% (3×8) to 3.44% (7×6). The four boards named in the same sentence give 2.53%, 2.96%, 3.44% and 3.43% | REFUTED (number) | — |
| 21 | Lemma 1 (K v K is dead) | Every step re-checked. The file-intersection argument is right for W = 3, W = 4 (V is free) and W ≥ 5. Brute force (`vsum --kvk`): no stuck king on cyl:3–8×4–8 | CONFIRMED | PROVED (refereed once) |
| 22 | Lemma 2 (White is never stalemated when W ≠ 4) | Every step re-checked. For W ≥ 5, bk covers at most one of A and B. If the pawn is on the other, it can be blocked only by bk on (f±1, r+1), which is adjacent to wk. W = 3 is right. Data: 0 Black wins under (N) on W ≠ 4; 28 on W = 4 | CONFIRMED | PROVED (refereed once) |
| 23 | Corollary 3 (Black never wins) | Follows from Lemmas 1 and 2. Data: 0 Black wins under (C) on every board, 4-file boards included | CONFIRMED | PROVED (refereed once) |
| 24 | Prop. 4 ((a) dud does not see stalemate; (b) DEC = P_L, Theorem 3.11 with the check rule) | (a) is right: the only moveless node of x ⊞ dud is mate. (b): the three remarks on steps (1)–(3) are right. A Black T-move needs "not in check", and then the virtual pass in off is also legal. White is never in check. A White-to-move node has Black out of check, so Right's pass back exists | CONFIRMED | PROVED (refereed once) |
| 25 | Prop. 5 (parity family `Ka6 Pa7 ka8 b`, W iff n < 0 and n odd, under (C)) | Every step re-checked. bk has no move with wk on c. With wk on r±, bk's only move is to (a∓, H−1), and the pawn then promotes. White's other king moves (rank H−3; from r± also (a±2, H−2) and (a±2, H−1)) unguard the pawn and allow Kxp. The pawn is blocked. The c–r± path is bipartite, so White cannot lose a tempo. The parity count is right | CONFIRMED | PROVED (refereed once) |
| 26 | Consequence: a parity class equals no loopy normal-play game, because r(G + n) is monotone in n "by Lemma 1.6" | The statement is right. Lemma 1.6 compares two option sets on the same position set, so it does not apply literally to G + n against G + (n+1). The same strategy simulation does apply: White ignores her extra token, or Black's options form a subset. This is KNOWN | CONFIRMED (the citation is loose) | KNOWN |
| 27 | Housekeeping: binaries deleted, no `__pycache__`, under 50 MB; PIDs killed were 65955 and 65981 | There are no binaries, no `__pycache__`, and K40/ totals 2.4 MB with my files. `pids.log` lists 65955 and **29511**, not 65981. None of the three is running | CONFIRMED, except a pids.log inconsistency | — |
| 28 | EDITS.md OLD occurs once and applies | `apply_edits.py` on a scratch copy reports 1 applied, 0 rejected | CONFIRMED | — |

## Problems found

1. **The EDITS.md percentage is wrong.** "1.4–3.0% of positions" should be 0.75–3.4% over the 12 boards, or 2.5–3.4% on the four boards named in that sentence.
2. **The EDITS.md fortress wording is inaccurate.** It says "both kings on the file antipodal to the pawn". For odd W there are two files at cyclic distance (W−1)/2. Each king is on one of them, often not the same one. findings.txt has it right.
3. **"These are (A_Q) failures" holds only on 3 and 5–8 files.** On cyl:4×6 and cyl:4×8, 24 disagreements per board are chess wins by a rook promotion, which the queen-only atlas misses. The atlas header claims underpromotion matters "in a handful of flat-board KPK stalemate positions only", and this is a counterexample to that claim on the 4-file cylinder. This does not touch the boards named in the brief.
4. **The labels can be raised.** The sum results are now CHECKED-2 (K40's kpsum against my vsum, position by position). The hand proofs are refereed once, by a referee of the same model family.
5. **Scope.** "θ = −1 only for H = 8" is true on K40's boards, but θ = −1 also occurs on H = 7. My runs extend the whole classification to H = 7 and to integers ±12 on every board, with the same structure.
6. **Context.** The edit does not mention K4, K6 and K8 (`kings/REPORT.md`), which studied the same object on boards up to 5×5 and 4–6 ranks. K40 agrees with them: no number or infinitesimal; insensitive under normal play on 3 and 5–8 files; sensitive under the chess stalemate rule on 5+ files.
7. **Minor.** Lemma 1.6 is cited for the monotonicity of r(G + n). `pids.log` lists 29511 where the report says 65981.

## Replacement edit

`verify/EDITS.md` replaces the whole of K40's EDIT 8.5, using the same OLD, which occurs once in the current LOOPY.md (`apply_edits.py`: 1 applied, 0 rejected). It fixes problems 1–6.

## Verdict

ACCEPT_WITH_FIXES. Every computed number I re-ran is right, and every hand proof is sound. The edit has one wrong number, one inaccurate geometric description and one over-broad (A_Q) sentence. Use `verify/EDITS.md` instead of `EDITS.md`.
