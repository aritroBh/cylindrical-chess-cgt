# K71 review (orchestrator), 2026-11-25

Task: remove the computed lemma (Lemma B) from Proposition 4.25 by changing the reduction. One AI investigator,
**not refereed, nothing installed in the note**; kept as a record of what was tried.

**Result: not achieved.** The label of Proposition 4.25 does not change.

- Proved (given F0, a pawnless lemma: lone White king against Black Kb6, pb7, pc6, White to move, Black wins all
  55 positions; CHECKED-2 by two programs without shared code): Black wins after the three king moves Ke3, Ke4,
  Ke5 at q1, and some sub-lines elsewhere. Route: take the c-pawn on c4 first, then b6; at most 9 plies.
- Left: 14 positions (`logs/left14.txt`), lines of 29 to 39 plies. Through K68's Lemma C they use 30 of the 42
  Lemma B positions.
- Route table (`findings.txt`): every other route meets a long fight around a protected c-pawn; "Black king
  stays on files a to c" fails exactly on the four hard positions the K68 referee named.

Use: if the K70 case table (another model's blind attempt at Lemma B as stated) survives its referee, K71 adds
nothing to the proposition; if it does not, K71's 14 positions are the shortest list of what a hand proof must
still cover.

Process: toy runs only (about 10 s, under 30 MB each); no rule broken by its own report.
