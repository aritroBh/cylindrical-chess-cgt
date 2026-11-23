# K50 referee report: kings/embed_check.py

Referee: an independent Claude agent (adversarial, separate context). Date 2026-11-23. Scripts, logs and outputs are in
`kings/delegate/out/K50/verify/`. The solver `kp_p` (built from `kings/delegate/out/K7/scripts/draft/kp_p.c`) was
compiled into `verify/` and deleted by name afterwards.

## Verdict: ACCEPT WITH FIXES

No false CERTIFIED was found. 6,222 compared positions on 6-rank boards gave 0 disagreements with `kp_p --pmodel` for
the verdict and for every CERTIFIED clause, with clause checks repeated at 8,572 chess-reachable descendants. No
BLOCKER was found. Two fixes are required before the program builds a test set:

- **F1 (MAJOR, crash).** A `ValueError` crash on about 4% of positions.
- **F2 (MAJOR, soundness gap; no counterexample found).** A missing case in the (V2) bound of the sharp form.

Both are fixed in `verify/embed_check.patch`, which applies cleanly to the committed file (`patch -p1 --dry-run`).
The remaining items are MINOR.

## Problems

| # | Where | Severity | What |
|---|---|---|---|
| F1 | `kings/embed_check.py:845` | MAJOR (crash) | `d0 = min([...] + [...])` has no `default`. When ω has no pawn in the terminal's component and there is no other component, `min` gets an empty list and the program raises `ValueError` (it is not caught in `run()` or `main()`). This kills a stdin batch at that line. It happened in 221 of 6,222 strict runs and 33 of 1,002 `--ctx` runs, on the random groups where the Proposition 2.11 route is open. It is not a false certificate, but those positions get no verdict. Fix: `default=INF` (no ω context pawn means μ_ω = ∞, so (L2) at the push nodes holds). With the patch the crashed positions give 114 strict and 16 `--ctx` CERTIFIED, and all 130 agree with kp_p (`verify/crash_recheck.py`). |
| F2 | `kings/embed_check.py:436-438, 836, 845` | MAJOR (soundness gap, not observed) | In `cert_terminal`, the bounds for the *other* components (`mu_`, `dmin_`) run over their **non-terminal** states only. That is right when the terminal comes from a move inside its own component. It is wrong in one case, which the enumeration creates on purpose: the e.p.-lapse terminal (lines 418-427). There, s plays in component B, so o's e.p.-protected pawn in A becomes passed. If that move of s also makes a passer in B, the whole-board terminal is a **race**, and B stands at one of its *terminal* states, which the bound skips. The skipped state can be one s-move closer to promotion (μ off by one). The full form is not affected, because a usable right in a position with two or more components makes (E) UNDECIDED. The sharp form is affected: `only_credit` checks the A-lapse terminal for β = o with this bound. A false certificate needs a non-passed s pawn that promotes faster than s's new passer, while o's passer is credited by the count rule. That is impossible on 6 ranks (a pawn one move from promotion is always passed) and possible in principle for H ≥ 7, 8×8 included. Searches: original against patched program, 1,748 positions (6 ranks) plus 2,033 targeted positions (7 ranks, double-step set-ups beside groups with the Proposition 2.11 route open). No verdict changed, so no counterexample was found. Fix: run both bounds over states ∪ terminal states (conservative). |
| M1 | `kings/embed_check.py:801-802` and findings.txt | MINOR | On flat boards (V2) is CERTIFIED through Proposition 2.11, which LOOPY *proves* only on the cylinder. For flat boards LOOPY says "the same proof works … (not separately written out)" and has reviewer evidence (434,429 positions). I read the proof for that question. Every step uses only (F1), (F2) and adjacency of files, and an edge file has fewer neighbours, which only removes attacks. So the claim is true. Strictly, though, it is a LOOPY remark and not a written proof. Either LOOPY adds one sentence (suggested text: "On a flat board the proof is verbatim, reading f ± 1 as the neighbouring files that exist; no step uses that a file has two neighbours"), or the output keeps the note. The note is already printed. I count it as acceptable. |
| M2 | `kings/embed_check.py:259-288, 387-395` | MINOR | The FEN e.p. square is not validated. The victim pawn must stand on the landing square, and the skipped and origin squares must be empty (kp_p rejects such input as illegal). With a bogus right the D-game simply has a capture that removes nothing. I found no route from that to a false CERTIFIED, but illegal input should FAIL separation. |
| M3 | `kings/embed_check.py:1007-1010` | MINOR | `parse` raises `ValueError` on a FEN whose rank or file count does not fit `--board`, and `main` does not catch it, so one bad line ends the batch. Same pattern as F1. Wrap each line and print an error object. |
| M4 | findings.txt, test (b) | MINOR (report) | Of the 2,080 runs in the report, all strict CERTIFIED were K29c2 and none exercised a reachable passer terminal through Proposition 2.11 ((H2) fails for every trébuchet-type group). The (V2) route was untested there. Here it was exercised: 1,209 strict and 196 `--ctx` positions with (V2)-passer CERTIFIED and at least one reachable terminal, on random groups whose kings stand away from Z-pawn files. 0 violations. |

Not problems (checked by reading the code against LOOPY; details in the attack list below):
- Theorem 1.14(i) and its per-(X, side to move) statement. The program's over-approximation covers both move orders, so the per-side statement is implied.
- Definition 2.1 and Lemma 2.2.
- Proposition 1.15(a): check status is decided at X, and separation FAILS when the side to move is in check or the side not to move is in check.
- (E) by L1.6: "≥ 2 components" is detected both at the root and after re-splits.
- The local game of Definition 2.6 with (L1_P): passes, confinement, promotion rules, mate, the T count.
- (L3_F) as stated.
- (L2): `dmin` is a valid lower bound, and the king search is a valid lower bound with min over components (pawn-only interaction between components is impossible, and other components only hinder the king). Proposition 2.10(a) is used only for T = 1, only in non-terminal contexts, and H ≥ 5 is enforced at separation.
- (H1)-(H5): (H2) needs Z-pawns only, because the buffer is empty. (H3) through the root files is a superset by (F1). (H5) excludes ω's Z-pawns soundly because they have no move at the root and cannot gain one under Π.
- The Corollary 2.7′ transfer: strict certificates only, and (L2) at the push nodes by D0 − (e − 1), not by Proposition 2.10(a), which would be wrong there since those contexts are terminal.
- The sharp-form choice of σ (the whole-board D winner) and the clauses it drops: (E), (V1b), (V3) for the winner, and terminals credited to the loser. This matches (S1)-(S3).
- Cylinder arcs (largest-gap complement), wrap in `file_groups`, both kings on one file (default F_Z = that file, so the neighbouring files are the buffer), and the wrong side in check.

## Harness counts (6-rank boards; `verify/harness.py`, `verify/ref.py`, `verify/summarize.py`)

Boards: cyl:6x6, cyl:7x6, cyl:8x6, flat:7x6, flat:8x6.

Groups:
- Z_T, K29 classes 1-4, Z72, Fig (a) (cyl), Fig (b) (flat, and mirrored).
- 48 random king groups on F_Z = a-c, selected by `verify/group_search.py` for an open (V3) or (V2) route.

Contexts: up to 3 pawns a side. 30% have an e.p. right at the root (1,417 roots), with a bias to start ranks. Both sides to move.

The reference D-game was written independently (`ref.py`, which does not import the program). Checks:
- **C1.** Verdict CERTIFIED ⇒ kp_p exact and equal to the predicted winner; the program's D equals the reference D.
- **C2.** Full form ⇒ P(Y) = refD(Y) at up to 25 chess-reachable Y.
- **C3.** (V3) CERTIFIED for side s ⇒ every Z-move of s at X and at the Y with s to move is a P-loss (kp_p `--moves`).
- **C4.** (V2)-passer CERTIFIED ⇒ every context move from X or a Y that reaches a terminal (whole-board credit) gives a P-win to the beneficiary.
- **C5.** (V1b) CERTIFIED ⇒ the side to move has a legal move.

| | strict | --ctx |
|---|---|---|
| positions run | 6,222 | 1,002 (a 20% / 15% sample: `--ctx` costs about 5 s a position) |
| CERTIFIED (full / sharp) | 439 (0 / 439) | 76 (7 / 69) |
| FAILS / UNDECIDED / CRASH (F1) | 586 / 4,976 / 221 | 80 / 813 / 33 |
| (V3) CERTIFIED for a side (C3) | 3,517 | 550 |
| (V2)-passer CERTIFIED (C4) | 1,209 | 196 |
| (V1b) CERTIFIED for a side (C5) | 11,622 | 1,914 |
| disagreements, C1-C5 | **0** | **0** |
| program D ≠ reference D | 0 | 0 |

- Chess-reachable descendants checked by C2-C5: 8,572.
- CERTIFIED roots that carry an e.p. right: 40.
- With the patch, the 254 crashed runs give 130 more CERTIFIED (114 strict, 16 `--ctx`), all agreeing with kp_p.
- Against the investigator's 2,080 runs (5 groups, 193 CERTIFIED): this run used about 3 times the positions, 9 named
  and 48 random groups, and 515 CERTIFIED verdicts. Every CERTIFIED clause was also checked, at the root and at
  reachable descendants, not only the verdict.

Not run or not compared:
- **cyl:9x6, 960 positions.** The 12 random groups on cyl:9x6 have no solver result (kp_p accepts W ≤ 8), so they are
  excluded above. The program ran on them without errors other than F1.
- **Named shard 0, run reduced.** The reboot at 12:13 cut it off before it started. After the reboot it was run with
  15 contexts a side instead of 60, giving 510 positions (counted above): cyl:6x6 ZT/K29c2/K29c4; cyl:7x6 K29c1/K29c3;
  cyl:8x6 ZT/K29c2/K29c4/Z72/FigA; flat:7x6 K29c1/K29c3/FigB; flat:8x6 ZT/K29c2/K29c4/Z72. The other shards ran in full.

Other checks:
- **ChessSums (item 4), `verify/chesssums_check.py`, log `verify/chesssums.log`.** All 200 positions of the engine
  subset were run with `--group`, classified independently. APART: 23/23 pass separation (all UNDECIDED). ADJACENT:
  14/14 FAIL (a buffer pawn). **SHARED: 163/163 FAIL**, every one with "component pawn on a group file". 0 mismatches.

## The `--ctx` argument (findings.txt): SOUND

Read as a proof against Theorem 2.7, Steps 0-6.

- **(L3) check.**
  - U is a superset of everything that can block or attack a king square off F_Z in any window position:
    - The window starts at Q, whose context is a reachable non-terminal context. These are enumerated as a product superset over components.
    - In the window, s̄'s context pawns never move and are only removed (I4), so their squares and attacked squares stay inside U.
    - s's context pawns stay on context files (Lemma 2.2), and every push, capture or e.p. capture keeps them in the forward cone of their position at Q.
    - Buffer squares never hold a pawn.
  - The remaining legality conditions are the same in the local and the real position, by Step 1:
    - not adjacent to s̄'s king;
    - not attacked by a Z-pawn;
    - the check is resolved (checkers are Z-pawns, by I4).
  - So a local king step to a square outside U is a legal real move.
  - Real s-turns project onto lines in which s̄ plays winning moves, by Step 1. The check covers every such line, which is stronger than the existence of one guided strategy.
  - So s is never stalemated in the window, which is (L3).
- **(V1b) via a buffer square.** Sound for the same reasons.
- **Harness.** No violation in 1,002 `--ctx` runs: 76 CERTIFIED, 550 (V3)-side certificates, every Z-move checked at the root and at the descendants.

**Recommendation: promote it to LOOPY, and keep it off by default until it is there and a second referee has read it.**
Do not remove it: it is the only route by which a trébuchet group can be certified at all. Proposed statement:

> **Lemma 2.6a ((L3) from a reachable-context envelope).** Let 𝒞 be a set of contexts containing the context of every
> Y at which LC_T(m) is to be used (for Theorem 1.14: every chess-reachable context before the first decisive event).
> Let U_s be the set of squares off F_Z that are occupied by an s̄ context pawn in some C ∈ 𝒞, are attacked by one, or
> lie in the forward cone, on the context files, of an s context pawn of some C ∈ 𝒞. Suppose that in every line of
> L_T(Q_Z) in which s̄ plays only winning moves, s has at each of its turns before s̄'s win a legal local move that is
> a Z-pawn move, a king step onto F_Z, or a king step onto a square not in U_s. Then (L3) holds at every such Y.
> (L3_F) is the case U_s = everything off F_Z.
>
> *Proof sketch.* Fix the guided strategy "play a winning local move". By Step 1 of Theorem 2.7 each real s-turn
> projects to an s-turn of such a line. By (I4) s̄'s context pawns only lose members after Q, so their squares and
> attacks at R lie in U_s. By Lemma 2.2 and the pawn move rules s's context pawns at R lie in the forward cones of
> those at Q. The buffer is empty. Hence a local king step to d ∉ U_s meets every real legality condition: d is
> empty of pawns, not attacked by a context pawn, and the king, adjacency and Z-pawn conditions coincide with the
> local ones. Z-pawn moves and steps onto F_Z are legal by Lemma 2.2. So s always has a legal move. ∎

## What the paper side must know before using the program to build a test set

1. **Apply `verify/embed_check.patch` first** (F1: crash; F2: the sharp-form race bound). Re-run the program's own tests
   after patching.
2. **Strict mode certifies none of the paper's trébuchet groups** (Fig (a), Fig (b), Z_T), beside any context. That is
   correct: (L3_F) fails, as LOOPY 5.1 says. A test set of trébuchet positions needs `--ctx`, which rests on Lemma 2.6a
   above (SOUND by this review, not yet in LOOPY). Until LOOPY has the lemma and a second referee, label such positions
   COMPUTED / argument-refereed, not PROVED. On 8 ranks even `--ctx` certifies a trébuchet only beside essentially
   locked or far-back contexts with no reachable passer terminal ((H2) fails for these groups).
3. **What CERTIFIED proves.** A result in P (first promotion wins), for the given side to move. The sharp form gives
   only "X is a P-win for σ", not P = D at other positions. A chess ground truth needs (A_Q)(X) checked separately
   (kpsolve), which the program never does. Engines play chess, not P.
4. **Use `--group` whenever the generator knows its group.** Without it, extra pawns on the kings' files become Z-pawns
   of a larger group, and some ChessSums SHARED rows then pass separation.
5. **Flat 8×8 (V2)** rests on LOOPY's one-line extension of Proposition 2.11 (M1). It is fine, but cite it as such.
6. **UNDECIDED is common and says nothing.** About 80% of the harness positions were UNDECIDED, and most of those had
   P = D anyway. Expect a test set built only from CERTIFIED positions to be small and biased towards locked contexts
   and groups whose Z-moves are punished at once.
7. **Feed only legal FENs** (M2: the e.p. square is not checked), and expect one bad line to stop a stdin batch until
   M3 is fixed.

## Files

`verify/`:
- `harness.py`, `ref.py`, `summarize.py`, `group_search.py`, `diff_patch.py`, `crash_recheck.py`, `chesssums_check.py`;
- outputs `rand_0.jsonl.xz`, `rand_1.jsonl.xz`, `named_1.jsonl.xz`, `named_0.jsonl` (+ `.log`), `summary_all.txt`, `chesssums.log`,
  `diff_patch*.log`, `gs*.jsonl`, `jobs_random.json`, `jobs_h7.json`;
- `patched/kings/embed_check.py` (the patched copy used for the experiments) and `embed_check.patch`.
