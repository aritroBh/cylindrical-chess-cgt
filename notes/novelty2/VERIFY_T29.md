# VERIFY_T29: adversarial check of the T29 novelty report

Verifier: Sonnet 5.5 subagent, 2026-10-22. Verdict: **ACCEPT_WITH_FIXES**.

## 5-line summary

1. There is no usable report file. `notes/novelty2/REPORT.md` (mtime 00:50) is the OLD unverified text the agent said it could not overwrite. It contradicts the agent's message in several places (it says Muller claimed a forced bishop-pair mate, and that KRK contradicts Muller). **Do not use it; overwrite it from the corrected table below.** The agent's message itself is truncated after item 10.
2. Every literature fact I could re-read agrees with the agent: Elkies 1996 pp. 139 and 148, Elkies 2002 pp. 61, 70-71, Drummond-Cole Fig. 11 (pp. 11-12), Nowakowski GONC5 p. 140 B3, the Muller-hosted quote, OEIS A002187. Two items I could not read myself (Chess Variant Pages text, Gik 1983).
3. Every number I recomputed with my own programs agrees with the paper: KPK 163,328 / 124,960 / 168,024 / 97,604 flat and 160,656 / 126,736 / 165,984 / 92,760 cylinder, 16,538 and 15,930, zugzwangs 160 and 216, Ka6 Pa5 vs Ka8, KQK, KRK 2.80%, KBBK 100% in 14, Dawson g(n), period 34, last exception 51, the zero list, and the ring rule by brute force for n <= 12.
4. Fixes needed in the report: Claim 5 (and the cylinder-values part of Claim 2) omit the project's own `prior_work/main.tex` section 8, which already states the ring rule Ring(n) = mex G(n-3); "only odd ranks" for Elkies 2002 is slightly too strong; one more T15 error was missed (tiny-one is NOT open in Elkies 1996).
5. No overstated novelty found in the agent's labels. The paper itself is exposed on Claim 4: its abstract says K+R "can no longer force mate" with no credit to the prose that already says so (Wikipedia, XBoard/Muller rules page, Chess Variant Pages).

## Recomputed numbers (all by programs I wrote from the rules; light compute, 1 core, nice 10)

Sources are in `notes/novelty2/verify_t29/` (five small files). Run from that directory; the two C files need `cc -O2`.

| Claim | Recomputed | Agrees | Command |
|---|---|---|---|
| Dawson g(n) = octal game 0.137, first 40 values equal OEIS A002187; paper's formula (mex of g(n-2) and g(a) xor g(b), a+b=n-3) equals the octal-code value for n <= 400 | identical | yes | `python3 dawson_check.py` |
| Period 34, last exception n = 51 (g(n) != g(n+34) exactly for n = 14, 16, 31, 34, 51) | same | yes | `python3 dawson_check.py` |
| Cylinder first-player wins n = 3,7,11,17,23,27,31,37,41,45,57,61,65 (g(n-3) = 0) | same | yes | `python3 dawson_check.py` |
| Ring rule by brute force on the real 3 x n game (forced captures, no double step, no promotion), cylinder n = 3..12 and flat n = 1..12 | all 10 cylinder and 12 flat outcomes equal the rule | yes | `python3 dawson_brute.py` |
| Study2025's recurrence agrees with g at 31 of 301 values; wrong cylinder outcomes 56 for n = 3..300, first at n = 4 | 31; 56 (57 if the range is extended to n = 303) | yes | `python3 study2025_check.py` |
| KPK flat: legal 163,328 / 168,024, wins 124,960 / 97,604 | same | yes | `cc -O2 -o vtb vtb.c && ./vtb` |
| KPK cylinder: legal 160,656 / 165,984, wins 126,736 / 92,760 | same | yes | same |
| 16,538 flat draws become cylinder wins; 15,930 flat wins become draws | 9,216 + 7,322 = 16,538; 5,126 + 10,804 = 15,930 | yes | same |
| Mutual zugzwangs 160 flat, 216 cylinder | same | yes | same |
| Ka6 Pa5 vs Ka8: draw on flat (both sides), win on cylinder (25 plies WTM, 26 BTM) | same | yes | same |
| KQK: flat 100% / 10, cylinder 100% / 10; KRK flat 100% / 16, cylinder 2.8015% / 3 | same | yes | same |
| KBBK opposite colours: flat 99.9792% / 19, cylinder 100% / 14 | same | yes | `cc -O2 -o vtb_bb vtb_bb.c && ./vtb_bb` |
| *2 values: C3 ring `W a2 a3 b2 / B b7 c6 c7`, C4 ring `W a4 b2 c2 / B b6 c5 d6 d7`, positions A and B are *2; the a2 c2 / b7 d7 candidate is {2+-1 / -2+-1} (repo engine only, so COMPUTED-1) | same | yes | `PYTHONPATH=. .venv/bin/python` with `pw.describe(Board(...), Pos.parse(...))` |

Notes on the numbers:
- The 16,538 counts (position, side to move) pairs, not placements. The paper's sentence "16,538 ordinary-board draws become cylinder wins" is true only in that sense (WTM 9,216 and BTM 7,322). Say so.
- My KPK solver uses all four promotions (sub-tables for Q, R, B, N). I did not test the paper's separate queen-only comparison (6 ordinary-board differences).
- I did not recompute the C5/C6 ring counts or the seven-pawn census (shared machine, heavy), so the "n+3" rule for n >= 4 rests on the paper's own labels, not on me.

## Literature claims: what I re-read

All via WebFetch or WebSearch (about 20 requests plus 4 searches, no bulk traffic). PDFs saved locally and read with pdftotext.

| Agent's statement | My check |
|---|---|
| Elkies 2002 pp. 61-78; abstract on p. 61 | Confirmed from the MSRI PDF (Vol. 42, pp. 61-78); Drummond-Cole's reference list gives the same pages. |
| Abstract: construction works for m >= 9 | Confirmed ("Our construction works for m >= 9 and n sufficiently large"). |
| Diag. 6A is "9 rows by 12 files", p. 70; even-rank boards need more work | Confirmed on printed p. 70, same page as the "odd number of rows ... orthodox 8x8 ... work harder" passage. p. 71: "at least n+6 files whose height is an odd number greater than 5". The *2 component (Diag. 7A/7E, stopped files) runs over pp. 71-73; "longer boards of odd height >= 9" is on p. 73. |
| Elkies 1996 lists *2 on files of 6 and 7 ranks, pp. 139 and 148; asks about *2 on 8x8 or larger as open | Confirmed. p. 139: value is * or *2 "when the board has width 5 or 6". p. 148: "Do *2, *4 and higher nimbers occur on the 8x8 or larger boards?", Pa2 vs Pa5 (length 6) and Pa2 vs Pb6 (length 7) give *2. Elkies 2002 itself quotes this as "[Elkies 1996, p. 148]". |
| Drummond-Cole 2005, Integers 5 #G06, Fig. 11, pp. 11-12: orthodox legal position of value *2 using other pieces | Confirmed. Fig. 10 (8x8, "arbitrary setup", p. 10) and Fig. 11 (reached by a legal game, move list pp. 11-12) use Q, R, B, N and pawns. The paper cites Elkies 2002 as pp. 61-78, so T15's "likely the same construction as Elkies 2002" is wrong. |
| Nowakowski, GONC 5 (2017), p. 140, Problem B3: Elkies' *k conjecture "on sufficiently large chessboards" | Confirmed (MSRI Publ. 70, p. 140; also gives "[MGONC, pp. 61-78]"). |
| Muller-hosted rules page: "Two Knights and Bishops in any combination cannot do that either." No author line | Confirmed on hgm.nubati.net/rules/Cylinder.html (no credit line; the page says a lone rook, bishop or knight cannot force mate and does not discuss the queen). The paper's KBBK row (opposite-colour bishops win 100%, mate in 14) does contradict it, and I reproduced that row. |
| Wikipedia "Cylinder chess": K+R cannot mate, no citation; K+Q cannot mate on a torus, citing Gik 1983 | Confirmed. The Gik citation is attached to the K+Q sentence; the K+2R sentence has no separate citation in the page text I fetched. Gik himself not read (nor by the agent). |
| Chess Variant Pages (rewritten 2019, Greg Strong): lone rook cannot win, queen and bishop pair can | NOT confirmed by me: every chessvariants.org URL returned 403. Search-engine snippets say the same thing, so plausible but second-hand. |
| OEIS A002187: period 34, last exception 51 | Confirmed ("Has period 34 with the only exceptions at n=0, 14, 16, 17, 31, 34 and 51"); my computed list of g(n) != g(n+34) is 14, 16, 31, 34, 51, same last element. |
| Errors in T15: paraphrases passed off as quotes, "pp. 1-21, 2000", Drummond-Cole = Elkies 2002 | Confirmed (T15 quotes "Does *2 occur on an 8x8 board with kings and pawns only?" and "We do not know whether 1/8, up-2 or tiny(1) can be realised"; neither is in Elkies 1996). The 21 is the page count of the arXiv version. |
| 24 searches / 42 requests, no Scholar or MathSciNet | Plausible; nothing in my 4 searches contradicts NOT FOUND. |

My own searches (4) for a K+P *2 on 8 ranks and for any CGT on cylinder boards returned only Elkies 1996, Elkies 2002 and unrelated pages.

## Problems and fixes

1. **Report not persisted.** `notes/novelty2/REPORT.md` still holds the old text, which is wrong on Muller, on Claim 4 (says KRK contradicts Muller; the real contradiction is KBBK) and on Claim 5 framing. The agent's message also ends mid-sentence at item 10. Rewrite the file from the table below.
2. **Claim 5 omits a self-prior.** The author's own 2025 study (`prior_work/main.tex`, section 8, line 219) already says "Ring(n) = mex(G(n-3)) ... the Grundy value for the ring is always either 0 or 1", for an abstract ring game with a wrong recurrence. The paper cites it (`Study2025`, unpublished). Correct label: PRIOR (own, unpublished) for the ring formula; what is new is the 3 x n chess derivation (forced five-ply captures), the corrected g, and the misere remark. External literature: NOT FOUND stands.
3. **Claim 2, same gap.** `prior_work/main.tex` computes CGT values on the cylinder (basic values, rings, a-h connected files). Label Claim 2's "no CGT on a cylinder" as RELATED (own unpublished 2025 study), while the n+3 ring-*2 rule is NOT FOUND.
4. **Elkies 2002 wording.** "Builds *2 only on boards with an odd number of ranks" should read: constructions and diagrams (6A, 7A, 7E) are on odd heights >= 9; the abstract states m >= 9 with no parity condition; even heights (the 8x8) are described as needing more work, not as impossible.
5. **A second T15 error the agent missed.** T15 section 4 says Elkies 1996 lists tiny(1) as open. It does not: Elkies 1996 builds tiny-one (Diagram 9, p. 144, with knights on the board) and says tiny-n for any n on larger boards; p. 148 says "We have seen how to construct tiny-x for integers x >= 0". Only 1/8 and the higher ups are asked there. The paper's abstract line "We also find ... Tiny 1" should say K+P only in the trebuchet model, or be dropped.
6. **Claim 4 exposure in the paper, not the report.** Abstract and intro present "king and rook can no longer force mate" and "on the torus only two major pieces force mate" without credit to Wikipedia, the XBoard/Muller rules page, the Chess Variant Pages or Gik. The numbers (2.80%, mate depths, all 24 tables) are new; the qualitative statements are not. Add a citation or soften.
7. **Claim 1 scope.** NOT FOUND is correct, but the paper's *2 holds only in the model (count rule, e.p.-aware test, frozen kings); positions A and B have open real-chess oracle values (`14_conclusion.tex`, item 2). The T29 summary line should say "in the model".
8. **Limits of this check.** I did not read Gik 1983, Winning Ways, Guy's "Twopins", Plambeck-Siegel or the Chess Variant Pages text myself.

## Corrected claim table (for the new REPORT.md)

| # | Claim | Verdict | Notes |
|---|---|---|---|
| 1 | K+P *2 on 8x8, seven pawns plus T, in the model | NOT FOUND | RELATED: Elkies 1996 pp. 139, 148 (*2 only on 6- and 7-rank files); Elkies 2002 pp. 61, 70-71 (*2 constructions on odd heights >= 9); Drummond-Cole 2005 Fig. 11 (8x8, other pieces); Nowakowski 2017 p. 140 B3 |
| 2 | First ring *2 on Cn has n+3 pawns | NOT FOUND | RELATED (own, unpublished): Study2025 values on the cylinder |
| 3 | Cylinder KPK, rook-pawn draw becomes a win, 16,538 | NOT FOUND | RELATED: "no edge pawns" remark; 16,538 counts (position, side to move) pairs |
| 4 | KRK cannot mate on the cylinder, KQK can | PRIOR in prose (Wikipedia, XBoard rules page; CVP second-hand); numbers NOT FOUND | KBBK: Muller-hosted page says no, paper (and my solver) says yes: 100%, mate in 14 |
| 5 | 3 x n cylinder Dawson's chess is a first-player win iff g(n-3) = 0 | External: NOT FOUND | PRIOR (own, unpublished): Study2025 section 8 states Ring(n) = mex G(n-3) with a wrong g |
