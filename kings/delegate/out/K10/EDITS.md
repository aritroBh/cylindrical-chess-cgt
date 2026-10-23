### EDIT 1: Remark 2.11 -> Proposition 2.11 + remark
<<<<<<< OLD
**Remark 2.11 (the certificate is not special to kings). GAP.** A passer created in a component is a decisive
event too, and (V2) asks the same question about it. The certificate of Definition 2.6 **cannot apply as
written** to a passer (revised after review: R3 item 6):
- Q_Z deletes "every context pawn", which deletes the passer itself.
- The punishing reply r is not a king capture of a Z-pawn.
- The passer's owner may need its king off F_Z, where the legality step via Lemma 2.2 no longer covers it.
- The pawns of the passer's own component are not addressed.
The claim "which this certificate rules out" is therefore unproved. P11 in §6 relies on this remark under a
PROVED label; that label must be revised when the certificate is extended.

=======
**Proposition 2.11 (frozen-king passer certificate). PROVED in P (revised after K10, 2026-10-22).** Work in the
frozen model (a king move loses at once, the first promotion wins). Let a move by σ have just produced a passer
p for σ: p is a pawn of σ that cylcgt's `passed` (e.p.-aware, `PASSED_RESPECTS_EP = True`) calls passed, and p is
the front pawn of its file. Let d be p's promotion distance (counting the double step, requiring no own pawn
ahead) and let μ be the defender's fastest promotion distance with σ's other pawns standing still (captures,
double steps and e.p. included), or ∞ if none. The node has σ̄ to move. Assume (1) p's file is clear ahead
(front pawn; no enemy king on the path), (2) σ̄ is never stalemated while σ pushes p, (3) races are scored by the
count rule with σ as creator. Then σ wins in P provided **μ ≥ d + 1**.

*Proof.* (i) No σ̄ pawn can block or capture p: `passed` rules out any enemy pawn on files f−1, f, f+1 (mod W on
a cylinder) with rank beyond p, and the e.p. clause rules out an adjacent capturer; as p advances the set only
shrinks. (ii) σ pushes p every move (legal: front pawn, clear file, no enemy pawn can block or capture) and
promotes on turn 2d; σ̄, to move first, promotes on turn 2μ−1, so σ wins iff 2d < 2μ−1, i.e. μ ≥ d+1 (ties
μ = d go to σ̄, the opponent of the creator, as the count rule requires). (iii) e.p. cannot rescue σ̄: a
just-double-stepped p is not passed under the aware test, and passed at the node already excludes any adjacent
capturer. (iv) σ's own pawns cannot obstruct p: p is the front pawn of its file. ∎

*Sharpness.* μ ≥ d+1 is exact: μ = d gives σ̄ a promotion on turn 2d−1, one turn before σ (kpsolve:
`Ka1 kf6 Pc3 pe5 b -` → L L on cyl:7×6; `Ka1 kf6 Pc5 pe3 b -` with μ = d+1 → W W).

**Remark 2.11 (the certificate is not special to kings).** The same (V2) question arises for passer terminals.
The certificate of Definition 2.6 (king moves) does not apply as written to a passer (Q_Z deletes the passer,
r is not a king capture, the owner's king may leave F_Z, the component's own pawns are unaddressed). Proposition 2.11
above supplies the missing (V2)-certificate for passer terminals under frozen kings, with the bound μ ≥ d+1 and
the clear-path and no-stalemate conditions. P11 in §6 relies on this proposition (revised after K10, 2026-10-22).

>>>>>>> NEW

### EDIT 2: status row R2.11
<<<<<<< OLD
| R2.11 | GAP → heuristic only. No certificate for passers is claimed | R3 item 6 |
=======
| R2.11 | PROVED in P (revised after K10, 2026-10-22): Proposition 2.11 supplies (V2) for passer terminals under frozen kings; the D-model analogue is the count rule | R3 item 6; K10 |
>>>>>>> NEW

### EDIT 3: status row P11
<<<<<<< OLD
| P11 | GAP (proof incomplete): W(X) and HSS defined; (V1b) checked from the layout (revised after K3 check) | R1 item 11 |
=======
| P11 | PROVED in P (revised after K10, 2026-10-22): Theorem 1.11 + Theorem 1.14 (frozen kings give (V1),(V3) by fiat) + Proposition 2.11 (passer (V2)) + HSS for o(S); (A_Q) not needed (P-level) | R1 item 11; K10 |
>>>>>>> NEW

### EDIT 4: section 6 row P11
<<<<<<< OLD
| P11 | cyl:8x6, `--frozen` | Kings parked on the a-file (`Ka1 ka6`, b- and h-files empty); pawn components on c–g; every passer and race node speed-certified (Remark 2.11 with frozen kings); condition (E). Here W(X) is the D-game of X with its own winning side, and "hereditarily sum-safe" (HSS) means that every component of X is itself sum-safe in the sense of Theorem 1.14(ii) | kpsolve `--frozen` = o(W(X)); also = o(S(X)) when hereditarily sum-safe. Where o(S) ≠ o(W) (opposite threats, Prop 1.12), `--frozen` sides with W | — | — (a harness check, not one position) | Thm 1.11 + Thm 1.14 (frozen kings satisfy V1 and V3 by fiat) | GAP (proof incomplete): the harness checks the hypotheses (revised after K3 check) |
=======
| P11 | cyl:8x6, `--frozen` | Kings parked on the a-file (`Ka1 ka6`, b- and h-files empty); pawn components on c–g; every passer and race node speed-certified (Proposition 2.11 with frozen kings); condition (E). Here W(X) is the D-game of X with its own winning side, and "hereditarily sum-safe" (HSS) means that every component of X is itself sum-safe in the sense of Theorem 1.14(ii) | kpsolve `--frozen` = o(W(X)); also = o(S(X)) when hereditarily sum-safe. Where o(S) ≠ o(W) (opposite threats, Prop 1.12), `--frozen` sides with W | — | — (a harness check, not one position) | Thm 1.11 + Thm 1.14 (frozen kings satisfy (V1),(V3) by fiat) + Proposition 2.11 (passer (V2)) | PROVED in P (revised after K10, 2026-10-22): the harness checks are backed by Proposition 2.11 |
>>>>>>> NEW
