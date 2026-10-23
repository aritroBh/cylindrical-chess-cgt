# T51 referee report: ring family proof (T50, `research/ring_family_proof/proof.tex`)

## 5-line summary
- I re-read `proof.tex` line by line and reproduced every computational claim by re-running `run_all.sh quick` (logs saved in `logs_reproduced/`); all numbers match the paper.
- An independent Python check using only `cylcgt.pawns.Board/Pos.parse/passed` plus a hand-written move generator found **0 exceptions** among 37 wall-pawn moves (incl. double steps) for O_n/E_n, n≤13.
- Lemma 1 (Reduction), Lemma 2 (Wall pawns), Lemma 3 (Insertion), the induction and finite checks are all **SOUND** as written; no mathematical gap found.
- Minor presentational gaps only: Lemma 2(b)'s table lists only forward steps (capture moves are impossible under the pattern window but this is not stated), and Lemma 3(iii) invokes Lemma 2(a) without restating the no-flag invariant it relies on.
- Overall verdict: **SOUND**. The claim "O_n and E_n are *2 for all n" survives this referee pass.

## 1. Reproduced computational claims

Re-run command (from project root, under `nice -n 15`):
`nice -n 15 sh research/ring_family_proof/run_all.sh quick > research/ring_family_proof_check/run_all_stdout.log 2>&1`
(PID 47133; completed; regenerated logs in `logs_reproduced/`.)

| Claim in `proof.tex` | Reproduced |
|---|---|
| O base graph 144 nodes | `odd n=17: 144 nodes` (`reduced_cyl_odd.log`) |
| E base graph 104 nodes | `even n=16: 104 nodes` (`reduced_cyl_even.log`) |
| edges 209/246 (O), 177/97 (E) | `kept=209 T=246` / `kept=177 T=97` (`pump_odd_c9.log`, `pump_even_c8.log`) |
| Lemma 2: 923607 wall-pawn moves, 0 not L/P | `Lemma 2(b): 923607 ... not L/P: 0` (`lemma2.log`) |
| Lemma 2(a): 960830 moves, 0 mover passer | `Lemma 2(a): 960830 ... mover obtains a passed pawn: 0` (`lemma2.log`) |
| Lemma 3 stress: 15840 (O) / 11440 (E) node-cut pairs, 0 mismatches | `15840 ... mismatches 0` / `11440 ... mismatches 0` |
| pumping 17→61 (O), 16→60 (E) | last lines `n=61` / `n=60`, `start->start True, nodes onto True, kept+T edges equal True` |
| 113 rings up to n=61, none not *2 | `total 113 rings, not *2: 0` (`fullsweep.log`) |
| reduced game value *2 at n0 | `odd n=17: ... value *2`, `even n=16: ... value *2` (`reduced_value.log`) |
| C engine == cylcgt graph at n0 | `identical: True` for both (`reduced_cyl_*.log`) |
| no e.p. flag in any node at n0 | `rg reduce` on `odd(17)` contains no `ep` token (checked) |

All reproduced numbers agree with `proof.tex`. No discrepancies found.

## 2. Independent check (step 3)

Script: `research/ring_family_proof_check/independent_check.py`.
Uses only `cylcgt.pawns.Board`, `Pos.parse`, `cylcgt.pawns.passed` (ep-aware, default) and a hand-written pawn move generator. Does **not** use `rg.c` or `cylcgt` game-value code.

For O_n (n = 5,7,9,11,13) and E_n (n = 6,8,10,12), for each side to move, for each wall pawn whose files j-1..j+3 or j-3..j+1 are wall files (pattern window), every legal move of that pawn was enumerated (37 moves total, including 6 double steps / ep cases). For each:
- (2a) mover has no passed pawn in the child: **0 violations**.
- (L/P) opponent either already has a passed pawn (L) or has a capture (including ep capture) yielding an opponent passed pawn with mover none (P): **0 violations**; 0 L, 37 P; every poisoning reply was a capture.

Result: `Total exceptions: 0` (`independent_check.txt`).

## 3. Lemma verdicts

### Lemma 1 (Reduction) — SOUND
T/L/P/K classification and deletion of L/P moves is standard finite-game reasoning; `lab{P}`. No gap found. Verified computationally by `reduced_value.py` (canonical form of the reduced game is *2, independent of the outcome search).

### Lemma 2 (Wall pawns) — SOUND
- 2(a): ep-lapsing and the white 2→4 step landing beside a B4 are handled; independent check (incl. double steps) gives 0 violations of the "mover has no passed pawn" claim.
- 2(b): the "two ranks further on" geometry gives the opponent a pawn on j±1 that can capture; the capture lands on file j, where files j-1,j,j+1 hold no pawn of the mover (verified for both step and double-step/ep cases, 0 exceptions). The one mover pawn on j+2 (resp. j-2) remains blocked by the opponent pawn on j+3 (resp. j-3).
- Minor presentational gap: the table lists only the five forward step moves and omits capture moves by q; under the pattern window q has no legal capture (adjacent files hold opponent pawns two ranks further, not on the capture square), but this should be stated. Not a mathematical gap.
- Lemma 2 also assumes the mover is the player X with the pattern window on the correct side; the "or" covers the mirror window by symmetry; the proof text only writes the j+1 reply but the intended mirror is clear.

### Lemma 3 (Insertion) — SOUND
- The stress test found 0 mismatches across 15840 (O) and 11440 (E) (node, cut) pairs.
- 3(iii): replies by pawns on files c-1..c+2 and inserted pawns never win for Y because each such pawn is a wall pawn satisfying Lemma 2(a) (pattern files c-2..c+3 hold in c_μ), so Y gets no passed pawn from that reply; and the no-flag invariant (C1 + induction) supplies the flag condition Lemma 2(a) needs. A referee should note that this reliance on the no-flag invariant is implicit in the text.
- Race (count rule) subtlety: a reply could in principle create a race only if both sides ended with passers; since Y gets no passer (Lemma 2(a)), no race win for Y arises. Consistent.

### Induction (Proof of Theorem) — SOUND
Files c-4..c+5 (5..14 O, 4..13 E) are outside the zone {n-1,0,..,4/3} for n≥n0 and are pattern files in every node (C1 for n0; insertion preserves them). No-flag invariant preserved by insertion. Reduced games of one parity are isomorphic to the n0 graph; by Lemma 1 and C1, G_n + *2 is P, so G_n = *2. Small n handled by C2.

### Finite checks C1, C2 — REPRODUCED (see table)
144/104 nodes; no flags; zones as stated; *2 at n0 by two independent routes (outcome search and cylcgt canonical form); all n≤61 (113 rings) give *2.

## 4. Conclusion
No gap found that affects the theorem. The proof is **SOUND**; the minor items above are presentational and do not change any claim. Every number in `proof.tex` was reproduced by an independent re-run, and the Lemma 2(b) claim (including ep double steps) was verified independently on n≤13 with 0 exceptions.