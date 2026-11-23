# F1, F2, F3 are $\star2$ on the Möbius strip for every width: the cylinder insertion proof, carried across the seam

**Summary**

1. **Theorem.** In the whole-board pawn game on the Möbius strip $M_n$ (8 ranks, race rule "count", e.p. on, an e.p.-capturable pawn is not passed, the game ends at the first passed pawn; conventions of `research/mobius_rings/REPORT.md`):
   - $F1(m)=(B4\,W2)^m\,B6\,W2\,W3\,B6\,B7\,W3\,B7\,W5$ ($n=2m+8$) is $\star2$ for every $m\ge1$;
   - $F2(m)=(B4\,W2)^m\,B6\,W2\,W3\,B6\,B7\,W3\,B7\,W5\,B7$ ($n=2m+9$) is $\star2$ for every $m\ge1$;
   - $F3(m)=B6\,W2\,W3\,B6\,B7\,W3\,(B7\,W5)^m\,W6B7$ ($n=2m+7$, $n+1$ pawns) is $\star2$ for every $m\ge0$.

   Status: **PROVED** for $m\ge5$ (all three families) by the insertion argument, given one finite check per family at $m_0=5$ (C1, my program `rgraph.py`); the cases $m<5$ are finite computations (C2, my programs plus the three solvers of `research/mobius_rings_n`). The hand proofs are [AI]; an independent AI referee (`delegate/out/T82/REPORT.md`) read them line by line, found them correct with two fixes of wording (applied here: one wall and one phase in the definition of pattern files; non-terminal roots in Lemma 1), recomputed C1 with its own program (all numbers agree, so C1 is CHECKED-2) and solved the unreduced game for $m=0..13$ (all signatures agree). No human has refereed them.
2. **The seam does not break the cylinder lemmas.** Every step of Lemmas 2 and 3 looks either at pawns whose three-file view lies inside a chart interval of pattern files (no seam inside it), or at "far" pawns, whose views $\mathrm{ins}_c$ leaves unchanged, the seam views included. The only new hypothesis is that the ten-file arc $c-4..c+5$ is a chart interval ($0\le c-4$, $c+5\le n-1$): it must not straddle the seam. The seam changes the dynamics only at the block's outer end, and there it changes the *base graph* (zone and node count), which the computation absorbs: e.g. in $F2$ the move $B4\to3$ on file 0 is K on the cylinder but P on the strip, because the $B7$ beyond the seam is seen on rank 2, behind the white capturer (section 2).
3. **Reduced graphs are constant in $m$** (no flag in any node, no passer, the zone avoids the block): $F1$: 435 nodes, 1118 K-edges, 404 T-moves for $m\ge2$; $F2$: 417, 1082, 356 for $m\ge2$; $F3$: 435, 1112, 428 for $m\ge1$. $\mathrm{ins}_c$ maps $R_m$ node by node onto $R_{m+1}$ for every step $m\to m+1$, $m=2..12$ ($F1$, $F2$) and $m=1..12$ ($F3$), for every cut inside the block (section 5). The linear growth of the solvers' node counts (+1251, +1239, +719 per step) is the L/P moves of block pawns, which the unreduced search visits and the reduced game deletes.
4. Cut and base: $F1$, $F2$: $c=4$, arc = files $0..9$ (the block's first ten files, ending at the seam), $m_0=5$; $F3$: $c=10$, arc = files $6..15$, $m_0=5$.

## 0. Claims and labels

PROVED = hand proof complete and its finite parts checked by my program (named). COMPUTED-1 = one program. CHECKED-k = $k$ independently written programs agree. Programs: **R** = `mgame.py` + `rgraph.py` (this folder, written for this note from the rules in `research/mobius_rings/REPORT.md`; the isomorphism test `rgraph.iso` is mine); **U** = `difftest.unreduced` (mine, full game, no pruning); **M1**, **M2**, **K** = `research/mobius_rings_n/bin/mob1_32`, `mob2_32`, `check` (earlier work, called as black boxes for values only).

| id | claim | label |
|---|---|---|
| V | view lemma on the strip (section 3) | PROVED |
| L1 | reduction lemma on the strip | PROVED (game-general); numerically: reduced = unreduced signature on 3000 random strip positions (R vs U, 0 mismatches) |
| L2 | wall-pawn lemma on the strip, walls W2/B4 and B7/W5 | PROVED; sanity: 36000 moves of random strip positions, 0 failures (`lemma_test.py`) |
| L3 | insertion lemma on the strip, arc a chart interval | PROVED; sanity: 3000 random strip positions (2826 with the arc touching the seam), 0 mismatches; control with a 4-file pattern: 31 of 436 mismatch |
| C1 | $R_5$ of $F1,F2,F3$: no flag, no passer, zone $\{10..15\}$, $\{10..15\}$, $\{0..5\}$; signature NNPNN | CHECKED-2 (R and the referee's program `delegate/out/T82/referee.py`); R reproduces the cylinder numbers of PROOF_N's C1M exactly (441/1128/428, zone $\{10..15,17\}$) |
| C2 | $F1(m),F2(m)$ for $m=1..4$, $F3(m)$ for $m=0..4$: signature NNPN | CHECKED-4 (R, M1, M2, K), plus U for $m\le2$; M1, M2 to $m=12$, K to $n\le21$ in the earlier report |
| C3 | $\mathrm{ins}_c(R_m)=R_{m+1}$ for every cut inside the block, steps $m=2..12$ (F1, F2), $1..12$ (F3) | COMPUTED-1 (R); not used beyond C1 (implied by L3 for $m\ge5$) |
| D | R agrees with M2 on 3000 random strip positions (n = 3..6, 2..6 pawns, either direction; 308 with an e.p. capture in the tree, 1167 with a capture across the seam) | CHECKED-2 (R/U vs M2) |
| T | $F1(m)=F2(m)=\star2$ ($m\ge1$), $F3(m)=\star2$ ($m\ge0$) | PROVED given L1-L3 and C1 (for $m\ge5$) and C2 ($m<5$) |

## 1. Setting

**Rules** (REPORT.md, "Rules as implemented"; implemented in `mgame.py`). Files $0..n-1$ form the *chart*; the seam joins file $n-1$ to file $0$ with ranks reversed. Every pawn has a direction $d=\pm1$ (White starts $+1$, Black $-1$); home rank, double step and distance follow $d$; a capture across the seam lands on the mirrored rank $9-r$ and flips $d$. Seen across the seam, a square $(f,r)$ appears at rank $9-r$ and a pawn's direction appears reversed. Passed = no enemy pawn (either direction) strictly ahead on its own or the two neighbouring files (seam neighbours mirrored), and not capturable e.p. now. Terminal = some side has a passed pawn; if both, race "count" (smaller distance $8-r-[r=2]$ up, $r-1-[r=7]$ down, over front passed pawns; ties to the side that did not just move). E.p.: the opponent may, on the next move only, capture onto the skipped square with any pawn whose diagonal capture square it is; the flag is stored only if such a capture exists (canonical; equivalent to M2's "always record, protect only if capturable", D).

**View.** The view of a pawn on file $f$ is the content of files $f-1,f,f+1$ as the pawn sees them (seam neighbours mirrored and direction-reversed) together with the flag. A pawn's moves and its passed status are functions of its view and its own square. For $1\le f\le n-2$ the view is files $f-1,f,f+1$ with no mirroring: **inside a chart interval the strip is a cylinder**.

**Classes, reduced game** (T50, `research/ring_family_proof/proof.tex`): a move $\mu$ of $X$ to $c_\mu$ is T (L) if $c_\mu$ is terminal and won (lost) by $X$; P if $c_\mu$ is non-terminal and $Y$ has a move to a terminal position won by $Y$; K otherwise. The reduced game $R$ of a root: nodes = positions reachable from the root by K-moves (of either side); each node carries, per side, its K-children and a T-flag (has a T-move). $R+\star h$: a side may take a T-move (wins), a K-move, or a heap move (the position, flag included, is kept).

**Walls.** A wall of type E is a chart interval of files holding single pawns alternating $W2$ (up) and $B4$ (down); type O is its colour reversal: $B7$ (down) and $W5$ (up). A *pattern file* is a wall file whose content is *exactly* its starting pawn, direction included (a reversed $B$ on rank 4 is not a pattern $B4$). In a hypothesis on consecutive pattern files, all those files belong to the same wall and follow its single alternating phase, with exactly the stated pawn and direction on each file. $\mathrm{ins}_c(p)$ ($0\le c$, $c+1\le n-1$): the position on $M_{n+2}$ with files $p_0..p_c,\,p_{c+1},\,p_c,\,p_{c+1},..,p_{n-1}$ (old file $f\ge c+1$ moves to $f+2$, a flag moves with its pawn). The seam stays between the last and the first file.

**$\kappa$** (colour reversal): $(colour,f,r,d)\mapsto(1-colour,f,9-r,-d)$. It maps steps, double steps (home $2\leftrightarrow7$), captures (the seam map $r\mapsto9-r$, $d\mapsto-d$ commutes with it), blockers, e.p. and distances ($8-r-[r=2]$ = $(9-r)-1-[9-r=7]$) onto themselves and swaps the players; the race tie rule is colour-blind. So $\kappa$ is an exact symmetry of the strip game exchanging Left and Right, and it maps a move of class T/L/P/K to a move of the same class. $\kappa(B7)=W2$, $\kappa(W5)=B4$: type O walls are $\kappa$-images of type E walls. The mirror $f\mapsto n-1-f$ is also an exact symmetry (it maps the seam to itself).

## 2. What the seam does at the blocks

`seam_moves.py` lists, at the root of each family at $m=5$, every move of a pawn on files $n-2,n-1,0,1$, with its class on the strip and on the cylinder (`logs/seam_moves.log`):

| ring | move | strip | cylinder | why |
|---|---|---|---|---|
| F1(5) | $W5\to6$ on file 17 | P, reply $B4$(0) takes across the seam | P, reply $B7$(16) takes | across the seam the white pawn on 17.6 is seen from file 0 on rank 3, moving down: $B4$ on file 0 captures it and becomes a black pawn on 17.6 moving *up*, passed. A new poisoning reply; class unchanged |
| F2(5) | $B4\to3$ on file 0 | **P**, reply $W2$(1) takes | **K** | on the cylinder the capturer $W3$ on file 0 is blocked by $B7$ on file 18 (rank 7, ahead); on the strip that $B7$ is seen on rank 2, behind: the capturer is passed |
| F3(5) | moves of files 0, 1 | K, K | K, K | the seam lies between $W6B7$ (immobile) and the zone; the block (files 6..15) does not touch it |

All other listed moves have the same class on both surfaces. Over all nodes of the reduced strip graph, every move of the file-0 pawn ($B4$) is P (F1: 435 of 435 nodes, F2: 417 of 417) and every move of the pawn on file $n-1$ is P. So the block's end next to the seam is *frozen*: on the strip neither end of the seam ever moves in the reduced game of F1, F2 (zone $\{2m..2m+5\}$), whereas on the cylinder file $n-1$ belongs to the zone of $M_n=F1$ ($\{n-8..n-3,n-1\}$, PROOF_N). This is why $R_m$ has 435 nodes on the strip and 441 on the cylinder (`logs/verify_F1_cylinder_control.log`).

**Effect on the lemmas.** The seam enters a pawn's moves and status only through the view of a pawn on file $0$ or $n-1$. Lemma 2 is applied only to pawns whose files $j-1..j+3$ (or $j-3..j+1$) form a chart interval of pattern files, so every view it inspects is a cylinder view. Lemma 3 treats the pawns on file $c-4$ (here file $0$ for F1, F2) and beyond as *far* pawns, and it needs of them only that $\mathrm{ins}_c$ does not change their views (V1 below), which holds on the strip because the inserted pair sits between chart files $c$ and $c+1$, away from the seam. The cylinder hypotheses therefore hold as stated, with one addition: the arc $c-4..c+5$ must be a chart interval. What would break is an arc across the seam: there the pattern does not continue (a $B4$ seen across the seam is a black pawn on rank 5 moving up), so "the inserted pair continues the wall" is false and the insertion is not even defined as a wall insertion. No such arc is used.

## 3. Lemmas on the strip, with proofs

**V (views).** Let $q$ be a position on $M_n$, $0\le c$, $c+1\le n-1$, and let files $c,c+1$ of $q$ be pattern files. (V1) Every old pawn of $\mathrm{ins}_c(q)$ has the same view as in $q$. (V2) A new pawn (on files $c+1,c+2$ of $\mathrm{ins}_c(q)$) has the view $(q_c,q_{c+1},q_c)$ or $(q_{c+1},q_c,q_{c+1})$, chart files, and is blocked by both neighbours. (V3) The passed pawns of $\mathrm{ins}_c(q)$ are exactly the images of those of $q$, with the same colour, rank, direction, own-file content and e.p. status; so $q$ and $\mathrm{ins}_c(q)$ are both non-terminal, or both terminal with the same winner for the same mover.

*Proof.* (V1) The adjacencies of $\mathrm{ins}_c(q)$ are those of $q$ except that the pair $(c,c+1)$ is replaced by $(c,\text{copy of }c+1)$ and $(\text{copy of }c,\,c+1)$; the seam pair $(n-1,0)$ becomes $(n+1,0)$ with the same contents and the same mirroring. So the old file $c$ sees on its right a copy of $q_{c+1}$, the old file $c+1$ sees on its left a copy of $q_c$, and every other view is literally the same. The flag moves with its pawn and its capturers have the same views, so it is recorded in both or neither. (V2) The new files are chart files $c+1,c+2$ ($c+2\le n$), not seam neighbours; with $E$ pattern a $W2$ sees $B4$ on both sides two ranks ahead, a $B4$ sees $W2$ on both sides two ranks ahead (type O: $\kappa$). (V3) Passed status is a function of the view (V1, V2); the race compares the distances of front passed pawns, which are the same pawns with the same squares; the mover is the same. $\square$

**Lemma 1 (reduction).** For every non-terminal pawn root $g$, every finite heap $\star h$, and either player to move, that player wins $g+\star h$ if and only if that player wins $R(g)+\star h$. An already-adjudicated terminal root keeps its assigned winner for every heap.

*Proof.* The game is finite (a pawn move advances a pawn or removes one; a heap move lowers $h$). A side wins a position moving first iff some option is lost by the opponent moving first. A terminal pawn move ends the whole game immediately. If just one colour has a passed pawn, that side wins. If both do, the count rule decides, with ties going to the opponent of the mover. Thus a T-move wins for its mover and an L-move loses for its mover. After a P-move the opponent has a reply to a terminal position he wins, so the P-option is a win for the opponent moving first: it never wins and may be deleted. K-moves and heap moves remain, and by induction on the game tree their values are those of the reduced game. Nothing here uses the geometry. $\square$

**Lemma 2 (wall pawns).** Let $c$ have no passed pawn and a flag (if any) that protects a pawn of the player not to move. Let $q$ be the pawn of the player $Z$ to move on a pattern file $j$, with files $j-1,j,j+1$ pattern files forming a chart interval. (a) After any move of $q$, $Z$ has no passed pawn. (b) If $c$ has no flag and files $j-1..j+3$ (or $j-3..j+1$) are pattern files forming a chart interval, every move of $q$ is L or P.

*Proof* (type E; type O by $\kappa$, which preserves classes; the window $j-3..j+1$ by the mirror). Files $j\pm1$ are chart neighbours of $j$ and hold exactly the pattern pawn of the other colour two ranks further on in $q$'s direction ($q=W2$: $B4$; $q=B4$: $W2$). *No capture by $q$:* its capture squares are rank 3 of files $j\pm1$, which are empty; an e.p. capture would need an enemy pawn that has just double-stepped on $j\pm1$ over rank 3, i.e. a white pawn now on 4 (if $q=B4$) or a reversed black pawn now on 4 (if $q=W2$); either would make $j\pm1$ a non-pattern file. So the moves of $q$ are $W2\to3$, $W2\to4$, $B4\to3$.
(a) Status depends on the enemy pawns in a pawn's view and on the flag. No enemy pawn moves; the old flag, if any, protected an enemy pawn, so its lapse changes no pawn of $Z$; so the other pawns of $Z$ stay non-passed. After $W2\to3$ (resp. $B4\to3$) $q$ is blocked by the pawns on $j\pm1$ (rank 4 ahead of 3 for White, rank 2 ahead of 3 for Black). After $W2\to4$ nothing is ahead of $q$ on $j-1..j+1$, but the $B4$ on $j+1$ can capture onto $(j,3)$, so the (canonical) flag is recorded and $q$ is not passed.
(b) By (a) $X=Z$ has no passed pawn after the move. If $Y$ has one, the move is L. Otherwise $Y$ answers with the pawn of $j+1$: it takes $q$ on $(j,3)$ (e.p. after $W2\to4$). No seam is crossed ($j$, $j+1$ are chart neighbours). The capturer stands on $(j,3)$; its view is files $j-1,j,j+1$ (chart, since $j\ge1$): $j-1$ holds only a pattern pawn of $Y$'s colour, $j$ only the capturer, $j+1$ is empty. So it is passed (no flag after a capture). The status of an $X$ pawn can change only if a pawn of $Y$ in its view moved or vanished: the departure square $(j+1,\cdot)$ is in the views of files $j,j+1,j+2$ only, since $j+1$ is an interior file of the chart interval $j-1..j+3$, so no pawn sees it across the seam. Files $j$, $j+1$ hold no $X$ pawn; the $X$ pawn on $j+2$ is still blocked by the $Y$ pawn on $j+3$ (two ranks ahead, chart neighbour). The arrival square only adds blockers. The flag of the double step protected $q$, which is gone. So $X$ has no passed pawn and $Y$ has one: the reply is a terminal position won by $Y$, and the move is P. $\square$

**Lemma 3 (insertion).** Let $p$ on $M_n$ have no passed pawn and no flag, let $4\le c\le n-6$ (so $c-4..c+5$ is a chart interval) and let files $c-4..c+5$ be pattern files of one wall. Then for each side the K-children of $\hat p=\mathrm{ins}_c(p)$ are the $\mathrm{ins}_c$-images of those of $p$, and the side has a T-move in $\hat p$ iff it has one in $p$.

*Proof* (this is PROOF.md 2b of `research/ring_n_plus_2_proof`, re-checked line by line for the strip; the seam enters only where marked). $X$ to move, $Y$ the other. $A=\{c-4..c+5\}$; in $\hat p$ the files $c-4..c+7$ are pattern files, a chart interval of $M_{n+2}$. By V3, $\hat p$ has no passed pawn.
(i) *Central pawns.* A pawn of $X$ on $j\in\{c-3..c+4\}$ has its window $j-1..j+3$ ($j\le c+2$) or $j-3..j+1$ ($j\ge c-1$) inside $A$, a chart interval. Lemma 2(b): all its moves are L or P. The same holds in $\hat p$ for the pawns on $c-3..c+6$, new pawns included.
(ii) *Far moves of $X$.* Every other pawn of $X$ is on a file $\le c-4$ or $\ge c+5$ of $p$ and corresponds to a pawn of $\hat p$ on $\le c-4$ or $\ge c+7$ with the same view (V1), hence the same moves. A move $\mu$ of it changes its own file and, for a capture or an e.p. capture, the target file, which is a chart neighbour or, across the seam, file $n-1$ (from file 0) or file 0 (from file $n-1$) **[seam: both are far, since $0\le c-4$ and $n-1\ge c+5$]**. So it changes only files $\le c-3$ or $\ge c+4$, files $c-2..c+3$ of $c_\mu$ are unchanged, $c,c+1$ are pattern files of $c_\mu$, and $\mathrm{ins}_c(c_\mu)$ is the child of the image move $\hat\mu$ (V1 for the flag). By V3 $\mu$ and $\hat\mu$ are both T, both L or both non-terminal.
(iii) *Poison.* Let $c_\mu$ be non-terminal. Files $c-2..c+3$ of $c_\mu$, and $c-2..c+5$ of $\mathrm{ins}_c(c_\mu)$, are pattern files. *Near* pawns of $Y$: those on $c-1..c+2$ (resp. $c-1..c+4$); *far*: the others. A near pawn has its three files inside those pattern files, a chart interval; $c_\mu$ has no passed pawn and its flag (if any) protects $X$'s stepper; by Lemma 2(a) no near reply gives $Y$ a passed pawn. Far pawns correspond (V1) with the same moves; a far reply changes only files $\le c-1$ or $\ge c+2$ **[seam: a capture across it changes files $0$ and $n-1$, both far]**, so $c,c+1$ stay pattern files and V3 gives: $c_\mu\nu$ is terminal-won by $Y$ iff $\mathrm{ins}_c(c_\mu\nu)$ is. An e.p. reply takes the stepper of $\mu$, which stands on a far file ($\le c-4$ or $\ge c+5$); its capturer is a chart or seam neighbour of it, on a file $\le c-3$ or $\ge c+4$, hence far. So $\mu$ is P iff $\hat\mu$ is.
By (i)-(iii) the T-moves of $\hat p$ are the images of those of $p$, and so are the K-moves, with children $\mathrm{ins}_c(c_\mu)$. $\square$

## 4. The families: block, cut, zone, invariant

| | $F1(m)$, $n=2m+8$ | $F2(m)$, $n=2m+9$ | $F3(m)$, $n=2m+7$ |
|---|---|---|---|
| block (wall) | files $0..2m-1$: $B4$ even, $W2$ odd (type E) | same | files $6..2m+5$: $B7$ even, $W5$ odd (type O) |
| seam neighbours | file $n-1$ $W5$ / file 0 $B4$ | $B7$ / $B4$ | $W6B7$ / $B6$ |
| zone $Z_m$ ($m\ge2$; F3 $m\ge0$) | $\{2m..2m+5\}$ | $\{2m..2m+5\}$ | $\{0..5\}$ |
| cut, arc | $c=4$, $0..9$ | $c=4$, $0..9$ | $c=10$, $6..15$ |
| arc inside block $\setminus Z_m$ iff | $m\ge5$ | $m\ge5$ | $m\ge5$ |
| $\mathrm{ins}_c(\mathrm{start}_m)=\mathrm{start}_{m+1}$ | $m\ge3$: copies of files 5 ($W2$), 4 ($B4$) after file 4 | same | $m\ge3$: copies of 11 ($W5$), 10 ($B7$) after 10 |
| $\mathrm{ins}_c(Z_m)$ | $Z_{m+1}$ (files $\ge5$ shift by 2, $2m\ge5$) | same | $Z_m$ (left of the cut) |

**H (start).** Each start position has no passed pawn and no flag (checked by R: `reduced()` asserts it; by hand e.g. for $F1$: $B4$ blocked by $W2$ on a neighbour file, $W2$ by $B4$, $B6$(2m) by $W2$(2m-1, rank 2 below), $W5$($n-1$) by $B7$($n-2$), and across the seam $B4$(0) sees $W5$ on rank 4, level, so the seam adds no blocker and removes none it needs).

**Invariant $I_m$:** no node of $R_m$ has a flag, and every node agrees with $\mathrm{start}_m$ outside $Z_m$.

**Step.** Let $m\ge5$ and $I_m$. Every node $p$ of $R_m$ is non-terminal (it is the root or a K-child), has no flag, and its arc files are block files outside $Z_m$, so they carry exactly their start content: pattern files. The arc is a chart interval ($c-4\ge0$, $c+5\le 2m-1<n-1$ resp. $\le 2m+5<n-1$). Lemma 3 applies to every node with the family's $c$. As $\mathrm{ins}_c(\mathrm{start}_m)=\mathrm{start}_{m+1}$ and $\mathrm{ins}_c$ is injective, induction on the K-distance from the root gives: the nodes of $R_{m+1}$ are the images of the nodes of $R_m$, with K-children and T-flags mapped. Images have no flag, and they agree with $\mathrm{start}_{m+1}$ outside $\mathrm{ins}_c(Z_m)=Z_{m+1}$ (the inserted files are copies of pattern files, i.e. of start content). So $I_{m+1}$, and $R_{m+1}\cong R_m$ as reduced games.

## 5. Finite checks (exact commands; `sh research/mobius_rings_proof/run_all.sh` reruns all, about 6 min, one process at a time, nice 15)

**C1 and C3** (`nice -n 15 python3 verify.py F1 0 13` etc., `logs/verify_F{1,2,3}.log`). Per $m$: nodes / K-edges / T-moves, flagged nodes, nodes with a passer, zone, signature $h=0..4$. Every line has flagged=0 and passer_nodes=0.

| m | F1 nodes/K/T, zone, sig | F2 nodes/K/T, zone, sig | F3 nodes/K/T, zone, sig |
|---|---|---|---|
| 0 | 411/944/476, $\{0..5,7\}$, RNRRR | 452/1172/456, $\{0..5\}$, NNRRR | 453/1148/476, $\{0..5\}$, NNPNN |
| 1 | 453/1154/452, $\{2..7\}$, NNPNN | 441/1128/428, $\{0,2..7\}$, NNPNN | 435/1112/428, $\{0..5\}$, NNPNN |
| 2..13 | 435/1118/404, $\{2m..2m+5\}$, NNPNN | 417/1082/356, $\{2m..2m+5\}$, NNPNN | 435/1112/428, $\{0..5\}$, NNPNN |

C1 is the line $m=5$ of each family: $F1$ zone $\{10..15\}$, $F2$ zone $\{10..15\}$, $F3$ zone $\{0..5\}$; none meets its arc; signature NNPNN.
C3 (the test of the step on the actual graphs, `rgraph.iso`: $\mathrm{ins}_c$(root) = root, node count equal, every image a node, per side the image of the K-children set equals the K-children set, T-flags equal): passes for **every** cut $c$ with $c,c+1$ in the block and $\mathrm{ins}_c(\mathrm{start}_m)=\mathrm{start}_{m+1}$, at every step $m\to m+1$ for $m=2..12$ (F1, F2; e.g. step $12\to13$: $c=0..22$) and $m=1..12$ (F3; step $12\to13$: $c=6..28$). The steps $5\to6,\dots,12\to13$ are eight consecutive steps beyond $m_0=5$. The Lemma-3-admissible cuts are listed in the logs ($c=4$ from step $5\to6$ for F1, F2; $c=10$ for F3). The test can fail: at $1\to2$ with $c=0$ it reports `count 453 435` (F1) and `count 441 417` (F2). Cuts $c<4$ (arc across the seam) also pass computationally; Lemma 3 does not cover them and they are not used.

**Cylinder control** (`verify.py F1 5 7 --cyl`): R with the twist off gives 441 nodes, 1128 K, 428 T, zone $\{10..15,17\}$, NNPNN at $n=18$, i.e. exactly PROOF_N's C1M (programs A and E there).

**C2** (`nice -n 15 python3 base.py`, `logs/base.log`, $m=0..6$; one ring per solver process):
```
F1 m=0 n=8  rgraph=RNRR unreduced=RNRR mob1=RNRR mob2=RNRR check=RNRR
F1 m=1..6   rgraph=NNPN (unreduced NNPN for m<=2) mob1=NNPN mob2=NNPN check=NNPN
F2 m=0 n=9  rgraph=NNRR unreduced=NNRR mob1=NNRR mob2=NNRR check=NNRR
F2 m=1..6   all NNPN
F3 m=0..6   all NNPN
```
(each line of the log lists all five programs; I have shortened identical lines here). M1, M2 give NNPN up to $m=12$ (F1, F3) and $m=11$ (F2), K up to $n=21$ (`research/mobius_rings_n/logs/famconfirm.log`).

**D, L1** (`difftest.py 7 3000`, `logs/difftest_7_3000.log`): 3000 random strip positions, signatures of $G+\star h$, $h=0..3$, by U and by M2: 0 mismatches; reduced (R) vs unreduced (U): 0 mismatches. Coverage (`difftest_cover.py`): 308 positions have an e.p. capture in their tree, 1167 a capture across the seam, 2238 a reversed pawn that moves. *Side finding:* a first run fed all 3000 positions to one M2 process and gave 1 mismatch (`W5 B6 w7 -`, M2 `LNLL`, alone `NNNN`, `logs/difftest_7_3000_mixedwidth_batch.log`): M2's memo key is the cell array without the width, so a batch mixing widths can reuse another width's entry. The scans and `famconfirm.py` use one width per process and are not affected; the test now runs one M2 process per width.

**L2, L3 sanity** (`lemma_test.py 3 3000`, `logs/lemma_test_3_3000.log`): `{'pos': 3000, 'l3_bad': 0, 'ctrl_pos': 436, 'ctrl_bad': 31, 'l2a': 36000, 'l2a_bad': 0, 'l2b': 36000, 'l2b_bad': 0, 'seam_touch': 2826}`.

**Seam table** (`seam_moves.py F1 5` etc., `logs/seam_moves.log`): section 2.

## 6. Theorem and proof

**Theorem.** $F1(m)=\star2$ and $F2(m)=\star2$ for every $m\ge1$, $F3(m)=\star2$ for every $m\ge0$, in the sense: $F(m)+\star h$ and $\star2+\star h$ have the same outcome for every nim-heap $\star h$. (PROVED, given C1 for $m\ge5$, C2 for smaller $m$.)

*Proof.* $m\ge5$: $I_5$ is C1; section 4 gives $I_m$ and $R_m\cong R_5$ for all $m\ge5$, with T-flags. The outcome of $R+\star h$ depends only on the graph, the T-flags and $h$, so by C1 it is N, N, P for $h=0,1,2$; by Lemma 1 so is that of $F(m)+\star h$. For $h\ge3$ the heap move to $F(m)+\star2$ (a P-position; the start has no flag) wins, so N. These are the outcomes of $\star2+\star h$. $m<5$: C2 gives NNPN for $h\le3$, and $h\ge4$ as before. $\blacksquare$

## 7. What is and is not shown

- The induction needs no property checked only up to some $m$: the only computer fact used for $m\ge5$ is C1 at $m=5$. C3 for $m=5..12$ is redundant evidence.
- The lemmas are re-proved here on the strip, but they are the cylinder lemmas of T50 / PROOF.md 2b with the seam remarks added; no new idea was needed. An AI referee has read this text (section 0); no human has.
- Not shown: the families on the strip for another race rule; the component-sum model; equality with $\star2$ against addends other than nim-heaps; rings with other blocks (REPORT lists more pump blocks; the same argument applies to any block that is a type E or O wall of at least ten files outside the base zone, but each needs its own C1).
- Resources: all runs under nice 15. For about half a minute three `verify.py` processes (F1/F3 chain, F2, cylinder control) ran at once, one over the limit of two; no other process was touched, no pid outside my own was signalled.

## 8. Self-check: the three steps most likely to be wrong

1. **C1 rests on one program (R).** The zone and "no flag" at $m=5$ are what the whole induction stands on, and only `rgraph.py` builds the reduced strip graph. Why I believe it: R reproduces the cylinder reduced graph of PROOF_N ($M_{18}$: 441/1128/428, the same zone) built by two other programs; the strip geometry of `mgame.py` agrees with M2 on 3000 random positions with seam captures, e.p. and reversed pawns; the reduced signatures equal M1/M2/K values for every $m$ checked. A misreading shared with M2 (both follow REPORT.md's rules: e.p. by any pawn whose capture square is the skipped square, blocking by enemy pawns of either direction) would not be caught; it would also invalidate the earlier computations.
2. **Lemma 3 on the strip with the arc ending at the seam (F1, F2, $c=4$, file $c-4=0$).** File 0 is a pattern file of the arc whose pawn sees across the seam. The proof uses it as a far pawn (V1 only) and as the left file of the windows of central pawns on files 1, 2 (where Lemma 2 inspects only views of files $1..4$, chart neighbours). The risk is a missed interaction, e.g. an e.p. or seam capture that changes a file in $c-2..c+3$. I checked the possibilities in (ii) and (iii) case by case, and the random test with 2826 seam-touching arcs found no mismatch. Taking $c=5$ (arc $1..10$, $m_0=6$, $m=5$ then from C2) removes file 0 from the arc and changes nothing else.
3. **Lemma 2 transfer: no capture by $q$, the canonical flag, and $\kappa$ for F3.** That a reversed pawn arriving on a neighbour file is excluded rests on "pattern file = exact content including direction", which the invariant $I_m$ provides (start content). The type O wall of F3 uses $\kappa$, whose exactness on the strip (seam map commutes with $r\mapsto9-r$, distances and tie rule symmetric) I checked by hand; `lemma_test.py` exercises type O walls directly (half the positions) with 0 failures. A subtle e.p. convention mismatch (who may take e.p. across the seam) would affect only far pawns, which Lemma 3 handles by V1 without using the convention.
