# $N1_n=\star2$ for every $n\ge 9$ (whole-board game): proof note

**Summary**
1. Theorem: in the whole-board game on $C_n$ (race rule "count", e.p. on, an e.p.-capturable pawn is not passed, the game ends at the first passed pawn), for every $n\ge9$ the $(n+1)$-pawn position
   $N1_n=(B4\,W2)^{\lfloor (n-7)/2\rfloor}\,B6\,W2\,W3\,B6\,B7\,W3\,W6B7$ (odd $n$) and the same with a trailing $W2$ (even $n$) is $\star2$.
2. The proof is T50's insertion proof (Lemmas 1-3, with the written-out Lemma 3 of `research/ring_n_plus_2_proof/PROOF.md` 2b), at two cuts: odd $n$, $c=6$, $n_0=19$; even $n$, $c=4$, $n_0=18$. The wall (files $0..n-8$ odd, $0..n-9$ even) has even length, $B4$ on even files and $W2$ on odd files.
3. C1: the reduced games at $n_0$ have 2404 (odd) and 435 (even) nodes, no e.p. flag, no passed pawn, zones $\{0,1\}\cup\{n-7..n-2\}$ resp. $\{n-8..n-3\}$, signature NNPNN; files $2..11$ resp. $0..9$ are exact pattern files in every node, and $\mathrm{ins}_c$ is an isomorphism from $n_0$ to $n_0+2$ (and on).
4. C2: $N1_n=\star2$ for odd $n=9,11,13,15,17$ and even $n=10,12,14,16$ by direct search (E ran both parities to $n=25$). Status: PROVED [AI] for $n\ge n_0$ given T50's Lemmas 1-3, 2b and C1; CHECKED-2 for the smaller $n$ (3 programs).
5. Scope: whole-board game, race rule "count" only; not the component-sum model of cylcgt, not other race rules, not equivalence against arbitrary addends.

## 0. Claims and labels
PROVED = by hand, given the lemmas (all hand proofs here are [AI]). CHECKED-2 = two or more independently written programs agree. Programs: **A** = `rg` (via `pump_verify.py`, `graph.py`); **E** = `verify_compute/myeng.py` (driven by `check_N1.py`, `base_N1.py`); **X** = `research/c9_rings/codex/engine.py` (driven by `base_codex.py`).

| id | claim | label |
|---|---|---|
| L1-L3 | T50 Lemmas 1-3 (reduction, wall pawns, insertion) and the written-out proof of Lemma 3 (`PROOF.md` 2b) | PROVED in T50 / PROOF.md (2b: Codex SOUND) |
| H1-H7 | hypotheses of the lemmas for $N1_n$, odd $c=6$, $n_0=19$ and even $c=4$, $n_0=18$; induction; meaning of $=\star2$ | PROVED [AI] given C1 and L1-L3 |
| C1o | $N1_{19}$: 2404 nodes, 7067 K-, 3348 T-moves, no flag, no passer, zone $\{0,1,12..17\}$, NNPNN, files $2..11$ exact pattern in every node | CHECKED-2 (A, E) |
| C1e | $N1_{18}$: 435 nodes, 1118 K-, 404 T-moves, no flag, no passer, zone $\{10..15\}$, NNPNN, files $0..9$ exact pattern in every node | CHECKED-2 (A, E) |
| C2 | $N1_n=\star2$ for odd $n=9,11,13,15,17$ and even $n=10,12,14,16$ (unreduced, no poison pruning, both e.p. readings) | CHECKED-2 (E, X for $n\le14$); E alone for $n=15,16,17$ |
| C3 | pump: $\mathrm{ins}_c$ isomorphism $n_0\to n_0+2\to\dots$ (20 steps odd, 16 even) | COMPUTED-1 (A) for all steps; CHECKED-2 for the first 2-3 steps (E) |
| S1 | Lemmas 2 and 3 on the actual nodes; sensitivity controls | CHECKED-2 (E) |

## 1. Setting
Model, classes T/L/P/K, reduced game: as in `proof.tex` and PROOF.md section 1 (race rule "count"). E.p. convention: a flag is recorded only if an enemy pawn stands beside the landing square (game-equivalent to `pawns.py`'s raw flags). "No flag" means this canonical convention.

**$N1_n$** (odd $n\ge9$, $n+1$ pawns): files $0..n-8$: $B4$ (even), $W2$ (odd); then $B6$ ($n-7$), $W2$ ($n-6$), $W3$ ($n-5$), $B6$ ($n-4$), $B7$ ($n-3$), $W3$ ($n-2$), $W6B7$ ($n-1$).

**$N1_n$** (even $n\ge10$, $n+1$ pawns): files $0..n-9$: $B4$ (even), $W2$ (odd); then $B6$ ($n-8$), $W2$ ($n-7$), $W3$ ($n-6$), $B6$ ($n-5$), $B7$ ($n-4$), $W3$ ($n-3$), $W6B7$ ($n-2$), $W2$ ($n-1$).

The **wall** is files $0..n-8$ (odd) resp. $0..n-9$ (even): type E (black pawn two ranks above the white one), even length $n-7$ resp. $n-8$ files, $B4$ on even files, $W2$ on odd files. Pattern file: a wall file whose content equals its start pawn. The **zone** $Z_n$: $\{0,1\}\cup\{n-7,\dots,n-2\}$ (odd), $\{n-8,\dots,n-3\}$ (even) (files on which some node differs from the start).

Lemma 1: a side wins $G+\star h$ moving first iff it wins the reduced game moving first. Lemma 2: for a wall pawn $q$ of the player to move with pattern neighbour files, (a) $Z$ has no passed pawn after any move of $q$, (b) if $c$ has no flag and the window $j-1..j+3$ (or $j-3..j+1$) consists of pattern files, every move of $q$ is L or P. Lemma 3: if $p$ has no passer, no flag, and files $c-4..c+5$ are pattern files, then the K-children and the existence of T-moves of $\mathrm{ins}_c(p)$ are the $\mathrm{ins}_c$-images of those of $p$.

## 2. The cut and the base
**Odd:** zone $\{0,1\}\cup\{n-7..n-2\}$; wall files $0..n-8$. The arc $A=\{c-4..c+5\}$ lies in the wall iff $6\le c\le n-13$; the least $n$ is $n_0=19$, where $c=6$ is the only cut (pump_verify finds $c=6$ automatically at $19\to21$), and $c=6$ is admissible for every $n\ge19$. $\mathrm{ins}_6$ fixes files $0..6$ and shifts files $\ge7$ by 2, so $\mathrm{ins}_6(Z_n)=Z_{n+2}$ (the $\{0,1\}$ part is fixed and belongs to $Z_{n+2}$).

**Even:** zone $\{n-8..n-3\}$; wall files $0..n-9$. The arc lies in the wall iff $4\le c\le n-14$; the least $n$ is $n_0=18$, where $c=4$ is the only cut (pump_verify finds $c=4$ at $18\to20$), and $c=4$ is admissible for every $n\ge18$. $\mathrm{ins}_4$ fixes files $0..4$ and shifts files $\ge5$ by 2, so $\mathrm{ins}_4(Z_n)=Z_{n+2}$.

For $n<n_0$ the reduced graphs have no ten-file arc of unchanged wall files; those $n$ are covered by C2, not by the induction.

## 3. Hypotheses of Lemmas 2 and 3
**H1 (wall, phase, ends).** The wall alternates $B4$ (even) / $W2$ (odd). $\mathrm{ins}_c$ inserts copies of files $c+1$ and $c$ after file $c$, which continue the phase, and $\mathrm{ins}_c(\mathrm{start}_n)=\mathrm{start}_{n+2}$ for $n\ge n_0$ (files $c,c+1$ are wall files). Neither end of the wall enters the lemmas: file 0 is $B4$ and the file beside the core is $W2$.

**H2 (no capture by $q$).** With pattern neighbours, the capture squares of $q$ on rank 3 are empty, and $B4$ cannot take e.p. a $W2$ that has not moved.

**H3 (windows at the two ends of the arc).**
- Odd, $c=6$, $n_0=19$: arc files $2..11$; central pawns files $3..10$. Left end $j=3$ ($W2$), window $2..6$; right end $j=10$ ($B4$), window $7..11$. Lemma 2(b) gives 0 T/K moves (file 3 has 1646 L + 3162 P over the nodes).
- Even, $c=4$, $n_0=18$: arc files $0..9$; central pawns files $1..8$. Left end $j=1$ ($W2$), window $0..4$; right end $j=8$ ($B4$), window $5..9$. Lemma 2(b) gives 0 T/K moves (all central moves are P except none; 3480 q-positions, 5220 moves).
In both, all windows lie inside the arc; the wall-end file beside the core ($n-8$ / $n-9$) is never part of a window.

**H4 (start).** $\mathrm{start}_n$ has no passed pawn and no flag: each pawn is blocked by an adjacent enemy pawn on the next rank; no double-step flag is live. E ran the passed-pawn test on all reduced nodes: none has a passer (C1).

**H5 (race rule).** Lemma 2 never uses the race; in Lemma 3 the passed pawns of $c_\mu$ and $\mathrm{ins}_c(c_\mu)$ coincide, so any rule depending on the passed pawns and on who moved gives the same class. The value is rule-specific, the lemmas are not. The base cases (C2) agree under both e.p.-across-heap readings "keep" and "expire".

**H6 (invariant).** $I_n$: no node of the reduced game has a flag, and every node agrees with $\mathrm{start}_n$ outside $Z_n$. $I_{n_0}$ is C1. If $I_n$ holds ($n\ge n_0$): every node is non-terminal with no flag, and $A$ consists of pattern files, so Lemma 3 applies to every node with $c$; with H4 and induction on the distance from the root, nodes, K-edges and T-flags of $G_{n+2}$ are the $\mathrm{ins}_c$-images of those of $G_n$. An image has no flag; it agrees with $\mathrm{start}_{n+2}$ outside $Z_{n+2}$ since the inserted files are copies of pattern files and $\mathrm{ins}_c(Z_n)=Z_{n+2}$. So $I_{n+2}$.

**H7 (meaning of $=\star2$).** $G=\star2$ means that for every heap $\star h$, $h<256$ (a passed pawn is worth $\pm256$), $G+\star h$ and $\star2+\star h$ have the same outcome: P for $h=2$ and N otherwise (signature NNPNN for $h=0..4$; for $h\ge5$ the heap move to the P-position $G+\star2$ gives N). The start has no flag and neither do the reduced nodes, so the e.p. convention across a heap move is immaterial (base cases ran both readings: identical).

## 4. Finite checks
Rerun commands (project root, `PYTHONPATH=.`). Logs in `research/ring_n_plus_1_proof/logs/`.

**C1o, C1e ($n_0$).** E: `logs/check_N1_N1.log`, `logs/check_N1_N1even.log`
(`.venv/bin/python research/ring_n_plus_1_proof/check_N1.py N1 19 6` and `... N1even 18 4`):
$N1_{19}$ has 2404 nodes, 7067 K-, 3348 T-moves, zone $\{0,1,12..17\}$, ep=0, NNPNN; $N1_{18}$ has 435, 1118, 404, zone $\{10..15\}$, ep=0, NNPNN; no passed pawn of either colour in any node; files $2..11$ resp. $0..9$ are exact pattern files in every node.
A: `logs/pump_N1odd_9_41.txt`, `logs/pump_N1even_10_40.txt`
(`.venv/bin/python research/ring_n_plus_2_proof/pump_verify.py N1odd 9 41` and `N1even 10 40`): same counts, ep=0, NNPNNNNN.

**Pump (C3).** A: for odd $n=19,21,\dots,41$ and even $n=18,20,\dots,40$ the node count, zone and signature stay fixed; each step $n\to n+2$ with the fixed cut reports "start->start True, nodes onto True, kept+T edges equal True". E: `check_N1.py` reports $\mathrm{ins}_c(\mathrm{start}_n)=\mathrm{start}_{n+2}$, graph equality node-for-node with equal K- and T-children, and Lemma 3 recomputed on every $\mathrm{ins}_c(p)$: 0 mismatches, for two steps ($19\to21\to23$, $18\to20\to22$).

**Lemmas 2, 3 (S1).** E: `check_N1.py` logs above: Lemma 2 on every central wall pawn, both colours, windows as in H3: odd 19232 q-positions, 28848 moves; even 3480 q-positions, 5220 moves; (a) 0 failures, (b) 0 T/K moves. Sensitivity: control cuts $c+1..c+5$ fail (odd: 2975 of 4808 at $c=11$; even: 595 of 870 at $c=9$), so the test can fail.

**C2 (base cases).** E: `logs/base_N1.log` (`.venv/bin/python research/ring_n_plus_1_proof/base_N1.py 25`): NNPNN for odd $n=9..25$ and even $n=10..25$, both e.p. readings identical. X: `logs/base_codex.log` (`.venv/bin/python research/ring_n_plus_1_proof/base_codex.py 14`): NNPNN for odd $n=9,11,13$ and even $n=10,12,14$, both ep-on-heap readings.

## 5. Proof of the Theorem
Let $n\ge9$ (odd) or $n\ge10$ (even). If $n\ge n_0$ (odd $n\ge19$, even $n\ge18$): $I_{n_0}$ is C1; H6 gives $I_n$ for all such $n$ and $G_n\cong G_{n_0}$ (nodes, K-edges, T-flags). By C1 and Lemma 1, $G_n+\star2$ is a P-position and the signature is NNPNN; H7 gives all heaps: $G_n=\star2$. For $n<n_0$ in range (odd $9,11,13,15,17$; even $10,12,14,16$) use C2 and H7. $\blacksquare$

## 6. Gaps and caveats
1. The proof for $n\ge n_0$ is "proved modulo C1": it rests on the finite reduced-graph check C1, and the hand part is [AI].
2. Lemmas 1-3 are cited, not re-proved; their hand proofs are T50's and 2b, refereed SOUND for $P_n$ (T53, Codex) and $Q_n$ (T62, Codex). This note has no non-Claude referee.
3. C2 for $n=15,16,17$ (and higher) rests on short-circuit solvers; the no-early-exit solver was not run for those (memory). Wherever a no-early-exit run exists (codex engine, $n\le14$) it agrees.
4. Scope: whole-board game, race rule "count", canonical e.p. convention; not the component-sum model, not other race rules.
5. $N1_9$ is $\star2$ with $10=n+1$ pawns on $C_9$: this is the $n+1$ minimum on $C_9$ (no 9-pawn ring is $\star2$ on $C_9$).
6. Do not claim: the component-sum model, another race rule, or equivalence against arbitrary addends rather than nim-heaps.

**Sentence the paper may use.** In the whole-board game on the cylinder (race rule "count", en passant on, an e.p.-capturable pawn is not passed), for every $n\ge9$ the $(n+1)$-pawn ring $N1_n$ (odd: $(B4\,W2)^{(n-7)/2}B6\,W2\,W3\,B6\,B7\,W3\,W6B7$; even: the same with a trailing $W2$) is $\star2$, meaning $G+\star h$ and $\star2+\star h$ have the same outcome for every nim-heap $\star h$ below 256: for $n\ge19$ (odd) or $n\ge18$ (even) this follows from T50's insertion argument adapted by hand [AI] and one finite check each (2404 resp. 435 nodes) [C1], and for the smaller $n$ from direct finite searches [C2], confirmed by independently written programs.
