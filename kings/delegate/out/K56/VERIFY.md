# K56 referee report

AI work (referee, one agent), no human re-derivation. I did not take part in K56 and did not read `src/pr56.cpp`.
My files are in `verify/`: `src/vg.cpp` (own pass-game solver), `src/toy.py` (abstract toy test), `src/mono.py`
(monotonicity search), `run.sh`, `runval.sh`, `logs/`, `pids.log`, `EDITS.md` (replacement edit set).

## Verdict in short

- **Lemma 2 of PROOF.md (Lemma 4.13 in EDITS): PROVED.** I re-derived every step; all steps of the main
  proof are SOUND. One side claim is WRONG: the monotonicity Att^X_∞ ⊆ Att^X_1 ⊆ Att^X_0 (§1), and with it the sentence
  "pass-robust exact ⇒ tempo-exact" (Definition 1′). The main proof never uses it. The conclusion it was meant to
  support (pass-robust exactness is sufficient) is still true: the same proof runs with an unlimited budget for both
  sides. Weakest step: the termination count of phase 2. It is correct, but the text only works if the ranks of
  different budgets are read as ranks in one game whose states carry the passes left. The text says this only in §1.
- **Part A: CONFIRMED** for every root move of Z_O (cyl:8×6) and of the 2 + 3 group H10 (cyl:10×6). I used my own
  solver; its P values equal `kp_p --pmodel` on 800 + 400 sampled states. Those entries become CHECKED-2. The other
  seven groups stay COMPUTED-1.
- **Edits:** apply `verify/EDITS.md` (my replacement), not the investigator's `EDITS.md`. Both apply cleanly (2 applied, 0
  rejected, table cell counts unchanged, bold markers balanced). The replacement removes the false implication, records
  the referee and the CHECKED-2 entries, and says plainly that no known group meets the criterion and that H10 = over
  stays open.

## 1. The proof, step by step (PROOF.md)

Notation as in PROOF.md: Y is the side with the strategy S in over_D ⊞ T, X is the other side, R = roots ∪ q's.

| Step | Verdict | Note |
|---|---|---|
| §1 sum model | SOUND | It matches the K47 bullet (K40's convention): a side in check may not move in T, a move in T clears the right, no move anywhere loses, terminals end the whole play. |
| (K-a), (K-b) | SOUND | Standard. Also "S wins every play" is enough for r = W on a finite graph: if r ≠ W, the other side can stay out of the attractor. |
| Pass games, attractor ranks | SOUND | Ranks must be read in one game whose states carry "passes left" (§1 says so). Then (P1)'s "smaller rank" is right. |
| Monotonicity Att^X_∞ ⊆ … ⊆ Att^X_0 | **WRONG** | A pass can be forced where a stalemate would draw. Toy: Black to move at a position with no Black option, where White has a move to ⊕. With 0 passes it is a stalemate (draw). With 1 pass Black must pass and loses. `src/mono.py` also finds a case of Att^X_∞ ⊄ Att^X_1. In chess this needs X stalemated in G, which is rare but possible. The main proof never uses this claim. |
| (P1) | SOUND | |
| (P2) | SOUND with its stated exception (k = 0) | It is not used. b-safety replaces it. |
| Stalemate paragraph, b-safe | SOUND | b-safety only asks that X's G-moves lead into Y's set, and that the pass target is in Att^X_{b−1} when X is not in check. It holds trivially when X has no G-move. It survives losing the right and a "pause" (both sides move in T), because it does not depend on whose turn the pass game would give. This is the key point, and it is right. |
| (T1) follows from 4.8 with K1, K2 | SOUND | At a root: K1 (no pawn attacks the king squares), K2 (kings two apart). At q: only White's freeze could give check, and then (O4) fails. White's own move cannot leave White in check. |
| Definition 1 = EDITS (T1)–(T3) | SOUND | Same hypotheses in the same model. Lemma 2 and the EDITS statement match: every finite D-game T, terminals allowed, both roots, every q, both sides. |
| Definition 1′ "pass-robust ⇒ tempo-exact" | **GAP / WRONG as stated** | It rests on the false monotonicity. Repair (mine): run §3 with b ≡ ∞ for both Y and every o. The (N) entry needs (x, Y) ∈ Att^X_∞ for every losing move at the roots and at the q's, and pass-robustness gives exactly that. Unforced moves are unlimited. Termination uses μ alone. So pass-robust exactness is sufficient, but by this argument, not as a special case of tempo-exactness. The toy found no pass-robust group that is not tempo-exact (0 of 1,574), so this is about the wording. |
| Reduction to (★) | SOUND | W ⇒ White has a winning S. L ⇒ Black has one. D ⇒ both have non-losing S. All three cases are covered, so draws match in both directions. |
| Phase 1, Y to move | SOUND | T-moves are legal by (T1). The freeze exists by (O2) and is not a promotion (Definition 4.8). The shuttle is legal by (O1). Roots never carry a right. At q, losing the right by a T-move leaves a q state whose conditions still hold, because the moves without the right are a subset of those with it. |
| Phase 1, X to move | SOUND | X's T-moves, the shuttle and the freezes are copied. Every other G-move loses at once: at a root by (O1) or by the definition of a freeze, at q by (O3)/(O4). If X has no G-move at q, then 0_D has none either. |
| Budget b(White, ω) = 1, b(Black, ω) = ∞, b(·, 0_D) = 0 | SOUND | Y makes an unforced G-move only when S names an over-move. X's over-moves are never copied in phase 2. |
| Entry (N) | SOUND | b = b(Y, φ(g)) gives exactly (N1), (N∞) and "loses at once" at q. Promotions by X are excluded, because Y's set contains no X promotion. |
| Entry (V), X = White (V0) | SOUND | m is copied as ω → 0_D. At 0_D, S names only T-moves, legal since Black is not in check by hypothesis. The real (x, W, no right) ∈ Att^W_0 is 0-safe. If S had no move, S would lose the virtual play. |
| Entry (V), X = Black (V1) | SOUND | If S names a T-move, (x, B, no right) ∈ Att^B_1 is 1-safe. If S names ω → 0_D, (P1) gives (x, W, no right) ∈ Att^B_0. White's moves with a possible right include these and lead to the same states. |
| Step (a) | SOUND | It is a null round, so the virtual state is unchanged. A check is answered on the board. |
| Step (b), pause | SOUND | Y is not in check: the board has not changed since Y's own last G-move or since the entry (the (V) hypotheses). b-safety is kept. |
| Step (b), S names an over-move | SOUND | X moved in T, so X is not in check, and b-safety gives (g, Y, no right) ∈ Att^X_{b−1}. For Y = White the budget goes 1 → 0, together with ω → 0_D. For Y = Black it stays ∞. |
| Termination | SOUND (weakest step) | (b, μ) is lexicographic over {∞ > 1 > 0} × ℕ, so it is well-founded. Step (a): μ′ < rank(g″, X) < rank(g′, Y) ≤ μ. Unforced move with b = ∞: μ′ < rank(g, Y, no right) ≤ μ. With b = 1 → 0, b falls. A pause does not raise μ. So there are finitely many G-moves in phase 2, however many times X moves in T, loopy T included. Every other real move is a virtual move. |
| Results | SOUND | An infinite real play gives an infinite S-consistent virtual play. X cannot promote: the shuttle and the freezes are not promotions, entry moves lose, and b-safe moves lead into Y's set. A T terminal is reached in both plays, so it is not X's terminal. Y always has a move. X with no move loses. So a winning S gives a real win, and a non-losing S gives a non-loss. |
| q statement | SOUND | Start in phase 1 with o = 0_D. |
| §4 points; Remark 4 | SOUND | Remark 4 is right for k = ∞: if Y passes, X passes back to a state of smaller rank, and an e.p. right only adds moves. It is not used in the lemma. |
| §4 "test games with terminals" | SOUND | A terminal of T cannot interrupt Y's forced win in the group without the same terminal being reachable against S. X's T-moves are always answered by S in T, and X's G-moves cost X the virtual turn. |

### Points the brief asked me to attack

- **Termination with an unbounded number of opponent moves in a loopy T.** Pauses are not G-moves and do not raise μ.
  Infinitely many pauses make the virtual play infinite, which a winning S excludes and a non-losing S allows (a draw on
  both sides). SOUND.
- **Draws.** They are matched through (★) for non-losing strategies, in both directions. SOUND.
- **Terminals in T.** See the table. A terminal ends both the real play and the virtual play with the same result. SOUND.
- **Checks.** Every pass the proof uses is either X's T-move, which is legal only if X is not in check, matching "a pass
  needs X not in check", or a pass that S answers in T. Y moves in T only when not in check. SOUND.
- **E.p. right and stalemate.** Handled by b-safety, which never needs Att^X_0 at a stalemated X. SOUND. The only false
  statement here is the monotonicity line.

### Sanity test of the statement (toy instances exist)

Definition 4.12 makes sense for an abstract D-game without checks or e.p. rights: roots A and B, Black's shuttle A ↔ B,
White's freezes to q's, "alone" means a side with no option and no pass draws, and the D-sum is that of Definition 1.3.
`src/toy.py` builds random groups (4 to 9 positions, loops and terminals), filters them by Definition 4.8 (over
orientation), and compares r(G ⊞ T) with r(over_D ⊞ T) at both roots and every q, both sides, every t, beside random
finite D-games T (1 to 4 positions, loopy, terminals in about two thirds). Five seeds, 300 tests each
(`logs/toy.out`):

- 2,000 tempo-exact groups (216 of them pass (T2)/(T3) only through the (V) alternatives): **0 differences in
  9,064,258 results**.
- 1,574 pass-robust groups: 0 differences.
- Control: 543 of the 3,954 exact groups that are not tempo-exact differ from over somewhere, so the test can tell
  groups apart.

COMPUTED-1 (one program). It supports the lemma but does not prove it, and it does not exercise checks or e.p. rights.

## 2. Part A: my own pass-game check

`src/vg.cpp` was written from SPEC.md, Definitions 1.2, 1.5, 4.8 and K56's Definition 1, with no code from pr56. It
builds the states reachable from the four roots under moves and passes of both sides. Every e.p. target is kept, so it
has more nodes than pr56: 6,496,367 for Z_O and 4,360,884 for H10. It then runs retrograde with counters on P^X_1 (a
"passes left" layer of 0 or 1, so P^X_0 is layer 0) and on P^X_∞, for X = White and X = Black.

**My reading of a pass:** it is allowed only when the passer is not in check. The board stays, the move goes to the
other side, and the e.p. right is lost. A side with no move and no pass left draws (stalemate), and a checkmated side
loses. This is the investigator's reading (PROOF.md §1).

**Validation without passes:** P values against `kp_p --pmodel --cap 1` (K44's kp_p10.c) on 400 random reachable
states per group, 44 of them with an e.p. target: **0 differences** (Z_O 180 W, 11 D, 209 L; H10 130 W, 11 D, 259 L).
Also 0 differences on 400 states of a 2 + 2 test group (`logs/val.log`, `logs/tiny.*`).

**Decisive entries** (`logs/ZO.out`, `logs/H10.out`):

- Z_O, d4 root, 1…e5–e4: in Att^B_0 (loses at once), **not** in Att^B_1 (one Black pass saves it), not in Att^B_∞.
  The same position after a White pass with Black to move is a Black win in P, so (V1) fails. Hence (T2) fails. AGREES.
- H10, White's Kg4–f3: in Att^W_0, **not** in Att^W_1 (one White pass saves it), at both roots. (V0) fails, so (T3)
  fails. AGREES.
- H10, my choice of Black non-shuttle move: 1…e5–e4 at the f6 root. It is in Att^B_1, so it is **not** saved by one
  pass, and (N1) holds; it is not in Att^B_∞. AGREES with pr56 ("unlimited only").

All other root moves of both groups agree with `logs/B_ZO_c8.out` and `logs/B_H10_c10.out` move for move: Att^X_0,
Att^X_1, Att^X_∞, (N1)/(V1), (N∞)/(V0), and the freezes and their (O3)/(O4) tests. That includes Z_O's e2–e4 at the
d5 root (saved by one pass; it gives check, so (V0) fails), and H10's e2–e4 at f6, e2–e3 at g6 (saved by one pass)
and Kg4–g3 at g6 (in Att^W_1, not in Att^W_∞). So for these two groups the statements "tempo-exact: no, and these are
the failing root moves" and "(T2) holds for H10, fails for Z_O" are **CHECKED-2**. The cyl:8×7 groups and the flat
translates were not re-run: COMPUTED-1.

## 3. Problems found

1. PROOF.md §1, "Monotonicity", is false in general (a forced pass against a stalemate draw; `src/mono.py`). Definition
   1′'s "⇒ tempo-exact" and the EDITS sentence "implies tempo-exactness" rest on it. Corrected in `verify/EDITS.md`
   to "is also sufficient (the same proof with an unlimited budget)".
2. EDITS.md calls the proof "not refereed" and gives all of Part A as COMPUTED-1. Updated: refereed, and CHECKED-2 for
   the Z_O and H10 root entries.
3. EDITS.md does not say in so many words that H10 = over stays open, and it says "no exact group found so far"
   only in the K47 bullet. Both are now explicit.
4. Minor, not changed: Part A's "smallest number of passes that saves it" presumes monotonicity. Read it as "the
   smallest k ≤ 8 for which the move is not in Att^X_k".

## 4. Edits

- Investigator's `EDITS.md`: 2 applied, 0 rejected, table cell counts unchanged, bold balanced. **Do not apply** (problems
  1 to 3).
- **Apply `verify/EDITS.md`**: `.venv/bin/python kings/delegate/apply_edits.py kings/theory/LOOPY.md <out> kings/delegate/out/K56/verify/EDITS.md`
  gives 2 applied, 0 rejected, table cell counts unchanged (`diff` of `awk -F'|'` field counts is empty), and bold
  markers balanced (958 → 966). Labels: Lemma 4.13 PROVED (hand proof, refereed); toy test COMPUTED-1; Part A
  CHECKED-2 for Z_O and H10, COMPUTED-1 for the other seven groups; sums COMPUTED-1. The scratch copy was deleted.

## 5. Process

All solver runs went through `kings/delegate/heavy.sh` under `/usr/bin/time -l`; their PIDs are in `verify/pids.log`.
I measured the smallest input first (a 2 + 2 group, 14 MB). Peak memory: vg on Z_O 1.28 GB, vg on H10 0.87 GB,
kp_p 33 MB; the Python toy runs are small (not measured). I signalled no process. Binaries were deleted. No output file is over 256 KB.
I made no git changes and edited nothing outside `K56/VERIFY.md` and `K56/verify/`.
