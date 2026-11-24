# K57 referee report

AI work (referee, one agent), no human re-derivation. I did not take part in K57. I did not use `src/toy57.py`,
`src/pr57.cpp` or the investigator's sum code. My files are in `verify/`: `src/vgsum.cpp` (the K56 referee's `vg.cpp`
generator and graph builder, copied unchanged, plus my own token-game and D-sum solvers), `src/toyref.py` (my own
abstract test, with checks and e.p. rights), `src/xval.py`, `src/mkT.py`, `src/cmp_h10.py`, run scripts, `logs/`,
`pids.log`, and `EDITS.md` (replacement edit set).

## Verdict in short

- **Proposition 4.14 (PROOF.md Proposition 1): PROVED.** Every step SOUND.
- **Lemma 4.15 (PROOF.md Lemma 2): PROVED.** Every step SOUND. Weakest step: the phase-2 bookkeeping (b-safety under
  pauses and the termination pair (b, μ)); it is correct as written.
- **Corollary 4.16: PROVED, given CHECKED-2 computations.** Definition 4.8 for H10 is CHECKED-2 (K45). (B1) for H10 is
  CHECKED-2 after my step 3: my own computation (sum rule, e.p. right kept) gives W at all ten moves, and so do the
  K56 referee's `vg` (pass game, implies (B1)), pr57, and za/rz (eight moves directly, the two double steps through
  b3×a4 e.p.). Weakest link: none in the proof; on the computed side, the completeness of the move list, now confirmed
  by `kp_p --moves`.
- **Edits:** apply `verify/EDITS.md` (mine), not the investigator's `EDITS.md`. Both apply cleanly. Mine also updates
  the six passages that still said "open" or "not realised", calls the proof refereed, and keeps the claim at "has the
  results of over beside every finite D-game".

## 1. The proofs, step by step (PROOF.md)

Notation as in PROOF.md: Y has the strategy S in over_D ⊞ T, X is the other side, R = roots ∪ q's.

### Proposition 1 (over ≥ 0)

| Step | Verdict | Note |
|---|---|---|
| Strategy: S0 in T; answer Black's ω → ω by ω → 0_D | SOUND | White's ω → 0_D is always legal (over has no checks). Black can play ω → ω at most once before the component is 0_D. |
| Deleting the pair gives an S0-consistent play | SOUND | The pair starts and ends at the same t with Black to move. Black's T-moves are the same in both plays. |
| Ends: terminals, stuck sides, infinite play | SOUND | A terminal of T is reached at the same move in both plays. White is never stuck: S0 names a move (a stuck White would lose the 0_D play). Black stuck needs component 0_D, so Black is stuck in both plays. An infinite play stays infinite. |
| Both senses (win ⇒ win, non-loss ⇒ non-loss); bounded win | SOUND | Length changes by at most 2, so (K-a) holds. The contrapositives give the Black statements used in E1. |
| Loopy T, draws, terminals | SOUND | Nothing in the argument uses acyclicity of T. |

### Lemma 2

| Step | Verdict | Note |
|---|---|---|
| §1 model; (K-a), (K-b) | SOUND | Matches the K47 bullet (K40's convention). |
| Token games, Att^X_k, "P-wins ⊆ Att^X_0" | SOUND | A P-win of Y never reaches a stalemate of Y (a draw in P). A stalemate of X only becomes a Y win. Promotions are terminals in both. |
| (P1) | SOUND | Spending the token is an X option of an X-to-move state of Att^X_1, so it leads to Att^X_0 with smaller rank. |
| (P2) | SOUND | Used only through b-safety. |
| The group's facts | SOUND | They follow from Definition 4.8 (over orientation). A move that does not lose at once is a freeze by definition, so every other White root move loses at once. A freeze that gives check makes (O4) fail, so no king is in check at a q. K1 and K2 cover the roots. At q without the right, Black's moves are a subset of those with it. |
| Reduction to (★) | SOUND | W, L and D are all covered. For D, both colours have non-losing strategies, so draws transfer both ways. |
| Phase 1, Y to move | SOUND | T-moves are legal: no check on R. The freeze exists (O2) and is not a promotion. The shuttle is legal (O1). At a q, S names only T-moves. |
| Phase 1, X to move | SOUND | X's T-moves, the shuttle and the freezes are copied. Every other G-move loses at once by Definition 4.8, at roots and at q's. X stuck loses. |
| E1 (X = White) | SOUND | Turn order checked. Virtual before m: (o, t, White). After m and Black's P-reply r: real (z, t, White), Att^W_0. If o = ω, the virtual state is replaced by (0_D, t, White) and S by S′; Proposition 1 applies because (ω, t, White) is S-consistent, so Black wins (does not lose) from it. The comparison game is the right one: same t, same side to move. If m gives check, r answers it (r is a P move). If r gives check, White must answer in G (step a). If White then moves only in T forever, Black answers by S′ in T: an infinite S′-play, which is a draw, allowed only in the non-loss case and impossible when S′ wins. A terminal of T is reached in the virtual play as well. Black is never asked for an unforced G-move: S′ lives at 0_D. |
| E2 (X = Black at q) | SOUND | o = 0_D, budget 0, no over-move can be asked. |
| E3 (X = Black at a root) | SOUND | (B1) gives (x, White, 1 token) ∈ Att^B_1, with the right if m is a double step. Black's real G-moves are never copied, so the virtual Black never uses ω → ω after the entry. That is a subset of S's opponent moves, which is allowed. |
| b-safety; invariant H | SOUND | b-safety asks only that X's G-moves land in Y's set and, if b = 1 and X is not in check, that the token target lands in Att^X_0. It survives losing the right and pauses. |
| Step (a) | SOUND | Y answers on the board. The virtual state is unchanged. Checks are answered on the board. |
| Step (b), pause | SOUND | Y is not in check: the board is the one after Y's own last G-move, or after the entry, or a board of R. |
| Step (b), over-move | SOUND | Only White, only at o = ω, b = 1. X has just moved in T, so X is not in check, and b-safety gives (g, W, no right, 0) ∈ Att^B_0. After it o = 0_D and b = 0. **One token suffices:** the virtual o never returns to ω, the play never returns to phase 1 (even if the board comes back to a root position, the real play is handled by the attractor, not by S's over-moves), and S at 0_D names no over-move. So White is asked at most once, whichever root Black left from. |
| Termination of phase 2 | SOUND (weakest step) | (b, μ) falls lexicographically at every G-move of phase 2. Pauses do not raise μ. Loopy T: unboundedly many pauses only lengthen the virtual play. |
| Results; X promotions; Y always has a move | SOUND | The shuttle, freezes and m are not promotions. b-safe moves lead into Y's set, which contains no X promotion. A terminal of T is reached in the virtual play as well. |
| q statement | SOUND | Phase 1 from q with o = 0_D. |
| Stalemate and e.p. conventions | SOUND | A stalemate is a draw in P and a loss in the sum. Only the inclusion "P-win ⇒ Att win" is used, and it holds. The right is lost by every move elsewhere, which matches the token. |

**Statement vs proof.** The investigator's EDITS statement matches the proof (model, hypotheses, class of T, both roots,
both sides, q's). It says "has the results of over", but one sentence goes further: "So over is realised in D-sums by a
king-and-pawn group of P." The note defines no equality of loopy D-games, and the result does not cover P contexts.
My replacement keeps the claim at "has the results of over beside every finite D-game" and says what that does not
cover. It also states (B1) explicitly under the sum's rule (check, right).

**Side claims checked.** "(B1) is (N1) of (T2) read with the sum's rule": correct as an implication, (N1) ⇒ (B1).
"Z_O and its flat translates fail (B1) exactly at 1…e5–e4": TRUE under the sum's rule, checked here (§3). "(B1) is
not necessary": consistent with my toy runs (§2), where groups without (B1) also often match over.

## 2. Brute force (own code, `verify/src/toyref.py`; COMPUTED-1)

The model has the two chess features the proof must handle, which the K56 referee's toy leaves out:

- **checks:** a side in check may not move in T or spend a token; a move into one's own check is illegal; in P a side
  with no move is checkmated (loss) if in check and stalemated (draw) otherwise;
- **e.p. rights:** a double step gives the opponent extra moves for one turn only, and a move elsewhere clears the
  right.

Definition 4.8 is applied in P and (B1) in the D-sum with −1. Each group is compared with over beside 224 finite
D-games: 24 hand-made, including Black and White threats of a terminal (answerable or not), "whoever moves wins",
loops with a terminal exit for one side, integers up to ±3, on, off, dud, \*, ↑, ↓, and unlimited White spare moves
next to a Black threat; plus 200 random ones (1 to 4 positions, loopy, terminals in about two thirds). The comparison
covers both roots, every q state (Black to move with and without the right, White to move), both sides and every t.
Solver cross-check: on check-free, right-free groups my sum solver equals the K56 referee's `toy.py` on 97,344 values
(`logs/xval.out`).

| Run | Exact groups with (B1) | Results | Differences | (T3) fails | Not won with 2 tokens | Without (B1): groups differing |
|---|---|---|---|---|---|---|
| random, seeds 1 to 4 | 8,000 | 41,284,356 | **0** | 2,107 | 96 (seeds 2 to 4) | 1,167 of 8,000 |
| adversarial gadgets, seeds 5, 6 | 4,000 | 22,065,572 | **0** | 3,477 | 1,553 | 58 of 4,000 |
| total | 12,000 | 63,349,928 | **0** | 5,584 | 1,649 | 1,225 of 12,000 |

What the gadget family contains:

- bad White root moves saved by one, two or three White passes, or by unlimited passes (a loop): the (T3) failures
  that Lemma 4.15 claims not to need;
- bad Black root moves saved only by 2, 3 or 4 Black tokens: (B1) holds but two tokens break it, so a proof that let
  over ask White twice would fail on them;
- different freezes at the two roots (6,124 of the 10,000 groups where this was recorded);
- checks and double steps.

7,161 of the 12,000 groups have a check somewhere, and 11,932 have a double step. Seed 1 ran with the first version
of the script, before the extra counters and the gadget mode were added; the core is the same.

**Proposition 4.14 by brute force:** r(0_D ⊞ t, s) ≤ r(ω ⊞ t, s) for White at all 150,796 comparisons (the 224 games
of each run and 3,000 random games of up to 7 positions per run), 0 violations.

So no counterexample to Lemma 4.15 or Proposition 4.14 in the abstract setting. The control shows the test can
separate groups from over.

## 3. (B1) for H10, independently

**Move list.** `kp_p --pmodel --moves` (K44's kp_p10.c, `logs/roots.kpp`) gives 6 Black moves at each root:

- f6 root: Kf6–g6 (shuttle), Kf6–e6, a5–a4, a5–a3, e5–e4, e5–e3;
- g6 root: Kg6–f6 (shuttle), Kg6–h6, a5–a4, a5–a3, e5–e4, e5–e3.

That is ten non-shuttle moves. The K56 referee's generator in `vgsum` lists the same ones, and no move is missing.
Both programs also list the White root moves: everything loses at once in P except e2–e3 (f6 root) and e2–e4 (g6
root). No king is in check at the roots.

**Do "beside −1" and "one Black pass" coincide?** They differ in one point only. In the pass game (vg, pr56/pr57) a
side with no move and no pass is stalemated, which is a draw. Beside −1 under the sum's rule it loses. Check (no pass
in check) and the right (cleared by the pass) are the same in both. So a White win in the pass game implies (B1), but
not conversely. I therefore computed (B1) directly with the sum's rule. `vgsum` does this in two ways: the
one-token game, and the product with T = −1 using the D-sum solver. Both keep the e.p. right (`logs/h10.out`).

| Root | Move | Right after it | P | (B1), sum rule (token game) | H10 ⊞ −1, White to move (product) | vg pass game, 1 pass (K56 referee) |
|---|---|---|---|---|---|---|
| f6 | Kf6–e6 | none | W | W | W | W |
| f6 | a5–a4 | none | W | W | W | W |
| f6 | a5–a3 | a4 (b3×a4) | W | W | W | W |
| f6 | e5–e4 | none | W | W | W | W |
| f6 | e5–e3 | e4 (no taker) | W | W | W | W |
| g6 | Kg6–h6 | none | W | W | W | W |
| g6 | a5–a4 | none | W | W | W | W |
| g6 | a5–a3 | a4 (b3×a4) | W | W | W | W |
| g6 | e5–e4 | none | W | W | W | W |
| g6 | e5–e3 | e4 (no taker) | W | W | W | W |

The double steps, treated directly:

- after …a5–a3 with the right, (B1) gives W at both roots;
- without the right the same board is not a White win (as za and rz found);
- after b3×a4 e.p., Black to move with the token, it is W;
- `kp_p` also says b3×a4 is White's only P-winning move there.

So the investigator's e.p. route is right, and the direct computation does not need it.

External agreement: beside 0, −1 and off, my values for the eight moves without a right equal za's
(`../logs/C_za_H10.out`) at all 24 entries, including the four draws beside off (White to move).

**Direct sums.** I computed r(H10 ⊞ T) with my own D-sum solver (`vgsum`, built on the K56 referee's generator, not
the investigator's code) beside 63 finite D-games (`logs/T_h10.txt`). There are 23 hand-made games (the integers, on,
off, dud, \*, ↑, ↓, and games with terminals: threats for either side, answerable or not, "whoever moves wins", loops
with terminal exits, unlimited White spare moves next to a Black threat) and 40 random ones (up to 3 positions). 34 of
the 63 have terminals. The comparison covers both roots and the q's (with and without Black's right after e2–e4),
both sides and every t: **1,215 results, 0 differences from over** (`logs/cmp_h10.out`, COMPUTED-1).

**Z_O and translates (side claim).** `vgsum` under the sum's rule (`logs/ZO_*.out`):

- Z_O on cyl:8×6 and on flat 8×6, and its translates by one and two files on flat 8×6, fail (B1) exactly at the
  e-pawn push e5–e4 (f5–f4, g5–g4);
- every other non-shuttle Black root move is W;
- for Z_O on cyl:8×6 this agrees with the K55 referee's solver (CHECKED-2); for the others it is COMPUTED-1.

I ran the direct two-file translate. The note lists its left-right reflection, which is equivalent on a flat board.

## 4. Problems found

1. Investigator's EDITS: "So over is realised in D-sums by a king-and-pawn group of P" is stronger than the statement
   proved, because the note has no equality of loopy D-games. Reworded.
2. Investigator's EDITS leave six passages that still say the question is open or that over is not realised:
   - the K55 bullet;
   - the K56 sentence in the K47 bullet;
   - the last sentences of Lemma 4.13;
   - the C4.7 status row;
   - the opening of Conjecture 4.7 ("the one tested in sums is not equal to over");
   - the second-half bullet ("over itself is still not realised as a sum value").
   Its "To settle" edit also asks for "a referee check", which is now done. All are covered by my edit set.
3. Investigator's EDITS call the lemma "not refereed" and do not say (B1) is read under the sum's rule (check, right,
   stalemate a loss). Fixed.
4. Minor, not changed: PROOF.md §5 says za/rz "report the position without the right (L, as expected)". Correct, but
   a reader may miss that the direct value with the right is W; my §3 records it.
5. No mathematical error found.

## 5. Edits

- Investigator's `EDITS.md`: 3 applied, 0 rejected. **Do not apply** (problems 1 to 3).
- **Apply `verify/EDITS.md`**:
  `.venv/bin/python kings/delegate/apply_edits.py kings/theory/LOOPY.md <out> kings/delegate/out/K57/verify/EDITS.md`
  gives 9 applied, 0 rejected. Table cell counts are unchanged (the `diff` of the `awk -F'|'` field counts is empty).
  Bold markers are balanced (966 → 974). Labels:
  - Proposition 4.14 PROVED (refereed);
  - Lemma 4.15 PROVED (refereed);
  - Corollary 4.16 PROVED, given CHECKED-2 computations (Definition 4.8, K45; (B1), this check);
  - the cyl:8×7 groups conditional on a COMPUTED-1 fact;
  - toy and direct-sum tests COMPUTED-1.
  The scratch copy was deleted.

## 6. Process

- All solver runs went through `kings/delegate/heavy.sh` under `/usr/bin/time -l`. PIDs are in `verify/pids.log`.
- I measured the smallest input first: a 1 + 1 group, 34 MB.
- Peak memory: `vgsum` on H10 with the 63 sums 1.11 GB; on Z_O and the translates 1.26 to 1.29 GB; kp_p 20 MB;
  toy runs 22 to 34 MB.
- No process signalled. Binaries deleted. No output over 256 KB.
- No git changes. Nothing edited outside `K57/VERIFY.md` and `K57/verify/`.
