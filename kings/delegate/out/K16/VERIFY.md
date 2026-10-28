# K16 referee report (K16v)

Verdict: ACCEPT_WITH_FIXES. The negative result (the real-king square rule is false as stated) reproduces under three
independent implementations. Theorem 2.11K has no gap that I could find and no counterexample in about 1.1 million
exhaustive and 16,500 random checks. Three text points in EDITS.md need fixing before integration (section 4); the
large sweeps (up to 1.4 * 10^8 positions) I could not re-run and they stay COMPUTED-1.

All code below is mine, written from the rules in LOOPY and not from K16's scripts: `verify/mine.py` (P-model solver,
own retrograde analysis), `verify/cert.py` (own certificate H1, H2, H4, H5K, SQ, NS by simulation, H3K, H3),
`verify/sweep.py` (own exhaustive enumeration, beta = White), `verify/gen.py` (random sampler), `verify/cmp.py`,
`verify/ctl.py`, `verify/vs.py`. The only K7/K16 code used as a tool is the private `kpp` build (kp_p.c, `--pmodel`) as
the second P solver. K16's `chk.c` was compiled (as `theirchk`) once, only to diagnose a count mismatch that turned out
to be my own bug (section 2.3); it was not used to confirm anything.

## 1. Counterexamples (claims 1 and 2): CONFIRMED, CHECKED-2 (now three solvers)

Reproduce (from `kings/delegate/out/K16/verify/`; `kpp` = `cc -O2 -o kpp ../../K7/scripts/draft/kp_p.c -lpthread`,
`kp` = `cc -O2 -o kp ../../../../kpsolve.c -lpthread`):

    printf 'Ka4 ka6 Pa5 Pd5 b -\n' | ./kpp --board cyl:6x6 --pmodel                      # D D
    printf 'Kc1 ka1 Pc2 pa2 w -\nKc1 ka1 Pc2 pa3 w -\nKd2 kf1 Pa2 Pf3 pf2 pd3 w -\n' | ./kpp --board flat:6x6 --pmodel   # D D each
    printf 'Ka1 ka6 Pc2 w -\n' | ./kp --board cyl:8x6 --frozen      # W W ;  ./kpp ... --pmodel gives D D
    PYTHONPATH=<repo> python mine.py cyl:6x6 < (same positions)      # my own solver: D for all five

Results: all five positions give the claimed values with kp_p, with my own solver `mine.py` (D; the cyl:8x6 `Ka1 ka6 Pc2`
position is D with real kings and W W frozen; exact chess D D as in LOOPY). My own certificate `cert.py` accepts the
named pawn in the four counterexamples (cyl:6x6: p = d5, e = 1, d = 1; flat:6x6 `Kc1 ka1 Pc2`: p = c2, e = 2, d = 3; the
fourth: p = a2 and p = f3) and the strategy simulation finds an omega stalemate line in each; it does not certify
`Ka1 ka6 Pc2 w -` on cyl:8x6 (SQ fails at q_2 = c5: d(a6, c5) = 2 < n_2 + 2 = 3), as claimed.
Hand check of the first: Black has no legal move at y itself (a6 king: a5 is guarded by Ka4, b6 and f6 are attacked
by Pa5 on the cylinder, b5 and f5 are adjacent to Ka4). So that example is a stalemate at y; the flat examples
`Kc1 ka1 Pc2 pa3 w -` (omega steers into the stalemate: c3 pa2 c4) and `Kd2 kf1 Pa2 Pf3 pf2 pd3 w -` (stalemate after the first
push) are genuine "walks into" cases.
Further, 31 positions drawn at random (6 per file of `viol_small/`, 7 files, only as inputs) were re-solved with
`mine.py` (all D) and re-certified with `cert.py` (each certified for exactly the stated pawn, each with an omega
stalemate line): 0 disagreements (`verify/vs.py`).

## 2. Counts (claims 3, 4, 6): reproduced exactly where I could re-run; the big sweeps are NOT_CHECKED

### 2.1 Exact agreement with K16's counts (my own enumeration, my own certificate, then kp_p on the stalemate-line positions)

Enumeration: beta = White, both sides to move, all kings, all legal e.p. rights, cylinder with beta's king on file a,
pawns restricted to files allowed by (H2) (a pure pruning, since (H2) is a hypothesis). Reproduce:
`python sweep.py <board> <maxW> <maxB> <outprefix> <bk-file-a 1/0> <shard> <nshards>` then
`./kpp --board <board> --pmodel < <outprefix>.cand | sort | uniq -c`.

| board, pawns (W+B, beta = White) | my certified positions | K16 | my positions with a stalemate line | of them kp_p non-wins | K16 violating |
|---|---|---|---|---|---|
| flat:6x6 <= 1+1 | 156,528 | 156,528 | 208 | 208 (all D D) | 208 |
| flat:7x6 <= 1+1 | 357,542 | 357,542 | 276 | 276 (all D D) | 276 |
| flat:6x6 <= 2+0 | 171,334 | 171,334 | 74 | 36 | 36 |
| cyl:6x6 <= 1+0 / 1+1 / 2+0 | 1,835 / 17,746 / 18,926 | same | 0 / 0 / 2 | 0 / 0 / 1 | 0 / 0 / 1 |
| cyl:6x6 <= 1+2 | 95,398 | 95,398 | 0 | 0 | (none listed) |
| cyl:6x6 <= 2+1 | 199,436 | 199,436 | 2 | 1 | (table: 1) |
| cyl:6x6 <= 2+2 | 1,072,469 | 1,072,469 | 2 | 1 (`Ka4 ka6 Pa5 Pd5 b -`; the other, `Ka4 ka6 Pa5 Pd4 w -`, is W W) | 1 |

(K16 numbers: `logs/small_exhaustive.txt`, `logs/aggregate_exhaustive_table.md`.) Also confirmed: "one pawn in all (1+0) never
violates" (flat 6x6 and 7x6, cyl:6x6), "1+1 violates on flat boards only", and the S0 numbers: of the 208 / 276 flat
violations, 58 / 74 have Black to move and no legal move at y, so 150 / 202 have a legal move at y (K16: S0 150 / 202),
i.e. "omega has a legal move at y" is not enough.
In every one of these sweeps the strategy "beta pushes p every turn" fails only through an omega stalemate (my
simulation reports kind `stalemate` for all 488 stalemate-line instances, never `other`).
cyl:6x6 <= 2+2 positive side: see section 3.

### 2.2 Not re-run (so NOT_CHECKED by me, remain COMPUTED-1 of K16)

cyl:6x6 <= 3+3 and <= 4+4 (19.4 M and 142 M certified), cyl:7x6 <= 3+3, cyl:8x6 <= 2+2, flat:6x6 <= 3+3, flat:7x6 <= 2+2 and
the KV 1 / KV 2 / S0 / S1 / S2 columns on them, the 175,454-position flip check, the 15,000-position pycert check.
My Python enumeration costs about 100 CPU-minutes for the smallest of them and the machine was at load 140.
The numbers that appear in EDITS.md for these are consistent with `logs/aggregate_exhaustive_table.md` and
`summary.json` (I re-added them; see 4.1 for the one arithmetic slip). The two nested families are not double counted in
the headline 7.6 * 10^8 (sum of the five top sweeps = 761,023,066 instances).

### 2.3 My own bug, for the record

My first cyl:6x6 <= 2+2 run gave 1,074,480 certified positions, 2,011 more than K16's 1,072,469. All 2,011 extra positions
carry an e.p. right whose pawn-origin or skipped square is occupied by a king (an impossible position); my enumerator
forgot the kings in its e.p. test. After fixing it the count is 1,072,469 exactly (and cyl:6x6 <= 2+1: 199,436 exactly).
K16's `cert` mode, which I ran only for this diagnosis, does not reject such positions, but K16's own enumerator does
not generate them (its `legal()` requires the origin and skipped squares to be free of kings). Nothing in K16's
counts is affected. (My random sampler `gen.py` had the same flaw: 3 of 16,500 sampled positions are impossible e.p.
positions that kp_p rejects with `X`; they are excluded below.)

## 3. Theorem 2.11K: no counterexample found (claim: PROVED)

Random test of "certified by (H1, H2, H4, H5K, SQ) and the strategy simulation finds no stalemate line (NS) implies beta
wins in P" with my own certificate, my own simulation of the strategy (all omega legal moves, real P rules), and kp_p
as the value oracle. beta random colour (about half of the samples have beta = Black), random e.p. rights, ranks and
files random (`gen.py`, `cmp.py`):

| board | max pawns per side | sampled certified positions | NS ok and kp_p beta win | NS ok, other | NS fail (stalemate) | NS fail but beta wins |
|---|---|---|---|---|---|---|
| flat:6x6 | 2 | 1,500 | 1,499 | 0 | 1 | 0 |
| flat:6x6 | 3 | 3,000 | 2,998 | 0 (+1 impossible e.p., rejected `X`) | 1 | 0 |
| cyl:6x6 | 3 | 3,000 | 3,000 | 0 | 0 | 0 |
| cyl:7x6 | 3 | 3,000 | 2,999 | 0 (+1 `X`) | 0 | 0 |
| flat:7x6 | 2 | 3,000 | 2,998 | 0 (+1 `X`) | 1 | 1 |
| cyl:8x6 | 2 | 3,000 | 3,000 | 0 | 0 | 0 |

Plus exhaustive: flat:6x6 <= 1+1: all 156,320 certified positions without a stalemate line are `W W` in kp_p (0 exceptions;
the other 208 are `D D`). flat:7x6 <= 1+1, flat:6x6 <= 2+0, cyl:6x6 <= 1+2, 2+1, 2+2: the stalemate-line positions are
exactly K16's (section 2.1); the positive side for cyl:6x6 <= 2+2: kp_p (through the shared lock, `verify/e_c66_22.vals`) on all 1,072,467 certified positions without a
stalemate line gives `W W` for every one (0 exceptions; a 10 percent subsample run earlier agreed).
(H3K) implies (NS): 0 exceptions in all samples (H3K held for 65-73 percent of the samples) and in all 488 certified
stalemate-line instances of the exhaustive lists (no one of them satisfies H3K or H3 at k_omega).
An example for the claim "a stalemate line does not always lose": my flat:7x6 sample contains a position with a stalemate line
and kp_p beta win (regenerate with `gen.py flat:7x6 2 24 3000 g_f76`, then kp_p and `cmp.py`; the line printed as `NSfail:stalemate betaWins`); this agrees with CONJECTURE'.

Proof, read step by step against the LOOPY definitions (setting, G_omega, H1-H5, F1-F3, Step 2 of Proposition 2.11):
* Step 1 (beta never attacked): by H2 and F1 no pawn ever stands on a file adjacent to beta's king, omega's king is
  never adjacent to it: OK.
* Step 2 (J_beta, J_omega, I1): the case analysis of Proposition 2.11 only uses pawn moves, H1, H4 and F1-F3. The new
  ingredient, omega's king capturing a beta pawn, removes a pawn and creates none, so every bound on landing ranks can
  only drop; (I1) is now stated for pawns only and the kings are handled in Step 3. One wording point: Steps 2 and 3
  use each other (Step 2 assumes p is alive, Step 3 shows the king never takes it); it is an induction on plies and
  should say so in one phrase (see 4.4). No gap.
* Step 3 (king neither captures nor blocks): the count n_j of omega moves before the j-th push is right for both
  move orders (checked: s = omega n_j = j, s = beta n_j = j - 1); capture needs d(k_omega, q_j) <= n_j + 1, blocking q_(j+1)
  needs d <= n_(j+1); the skipped square of the double step is adjacent to q_1; the j = 0 clause is only needed for
  s = omega. Distance is the board metric on both boards. OK.
* Step 4 (nobody is stalemated, beta's push is always legal): OK given NS (checkmate of omega is a win for beta).
* Step 5 (timing): every real omega move is a move of G^K_omega (p deleted, squares empty in the play are empty in G,
  king moves go to squares G allows; the K1 variant also, because a real king avoids attacked squares). The e-move
  bound is exactly H5K. OK. Note that H5K is needed with the king: my control run shows it (section 5).
* (H3K) implies (NS): at omega's m-th turn the king is within m - 1 <= e - 1 of k_omega, t is never occupied or attacked
  because the three files around t never hold a pawn (F1), t is not beta's king and not adjacent, so x -> t is legal even
  in check: OK. (e = 0 is vacuous and correct: no omega turn precedes beta's promoting push.)
I found no missing case. Label: PROVED (one AI proof) is not stronger than the evidence; I would add "read step by step
by K16v; no gap found; not independently re-derived by a second model" in the LOOPY wording, as was done for Proposition 2.11.

## 4. Proposed EDIT review

All five OLD blocks occur exactly once in the current LOOPY.md (checked with a script: counts 1, 1, 1, 1, 1; lengths 97,
114, 995, 108, 178). Targets (table row line 76, Remark 2.11 lines 1525 and 1529-1537, R3 item 1 line 2407, R3 item 5
lines 2430-2431) are the only places that mention the old conjecture; there is no other occurrence to update
(`grep -n -i "square rule\|square-rule\|real-king"` shows no further hit that would become false).
The NEW texts are accurate except for these points:

4.1 EDIT "Remark 2.11, square-rule conjecture replaced by the K16 outcome", CONJECTURE' bullet: "573 cases (180 instances
in the exhaustive sweeps, 393 positions in random hunts)". The 180 is 134 (flat:6x6 <= 3+3) + 36 (flat:7x6 <= 2+2)
+ 8 (flat:6x6 <= 2+2) + 2 (cyl:8x6 <= 2+2) from `summary.json`, but the flat:6x6 <= 2+2 sweep is contained in the <= 3+3 sweep,
so the 8 are counted twice. The count is 172 instances and 565 in total. (I did not re-derive the 393 of the hunts.)

4.2 Same edit, last line of the Theorem block: "Checked, not proved: on every certified instance of every sweep (H3K) implies
(NS) ..." But (H3K) implies (NS) is proved two lines above (the last `∎`). Replace by: "Computational counterpart
(COMPUTED-1): on every certified instance of every sweep ..." (the 0 exceptions among about 7.6 * 10^8 instances is
then a check of the proved implication, and "(NS) leaves 0 violations" is a check of the theorem).

4.3 Same edit, "The control without king moves in G_omega (variant KV = 2) fails on 153,582 instances of cyl:6x6 <= 3+3 (the
king captures a blocker and ω promotes first)": the number is K16's (not re-run), but the mechanism in parentheses is not
what K16's data show (they only record "omega promotes first"), and it omits the simplest mechanism. Hand example, checked
with kp_p and my certificate: cyl:6x6 `Ka1 ke1 Pc2 pe2 w -` passes every hypothesis with KV = 2 (the king is frozen, so the
pawn on e2 never moves) and is `L L` in P: Black plays Kd1 and e1=Q. Suggested wording: "(the king steps off its own pawn's
path or captures a blocker, and omega promotes first; e.g. `Ka1 ke1 Pc2 pe2 w -` on cyl:6x6 is (L, L))".

4.4 Optional, Theorem 2.11K proof: say in Step 2 "by induction on the plies of the play" so that the mutual use of Steps 2
and 3 is explicit; and keep "(one AI proof, ...)" in the form of 3 above.

Everything else in the five blocks I checked against the data (table figures, 1+1 flat counts 208 and 276, cylinders from
2 pawns, "22 violating instances of cyl:6x6 <= 4+4 with a legal move at y" = 496 - 474 at y, "45,566" is in instances
and is stated as such, 5,490 and 9,662, 101 / 93 / 2, 32, 4) and found them consistent with `logs/` and `summary.json`; the
claim "the earlier scratch evidence (`Ka1`, <= 2+2) cannot meet such nets" is consistent: the only cyl:6x6 <= 2+2 violation has
the king on a4 (and the 4+4 list has Ka1 violations).

## 5. Control (claim 5)

KV = 2 numbers (253,218 strategy failures, 153,582 real violations on cyl:6x6 <= 3+3): NOT_CHECKED (not re-run).
Qualitative claim "H5 must use the king": CONFIRMED by the hand example in 4.3.

## 6. Per-claim summary

See `summary.json`-style list returned with this report (StructuredOutput). Clean-up: bulk inputs, outputs, `.all`
dumps and binaries were deleted at the end; kept: scripts, logs (`*.json`, `*.cand`, `*.log`), this file.
