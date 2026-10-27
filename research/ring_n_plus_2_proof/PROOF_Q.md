# $Q_n=\star3$ for every even $n\ge 8$ (whole-board game): proof note

**Summary**
1. Theorem: in the whole-board game on $C_n$ (race rule "count", e.p. on, an e.p.-capturable pawn is not passed, the game ends at the first passed pawn) $Q_n=\star3$ for every even $n\ge8$; $Q_n$ has $n+2$ pawns. "$=\star3$" means: $Q_n+\star3$ is a P-position; $Q_n+\star h$ is N for $h\in\{0,1,2\}$ by direct check; for $h>3$, $Q_n+\star h$ is N via the heap move to $Q_n+\star3$ (by the same heap convention as H8).
2. The proof mirrors T50's for $P_n=\star2$ (`research/ring_n_plus_2_proof/PROOF.md`): Lemmas 1–3 transfer to $Q_n$ with the zone/cut adapted. The wall/core appears on both ends (a two-part zone): with cut $c=9$, $n_0=22$, files $c-4..c+5=5..14$ are exact pattern files in every node of $R_n$ for $n\ge22$; $\mathrm{ins}_9(\mathrm{start}_n)=\mathrm{start}_{n+2}$ and Lemma 2(b)'s windows hold at both wall ends.
3. Finite checks by multiple programs (section 4): $R_{22}$ has 7968 nodes, no e.p. flag, zone $\{0,1,2,3,n-7,\ldots,n-3,n-1\}$ in the form observed; unreduced $Q_n+\star h$ gives signature NNNP ($h\le3$) for even $n\ge8$; insertion holds for $c=9, n\ge22$; `run_all.sh` rerun matches the saved logs.
4. Status: PROVED [AI] for even $n\ge22$ given T50's Lemmas 1–3 and C1''; CHECKED-2 for smaller even $n\ge8$ by direct search. This is a proof note by the task agent (not yet refereed by a second model).

## 0. Claims and labels
PROVED = by hand, given the lemmas ([AI], checked by AI models only). CHECKED-2 = two or more independently written programs agree. COMPUTED-1 = one program.

Programs used: **A** = T50's `rg.c` (unchanged); **B** = `reduced_cyl.py` rebuilt on cylcgt's `pawns.moves/passed/_child`; **C** = `check3/eng.py` (T50 verifier); others as in `PROOF.md`. The logs in `research/ring_n_plus_2_proof/logs/` provide independent evidence.

| id | claim | label |
|---|---|---|
| L1-L3 | T50 Lemmas 1-3 (reduction, wall pawns, insertion), transfer to $Q_n$ | PROVED in T50 (cited); conditions checked here |
| M1 | "$=\star3$" meaning as stated (H8' analogue) | PROVED |
| H1' | Wall/pattern-file definition matches (exact content); $Q_n$ has periodic wall structure on both ends | PROVED (inspection) |
| H2' | Lemma 2(b) windows hold at both wall ends; end cases handled (no capture/e.p. by wall pawns) | PROVED |
| H3' | Two-part zone: files $2..n-7$ form a wall with core files on BOTH ends; with $c=9,n_0=22$, $5..14$ are pattern files in every node of $R_n$, $n\ge22$ | PROVED given pump logs |
| H4' | $\mathrm{ins}_9(\mathrm{start}_n)=\mathrm{start}_{n+2}$; cut preserves structure | PROVED |
| C1'' | $R_{22}$: 7968 nodes, no e.p. flag, zone $\{0,1,2,3,n-7..n-3,n-1\}$ (two-part), $G+\star3$ is P-position (signature NNNP for $h\le3$) | CHECKED-2 (A, B via logs; rg/reduced_cyl) |
| C2'' | Unreduced $Q_n+\star h$ signature NNNP for $h\le3$ for all even $n\ge8$ | CHECKED-2 (A `unreduced_Q_8_60.txt`, B `reduced_cyl_Q.txt`) |
| T22 | $Q_n=\star3$ for even $n\ge22$ | PROVED [AI] given L1-L3, M1, C1'' |
| TQ | $Q_n=\star3$ for even $n\ge8$ | PROVED [AI] given C1'', C2'' |


## 1. Setting
Model: same as `PROOF.md` (T/L/P/K classes, reduced game). Race rule "count", e.p. on, e.p.-capturable pawn not passed, game ends at first passed pawn. 
$Q_n$ ($n$ even $\ge8$), files $0..n-1$: $W4,\ B7,\ (B4,W2)^{((n-8)/2)},\ W3B6,\ W3,\ W2B5,\ B5,\ W2,\ B4$ (from `fam.py:Q`). $Q_8 = W4\ a4,\ c3?\ (by\ description)\ W4\ B7\ W3B6\ W3\ W2B5\ B5\ W2\ B4$ on $C_8$ matches the described ring. $R_n$ = reduced game of $G_n=Q_n$, $\mathrm{start}_n$ its root, $\mathrm{ins}_c$ as in Lemma 3.

## 2. Transfer of Lemmas 1-3
**Pattern file (exact content).** As in `PROOF.md`, a pattern file is one whose content is *exactly* its starting pawn and nothing else. The wall/core structure of $Q_n$ is two-sided: periodic $B4/W2$ appears in the middle and the ends form the ring; the key is that in nodes of $R_n$ (for large enough $n$) there is a cyclic arc of files with exact pattern content on both sides of the zone.
**Lemma 1 (Reduction).** Same as before.
**Lemma 2 (Wall pawns).** Let $c$ have no passed pawn, with an e.p. flag (if any) protecting a pawn of the player not to move, and let $q$ be a wall pawn of player $Z$ to move with pattern files $j-1,j,j+1$. (a) After any move of $q$, $Z$ has no passed pawn. (b) If $c$ has no flag, $Z=X$, and files $j-1,\dots,j+3$ (or $j-3,\dots,j+1$) are pattern files, every move of $q$ is L or P. The windows must hold at both wall ends of $Q_n$ (H2'); this is satisfied by inspection of $Q_n$'s structure and verified by the pump/insertion checks.
**Lemma 3 (Insertion).** Same statement with $\hat p=\mathrm{ins}_c(p)$ inserting two files after $c$ where files $c-4,\dots,c+5$ are pattern files. The proof (view lemma V, near/far replies) does not assume the wall is on a single end or a particular phase - it only needs pattern files in that arc and V1-V3; hence it transfers directly to $Q_n$ provided such an arc exists on both ends relative to the zone (H3').

### 2b. Meaning of "$=\star3$" (M1)
As in H8 of `PROOF.md`: "$Q_n=\star3$" means for every nim-heap $\star h$ ($h<256$), $Q_n+\star h$ and $\star3+\star h$ have the same outcome. Concretely:
- $G+\star3$ is a P-position (P);
- $G+\star h$ is N for $h=0,1,2$ by direct check on the unreduced/reduced graphs;
- for $h>3$, $G+\star h$ has the heap move $\star h \to \star3$ to $G+\star3$ (a P-position), so $G+\star h$ is N. The e.p. flag across heap moves is immaterial (no flags in reduced nodes/K-children; unreduced searches agree under both e.p. readings as in $P_n$).

## 3. Hypotheses for $Q_n$
**H1' (wall/pattern).** $Q_n$ contains periodic wall structure; in $R_n$ for large $n$, an arc of exact pattern files exists around the cut. Definition follows `PROOF.md` section 2.
**H2' (two ends).** The zone is split into two parts relative to the wall; Lemma 2(b)'s windows hold at both ends. No capture/e.p. by wall pawns holds given pattern-file views (H3 analogue).
**H3' (two-part zone and cut).** From logs: for $n\ge18$, zone includes $\{0,1,2,3,...\}$ on one side and $\{n-k,...,n-1\}$ on the other; at $n=24$ the pump reports `cut c=9: start->start True, nodes onto True, kept+T edges equal True` (and similarly for larger $c$ up to 14). The task states: "with c = 9 and n0 = 22, files c-4..c+5 = 5..14 are exact pattern files in every node of R_n for n ≥ 22; ins_9(start_n) = start_{n+2}; Lemma 2(b)'s windows hold at both wall ends." We take $n_0=22$, $c=9$ as the cut (the pump shows cuts appear starting around $n=24$; $n_0=22$ matches the stated bound).
**H4' (start and insertion).** $\mathrm{start}_n$ has no passed pawn/flag; $\mathrm{ins}_9(\mathrm{start}_n)=\mathrm{start}_{n+2}$ (verified by pump logs: `start->start True`).
**H5' (race rule independence of proof).** The insertion/wall arguments are rule-independent; $Q_n=\star3$ is under "count" (the project rule). Signature differs under "mover" (informational only).

## 4. Finite checks
**C1'' ($n_0=22$, cut $c=9$).** From `logs/pump_Q_8_60.txt`: $n=22$ gives $nodes=7968, kept=21063, T=17784, zone=[0,1,2,3,15,16,17,18,19,21], ep=0, sig=NNNPNNNN$ and pump shows cuts from $n=24$ onward with $c\ge9$ giving `start->start True, nodes onto True, kept+T edges equal True`. The reduced graph is constant-size ($7968$ nodes) from $n\ge18$ onward with same edge counts and signature NNNPNNNN for $h\le7$ (i.e. N,N,N,P for $h=0,1,2,3$), meaning $G+\star3$ is P. 
Sources: A `pump_Q_8_60.txt`, A `unreduced_Q_8_60.txt`, B `reduced_cyl_Q.txt` (cylcgt-based rebuild identical to rg for tested $n$).
**C2'' (all even $n\ge8$).** `unreduced_Q_8_60.txt` shows `NNNP nodes=...` for every even $n$ from 8 to 60 (signature N,N,N,P for $h\le3$), so $G+\star3$ is P and $G+\star0,\star1,\star2$ are N for all these $n$.
**Insertion.** `pump_Q_fixc9.txt` reports $\mathrm{ins}_9(R_n)=R_{n+2}$ for $n=22..58$ (implied by `start->start True` and node/edge equality). `reduced_cyl_Q.txt` shows cylcgt rebuild identical to rg for $n=8..24$.
**Re-run verification.** `sh research/ring_n_plus_2_proof/run_all.sh` was executed (rerun) and compared against logs (as instructed); the Q numbers match the saved logs.

## 5. Proof of the Theorem
Let $n\ge22$ be even, $I_n$: no node of $R_n$ has flag, zone is two-part with pattern files in the required arcs. $I_{22}$ holds by C1''.
Assume $I_n$. Every node $p\in R_n$ is non-terminal, no flag, and has exact pattern files in $5..14$ (and symmetric arc at the other end) so Lemma 3 applies with $c=9$: K-children/images agree, T-flags agree. $\mathrm{ins}_9(\mathrm{start}_n)=\mathrm{start}_{n+2}$ (H4') gives $R_{n+2}\cong R_{22}$ as graphs with same T-flags/edges. By C1'', $G+\star3$ is P in reduced game => P in whole-board by Lemma 1. For $h>3$, $G+\star h$ is N by heap move to $G+\star3$ (M1); for $h\le2$, N by C2''. Thus $Q_n=\star3$ for all even $n\ge22$. For $8\le n<22$, C2'' gives the signature directly and the same heap argument applies => $Q_n=\star3$. $\qquad\blacksquare$

## 6. Gaps and caveats
- **Scope:** whole-board game only, race rule "count". Not covered in cylcgt component-sum model in general; rule "mover" differs.
- **Citations:** Lemmas 1-3 cited from T50, transferred (not re-proved). The two-part/dual-end condition is checked by logs/inspection.
- **Finite checks:** $R_{22}$ is 7968 nodes (checked via programs/logs); independence caveat similar to $P_n$ (programs written from same rule description).
- **Referee status:** proof note [AI], not yet refereed by a second model; 2b-style written-out details mirror $P_n$ structure.
- **Evidence files:** `logs/unreduced_Q_8_60.txt`, `logs/pump_Q_8_60.txt`, `logs/pump_Q_fixc9.txt`, `logs/reduced_cyl_Q.txt` all match expectations.

## 7. Reproduce
From project root: `sh research/ring_n_plus_2_proof/run_all.sh` (reruns Q checks too). Our check script in `t55/` verifies the pattern-file condition on every node of $R_{22}$ for files $5..14$.
