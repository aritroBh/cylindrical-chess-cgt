# T27: report (agent text) with the verifier's findings

Written by the orchestrating session on 2026-10-22. The subagent could not write report files, so its
final message is reproduced verbatim under "Agent report". An independent Sonnet verifier then tried to refute
it; its verdict, summary and fix list come first and **take precedence over the agent text where they differ**.

## Verifier verdict: ACCEPT_WITH_FIXES

I could not refute the claims. REPORT.md and VERIFY_T27.md are both absent. No REPORT.md exists in /Users/aritro/Downloads/Research/Chessendgames/research/star27_textbook3/. The agent says its session blocked report files, and my session blocks them as well, so I did not write VERIFY_T27.md. I treated the agent's reply, relayed in the task text, as the report and checked it against the evidence files, which are all present. I therefore did not return NO_REPORT. Whoever has write access should save the reply as REPORT.md.

I recomputed independently:
- A fresh awk count over all five T24 split files gives 16, 16, 14 and 22 hits for count/T, count/off, mover/T and mover/off, and 0 in both aware columns. There are 26 distinct positions, all in the 4+4 file; the other four files have none, even in the opponent columns. The files hold 32,951,871 rows, matching T24's root total.
- A solver I wrote from the rules, with no code from cylcgt, the scanner or solver.py, finds that G+*k is a second-player win only at k=3 for all 16 count/off hits and all 22 mover/off hits. The gadget `W c2 e2 / B d7 f7` comes out *2 and the a-file group `W a2 a4 / B a3 a6` comes out *. Ten scanner non-hit cells give no k in 0..4.
- cylcgt reproduces `*3` for hit 1 under count/off, count/T and mover/off, and `{{3*|1*}|{-1*|-3*}}` under count/aware. The paper's 4-file gadget `W a2 c2 / B b7 d7` is *2 with e.p. off and under the textbook test, and `{2±1|-2±1}` under the aware test.
- `why_aware.py` rerun gives 835 reachable positions, 225 non-terminal, 35 differing between e.p. off and aware, and 0 between off and the textbook test.

The 68 cells, 26 positions, 234 of 234 cylcgt-versus-scanner matches and the 27 s maximum all check out against `all_hits.tsv` and `cylcgt_results.tsv`. The solver tables back claims 3 and 5. The labels are justified: CHECKED-2 for the values, COMPUTED-1 for the completeness of the hit set and the structure. The scanner is standalone C that tests nimbers up to k=63, so its `-1` really means not a nimber.

The fixes below are presentation only; none changes the verdict.

### Fixes and problems found by the verifier

- REPORT.md is missing from research/star27_textbook3/, so the brief's deliverable was not met. The reply states it was blocked by the harness. The reply text should be saved as REPORT.md, with a 5-line summary first, by a session allowed to write it. The relayed reproduce list is also truncated at 'PYTHONPATH=. .venv/bin/pyth'; the remaining commands should be completed (decompose.py, explain_star3.py, why_aware.py and make_table.py exist in the directory).
- Multiplicity is overstated. The 16 count/off hits are 8 colour-reversal pairs, since swapping colours and flipping ranks maps a hit to a hit. Example: `W a2 a4 c2 e2 / B a3 a6 d7 f7` pairs with `W a3 a6 d2 f2 / B a5 a7 c7 e7`. The 4 b-file hits are 2 pairs. Across all cells the 26 positions fall into 15 classes under colour reversal, or 13 with left-right mirror. The report should say '16 listed (8 up to colour reversal)', and likewise for the 26. The existence verdict is unaffected.
- Completeness of the hit set rests on the C scanner alone, which is COMPUTED-1: nobody re-solved the other 33 million roots. The reply labels this correctly in item 1, but item 4 ('16 positions are *3') is best worded as 'at least these 16, all verified three ways' for the existence claim, with the full count carrying the COMPUTED-1 label.
- Minor factual slip: 'slowest position 541 s and 120 MB'. The 541 s run used 88 MB; the peak RSS anywhere is 170 MB. State the exact figures.
- Wording: 'locked a-file pair' is loose. In the 12 count-rule sums the a-file piece is a 2-versus-2 group (four pawns, one free square, value *). In the mover-only sums it is a lone 1-versus-1 pair, or `f2/f4`.
- Scope and dependence caveats should sit next to the verdict, not only in the caveats list. The *3 needs the count or mover race rule (the opponent rule gives *1 for hit 1), and the mover-only hits depend on the mover rule being a mover-wins race. The 122 opponent-rule cells survive the aware test, so 'the aware test removes them' holds only for count and mover. The hits are a *3 of the pawn-only model without en passant, not of chess. The reply already says the model is not exact chess; it should connect that statement to the verdict.
- Downstream wording: RESULTS.md (the section on searching for other *k) is scoped to widths 1-4 and 6 pawns, so it is not contradicted. T24's REPORT.md still states 'no *3 under count or mover' in three places; it should get an erratum note pointing to T27.

### Claims the verifier recomputed

- **agrees.** Claim: Hit counts from T24 files: count/T 16, count/off 16, mover/T 14, mover/off 22, 0 in aware cells, 68 cells on 26 distinct positions, all in 4+4; other four splits have none
  Recomputed: Own awk, one pass over all five flat_w6p8_*.tsv files. Per column, 4_4 gives col4=16, col5=16, col6=0, col7=14, col8=22, col9=0, opponent 40/2/80, with 26 distinct count-or-mover positions. 2_6, 3_5, 5_3 and 6_2 give 0 in all nine columns. Row total is 14,685,961 + 2×8,201,425 + 2×931,530 = 32,951,871, equal to T24's root count. all_hits.tsv has 68 rows and 26 distinct positions.
- **agrees.** Claim: T24's prose 'no *3 under count or mover' contradicts its own table
  Recomputed: research/star3_hunt/REPORT.md lines 12, 36 and 155 say there are none. Its summary table shows 16/16/14/22 in the *3+ column. My awk counts match the table.
- **agrees.** Claim: Each count/off hit (16) and each mover/off hit (22) is exactly *3 for an independent whole-board solver
  Recomputed: My own solver (written from the rules, count and mover race, e.p. off, first passed pawn ends the game) tested G+*k for k=0..4. All 16 count/off and all 22 mover/off hits give outcome classes N N N P N, so the least k with a P-position is 3. The run is sub-second per position, since it needs outcomes only rather than canonical forms. Negative controls (10 positions that the scanner says are not *3 under count/off) give no P at any k in 0..4.
- **agrees.** Claim: cylcgt agrees with the scanner on all 26 × 9 = 234 cells, at most 27 s per value
  Recomputed: cylcgt_results.tsv has 234 rows, 234 'yes' and 0 'NO', 26 positions, 26 rows per setting, maximum 27.26 s. I recomputed hit 1 with cylcgt: *3 under count/off, count/T and mover/off, and {{3* | 1*} | {-1* | -3*}} under count/aware.
- **agrees.** Claim: Independent solver.py gives *3 on all 16 count/off and 22 mover/off hits, *3 on the 16 count/T and 14 mover/T hits, and {{3*|1*}|{-1*|-3*}} for the 16 count e.p.-aware cells
  Recomputed: Read every codex_*.tsv. codex_count_off_cheap (12) plus codex_count_off_exp (4) give 16 *3. codex_mover_off has 22 lines, all *3. codex_count_epon_textbook has 18 lines, 16 of them *3 (the other two, rows 6 and 23, are not hits). codex_mover_epon_textbook has 14 lines, all *3. codex_count_epon_aware has 16 lines, all {{3|3}|{1|1}}|{{-1|-1}|{-3|-3}}.
- **DISAGREES.** Claim: Slowest solver position took 541 s and 120 MB
  Recomputed: The slowest run is 540.6 s (`W a5 b2 c2 e2 / B a4 a7 d7 f7`, count/e.p.-on/aware), but the RSS column for that run is 88 MB. The largest peak RSS anywhere is 170 MB, in the count/T textbook runs. No run shows 120 MB. The time matches; the memory figure is imprecise.
- **agrees.** Claim: Structure: 12 of the 16 are a locked a-file pair (*) plus c2 e2 / d7 f7 (*2), a translate or mirror of the paper's candidate; the other 4 have a b-file pawn and form one 8-pawn component that is *3 as a whole
  Recomputed: decompose.out and cylcgt give components * and *2 for the 12 sums. My solver gives * for `W a2 a4 / B a3 a6` and *2 for `W c2 e2 / B d7 f7`. Rows 3, 9, 22 and 26 have b pawns, so all six files are occupied and they are one component with value *3. Wording nit: in the 12 sums the a-file piece is a 2-versus-2 group (four pawns, one free square), not a pair.
- **agrees.** Claim: 10 mover hits are mover-only; 8 of them are * plus a 3-per-side component that is *2 only under mover/off
  Recomputed: 22 minus the 12 shared with count/off gives 10, namely rows 6, 16-21, 23, 24 and 25. decompose.out shows rows 16-21, 24 and 25 as * (`f2/f4` or a lone a-file pair) plus a 3-versus-3 component that is *2 under mover/off and complicated under count/off and mover/T. Rows 6 and 23 are the two b-file ones.
- **agrees.** Claim: Option anatomy of the first hit: a4-a5 gives *2, e4 gives *, c4 gives 0, e3 and c3 are dominated and reversible through -1*, and d7-d5 refutes them; the canonical form is {0,*,*2 | 0,*,*2}
  Recomputed: explain_star3.out matches the claim. cylcgt gives `W c2 e3 / B d5 f7` = -1 and `W c2 e3 / B d7 f7` = -1/2±1/2. I checked by hand that {*|-1*} is at most 0, so it is dominated by the c4 option.
- **agrees.** Claim: Why the aware test removes the hits: in the 4-file gadget 35 of 225 non-terminal values change (e.p. off versus aware), and the root changes from *2 to {2±1|-2±1}; the textbook test with e.p. on changes none; with e.p. off the textbook and aware tests coincide
  Recomputed: Reran why_aware.py: 835 reachable, 225 non-terminal, 35 differ (off versus aware), 0 differ (off versus textbook). cylcgt gives the root as *2 (off), *2 (textbook, e.p. on) and {2±1|-2±1} (aware). In pawns.py, ep_capturable needs pos.ep, which is never set when Board.ep is False, so the tests coincide with e.p. off.
- **agrees.** Claim: The 122 opponent-rule cells (O/T 40, O/off 2, O/aware 80) were not checked and keep *3 under the aware test
  Recomputed: My awk count gives 40, 2 and 80 in cols 10-12 of the 4+4 file, i.e. 122 in total. I did not verify them further. For hit 1 the opponent rule gives *1 in cylcgt (and `N,1` in the scanner), so the 16 hits depend on the count or mover race rule.

## Agent report (verbatim)

T27 result: there is a \*3 under the count rule with e.p. off on six files, and it is CHECKED-2. I did not write `REPORT.md`, because this subagent session blocks report files. This reply carries its content, and the evidence files are in `/Users/aritro/Downloads/Research/Chessendgames/research/star27_textbook3/`.

1. **Hit set (COMPUTED-1, reproduced by a fresh stream of the 5 T24 files).** There are 68 hit cells on 26 distinct positions, all in the 4+4 split. Counts match T24's table: count/T 16, count/off 16, mover/T 14, mover/off 22, and 0 in e.p.-aware cells. The 2+6, 3+5, 5+3 and 6+2 files have none. T24's prose summary ("no \*3 under count or mover") contradicts its own table; the table is right. The single hits file is `all_hits.tsv`.
2. **cylcgt versus the scanner (CHECKED-2).** All 26 × 9 = 234 cells agree in outcome and nimber (`cylcgt_results.tsv`). cylcgt took at most 27 s per value, so the 20-minute sampling fallback was never needed.
3. **Independent solver `verify_ext/codex/solver.py` (CHECKED-2, now three programs).**
   - It gives exactly \*3 on all 16 count/off hits and all 22 mover/off hits.
   - It gives \*3 on all 16 count/T and all 14 mover/T hits.
   - Its e.p.-aware value for the 16 count hits is `{{3*|1*}|{-1*|-3*}}`, which is not a nimber.
   - The slowest position took 541 s and 120 MB.
4. **Verdict.** Yes, 16 positions on the flat 6-file board are \*3 with count and e.p. off, for example `W: a2 a4 c2 e2 / B: a3 a6 d7 f7`. With e.p. off the textbook and e.p.-aware tests coincide, so it is not a passed-pawn-test artifact. It is a \*3 of pawn play without en passant, not of chess.
5. **Structure (COMPUTED-1, cylcgt decomposition).**
   - Twelve of the 16 are a sum: a locked a-file pair (\*) plus `W c2 e2 / B d7 f7` (\*2, a translate or mirror of the paper's candidate). That is \*2 + \* = \*3, so it is not a new phenomenon.
   - The other four have a b-file pawn joining everything into one 8-pawn component. They are \*3 as a whole, and I did not explain them.
   - Of the mover hits, 10 are mover-only; eight of those are \* plus a 3-per-side component that is \*2 only under mover with e.p. off.
6. **Option anatomy of the first hit (cylcgt).**
   - White's moves are a4–a5 → \*2, e2–e4 → \*, c2–c4 → 0, and e2–e3 and c2–c3 → `{*|-1*}` and `{0|-1*}`.
   - e3 and c3 are dominated and reversible through −1\*; Black refutes them with d7–d5.
   - Each side keeps {0, \*, \*2}, so the position is \*3 (output in `explain_star3.out`).
7. **Why the e.p.-aware test removes them (e.p. on only).** In the 4-file gadget `W a2 c2 / B b7 d7`, 35 of 225 non-terminal values change between e.p. off and e.p. on with the aware test, including the root (\*2 becomes `{2±1|-2±1}`). With the textbook test and e.p. on, 0 change. A double step beside an enemy pawn, such as `W a2 c2 / B b4 d4` with a2–a4, is passed at once with e.p. off or the textbook test. With the aware test it is capturable by b4×a3 e.p. and is not passed. The test does nothing to the e.p.-off game, so the 16 hits remain there. With e.p. on and the aware test, none of the 26 positions is a nimber under count or mover.
8. **Caveats.**
   - All three programs share one model (pawns only, flat board, no kings, race rules that are not exact chess), so CHECKED-2 means the implementations agree, not that the model is chess.
   - Scope is 4+4 roots on width 6 only.
   - I did not check the opponent-rule cells (122: O/T 40, O/off 2, O/aware 80). They keep \*3 even under the aware test (scanner only, COMPUTED-1).
9. **Reproduce** (from the project root, in order):
   - `nice -n 10 sh research/star27_textbook3/extract_hits.sh`
   - `sh research/star27_textbook3/collect_rows.sh`
   - `PYTHONPATH=. nice -n 10 .venv/bin/python research/star27_textbook3/verify_cylcgt.py > research/star27_textbook3/cylcgt_results.tsv`
   - `sh research/star27_textbook3/run_codex.sh count off aware 5` (the last argument is the scanner column; use 8 for mover/off)
   - `PYTHONPATH=. .venv/bin/python research/star27_textbook3/explain_star3.py`
   - `PYTHONPATH=. .venv/bin/python research/star27_textbook3/why_aware.py`
10. **Files.** The full hit table is `hit_table.txt` (cylcgt and solver values per hit). The solver outputs are `codex_*.tsv`, the component split is `decompose.out`, and a first agent's superseded files are in `superseded/`. I did not touch `paper/` and ran no git commands.
