## 3. Exact under and over groups (class b): the over half of §8 item 2, and Conjecture 4.7

Search: White's king shuttles on a pair z, Black's king stands on one square b0 (K1, K2), at most n_W + n_B pawns on F_Z, four roots; then the freezes at the two Black-to-move roots are followed to the positions q (`over3.py`, written for K26).
The search for under with (n_W, n_B) covers over with (n_B, n_W) by the colour mirror.

**Lemma 4.9 (no king freeze) — PROVED (hand proof; the filter of `over3.py` rests on it, and the unfiltered runs `over2.py` agree).**
*In an exact under group (U1)–(U4) no freeze is a king move that captures nothing.*
*Proof.* Let m be a freeze b0 → b1 that captures nothing, q the position after it. In q Black can play b1 → b0: b0 is empty (the king just left it), no White pawn attacks it (K1), and it is not next to the White king, which has not moved (K2 at the root); no pawn has moved, so there is no e.p. right.
The result is the root with White to move. By (U2) and (U3) the other Black-to-move root has a freeze to a position of value L (White has lost), so that root has value L. At the first root every non-shuttle White move loses at once (U1) and the shuttle leads to the second root, value L.
So the first root has value L: the move b1 → b0 is a legal Black move at q that does not lose at once, and (U4) fails. ∎
So the freeze of an exact group is a pawn move or a king capture of a pawn of the group. (A Black promotion as a freeze is a decisive event, not a group move; those placements are counted separately.)

**Result: no exact under or over group was found in any searched range.** The fresh run of `over3.py` (`scripts/queueF_over.sh`) did not get a slot of the shared lock before the time limit of this attempt; the table therefore lists the earlier attempt's runs (reused; same scripts, same source md5, the fresh two-shuttle and one-shuttle searches that feed them reproduced exactly). Rows from a fresh run appear first if there are any.

@@OVER3@@

(Reused, not re-run: four files a–d on cyl:8×6 with at most 2 + 2 pawns, 5,793,156 placements: 66,476 pass the king filter and (U1)–(U3) at one root, 55,331 at all four roots, 41,169 fail (U4), 14,162 have a promotion as the freeze, **0 exact groups**; `logs/over3_cyl_8x6_22_nf4_*`.
The unfiltered runs `over2.py` (no use of Lemma 4.9) on cyl:7×6, cyl:8×6, flat 7×6, flat 8×6 with at most 2 + 2 pawns also give 0 exact groups: `logs/over2_*_22.json`.)

**Loose under/over groups are plentiful, but they are not over_D.** Loose = (U1)–(U3) with exactly one freeze at each Black-to-move root (`over_exact` in the t1 table of section 4): 118 on cyl:7×6, 120 on cyl:8×6, 142 on flat 7×6 and flat 8×6, 586 on flat 7×7 for at most 2 + 2 pawns (see the t1 table; 626 on cyl:8×6 with four files, reused).
After the freeze only White is in zugzwang; Black still has a move that does not lose. Beside contexts Proposition 4.6 (and its mirror) holds in 537 of the 552 premise roots of the fresh sampled run (section 6; 762 of 768 in the earlier attempt's different sample), so the loose groups are not over_D. The failing roots were not diagnosed.

**Verdict on Conjecture 4.7 (P model, COMPUTED-1 as a search; exact boundaries above).**
- First half ("no over-type group with at most 2 + 2 pawns fits on 3 files of the 8×6 cylinder"): **supported**. No exact under/over group exists with at most 2 + 2, 3 + 2 or 2 + 3 pawns on 3 files of cyl:8×6, nor with at most 2 + 2 on cyl:7×6, flat 7×6 and flat 8×6 (the 2 + 2 runs without the king filter); nor with at most 2 + 2 on 4 files of cyl:8×6.
  Not searched for exact under/over: 3 + 2 and 2 + 3 on cyl:7×6 and flat 7×6, and flat 7×7 (the queue for them never got a lock slot).
  Lemma 4.9 shrinks the freeze to pawn moves and king captures.
- Second half ("over is realisable on the cylinder with wider groups"): **neither supported nor refuted.** Nothing wider than 4 files, 3 + 2 pawns, or the pawns-on-F_Z-only setting was searched.
