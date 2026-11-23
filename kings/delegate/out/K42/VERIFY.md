# K42 referee report: tempo matching, the promotion-free form

Date: 2026-11-23. Independent referee (AI, same model family as the investigator); no human re-derivation.
Referee files: `kings/delegate/out/K42/verify/` (`src/vk42.cpp`, `src/vctx.py`, `src/mkfailpos.py`, `logs/`, `EDITS.md`, `pids.log`).

## Verdict

**ACCEPT, with label updates.** Every number I re-ran agrees exactly, every named example agrees move by move, and the proof of
Proposition 8.1′ re-derives without a gap. The only changes are labels: parts that were COMPUTED-1 or "not refereed" are now
CHECKED-2 or refereed. A full replacement set of edits is in `verify/EDITS.md` (5 edits, all apply cleanly).

## 1. Own solver (written before reading `src/k42.cpp`)

`verify/src/vk42.cpp` was written from `kings/SPEC.md` (model P: the first legal promotion wins, mate loses, stalemate and
infinite play draw) and Definition 2.6. It uses retrograde analysis by pawn-configuration layers, with a bucket queue inside each layer.
Its switches give:
- the local game (Black's king confined to a–c; White passes; the queen clause);
- the K42 diagnostics: m1 (stalemate of White scored as a Black win) and m2 (White's king confined to F_Z and the buffer).

`verify/src/vctx.py` enumerates contexts independently, using the promotion-free test and the normal-play pawn game.

I found and fixed one bug of my own during the first example run: a loss was assigned before a pending out-of-layer win. All
results below come after the fix. K42's solver, `ref3` and `lg.cpp` were not read; only their output files were compared.

## 2. Re-computed values (all CHECKED-2 now: K42's solver and the referee's agree)

| check | K42 | referee |
|---|---|---|
| roots (≤ 2 + 2, all three boards) | 551,138 | 551,138 |
| plain-only sorties, either form: cyl:7×6 / 8×6 / 9×6 | 91,548 / 91,622 / 91,640 | the same; line-by-line identical lists, including the 4 flags P0 Pinf P0q Pinfq (0 differing lines after normalising the capture mark "x") |
| promotion-free contexts with White to move losing (≤ 2 + 2): 7×6 / 8×6 / 9×6 | 26 / 56 / 100 (zero 24/53/96, negative 2/3/4), classes 13/36/53 | the same, and the same lists. My enumeration also returns the empty context, which K42 excludes. |
| cyl:8×6 `Pe2 pe3` (c1), all 91,622 sorties | legal 87,564, L 86,067, D 833, W 664 | identical; same 1,497 failures, pair by pair |
| cyl:8×6 `Pe2 Pg2 pe4 pg4` (c25, K18's family) | 85,748, 84,428, 52, 1,268 | identical; same 1,320 failures |
| cyl:7×6 `Pe2 pe3` (c1) | 87,490, 86,144, 605, 741 | identical; same 1,346 failures |
| cyl:9×6 `Pe2 pe3 pe5` (c3, negative class) | 86,347, 85,978, 345, 24 | identical; same 369 failures |
| mechanism for c1 of cyl:8×6 (m1/m2/m3 on 1,497 failures) | per-failure classes in `logs/diag8c.tar.xz` | identical for every failure. W fixed by m2 alone: 660; W fixed only by m3: 4; D fixed by m1 alone: 374; D fixed by m2 alone: 34; D fixed by either: 425; 0 survive m3. |

Note on the sortie count: K42's `sort8_22.err` reports 2,205,120 sorties; I count 2,214,377 legal non-promoting White moves
with no immediate Black promotion. That figure is not quoted in findings.txt or EDITS.md, and the plain-only sets are identical,
so it does not matter. The likely cause is a different pre-filter.

**Named examples** (`verify/logs/examples_in.txt`, `lg_examples_out.txt`). All values agree with K42 and `ref3`:
- E1:
  - bare: L, only 1...Kb3 wins;
  - with G: D, and only 1...Kb3 draws (every other Black move loses);
  - after 1...Kb3, 2.e3 is White's only drawing move;
  - after 2.e3, 2...g3 is Black's only non-losing move, and it stalemates White;
  - plain T = 1, queen-clause T = 2, the pass game is not won.
- E2:
  - with G: W; after 1...Kb2, 2.Kxg4 is the only winning move;
  - bare: L, only by 1...Kb2;
  - plain T = 6, the pass game is not won;
  - the μ_s ≤ 5 line Kxg4, Kh5, g2–g4, g5, g6 checked by hand.
- E3:
  - with G: W; after 1...Kc2 the winning moves are Kxe4, Ke3, a3, e3, g3;
  - bare: L; plain T = 7 (8 with the queen clause); the pass game is a draw.
- E4:
  - with G: D; 1...Kb5 loses, 1...g5–g3 is the only drawing move;
  - bare: L, only by 1...Kb5.
- E0: with G: D (1...Kb3 stalemates White); bare: L.

Diagnostics on E1, E2, E4: E1 is fixed by m1, E2 by m2, E4 by m2 and not by m1, as stated.

**Arithmetic.**
- Board totals: 15,700 + 39,673 + 13,022 = 68,395; draws 3,175 + 6,071 + 2,185 = 11,431; White wins 12,525 + 33,602 + 10,837 = 56,964; legal pairs 1,135,472 + 3,195,699 + 1,702,252 = 6,033,423.
- The cyl:8×6 table is the 42-context summary less the six mirror contexts c13–c18 (3,720,741 − 525,042 = 3,195,699).
- The K18-family rows add up: 117 + 5,407 = 5,524, and 87 + 3,163 = 3,250.
- The 1,182 NOESC failures are 1,318 − 136 (c13–c18).
- The lg.cpp root-line totals are about 51,000 (P) and 46,000 (Q).

**Not re-run by the referee (they stay COMPUTED-1):**
- the per-context totals other than the four rows above;
- the mechanism counts other than c1 of cyl:8×6;
- the 5–6-pawn sample (216 failures in 37,362 pairs);
- the certificate counts (1,213,383 and 967,308; 0 certified failures).

The certificate counts are a consistency check, not part of the proof.

## 3. Proof of Proposition 8.1′ (PROOF.md), re-derived step by step

**Lemma A, SOUND.**
- Take 𝒢 = the positions with s to move that are reachable from G and lost for s.
- Closure: after an s-move from c ∈ 𝒢, the position c′ is a win for s̄ to move, so s̄ has a reply c″ that is lost for s and reachable; hence c″ ∈ 𝒢.
- No promotion: promotion-freeness is quantified over all move orders, so it covers alternating play and e.p. captures.
- Deleting a pending right keeps loss and closure: the moves without the right are a subset of the moves with it.
- So (P2) of Proposition 8.1 follows from (PF).

**X ∪ E ∪ A ⊆ X ∪ N(X), SOUND.** A square of E is next to the landing square of the double step, and a square of A is diagonally next to the square of the attacking pawn.

**Steps 1–5, SOUND.**
- The induction is not circular. Step 3(i) applies to every legal real king move, a capture included, which the projection reads as a plain move. So the target lies in R and hence outside X. This rules out king captures and blocks, and Step 1 then follows.
- Contexts present while s's king stands somewhere are always in 𝒢⁺:
  - at s-turns, in 𝒢;
  - after an s context move, in 𝒢⁺, and the s̄ pawns are a subset of those before it;
  - after a pairing reply, in 𝒢.
  So "no s̄ context pawn attacks s's king" needs exactly A. This is Step 2.
- Step 3(ii) needs the king target to be:
  - free of the context pawns of both colours (X);
  - unattacked by s̄ context pawns (A).
  Both hold.
- Pairing replies are legal:
  - their squares are in X or E;
  - an e.p. pairing reply lands on a square of E that is also in X;
  - s̄'s king is never in check at a pairing turn: there are no sliders, and Lemma 2.2 holds.
- Stalemate at a turn after a pairing reply is handled by (P1e) as in Proposition 8.1. A mate in the projection is a real mate, because a context pawn can neither capture on F_Z nor block a pawn check.
- Finiteness: the pawn game is finite, and the deleted play has at most T s̄-moves.

**The "game form" remark of PROOF §5 is a correct equivalence.** When stepping onto X ∪ E ∪ A counts as a failure for s̄, s chooses whether to step, so a winning s̄ strategy is exactly a σ whose R avoids the set.

**Example 1 (A cannot be dropped), SOUND.**
- At Q = `Ka1 Pb2 kb3 pa2` + G (White to move) the local game has R = {a1, h2}: White's only move is Kh2, then ...a1 promotes, so T = 1.
- Hand computation for G = `Pe2 Pg2 pe4 pg4`:
  - 𝒢⁺ contexts: `Pe2 Pg2 pe4 pg4`, `Pe3 Pg2 pe4 pg4`, `Pe2 Pg3 pe4 pg4`, `Pe3 Pg2 pe4 pg3`, `Pe2 Pg3 pe3 pg4`;
  - X = {e2, e3, e4, g2, g3, g4};
  - E = ∅ (no double step is possible);
  - A = {d2, d3, f2, f3, h2, h3}.
- So R avoids X ∪ E and h2 ∈ A. My solver gives Q = D (2.e3 g3 stalemate), so the conclusion fails.

**Minor wording point (no change needed).** PROOF.md defines E through "the pairing reply". K42's certificate takes X, E, A over all winning replies, which is a superset. Either choice works if the pairing strategy picks its replies from the set used to define E.

## 4. Labels

- PF-TM FALSE: CHECKED-2. Three P solvers (K42's own solver, `ref3`, the referee's) agree on the examples, and two of them agree on four full context rows.
- Plain-only sortie lists and context lists: CHECKED-2.
- Proposition 8.1′: PROVED. It has now been re-derived by a referee (same model family), and no human has re-derived it.
- Mechanism: CHECKED-2 for c1 of cyl:8×6 and the examples; COMPUTED-1 elsewhere.
- Certificate counts: COMPUTED-1.
- No solver result is labelled PROVED.

## 5. EDITS.md

- The original `EDITS.md` applies cleanly to a temporary copy of LOOPY.md (5 applied, 0 rejected).
- `verify/EDITS.md` is a full replacement set with the same 5 anchors, each OLD occurring exactly once. It also applies cleanly (5 applied, 0 rejected).
- It changes only labels and provenance:
  - "no referee yet" and "not refereed" become references to this report;
  - the referee's CHECKED-2 rows are added;
  - "three P solvers" replaces "by `ref3`" for the examples;
  - "not re-run by the referee" is added for the certificate counts.

## 6. Housekeeping

- Heavy runs went through `heavy.sh` at nice 15. These were the four full context runs; the largest, c25, peaked at 2.95 × 10⁹ bytes RSS (2.75 GiB) and took 460 s. Short runs went direct at nice 15: the examples, the sortie enumerations (about 7 s each) and the c1 diagnostics.
- PIDs are in `verify/pids.log`, which also records one correction. None of these processes was killed.
- Both binaries (`bin_vk42`, `bin_vk42_d`) are deleted.
- Outputs over 256 KB are compressed with xz.
- No git was used.
