# VERIFY2.md (referee 2 for K29, 2026-10-29)

**Verdict: ACCEPT_WITH_FIXES.** Every number I re-ran agrees with K29, with no solver disagreement anywhere. The result
("a bare group with exact-P punishment T_P >= 2 on both sides can act as 0 beside all 885 contexts of the stated class on
cyl:7x6") stands at CHECKED-2. What must change is wording, in the LOOPY edits and in two sentences of the findings:

1. K29's edits write "frozen groups with T >= 2" and "false in the form ...". K29 only has T_P (exact P-win length); the T of
   Definition 2.6 was not computed for any survivor. So the CONJECTURE of Prop. 2.10(b) is not refuted and not even
   touched in its own terms. EDITS2 rewrites the four edits accordingly.
2. "The same classes survive on flat 7x6" is wrong for the contexts e,f of flat:7x6 (F_Z = a-c): two of the four classes survive,
   the two with T_P (6,7) fail. All four survive on flat:7x6 with F_Z = c-e (contexts a,g).
3. "107 classes re-checked" hides that 90 of them were checked on one file (63 contexts) only.
4. Slips in K29's edit 1 (reversed movers in the T_P sentence, "its mirror", the guess declared refuted) and a missing hypothesis in Lemma N1: problems 1b and 1c.

Replacement edits: `verify/EDITS2.md` (the four OLD blocks of K29/EDITS.md, each occurring exactly once in the current LOOPY.md,
re-checked by script after LOOPY's 05:13 change).

## What I reused and what I wrote

- Reused from the first referee (`VERIFY.md`): `verify/scripts/ref3enum.cpp`, the enumerator written on top of the K23 referee's
  `ref3` (I rebuilt and re-ran it for all ten configurations myself; I read its `main`: pawn sets up to 2+2 on F_Z ranks 2-5, kings on any F_Z
  square, keep only P value (L,W) for both sides). Nothing else from `verify/` was used. Its orbit counts were NOT reused: I wrote my own orbit code.
- Built privately in `verify/r2/bin/` (deleted at the end): `kpsolve.c` (`--frozen`), `kp_p.c` (`--pmodel`), `ref3.cpp`, `ref3m.cpp`, `ref3enum.cpp`.
- Written by me (`verify/r2/scripts/`): `ctx.py`, `ctx3.py` (context generators, own counting), `drive.py`, `drive_ctx.py` (harness: Phi by `kp_p` and
  `ref3`, Psi by `kpsolve --frozen` and `ref3 --frozen` with two parkings), `orbit.py` (symmetry classes), `wsample.py` (witness sample with
  non-representative members), `stalecheck.py`, `depthcmp.py`, **`mini.py` (a third, independent solver of the P model for bare groups: bounded-depth
  search from `SPEC.md`, shares nothing with kpsolve/kp_p/ref3/grp)**, `summ.py`, `mkedits2.py`.
- Honest note on `mini.py`: its first version disagreed with K29's depths on 6 of 130 groups. The bug was mine (a promotion was allowed while the mover's king
  was in check, and a double step could land on the mover's own king); after the fix all 130 agree. K29's depths were right.

## Claim table

| # | Claim (K29) | My result | Label |
|---|---|---|---|
| 1 | cyl:7x6, F_Z a-c, contexts e,f (885, both sides to move): four classes (14 groups) act as 0: `Kb3 Pa2 Pc2 kb1 pa3 pc3`, `Kb1 Pa2 Pb3 ka3 pb2 pc5`, `Kb3 Pa2 Pa4 ka5 pa3 pb4`, `Kb3 Pc2 Pa4 ka5 pc3 pb4` | **CONFIRMED.** I solved ALL 60 candidate groups against all 885 contexts: 46 fail, 14 act as 0, and the 14 are exactly the images of K29's four representatives under my own symmetry code (`verify/r2/logs/c7f3_*.out`). `kp_p` = `ref3` on every Phi (60 x 1,770 positions), `kpsolve --frozen` = `ref3 --frozen` on every Psi, 0 parking mismatches (two parkings, both solvers). Z_T reproduced: 47 differ. | CHECKED-2 |
| 2 | The same classes survive cyl:8x6 (e,g: 885), flat:7x6 (e,f: 885; a,g with F_Z c-e: 885) | **CONFIRMED with a correction.** cyl:8x6 e,g: 4 of 4 reps survive (`kp_p`+`ref3`/`kp`+`ref3`). flat:7x6 e,f: 5 reps survive, but they are `Kb3 Pa2 Pc2 kb1 pa3 pc3`, `Kb1 Pa2 Pb3 ka3 pb2 pc5` and three others; the two T_P (6,7) classes FAIL there (`Kb3 Pa2 Pa4 ka5 pa3 pb4` is not even (L,W): Phi = (D,D); `Kb3 Pc2 Pa4 ka5 pc3 pb4` differs in 17 contexts). flat:7x6 a,g, F_Z c-e: 4 of 4. | CHECKED-2 |
| 3 | 63-context survivors: 28 (cyl:7x6 f4), 17 (cyl:8x6 f4), 45 (flat:7x6 f4), 15 (cyl:8x6 f3 d3) | **Reproduced** with `ref3` for Phi (single solver) and two solvers for Psi: 105 of 105 survive. Weak statement (one context file). | CHECKED-2 for Psi, one solver for Phi (K29 had two) |
| 4 | Screen-only survivors (70) | Not re-run, except flat:8x6 f3 (5 classes) on e,f (885 contexts, `ref3`): all 5 survive, consistent. | COMPUTED-1 |
| 5 | 269 failing classes, 278 witnesses, 96 sampled members confirmed | Whole-class check on cyl:7x6 f3 (46 failing groups). Fresh sample of **47 witnesses over the 13 configurations, 25 of them for non-representative members** (colour swap + rank flip, F_Z reflection, my code), solved with `kp_p`, `ref3`, `kpsolve --frozen`, `ref3 --frozen` and a second parking: **47 of 47 CONFIRMED**, each equal to K29's pair after mapping (`logs/wsample_cmp.txt`). K29's own `ver_*.cmp` files: all 122 lines read 0 disagreements and 0 differences. | CHECKED-2 |
| 6 | `Kb3 Pa2 Pa4 ka5 pa3 pb4` and `Kb3 Pc2 Pa4 ka5 pc3 pb4` (K29 calls the second "its mirror": wrong, they are two classes) fail beside `Pf2 pf3 pf4 pf5` (Phi (L,D), Psi (L,W)) | **CONFIRMED** (`kp_p`, `ref3`, `kpsolve --frozen`, `ref3 --frozen`, second parking). `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5` do NOT fail there (Phi = Psi = (L,W)). | CHECKED-2 |
| 7 | The two other survivors have no failing context among 0-2681 of 3,237 contexts (3+3 pawns, e,f) | Not contradicted. With `ref3` alone, for each of the two groups: 150 of 980 four-pawn, 400 of 1,120 five-pawn, 80 random and 120 "at least two locked pawn pairs" of 560 six-pawn contexts: 0 differences (`logs/t4*.out`, `t5*.out`, `t6*.out`). The counts 1/16/112/448/980/1,120/560 = 3,237 and 2,677 are right. Six-pawn tier still incomplete. | COMPUTED-1 (one solver each time; K29: one code) |
| 8 | Candidate lists: 1,236 groups, 446 classes, ten configurations | **CONFIRMED**: my rebuilt `ref3enum` gives the same sets as K29's `enum_*` in all ten configurations (60, 264, 62, 260, 36, 200, 58, 36, 200, 60). My orbit code gives the class sizes of K29's table for every surviving class (`orbit.py`: no mismatch). | CHECKED-2 |
| 9 | T_P values; "all 1,236 have T_P >= 5; 202 have T_P = 1 on one side; survivors (4,5), (2,8), (6,7), (6,7)" | **CONFIRMED.** `mini.py` gives loss depths 8/10, 4/16, 12/14, 12/14 for the four reps and 10/10 for Z_T. For `Kb3 Pa2 Pc2 kb1 pa3 pc3` every White move has d = 7 and every Black move d = 9, so "Black needs exactly 4 moves after every White move, White exactly 5 after every Black move" is exact. K29's edit says "4 White moves after any White move": the movers are reversed (the winner moves), see problem 1b. 130 groups (cyl:7x6 f3 24, cyl:8x6 f3 24, flat:7x6 f3 18 and 24, cyl:7x6 f4 40; those with depth <= 14) agree with K29's `enum_*` columns; from the ten `enum_*` files I recomputed: 202 groups with a side of loss depth 2 (T_P = 1), minimum over groups of the larger loss depth 10 (T_P 5), maximum 38. | CHECKED-2 |
| 10 | Mechanism counts 124 / 47 / 45 / 8 / 34 / 13 (271 lines); 267 of 269 first failures have a pawn on the file next to the buffer | Counts re-added from `data/M_*.txt` (they match). Distance claim recomputed from `table_all.tsv`: 267 at distance 2, 2 at distance 3 (main); d3 runs 8 at 3 and 1 at 4. All 47 STALE lines: my own move generator finds no legal move and no check in each. | COMPUTED-1 / CHECKED-2 for the stalemates |
| 11 | Addendum 9 (agent B): Lemma "T_P(m) >= 3 excludes LC_1(m)"; Lemma N1 (stalemate) | Both read and accepted. The first is one line from Theorem 2.7(a) with T = 1 (the bare group has mu_s = infinity, so (L2) is vacuous): a certificate would give a P-win with the promotion on the first move after r, so L(m) <= 2. It shows only that the survivors are not T = 1 groups of Prop. 2.10(a); it does not give T >= 2 in the sense of Definition 2.6. N1: valid at the root, once "s is not in check in the bare group" is added (problem 1c) (context pawns neither stand on nor attack F_Z squares); example `Ka1 Pb2 Pa3 kb3 pa2 pa4` beside `pf3` checked (Kg1 is covered by Z's own pawn a2, Kg2 by pf3). | PROVED (hand proofs, relying on Theorem 2.7(a) and Lemma 2.2) |

## Problems

1. **T versus T_P (fix in EDITS2).** `EDITS.md` edits 2, 3 and 4 say "frozen groups with T >= 2 ... it is false in the form ...". K29 shows bare groups with
   P value (L,W) and T_P >= 2; "frozen group with T" in LOOPY is a group with a certificate LC_T for every sortie, and no certificate was computed.
   `agentB` says so itself (the K24 local-game script `lg.py` cannot run on groups with a blocked pawn on its start rank). The Prop. 2.10(b) CONJECTURE is therefore not refuted.
1b. **Three slips in K29's edit 1 (all fixed in EDITS2).** (i) The movers are reversed: "the exact P-win takes 4 White moves after any White move" should read: after any White move Black needs
   4 moves (T_P counts the winner's moves). I first copied this slip into EDITS2 and corrected it only after reading the parallel referee's summary at the end (see below). (ii) `Kb3 Pc2 Pa4 ka5 pc3 pb4` is not the mirror of
   `Kb3 Pa2 Pa4 ka5 pa3 pb4`: the mirror (reflection of F_Z) of the first is `Kb3 Pc2 Pc4 kc5 pc3 pb4`, a member of its own class; they are two classes. (iii) The edit says the guess "a sortie king cannot reach the buffer
   in time" is refuted and deletes it from the open list. K29 shows only that reaching in time is not necessary (the survivors' sortie kings do reach the buffer) and that one slack number does not separate survivors from failures; the converse
   direction (groups whose sortie kings cannot reach the buffer in time) was not isolated. EDITS2 keeps that as open.
1c. **Lemma N1 (addendum) needs a hypothesis.** Its proof says "s is not in check (context pawns do not attack F_Z)", which excludes checks by context pawns only. A check by a Z-pawn of the other side in the bare group would turn the
   stalemate into a mate (a loss, Phi = Psi). Add "s is not in check in the bare group". All 47 STALE witnesses satisfy it (my move generator: no legal move, no check, 47 of 47).
2. **Flat 7x6.** See claim 2. `EDITS.md` edit 1 and the sentence "Kb3 Pa2 Pc2 kb1 pa3 pc3 survives in all 13 configurations" are right, but "the same classes survive on ... flat 7x6" is not.
3. **Weight of the 107.** 17 of the 107 two-solver classes are on 885-context sets; 90 on 63 contexts of one file. Stated in EDITS2.
4. **Headline sentence (1) of the findings** says survivors act as 0 "beside EVERY context of the class" (<= 2 pawns a side, files at distance >= 2). That is the whole class only on cyl:7x6;
   on cyl:8x6 it is the files e,g, on flat:7x6 the files e,f (or a,g), elsewhere a screen. The same sentence's second half says so; EDITS2 keeps the file sets explicit.
5. **Report consistency.** `findings.txt` (= `FINDINGS.md`, which now exists although the text says the harness refused it) has an Addendum 9 from "agent B" that is not in `summary.json["report"]`
   (123 lines against 117) and not in the claims list. It contains two PROVED lemmas (claim 11) and a second set of mechanism counts (281 lines over 13 configurations: 98 / 51 / 47 / 46 / 39) next to
   the first (271 lines over 10: 124 / 47 / 45 / 8 / 34 / 13). Both sets are internally consistent (I re-added the first); the two classifications differ by definition.
6. **Evidence for the two remaining survivors is thin and one-code.** Even with my additions (ref3, 550 + 200 contexts of 3+3 per group) it is COMPUTED-1, and the 6-pawn tier is mostly unsolved. Do not read it as support for a universal zero.
7. **Rules.** K29 reports breaking the 20-minute rule (investigator's own section 8). Mine: every solver run went through `heavy.sh`; two of my Python runs (`mini.py`, depth comparisons, 1-2 CPU-minutes in total) ran niced outside `heavy.sh`, one of them
   (a first version of `depthcmp.py`, about 2 CPU-minutes) was killed by me by its PID (71367, 71363, recorded). I tried to kill queued `heavy.sh` waiters of my own by a list of PIDs derived from `ps`; the permission layer
   refused, so I did not, and dropped the queued jobs with cancel flags read by my harness (`data/cancel_*`). No pkill, no git, no installs, no network. Other agents' jobs shared the two slots; waits were up to 30 minutes.

## Parallel referee

Another referee instance worked in the same directory at the same time (`verify/me/`, `verify/EDITS.md`, `verify/summary_refB.json`; shared `heavy.sh` slots). I did not read any of it while checking (claims 1-11 are mine alone);
at the end I read only `verify/summary_refB.json`. It agrees on the verdict (ACCEPT_WITH_FIXES), on claims 1, 2, 8, 9 and on the T versus T_P problem, and it found two errors that I had copied from `EDITS.md`: the reversed movers and the false "its mirror"
(problem 1b), plus the missing "not in check" hypothesis of Lemma N1 (problem 1c) and the over-strong treatment of the LOOPY guess. Its larger witness check (all 278 witnesses, 227 symmetric images) is stronger than my 47 and I did not repeat it.

## EDIT check

- `EDITS.md`: all four OLD blocks occur exactly once in the current `LOOPY.md` (modified 05:13): CHECKED by script (`mkedits2.py`). Their NEW text carries problems 1-3.
- `verify/EDITS2.md`: same four OLD blocks, new NEW text; every OLD re-checked to occur once at write time. Numbers in the NEW text are those of this file.
- `LOOPY.md` was not touched.

## Not checked

- The 70 screen-only survivors (except flat:8x6 f3), the 6-pawn tier, groups outside the enumeration (3+ Z-pawns of one colour, pawns off F_Z, e.p. layers, F_Z of other widths), the T of Definition 2.6,
  boards other than the four named, and whether parking neutrality holds for every context (checked only on the contexts I solved, 0 mismatches, two parkings).
- That K29's class representatives of the one-file rows (28 / 17 / 45 / 15) survive with `kp_p` too (I used `ref3` for Phi there).

## Reproduce (all under `kings/delegate/out/K29/verify/r2/`, binaries deleted afterwards)

```
python3 scripts/ctx.py "" ef 2 2 2 5 | wc -l                      # 1770 positions = 885 contexts
scripts/runshard.sh TAG cyl:7x6 ef 2 2 2 5 "Ka1 ka6" "Kb1 kc6" data/g_c7f3_0.txt   # via heavy.sh; groups from ../data/r3e_cyl7x6_f3.txt (shards 0-3)
python3 scripts/summ.py logs/c7f3_*.out                           # 60 groups, 14 survivors, 0 disagreements
python3 scripts/wsample.py gen 11 4 ; scripts/wrun.sh cyl7x6 ... ; python3 scripts/wsample.py cmp   # 47 witnesses
python3 scripts/mini.py cyl:7x6 "Kb3 Pa2 Pc2 kb1 pa3 pc3"         # loss depths 8 and 10 plies
python3 scripts/depthcmp.py cyl:7x6 ../../data/enum_cyl7x6_f3.txt ; python3 scripts/stalecheck.py
python3 scripts/ctx3.py ef 2 5 3 3 6 80 17 > data/ctx_c7_t6s80.txt ; scripts/run3.sh t6a ctx_c7_t6s80.txt g_a.txt 20
python3 scripts/mkedits2.py                                        # writes ../EDITS2.md and checks each OLD occurs once
```

Files kept: `verify/r2/scripts/`, `verify/r2/logs/` (all run logs, `RESULTS_survivors.txt`, `wsample_cmp.txt`, `pids.log`), small tables in `verify/r2/data/`, `verify/EDITS2.md`.
