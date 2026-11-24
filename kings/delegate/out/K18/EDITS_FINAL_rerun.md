# EDITS_FINAL for K18 (fix round rerun, 2026-10-28): no EDIT blocks, on purpose

Integrator notes (this prose is outside the EDIT blocks, which are the only part `apply_edits.py` reads). This file contains
zero EDIT blocks. Applying it changes nothing: `apply_edits.py` reports 0 applied, 0 rejected.

## Why there is nothing to apply

The task text for this round says the K18 edits were written against a LOOPY.md that did not yet contain them. That is out of date.
The current `kings/theory/LOOPY.md` (HEAD 3123e218) already holds the K18 edits in full, integrated in commit 08267b69 ("K18
integrated (open question 1) ... Proposition 8.1 PROVED after repair") and amended in 68f3ebf5. `kings/delegate/out/K18/REVIEW.md`
records the earlier rounds: `EDITS_FINAL.md` (first fix round, repaired Proposition 8.1 with (P1e)), a fresh referee's
`verify/P81_RECHECK.md` (ACCEPT_REPAIR), `EDITS_FINAL2.md`, and `EDITS_FINAL3.md` (the version the integrator applied: 3 blocks, 0
rejected). The first version of this file (the 32,257-byte first-round set) was committed in git before this overwrite; it is
recoverable from history and is superseded by `EDITS_FINAL3.md`.

Checked mechanically today: the K18 heading and body OLD texts (the "question is untested" bullets) occur 0 times in the current
LOOPY.md. The Appendix A OLD text (the K24 bullet) still occurs once, so re-applying the old K18 block would add a second, duplicate
K18 bullet to Appendix A. That is why no block is written here. Do not apply `EDITS.md`, an old `EDITS_FINAL*.md`, or this round's
earlier output on top of the current LOOPY.md.

## The eight referee fixes, as they stand in the current LOOPY.md (section 8, item 1; Appendix A)

1. Flat 6x6: no class count; "1,695 (1,829) roots with a plain-only sortie and no outright escape, not merged" and the reason
   (a-c reflection is not a symmetry of the flat board). Present, with the old "960 (1056)" named as invalid.
2. "about half": "in about half of them, 487 of 953, with T_k = T_0 + k", with the other increment patterns named. Present.
3. Totals: 42 of 2,305 legal (ES 1,017, ES7 601, E3 687), 2,263 punished (29, 7 and 6 failures). Present. `summary.json` still says
   2233; it is the investigator's output and was left verbatim (REVIEW.md notes it as stale).
4. The mechanism sentence "(L2) fails because a free context pawn promotes in 3" is not used as a mechanism. LOOPY states the
   referee's measurement as data only: in all 29 ES failures a free White context pawn promotes within 3 moves while T = 4 to 7,
   so (L2) fails there and Theorem 2.7 does not apply to those 29 cases; "It is data, not a mechanism". The king-captures-the-pawn
   guess is kept only as a CONJECTURE. Judgement call: the instruction says to drop a mechanism sentence; this measured fact
   is not a mechanism claim, and it is the referee's own point 6, so it stays, labelled COMPUTED-1.
5. Proposition 8.1: the e.p.-lapse gap was repaired in full with the added hypothesis (P1e) and a rewritten proof, then re-derived
   by a second referee (P81_RECHECK.md, ACCEPT_REPAIR). Label in LOOPY: "PROVED after repair (re-derived by a second referee,
   same model family)". The lapse-game form that might remove (P1e) is a CONJECTURE, with the 0-violation test as COMPUTED-1.
   Note for the integrator: the task allowed either a full repair or a downgrade to CONJECTURE. The repaired proof is a full proof,
   AI-derived twice, no human check; if that is judged too weak for PROVED under the LOOPY label rule, the one-line change is
   PROVED -> CONJECTURE (evidence COMPUTED-1 / CHECKED-2) in the Proposition 8.1 heading and in the item-1 summary sentence.
6. The Y counterexample (`Ka1 Pa2 kc1 pa3`, m = Ka1-h1, G = `Pe2 Pg2 pf4`) and the budget values k = 1..6: CHECKED-2. Present
   (two solvers agree on the counterexample; two implementations give the budget vectors for all 941 classes).
7. E3 (the 681 cases not re-run), E1 (reservoir) and the chess runs: COMPUTED-1. Present.
8. EDIT 1 corrections (verdict wording, CONJECTURE for the promotion-free form, flags for what the referee did not re-run):
   present in "Verdict on open question 1".

Open question 1 answer, as it stands: tempo matching is false as worded in P (CHECKED-2); it held in every promotion-free test run
(contexts with no pawn race or capture sequence that promotes), 0 failures in 292 cases in which s has no more spare moves than s-bar
(CONJECTURE; 123 of 292 CHECKED-2). Exact boundary: the 5 promotion-free zero contexts of the 4160 against 25 + 6 sorties (153
legal cases) and the reservoir contexts with Delta <= 0 (139 cases); no promotion-free negative or positive context exists in the
family; model P, at most 2 + 2 pawns, 3 or 4 files of `cyl:7x6` and `cyl:8x6`, contexts of at most 2 + 2 pawns (modules up to 3).

Stale statement to correct elsewhere (not in LOOPY): `kings/delegate/out/K18/summary.json` "punished": 2233 should read 2263.
