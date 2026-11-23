# K49 referee report (the ON class of K+P v K on the cylinder, LOOPY §8 item 5)

Referee, 2026-11-23. One referee, same model family as K49. My files are in `kings/delegate/out/K49/verify/`:
- `vk.c`: my own solver for x ⊞ T (P model, convention (N), Black may not move in T while in check, promotion = ⊕, Kxp = dead
  draw or, with `-k`, a Black win; any finite T from a text file). Written from `kings/SPEC.md` and LOOPY Definitions 1.2, 1.3,
  1.5. I did not read K49's `kn.c`. The binary was built as `verify/vk` and deleted at the end.
- `mkt.py` (test-game files in `t/`), `cmp40.py`, `lemmap.py`, `rule6.py`, `count6.py`, `fort.py`, `randT.py`; outputs in `verify/logs/`.
- `EDITS.md`: a full replacement set for K49's three edits.
All runs were seconds; the longest (random T on 8×8 and 7×8) about two minutes in all. No background job is left; nothing was killed.

## Verdict

**ACCEPT_WITH_FIXES.** Every computed number I re-ran is right, and every hand proof is sound or sound with a small fix.
The one real gap is in the written proof of Theorem 1: the direction "White needs no spare" (W(x ⊞ n) ⇒ W_N for n > 0) is
attributed to monotonicity, which gives the other direction. The statement is true given Lemma P, by the argument of
Theorem 4(iii). EDITS.md repeats the gap, mislabels Proposition 3 as dependent on Lemma P, overstates two interpretive
sentences, and leaves an orphaned K40 sentence under the new "What is computed only" bullet. Use `verify/EDITS.md`.

## 1. My solver against K40 (to calibrate it)

`cmp40.py`: vk.c against K40's (N) tables (CHECKED-2) for the 16 tests 0, ±1, ±2, ±3, on, off, dud, over, under, \*, ↑, ↓, ±1:
cyl:5×6, 8×8, 4×6, 3×8, 7×8: 9,376,224 results, **0 differences**, and the same set of legal positions (`logs/cmp40.log`).
The 4×6 board, which has Black wins, agrees as well.

## 2. Per-statement verdicts (hand proofs)

| Statement | Verdict | Notes |
|---|---|---|
| Setting (§0): (t, L) ∈ ON_T ⟺ (t, R) ∈ ON_T or some (t′, R) ∈ ON_T | SOUND | Left's options in on ⊞ T are the pass and her T-moves; Right never wins on ⊞ T (Left always has the pass), so r(on ⊞ T) ∈ {W, D}. |
| Lemma P′ (Lemma P ⟺ one Black spare never helps) | SOUND | ⇐: in y_b ⊞ (−1) Black's spare leads to y_w ⊞ 0 (legal because Black is not in check). ⇒: Theorem 1 with k = 1, which needs Lemma P on the whole board; it does. |
| Theorem 1 (r(x ⊞ n) = r(x ⊞ 0) for every integer n) | **SOUND WITH FIX** | The proof says "(⇒) for n ≤ 0 and (⇐) for n ≥ 0 are monotonicity; the real content is (⇐) for n < 0". That misses (⇒) for n > 0: W(x ⊞ n) ⇒ (x, s) ∈ W_N, i.e. "White needs no spare", one of the two claims in the theorem's title. Monotonicity only gives W_N ⊆ W(x ⊞ n). Fix: outside W_N, every White x-move stays outside W_N, a White spare leads from y_w ∉ W_N to y_b ∉ W_N (Lemma P, contrapositive; y_b is legal since y_w is), and a Black-to-move position outside W_N has a move that stays outside W_N or is Kxp (it is not stuck, since a stuck Black loses under (N)). So White never promotes and never leaves Black stuck in x ⊞ n, nor even in x ⊞ on: this is Theorem 4(iii)'s argument, which does not use Theorem 1, so there is no circularity. The (⇐, n = −k) strategy proof is right: the Black spare is legal only out of check, so Lemma P applies, and the pair (spares left, ρ) decreases lexicographically (ρ may rise after a spare, which is why the pair is needed). |
| Theorem 2 (lower bound for every terminal-free T) | SOUND | I re-derived the virtual-game argument. The T-coordinate of the virtual on ⊞ T is always the real one. A λ pass is replaced by a W_N move from y_w, which is in W_N by Lemma P, and y_w is legal because Black has just made a T-move, so he is not in check. The measure (virtual stage, ρ) is right: after a pass reply ρ may rise, but the first entry has dropped. W_N Black-to-move positions do not allow Kxp. Properties of T used: finite, terminal-free (no ⊖ for Right; no ⊕ needed for Left), and only the predicate (t, R) ∈ ON_T. The check rule only removes Black T-moves. Under (N) a Black with no move loses; White is never stuck at a W_N node (she has a winning option). |
| Corollary 2a (Right-finite T) | SOUND | Left passes until Right is stuck. With over = {0 \| over} and under = {under \| 0} (LOOPY Def. 4.4), the list (integers, \*, ↑, ↓, ±1, under, on, on + \*) is right. Lemma P is used whenever Black makes a T-move (λ always passes), so "as Theorem 2" is the right label. |
| Corollary 2b (over, no Lemma P) | SOUND | λ answers over → over by over → 0; a pass is never needed, so Lemma P is not used. For s = w White first plays her W_N move in x. |
| Proposition 3 (Right reserves) | SOUND | Black copies his dud strategy that avoids W(x ⊞ dud); White's T-moves stay in S and read as her dud pass; Black's dud pass becomes a Right move into S, legal exactly when not in check, which is also when the dud pass is legal in K40's sum. A Black with no move in x ⊞ T would have none in x ⊞ dud either. Uses W ≠ 4 (Black never wins, K40 Cor. 3) but **not** Lemma P. EDITS.md lists it under "Given Lemma P"; it is unconditional. |
| Theorem 4 (trichotomy DEC = P_L, ON = W_N ∖ P_L, DUD = ¬W_N) | SOUND | P_L ⊆ W_N is Theorem 3.11 with S = 0 (not stated, immediate). DEC: K40 Prop. 4. ON: Theorem 1, Cor. 2a, 2b, Prop. 3. Third item: the trap argument above plus Theorem 3.11 step (2) (White is never in check, so it survives the check rule, K40 Prop. 4) and K40 Cor. 3. Correctly labelled "PROVED given Lemma P". |
| Lemma P on rank H−1 | SOUND | The only White-to-move non-wins with the pawn on H−1 are W3; there wk is not next to p and bk = q is, so Black to move has Kxp (B1). Since play from rank H−1 stays on rank H−1 (until a promotion or Kxp), Theorems 1, 2 and 4 are PROVED outright for the pawn on rank H−1. K49 does not say this; the replacement edit does. |
| Proposition 6 (pawn on rank H−1) | SOUND (one vacuous clause) | I re-derived W1 (the four squares (f±1, H), (f±1, H−1), the "at most one side" file argument for W ≥ 5, W = 3 forces bk to rank ≤ H−2), the Π argument, W3, the bind B2 (for W = 3 all of Π is pairwise adjacent and both (f±1, H−1) are covered; for W ≥ 5 the far square is free only from r∓, and then White promotes), W2 in both sub-cases, B1, B3, B4. Remark: in B3 the step to q must not be met by Kxp, and every square next to q is next to p, so p is guarded and wk ∈ Π; hence B3 is **always** ON of type (on, L), never DUD. The "or DUD" in B3 is vacuous (894 B3 positions over the 18 boards of the 463,616 count, wk ∈ Π in all; `logs/count6.log`). Harmless. |
| Proposition 5 (ON is not one game) | SOUND | (T₀, L) ∈ ON_T (Left → 0, Right stuck), (T₀, R) ∉ ON_T (Right → off). `Kc6 Pa7 ka8 w`: W2 with wk one step from Π (c6–b6), type (on, R), so D against T₀; Black to move it is B1 (Kxp), so ON/DUD. `Kb6 Pa7 kb8 b`: Black in check, B3 (b6 ∈ Π guards a7, b6 not next to a8), so (on, L): W against T₀. |
| Conjecture 7 (two types) | Label right (CONJECTURE; PROVED on rank H−1) | |
| Proposition 8 (forced Kxp ⇒ DUD) | SOUND | This is the L-line of Theorem 3.11 (L(K ⊞ on) ⇒ L(K ⊞ S)) for x′ with Kxp = ⊖, i.e. step (1) with colours exchanged; White's T-moves become her pass in on (always legal, White is never in check), and Black's real moves are x-moves, legal exactly when they are virtually. Then Kxp is a dead draw (K40 Lemma 1), and Black never wins (K40 Cor. 3). |
| Fortress "explanation" | Not a proof; correctly labelled | It does not explain why 3 files (back files f±1, adjacent) have none, or why 7×6, 9×6, 9×7 have none while 5×6 has 30. |

**Labels.** "PROVED given Lemma P" is used consistently in PROOF.md, and findings.txt says which step is computed. Two
blemishes: (a) "Theorem 1 ... hence CHECKED-2 for every integer n" mixes a hand proof with a computed lemma; better "PROVED
given Lemma P, which is CHECKED-2 on these boards". (b) EDITS.md puts Proposition 3 under "Given Lemma P" (it is PROVED
outright) and calls Theorem 4(iii) "by Theorem 3.11" without naming Lemma P. Neither labels a conditional statement as plain
PROVED; the replacement edit states the scope explicitly.

**The check rule and (N).** Checked in every proof: Black's T-moves (and spares) exist only out of check, which is exactly
when Lemma P is applicable (y_w legal); Kxp is a king move and legal in check; Black on q is never in check; White is never in
check, so her T-moves and passes are always legal; a Black with no move loses under (N), and White always has a move when
W ≠ 4 (K40 Lemma 2). No proof uses a move that the check rule forbids.

## 3. Computations re-run with my own solver

| Claim | My result | Status |
|---|---|---|
| Lemma P on cyl:3×6, 5×6, 6×6, 7×6, 8×6, 8×8 | 0 violations (`logs/lemmap.log`) | CONFIRMED (CHECKED-2 already via K40) |
| Lemma P on cyl:3×10, 5×10, 9×8, 10×10 (K49: COMPUTED-1) | 0 violations; placement counts equal kn.c's (13,518; 76,610; 234,198; 703,620) | now **CHECKED-2** on these four boards |
| Lemma P false on 4 files: 8, 8, 12, 16, 20, 24, 28 violations on cyl:4×4…4×10 | Same counts. In every violation y_w is **D**, not L | CONFIRMED, CHECKED-2. So the violations are not White stalemates; the 4-file Black wins (White stalemated, Lemma 2) are a separate phenomenon. PROOF.md's parenthesis "(finite thresholds; White can be stalemated in front of the pawn)" and the edit's "this is where K40's 4-file anomalies come from" overstate the link. |
| Theorem 1 for n = −3…3 | 0 positions with r(x ⊞ n) ≠ r(x ⊞ 0) on cyl:3×6, 5×6, 6×6, 7×6, 8×6, 8×8, 3×10, 5×10; 108–796 on the 4-file boards | CONFIRMED |
| Prop. 5 examples on cyl:8×8 | `Kc6 Pa7 ka8 w`: D against {0 \| off}; W against 0, on, −3, +1; D against off, dud. `Kb6 Pa7 kb8 b`: W against {0 \| off}; same ON signature (`logs/prop5.log`) | CONFIRMED |
| Prop. 6 rule (class and type) | 0 exceptions on cyl:3×6, 5×6, 7×7, 8×8, 9×8 (166,710 positions). Class from 16 tests; type from {0 \| off} and {0 \| dud} (each separates (on, L) = W from (on, R) = D) (`logs/rule6.log`) | CONFIRMED |
| 463,616 positions with the pawn on rank H−1 (W ∈ {3, 5, …, 9}, H ∈ {6, 7, 8}) | 463,616 legal positions (`logs/count6.log`) | CONFIRMED (count) |
| Only DEC/ON/DUD on W ≠ 4 | 0 "other" signatures on the five boards above | CONFIRMED |
| Fortresses: 5×6 30, 5×7 100, 5×8 170, 7×7 182, 7×8 378, 9×8 522; none on 3×8, 6×8, 7×6, 8×8, 9×6, 9×7 | All counts reproduced (`logs/fortress.log`) | CONFIRMED; 9×8 = 522 now CHECKED-2 |
| Fortress geometry: back files; White to move same file; Black to move different files except 10 (5×7) and 20 (5×8) on the same file at rank distance 5; rank distance ≥ 2 | All reproduced on every fortress board | CONFIRMED |
| Random T (Theorem 2, Prop. 3, Theorem 4(iii), two types) | 1,300 random T of 1–4 nodes on cyl:5×6, 6×6, 7×6, 8×8, 3×8, 7×8: 0 violations of each (`logs/randT.log`) | CONFIRMED for Theorem 2, Prop. 3, Thm 4(iii). For the two-type pattern my generator produced only 12 T that separate (on, L) from (on, R), so my check of Conjecture 7 is weak; it rests on K49's run |

## 4. Problems

1. **Theorem 1, gap in the written proof** (statement true given Lemma P). "White needs no spare" (⇒ for n > 0) is not
   monotonicity; it needs the closure of ¬W_N under White's pass (Lemma P) as in Theorem 4(iii). EDITS (i) describes only
   the Black-spare strategy. Fixed in the replacement edit.
2. **Proposition 3 is unconditional** (given W ≠ 4); EDITS lists it under "Given Lemma P". Fixed.
3. **The 4-file link is overstated.** The Lemma P violations are draws with White to move, not White stalemates; the 28
   Black wins per 4-file board come from Lemma 2's failure. "Every 4-file cylinder" means H = 4…10. Fixed.
4. **"No comparably short rule exists two ranks down"** (EDITS) is not shown; K49 only found none (and findings.txt says so).
   Fixed to "no short rule was found".
5. **"The fortress needs height"** is wrong as a general statement: cyl:5×6 has 30. True for 7 and 9 files on the boards
   run. Fixed.
6. **Orphaned text.** K49's OLD replaced only the first line of the K40 bullet, so "No number and no infinitesimal occurs…"
   ended up under "What is computed only. Lemma P below the last rank." The replacement edit takes all three lines as OLD and
   keeps K40's sentence as its own bullet. "Below the last rank" is also ambiguous (the pawn never stands on rank H); now
   "for the pawn below rank H−1".
7. **Minor.** Proposition 6 B3's "or DUD" is vacuous; Theorems 1, 2, 4 are PROVED outright on rank H−1 (not stated); the
   label "CHECKED-2 for every integer n" should read "PROVED given Lemma P, which is CHECKED-2 there".

## 5. EDITS.md

K49's EDITS.md applies to a scratch copy of the current LOOPY.md: 3 applied, 0 rejected. `verify/EDITS.md` (same three
titles; 8.5a now takes the three-line K40 bullet as OLD; every OLD occurs once) applies: 3 applied, 0 rejected. Changes
against K49's edits:
- 8.5a: Theorem 1's "White needs none" argument added; Proposition 3 moved to "PROVED without Lemma P"; Lemma P CHECKED-2
  also on cyl:3×10, 5×10, 9×8, 10×10; the 4-file sentence corrected (H = 4…10, violations are draws, Black wins have another
  cause); scope sentence that (i)–(iii) carry the label of Lemma P on each board, and are PROVED outright for the pawn on rank
  H−1; B3 stated as always ON; "no short rule was found" instead of "no comparably short rule exists"; the referee's
  re-check of the rule (166,710 positions on five boards) and of the 8×8 examples cited; the K40 "no number" sentence kept
  as its own bullet; "What is computed only: Lemma P for the pawn below rank H−1".
- 8.5b: "needs height" restricted to 7 and 9 files; counts and geometry marked CHECKED-2; the odd-width explanation marked
  as a heuristic, with the 3-file exception noted.
- 8.5c: "below the last rank" → "for the pawn below rank H−1"; otherwise unchanged.
