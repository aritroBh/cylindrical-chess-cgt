# K1a — exact edits to `kings/theory/LOOPY.md` (§1 and Theorem 2.4)

## Summary (5 lines)

1. All eight defects in the K1a brief are fixed in `EDITS.md` (29 edit blocks, all OLD blocks verbatim from
   `LOOPY.md` and each occurring exactly once; `apply_edits.py` applies all 29 with 0 rejected).
2. The threat set τ of Definition 1.10 now counts options to ⊕/⊖ by **either** player, and Theorem 1.11(b) is
   re-proved on that τ (PROVED after repair); the counterexample of R1 item 1 / R2 item 1 is excluded by it.
3. `S(X)` is no longer identified with `cylcgt.pawns.value`: it is the **re-splitting** BIG value, and the new
   Theorem 1.11(c) proves the hereditary (HSS) version of Theorem 1.11 for it; (V4) is restated accordingly,
   with the king group Z deleted.
4. Proposition 1.13 is restated with A′ = { | ⊖} (translation −B−1) and Theorem 3.3(b) is made consistent;
   Theorem 1.14(ii)/(iii) and its sharp form are repaired, and Theorem 2.4 is restricted to games without
   draws with a new strategy-transfer form (c).
5. (A_Q) is demoted from an axiom to the per-position hypothesis (A_Q)(X) (false in general: two solver
   counterexamples given), and the "each hypothesis is needed" table now says honestly that (V1a) is a
   CONJECTURE.

## What was established, and with what label

| item | final label | evidence |
|---|---|---|
| Def 1.10 τ (either player) | PROVED after repair | full proof in the note; the τ of `notes/lemmas.md` Def 2.0 |
| Thm 1.11(b) | FALSE as originally stated → PROVED after repair | full proof in the note (frontier + tempo count) |
| Thm 1.11(c) (re-splitting, new) | PROVED after repair | full proof in the note; L2.1/Thm 2.1 of `notes/lemmas.md` in D-game language |
| Def 1.5, S(X) = cylcgt | FALSE as originally stated → corrected definition | counterexample computed (see below) |
| Def 1.5, the Z-terminal | wording corrected | R2 item 10 |
| Remark after Thm 1.9 | corrected (it was false for cylcgt) | R2 item 2 |
| Prop 1.13 | FALSE as originally stated → PROVED after repair | regimes re-derived and computed |
| Thm 3.3(b) | PROVED after repair, now { \| ⊖} | R1 item 2 |
| Thm 1.14(ii) | GAP → PROVED after repair | (V4) hereditary, Z deleted, corrected τ; uses (i) and 1.11(c) |
| Thm 1.14(iii) | PROVED, but a tautology | (A_Q)(X) is per position |
| Thm 1.14, sharp form | FALSE as originally stated → PROVED after repair | every legal Z-move of the loser at its turns must be a P-loss |
| Thm 2.4 | FALSE as originally stated (the P-game option) → PROVED after repair | G without draws, plus form (c) |
| (A_Q) | FALSE as a general statement → per-position hypothesis (A_Q)(X) | two solver counterexamples |
| §1.5 table | (V1b) row corrected; (V1a) "needed" is a CONJECTURE | R1 item 4, R2 item 7 |
| Def 1.10 minor items | corrected (M of a sum, the 6p ≤ 48 bound, a final Z-move) | R2 item 9 |

## The 29 edits

Numbers are the order in `EDITS.md`; the review item is in the heading of each block.

| # | review item | what it changes |
|---|---|---|
| 1 | R1 item 6, R2 item 8 | §0: the axiom (A_Q) becomes the per-position hypothesis (A_Q)(X) |
| 2 | R1 item 1, R2 items 1 and 2 | §0: the (V4) bullet says the check is hereditary and either-player |
| 3 | R1 item 1, R2 item 1 | §0 results table, row T1.11 |
| 4 | R1 item 2, R2 item 3 | §0 results table, row P1.13 |
| 5 | R2 item 8 | §0 results table, row T1.14 |
| 6 | R2 item 4 | §0 results table, row T2.4 |
| 7 | R2 items 2 and 10 | Def 1.5: the Z-terminal and the identification of S(X) |
| 8 | R2 item 2 | the bridge diagram: S --Thm 1.11(c)--> D --Thm 1.14--> P --(A_Q)(X)--> C |
| 9 | R1 item 11 | notation o(·), W(X), S(X), HSS (used by §6, P11) |
| 10 | R1 item 6, R2 item 8 | the axiom (A_Q) itself, with the two counterexamples |
| 11 | R2 item 2 | the remark after Theorem 1.9 |
| 12 | R2 item 9 | Def 1.10: M of a sum is the sum over the coordinates |
| 13 | R1 item 1, R2 items 1 and 9 | Def 1.10: the threat set τ, and the tempo bound (≤ 6p, p ≤ 42, +1 for a Z-move) |
| 14 | R1 item 1, R2 item 1 | Theorem 1.11: heading and statement of (b) |
| 15 | R1 item 1, R2 item 1 | Theorem 1.11: repaired proof of (b) |
| 16 | R2 item 2 | the remark after Theorem 1.11 and the new Theorem 1.11(c), with its proof |
| 17 | R1 item 2, R2 item 3 | Prop 1.13: statement, with A′ = { \| ⊖} and the {∅ \| ⊖} variant |
| 18 | R1 item 2, R2 item 3 | Prop 1.13: proof |
| 19 | R1 item 2 | Theorem 3.3(b) |
| 20 | R2 item 9 | the tempo bound quoted after Prop 1.13 |
| 21 | R2 items 2, 5 and 8 | Theorem 1.14: heading (label) |
| 22 | R2 items 2 and 5 | Theorem 1.14: the hypothesis (V4) |
| 23 | R2 items 2, 5 and 8 | Theorem 1.14: conclusions (ii) and (iii) |
| 24 | R2 items 2 and 5 | Theorem 1.14: proof of (ii) and (iii) |
| 25 | R2 item 6 | Theorem 1.14: sharp form |
| 26 | R1 item 4, R2 item 7 | the sentence above the "each hypothesis is needed" table |
| 27 | R1 item 4, R2 item 7 | the table: rows (V1b) and (V1a) |
| 28 | R2 item 4 | Theorem 2.4: statement, forms (a)–(c), and the P-game counterexample |
| 29 | R2 item 4 | Theorem 2.4: proof of (c) |

## Computational claims and how to reproduce them

All of them are in `kings/delegate/out/K1a/verify.py`; run

```
cd /Users/aritro/Downloads/Research/Chessendgames
PYTHONPATH=. .venv/bin/python kings/delegate/out/K1a/verify.py
```

| # | claim | label | output |
|---|---|---|---|
| 1 | Prop 1.13 with A′ = { \| −B}, B = 4: n = 0..7 gives 𝓡,𝓡,𝓡,𝓡,𝓡,𝓟,𝓛,𝓛 | COMPUTED-1 (`cylcgt.cgt`) | `R R R R R P L L` |
| 2 | the {0 \| −B} (dead position) reading gives 𝓝,𝓝,𝓝,𝓝,𝓝,𝓛,𝓛,𝓛 | COMPUTED-1 | `N N N N N L L L` |
| 3 | the frontier of the R1/R2 counterexample is B + { \| −B} = −1, an 𝓡-position, for every B | COMPUTED-1 | `B=2,3,4,10,100 → -1 R` |
| 4 | Prop 1.12's BIG part: {B \| 0} + {0 \| −B} = 0 for every B (so 1.12 is sound) | COMPUTED-1 | `is 0: True` |
| 5 | the positive integer B has canonical form {B−1 \| } and −B has { \| −B+1} (so the opponent cannot move in a positive summand) | COMPUTED-1 | `True True` for B = 1, 2, 4, 256 |
| 6 | R2 item 2: flat 7×6, e.p. on, count rule, `W: b2 d3 f2 / B: c4 c5 e5 g5` is **one** component at the root, o(S) = 𝓝, o(W) = 𝓡, and it is **not** HSS | COMPUTED-1 (`lemmas/common.py`) | `components 1; o(S)=N; o(W)=R; HSS False` |

Chess claims, with `cc -O2 -o kings/delegate/out/K1a/kp kings/kpsolve.c` (the binary is in the output directory):

| claim | label | command and output |
|---|---|---|
| R2 item 4: `Ka4 Pb3 Pe3 kc3 pb4 pe4` (cyl:7x6) is (D, D) in P, (L, W) frozen, and White to move is L in chess | COMPUTED-1 | `printf 'Ka4 Pb3 Pe3 kc3 pb4 pe4 w -\\nKa4 Pb3 Pe3 kc3 pb4 pe4 b -\\n' \| kp --board cyl:7x6 --cap 1` → `L L` / `W D`; with `--frozen` → `L L` / `W W` |
| R1 item 6 / R2 item 8: `Ke2 Pb5 ka5 w -` (cyl:7x6) is a P-win and a chess draw | COMPUTED-1 | `kp --board cyl:7x6 --cap 1` → `D D`; `--frozen` → `W W` |
| R1 item 6: flat 4x4 `Kd1 Pb3 ka3 w -` is a P-win and a chess draw | COMPUTED-1 | `kp --board flat:4x4 --cap 1` → `D D`; `--frozen` → `W W` |
| R2 item 7: `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` (cyl:7x6) is (D, D) in the frozen model | COMPUTED-1 | `kp --board cyl:7x6 --cap 1 --frozen` → `D D` / `D D` |

## Notes for the coordinator

- The `## STATUS ROWS` section at the end of `EDITS.md` agrees row by row with the note's own
  "Status after review" table for every result in this part (T1.9, T1.11(a)(b)(c), P1.12, P1.13,
  T1.14(i)(ii)(iii), the sharp form, §1.5's table, T2.4, T3.3(b), (A_Q)), so the status table can be kept
  as it stands.
- The new Theorem 1.11(c) is the note's version of L2.1 (Theorem 2.1) of `notes/lemmas.md`; it is stated and
  proved in D-game language, so the note no longer needs the "L2.1 restated" claim that R2 item 1 rejected.
- §6's P11 row uses `o(W(X))` and "hereditarily sum-safe"; edit 9 defines both (R1 item 11) in §1.2. K1c may
  still want to touch that row; the definitions are in a separate place, so there is no overlap.
- The (V1b) row now cites the frozen model as the isolated witness; K1b's edits to §5.4 are unaffected.
- `LOOPY.md` itself was not modified. `make_edits.py` regenerates `EDITS.md` from the note, so the OLD blocks
  are guaranteed to be verbatim; `apply_edits.py` reports 29 applied, 0 rejected.
- Negative results reported plainly: no (V1a) counterexample exists in the project, so "each hypothesis is
  needed" is left unproved for (V1a) and labelled CONJECTURE; the P-game variant of Theorem 2.4 is false, not
  merely unproved, and the counterexample is given.
