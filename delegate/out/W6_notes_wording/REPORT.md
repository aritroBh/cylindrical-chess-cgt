# W6 notes wording report

All edits were applied by exact-string replacement in Python, with an assertion that each old string occurs exactly once. The script is in the session scratchpad; edits.json in this folder lists every old/new pair. Only the following files were edited: dist/tog/supp_src/s14_ringn.md and s15_note1.md to s15_note4.md. No number, family, node count, cut, base width or evidence label was changed. Nothing was built, staged or committed.

## Edits

### 1. s15_note1.md

- Old: insertion), quoted in section 2 |
- New: insertion), restated in section 2 |
- Why true: Item 1. The note restates the lemmas in its own words; it does not quote them.

### 2. s15_note1.md

- Old: (with the repaired definition of section 2)
- New: (restated in section 2)
- Why true: Item 1. proof.tex now defines pattern file exactly (lines 52-53), so section 2 restates it and repairs nothing.

### 3. s15_note1.md

- Old: (statements quoted from Lemmas 1-3 there)
- New: (statements restated from Lemmas 1-3 there)
- Why true: Item 1. Same reason as above, in the heading.

### 4. s15_note1.md

- Old: The statements of Lemmas 1-3 below are those of Section S13. They rely
- New: The statements of Lemmas 1-3 below have the hypotheses and conclusions of Section S13 in abbreviated wording (in Lemma 3 the insertion is that of Section S13, paragraph "Insertion"). They rely
- Why true: Item 1. Lemmas 1-3 in the note have S13's hypotheses and conclusions, but the wording differs (R(g), the inline ins definition), so they are not S13's statements verbatim.

### 5. s15_note1.md

- Old: Lemma 2's proof ("neighbours of $q$ are pawns of the other colour two ranks further on") needs the exact content.
- New: Lemma 2's proof (files $j\pm1$ hold only an enemy pawn two ranks ahead of $q$) needs the exact content.
- Why true: Item 1. The old quotation was not S13's wording. The new parenthesis gives S13 proof.tex line 83 ('Files j+-1 hold only an enemy pawn two ranks ahead of q').

### 6. s15_note1.md

- Old: with an e.p. flag (if any) protecting a pawn of the player not to move.
- New: with an e.p. flag (if any) marking an e.p.-capturable pawn of the player not to move.
- Why true: Item 1. This matches S13's Lemma 2 hypothesis ('marking an e.p.-capturable pawn of the player not to move'), so the restated hypothesis is now S13's.

### 7. s15_note1.md

- Old: and an e.p. flag (if any) protecting a pawn of $X$, the player not to move.
- New: and an e.p. flag (if any) marking an e.p.-capturable pawn of $X$, the player not to move.
- Why true: Item 1. Same terminology at the place where 2b uses Lemma 2(a). After X's far double step the flag, if any, marks X's pawn, which can be taken e.p. (canonical flag).

### 8. s15_note1.md

- Old: Step (iii) of the proof of Lemma 3 concerns the replies of $Y$ to a far move of $X$. What it needs is the following, which is proved here in full from Lemma 2 and the view lemma V.
- New: Section S13 proves steps (i)-(iii) of Lemma 3 in full. This section gives the same local proof in the coordinates of $P_n$. Step (iii) concerns the replies of $Y$ to a far move of $X$; it is proved below from Lemma 2 and the view lemma V.
- Why true: Item 1 (T90 'at 56'). S13 now proves (i)-(iii) in full (proof.tex lines 119-139). 2b actually covers steps (i)-(iii) in P_n coordinates.

### 9. s15_note1.md

- Old: It also shows that the only role of the cut is to guarantee that $A\subset$ pattern files (the hypothesis); it is not otherwise special (H6).
- New: It also shows that, besides the numeric bounds $4\le c\le n-6$ of Lemma 3, which keep the files $c-4,\dots,c+5$ distinct, with no wrap across the seam between files $n-1$ and $0$, the only role of the cut is to guarantee that $A$ consists of consecutive pattern files of one wall (the hypothesis); it is not otherwise special (H6).
- Why true: Item 1 (T90 'at 73'). 4<=c<=n-6 gives 0<=c-4 and c+5<=n-1, so the ten files are distinct and do not wrap. 2b's partition 'files <=c-4 or >=c+5' depends on this.

### 10. s15_note1.md

- Old: (This justifies that the case analysis of Lemma 2(b) in Section S13 lists only forward steps.)
- New: (The proof of Lemma 2 in Section S13 gives the same argument before its case analysis, which therefore lists only forward steps.)
- Why true: Item 1. S13's proof of Lemma 2 (lines 83-85) itself rules out captures and e.p. captures before it lists the advances. The old text suggested that S13 needed this justification.

### 11. s15_note1.md

- Old: ($h<256$ in the model of Section S13, where a passed pawn is worth $\pm256$; the step below uses no bound)
- New: (the theorem of Section S13 holds for every $h\ge0$ and names the range $0\le h<256$ in particular; the step below uses no bound)
- Why true: Items 1 and 5 (T90 'at 91'). S13 Theorem: 'every integer h>=0 ... in particular ... 0<=h<256'. H8's own heap step proves the claim for all h, so the note claims nothing beyond what it proves.

### 12. s15_note1.md

- Old: The only repairs are precisions: the definition of "pattern file" (section 2), the explicit bound $n\ge n_0$ (H6), the no-capture remark (H3), the large-heap step and the meaning of "$=\star2$" (H8), and the written-out step (iii) (2b).
- New: What this note adds for $P_n$ are precisions: the restated definition of "pattern file" (section 2), the explicit bound $n\ge n_0$ (H6), the no-capture remark (H3), the large-heap step and the meaning of "$=\star2$" (H8), and the local proof of steps (ii)-(iii) in the coordinates of $P_n$ (2b).
- Why true: Item 1 (T90 '109-110'). The word 'repairs' implied that S13 was defective. The listed items are additions for P_n; 2b gives the local proof in P_n coordinates.

### 13. s15_note1.md

- Old: Their hand proofs are those of Section S13; H4 restates the race rule. Section 2b writes out steps (ii)-(iii) of Lemma 3 for this family.
- New: Their hand proofs are those of Section S13, which defines the model in full (including the race rule and the flag across a heap move) and proves Lemma 3 (i)-(iii) in full; H4 discusses the role of the race rule. Section 2b gives the local proof of steps (ii)-(iii) in the coordinates of $P_n$.
- Why true: Item 1 (T90 '109-110'). S13 defines the race rule (lines 29-32) and the flag under a heap move (line 26), and it proves Lemma 3 (i)-(iii). 'H4 restates the race rule' was inaccurate, because H4 discusses the rule's role.

### 14. s15_note1.md

- Old: | H4 | the race rule enters only through the passed-pawn set of a child, which $\mathrm{ins}$ preserves | PROVED |
- New: | H4 | the race rule enters only through the passed pawns of a child (colour, rank, front-pawn status) and the last mover, which $\mathrm{ins}$ preserves; so the argument holds for any race rule invariant under the file embedding and determined by these data, such as count, mover and opponent | PROVED |
- Why true: Item 4 (line 25, which the earlier pass skipped). Count uses colour, rank and front-pawn status of passed pawns plus the last mover for ties; mover and opponent use only the last mover. V3 preserves all of these.

### 15. s15_note1.md

- Old: (and under any race rule invariant under this file embedding and determined by preserved data, including the front-pawn information and last mover needed for count)
- New: (and under any race rule that is invariant under this file embedding and is determined by data the insertion preserves: the passed pawns with their colours, ranks and front-pawn status, and the last mover; count, mover and opponent are such rules)
- Why true: Item 4 (line 83, which the earlier pass had already partly fixed). The class is now named precisely, and count, mover and opponent are stated to belong to it.

### 16. s15_note1.md

- Old: The proof's lemmas are rule-independent (H4); C1' is not.
- New: The proof's lemmas hold for every race rule of the class described in H4, which contains count, mover and opponent; C1' does not.
- Why true: Item 4 (same shorthand, gaps item 4). Lemma 2 does not use the race at all. Lemma 3 holds for the H4 class. C1' depends on the rule (S6).

### 17. s15_note1.md

- Old: passes for every $c=7..n-2$ and fails only for $c=6$, which cuts the zone)
- New: passes for every $c=7..n-2$, which for $c$ outside $11..n-6$ is a test of the conclusion outside the sufficient hypotheses, and fails only for $c=6$, where file 6 lies in the zone, so the copied pair is not always a pattern pair and the map tested is the unrestricted file-copy map)
- Why true: Item 3 (line 88). For c in 7..10 or n-5..n-2 the ten-file or numeric hypothesis fails, but the copied pair lies in 7..n-1 and is a pattern pair. File 6 is in Z_0={0,2,..,6}, so the pair (6,7) is not a pattern pair in every node.

### 18. s15_note1.md

- Old: and with the arc requirement dropped it finds 774 and 422 mismatches at $c=5,6$ ($n=18$), so the test can fail.
- New: and at the cuts $c=5,6$ ($n=18$), where the copied pair is not always a pattern pair (file 5 is a core file, file 6 lies in the zone) and the map is the unrestricted file-copy map, it finds 774 and 422 mismatches, so the test can fail.
- Why true: Item 3 (line 101). File 5 holds W3B6 (core). File 6 is in the zone. The numbers 774 and 422 are unchanged.

### 19. s15_note1.md

- Old: arcs of 2 and 4 files fail (897 and 99 mismatches), arcs of 6 files and longer pass, so radius 5 is conservative.
- New: with arcs of 2 and 4 files, a test of the conclusion outside the sufficient hypotheses, the tested correspondence fails (897 and 99 mismatches); arcs of 6 files and longer pass, so radius 5 is conservative.
- Why true: Item 3 (line 101). In D's sensitivity harness (verify_logic/audit4b_sensitivity.py) the cut is in the middle of the short arc, so the copied pair stays a pattern pair and only the ten-file hypothesis fails.

### 20. s15_note1.md

- Old: with the arc shortened by 3 files the same test finds a mismatch (1 of 42 accepted).
- New: with the arc shortened by 3 files, a test of the conclusion outside the sufficient hypotheses, the same test finds a mismatch (1 of 42 accepted).
- Why true: Item 3 (line 101). C's radius_shrink (check3/lem.py) damages files c-4..c-2 and c+3..c+5, so c and c+1 stay pattern files and only the ten-file hypothesis fails.

### 21. s15_note1.md

- Old: and for every cut $c=7..n-2$ (fails only for $c=6$).
- New: and for every cut $c=7..n-2$ (for $c$ outside $11..n-6$ a test of the conclusion outside the sufficient hypotheses); at $c=6$, where the copied pair is not always a pattern pair and the map is the unrestricted file-copy map, the tested correspondence fails.
- Why true: Item 3 (line 119). Same classification as line 88.

### 22. s15_note2.md

- Old: **PROVED**: Lemmas 1–2 and the statement of Lemma 3 in Section S13; the proof of Lemma 3 (ii)–(iii) is written out in Note 1 of Section S15, §2b. |
- New: **PROVED**: Lemmas 1–3 and their proofs, including steps (i)–(iii) of the proof of Lemma 3, in Section S13; steps (ii)–(iii) are also written out, in the coordinates of $P_n$, in Note 1 of Section S15, §2b. |
- Why true: Item 2. S13 now contains the full proof of Lemma 3 (i)-(iii), and Note 1 section 2b writes out the same local proof for P_n.

### 23. s14_ringn.md

- Old: At $O_{19}$ the five additional controls $c=6$ through $10$ all had zero mismatches. No failing $O$ control was recorded in that sweep.
- New: At $O_{19}$ five additional cuts all had zero mismatches: $c=6$ through $9$, where the copied pair is a pattern pair but the ten-file interval leaves the wall (a test of the conclusion outside the sufficient hypotheses), and $c=10$, where file 11 lies beyond the designated wall, so the map is the unrestricted file-copy map. No mismatch at an $O$ cut was recorded in that sweep.
- Why true: Item 3 (S14 line 48). The O19 wall is files 1..10, which are pattern files in every node (C1O). For c=6..9 the pair lies in 1..10 but c+5>=11. For c=10 the copied file 11=n-8 is core (B7).

### 24. s14_ringn.md

- Old: control fails at $c=9$ (600 of 882).
- New: at the control cut $c=9$, where file 10 lies beyond the wall, so the map is the unrestricted file-copy map, the tested correspondence fails (600 of 882).
- Why true: Item 3 (S14 line 70). The M18 wall is files 0..9 (n-9=9). The copied file 10=n-8 is B6 (core). The numbers are unchanged.

### 25. s14_ringn.md

- Old: the five further controls $c=6..10$ at $O_{19}$ all had 0 mismatches (the proof uses $c=5$); no failing $O$ control was recorded.
- New: the five further cuts $c=6..10$ at $O_{19}$ (for $c\le9$ tests of the conclusion outside the sufficient hypotheses, for $c=10$ the unrestricted file-copy map) all had 0 mismatches (the proof uses $c=5$); no mismatch at an $O$ cut was recorded.
- Why true: Item 3 (S14 line 71). Same classification as S14 line 48.

### 26. s14_ringn.md

- Old: $G\equiv\star2$ means that for every heap $\star h$, $h<256$ (a passed pawn is worth $\pm256$), $G+\star h$ and $\star2+\star h$ have the same outcome: P for $h=2$ and N otherwise.
- New: $G\equiv\star2$ means that for every heap $\star h$ with $h<256$ (the range named in the theorem of Section S13, which itself holds for every $h\ge0$; a resolved position is scored $\pm256$), $G+\star h$ and $\star2+\star h$ have the same outcome: P for $h=2$ and N otherwise; the argument below uses no bound on $h$.
- Why true: Item 5 (S14 H7). S13's theorem holds for all h>=0 and names 0<=h<256. The H7 step (heap move to G+*2 for h>=5) and the signed-integer argument use no bound. The note's own theorem statement (line 4) is unchanged.

### 27. s15_note3.md

- Old: so it is sufficient, not necessary: the computation shows that
- New: so it is sufficient, not necessary: in a test of the conclusion outside the sufficient hypotheses, the computation shows that
- Why true: Item 3 (Note 3 line 42). Cuts c=2..n-9 copy a pair inside the pattern files 2..n-8, while the ten-file arc or 4<=c fails, so the hypotheses fail but the map is the restricted one.

### 28. s15_note3.md

- Old: Control: for the cuts $c=7..10$ Lemma 3's conclusion still holds on the nodes of $n=19$ although the arc meets the zone (radius 5 is conservative), for $c=11$ (arc $7..16$) it fails at 48 of 858 ($R$) and 150 of 2574 ($Qo$) (node, side) pairs, so the test can fail.
- New: Control: for the cuts $c=7..10$ the copied pair is a pattern pair but the arc meets the zone; in this test of the conclusion outside the sufficient hypotheses the conclusion of Lemma 3 still holds on the nodes of $n=19$ (radius 5 is conservative). For $c=11$ (arc $7..16$) the copied file 12 lies in the zone, so the map is the unrestricted file-copy map, and the tested correspondence fails at 48 of 858 ($R$) and 150 of 2574 ($Qo$) (node, side) pairs, so the test can fail.
- Why true: Item 3 (Note 3 line 64). At n=19 the pattern files are 2..11. For c=7..10 the pair lies in 2..11 and the arc meets Z={12..}. For c=11 the copied file 12 is in the zone.

### 29. s15_note3.md

- Old: gives 0 mismatches at $c=5,7,9$ (the radius-5 hypothesis is conservative) and mismatches at $c=10$ (208 of 1500), $c=11$ (233) and $c=12$ (1311), so the test fails when the hypothesis fails (a rerun
- New: gives 0 mismatches at $c=5,7,9$ (tests of the conclusion outside the sufficient hypotheses; the radius-5 hypothesis is conservative) and mismatches at $c=10$ (208 of 1500), $c=11$ (233) and $c=12$ (1311). At $c=10$ the ten-file hypothesis fails; at $c=11,12$ the copied pair can contain a randomized file, so the map is the unrestricted file-copy map. The tested correspondence fails at these control cuts (a rerun
- Why true: Item 3 (Note 3 line 64, random test). The outside content of arc 2..11 is randomized. For c=5,7,9,10 the pair lies in 2..11 but the arc reaches randomized files. For c=11,12 the pair includes file 12 or 13, which can be randomized.

### 30. s15_note3.md

- Old: (the tested correspondence fails at this control cut only at $c=11$)
- New: (the tested correspondence fails only at the control cut $c=11$, where the map is the unrestricted file-copy map)
- Why true: Item 3 (Note 3 line 78). This repairs the garbled earlier wording, and c=11 is the unrestricted map (file 12 is in the zone).

### 31. s15_note3.md

- Old: so any race rule invariant under this file embedding and determined by preserved data, including the front-pawn information and last mover needed for count, gives the same class (Note 1 of Section S15, H4).
- New: so any race rule that is invariant under this file embedding and is determined by data the insertion preserves (the passed pawns with their colours, ranks and front-pawn status, and the last mover) gives the same class (Note 1 of Section S15, H4); count, mover and opponent are such rules.
- Why true: Item 4 (Note 3 line 53). This is the precise class, with count, mover and opponent named as members.

### 32. s15_note3.md

- Old: $G=\star k$ means that for every heap $\star h$, $h<256$ (a passed pawn is worth $\pm256$), $G+\star h$ and $\star k+\star h$ have the same outcome, namely P for $h=k$ and N otherwise.
- New: $G=\star k$ means that for every heap $\star h$ with $h<256$ (the range named in the theorem of Section S13, which itself holds for every $h\ge0$; a resolved position is scored $\pm256$), $G+\star h$ and $\star k+\star h$ have the same outcome, namely P for $h=k$ and N otherwise; the heap steps below use no bound on $h$.
- Why true: Item 5 (Note 3 H7). The heap steps 'h>=3' and 'h>=4' use no bound. S13's range is attributed correctly.

### 33. s15_note4.md

- Old: The ranges are sufficient, not necessary: E's control cuts give exact insertion for $c=5..8$ ($T$, $n=20$) and $c=8..11$ ($S$, $n=23$), first failure at $c=9$ ($T$) and $c=12$ ($S$).
- New: The ranges are sufficient, not necessary: E's control cuts $c=5..8$ ($T$, $n=20$) and $c=8..11$ ($S$, $n=23$), tests of the conclusion outside the sufficient hypotheses, give exact insertion. At $c=9$ ($T$) and $c=12$ ($S$) the copied pair is not always a pattern pair (file 10 of $T_{20}$ is a core file; file 13 of $S_{23}$ lies in the zone), so the map is the unrestricted file-copy map, and the tested correspondence first fails at these control cuts.
- Why true: Item 3 (Note 4 line 46). The T20 wall is files 0..9; file 10=n-10 is B5 (core). The S23 fixed run is 3..12; file 13=n-10 is in the zone {0,1,2,13,14,16..22}. For c=5..8 (T) and c=8..11 (S) the pair is pattern but the arc leaves the run.

### 34. s15_note4.md

- Old: control fails first at $c=9$ (1328 of 2610).
- New: the tested correspondence first fails at the control cut $c=9$ (1328 of 2610), where the copied file 10 is a core file, so the map is the unrestricted file-copy map.
- Why true: Item 3 (Note 4 line 70). As above. 1328 of 2610 is unchanged.

### 35. s15_note4.md

- Old: control fails first at $c=12$.
- New: the tested correspondence first fails at the control cut $c=12$, where the copied file 13 lies in the zone, so the map is the unrestricted file-copy map.
- Why true: Item 3 (Note 4 line 71). As above.

### 36. s15_note4.md

- Old: $G\equiv\star3$ means that for every heap $\star h$, $h<256$ (a passed pawn is worth $\pm256$), $G+\star h$ and $\star3+\star h$ have the same outcome: P for $h=3$ and N otherwise. C1 gives signature NNNPNN for $h=0..5$; for $6\le h<256$, the heap move to the P-position $G+\star3$ gives N.
- New: $G\equiv\star3$ means that for every heap $\star h$ with $h<256$ (the range named in the theorem of Section S13, which itself holds for every $h\ge0$; a resolved position is scored $\pm256$), $G+\star h$ and $\star3+\star h$ have the same outcome: P for $h=3$ and N otherwise. C1 gives signature NNNPNN for $h=0..5$; for $6\le h<256$, the heap move to the P-position $G+\star3$ gives N (this step uses no bound on $h$).
- Why true: Item 5 (Note 4 H7). The theorem's stated range h<256 is kept. The note only adds that the step uses no bound, which is true (heap move to G+*3).

### 37. s15_note1.md

- Old: a sensitivity control (arcs of 2 and 4 files) fails as it should.
- New: a sensitivity control with arcs of 2 and 4 files, a test of the conclusion outside the sufficient hypotheses, finds mismatches, as expected.
- Why true: Item 3 (Note 1 line 117, same kind as 88/101/119). D's short-arc control is outside the sufficient hypotheses (see line 101).

### 38. s15_note3.md

- Old: the control fails at $c=10,11,12$ and passes at $c=5,7,9$.
- New: the tested correspondence fails at the control cuts $c=10,11,12$ (at $c=10$ outside the sufficient hypotheses, at $c=11,12$ the unrestricted file-copy map) and holds at $c=5,7,9$.
- Why true: Item 3 (Note 3 line 81, same D random test as line 64). This uses the same classification.

## Item 6: other sentences that contradict, or sit badly with, the current proof.tex (not fixed)

1. s15_note3.md line 5: "with the repaired \"pattern file\"". This implies that S13's pattern-file definition was defective; proof.tex now defines it exactly (lines 52-53). Suggested wording: "with the exact-content \"pattern file\"".
2. s15_note2.md line 31: "The terminal score convention is +-256, so heaps considered in the value statement have h<256." It is not attributed to S13, but the "so" presents the bound as forced. S13's theorem and the note's own H8 step hold for every h>=0. T90 says the narrower heap conclusions may stand.
3. The H7 parentheses of S14 and Notes 3-4, as printed before this pass, and Note 1 H8 ("where a passed pawn is worth +-256"): S13's Model paragraph does not mention +-256. The +-256 scoring is in S13's "Scope and ordinary game value" paragraph. The brief says "the model says a passed pawn is worth +-256", so I wrote "the range named in the theorem of Section S13" rather than "stated in the model". The sentences I wrote say "a resolved position is scored +-256", which matches proof.tex line 179.
4. s14_ringn.md line 52: S13 defines walls only of types W3/B5 and W2/B4. S14 applies the lemmas to a B7/W5 wall by colour reversal (T90 accepted this). The sentence is not wrong, but the lemmas of S13 are not literally stated for that wall.
5. s15_note1.md lines 61 and 83 and s15_note3.md: "e.p. protection" (V3, H4) is the note's own term for flag status, which S13 calls "flag status". This is not a contradiction. I changed only the Lemma 2 hypothesis and its use at line 67 to S13's "marking an e.p.-capturable pawn".
6. s15_note1.md line 10, s14 line 81, s15_note3.md lines 74 and 81-85, and s15_note4.md line 81 describe referees and reviews. They are pre-existing and do not contradict the mathematics; I left them alone, following the rule on the text I write.
7. s15_note3.md line 83 ("control: 0 failures at c=7..10, 48 of 858 ... at c=11"). This is the same kind of control sentence as line 64. It does not suggest that Lemma 3 fails, so I left it unchanged. The same holds for s15_note1.md line 99 "(also c=11)", which is a cut within the hypotheses.
No other sentence in the five files contradicts proof.tex as far as I could find. Lemma statements, the window choices, the ranges of the far and near files in 2b, the race rule and the flag-under-heap-move convention all agree with it.

