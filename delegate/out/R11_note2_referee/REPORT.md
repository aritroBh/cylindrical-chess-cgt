SOUND WITH FIXES

# R11 referee report: Note 2 of Section S15 (`dist/tog/supp_src/s15_note2.md`), the even Q family is *3

Line numbers refer to `dist/tog/supp_src/s15_note2.md` (58 lines). The working original
`research/ring_n_plus_2_proof/PROOF_Q.md` differs only in labels, file references and a removed
referee/reproduction section. The mathematics is the same in both.

Summary. I found no gap in the mathematics. The family is well defined. Every hypothesis of Lemmas 1-3
holds at every node the induction uses. The insertion step gives an isomorphism of reduced games with
T-flags for each side. No width is skipped. The step from N N N P (h = 0..3) to all heaps is right.
My own engine, written from the rules, reproduces every finite number the proof uses:
- R_22: 7,968 nodes, 21,063 K-edges, 17,784 T-edges, no flags, no passers, zone Z_22, reduced signature NNNPN.
- ins_9 maps R_n onto R_{n+2} for n = 18..24.
- Whole-board signatures are NNNPN for n = 8..16 in both heap/e.p. readings.

All the findings are MINOR:
- one misplaced window in H2;
- a wrong reason for the base width in H6;
- a pattern-file definition that drops the word "wall";
- a table row that credits Note 1's text to Section S13;
- an overstatement of how independent the programs are;
- a claim about F's runs that F's saved log does not show;
- an H8 that claims less than is proved.

There is no BLOCKER and no MAJOR finding.

## 1. Line-by-line refereeing

### Family and notation (lines 33-35)
- `s15_note2.md:34` CORRECT. The count is 2 + (n-8) + 6 = n files and 1+1+(n-8)+2+1+2+1+1+1 = n+2 pawns.
  Files are numbered from 0, and file n-1 is adjacent to file 0:
  - file 0 = W4, file 1 = B7;
  - files 2..n-7 = B4,W2,...,B4,W2 (B4 on even files, W2 on odd files);
  - n-6 = W3B6, n-5 = W3, n-4 = W2B5, n-3 = B5, n-2 = W2, n-1 = B4.

  H1, H5 and H6 use this reading, and I computed with it. It reproduces every number.
- `s15_note2.md:34` MINOR (presentation). The note never states how files are numbered, but H1-H7 use
  file indices. Replacement, after the display: "listed as files $0,1,\dots,n-1$ of $C_n$ (file $n-1$ is
  adjacent to file 0); $Wr$/$Br$ is a white/black pawn on rank $r$, and $W3B6$ is a file holding both."
- `s15_note2.md:35` MINOR. "A pattern file is a file whose content is exactly its starting pawn" leaves out
  "wall". As worded, files 0 (W4), n-3 (B5) and n-2 (W2) are pattern files too. Lemma 2 also speaks of a
  "wall pawn", which Note 2 never defines. No use in the proof is affected, because every use is on files
  4..16. Replacement: "A **pattern file** is a wall file (H1) whose content is exactly its starting pawn and
  nothing else; a **wall pawn** is the pawn of a pattern file."

### Model and lemmas (lines 29-39)
- `s15_note2.md:31` CORRECT, with one MINOR omission. The line does not repeat two things from Section S13
  and Section II: the e.p.-flag convention (a flag is recorded only if an enemy pawn stands beside the
  landing square) and how the race rule counts distance. "No flag" in C1 means that flag convention.
  Replacement for the third sentence: "Race rule is `count` (promotion distance counted as on an empty
  board, a double step counting as one move); en passant is on, an e.p. flag is recorded only if an enemy
  pawn stands beside the landing square, and an e.p.-capturable pawn is not passed."
- `s15_note2.md:37` CORRECT. I rechecked Lemma 2 for the Q phase by hand, with pattern files j-1..j+3:
  - A W2 on j that advances to (j,3) is taken directly by the B4 on j+1. One that advances to (j,4) is
    taken e.p. by the same B4.
  - A B4 on j that advances to (j,3) is taken by the W2 on j+1.
  - The capturer then stands on file j with no X pawn on j-1, j or j+1. It did not double-step, so it
    cannot be taken e.p., and it is passed.
  - The only X pawn whose three-file view changed is on j+2. The Y pawn on j+3 still blocks it.
  - After the wall move itself X has no passer (Lemma 2(a)). After 2->3 or 4->3 the pawn is still blocked.
    After 2->4 it stands beside a B4 and can be taken e.p.
  - The mirror window is symmetric, and the proof does not use the phase.

  Remark: the Q phase (W2 on odd files) is the phase of Section S13's own E_n. So the lemma is used here
  exactly as printed in S13. "Opposite phase from P" is true but not the relevant comparison.
- `s15_note2.md:39` CORRECT. In p, c-3..c+4 = 6..13 and the arc c-4..c+5 = 5..14. After insertion,
  c-3..c+6 = 6..15 lies inside c-4..c+7 = 5..16. Steps (ii)-(iii) of Note 1 §2b handle the far moves of the
  pattern pawns on files 5 and 14, which are not central. I re-read those steps, and they hold here:
  - every far move touches only files <= 6 or >= 13;
  - files 7..12 stay pattern files;
  - the e.p. replies to a 2->4 on file 5 or file 13 are far replies.

### H1-H8 (lines 41-50)
- H1 `s15_note2.md:43` CORRECT. The wall is files 2..n-7, with B4 on even and W2 on odd files and the black
  pawn two ranks above the white. My zone computation confirms that files 4..14 are fixed in every node of
  R_22. File 20 = n-2 is fixed too.
- H2 `s15_note2.md:44` MINOR (wrong window, harmless).
  - Lemma 3 (Note 1 §2b (i)) applies Lemma 2(b) to the central files c-3..c+4 = 6..13. So the left end case
    is q on file 6 with window 5..9, not q on file 5 with window 4..8.
  - File 5 is a far file (c-4) and needs no Lemma 2(b).
  - The first sentence of H2 contradicts its own last sentence ("only on central files 6..13").
  - The computation behind H2 is fine. E's log checks files 5..13 on all 7,968 nodes, and every move on
    file 6 is P (7,968 of them). Nothing is missing; only the text is off by one.

  Replacement for the second and third sentences: "Lemma 3 at $c=9$ applies Lemma 2(b) to the central files
  $6..13$; the extreme windows are $5..9$ (q on file 6, window $j-1..j+3$) and $10..14$ (q on file 13,
  window $j-3..j+1$), both inside the pattern arc. On all actual $R_{22}$ nodes E checked every move of a
  wall pawn on files $5..13$ (C1); file 5 lies outside the central range and is listed only as an extra
  check."
- H3 `s15_note2.md:45` CORRECT. Between pattern neighbours, the rank-3 capture squares of a W2 and of a B4
  are empty. A B4 cannot take an unmoved W2 e.p., and a W2 on rank 2 has no e.p. capture at all.
- H4 `s15_note2.md:46` CORRECT. By V3 of Note 1 §2b, both positions have the same passers, ranks, e.p.
  protection and mover.
- H5 `s15_note2.md:47` CORRECT. I checked every root pawn by hand:
  - W4(0) is blocked by B7(1). The B4 on n-1 stands level with it, not ahead.
  - B7(1) is blocked by W4(0), and B4(2) by W2(3).
  - Each wall W2 is blocked by a neighbouring B4. W2(n-7) is also blocked by B6(n-6).
  - W3(n-6) is blocked by B6(n-6). B6(n-6) is blocked by W2(n-7), W3(n-6) and W3(n-5).
  - W3(n-5) is blocked by B6(n-6) and B5(n-4).
  - W2(n-4) is blocked by B5(n-4). B5(n-4) is blocked by W3(n-5) and W2(n-4).
  - B5(n-3) is blocked by W2(n-4) and W2(n-2). W2(n-2) is blocked by B5(n-3) and B4(n-1).
  - B4(n-1) is blocked by W2(n-2).
  - There is no flag.

  ins_9 inserts the contents of file 10 (B4) and file 9 (W2) after file 9, which extends the alternating
  block. So ins_9(start_n) = start_{n+2}. File 9 is W2 and file 10 is B4 already for n >= 18. My pump check
  confirms this for n = 18..24.
- H6 `s15_note2.md:48` CORRECT WITH A FIX (the reason given for the base width).
  - The stated bound, "the first even n for which c+5 = 14 <= n-7", ignores that file n-7 is in the zone
    Z_n. It also does not say why the arc cannot start further left.
  - The correct reason: the arc of ten pattern files must avoid Z_n, so it lies in 4..n-8. That needs
    n-8 >= 13, and the first even such n is 22.
  - c = 9 (arc 5..14) is one admissible cut; c = 8 (arc 4..13) is another. The number 22 does not change.

  Replacement for the last sentence: "The arc $c-4..c+5$ must avoid $Z_n$, i.e. lie in $4..n-8$; this needs
  $n\ge21$, so $n_0=22$ is the first even width, and $c=9$ (arc $5..14$) is admissible there. (The reduced
  graph already has 7,968 nodes and the shifted zone at $n=18,20$, but those widths are covered by C2, not
  by the induction.)"
- H7 `s15_note2.md:49` CORRECT.
  - ins_9 fixes the files <= 9 and sends each file f >= 10 to f+2. So
    ins_9(Z_n) = {0,1,2,3} u {n-5..n-1} u {n+1} = Z_{n+2}.
  - For n >= 22, Z_n does not meet 4..14, so Lemma 3 at c = 9 applies at every node.
  - ins_9 is injective. Induction on the distance from the root then shows that the nodes, the K-edges per
    side and the T-flags per side of R_{n+2} are the images of those of R_n.
  - Which side has a T-move is preserved, because Lemma 3 is stated for each side separately.
  - "No passer" is automatic, because K-children are non-terminal.

  MINOR: start H7 with "Let $n\ge22$ be even".
- H8 `s15_note2.md:50` CORRECT, MINOR (it claims less than is proved).
  - Nothing about heaps larger than 3 is missing. For h > 3, the heap move to Q_n + *3 wins: that sum is
    a P-position, and the root has no flag. *3 + *h is also N. For h = 0, 1, 2 the outcome is computed as
    N. So the outcomes agree for every h < 256.
  - "It does not claim equivalence against arbitrary addends" is weaker than what is proved. It is also
    weaker than the paper's "=" (Section II: G = H iff G - H is a second-player win).
  - Since -*3 = *3, "Q_n + *3 is P" already means Q_n = *3 as a game in the model, with terminal positions
    as the numbers +-256. This holds in the heap-sum reading `keep` (flags survive heap moves, which is the
    true disjunctive sum). F and my program both ran that reading.

  Replacement for the second sentence: "Since $-\star3=\star3$, P at $h=3$ in the reading `keep` (the
  disjunctive sum) is already $Q_n-\star3=0$, i.e. $Q_n=\star3$ as a game of the model; the outcomes for
  $h=0,1,2$ are a consequence and are also computed." If the authors prefer to keep the weaker claim, they
  should drop "Not claimed: equivalence against arbitrary addends" from line 12. That phrase suggests the
  paper's "whole-board *3" means less than CGT equality.

### Theorem (line 58)
- `s15_note2.md:58` CORRECT.
  - n >= 22 follows from H7, C1 and Lemma 1.
  - n = 8, 10, 12, 14, 16, 18, 20 (seven widths) follow from C2. C2 covers 8..24 (nine widths), so 22 and
    24 are covered twice.
  - No even width >= 8 is skipped.
  - n = 8 is the member with an empty block: W4 B7 W3B6 W3 W2B5 B5 W2 B4, with 10 pawns.

### Section 0 table and summary
- `s15_note2.md:20` MINOR (label). The row says "the insertion detail in Note 1 of Section S15, §2b" is
  "PROVED in Section S13". §2b is new text, proved in Note 1, not in S13. Replacement for the status cell:
  "**PROVED**: Lemmas 1-2 and the statement of Lemma 3 in Section S13; the proof of Lemma 3 (ii)-(iii) is
  written out in Note 1 of Section S15, §2b."
- `s15_note2.md:21`, `:58` MINOR. "Conditional on ... the lemmas of Section S13" should also name Note 1
  §2b, because that is the proof of Lemma 3 the note relies on. Replacement in line 58: "(PROVED,
  conditional on C1-C2, Lemmas 1-3 of Section S13 and the proof of Lemma 3 in Note 1 of Section S15, §2b)".

## 2. Finite facts

| Fact used | Label in note | Programs the note cites | Honest? | My recomputation |
|---|---|---|---|---|
| C1: R_22 has 7,968 nodes, 21,063 K-edges, 17,784 T-edges, no flags, zone Z_22 = {0,1,2,3,15..19,21}, reduced signature NNNPN (h=0..4) | CHECKED-2 | A (`rg.c` pump log) and E | Yes. A's saved pump log and E's saved log both show these numbers. | **Agrees exactly** on all six numbers; no node has a passer. |
| C1 part: Lemma 2(a),(b) on every R_22 node: 71,712 q/node positions, 111,552 moves, 0 failures; file 5: 5,691 L / 10,245 P; file 13: 414 L / 15,522 P | COMPUTED-1 (E) | E | Yes. The arithmetic checks: 71,712 = 7,968 x 9 (files 5..13); 111,552 = 7,968 x 14 (five W2 files x 2 moves + four B4 files x 1 move); 5,691+10,245 = 414+15,522 = 15,936 = 2 x 7,968. | Not recomputed separately. My pump check below makes it redundant for the induction. |
| C2: whole-board NNNP, h=0..3, even n=8..24 | CHECKED-2 | A (unreduced search) and F | Yes for h=0..3. A's saved log has 27 lines NNNP (n=8..60). F's saved log has NNNPN for n=8..22 in both readings, and for n=24 in `expire`. | **Agrees** for n=8..16, both readings, h=0..4. |
| F: h=4 and both readings for all nine sizes; P_8 control NNPNN | COMPUTED-1 | F | **Partly unsupported.** F's saved log (`research/ring_n_plus_2_check/q/independent.log`) ends after n=24 `expire`. It has no n=24 `keep` line and no P_8 control line, although `independent.py` prints both. | Not recomputed; I did not run P_8. |
| Pump beyond 22 | one program, "not used" | A | Yes | ins_9(R_n) = R_{n+2} holds for n = 18->20->22->24->26: root, node sets, K-edges, and T-counts per side. |

Findings on labels:
- `s15_note2.md:56` MINOR. F's saved log stops after n=24 `expire`. It does not show the claim
  "F additionally computes h=4 and both e.p.-across-heap readings: NNNPN for each of those nine sizes. The
  control P_8 is NNPNN in both readings". Either rerun F to completion and keep the log, or replace the
  claim with: "F computes $h=4$ in both readings for $n=8..22$ and in the reading `expire` for $n=24$:
  NNNPN each time." Then drop the P_8 sentence, or cite where its output is. The theorem uses none of this.
- `s15_note2.md:16` MINOR. "The programs share the written rules, not implementation code" is not true of
  F, which imports `cylcgt.pawns.passed` (line 27 says so). CHECKED-2 still stands, because no two of the
  cited programs share code: A is in C, and E does not import `cylcgt`. Replacement: "The programs share the
  written rules; A and E share no code with any other program, and F imports only the passed-pawn predicate
  of `cylcgt`."
- `s15_note2.md:8` MINOR. "An independent full-game run also checks h=4 and Lemma 2(b) on every Q_22 node"
  merges two programs: F did h=4 and E did Lemma 2(b). Replacement: "COMPUTED-1: F also checks $h=4$; E
  checks Lemma 2(a),(b) on every $R_{22}$ node."
- `s15_note2.md:22-23` MINOR. The paths `verify_compute/myeng.py` and `q/check_wall_q22.py` are relative to
  two different folders (`research/ring_n_plus_2_proof/` and `research/ring_n_plus_2_check/`) and are not
  in the supplement. Give full repository paths or the GitHub link.

### What I recomputed (my own code, no repository code imported)
The engine is `delegate/out/R11_note2_referee/qref.py`. I wrote it only from Section II and the Model
paragraph of S13. It implements:
- move generation with double steps, captures across the seam, and e.p., with a flag recorded only beside
  an enemy pawn;
- the e.p.-aware passed test;
- race rule `count`, with a tie going to the side that did not move;
- normal play in G + *h;
- heap moves with flags kept (`keep`) or cleared (`expire`).

Reduced graphs (Lemma 1 classes T/L/P/K computed from scratch):

| n | nodes | K-edges | T-edges | flagged | nodes with a passer | zone | reduced sig h=0..4 |
|---|---|---|---|---|---|---|---|
| 8 | 1,894 | 4,250 | 3,430 | 0 | 0 | 0,1,2,3,4,5,7 | NNNPN |
| 10 | 7,141 | 18,937 | 16,650 | 0 | 0 | 0..7, 9 | NNNPN |
| 12 | 8,556 | 22,631 | 21,190 | 0 | 0 | 0..9, 11 | NNNPN |
| 18 | 7,968 | 21,063 | 17,784 | 0 | 0 | 0,1,2,3,11..15,17 | NNNPN |
| 22 | 7,968 | 21,063 | 17,784 | 0 | 0 | 0,1,2,3,15..19,21 | NNNPN |

At every width I ran, these are identical to A's saved pump log
(`research/ring_n_plus_2_proof/logs/pump_Q_8_60.txt`). At n=22 they are also identical to the note's C1.

Insertion: for each side and for n = 18, 20, 22, 24 (four steps, all true):
- ins_9(start_n) = start_{n+2};
- ins_9 maps the nodes of R_n onto the nodes of R_{n+2};
- it maps K-children onto K-children and T-counts onto T-counts.

Whole-board search, signature for h = 0..4. There is no pruning by classes; the search stops at the first
winning move.

| n | `keep` | `expire` | states |
|---|---|---|---|
| 8 | NNNPN | NNNPN | 35,507 |
| 10 | NNNPN | NNNPN | 153,839 |
| 12 | NNNPN | NNNPN | 535,713 |
| 14 | NNNPN | NNNPN | 1,783,228 |
| 16 | NNNPN | NNNPN | 4,333,982 |

All of these agree with C2. The state counts differ from F's because the search stops in a different
order; the note does not claim them. So C2 for n = 8..16 and C1 at n = 22 each now have a third
independent program.

Rerun from the repository root. It takes about 14 minutes in total, with peak memory about 0.9 GB:
```sh
cd delegate/out/R11_note2_referee
nice -n 15 python3 -I qref.py reduced 8 10 12 18 22
nice -n 15 python3 -I qref.py pump 18 26
nice -n 15 python3 -I qref.py full 8 10 12 14 16
```
Outputs: `run_reduced_small.log`, `run_reduced22.log`, `run_pump.log`, `run_full.log` in this folder.

## 3. Consistency with the paper
`dist/tog/sections/08_star2.tex`, lines 124-125, says: "Wall insertion gives a whole-board *3 with n+2
pawns on every C_n with even n >= 8 [and odd n >= 11] (S)". The even part matches Note 2 exactly:
- the same game: whole-board, count, e.p. on, e.p.-aware test;
- the same pawn count, n+2;
- the same range, even n >= 8.

Q_n is a ring (every file is occupied), as the surrounding paragraph requires. Two nuances, both MINOR:
- For n = 8..20 the result is a finite computation (C2, CHECKED-2), not wall insertion. "Wall insertion
  gives" covers only n >= 22. S13 uses the same convention (C2 for n < n_0), so the label S matches the
  rest of the paper. A precise sentence would be: "Wall insertion, with a direct check of the widths below
  its base, gives ...".
- The paper's "=" is CGT equality, while Note 2 line 12 disclaims equivalence against arbitrary addends.
  As explained under H8, the computed P at h = 3 (reading `keep`) already gives CGT equality. So the
  paper's statement is covered, but the note's disclaimer should go.

## 4. Presentation problems a human referee would notice
- `s15_note2.md:10` MINOR. The paragraph on AI drafting and AI refereeing is honest, and it is fine to keep,
  though long for a supplement. It says the referee "recomputed ... C2 for h=0..4 in both e.p. heap
  readings", but the saved log shows that only up to n=22 (see section 2).
- `s15_note2.md:27` MINOR. Program B is introduced only to say that it is not evidence. This can be cut.
- `s15_note2.md:37` and `:56` MINOR. "Phase from P" and "control $P_8$" refer to Note 1's family without
  saying so. Replacement: "the family $P_n$ of Note 1 of Section S15".
- `s15_note2.md:44`: the H2 window is off by one (see section 1).
- `s15_note2.md:48`: the reason H6 gives for n_0 (see section 1).
- `s15_note2.md:35`: the pattern-file definition drops "wall" (see section 1).
- `s15_note2.md:20`: §2b is credited to S13 (see section 1).
- `s15_note2.md:5`: "PROVED, conditional on finite checks" is accurate, and the theorem on line 58 says
  the same.

## What I did not check
- I did not re-prove Lemma 1 or Lemma 3 from scratch. I re-read their proofs (S13 and Note 1 §2b) and
  confirmed that each step applies to Q. My pump check confirms the conclusion of Lemma 3 on the actual
  nodes for four steps. That is evidence for the general step, not proof.
- I did not run the whole-board search for n = 18..24, to stay within budget. Those widths rest on A and F;
  n >= 22 also rests on the induction.
- I did not recompute E's Lemma 2 counts per file, the P_8 control, or the odd family (Note 3).
- I did not read the source code of A, E or F. I compared only their saved outputs with mine.
- My engine and the others share the written rules, so a misreading common to all of them would not be
  caught.
