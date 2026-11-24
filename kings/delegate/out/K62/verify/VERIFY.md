# K62 referee report

Referee: one AI agent (independent of the K62 investigator), 2026-11-24. Read the K61 packet §1, the K62 brief,
LOOPY.md Definition 4.8, Lemma 4.15, Theorem 4.18, Corollary 4.19, and the investigator's PROOF.md, findings.txt,
EDITS.md. Wrote an own solver (`src/`) before reading the investigator's `src/`. No human re-derivation.

## Verdicts

| Item | Verdict | Short reason |
|---|---|---|
| Lemma 1 (P-wins are H-wins), Lemma 2 (ladder recursion), Lemma 3 (localisation, E-reduction) | CONFIRMED | re-derived step by step |
| Lemma 4 (route lemma) | CONFIRMED | re-derived; first half uses (V1), (V2) only, as Theorem 4.22 needs |
| Theorem 4.20 (a)–(d) | CONFIRMED WITH WORDING FIXES | proof correct; EDIT's definition of P(x) differs in words from PROOF.md (same \|P \ E\|), aligned; model named |
| Proposition 4.21, existence for every N | CONFIRMED | all constructions re-derived by the route lemma; exact in both readings; N\* reproduced by a separate program (CHECKED-2) |
| Proposition 4.21, smallest board counts | CORRECTED (two errors of scope, one open case settled) | the counts hold only in the *strict* reading, but Definition 4.8 as written is the *literal* one: there 3 boards give N\* = 3 with e.p. (new example Λ³), so the e.p. column is max(3, N); in M2 with e.p. 4 boards give N\* = 3 and 4 (new example Δ4), not "5, 4 open" — see §3 for the M2 reading |
| Lower bounds 2.5.1, 2.5.2, 2.5.3 | CONFIRMED | re-derived; 2.5.1's "≥ 4" is strict-reading only (≥ 3 literal), as PROOF.md says |
| Theorem 4.22 (i), (ii), (iv) | CONFIRMED | re-derived; one counting step needs a sharper wording (fixed) |
| Theorem 4.22 (iii) "no finite family / no single finite D-game is universal" | CONFIRMED WITH A SCOPE FIX | true for abstract exact over groups (the K61 model). Λ_N is not a king-and-pawn group; for chess groups it is open (and on one board size one ladder decides, Corollary 4.23). The EDIT said "some exact over group", which in the note means Definition 4.8 / chess. Also N = max(1, max \|T\|) |
| Theorem 4.22 scope remark (win half / draw half) | CONFIRMED WITH WORDING FIX | correct as "a group with the results of ω beside under_D can fail only in the win half"; the draw-half fact is K60's refereed remark |
| Corollary 4.23 | CONFIRMED | count of boards correct; Z_O's N\* = 2 is CHECKED-2 in K60 (W beside T_0, T_1, L beside T_2..T_6, two programs) |
| Lemma 5 (reduction for the 3-position enumeration) | CONFIRMED | re-derived; checks handled (the reduced option is unusable in check either way) |
| Q4 remark (counters in chess) | CONFIRMED WITH WORDING FIXES | claims nothing beyond a remark; but "the walking piece has no move in those zugzwangs" is too strong (its moves need only lose at once), and "White's only non-losing reply" holds beside the ladder, not in general |

Nothing is REFUTED. Labels proposed: Theorem 4.20, Proposition 4.21, Theorem 4.22, Corollary 4.23 PROVED (one AI
proof, re-derived by the referee); the family computations CHECKED-2; my random batteries and the four-position
enumeration COMPUTED-1.

## 1. Readings decided

- **Definition 4.8 is the literal reading.** It names the states it constrains: the roots without a right (both sides
  to move) and, after each freeze, q with Black to move (with the freeze's right) and q with White to move (no right);
  O1–O4 of the K61 packet §1.5 are the same. A promotion by the mover never "loses at once", so "none promotes" at the
  named states follows from the wording. Nothing is said about (root, right, either side) or the q-board states not
  named. The *strict* reading (no promotion at any state of a root board or q-board) is stronger.
- **Which claims depend on it.** Existence (Proposition 4.21 for every N), Theorem 4.20, Theorem 4.22 and Corollary 4.23
  do not: every construction is exact in both readings (checked by program for all of them), and the proofs use only
  O0–O4 at named states. Only the smallest board counts with e.p. rights depend on it (§3). The readings differ only by
  e.p. promotions: a non-e.p. promotion at an unnamed state of a root or q-board is also present at the corresponding
  right-free state (a right only adds moves), which is named. Chess has no e.p. promotions, so in chess they agree.
- **M1 / M2.** M1 is the K61 model (a move may return to its own board; two moves of a state may share a successor).
  The investigator's M2 forbids both, but allows two moves of a state to the same board with different rights. Chess
  is stricter still: two different moves never give the same board. I call that M2b. It matters for §3 only.

## 2. Re-derivation, step by step

**Lemma 2.** Beside u_0 of T_n the moves are group moves, White's advance (not in check; clears her right) and Black's
cut (not in check). After an advance the ladder above u_1 is T_{n−1} with Black to move at (g, 0, Black); after a cut
the rest is H from (g, 0, White) (z inert, and a move elsewhere gives no right). A side with no group move in check has
no ladder move and loses. So White's finite win is a finite success in the layer game with R = B₀ (n = 0, where the
advance is u_0 → ⊕) or R = S_{n−1} ∩ B₀. Monotonicity of F gives the descent. Correct.

**Lemma 3.** A layer play from a state of Z(x) stays in Z(x) until it exits; advances land on B_{P(x)}. For g ∈ E(x)
the modified strategy switches to an F(∅)-strategy at the first White-to-move, not-in-check state on g, so it never
needs (g, 0, Black). Applying (ii) board by board is legitimate because (ii) holds for every R. Correct.

**Theorem 4.20.** S_{n+1} ∩ Z = F(R̂_n) ∩ Z with R̂_n = S_n ∩ B_X, R̂_{−1} = B_X ⊆ Z; equality of two consecutive R̂
propagates; at most |X| strict steps, so S_n ∩ Z is constant for n ≥ |X| (also when |X| = 0). (a): x ∈ S_{|X|} gives x ∈
S_n for n ≥ max(K, |X|), and Theorem 4.18(c)(4) ⇒ (1). (b): x ∈ S_{N−1} \ S_N forces R̂_{N−2} ≠ R̂_{N−1}, hence all N
transitions from R̂_{−1} are strict, each removing a state of B_X outside S_∞. (c): x is a P-win for White by O1; a
P-winning play ends with a White promotion or a mate of Black; a mate board k has Black in check, so no White-to-move
state on k is reachable (Black cannot move into check; x itself follows a legal Black move), k ∉ P; a non-e.p. promotion
is legal at every right of its board, so that board is in E or not in P. Hence |X| ≤ b − 1 when no White e.p. move
promotes. (d): m is a Black option at the root, so a White win of ρ ⊞ u_0 (Black to move) beside T_b gives x_m ∈ S_b ⊆
S_{|X|}. Correct.
Wording: the EDIT defined P(x) as the boards whose (g, Black, no right) is reachable; PROOF.md as the boards with a
reachable White-to-move state not in check. The EDIT's set is larger (it includes boards reached by a White group
move only), but such boards fall into E vacuously, so |P \ E| is the same. I used PROOF.md's definition.

**Lemma 4 (route lemma).** n < d: White advances (V1), Black is at non-exit states (an exit needs d advances), where a
cut gives White an H-win and no promotion exists (V2); White's (n+1)-th advance is u_n → ⊕. n ≥ d: Black follows a
shortest path; a White group move is answered by a promotion or a cut into h = L (V3; Black not in check); after d
advances (d ≤ n, so not ⊕) Black at the exit promotes or cuts. Correct.

**Constructions.** I rebuilt Γ2(k, R), Γ(0, R), Π(k, R), Π_self(3), Π_self(4), Λ_N and the 2.5.4 group from the
PROOF.md text and checked exactness, h-values and routes by hand and by program (§4). One ambiguity: in Γ2(k, AB) and
Π(k, AB) A must *not* have the move A → c_1 ("then as for A" could be read so); with it N\* drops to k + 3 (computed).
The investigator's code has it right; the EDIT now says so.

**2.5.1–2.5.3.** 2.5.1: a freeze to a root board would make (ρ, 0, White) a q-state whose moves all lose (O4) while it
has a freeze (O2). A P-win exists after a freeze (O3); its terminal is a promotion or a mate, neither at a root or q-board
in the strict reading. 2.5.2: without double steps every state of a root or q-board is named; with 4 boards there are
one q and one y; the bad moves reach root White states or (y, White) (not (q, White), a P-loss); if (y, White) is
reachable Black is not in check at y, so no mate exists and White's P-wins end with a promotion at (y, White); passing at
roots and promoting at y wins Aux. 2.5.3: in M2 without double steps a bad move cannot reach a root White state; the
induction keeps the root Black states in S_j for j < N\*, so only (q, 0, Black) and (y, 0, Black) can be removed:
N\* ≤ 2. All correct.

**Theorem 4.22 (i).** Theorem 4.18(b) reduces to (C) at the single bad move. Shadow play: real (c_i, t′, s) against
shadow (ω, t′, s); counter moves are copied as shuttles, White's c_i → q as ω → 0_D, after which Theorem 4.18(a)
applies at (q, t′, Black). W case: an attractor strategy never repeats a shadow state, so the copied play meets
(ω, ·, Black) at most |T| times; the first meeting is the virtual shuttle, and the real Black is to move at c_j only at
the (j+1)-th, so he is never to move at c_N when |T| ≤ N, and c_N → e never happens. (The PROOF counts shuttles and says
"reaching e needs N counter moves"; the argument needs the meetings counted, or c_N → e copied as a shuttle too. The
fix is one sentence, made in the EDIT.) No side is stuck at a c_i; terminals of T are copied; the play is finite. D case:
if Black plays c_N → e, the shadow is at (ω, t″, Black) with S non-losing, so t″ has no Black option ⊖; White promotes
by ⊕ in T or loops e → p; at p every Black T move is answered by White's promotion. Correct.

**Theorem 4.22 (ii).** C_N: ω ⊞ N, Black to move, is W (White walks the chain down, answers a jump to 0 or the end by
ω → 0_D). In Λ_N Black plays m, answers chain moves with counter moves (the chain stays ≥ 1 at every White turn on a
c_j) and a freeze with the jump to 0, after which White has only q → e and Black promotes; after N chain moves White is
in the e–p loop. T_{N+1}: Black walks the counter, White's (N+1)-th advance from e is not ⊕; a freeze is met by a cut
(h(q, White) = L). Values ≤ D; computed exactly D. Passing T_n for n ≤ N: first half of Lemma 4 with the exit (e,
Black) after N + 1 White states; (C) at u_i is the T_{n−i} statement, at z it is h(x) = W. Correct.

**Theorem 4.22 (iii).** Follows from (i), (ii) for every finite F (with N ≥ 1) and for every single finite D-game U,
loopy or short, because (i) covers all finite D-games with at most N positions, loopy ones included, all positions,
both sides, roots and q-states. But it is a statement about abstract groups. Λ_N is not claimed to be a
king-and-pawn position, and for chess groups on a fixed board Corollary 4.23 gives a single
universal ladder. So the EDIT must not say "some exact over group" without "abstract". Fixed.

**Corollary 4.23.** A board is a placement of two kings and at most p pawns a side: b ≤ (wh)² (Σ_{i≤p} C(wh, i))², and
Σ_{i≤p} C(n, i) ≤ Σ_{i≤p} C(p, i) n^i = (n + 1)^p. Chess groups satisfy "a right only adds moves" and have no e.p.
promotions, so T_{b−1} and hence T_M decide. Correct.

**Lemma 5.** A move to one's own losing terminal is never better than another move, and if it is the only move
anywhere the mover loses with or without it; a winning terminal in L(t) makes the rest of L(t) irrelevant wherever
L(t) is usable, and in check neither is usable. Correct, so the reduced 3-position enumeration covers all games.

**Where the rules enter (checked).** Side to move: every comparison in (C) has White to move on the left and Black on
the right; the root test uses Black to move. No-move-loses versus stalemate: only (O1)–(O4) and Lemma 1 use P; all
constructions have a move at every state. Checks: advances, cuts, passes are moves elsewhere, forbidden in check
(Lemma 2, Z, P, E); 2.5.2 and Theorem 4.20(c) use that Black cannot move into check. E.p. right: cleared by passes and
cuts (Z uses right-free Black states); "only adds moves" is used in Theorem 4.20(c). Promotions: terminals in every
sum. Draws: Λ_N's failure is W against D; D transfer in 4.22(i) uses non-losing strategies.

## 3. Smallest numbers of boards (corrected table)

Least b for which some exact over group has a bad move with N\*(m) = N. "e.p." = double steps and e.p. moves allowed
(including e.p. promotions); "no e.p." = no double steps. Checks allowed but not used by any construction.

| N | no e.p., M1 | no e.p., M2 | e.p., M1, strict | e.p., M2, strict | e.p., M1, literal (Definition 4.8 as written) |
|---|---|---|---|---|---|
| 1 | 5 | 5 | 4 | 4 | 3 (PROOF 2.5.4, its move B ⇒ q) |
| 2 | 5 | 5 | 4 | 4 | 3 (PROOF 2.5.4) |
| 3 | 5 (Π_self(3)) | 6; 5 impossible without checks, open with checks | 4 (Γ(0,A)) | **4** (climb example, `logs/mini.log`) | **3 (Λ³, new)** |
| 4 | 5 (Π_self(4)) | 6; same | 4 (Γ(0,AB)) | **4 (Δ4, new)** | 4 |
| ≥ 5 | N + 1 | N + 1 | N | N | N |

Without e.p. the readings agree. The investigator's table had "e.p., M2: 5 for N = 3, 4 (4 open)" and gave only the
strict counts; the EDIT presented max(4, N) as the smallest count without saying that Definition 4.8 is the literal
reading. Δ4 and the N\* = 3 example use two moves of one state to the same board with different rights (B → A, the
shuttle, and B ⇒ A), which the investigator's M2 allows but chess does not. In the chess-like M2b (two moves of a
state never give the same board) Δ4 is excluded; there 5 boards give N\* = 3 and 4 (Γ2(1, ∅), Γ2(1, A) are M2b), and
whether 4 boards do stays open, as the investigator said for its M2. Hill climbing in M2b with e.p. found only N\* ≤ 2
on 4 boards, but also only N\* ≤ 2 on 5 boards, where Γ2 gives 3 and 4: weak evidence either way.

**Λ³ (literal reading, M1, N\* = 3 on 3 boards).** Boards A, B, q, no checks. Black: A → B; B → A twice (the shuttle
and a bad move with the same successor), B ⇒ q, q ⇒ B, e.p. promotion at (B, Black, right). White: A → q, B → q, q ⇒ B,
e.p. promotion at (B, White, right), e.p. move q → q at (q, White, right). P-values: (B,1,W) = W, (B,1,B) = L, (q,0,B) = W,
(q,0,W) = L, (q,1,W) = W (by q → q), roots W both sides. Exact in the literal reading (the promotions at board B are at
the unnamed states (B, right, ·)), not in the strict one. Route after the second B → A: x = (A, 0, White), A, B (B ⇒ q),
q: (V1)–(V3) hold, d = 3. Computed: W beside T_0..T_2, L beside T_3, T_4.

**Δ4 (strict, M2, N\* = 4 on 4 boards).** Boards A, B, q, g. Black: A → B; B → A, B ⇒ A, B → g; q ⇒ g; g → q; e.p.
promotion at (g, Black, right). White: A → q, B → q; q ⇒ g; g → q; e.p. promotion at (g, White, right). P-values:
(g,1,W) = W, (g,1,B) = L, (q,0,B) = W, (q,0,W) = L, (g,0,W) = W, (g,0,B) = L, roots W both sides, (A,1,W) = W. O1: B ⇒ A
and B → g lose at once; O2: freezes to (q, 0, Black) = W; O3, O4 at q. Route after m = B ⇒ A (x = (A, 1, White)): A, B,
g, q; (V2): (A,0,B), (B,0,B), (g,0,B) do not promote and have h = W; (V3): White's moves go to (q, 0, Black) (h(q, 0,
White) = L) or q ⇒ g (Black promotes e.p.). So N\* = 4 = b. Computed: same.

## 4. Own computations (src/, logs/; COMPUTED-1 unless said)

My code: `src/ref62.py` (retrograde solver with a draw terminal for stalemate in P; D-sums with checks, rights,
promotions, no-move-loses; two separate Büchi solvers for Aux, νZ.μY and the classical attractor-removal algorithm,
asserted equal on every group; exactness in the strict and literal readings, M1/M2/M2b; Z, P, E, S_n by direct ladder
solves), `src/fam62.py` (families from PROOF.md's text, plus Δ4), `src/chk62.py` (families, random groups, hill
climbing), `src/lam62.py` (Λ_N against games), `src/small62.py`, `src/mini62.py`. Commands from the repository root:
`.venv/bin/python kings/delegate/out/K62/verify/src/<file> <args>` as in each file's docstring. Every run under 100 s
wall and under 25 MB (`/usr/bin/time -l` in the logs); runs over a minute went through `heavy.sh`.

1. **Families** (`chk62.py families`, `logs/families.log`): 41 groups (Γ2(k, ·) k ≤ 4, Γ(0, ·), Π(k, ·) k ≤ 4,
   Π_self, Λ_1..Λ_6, the 2.5.4 group, Δ4, and Γ2(2, AB) with the extra move A → c_1). Every N\* from direct ladder
   solves equals PROOF.md's value (Γ2: 1, 2, k+2, k+3, k+4; Γ: 3, 4; Π: 1, k+2, k+3, k+4; Π_self: 3, 4; Λ_N: N + 1 with
   value D beside T_{N+1}; the literal group: 2), the value beside T_{N\*} is L (D for Λ_N), Aux is lost exactly when
   N\* is finite, N\* ≤ |P \ (E ∪ S_∞)| ≤ |P \ E| ≤ b (≤ b − 1 without White e.p. promotions), x ∈ S_{|P\E|} iff Aux
   won, root test beside T_b (and T_{b−1}) iff Aux at every bad move: 0 violations. Exactness: all strict and
   literal; Γ(0, ·) and Π_self M1 only; the 2.5.4 group literal only. With A → c_1 in Γ2(2, AB): N\* = 5 = k + 3.
   x ⊞ under_D is L for Γ2, Π and D for Λ_N, as PROOF.md says. **CHECKED-2** with the investigator's
   `logs/q1_families.log`.
2. **Random exact groups** (`chk62.py random 11|12|13 1500`, `logs/random.log`): 4,500 exact groups, 4 to 9 boards,
   one or two q-boards, models plain / checks / e.p. / checks + e.p., strict and literal readings, M1 and M2, half of
   them biased toward counter-like routes; 1,204 with a check, 2,332 with e.p. moves, 885 with a White e.p. promotion;
   6,288 bad moves (1,403 double steps), 419 failing (C), N\* = 0..5 (21, 212, 130, 43, 11, 2). 0 violations of every
   check of item 1. The bound N\* = |P \ (E ∪ S_∞)| is attained at N\* = 1, 2, 3, 4. (Separate generator and program
   from the investigator's 4,500; same conclusion.)
3. **Small boards** (`small62.py 3 20000`, `logs/small.log`): 674 exact groups with 4 boards and no e.p. (175 with
   checks): all satisfy (C) (2.5.2); 1,827 M2 groups with 5 boards, no e.p., no checks: largest N\* = 2 (2.5.3); 682
   such groups with checks: largest N\* = 2 (the open case; no example found).
4. **Hill climbing** (`chk62.py climb`, `logs/climb.log`, `climb2.log`, `climb3.log`; `mini62.py`, `logs/mini.log`):
   literal, 3 boards: N\* = 3 found and minimised to Λ³; strict M2, 4 boards, e.p.: N\* = 3 and 4 found (and Δ4 by
   hand); strict M2, 5 boards, checks, no e.p.: best N\* = 2; literal M2, 3 boards: best N\* = 0; strict M2b, e.p.: best N\* = 2
   on 4 and on 5 boards (on 5 boards Γ2 reaches 4, so the climb misses long routes; evidence only).
5. **Λ_N against games** (`lam62.py`): Λ_1..Λ_5 against every D-game with 1 and 2 positions, unreduced (64 and 32,896
   up to relabelling; `logs/lam_exhaust12.log`) and every reduced D-game with 3 positions (89,613;
   `logs/lam_exhaust3.log`): Λ_1 fails 0, 128, 3,868 (first \*), Λ_2 fails 0, 0, 384 (first C_2), Λ_3..Λ_5 pass all;
   **CHECKED-2** (identical counts to the investigator's). Referee only: every 4-position D-game with at most one
   option per side and position (none, a position, or the mover's winning terminal; by Lemma 5 a losing terminal is
   the same as none), up to relabelling, 72,567 games (`logs/lam_exhaust4_single.log`): Λ_1 4,474, Λ_2 417, Λ_3 24
   fail (first C_3), Λ_4, Λ_5 pass all; 60,000 random reduced 4-position and 20,000 5-position games
   (`logs/lam_randfixed.log`): Λ_4, Λ_5 pass all, Λ_3 fails 12 and 18; 20,000 random loopy games with 2 to 9 positions
   and terminals for both sides, half chain-shaped (adversarial: White steps down, Black jumps), against Λ_1..Λ_9
   (`logs/lam_random.log`): no game with at most N positions separates Λ_N (12,511 tests for Λ_6, 20,000 for Λ_9).
   Ladders, chains, under_D (`logs/lam_named.log`): Λ_N passes T_0..T_N, fails T_{N+1}..T_8, passes C_1..C_{N−1},
   fails C_N..C_8 with A = D and ω = W at every failure, passes under_D (N ≤ 6). On every game the full check (both
   roots, both sides, every position, both q-states) equals (C), as Theorem 4.18(b) says. Symmetry reduction used:
   relabelling of positions only (it maps every value to the same value at the image position).

Exhaustive enumeration of all 4-position D-games (17^8 reduced option tuples) was not done: too large for this
check. The 4-position evidence for Λ_4 is the single-option class, random games and Theorem 4.22's proof.

## 5. Comparison with the investigator's code (read after mine)

`k62families.py` builds the same groups as my reading of PROOF.md (A → c_1 absent in the AB route). Its exactness
check is the literal reading; its random groups never put a promotion on a root or q-board, so they are strict. Its
random generator differs from mine (it forces a hot board 3 in 70 percent of groups; mine repairs random groups
toward exactness and biases half of them toward routes). Results agree wherever the same objects are computed.

## 6. Not checked

- Exhaustive 4-position D-games against Λ_4 (only the single-option class and random samples).
- Whether 5 boards allow N\* = 3 or 4 in M2 without e.p. when checks are used (no example in 682 random groups or by
  hill climbing).
- Whether 4 boards allow N\* = 3 or 4 in the chess-like M2b with e.p. rights (Δ4 needs two moves to one board).
- The draw-half statement (under_D decides it) is K60's refereed remark; not re-derived here beyond the necessity
  direction.
- No real-board computation (by the brief); the Z_O and H10 facts are quoted from K60 and its referee.
- Whether any king-and-pawn exact group realises a Λ_N-like counter (so whether Theorem 4.22 has a chess form).

## 7. Files

`VERIFY.md` (this file), `EDITS.md` (replacement for the investigator's; applies to the current LOOPY.md with 3
applied, 0 rejected, `logs/apply_edits.log`), `src/ref62.py`, `src/fam62.py`, `src/chk62.py`, `src/lam62.py`,
`src/small62.py`, `src/mini62.py`, `logs/*.log`, `pids.log`.
