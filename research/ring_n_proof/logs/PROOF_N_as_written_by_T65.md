# $M_n=\star2$ and $O_n=\star2$ for every $n\ge 10$ (resp. odd $n\ge 11$): proof note (whole-board game on $C_n$)

**Summary**
1. Theorem: in the whole-board game on $C_n$ (race rule "count", e.p. on, an e.p.-capturable pawn is not passed, game ends at the first passed pawn), the $n$-pawn rings $M_n = (B4\,W2)^{(n-8)/2}\,B6\,W2\,W3\,B6\,B7\,W3\,B7\,W5$ (even $n\ge10$) and $O_n = B4\,(B7\,W5)^{(n-9)/2}\,B7\,W3\,B7\,B6\,W3\,W2\,B6\,W2$ (odd $n\ge11$) are $\star2$.
2. The proof is T50's insertion proof (`research/ring_family_proof/proof.tex`, Lemmas 1-3, with the written-out Lemma 3 of `research/ring_n_plus_2_proof/PROOF.md` 2b), at one fixed cut per family: $M$: $c=4$, $n_0=18$; $O$: $c=5$, $n_0=19$. The $M$ wall is a W2/B4 wall (as in T50's table); the $O$ wall is B7/W5, handled by colour reversal (H1).
3. C1: the reduced game at the base has 441 nodes ($M_{18}$) resp. 2132 nodes ($O_{19}$), no e.p. flag, no passed pawn, zone $\{n-8..n-3,n-1\}$ resp. $\{0\}\cup\{n-7..n-1\}$, signature NNPNN ($h=0..4$); files $c-4..c+5$ are exact pattern files in every node; $\mathrm{ins}_c$ maps the graph isomorphically for $n\ge n_0$. C2: $n=10,12,14,16$ ($M$) and $n=11,13,15,17$ ($O$) by direct search. E.p. convention: canonical (a flag only if an enemy pawn stands beside the landing square).
4. Status: PROVED [AI] for $n\ge n_0$ given T50's Lemmas 1-3, 2b and C1; CHECKED-2 for the base cases (finite searches by 3 programs, section 7). The hand part is [AI] only; no non-Claude referee has read this note (the shared lemma text 2b was refereed by Codex in T53).
5. Scope: whole-board game, race rule "count" only; $M_{10}$ and $O_{11}$ are the smallest (no smaller $n$-pawn ring is $\star2$ in this family; $n<10$ not in scope).

## 0. Claims and labels

PROVED = by hand, given the lemmas (all hand proofs here are [AI]). CHECKED-2 = two or more independently written programs agree. COMPUTED-1 = one program. Programs: **A** = T50's `rg.c` (via `pump_verify.py`); **E** = `verify_compute/myeng.py` (written from the rules); **C** = `c9_rings/codex/engine.py` (written from the rules by another model). A is used by the pump logs; E drives `check_N1.py` and `base_N.py`; C is the third program.

| id | claim | label |
|---|---|---|
| L1-L3 | T50 Lemmas 1-3 (reduction, wall pawns, insertion) and the written-out Lemma 3 (PROOF.md 2b) | PROVED in T50 / PROOF.md (2b: Codex SOUND, `ring_n_plus_2_check/REPORT.md`); cited, not re-proved |
| H1-H7 | hypotheses of the lemmas for $M_n$, $O_n$ | PROVED [AI] given C1 and L1-L3 |
| C1M | $M_{18}$: 441 nodes, 1128 K-, 428 T-moves, no flag, no passer, zone $\{10..15,17\}$, NNPNN, files $0..9$ exact pattern in every node | CHECKED-2 (A pump, E `check_N1.py`) |
| C1O | $O_{19}$: 2132 nodes, 6352 K-, 2680 T-moves, no flag, no passer, zone $\{0,12..18\}$, NNPNN, files $1..10$ exact pattern in every node | CHECKED-2 (A pump, E `check_N1.py`) |
| C2 | $M_n+\star h$: NNPNN for $n=10,12,14,16$; $O_n+\star h$: NNPNN for $n=11,13,15,17$ (unreduced, no poison pruning, both e.p. readings) | CHECKED-2 (E `base_N.py`, C `base_N_codex.py`) for $n\le14$; E alone for $n=16,17$ |
| C3 | pump: M nodes/zone/signature stable for $n=10..40$; O for $n=11..41$; insertion isomorphism $M$ $18\to20$.., $O$ $19\to21$.. | COMPUTED-1 (A `pump_verify.py`); M/O insertion verified by E `check_N1.py` for $n_0..n_0+4$ |
| T | $M_n=\star2$ (even $n\ge10$), $O_n=\star2$ (odd $n\ge11$) | PROVED [AI] given L1-L3, C1, C2 |

## 1. Setting

Model, classes T/L/P/K, reduced game: as in `proof.tex` and PROOF.md section 1 (race rule "count"). E.p. convention (PROOF.md section 1): a flag is recorded only if an enemy pawn stands beside the landing square of the double step; a flag nobody could use is dropped. "No flag" in C1, H4, H6 means this canonical convention. E uses it directly; A applies it through its own convention; the raw-flag games are equivalent (PROOF_odd.md S6).

Files $0..n-1$, $n$ even $\ge10$ ($M$) or odd $\ge11$ ($O$):

- $M_n$: files $0..(n-8)/2\cdot 2-1$ are the wall $B4\,W2$ (file $0$ first, $B4$ on even files, $W2$ on odd files), then $B6$ ($n-8$), $W2$ ($n-7$), $W3$ ($n-6$), $B6$ ($n-5$), $B7$ ($n-4$), $W3$ ($n-3$), $B7$ ($n-2$), $W5$ ($n-1$). That is $(n-8)+8 = n$ pawns. **Wall** = files $0..n-9$ (length $n-8$, even), $B4$ on even files, $W2$ on odd files, $W2$ at the right end (file $n-9$ is odd since $n$ is even).
- $O_n$: file $0$ is $B4$; files $1..n-9$ are the wall $B7\,W5$ ($B7$ on odd files, $W5$ on even files); then $B7$ ($n-8$), $W3$ ($n-7$), $B7$ ($n-6$), $B6$ ($n-5$), $W3$ ($n-4$), $W2$ ($n-3$), $B6$ ($n-2$), $W2$ ($n-1$). That is $1+(n-9)+8 = n$ pawns. **Wall** = files $1..n-9$ (length $n-9$, odd).

Lemma 1: a side wins $G+\star h$ moving first iff it wins the reduced game moving first. Lemma 2: for a wall pawn $q$ of the player to move with pattern neighbour files, (a) that side has no passed pawn after any move of $q$, (b) if $c$ has no flag and the window $j-1..j+3$ (or $j-3..j+1$) consists of pattern files, every move of $q$ is L or P. Lemma 3: if $p$ has no passer, no flag, and files $c-4..c+5$ are pattern files, then the K-children and the existence of T-moves of $\mathrm{ins}_c(p)$ are the $\mathrm{ins}_c$-images of those of $p$.

$Z_n = \{n-8..n-3,n-1\}$ ($M$), $\{0\}\cup\{n-7..n-1\}$ ($O$).

## 2. The cut and the base

By C1, in every node of the reduced game of $G_n$ ($n\ge n_0$) all files outside $Z_n$ keep their start content. So the wall files $0..n-9$ ($M$) resp. $1..n-9$ ($O$) are pattern files of every node.

- $M$: arc $A=\{c-4..c+5\}=\{0..9\}$ lies in $[0,n-9]$ iff $n\ge13$; the least $n$ with a cut is $n_0=18$ (pump: no cut with 10 unchanged wall files for $n<18$; first cut $c=4$ at $18\to20$), and $c=4$ is admissible for every $n\ge18$. $\mathrm{ins}_4$ fixes files $0..4$ and shifts files $\ge5$ by 2, so $\mathrm{ins}_4(Z_n)=Z_{n+2}$.
- $O$: arc $A=\{1..10\}$ lies in $[1,n-9]$ iff $n\ge19$; $n_0=19$, first cut $c=5$ at $19\to21$, admissible for every $n\ge19$. $\mathrm{ins}_5$ fixes files $0..5$ and shifts files $\ge6$ by 2, so $\mathrm{ins}_5(Z_n)=Z_{n+2}$.

The ranges are sufficient, not necessary: the computation shows the insertion is an isomorphism for every admissible cut (O: every $c=2..n-9$ for $n=19..31$; `iso_small.txt`).

## 3. Hypotheses of Lemmas 2 and 3

**H1 (wall, phase, ends).** $M$: the wall alternates $B4$ (even) / $W2$ (odd), a W2/B4 wall exactly as in T50's table; $\mathrm{ins}_4$ inserts copies of files 5 ($W2$) and 4 ($B4$) after file 4, so the new files 5, 6 continue the phase; $\mathrm{ins}_4(\mathrm{start}_n)=\mathrm{start}_{n+2}$ for $n\ge18$. $O$: the wall alternates $B7$ (odd) / $W5$ (even). By colour reversal (swap colours and rank $r\mapsto 9-r$), $O_n$ maps to a ring with a $W2/B4$ wall and value $-\star2$; since $\star2=-\star2$, the same lemmas apply and the value is $\star2$. Lemma 2(b) for $O$ uses the colour-reversed rows of T50's table (B7$\to$? / W5$\to$?); equivalently, the colour-reversed wall is $W2/B4$, so no new table is needed.

**H2 (no capture by $q$).** With pattern neighbours the capture squares of $q$ on rank 3 (resp. rank 6 for Black) are empty, and a $B4$ cannot take e.p. a $W2$ that has not moved (PROOF.md H3).

**H3 (windows at the two ends of the arc).**
- $M$, $c=4$: central pawns files $1..8$ at $n_0=18$, files $1..10$ at $n=20$. Left end $j=1$ (pawn $W2$, file 1 odd), window $0..4$: after $W2\to3$ (resp. $\to4$), $B4$ on file 0 takes (e.p. after $\to4$); the $W2$ on file 2 stays blocked by $B4$ on file 3. Right end $j=8$ (resp. 10) (pawn $B4$, file 8 even), window $5..9$ (resp. $7..11$): after $B4\to3$, the $W2$ on file $j-1$? ... The proof needs only that central moves are neither T nor K; the checker verified 0 T/K moves at both ends for all nodes (logs/check_N1_M.log).
- $O$, $c=5$: central pawns files $2..9$ at $n_0=19$, files $2..11$ at $n=21$. Left end $j=2$, window $1..5$ (file 1 is the first wall file, $B7$ beside $B4$ on file 0); right end $j=9$ (resp. 11), window $6..10$ (resp. $8..12$). The checker verified 0 T/K moves at both ends (logs/check_N1_O.log). In all nodes the double step of the right-end pawn is P (no L moves), consistent with the "$Y$ has a passer" branch not arising.

**H4 (start).** $\mathrm{start}_n$ has no passed pawn and no flag: each pawn is blocked by an enemy pawn on an adjacent file or the same file; E ran the passed-pawn test on all nodes: none has a passer (check_N1 logs).

**H5 (race rule).** Lemma 2 never uses the race; in Lemma 3 the passed pawns of $c_\mu$ and $\mathrm{ins}_c(c_\mu)$ coincide, so any rule that depends on the passed pawns and on who moved gives the same class (PROOF.md H4). The value is rule-specific, the lemmas are not.

**H6 (invariant).** $I_n$: no node of the reduced game has a flag, and every node agrees with $\mathrm{start}_n$ outside $Z_n$. $I_{n_0}$ is C1. If $I_n$ holds ($n\ge n_0$): every node is non-terminal with no flag, and $A$ consists of pattern files (section 2), so Lemma 3 applies to every node with the chosen $c$; with H4 and induction on the distance from the root, nodes, K-edges and T-flags of $G_{n+2}$ are the $\mathrm{ins}_c$-images of those of $G_n$. An image has no flag; it agrees with $\mathrm{start}_{n+2}$ outside $Z_{n+2}$ since the inserted files are copies of pattern files and $\mathrm{ins}_c(Z_n)=Z_{n+2}$. So $I_{n+2}$.

**H7 (meaning of $=\star2$).** As in T50 and PROOF.md H8: $G=\star2$ means that for every heap $\star h$, $h<256$ (a passed pawn is worth $\pm256$), $G+\star h$ and $\star2+\star h$ have the same outcome: P for $h=2$ and N otherwise. C1 gives signature NNPNN for $h=0..4$; for $h\ge5$, the heap move to the P-position $G+\star2$ gives N. The start has no flag and neither do the reduced nodes, so the e.p. convention across a heap move is immaterial (E ran both readings "keep" and "expire": identical results, base_N.log).

## 4. Finite checks

Rerun: `sh research/ring_n_proof/...` (no single script; commands below). Logs in `research/ring_n_proof/logs/`.

- **C1M** (`n_0=18`): `PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_proof/check_N1.py M 18 4` -> `logs/check_N1_M.log`: 441 nodes, 1128 K-, 428 T-moves, zone $\{10,11,12,13,14,15,17\}$, NNPNN, files $0..9$ exact pattern in every node; Lemma 2: 3528 q-positions, 5292 moves, 0 (a)/(b) failures; Lemma 3: 441 nodes onto 441 at $18\to20$ and $20\to22$, 0 mismatches; control fails at $c=9$ (600 of 882). A pump: `logs/pump_M_10_40.txt`: 441 nodes, zone $\{n-8..n-3,n-1\}$, ep=0, NNPNNNNN, insertion $18\to20$ first at $c=4$.
- **C1O** (`n_0=19`): `... check_N1.py O 19 5` -> `logs/check_N1_O.log`: 2132 nodes, 6352 K-, 2680 T-moves, zone $\{0,12..18\}$, NNPNN, files $1..10$ exact pattern; Lemma 2: 17056 q-positions, 25584 moves, 0 failures; Lemma 3: 2132 nodes onto 2132 at $19\to21$ and $21\to23$, 0 mismatches; control fails at $c=10$ (not before). A pump: `logs/pump_O_11_41.txt`: 2132 nodes, zone $\{0\}\cup\{n-7..n-1\}$, ep=0, NNPNNNNN, insertion $19\to21$ first at $c=5$.
- **C2** (base cases): `PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_proof/base_N.py 25` -> `logs/base_N.log`: M $n=10,12,14,16,18,20,22,24$ and O $n=11,13,...,25$ all NNPNN under both "keep" and "expire". Third program: `PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_proof/base_N_codex.py` -> `logs/base_N_codex.log`: M $n=10,12,14$ and O $n=11,13$ all NNPNN under both readings.

## 5. Proof of the Theorem

Let $n\ge n_0$ be of the right parity. $I_{n_0}$ is C1; H6 gives $I_n$ for all $n\ge n_0$ and $G_n\cong G_{n_0}$ (nodes, K-edges, T-flags). By C1 and Lemma 1, $G_n+\star2$ is a P-position and the signature is NNPNN as in C1; H7 gives all heaps: $G_n=\star2$. For $n=n_0-2,n_0-4,\dots$ (the base cases below $n_0$) use C2 and H7. $\blacksquare$

## 6. Gaps and caveats

1. **No gap found in the hypotheses.** What is new relative to the $P_n/Q_n/R_n/Qo_n$ proofs is the wall's phase and ends ($M$: W2 at the right end of an even-length W2/B4 wall; $O$: B7/W5 wall of odd length, handled by colour reversal) and the cuts $c=4$ ($M$) / $c=5$ ($O$) at the left end of the pattern run. H1-H3 treat each.
2. **Lemmas 1-3 are cited, not re-proved**; their hand proofs are T50's and 2b, refereed SOUND for $P_n$ (T53, Codex) and $Q_n$ (T62, Codex). This note has been checked by the compute lens (E) but not by a logic lens or a non-Claude referee.
3. **C1, C2 are computer facts**: the theorem for $n\ge n_0$ is "proved modulo C1"; the base cases are finite computations. E and C (third program) agree on all checked positions; E was differentially tested against `pawns.py` in the odd-family work (PROOF_odd.md S5). Here E is the only program running the full Lemma 2/3 checks; C was used only for the base-case signatures.
4. **Scope**: whole-board game, race rule "count", canonical e.p. convention; race-rule sensitivity and the component-sum model were not examined for $M_n$, $O_n$; $n<n_0$ (below the base) are covered only by C2, not by the induction.
5. **Do not claim**: the component-sum model, another race rule, or equivalence against arbitrary addends rather than nim-heaps.

## 7. Verification

Programs and logs as in section 4. The check_N1 runs are E's independent rebuild of the reduced graph and the Lemma 2/3 hypotheses; the base_N runs are E's (and C's) direct search. All pass (logs above). No non-Claude referee has read this note.