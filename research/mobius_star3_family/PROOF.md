# TT and SS are $\star3$ on the Möbius strip with $n+1$ pawns for every $n\ge11$: the Note 5 insertion proof, with the arc at the seam

**Summary**

1. **Theorem.** In the whole-board pawn game on the Möbius strip $M_n$ with the rules of Note 5 (section 1 there: e.p. on, an e.p.-capturable pawn is not passed, the game ends at the first passed pawn, race rule "count" with ties against the mover):
   - $TT(m)=B5\,W2\,W6B7\,W3\,B7\,B6\,W3\,W2\,B6\,W2\,(B4\,W2)^m$ ($n=2m+10$, $n+1$ pawns) is $\star3$ for every $m\ge1$;
   - $SS(m)=B6\,W3\,(W2\,B4)^m\,W6B7\,W3\,B7\,B6\,W3\,W2\,B6\,W2\,B4$ ($n=2m+11$, $n+1$ pawns) is $\star3$ for every $m\ge0$.

   Here "$G$ is $\star3$" means: $G+\star h$ and $\star3+\star h$ have the same outcome for every nim-heap $\star h$ (P for $h=3$, N otherwise). Together the families give a $\star3$ ring with $n+1$ pawns on $M_n$ for every even $n\ge12$ (TT) and every odd $n\ge11$ (SS).
2. **Method.** The insertion proof of Note 5 (Section S15), with its statement V and Lemmas 1, 2, 3 cited, not re-proved. Both walls are type E walls of Note 5 (single pawns alternating $W2$/$B4$); no colour reversal $\kappa$ is used. Cuts and bases: TT $c=14$, arc $10..19$, $m_0=5$ ($n=20$); SS $c=6$, arc $2..11$, $m_0=6$ ($n=23$). Smaller $m$ by direct search.
3. **The seam.** At the TT base the arc ends at the seam file $19=n-1$, and the file across the seam, file 0, is in the zone (it changes in 435 of 1305 nodes). This is the mirror image of the endpoint case $c-4=0$ of Note 5, which its Lemma 3 already covers ($4\le c\le n-6$ with equality). Nothing in V or Lemmas 2, 3 uses the contents of a file outside the arc, so file 0 changing does no harm (section 2).
4. Status: **PROVED** for $m\ge m_0$ given C1, and for smaller $m$ by C2 (CHECKED-2). C1 is CHECKED-2.

## 0. Result and labels

PROVED = hand proof complete, given the cited lemmas and the named finite facts. COMPUTED-1 = one program. CHECKED-$k$ = $k$ independently written programs agree. Programs: **R** = `rgraph.py` of `research/mobius_rings_proof` (the program R of Note 5), run on `fgame.py`, a faster drop-in for its move generator and adjudicator (`fverify.py`, `seam_check.py`, `cyl_compare.py`); **M1**, **M2** = the solvers `mob1_32`, `mob2_32` of Note 5 (`confirm.py`, one ring per process).

| id | claim | label |
|---|---|---|
| V, L1, L2, L3 | statement V and Lemmas 1, 2(a), 2(b), 3 on the strip | PROVED in Note 5, section 3 (refereed); cited |
| H | hypotheses of V and Lemmas 2, 3 for TT, SS at the chosen cuts (sections 1-3) | PROVED here, given C1 |
| C1 | $R$ of $TT(5)$ and $SS(6)$: no flag, no passer, zone disjoint from the arc, signature NNNPN | CHECKED-2 (R and an independent program, see below) |
| C2 | $TT(m)$, $m=1..4$, and $SS(m)$, $m=0..5$: signature NNNP | CHECKED-2 (M1, M2); R's reduced graphs agree for TT $m=1..4$, SS $m=1..5$ |
| C3 | $\mathrm{ins}_c(R_m)=R_{m+1}$ at every cut tested (section 4) | COMPUTED-1 (R); extra evidence, not used |
| S | seam facts of section 2 | COMPUTED-1 (R); extra evidence, not used |
| D | `fgame.py` equals R's original rules module `mgame.py` (moves, passers, classes) on 2000 random positions, both surfaces | COMPUTED-1 (`fgame_test.py`, 0 mismatches); Note 5's D compares `mgame.py` with M2 |
| T | $TT(m)\equiv\star3$ ($m\ge1$), $SS(m)\equiv\star3$ ($m\ge0$) | PROVED given V, L1-L3, C1, C2 |

C1 label after the independent recomputation: **CHECKED-2**. A program written by a model of another vendor on its own rules implementation (the referee's program of Note 5, extended; it uses no code of R, `fgame.py`, M1 or M2) gave the same graphs: $TT(5)$: 1305 nodes, 4018 K-edges, 1212 T-moves, no flagged node, no node with a passer, zone $\{0,1,3..8\}$, NNNPN; $SS(6)$: 22755, 72730, 49694, none, none, zone $\{0,1,12,13,15..22\}$, NNNPN. It also confirmed $\mathrm{ins}_{14}$ from $TT(5)$ onto $TT(6)$ and $\mathrm{ins}_6$ from $SS(6)$ onto $SS(7)$ as isomorphisms of reduced graphs (roots, nodes, K-children and T-flags per side), the seam facts of section 2 (no capture across the seam in any node of $TT(5)$; in $SS(6)$ 1705 and 1640 captures across it, all of class T), and C2 by its own whole-board search (a third program for every line of C2).

## 1. Families, walls, cuts

Files $0..n-1$ form the chart; the seam joins file $n-1$ to file $0$. Pattern file, wall, $\mathrm{ins}_c$ (new files $c+1,c+2$ hold copies of files $c+1,c$; old files $\ge c+1$ shift by 2) and "far" are as in Note 5, sections 1 and 3.

| | $TT(m)$, $n=2m+10$ | $SS(m)$, $n=2m+11$ |
|---|---|---|
| fixed part | files $0..9$: $B5\,W2\,W6B7\,W3\,B7\,B6\,W3\,W2\,B6\,W2$ | files $0,1$: $B6\,W3$; files $2m+2..2m+10$: $W6B7\,W3\,B7\,B6\,W3\,W2\,B6\,W2\,B4$ |
| wall (type E) | files $10..n-1$: $B4$ even, $W2$ odd | files $2..2m+1$: $W2$ even, $B4$ odd |
| seam neighbours (file $n-1$ / file 0) | $W2$ (wall) / $B5$ (zone) | $B4$ (zone) / $B6$ (zone) |
| zone $Z_m$ (C1, C3) | $\{0,1,3..8\}$ for $m\ge1$ | $\{0,1\}\cup\{2m,2m+1\}\cup\{2m+3..n-1\}$ for $m\ge4$ |
| cut, arc $c-4..c+5$ | $c=14$, $10..19$ | $c=6$, $2..11$ |
| arc inside wall $\setminus Z_m$ iff | $n-1\ge19$: $m\ge5$ | $2m-1\ge11$: $m\ge6$ |
| $\mathrm{ins}_c(\mathrm{start}_m)$ | inserts copies of files 15 ($W2$), 14 ($B4$) after file 14: $\mathrm{start}_{m+1}$ for $m\ge3$ | inserts copies of files 7 ($B4$), 6 ($W2$) after file 6: $\mathrm{start}_{m+1}$ for $m\ge3$ |
| $\mathrm{ins}_c(Z_m)$ (old indices) | $Z_m$ (all $<15$) $=Z_{m+1}$ | $\{0,1\}$ fixed, $\{2m,2m+1\}\to\{2m+2,2m+3\}$, $\{2m+3..2m+10\}\to\{2m+5..2m+12\}$: $Z_{m+1}$ ($m\ge4$) |

**Phase.** Note 5 defines a type E wall as single pawns alternating $W2$ (up) and $B4$ (down) on a chart interval; the parity of the phase is not part of the definition, and Lemma 2's proof treats $q=W2$ and $q=B4$ separately, each with the other pattern pawn on both neighbours. TT has the phase of Note 5's F1, F2 ($B4$ even); SS has the opposite phase ($W2$ even). Both are type E, so Lemmas 2 and 3 apply as stated; $\kappa$ (needed in Note 5 only for type O, F3) is not used. The mirror $f\mapsto n-1-f$ enters only inside Note 5's proof of Lemma 2 (the window $j-3..j+1$). Insertion keeps the phase: TT's new files 15, 16 hold $W2$, $B4$ between $B4$ (14) and $W2$ (old 15, now 17); SS's new files 7, 8 hold $B4$, $W2$ between $W2$ (6) and $B4$ (old 7, now 9).

**Lemma 3's range** ($4\le c\le n-6$): TT $c=14$, $n\ge20$ (equality $c=n-6$ at $n=20$); SS $c=6$, $n\ge23$.

## 2. The seam

The seam enters a pawn's moves, flag and passed status only through the view of a pawn on file $0$ or $n-1$ (Note 5, section 1, View). We go through the places where Note 5 uses the arc or its surroundings.

- **V** needs only that files $c,c+1$ are pattern files and $c+1\le n-1$. (V1)'s proof replaces the chart pair $(c,c+1)$ and keeps the seam pair $(n-1,0)$, now $(n+1,0)$, with the same contents and the same mirroring, whatever those contents are. For TT, $c+1=15<19$; for SS, $c+1=7$.
- **Lemma 2** is used for central pawns on files $c-3..c+4$ (TT: $11..18$; SS: $3..10$), with windows $j-1..j+3$ or $j-3..j+1$ inside the arc. Its proof reads the contents of the window's files, the views of the window's interior files, and the view of the capturer on file $j$. For TT's $j=18$ (window $15..19$) the capturer's view is files $17,18,19$, all chart files; the departure square on file 17 is seen from files $16..18$ only. File 19's own view, which contains file 0 across the seam, is never read. So nothing in Lemma 2 depends on file 0.
- **Lemma 3.** Far files are $f\le c-4$ or $f\ge c+5$ in chart coordinates: TT $\{0..10\}\cup\{19\}$ at $n=20$, SS $\{0,1,2\}\cup\{11..n-1\}$. In (ii) a far first move changes its own file and its capture target, a chart neighbour or the seam neighbour; from file 19 these are 18 ($=c+4$) or 0, from file 0 they are 1 or 19. In (iii) a far reply changes files $\le c-1$ or $\ge c+2$, a seam capture changes files 0 and $n-1$, and an e.p. capturer is a chart or seam neighbour of a far stepper. In every case files $c-2..c+3$ are untouched, $c,c+1$ stay pattern files, and V gives the correspondence. The far pawns may have any content: the proof matches their moves through V1 (same view, hence same moves, flags and status) and never asks them to be pattern pawns or to be unchanged. Note 5's bracketed seam remarks ("both are far, since $0\le c-4$ and $n-1\ge c+5$") cover the case $c+5=n-1$ exactly as they cover $c-4=0$.
- **Answer.** No step uses that the seam neighbour of the arc's end file is a pattern file or is unchanged. In Note 5's F1, F2 that neighbour (file $n-1$) happens to be frozen; for TT at $n=20$ it is file 0, a zone file, and the lemmas still apply. For $m>5$, TT's arc $10..19$ is interior ($n-1\ge21$) and the question does not arise. SS's arc $2..11$ is interior for every $m\ge6$; files 0, 1 (zone) and the seam lie on the far side of file 2, and the seam captures between files 0 and $n-1$ (both far) are matched by (ii), (iii).

**Computed corroboration (S; `seam_check.py`, `logs/seam_check_TT5.log`, `logs/seam_check_SS6.log`).** $TT(5)$: in all 1305 nodes the arc $10..19$ equals the start and there is no flag; file 0 differs from the start in 435 nodes, file 19 in none; the pawn on file 19 has exactly two moves per node, $W2\to3$ and $W2\to4$, both P (2610 moves); no capture across the seam exists in any node; no K-move touches the arc. Moreover the strip and cylinder reduced graphs of $TT(5)$ coincide: the same 1305 positions, the same K-children and T-counts (`cyl_compare.py`, `logs/cyl_compare_TT5.log`). These are the numbers of C1T in Note 4 for $T_{20}$, which is $TT(5)$ rotated. $SS(6)$: in all 22755 nodes the arc $2..11$ equals the start, no flag; captures across the seam occur (1705 from file 0, 1640 from file 22), all T, both files far; no K-move touches the arc. Unlike TT, SS's strip graph differs from the cylinder's (22755 versus 40445 nodes for $S_{23}$ in Note 4): the seam acts inside the zone.

## 3. Invariant and step

**H (start).** $\mathrm{start}_m$ has no flag (no pawn has just double-stepped) and no passed pawn (C1 for the base; for $m>m_0$ by V3 and $\mathrm{ins}_c(\mathrm{start}_m)=\mathrm{start}_{m+1}$).

**Invariant $I_m$** (Note 5, section 4): no node of $R_m$ has a flag, and every node agrees with $\mathrm{start}_m$ outside $Z_m$.

**Step.** Let $m\ge m_0$ and $I_m$. Every node $p$ of $R_m$ is non-terminal (root or K-child) and has no flag. The arc lies in the wall and avoids $Z_m$ (section 1 table), so its files carry exactly their start content: pattern files of one wall, in its single phase. The arc is a chart interval ($c-4\ge0$, $c+5\le n-1$). So Lemma 3 applies to every node with the family's fixed $c$, and $\mathrm{ins}_c(\mathrm{start}_m)=\mathrm{start}_{m+1}$. Induction on K-distance from the root (Note 5, section 4) gives: the nodes of $R_{m+1}$ are the images of those of $R_m$, with K-children and T-flags mapped. Images have no flag and agree with $\mathrm{start}_{m+1}$ outside $\mathrm{ins}_c(Z_m)=Z_{m+1}$, since the inserted files are copies of pattern files. So $I_{m+1}$ and $R_{m+1}\cong R_m$. For SS the zone moves with $m$; the check that the moved zone is the next zone, including the wall-end files $2m,2m+1$, is the last table row of section 1 (valid for $m\ge4$, in particular $m\ge6$).

## 4. Finite inputs

**C1** (`fverify.py`, `logs/fverify_TT.log`, `logs/fverify_SS.log`). Every line has flagged $=0$ and passer nodes $=0$.

| family, base | nodes / K-edges / T-moves | zone | arc | signature $h=0..4$ |
|---|---|---|---|---|
| $TT(5)$, $n=20$ | 1305 / 4018 / 1212 | $\{0,1,3..8\}$ | $10..19$ | NNNPN |
| $SS(6)$, $n=23$ | 22755 / 72730 / 49694 | $\{0,1,12,13,15..22\}$ | $2..11$ | NNNPN |

**C2** (`confirm.py`, `logs/confirm_TT_SS.log`): M1 and M2 give NNNP ($h=0..3$) for $TT(m)$, $m=1..4$ ($n=12..18$), and for $SS(m)$, $m=0..5$ ($n=11..21$). R's reduced graphs give NNNPN for TT $m=1..4$ and SS $m=1..5$. ($TT(0)$, $n=10$, gives LLLL and is not claimed.)

**C3** (extra). R found $\mathrm{ins}_c(R_m)=R_{m+1}$ for every cut $c$ with $c,c+1$ in TT's wall at the steps $m\to m+1$, $m=1..7$. For SS at the steps $m\to m+1$, $m=4,5,6$, it holds for $c=2..2m-2$ and fails at $c=2m-1,2m$, the two cuts whose copied files reach the zone (not admissible); at $m=1,2,3$ the SS graphs are not yet stable (node counts 18649, 28307, 24837, then 22755 from $m=4$). Admissible cuts reported by `fverify.py`: TT at $m=5$: $\{14\}$; SS at $m=6$: $\{6\}$. M1 and M2 also give NNNP for TT $m=5..11$ and SS $m=6..10$ (beyond what the proof needs).

## 5. Theorem and proof

**Theorem.** $TT(m)\equiv\star3$ for every $m\ge1$ and $SS(m)\equiv\star3$ for every $m\ge0$: $G+\star h$ has the outcome of $\star3+\star h$ for every nim-heap $\star h$. Hence $M_n$ carries a $\star3$ ring with $n+1$ pawns for every $n\ge11$.

*Proof.* Let $G$ be TT or SS, $m\ge m_0$. $I_{m_0}$ is C1 (with section 1 for the zone and arc). Section 3 gives $I_m$ and $R_m\cong R_{m_0}$, with T-flags, for every $m\ge m_0$. The outcome of $R+\star h$ depends only on the graph, its T-flags and $h$, so by C1 it is N, N, N, P for $h=0,1,2,3$ with either player to move first; by Lemma 1 of Note 5 (the start is non-terminal) so is that of $G(m)+\star h$. For $h\ge4$ the player to move takes the heap to $\star3$; the pawn position, which has no flag, is kept, and $G(m)+\star3$ is P, so $G(m)+\star h$ is N. These are the outcomes of $\star3+\star h$: P exactly for $h=3$. For $m<m_0$ (TT $m=1..4$, SS $m=0..5$) C2 gives NNNP for $h\le3$, and $h\ge4$ follows as before. TT covers $n=2m+10$, every even $n\ge12$; SS covers $n=2m+11$, every odd $n\ge11$. $\blacksquare$

## 6. Scope and self-check

**Not claimed.** Other race rules; the component-sum model; equality with $\star3$ as a standard partizan game or against addends other than nim-heaps (as in Note 4, H7). $n=10$ with 11 pawns is open: $TT(0)$ is LLLL, the targeted search found $\star3$ rings with 12 pawns but none with 11 (REPORT.md section 4). $n=9$ is covered by the previously known ring, not by these families. The further $n+1$ families H2 (odd $n=9..31$) and E2 (even $n=12..32$) are CHECKED-2 only (M1, M2): their reduced graphs carry e.p. flags, so Lemmas 2, 3 do not apply as stated and no proof is given for them.

**Weakest points.**
1. **C1 is one program.** The whole induction rests on two graphs computed by R on `fgame.py`. Evidence short of a second program: `fgame.py` = `mgame.py` on 2000 random positions; Note 5's D ties `mgame.py` to M2; R's TT base graph on the strip equals R's cylinder graph of the same ring position for position, and the cylinder counts and zone are those of Note 4's C1T for $T_{20}$ (its rotation), computed there by three other programs; C2's M1/M2 signatures agree with R's at every overlapping $m$. The SS base graph has no such cross-check. A rules misreading shared by all programs would not be caught.
2. **The arc at the seam (TT, $n=20$).** Section 2 argues that Lemma 3's case $c+5=n-1$ is covered by Note 5's proof as written, and that file 0 changing is irrelevant. Note 5's random test of Lemma 3 (2826 seam-touching arcs) and its referee covered $c-4=0$ with a frozen neighbour, not this mirror case with a moving neighbour; S shows that, in this graph, the file-19 pawn's only moves are pushes (all P) and no seam capture ever arises, so the case is not stressed. If in doubt, one can avoid it: take $m_0=6$ for TT ($n=22$, arc $10..19$ interior), with $TT(5)$ moved into C2 (M1, M2 give NNNP); the C1 line for $m=6$ is in `logs/fverify_TT.log` with the same numbers and zone.
3. **SS's base is the larger graph** (22755 nodes) and its zone contains two wall files that move; the arc's clearance from them is one file (arc ends at 11, zone starts at $2m=12$). The C3 failures at exactly the two cuts whose arc would reach the zone are consistent with this and show that the test can fail.
