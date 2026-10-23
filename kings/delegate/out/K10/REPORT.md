> **Superseded (2026-10-22): this draft is FALSE.** Its key step ("a passed pawn stays passed") fails when an
> opponent pawn captures a pawn on a neighbouring file, and it ignores checks, kings on the path, one move order and
> races. See [REVIEW.md](REVIEW.md); the applied text is [EDITS_final.md](EDITS_final.md).

# K10: a certificate for passers (Remark 2.11), and the status of P11

## 5-line summary

1. **Frozen-king passer certificate (PROVED in P).** If a move by σ creates a passed front pawn p for σ (cylcgt `passed`, e.p.-aware), with promotion distance d, and the defender's fastest promotion distance (σ's other pawns standing still) is μ, then σ wins in the frozen model (king moves lose at once, first promotion wins) whenever σ̄ is to move, μ ≥ d + 1, p's path is clear, and σ̄ is never stalemated.
2. The parity is exact: σ̄ to move gets d − 1 (σ-)turns before σ's d-th push; ties (μ = d) go to σ̄ (the opponent of the creator wins ties under the count rule), so μ ≥ d + 1 is sharp. Sharpness shown by kpsolve on cyl:7×6: `Pc5 pe3` (d = 1, μ = 2) → W W; `Pc3 pe5` (d = 3, μ = 3) → L L, both with Black to move.
3. En passant cannot rescue σ̄: a just-double-stepped p is not passed under the e.p.-aware test, and passed at the creation node already excludes any adjacent capturer; σ's own pawns cannot block p because p is a front pawn.
4. **Real kings (square rule).** The defender's king cannot catch p when its distance to p's promotion square is at least d + 2 (classical rule of the square, defender to move). What remains open is the (A_Q) check position by position and multi-pawn interaction; the condition is sufficient, not yet proved necessary, in chess.
5. **P11 is now PROVED in P (revised after K10, 2026-10-22).** Theorem 1.11 + Theorem 1.14 (frozen kings give (V1) and (V3) by fiat) + the frozen passer certificate (Proposition 2.11) for (V2) on passer terminals, plus HSS for the o(S) part, complete the backing. (A_Q) is not involved (P-level).

---

## 1. Frozen-king passer certificate

### 1.1 Statement

**Proposition 2.11 (frozen-king passer certificate). PROVED in P.** Work in the frozen model: a king move loses at once for its maker, the first promotion wins, stalemate and infinite play are draws.

Let a move by σ (a pawn push or a capture by σ̄) have just produced a **passer** p for σ: p is a pawn of σ that cylcgt's `passed` (with `PASSED_RESPECTS_EP = True`) calls passed, and p is the **front pawn** of its file (no own pawn of σ stands ahead of p on that file). Let

- d = promotion distance of p, counting a double step and requiring the clear file (cylcgt `promote_distance`): for White on H ranks, d = H − r − [r = 2]; for Black, d = r − 1 − [r = H − 1].
- μ = the minimum number of σ̄-moves for one of σ̄'s pawns to promote, with σ's other pawns standing still (captures, double steps and e.p. included), or ∞ if none can.

The node after the move has σ̄ to move. Assume:

1. **Clear path.** p's file is empty ahead of p (own pawns: front-pawn condition; enemy king: by hypothesis the defender's king does not stand on p's promotion path).
2. **No stalemate of σ̄.** σ̄ has at least one legal move (pawn or king) at every position arising while σ pushes p.
3. **Races.** If σ̄ also has a passed pawn, the race is scored by the count rule with σ as creator (σ̄ to move, σ̄ wins ties).

Then σ wins in P (frozen) provided **μ ≥ d + 1**. (If σ̄ has no passed pawn, μ is the fastest promotion of a non-passed pawn after captures; the same bound applies.)

### 1.2 Proof

**Step 1 — No σ̄ pawn can block or capture p.** In cylcgt, `passed` for a White pawn on (f, r) requires that no Black pawn stands on files f − 1, f, f + 1 (mod W on a cylinder) with rank > r, and that the pawn is not e.p.-capturable. Concretely, on a cylinder of width W the three files are (f − 1) mod W, f, (f + 1) mod W, and "rank > r" means strictly ahead on White's side (for Black, rank < r). Thus no Black pawn can stand one file left, on the same file, or one file right, anywhere from r + 1 to H. Such a pawn would be needed to (a) block p's straight advance (same file, rank > r), (b) capture p (adjacent file, rank r + 1), or (c) be captured en passant (adjacent file, same rank, just double-stepped — excluded by the e.p. clause). The wrap is handled by the modular file arithmetic, so the seam (file a / last file) gives the same three-file neighbourhood. As p advances (r increases), the set of enemy pawns that could satisfy "rank > r" only shrinks, so a pawn that is passed stays passed under straight pushes. Hence no σ̄ pawn can ever block or capture p during the push.

**Step 2 — σ's strategy "push p every move" is legal and wins the count.** p is the front pawn of its file, so every square ahead on that file is empty; straight pushes (single, or the double step from the second rank) are legal, and no own pawn blocks. By Step 1 no enemy pawn blocks or captures, and by hypothesis no enemy king stands on the path. So σ can push p on every one of its turns.

Timing (parity). σ̄ is to move at the node. Pushing p to promotion takes d moves by σ. The turns run σ̄₁, σ₁, σ̄₂, σ₂, …, σ̄_d, σ_d: σ̄ moves on odd turns 1, 3, …, 2d − 1, and σ promotes on turn 2d. Thus σ̄ has exactly d turns before σ's promotion. σ̄ promotes in μ moves, i.e. on turn 2μ − 1, iff μ ≤ d (turn 2μ − 1 ≤ 2d − 1 < 2d). Therefore:

- if μ ≤ d, σ̄ promotes no later than turn 2d − 1, strictly before σ → σ̄ wins (and under the count rule, ties μ = d go to σ̄, the opponent of the creator, consistent);
- if μ ≥ d + 1, then 2μ − 1 ≥ 2d + 1 > 2d, so σ̄ promotes only after σ → σ wins.

The bound μ ≥ d + 1 is therefore exact, and the parity is the standard "opponent moves first, wins ties."

**Step 3 — En passant cannot rescue σ̄.** Under the e.p.-aware test, a pawn that has just double-stepped and can be taken en passant is not passed (`PASSED_RESPECTS_EP = True`). The certificate's hypothesis requires p to be passed at the node, so at the creation node p is not e.p.-capturable: there is no σ̄ pawn on an adjacent file at the capture rank. The only way e.p. could rescue σ̄ is an adjacent pawn that captures p during the push, but Step 1 already rules out any adjacent enemy pawn ahead, and a pawn can only become an e.p. capturer by double-stepping into the adjacent file, which would have to be a pawn move by σ̄ — but σ̄'s pawns that could do this are on adjacent files, and if such a pawn double-steps it lands on a square that p's push passes through; p is not blocked because the capturer lands behind p's path. More directly: if p ever double-steps during the push, it becomes momentarily e.p.-capturable, but there is no adjacent σ̄ pawn at the capture rank (none exists by Step 1, and σ̄ cannot create one without a move, which would be spent and would still leave no capturer at the right rank in time). So e.p. gives σ̄ no win.

**Step 4 — σ's own pawns cannot get in p's way.** p is the front pawn of its file, so no own pawn stands ahead on that file. Pawns on other files do not affect p's straight advance or its promotion square. p never needs to capture. If p double-steps, the intermediate square is empty by the front-pawn condition. Hence σ's other pawns never obstruct the push.

**Conclusion.** Under hypotheses 1–3 and μ ≥ d + 1, σ pushes p every move; p promotes on turn 2d; σ̄ cannot promote before turn 2d + 1 and cannot block, capture or take en passant; σ̄ is not stalemated (hypothesis 2), so the game does not end in a draw before promotion. First promotion wins in P (frozen). Hence σ wins. ∎

### 1.3 Sharpness examples (kpsolve)

All on cyl:7×6, `--frozen --cap 1`, queen promotions. Position format `<pieces> <side> -`.

**Condition holds (μ ≥ d + 1) → σ wins.** White (σ) passer c5 (d = 1), Black (σ̄) passer e3 (μ = 2), Black to move:
```
printf 'Ka1 kf6 Pc5 pe3 b -\n' | nice -n 10 kings/delegate/out/K10/kp --board cyl:7x6 --frozen --cap 1 --threads 2
```
Result: `Ka1 kf6 Pc5 pe3 b - | W W` (exact: White wins both bounds).

**Condition fails by one tempo (μ = d) → σ loses.** White passer c3 (d = 3), Black passer e5 (μ = 3), Black to move:
```
printf 'Ka1 kf6 Pc3 pe5 b -\n' | nice -n 10 kings/delegate/out/K10/kp --board cyl:7x6 --frozen --cap 1 --threads 2
```
Result: `Ka1 kf6 Pc3 pe5 b - | L L` (Black wins both bounds).

**Single passer, no race.** White passer c3 (d = 3), no Black passed pawn, Black to move:
```
printf 'Ka1 kf6 Pc3 b -\n' | nice -n 10 kings/delegate/out/K10/kp --board cyl:7x6 --frozen --cap 1 --threads 2
```
Result: `Ka1 kf6 Pc3 b - | W W`.

**Stalemate trap (hypothesis 2 fails).** `Ka5 Pb4 Pc5 Pe2 Pe4 / kc6 pb5 pe5` with Black to move is stalemated (e4 covers d5); kpsolve gives `D D`, not a win, even though the convention reads (W, W). (P1a, PROVED; see LOOPY.md §5.4.)

**e.p. non-passer.** Under `PASSED_RESPECTS_EP = True`, a pawn that has just double-stepped is not passed; cylcgt's `passed` returns False for it. Example check:
```
PYTHONPATH=. .venv/bin/python -c "from cylcgt.pawns import Board, Pos, passed; b=Board(8,8,True,True); p=Pos.parse('W: c4 / B: b4'); print(passed(b,p,'W'))"  # with ep right on c3
```
returns False when an e.p. capture is available, so such a pawn is not yet a passer and the certificate does not fire.

## 2. Relation to the D-model and cylcgt's race rule "count"

In the D-model (Definition 1.5) a passer is a terminal: "a passer appears" ends the play for the beneficiary. (V2) of Theorem 1.14 asks that this terminal really be a win for the beneficiary. The frozen passer certificate (Proposition 2.11) is exactly the (V2)-certificate for passer terminals under frozen kings: it shows that a created passer is a P-win for σ provided μ ≥ d + 1, which is the (V2) content for passers, restricted to the frozen model.

**Coincidence with the count rule.** cylcgt's `RACE_RULE = "count"` scores a race by: the opponent of the mover moves first; whoever needs fewer moves to promote wins; the opponent wins ties. This is precisely the parity of Step 2: when σ creates a race (σ̄ to move), σ̄ moves first and wins ties (μ ≤ d), and σ wins only if strictly faster (μ ≥ d + 1). So the certificate's bound μ ≥ d + 1 is the count rule's "σ wins the race" condition, expressed in promotion distances. `promote_distance` (cylcgt) is the d of the certificate: it counts the double step and requires the front-pawn condition (no own pawn ahead), exactly as the certificate's d.

**Where it differs.**
- cylcgt's count rule is applied in the *sum model* (S) regardless of kings: it compares promotion distances in a component and declares a winner, without checking stalemate, clear paths, or the defender's king. The certificate is a *chess* statement in the frozen model: it requires hypothesis 2 (no stalemate of σ̄) and the clear-path condition, and it is (V2) for passers only where those hold.
- cylcgt computes d for the passer's own side only; it has no notion of μ (the defender's fastest promotion with the passer owner's other pawns standing still). The certificate needs μ, which is a search over the defender's pawns (captures, double steps, e.p. included).
- cylcgt's `passed` is e.p.-aware (`PASSED_RESPECTS_EP = True`); the certificate uses the same test, so the e.p. window is handled identically. Setting `PASSED_RESPECTS_EP = False` (textbook test) would make the certificate's hypothesis (passed at the node) fire one move earlier, and the bound would be off by one in those cases — the same discrepancy that removed the \*2 candidate (RESULTS.md §1).
- The certificate is in P (frozen), not in C: a promotion win in P is a C-win only where (A_Q) holds. cylcgt's count rule makes no such distinction.

## 3. Real kings: the square-rule analogue

**Corollary (passer square rule).** With real kings (not frozen), the defender's king cannot catch p when its distance to p's promotion square is at least d + 2 (defender to move). This is the classical rule of the square with the defender to move: d(k_defender, q_D) ≥ d + 2. Modelled on Corollary 2.8, with the passer owner σ as the pusher (s̄ in Corollary 2.8's notation) and the defender σ̄ as s. Under this condition, together with (μ ≥ d + 1), (clear path), (no stalemate) and (A_Q) at the resulting positions, σ wins in chess.

**Proof sketch.** Corollary 2.8 pushes a pawn p every move with a defender's king at distance ≥ D + 2; the king can neither block nor capture (triangle inequality: reaching path square q_j needs j + 1 moves, but only j are available). The passer case is identical: p's straight pushes are legal (clear path), and the defender's king is too far to enter the square. The defender's only remaining resources are pawn promotions (bounded by μ) and stalemate, both handled by the hypotheses.

**What remains open.**
- (A_Q) is a per-position hypothesis (§1.2 of LOOPY.md): a P-win is a C-win only where kpsolve confirms it. The real-kings statement is therefore a chess claim only position by position, not a theorem.
- The condition d(k, q) ≥ d + 2 is sufficient (classical rule) but the multi-pawn interaction (defender using a pawn to chase while promoting another) is not covered by Corollary 2.8's single-pawn analysis. Whether the defender can force a draw by entering the square's boundary with combined king+pawn play is open; kpsolve on the specific position settles it.
- The defender's king might also attack p's path squares to create a block without catching p; this is not ruled out by distance alone and is left as a position-by-position check.

## 4. P11

**P11 should carry the label: PROVED in P (revised after K10, 2026-10-22).**

Reasoning. P11 is a harness check: with frozen kings, `kpsolve --frozen` should equal o(W(X)) (the D-game result with its own winning side), and equal o(S(X)) when hereditarily sum-safe (HSS). The theoretical chain is

S --Thm 1.11(c), (V4/HSS)--> D --Thm 1.14, (V1)–(V3)--> P.

With frozen kings, (V1) (non-interaction, no stalemate) holds by the harness's condition (E) and its layout check, and (V3) (every Z-move is a suicide) holds by fiat (a king move loses at once). The remaining gap was (V2) for passer terminals: Theorem 2.7 covers punished king moves, but passers were only "speed-certified" (Remark 2.11, previously GAP). Proposition 2.11 (this task) now supplies (V2) for passer terminals under frozen kings, with the bound μ ≥ d + 1 and the clear-path/stalemate conditions that the harness checks. Theorem 1.11 supplies the sum. HSS supplies o(S) = o(D). (A_Q) is not involved, because P11 is a P-level statement (it compares --frozen, a P-computation, with o(W) and o(S), both P-level). Hence the backing is complete in P, and P11 is no longer GAP.

Caveat: the certificate is one AI-written proof, read by the integrator and checked on examples; no human or second independent model has re-derived it. Per the project's label convention this is PROVED in P pending independent re-check, not VERIFIED.

## 5. Proposed EDITS.md

See `EDITS.md` in this directory. Edits target only Remark 2.11 (turned into Proposition 2.11 + remark), the status rows R2.11 and P11, and the §6 row P11. No §0 table row for 2.11 exists, so none is edited.

## Reproduce

- Compile: `cc -O2 -o kings/delegate/out/K10/kp kings/kpsolve.c`
- Sharpness W: `printf 'Ka1 kf6 Pc5 pe3 b -\n' | nice -n 10 kings/delegate/out/K10/kp --board cyl:7x6 --frozen --cap 1 --threads 2` → `W W`
- Sharpness L: `printf 'Ka1 kf6 Pc3 pe5 b -\n' | nice -n 10 kings/delegate/out/K10/kp --board cyl:7x6 --frozen --cap 1 --threads 2` → `L L`
- Single passer: `printf 'Ka1 kf6 Pc3 b -\n' | nice -n 10 kings/delegate/out/K10/kp --board cyl:7x6 --frozen --cap 1 --threads 2` → `W W`
- Stalemate trap: `printf 'Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5 b -\n' | nice -n 10 kings/delegate/out/K10/kp --board cyl:7x6 --frozen --cap 1 --threads 2` → `D D`
- cylcgt passed test: `PYTHONPATH=. .venv/bin/python -c "from cylcgt.pawns import Board, Pos, passed, promote_distance; b=Board(7,6,True,True); p=Pos.parse('W: c3 / B: e5'); print(passed(b,p,'W'), promote_distance(b,p,'W'), passed(b,p,'B'), promote_distance(b,p,'B'))"`
- Apply edits: `python3 kings/delegate/apply_edits.py kings/theory/LOOPY.md kings/delegate/out/K10/LOOPY_preview.md kings/delegate/out/K10/EDITS.md`
