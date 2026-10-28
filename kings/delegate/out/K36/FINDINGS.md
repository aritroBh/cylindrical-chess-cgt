# Findings: blind review of Theorem 2.7

Theorem 2.7(a) and (b) are **PROVED** in P by the blind derivation and the comparison below.
The proof transfers a local winning strategy through π, with context-pawn moves represented by passes.
(L2) blocks an unrepresented context promotion before the local deadline; (L3) excludes real stalemate.
LOOPY's move-legality and timing steps are sound; Step 0 has one repairable invocation gap for (b).
No solver was run; the listed counterexamples remain reported data, not independently checked here.

## Route compared with the blind proof

My proof established the projection and timing directly, then listed where each hypothesis is needed. LOOPY expands that simulation into pawn/file, attack, and en-passant invariants (I1–I5), followed by move-type checks. Its Step 4 gives a more explicit deletion argument for μ_s than my direct mapping of an actual s-move sequence into Q°. Both routes use the same decisive separation: Z-pawn promotions are visible to (L1), context promotions are bounded by (L2), and stalemate is handled only by (L3). Neither route promotes a passer to a terminal in P.

## Step-by-step audit of LOOPY's proof

- **Step 0, I1 — GAP (repairable).** Lemma 2.2 is stated for Definition 2.1, whose initial setup puts both kings on F_Z. Part (b) allows s's king elsewhere, so the sentence “Lemma 2.2, applied from Q” invokes the lemma outside its stated setup. The pawn/file/buffer conclusion follows directly by induction from (b)'s explicit pawn placement and empty-buffer conditions: pawns stay on their file, cannot move sideways, and promotions are excluded until the first promotion. State that short argument or state the invariant in that broader form. No counterexample to the invariant follows.
- **Step 0, I2 — SOUND.** Pawn attacks are to adjacent files; the one-file buffer and distance-at-least-two context keep context pawns from attacking F_Z. A Z-pawn's diagonal capture cannot reach a context file across the empty buffer.
- **Step 0, I3 — SOUND.** The guided strategy confines s̄'s king to F_Z, and it starts there by hypothesis.
- **Step 0, I4 — SOUND.** s̄ context pawns stay fixed or are removed. Their attack set only shrinks, and legal king moves cannot enter an attacked square. Thus the only check on s relevant to projection is from retained Z-pawns; this also justifies treating a context-pawn move as a pass only when s is not checked.
- **Step 0, I5 — SOUND.** A right created by a guided s̄ Z-pawn double step has target on F_Z and is available to a Z-pawn. A right created by s cannot be used by s's own context pawn; an off-F_Z right already at Q is the only context en-passant capture available to s, and it expires after s's first turn. The on-F_Z case is retained by π.
- **Step 1 — SOUND.** Each real king or Z-pawn move projects to the same legal local move; a king capture of a context pawn becomes a king step to an empty square. Context-pawn moves, including the one possible off-F_Z en-passant capture, leave the projection unchanged and are legal passes because they cannot answer a Z-pawn check. Context promotions are deferred to Step 4, where they are excluded by (L2).
- **Step 2 — SOUND.** The local permitted s̄ moves see the same F_Z occupancy and on-F_Z en-passant right. Context pawns do not attack the destination king square, and all other king/pawn attacks are represented in π. With no officers there are no slider pins omitted by projection.
- **Step 3 — SOUND.** Before the local win, the local winning strategy has a legal permitted move. Step 2 makes it a legal real move, so s̄ cannot be stuck or stalemated.
- **Step 4 — SOUND.** A Z-pawn promotion by s is a forbidden failure along the (L1) winning line. For a context promotion on s's j-th turn, delete s̄'s moves and s's Z-pawn moves. The remaining s king/context-pawn sequence is legal in Q°: deleted pieces only remove blockers and attacks; s̄ context pawns remain fixed; the king and context pawns retain their real squares; and the sole possible off-F_Z en-passant capture is available only on the first turn and is retained by Q°. This yields μ_s ≤ j ≤ T, contradicting μ_s ≥ T+1. A context passer that has not promoted is not terminal in P.
- **Step 5 — SOUND.** Step 3 excludes s̄ being mated or stalemated before its win. (L3), not (L1), excludes a real stalemate of s. The guided local win is bounded, so no infinite play remains.
- **Step 6 — SOUND.** The projected local game ends by s̄'s T-th move through an allowed promotion or mate. A local promotion is a P win when made by s̄; for a local mate of s, Step 1 preserves all legal s moves and checks, and no pass is available in check. Thus the real result agrees and the move count is correct.
- **Part (b) bridge — SOUND, with the I1 repair above.** Its hypotheses supply the starting placement, empty buffer, no officers, s̄ king location, no s̄-context-pawn check, and en-passant handling used in I1–I5. The proof is independent of how Q arose.
- **Part (a) reduction — SOUND.** After legal non-promoting m and r, the window starts with s to move; r is a Z-move, so any new en-passant target is on F_Z. The certificate hypotheses apply and the window result gives the stated T-move bound after r.
- **K3 objection remark — SOUND.** A passer is not terminal in P; only promotion is. The distinction from D is necessary, and (L2) bounds the relevant actual promotion.

No step is FALSE. The I1 gap is a missing invocation condition in the written proof, not a counterexample: its claim follows from a one-line pawn-movement induction and does not require either king to be on F_Z.

## “The conditions cannot be dropped” list

The list is consistent with the theorem's scope. It supplies examples against omitting (L3), the main μ_s condition in (L2), the off-F_Z en-passant clause, and the exact μ_s ≥ T+1 threshold; it also identifies (L1) as the substantive local-win premise. The EP example explains why the first draft of (b) was false and why part (a), after r clears m's right, does not cover that case. The chess counterexamples in “What Theorem 2.7 does not give” also correctly keep (A_Q) separate from this P theorem.

These examples are reported in LOOPY as `CONJECTURE`/computed data under the project's label rules. I did not run the private P solver or recheck their values, so I make no independent claim about those computed outcomes. No example or omitted-hypothesis counterexample was run as part of this task.

## Tests and recommendation

- **Tests run:** none. This review was a proof audit; no solver or computation was run.
- **Exact reproduce command for test counts:** not applicable; there are no computed counts in this report.
- **Recommended label:** **PROVED (in P), after repairing Step 0's invocation of Lemma 2.2 as noted.** The theorem does not establish a chess win or a D-model result. The theorem's listed solver examples remain at their existing data/CONJECTURE status.
