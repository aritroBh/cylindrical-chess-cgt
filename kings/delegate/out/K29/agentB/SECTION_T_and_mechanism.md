# Agent B section: T, exact punishment lengths, failure mechanisms (2026-10-28/29)

All numbers below are reproducible with the scripts in `agentB/` (listed at the end). Labels follow the brief.

## 1. "Acts as 0 beside H" and the parking
Z acts as 0 beside H (in P) iff the P pair (White to move, Black to move; White's view) of Z + H equals the pair of the frozen model
(`--frozen`: a king move loses at once, a promotion wins at once, stalemate draws) on H with Z replaced by two parked kings
(White king on file zs rank 1, Black king on file zs rank H, both on F_Z; a second parking on another F_Z square was checked as well by the
referee of the first attempt: 0 differences on the 885 contexts of cyl:7x6). Why parking is neutral: in the frozen model every king move
loses at once, so only the fact that each parked king has at least one legal move matters (otherwise a parked side would be stalemated and
draw). By Lemma 2.2 the kings stand on F_Z, are never attacked by a context pawn and never block one. The parked kings are on rank 1 and
rank H of F_Z, where no pawn stands, so a parked king always has a legal king step (a king step is never attacked by a context pawn
inside F_Z). Real P kings are NOT used for parking: a real king would walk to the context and change the value.
The Z-moves of a frozen group are king moves AND Z-pawn moves (Definition 2.5): a group may have a mobile Z-pawn whose every move loses
in P (for example `Kb1 Pa2 Pb3 ka3 pb2 pc5`, whose pawn c5 can move and loses by it). Such groups are frozen in the sense of Theorem 2.4,
and the parked comparator (no Z-pawns) is the right "0".

## 2. T ≥ 2: what is tested
Exact punishment length of a sortie m of the side s: L(m) = number of punisher moves in the exact P-win after m, the reply r included
(grp2 `--depth`: win depth d in plies after m, L = (d+1)/2; COMPUTED-1). For Z_T every sortie has L = 5, and the local game of LOOPY gives T = 4
after the reply Kxb4: T = L - 1 there.
**Lemma (PROVED, from Theorem 2.7(a)).** If L(m) ≥ 3 for a sortie m of the bare group, then no certificate LC_1(m) with a valid (L3) exists for m.
*Proof.* LC_1(m) with reply r gives by Theorem 2.7(a) a P-win for s̄ in which s̄ plays r and promotes by its first move after r, so L(m) ≤ 2. ∎
So "T ≥ 2" is certified by L(m) ≥ 3 for one sortie of one side. (The converse, T ≥ 2 only if L ≥ 3, is not claimed; the certificate T of the local
game can exceed L - 1, and I did not run the local game for these groups: `kings/delegate/out/K24/scripts/lg.py` asserts that no pawn stands on its
start rank, and most groups here have a blocked pawn on its start rank.)
Independent check of the small values (CHECKED-2, `agentB/depth3.py`): a depth-3 search using only ref3m's legal move lists and values
(K23 referee's solver, written from SPEC.md) decides "the punisher wins within 3 plies after m" (L(m) ≤ 2). On the 20 (group, configuration) survivors of the
four f3 configurations with a context class of at least two files that survived Phase A (agentB/surv_*.txt), it agrees with grp2's table on every
move: L ≤ 2 exactly for Kb1c2 / Kb1a2 / Kd1e2 / Kd1c2 (L = 1) and Pb3b4 / Pd3d4 (L = 2), and for no other move (`agentB/depth3_survivors.txt`).
Every survivor has a sortie with L ≥ 3 (L = 4 or more): so none is a T = 1 group of Proposition 2.10(a).

## 3. Failure mechanisms (first failing context of every class representative of Phase A; `agentB/mech_*.txt`)
`scripts/mech2.py` (session 2's tool, unchanged) classifies the side to move at the first failing context with Φ ≠ Ψ, by kp_p `--moves`.
Counts over the 13 configurations (each class representative once per configuration, 281 first failures):
| class | count | meaning |
|---|---|---|
| A, K>B | 98 | the side that loses in Ψ has a king step onto a buffer file that does not lose in P (the Z_T mechanism) |
| B refuted | 51 | a Ψ-winning move of the side is answered by a non-losing reply of the other side (K>B or K>Z reply) |
| A, STALE | 47 | the side to move has NO legal move in P (stalemate, a draw) while the parked kings lose in Ψ |
| A, K>Z | 46 | a king step inside F_Z does not lose (context with a fast counter-passer; no buffer step needed) |
| A, other (K>B,K>Z / Pz / mixtures) | 39 | |
**Lemma N1 (stalemate, PROVED).** Let Z be a frozen group (bare pair (L, W)) and s a side all of whose legal moves in the bare group are king steps onto
buffer-file squares (exit-only). Let G be a context in which s has no legal move and in which each exit square is attacked by an s̄ context pawn. Then at Z + G with
s to move, s has no legal move (a stalemate, value D in P), while the frozen model with parked kings gives a loss for s (the parked king has a legal move and every
king move loses at once). So Z does not act as 0 beside G.
*Proof.* By Lemma 2.2 no context pawn occupies or attacks a square of F_Z and none is ever on a buffer file, so the legal moves of s inside F_Z and the Z-pawn moves are the same
in Z + G as in Z; by hypothesis there are none. Its other legal moves in Z are king steps onto buffer squares, now attacked, so illegal. G gives s no move. s is not in check
(context pawns do not attack F_Z). So s is stalemated; P scores stalemate as a draw. In the frozen model the parked king of s has a legal step (rank 1 or rank H of F_Z
has a free neighbour) and it loses at once. ∎
Example (from the data): cyl:7x6 `Ka1 Pb2 Pa3 kb3 pa2 pa4` with context `pf3`, White to move: the only legal White move is Kg2, g2 is attacked by pf3, so
White is stalemated: Φ = (D, L), Ψ = (L, L). Coverability: an exit square on rank ρ of a buffer file is attacked by a black pawn on an adjacent context file at rank ρ + 1 (so ρ ≤ 4 on 6
ranks) or by a white pawn at rank ρ - 1 (ρ ≥ 3) when s is Black; with at most 2 pawns of s̄ the lemma applies to groups with at most 2 coverable exit squares.
Consequence for a universal zero: both sides must have a legal move inside F_Z (or a Z-pawn move) in the bare group, or at least 3 exit squares in the class of contexts. All survivors listed have it.

## 4. What the exact depth does NOT predict (a negative result)
A simple race conjecture: "if a sortie m puts the king on a buffer square next to a capturable context pawn and the punisher needs L(m) ≥ 5 moves, some context beats the punisher by
a tempo, as in Z_T" is FALSE as a predictor of failure. Counterexample, cyl:7x6: `Kb1 Pa2 Pb3 ka3 pb2 pc5` has Black sorties Ka3g4 (L = 8) and Ka3g2 (L = 4), both onto the buffer file g,
and it acts as 0 beside all 885 contexts on e, f (A's Phase A/B and the first attempt's `ver` run, kp_p and ref3 agree). Reason found: L(m) is the exact length against the defender's best
delaying defence, which uses the king to walk back; a sortie that goes to capture a context pawn gives up that defence, so the punisher is faster against it; the right quantity is the
local-game T (a defender who may pass), which was not computed. Also, the squares that the king can use are often attacked by the pawns of Z itself (on a cylinder a Z-pawn on file a attacks file g).
Status: CONJECTURE (not tested further).

## 5. Reproduce
`agentB/run_mech.sh` (mechanism, uses scripts/mech2.py), `agentB/sortie_table.py BOARD ZS FZ REPFILE OUT` (L(m), class of every move), `agentB/depth3.py BOARD ZS FZ 'Z'` (independent L ≤ 2 test, ref3m),
`agentB/run_depth3.sh`, `agentB/analyze.py` (join). Binaries: `bin/kpp` (kp_p `--pmodel`), `bin/ref3m`, `bin/grp2` built from the sources named in the brief and `scripts/grp2.c`.
