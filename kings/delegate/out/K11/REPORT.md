# K11: independent re-derivation of Proposition 2.11 and P11

## 5-line summary
1. I re-derived Proposition 2.11 (frozen-king passer certificate) step by step in my own words, checking the invariants Jβ, Jω, I1 under every kind of ω move, and found no gap or error: Steps 0–5 are SOUND.
2. Corollary 2.11a matches cylcgt's race rule (count) for both move orders; Corollary 2.11b's layout claims (H2),(H3) hold as stated.
3. Theorem 1.14(i) plus Corollary 2.11a at move-reached terminals and Proposition 2.11 at a root that already has a passer do prove `--frozen` = o(W(X)) in conditional form; the remaining gap is roots with a passer (including races and e.p. rights), which have not been swept end to end.
4. I rebuilt kpsolve privately and re-ran all 18 examples of §"What the hypotheses do" plus the two counterexamples; every outcome matches the table (e.g. `Ka1 ka6 Pc2 Pd4 pd3 b -` = (L,L), `Ka1 ka6 Pc4 pe4 b -` = (W,W)).
5. Recommended labels: Proposition 2.11 stays PROVED in P (frozen), conditional; P11 stays PROVED in P, conditional, with the root-with-passer gap recorded as an open verification item, not as a proof gap.

---

## 1. Written proof of Proposition 2.11 (my derivation)

**Setting.** Work in the frozen promotion model F (`kpsolve --frozen`): a promotion wins at once for the promoter; a legal king move ends the play at once in favour of the opponent of its maker; a side with no legal move at all that is not in check draws, and one in check loses; infinite play is a draw. Board is a cylinder with W files and H ≥ 5 ranks (files mod W); the same argument works on a flat board with the files that exist. The position y is legal: kings not adjacent, the side not to move not in check, before any promotion.

**Notation.** Fix y, side s to move, beneficiary β and the other side ω. For a pawn q of either colour, ρ(q) = rank(q) if β is White, and ρ(q) = H+1−rank(q) if β is Black, counted from β's side. β's pawns advance toward larger ρ, ω's toward smaller ρ. β's start rank is ρ = 2, ω's is ρ = H−1. For β's front pawn p, d = H − ρ(p) − [ρ(p)=2] is the number of β pushes p needs to promote (cylcgt's `promote_distance`); e = d if s = ω (ω moves first), and e = d − 1 if s = β (β moves first).

**The ω-only game G_ω(y;p).** Delete p. Only ω moves, one after another; β's other pawns stay and can be captured; both kings stay and block squares; nobody captures a king. ω's pawns push, double step from the start rank over an empty square, capture, and use the e.p. capture that y offers (only as the first move, and only if s = ω). μ_ω(y;p) is the least number of ω moves after which some ω pawn stands on its last rank (promoting move included), or ∞. It is a minimum over all ω pawns, passers or not, with captures allowed. An ω king move ends F at once, so it never occurs in G_ω.

**Hypotheses.**
- (H1) clear path. p is a β pawn passed in cylcgt's e.p.-aware sense (`passed` with `PASSED_RESPECTS_EP = True`: no ω pawn on files f−1, f, f+1 with ρ > ρ(p), and p cannot be taken en passant at y), and every square of p's file ahead of p, promotion square included, is empty. So p is the front pawn of its file, and no pawn and no king of either colour stands on the path.
- (H2) no check. No pawn of either colour stands on a file adjacent to the file of β's king.
- (H3) no stalemate. ω's king has a neighbouring square t that is not adjacent to β's king, such that no pawn of either colour stands on the file of t or on a file adjacent to it.
- (H4) no interference. Every β pawn other than p that stands on a file adjacent to p's file has ρ ≤ ρ(p)+1.
- (H5) timing. μ_ω(y;p) ≥ e + 1.

**Statement.** Under (H1)–(H5), β wins F from (y,s) by pushing p at every turn (double step first if ρ(p)=2).

**Proof.** Write f for p's file and ρ₀ for ρ(p) at y.

*Step 0 — three facts about F.* (F1) A pawn changes file only by a capture, landing on the square of the captured piece (an e.p. capture lands on the file of the captured pawn). There are no officers before the first promotion and a king is never captured, so a pawn enters a file only by capturing a pawn that stands on it, and a file without pawns never gets one. (F2) A king move ends F at once, so in any play in which its maker has not lost, no king moves and both kings stand where they stand at y. (F3) A promotion ends F with a win for the promoter.

*Step 1 — safety of the kings.* By (H2) and (F1), no pawn ever stands on a file adjacent to β's king, so no ω pawn ever attacks it; ω's king gives no check. Thus β is never in check and no push of p is ruled out by king safety. By (H3) and (F1), the three files around t never hold a pawn, so t is never occupied, never attacked by a β pawn (p included, by the same file condition), and is not adjacent to β's king: a move of ω's king to t is always legal, even if ω is in check. So ω always has a legal move — it is never stalemated, and F has no draw by stalemate in the play below.

*Step 2 — the invariant.* In plays where β follows the strategy Π (push p) and ω moves arbitrarily, let ρ_p be the current value of ρ(p) and call files f−1, f, f+1 the strip. We show:
- (Jβ) at every node with β to move, every ω pawn in the strip has ρ ≤ ρ_p + 1;
- (Jω) at every node with ω to move, every ω pawn in the strip has ρ ≤ ρ_p, and p cannot be taken en passant;
- (I1) at every node, every square of file f ahead of p is empty.

At y, (Jβ) or (Jω) (according to s) is (H1) (passed, aware), and (I1) is (H1). β's other pawns and both kings never move, by Π and (F2).

β moves. p goes from ρ_p to ρ′ ∈ {ρ_p+1, ρ_p+2}; the squares are empty by (I1), and the move is legal by Step 1. By (Jβ), the ω pawns in the strip have ρ ≤ ρ_p+1 ≤ ρ′. A double step (ρ′ = ρ_p+2) leaves every ω pawn strictly below ρ′, and an e.p. capturer would have to stand at ρ′ (the rank of p after the push), which (Jβ) forbids; a single step gives no e.p. right. So (Jω) holds, and (I1) still holds.

ω moves a pawn. (a) A push or double step lowers ρ; it cannot enter p's square or a square ahead of p on file f, because the pawn stands at ρ ≤ ρ_p. (b) A capture lands on the square of a captured β pawn q (or on an e.p. target). It never captures p: (Jω) leaves no ω pawn at ρ_p+1 next to p, and p is not e.p.-capturable. So q ≠ p. If q is on file f, then q stands behind p (nothing of β stands ahead of p by (H1)), and the landing rank is below ρ_p. If q is on file f ± 1, then ρ(q) ≤ ρ₀+1 ≤ ρ_p+1 by (H4), and the landing rank is ρ(q). An e.p. capture is possible only with the right offered by y when s = ω: the victim q′ is a β pawn that just double-stepped, and the landing square is the skipped square, one rank below q′. If q′ is on f ± 1 then ρ(q′) ≤ ρ₀+1 by (H4); if on f it is behind p. Either way the landing rank is at most ρ_p+1. (c) So every ω pawn in the strip after the move has ρ ≤ ρ_p+1, which is (Jβ), and nothing lands on file f ahead of p, which is (I1). Captures landing outside the strip change nothing. (The one-line argument "ω pawns move away from p's promotion side, so none can ever stand beside its landing square" is false: a capture of a β pawn on a neighbouring file puts an ω pawn there. (H4) is what bounds the landing rank.)

*Step 3 — consequences.* At every ω turn no ω pawn stands at ρ_p+1 next to p and p cannot be taken e.p., so p is never captured; nothing stands ahead of p on file f ((I1)), so p is never blocked. At every β turn the push is legal. So Π can be played to the end.

*Step 4 — ω's moves are moves of G_ω.* In a play consistent with Π, each ω pawn move is a move of G_ω(y;p): the squares and the captured pawns are the same, p never takes part (Step 3), β's other pawns stay (Π), the kings stay (F2), and the only e.p. capture is the one offered at y. G_ω has fewer obstacles, since p is deleted, which only enlarges its move set. So if ω promotes after k of its moves in the real play, then k ≥ μ_ω(y;p). An ω king move loses at once (F2).

*Step 5 — timing.* Under Π, β promotes with its d-th push. Before that push ω has made exactly e moves (e = d if s = ω, e = d−1 if s = β). By (H5), e < μ_ω(y;p), so by Step 4 none of those moves promotes; by Step 1 ω has a legal move each time, so the play is not a draw. ω's only other moves are king moves, which lose at once. β's d-th push is legal (Step 3) and promotes, and by (F3) β wins. ∎

---

## 2. Per-step verdicts

| Step | Verdict | Notes |
|---|---|---|
| Step 0 (F1–F3) | SOUND | Standard facts of F; F1 is the empty-file invariance used everywhere. |
| Step 1 (king safety) | SOUND | (H2) blocks pawn attacks on β's king; (H3) supplies a safe square t for ω's king; legality of y ensures kings not adjacent. |
| Step 2 (invariants Jβ, Jω, I1) | SOUND | Checked under push, double step, capture landing in the strip (from outside or within), capture leaving the strip, and the e.p. capture offered at y. The e.p. capturer after a double step would need rank ρ_p, forbidden by (Jβ); (H4) bounds captures of β pawns on neighbouring files. |
| Step 3 (p never captured) | SOUND | Follows from (Jω) and (I1); includes the e.p. case after p's own double step. |
| Step 4 (ω moves are G_ω moves) | SOUND | Real play is a subset of G_ω moves because p is deleted; promotion time in real play ≥ μ_ω. |
| Step 5 (timing, both orders) | SOUND | e = d when s = ω, e = d−1 when s = β; (H5) gives e < μ_ω. |
| H ≥ 5 needed | SOUND (needed) | On 4 ranks a pawn can promote by a double step without being passed, so μ_ω can be 1 while e ≥ 1 and (H5) collapses; the distance formula also degenerates. |
| Legality assumption on y | SOUND (needed) | Used for kings not adjacent and the side not to move not in check; without it (H2)/(H3) do not exclude an initial check. |

I checked the tempting false one-liner noted in Step 2 explicitly: a capture of a β pawn on a neighbouring file does put an ω pawn into the strip, and (H4) is exactly the bound that saves the invariant. This matches the first K10 error (a capture of a β pawn on a neighbouring file lets an ω pawn stop the passer).

---

## 3. Corollaries

**Corollary 2.11a.** At a node y′ reached by a move of M, with N to move, cylcgt credits the terminal to b as follows: only M has a passed pawn ⇒ b = M; only N ⇒ b = N; both (a race, count rule) ⇒ b = N if dp(N) ≤ dp(M), else b = M. This is exactly cylcgt's `_child` race rule (winner = the opponent of the mover when the opponent's `promote_distance` ≤ the mover's). The corollary applies Proposition 2.11 at (y′, s = N, β = b), with e = d if b = M and e = d − 1 if b = N, covering both move orders and a race won by the side to move. **Verdict: SOUND**, and it matches the code.

**Corollary 2.11b.** On cyl:8×6 with `Ka1 ka6` and pawns only on c–g: pawns stay on c–g (F1). For either colour as β, (H2) holds (the neighbours of the a-file are b and h, and no pawn stands there); (H3) holds with t = a5 for ω = Black and t = a2 for ω = White (king distance 4 ≥ 2, and the files around t are pawn-free). So at a terminal only the passed front pawn, (H4) and (H5) must be checked. A pawn on the a-file breaks (H3) (`Ka1 ka6 Pa3 Pc2 w -` has no neighbour of a6 with three pawn-free files). **Verdict: SOUND**, and the second-round reviewers reproduced (H2),(H3) and the king clause of (H1) in all 371,250 instances on cyl:8×6 with pawns on c–g.

---

## 4. P11 as now amended

**Does Theorem 1.14(i) + Corollary 2.11a at every terminal reached by a move + Proposition 2.11 at a root that already has a passer prove `--frozen` = o(W(X))?** Yes, in conditional form. The chain is:

- Theorem 1.14(i) gives P(X) = D(X) (no draws) from (V1)–(V3).
- (V3) (frozen Z) holds by fiat: every king move is a suicide.
- (V1) holds in the layout by Corollary 2.11b: no check is possible and a king move is always legal (a2 or a5 is available); condition (E) of L1.6 governs en passant.
- (V2) (decisiveness) holds by fiat at king moves (a frozen king move loses at once, a P-win for the opponent), by Corollary 2.11a at every passer and race terminal reached by a move, and by Proposition 2.11 at a root that already has a passer (s = side to move, β = the side W(X) credits).
- The o(S) clause adds (V4) (hereditary sum-safety) via Theorem 1.11(c) and Theorem 1.14(ii).

So `--frozen` = o(W(X)), and also = o(S(X)) when hereditarily sum-safe.

**Cases still missing / open.**
- A root that already has a passer (including races): covered formally by the root clause, but there is no end-to-end sweep over such roots. P11's harness (56,872 roots) explicitly excludes passers at the root. This is the gap the second round found; it rests on Proposition 2.11 itself plus one counterexample.
- A root with an e.p. right: Proposition 2.11 handles an e.p. capture offered at y, and condition (E) is part of (V1), but roots carrying an e.p. right have been certified only at the instance level (K10v: 5,716 instances, 0 violations), not end to end through P11.
- A root where the side to move is in check: in the `Ka1 ka6` layout this cannot happen — (H2) rules out pawn checks and the kings are distance 4 apart — so it is not a live case for P11, but it is a hypothesis of Theorem 1.14(i) that must be checked per layout.
- Terminals that are king moves: (V2) by fiat, no gap.
- Condition (E): required for (V1a); included.
- Race roots: a race has a passer on both sides, so the root clause applies with β = the credited side and p = its front passed pawn, but (H4)/(H5) must then be checked at that root; not yet swept.

**Counterexample for the gap (verified with kpsolve).** Without the certificate, `--frozen` ≠ o(W(X)): `Ka1 ka6 Pc2 Pc3 pd3 pd4 w -` has o(W) a White win but `--frozen` = (L,L). With the certificate's H5 failing: `Ka1 ka6 Pc2 Pd4 pd3 b -` (p = Pd4 passed, d = 2, e = 2, but μ_ω = 2 < 3) is (L,L) although cylcgt credits White. Both reproduced above.

---

## 5. My computations

**Build.**
```
cc -O2 -o kings/delegate/out/K11/kp kings/kpsolve.c -lpthread
```

**Run (shared lock, as instructed).**
```
kings/delegate/heavy.sh kings/delegate/out/K11/kp --board cyl:8x6 --frozen --cap 1 --threads 2 < in.txt > out.txt
```

**Example outcomes re-run (all match the table in LOOPY §"What the hypotheses do").** 18 positions; selected results (full list in the shell output above):
- `Ka1 ka6 Pc4 pe3 b -` → (L,L) (μ = e = 2, ω wins the tie)
- `Ka1 ka6 Pc4 pe4 b -` → (W,W) (μ = 3 = e+1)
- `Ka1 ka6 Pc4 pe3 w -` → (W,W) (e = 1, μ = 2)
- `Ka1 ka6 Pc3 pe3 w -` → (L,L) (e = 2, μ = 2)
- `Ka1 ka6 Pc2 Pd4 pd3 b -` → (L,L) (H5 fails; μ = 2 < e+1 = 3)
- `Ka1 ka6 Pc4 Pd2 pe3 pf4 b -` → (L,L) (non-passer e3 takes d2 and promotes in two)
- `Ka1 ka6 Pc2 Pd4 Pe2 pe5 b -` → (L,L) (H4 fails: d4 at ρ(p)+2)
- `Ka1 ka6 Pc2 Pd3 Pe2 pe5 b -` → (W,W) (H4 holds)
- `Ke2 ka6 Pc4 pf4 b -` → (L,L) (H2 fails)
- `Ka1 ka6 Pc4 pf4 b -` → (W,W) (H2 holds)
- `Ka1 kc5 Pc4 pf4 b -`, `Kc5 ka6 ...`, `Kc6 ka6 ...`, `Ka1 kc6 ...` → (L,L) (king on path)
- `Ka1 ka6 Pe4 pd4 b e3` → (L,L) (e.p. right makes μ = 3 ≤ e = 3); `... b -` → (W,W)
- `Ka1 ka6 Pc3 Pd4 Pf2 pc4 b d3` → (L,L) (e.p. right is the only reason μ ≤ e)
- `Ke1 ka6 Pa4 Pc5 Pg5 pa5 b -` → (D,D) (H3 fails: no legal move for Black)
- `Ka1 ka6 Pc2 w -` → (W,W) in F (frozen); real kings give (D,D), as the text records.

**Counts from the literature checks I rely on (not re-run by me in full):** K10 parked sweep 954,392 positions, 0 violations; K10v independent 146,328 instances (5,716 with an e.p. right), 0 violations; K10 second round 5,730,596 certified positions with side to move (6,783,482 instances) on cylinders plus 434,429 flat positions, 0 violations. P11 end-to-end: 56,872 roots, 48,000 conservative wins and 26,014 fully certified roots, 0 violations; 3,194 roots differ when some terminal is uncertified; 8 violations when (H4) is dropped.

---

## 6. Recommended labels

- **Proposition 2.11:** PROVED in P (frozen), as a sufficient condition. I found no gap or false step in Steps 0–5; all invariants hold as claimed, including under e.p. captures and captures of β pawns on neighbouring files. The computation is CHECKED-2 (K10v plus the second round). No model outside the Sonnet family had re-derived it before this task; this report is that re-derivation.
- **Corollaries 2.11a and 2.11b:** PROVED (as corollaries of Proposition 2.11), matching cylcgt and the layout.
- **P11:** PROVED in P, in conditional form: `--frozen` = o(W(X)) for every X of the layout whose passer and race terminals are all certified, plus the root clause for roots that already have a passer. The root-with-passer clause (including races and e.p. rights) is not yet swept end to end, so P11 should keep its conditional label and record that verification item; it is not a proof gap, because Proposition 2.11 supplies the certificate. Without the certificate the equality is FALSE, as the two counterexamples show.