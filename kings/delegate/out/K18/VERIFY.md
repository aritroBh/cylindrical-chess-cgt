# VERIFY: K18 (tempo matching, LOOPY section 8, open question 1)

Referee: independent re-check, 2026-10-27. Own code and logs in `K18/verify/mine/` (local-game solver `mylg.cpp`, search
outputs, comparison scripts) and `K18/verify/r3/` (context experiments, ref3 runs). Both are inside the allowed directory.
Nothing else was written. LOOPY.md and all existing files were left alone, no git, no pattern kills (the one background job I
started, a chess re-run waiting for a heavy slot, was killed by its recorded PID, `verify/r3/pid_chess.txt`).

## Verdict: ACCEPT_WITH_FIXES

The computations are right. Every search number I could rebuild was rebuilt exactly, with a solver written by me. What is wrong
is a handful of statements around them: one invalid class count (flat 6x6), a total that is 30 off, a proof with a gap
(Proposition 8.1, e.p. lapse), a mechanism sentence that the data do not need, and one "usually". The two EDITS apply
cleanly (OLD occurs once in the current LOOPY.md, re-checked after LOOPY.md changed at 20:02), but EDIT 1 must be corrected
before it is applied (list at the end).

## What I reused from the earlier, stopped referee

Nothing. I listed `K18/verify/` (it holds its `kp`, `kpp`, `vlg.py`, `bare11*`, `p3_*` files and logs, some empty or half
written) and did not read or run any of it. All numbers below come from my own code and my own builds (`kpsolve.c`, `kp_p.c`
only as a cross-check of the headline counterexample).

## My independent code

* `verify/mine/mylg.cpp`. A local-game solver for Definition 2.6 written by me from the Definition and the K18 text. I read
  K18's `lg.cpp` only for the passer rule (`cylcgt.pawns.passed`) and the `--search` output format, which are needed to compare.
  Design: layers by pawn configuration, inside a layer rounds of "least T"; budgets 0..6 and infinity; queen clause as a switch;
  e.p. rights exact; cylinder or flat.
  Two bugs of mine were found and fixed by comparing with the section 5.1 lists (queen safety inverted; a value assigned in the
  wrong round). After the fixes the solver reproduces section 5.1: after Kxa4, T = 6, 6, 6, 7, 7 (queen clause) and 6, 6, 5, 6, 6
  (L1_P) for Kg4, Kg5, Kg6, Kh6, Ka6, and the finite-budget vectors, identical to K18's `lg` (cyl:8x8, F_Z = {h, a, b},
  rotated by one file).
* `verify/r3/ref3` is K23's independent P-model solver (given in the task), built privately; `kpp` is K7's `kp_p.c`.

## Claim by claim

| claim | verdict | what I did |
|---|---|---|
| Counterexample Y = `Ka1 Pa2 kc1 pa3`, m = Ka1-h1, G = `Pe2 Pg2 pf4`: `Kh1 ... b` is a White win in P, `Ka1 ... w` is a White win in P, G alone is zero | CONFIRMED, CHECKED-2 (K18 labels it COMPUTED-1; two solvers agree, so the label can go up) | ref3 and ref3m (`--moves`): `Kh1 Pa2 kc1 pa3 Pe2 Pg2 pf4 b -` = W, all six Black moves W; `Ka1 ... w` = W; bare `Ka1 Pa2 kc1 pa3 w` = L; `--frozen` `Ka1 kc6 Pe2 Pg2 pf4`: w = L, b = W (zero). My own build of K7's kpp reproduces `logs/cx_small.txt` line for line, including the negative context `Pe2 pg3` and the control `Pe2 Pg2 pe4 pg4` (L L, punished). |
| Group search: roots 88,758 (3 files, <= 2+2, cyl:8x6), candidate counts, classes | CONFIRMED, CHECKED-2 | `mylg --search`, both queen settings, compared with K18's whole 32,539-line output (`keep/search_c8x6_f3_22.out.gz`) after stripping reply names: 0 lines only in theirs, 0 only in mine (every root, every sortie class, every T, every esc/only count). Also matched summary.json for cyl:7x6 3 files (88,758 roots; 15,370/17,055; 2,505/1,870), cyl:8x6 and cyl:7x6 with <= 3+2 (194,791 roots; 21,547/23,696 and 21,445/23,588; no-escape 2,138/2,773 and 2,138/2,771), and 4 files <= 2+2 (419,414 roots; 98,242/90,506 and 97,820/90,052; no-escape 13,204/13,728 and 13,196/13,720). |
| Mirror-class numbers 941 (1257), 6602 (6864), 6598 (6860), 1075 (1391) and 1075 (1390), 7708/8549 | CONFIRMED for the cylinders | `dedupe.py`. On a cylinder, a-c file reflection is a symmetry: all 15,422 candidate roots have their mirror partner with the same flag. |
| flat:6x6, 3 files: 960 (1056) | REFUTED as a class count | The counts of roots match (11,801 and 11,850 candidates; 1,695 and 1,829 without escape), but a-c reflection is not a symmetry of the flat board (F_Z = a,b,c has the board edge on one side and the buffer on the other). Of the 11,801 candidate roots 2,647 have no candidate partner and 210 have a partner with another flag; K18's merge is also order dependent (my merge gives 1,012 and 1,124). Correct statement: 1,695 (1,829) roots with a plain-only sortie and no escape, not merged. |
| Plain local game is a lower bound of bare P: 108,710 of 108,710 (queen clause 100,625 of 100,625); pass game 95,658 of 95,666, the 8 exceptions being draws | CONFIRMED | My dump of every White move at every root of the same search gives exactly 232,343 distinct positions (K18's number). ref3 on all of them: plain-won (P) 108,710, all L; queen clause 100,625, all L; pass-won 95,666 = 95,658 L + 8 D (queen clause 88,866 + 8). The 8 positions are in `verify/mine/exc8.txt`; every Black move there is D in P (that the cause is a stalemate of White was not traced). |
| 941 groups: 4,593 punished moves = 1,864 plain-only + 2,726 both + 3 pass-only (two L, one D) in bare P | CONFIRMED | ref3 on the positions after each move (representative root per class): exactly (PLAIN-ONLY, L) 1,864; (both, L) 2,726; (pass-only, D) 1; (pass-only, L) 2. |
| 1,372 plain-only king sorties (and 492 pawn sorties); classes 953 / 327 / 77 / 15; 61 prefix, 12 (k = 0 and odd k), 4 other | CONFIRMED, upgraded to CHECKED-2 | `mylg --kmax 6 --search`, then `kclass.py`: 1,372 and 492; {finite for every k <= 6: 953, k*=0: 327, other: 77, even k only: 15}; of the 77, 61 prefix (40 + 3 + 12 + 6), 12 of the form k = 0 and odd, 4 other (`1011111`). The k-vectors of all 941 classes equal K18's (0 differing classes). K18 had only lg.cpp for k = 1..6 (its cross-check had finished 1 of 60); now there are two implementations. |
| "usually with T_k = T_0 + k" | NOT SUPPORTED as worded | Of the 953, only 487 have all increments 1; 85 have (2,0,2,0,2,0), 78 have (2,1,1,1,1,1), 40 (4,1,1,1,1,1), 36 (1,0,1,1,2,1). Say "in about half". |
| 19 groups with one pawn a side, 25 plain-only king sorties | CONFIRMED | `es_rep.py`: 19 classes, 25 sorties (cyl:8x6 and cyl:7x6). |
| Section 5.5 mirror: Kd3, Kd2 plain-only with T = 6, Kd4 both with T = 5, Kc2 neither | CONFIRMED | root `Kc3 Pb4 ka3 pb5` in my search: Kc3-c2 ESC, Kc3-d2 and Kc3-d3 PLAIN-ONLY T = 6, Kc3-d4 both T = 5. |
| 4160 contexts (e, f, g, <= 2+2, a pawn move for each side); promotion-free: 5 zero and 45 fuzzy, no negative or positive | CONFIRMED | `ctx_enum.py` (own enumerator, own reachability search with e.p.): 4160; frozen classes (ref3 `--frozen`, kings a1/c6) fuzzy 1633, negative 1234, zero 59, positive 1234; promotion-free zero 5, fuzzy 45. cyl:7x6 e,f: 716 contexts, as in the text. |
| ES: 125 contexts, 1,017 legal zero or negative cases, 29 not punished | CONFIRMED exactly | `es_run.py` (own sorties from my search, own contexts, ref3, Black to move after m): the class by result table equals K18's `analysis_ES.txt` cell by cell (zero D7 L235 W7 X1; neg D2 L753 W13 X32; pos L36 W759 X5; fuzzy D3 L1192 W64 X16). |
| ES7 (cyl:7x6): 59 contexts, 601 legal, 7 not punished | CONFIRMED exactly | `es7_rep.py`; table equals `analysis_ES7.txt`. |
| E3 (6 of 12 sorties, 159 contexts, 687 legal, 6 not punished) | PARTLY CHECKED | The six listed failures (sortie 0 with `Pe2 Pg2 pf4`; sortie 2 with `Pg2 pe3` and `Pe2 Pg2 pf4`; sortie 11 with `Pf2 pg4`, `Pe2 Pg2 pf4`, `Pe4 Pf2 pe5 pg4`) are each a White win in P in ref3 (`e3_fail_out.txt`). The other 681 were not re-run: ref3 needs more than 60 CPU seconds per sortie with 4 + 3 pawns, and the heavy slots stayed taken. |
| EP: 5 promotion-free zero contexts, 123 legal, all punished | CONFIRMED | `ep_rep.py`: 125 pairs, 123 L, 2 illegal. |
| E1 reservoir contexts: Delta <= 0 139 of 139, Delta > 0 60 of 60, 7 + 24 | NOT CHECKED (arithmetic only) | ref3 did not finish one sortie against the 8 contexts in 60 CPU seconds (the first position agreed, L). The totals are internally consistent: 26 + 57 + 56 = 139, 46 + 14 = 60, 2+2+2+1 = 7 and 11 + 13 = 24, 248 = 31 x 8 with 18 illegal. Note `keep/table_E1.json.gz` is an older table of 29 sorties (129, 42 + 12): not the data behind the quoted 31-sortie numbers. |
| "42 of the 2275 legal zero or negative contexts of these three runs" and summary.json "punished": 2233 | REFUTED (arithmetic) | ES 1,017 + ES7 601 + E3 687 = 2,305 legal; with 42 not punished that is 2,263 punished. K18's 2,275 and 2,233 are each 30 short. The two runs I rebuilt (1,017 and 601) are exact, and the E3 sum (350 + 337) is printed in `analysis_E3.txt`. |
| In all 42 failures the sortie king stands within 2 steps of a context pawn after m, T >= 4; none promotion-free | CONFIRMED for the 29 ES failures | `p3_rep.py`-style check: maximum distance 2, none promotion-free. The E3 six were checked by hand for distance (all <= 2); the ES7 seven were not checked, so "all 42" is confirmed for 35 of them. |
| "mechanism: the king captures the pawn that makes G a second-player win" | UNSUPPORTED, and a simpler cause exists | In all 29 ES failures a White context pawn is free and promotes in 3 moves (double step) while T = 4 to 7, so mu_s <= 3 <= T: (L2) of Definition 2.6 fails, and Theorem 2.7 does not apply. The failures say that a frozen "zero" containing a promoting race is not a tempo game; they do not touch Theorem 2.7. LOOPY already says the zero next to fast pawns has to be checked case by case (section 5.1). The EDIT should say this instead of the king-captures-pawn sentence, or keep that sentence as CONJECTURE and add the mu_s fact. |
| Chess: 29 non-punished ES sorties, B is D or W in 20; 3 exact Black wins; 6 undecided; 12 controls 11 exact, 1 undecided (kpsolve cap 1) | NOT CHECKED (log recount only) | I recounted `logs/C2_out.txt`: 20 / 3 / 6 and 11 / 1, as stated. I tried to re-run the two headline positions through `heavy.sh` but both slots were held by other jobs for the whole session, so the job was killed unstarted. |
| Proposition 8.1 "PROVED" | NOT ACCEPTED as PROVED (gap), see below | |
| "(P3) fails in all 1,827 matched pairs and all 256 reservoir pairs; the king can reach the context files" | CONFIRMED for ES, with a stronger test; label mismatch | 1,827 = 1,017 + 123 + 687, consistent. K18's R is the union over all fastest strategies, so "fails" there does not say "fails for every strategy sigma". I tested that directly (`mylg --fquery`, `p3_gen.py`): the local game in which White's king may never step on a square of X or its king-neighbourhood (X as in (P2), all pawn-move sequences without promotion). For all 1,050 ES zero or negative pairs (legal or not) s-bar cannot win at all, for any T, while the same 24 Y.m positions are won with T = 4 to 7 without the restriction. So (P3) fails for every sigma in ES. The script `p4_check.py` calls this hypothesis (P4); the EDIT calls it (P3). 256 for E1 is 32 x 8, but only 31 sorties were finished for the results. |
| Budget k = 1..6 values "from lg.cpp alone (COMPUTED-1)" | OUTDATED | now CHECKED-2 (see above). |
| 140 random positions lg vs lg2, 0 mismatches | NOT RE-RUN | I did not run `lg2.py`; my solver agrees with `lg` on all 32,539 search lines instead, which is stronger for the claims that depend on it. |

## Proposition 8.1: gap in the proof

The proof says that s is never stalemated in the real play "because it has a local move whenever it has one in the plain
game". That is true at the positions of the plain game, but a context pair is a pass for s and it clears a pending e.p. right
on F_Z. The plain game never visits the position without the right. The claim "a pending e.p. right that s lets lapse only
removes an option of s" is true for the rest of the game but not for stalemate: if the only legal local move of s is the e.p.
capture, then s declines it by a context move, s-bar answers in the context, and s has no local move in the position without
the right. If the context is then exhausted, s is stalemated (a draw in P). The plain game, where s may not pass, counts
the position with the right as won for s-bar.

Such nodes exist: with <= 3 + 3 pawns on 3 files, cyl:8x6, there are 36 s-to-move states (P variant) whose only legal moves
are e.p. captures, e.g. `Kb1 Pc3 kc4 pb2 pa3 pb3 w b4` (the White king has no move, the pawn c3 is blocked, only c3xb4;
plain T = 2; with the option "s lapses the right", no win). With <= 2 + 2 pawns there are none.
I did not find a counterexample to the Proposition: I added the lapse option to my solver (`LAPSE=1`) and compared, over
every ep-free state with <= 3 + 3 pawns (5,293,277 won states), the plain game with and without the option: the sets and every
T are identical. So the statement may well be true in this range, but the proof as written has a gap. Fix: add the lapse option
to the plain game (a move of s to the same position without the right, s to move again), or assume that no node of the winning
lines is a position whose only legal moves for s are e.p. captures. Until then the label should be "proof sketch, one
derivation, gap identified by the referee", not PROVED. The rest of the proof I checked step by step against Definition 2.6
and Theorem 2.7 and found no other gap; the text itself says (P3) never holds in the tests, so the Proposition is not
exercised by any data.

## The verdict of EDIT 1, read against the evidence

* (a) "false as stated": true for the reading "every context that is a second-player win in the frozen convention". It is not
  surprising and not about tempo: see mu_s above. The EDIT should say which contexts the counterexamples have (a free
  promoting pawn, (L2) fails), since otherwise the wording of open question 1 looks refuted by something that Theorem 2.7 never
  claimed.
* (b) "292 of 292, CONJECTURE": EP's 123 reproduced; the other 169 (30 E3 + 139 reservoir) not re-run, the reservoir ones not
  checked.
* Search boundary stated in the EDIT: confirmed, except that flat 6x6 was not mirror-reduced correctly.

## Hidden cut-offs

None found. My solver has no time cut-off in the sense of the search (rounds to 250, values up to 254; the largest T found is
well below that) and its least fixed points equal K18's for all 32,539 lines. K18's group search is restricted to roots without
a passer (the note's own rule), no immediate promotion, F_Z = 3 or 4 files, <= 2+2 or 3+2 pawns on ranks 2 to H-1 of F_Z, and
admissible replies that keep s-bar's king on F_Z: all as stated. In this search no sortie has an immediate promotion reply
(0 IMM sorties), so the difference between the text's definition of plain-only and the code's (a safe immediate promotion
counts as a win of both games) is empty.

## Edits

Both OLD blocks occur exactly once in the current LOOPY.md (checked twice, `verify/r3/edits_chk.py`).
NEW is accurate except for these corrections, to be made in EDIT 1 before applying (EDIT 2 is accurate as a description of
what K18 did, but it repeats "108,710 of 108,710", which is right, and nothing else needing change):

1. Replace `flat:6x6, 3 files: 960 (1056)` by `flat:6x6, 3 files: 1,695 (1,829) roots with a plain-only sortie and no escape (no mirror merge: a-c reflection is not a symmetry of the flat board)`.
2. Replace `In 42 of the 2275 legal zero or negative contexts of these three runs ... in the others it is` by `In 42 of the 2,305 legal zero or negative contexts of these three runs (ES 1,017, ES7 601, E3 687) ...`, and fix `summary.json` (2,263 punished).
3. Replace `usually with T_k = T_0 + k` by `in about half (487 of 953) with T_k = T_0 + k`.
4. Label the counterexample CHECKED-2 (ref3 and kpp agree), and the budget values k = 1..6 CHECKED-2 (second implementation: verify/mine/mylg.cpp, all 941 classes).
5. Relabel Proposition 8.1: "PROVED" -> "proof with one gap (e.p. lapse), see VERIFY.md of K18"; add the lapse option to the plain game or the no-e.p.-only-move hypothesis; keep "(P3) fails in the ES tests (checked for every strategy sigma)".
6. Add to the mechanism sentence: in all 29 ES failures a free White context pawn promotes in 3 moves, so mu_s <= 3 <= T and (L2) fails; keep the king-captures-pawn sentence only as a CONJECTURE.
7. Say that E1 (reservoir) and the E3 numbers other than the six failures, and the chess runs, are as K18 reported and were not re-run by the referee.

## Reproduce (all under one CPU-minute each except the 4-file searches, about 10 s CPU)

* Solver: `c++ -O2 -std=c++17 -o mylg verify/mine/mylg.cpp` (the binaries were deleted at the end).
* Search: `mylg --board cyl:8x6 --fz 3 --maxw 2 --maxb 2 --kmax 0 --queen 1|0 --search`; compared with `verify/mine/cmp_search.py keep/search_c8x6_f3_22.out.gz <my q1 file> <my q0 file>` (my outputs are `verify/mine/s22_q1.txt.gz`, `s22_q0.txt.gz`, `s22_k6_q1.txt.gz`, `s_flat6x6_q*.txt.gz`; gunzip first).
* Section 5.1: `mylg --board cyl:8x8 --fz 3 --maxw 1 --maxb 1 --kmax 8 --queen 1|0 --query < verify/mine/q51.txt`.
* Full-board checks: ref3 (`c++ -O2 -std=c++17 -o ref3 kings/delegate/out/K23/verify/ref3.cpp`), `ref3 --board cyl:8x6 < positions`; the 232,343 positions are in the gzip `verify/mine/posAll_ref3.txt.gz` (with ref3's value); `cmp_bare_all.py` needs the dumps (regenerate with `mylg --search --dump`).
* Contexts and ES, ES7, EP, p3: `verify/r3/ctx_enum.py`, `es_rep.py`, `es_run.py`, `es7_rep.py`, `ep_rep.py`, `p3_gen.py` + `mylg --fquery`.
* Lapse test: `LAPSE=1 mylg --board cyl:8x6 --fz 3 --maxw 3 --maxb 3 --kmax 0 --queen 0 --query < verify/mine/stale.txt` (INF) and the same without `LAPSE` (T = 2).
