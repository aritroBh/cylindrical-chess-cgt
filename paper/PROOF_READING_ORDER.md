# Reading order for the AI-written proofs

Page numbers are those of `dist/tog/supplement.pdf` (68 pages, build of 2026-11-26; S17 gained a paragraph on the Lean check, and the pages of S12 to S16 are those of the 67-page build of 2026-11-23).
The 10-page paper's ⟨S⟩ claims rest on about 43 of these pages: S12.1 (pp. 17–23) and S13–S15 (pp. 28–63).
S12.2 (pp. 23–27) is not needed for them; S12.1 is self-contained.

Each item lists what it proves in the paper, what it uses, and the steps where a referee already found an error
(read those slowest).

## Part A. Kings and sums (S12.1, 7 pages)

| # | Read | Pages | Proves (10-page paper) | Uses | Read slowest |
|---|---|---|---|---|---|
| 1 | A.10, then A.15–A.17 | 20, 22–23 | Certificate sentence, Section IV | A.10 only | The timing clause of A.16 ("no later than"; the reply itself can be mate) and Steps 1–4. A.17: the theorem is about the promotion game only. |
| 2 | A.2, then A.11–A.13 | 17, 21 | Validity theorem and corollary (Theorem 3, Corollary 4) | A.2, A.10 | The corollary holds per side to move, not for both (the 10-page paper now says so). A.2(c) needs five ranks. |
| 3 | A.1–A.9 | 17–20 | Sum safety (Theorem 6) | nothing outside | A.7: the induction runs over positions with their actual side to move; the step that drops an unusable e.p. right uses A.4(a). A.6 (frontier) is the hardest lemma. Check the "(E) cannot be dropped" position by hand on a board. |
| 4 | A.14 (optional) | 21–22 | Proposition 7, labelled ⟨C2⟩ (computed, not an AI proof) | the race rule and BIG = 256 | One position; it can be played through on a board. The race rule was missing from the statement once. |

## Part B. Rings (S13–S15, 36 pages)

Every ring proof has two parts. The hand part shows that inserting two files leaves the reduced game unchanged
(Lemmas 1–3). The computed part is one base graph and the small widths. Reading can check only the hand part;
the computed part can only be rerun (S17, pp. 64–68, says which programs agree).

| # | Read | Pages | Proves (10-page paper) | Read slowest |
|---|---|---|---|---|
| 5 | S13 | 28–31 | Wall rings ★2 with n+3 pawns, n ≥ 5 | Lemmas 1–3. Everything below rests on them. This text was rewritten on 2026-11-23 after an other-vendor referee found that Lemma 2(b) named the wrong capture in one case and that step (iii) of Lemma 3 had a gap; read those two places slowest. |
| 6 | Note 1 | 36–42 | n+2 pawns ★2, even n ≥ 8; the full proof of Lemma 3 (§2b) | The ten-file arc c−4..c+5: why a move outside it cannot see the inserted files. |
| 7 | Note 2 | 42–44 | n+2 pawns ★3, even n ≥ 8 | H2 windows and the reason for n ≥ 22 in H6 (both were wrong once). |
| 8 | S14 | 32–35 | One pawn per file ★2, n ≥ 10 | H7: the heap test is "≡", and in what sense it gives G = ★2. The colour-reversal step. |
| 9 | Note 4 | 50–54 | n+1 pawns ★3, n ≥ 12 | Same H7 point for ★3. |
| 10 | Note 3 | 44–50 | n+2 pawns ★2 and ★3, odd n ≥ 11 | The single cut c = 6 and base n = 19. |
| 11 | Note 5 | 54–59 | Möbius strip ★2, one pawn per file, ≥ 10 files | Lemmas 1–3 restated for the strip; pawns reversed across the seam. |
| 12 | Note 6 | 60–63 | Möbius strip ★3, n+1 pawns, n ≥ 11 | The insertion step: a far reply can change a file near the cut (a sentence saying otherwise was false). The range 4 ≤ c ≤ n−6. |

## Part C. Optional: two statements of supplement Section S2

S12.2 (pp. 23–27): A.18–A.18b (theorem on outcomes with spare king moves) and A.19–A.19b (frozen-king passed-pawn test).
Supports two statements of supplement Section S2, not the 10-page paper. Newly condensed on 2026-11-23; read slowest:
- A.18 and A.18a: the proof was rewritten with explicit strategies (a forcing strategy that never passes, a blocking strategy
  that may pass) instead of the note's stage argument, which had needed a correction because a winning move can be a pass.
  Check the bound of 2h+1 moves and that suicides never enter the strategies. An other-vendor referee found that
  A.18(b),(c) were false as first written (the blocking strategy used a pass the blocker need not have); they now grant
  the pass explicitly. Check that each case of A.18a uses a blocker only where that side can wait.
- A.18b: the pass of the spare-move game keeps the e.p. right, while a real king shuttle ends it; the remark says the
  theorem does not treat this.
- A.19: the passer test is proved for frozen kings only. Check the e.p. step, that no capture lands ahead of the passer, and
  the move count (hypothesis H5 counts every enemy pawn and every sequence of enemy moves). The flat-board case is stated
  although the note writes out only the cylinder.

## What to note down

For each item: "read, agree", or the page and sentence you doubt. A doubt gets fixed or refereed again.
When you are done, Section XIII, S17 and the AI statement change to name exactly the items you read, and no others.
