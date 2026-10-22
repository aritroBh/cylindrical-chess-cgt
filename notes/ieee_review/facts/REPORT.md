# IEEE Paper Fact-Check Report

## 5-Line Summary

This adversarial fact-check of the IEEE paper "Pawn Endgames on a Cylindrical Chessboard" recomputed every pawn position value and walk-through move using `cylcgt` under the e.p.-aware passed-pawn test (count rule). The paper's core numerical results (values, census counts, tablebase statistics) are correct and match independent verification [C2]. However, several walk-through descriptions contain inaccuracies in intermediate move values, some real-chess claims overstate the evidence by omitting "queen-promotion-only" and "e.p.-aware tree" qualifiers, and the 1/8 certification status is reported more strongly than the data supports. Chess legality issues: one diagram (Puzzle 3) correctly marked illegal (pawns on rank 1); all other FENs decode to legal positions.

---

## Fact-Check Table

| Location | Claim | Source / Recomputation | Verdict | Fix |
|----------|-------|------------------------|---------|-----|
| **sections/08_star2.tex:69–71** | Position A: after 1...d3-d4, c5xd4, 2.b3-b4 reaches ⋆ | `cylcgt` recomputation: after d3-d4, c5xd4, b3-b4 the value is +W (passed pawn), not ⋆. The move d3-d4 is winning (+W), but the paper's specific line "continues b3-b4 to ⋆" is incorrect. | **WRONG** | Change "white continues b3-b4 to ⋆" to "white continues b3-b4 to a winning position (+W)" or describe the correct canonical form derivation. |
| **sections/08_star2.tex:79–81** | Position B: after 1...a6-a5, 2.b4xa5, 3...c6-c5 reaches ⋆ | `cylcgt` recomputation: after a6-a5 the value is {⇑⋆ | -W}; after b4xa5 it is ⇑⋆; after c6-c5 it is ↑. None of these equal ⋆. | **WRONG** | Correct the intermediate values: "after b4xa5 the value is ⇑⋆; after c6-c5 it is ↑" or rephrase to reflect the correct canonical form. |
| **sections/05_sums.tex:49–50** | Puzzle 1 h/a component: "White's a5--a6 still wins outright, but black, moving first, plays h6×a5 across the seam and leaves ⋆" | `cylcgt` recomputation (textbook test): value is 255/2±+W (hot); White a5-a6 → +W; Black h6-h5 → ⋆; Black a6-a5 → +W±+W (race). The paper's simplified {+BIG | ⋆} omits Black's race option. | **OVERSTATED** | Note that Black also has a6-a5 leading to a race; the canonical form is more complex than {+BIG | ⋆}. |
| **sections/09_real.tex:52–55** | 1/8 certification: "All 306 end-position sides with at most seven men are resolved... 283 agree, 5 disagree, 2 are draws" | 283 + 5 + 2 = 290, not 306. 16 sides unaccounted for. | **WRONG** | Give the full breakdown or reword so numbers add up (e.g., "290 of 306 sides resolved: 283 agree, 5 disagree, 2 draws; 16 remain"). |
| **sections/09_real.tex:62–65** | Proposition: "conditional only on the king freeze" for 1/8 | RESULTS.md §6b: "queen promotions only, so not yet a full-chess certificate." The proposition omits the underpromotion caveat. | **OVERSTATED** | Change to "conditional on the king freeze and on an underpromotion rerun". |
| **sections/00_abstract.tex:9–10** | Abstract: "exact search leaves a single undecided end position" | The open item is one *side* (Black to move) of one end position, not a whole end position. | **OVERSTATED** | "a single undecided end-position side (Black to move)" or "one open side of one end position". |
| **sections/01_intro.tex:48–49** | Intro: "exact search on larger ones pins the oracle value between 0 and 1/8" | Same caveat: queen-promotion-only search. | **OVERSTATED** | Add "queen-promotion search" or "conditional on underpromotions". |
| **sections/04_kings.tex:127–135** | King-failure sweep: "159 of 500 get the wrong outcome... 18 through en passant" | kings/REPORT.md: sweep used *textbook* passed-pawn test. The paper presents this as a failure of its own (e.p.-aware) model without labeling it. | **OVERSTATED** | Label the sweep "(textbook test)" and note that under e.p.-aware test the 18 e.p. failures disappear and the 7×6 mismatch count falls from 143 to 138. |
| **sections/01_intro.tex:39–40** | Kings bullet: "the convention fails for 159 of 500 components" | Same issue: textbook test, not the paper's default e.p.-aware test. | **OVERSTATED** | Add "(textbook test)" or report the e.p.-aware numbers. |
| **sections/09_real.tex:27–30** | Theorem oracle-cand (a): "In real chess the side to move wins; only 1...b5 wins for black, 1.c4 wins for white, and every king move loses [C2]" | The Lichess tablebase confirms the root is N (side to move wins) and the winning moves. The "every king move loses" part is from the model with frozen kings, not from tablebase. | **UNSUPPORTED** | Clarify which parts are tablebase-verified vs. model-predicted. |
| **sections/09_real.tex:27–30** | Theorem oracle-cand (b): "In the e.p.-aware tree, under every draw treatment, O has left stop ≥1 and right stop ≤-1, so O is neither 0 nor ⋆2" | The paper presents this as holding for the e.p.-aware tree, but the intro bullet says "however draws are treated" without the e.p.-aware qualifier. | **OVERSTATED** | Intro bullet should specify "in the e.p.-aware pawn tree". |
| **sections/13_verify.tex:7–10** | Cross-checks: "all 4,967,550 outcomes of G+X match under the textbook test, e.p. on and off, and all 2,483,775 under the e.p.-aware test" | The numbers are correct per delegate/checks, but the e.p.-aware test count (2,483,775) is for one race rule only (count), not all three. | **UNSUPPORTED** | Specify "under the count rule with the e.p.-aware test". |
| **sections/06_atlas.tex:46–52** | "An independent minimax program confirms the textbook outcomes for all 1,223,689 positions" | atlas/cylinder/REPORT.md C9: minimax checked winners only, for 12,568 rings and 4,000 random flat components, not all 1,223,689. | **OVERSTATED** | "confirms the winners of all 12,568 rings and of 4,000 random flat components". |
| **sections/07_targets.tex:57–58** | Theorem thm:eighth: "has value exactly 1/8 in all nine settings... and for every assignment of outcomes to its race positions" | Verified by `cylcgt` and independent C solver for all 9 settings. The "every race outcome" claim was checked on the mirror position. | **OK** | Add "checked on its mirror image, which has the same value by symmetry" (already in SPEC). |
| **sections/07_targets.tex:73–75** | upsecstar walkthrough: White a2-a4 → 0, a2-a3 → ⋆; Black a6-a5 → ↓ | `cylcgt` confirms: {0, ⋆ | ↓} in all 9 settings. | **OK** | — |
| **sections/07_targets.tex:77–80** | Tiny 1 walkthrough: White a2-a3 → 0; Black a6-a5 → -1/2±1/2 = {0 | -1} | `cylcgt` confirms: tiny(1) under every race rule with e.p. on (count rule [C2], others [C1]). | **OK** | Note: C2 label holds only for count rule. |
| **sections/08_star2.tex:30–34** | Textbook candidate walkthrough (textbook test): White a2-a4 → ⋆, c2-c4 → 0; Black d7-d5 → ⋆, b7-b5 → 0 | `cylcgt` with textbook test confirms exactly these values. | **OK** | — |
| **sections/08_star2.tex:36–44** | Textbook candidate walkthrough (e.p.-aware): White a2-a4 → ⋆, c2-c4 → 2±1; Black d7-d5 → ⋆, b7-b5 → -2±1 | `cylcgt` with e.p.-aware test confirms exactly these values. | **OK** | — |
| **sections/08_star2.tex:48–50** | Census theorem: no ⋆2 with ≤6 pawns in default setting; 6,724 zeros, 4,042 stars | `cylcgt` and independent C solver agree on all 231,071 records. Codex solver finds no ⋆k for 2≤k≤292 among 793,299 placements. | **OK** | — |
| **sections/08_star2.tex:63–67** | Theorem thm:star2seven: Position A and B are ⋆2 in default setting | `cylcgt`, C solver, and Codex whole-board solver all confirm ⋆2 for both positions under count/aware. | **OK** | — |
| **sections/08_star2.tex:108–111** | Five-file ⋆2 positions: three 8-pawn positions are ⋆2 on flat 5 files | `cylcgt` and Codex confirm all three. | **OK** | — |
| **sections/06_atlas.tex:40–44** | Hottest position: ±3 at W a2 b4 / B a5 b7 | `cylcgt` confirms ±3. | **OK** | — |
| **sections/06_atlas.tex:55–59** | Cylinder-only values: 3/4 on C3, 1/4±1/4 on C3, {3/2±1/2 | -3/2±1/2} on C4 (textbook) | `cylcgt` confirms all three. The C4 candidate becomes {2±1 | -2±1} under e.p.-aware. | **OK** | — |
| **sections/10_tablebases.tex:17–38** | 4-man tablebase statistics (won%, longest mate) for plane/cylinder/torus | Two independent solvers agree on all 24 tables (~607M values) [C2]. | **OK** | — |
| **sections/10_tablebases.tex:65–88** | KPK statistics: cylinder 78.89% / 55.88% vs plane 76.51% / 58.09%; 16,538 flat draws → cylinder wins; 216 mutual zugzwangs | T10 and T25 cross-checks confirm all numbers [C2]. | **OK** | — |
| **sections/11_dawson.tex:48–57** | Dawson's chess: g(n) period 34, last exception n=51; ring rule g(n-3)=0 | `cylcgt.dawson.octal_0137` reproduces period 34 and last exception 51; cylinder win list matches paper: n=3,7,11,17,23,27,31,37,41,45,57. | **OK** | — |
| **sections/12_engines.tex:15–22** | Stockfish accuracy by CGT class at fixed depths | engine/runs/ analysis matches Table VI [C1]. Lc0 perfect at 1k–100k nodes [C1]. | **OK** | — |
| **sections/12_engines.tex:57–72** | ChessSums: 418 components, 26,000 rows; Stockfish 26.5–28.0%, Lc0 32.5–33.5% on winning moves | engine/runs/chesssums/ results match [C1]. Caveat stated: model ground truth, not real chess. | **OK** | — |
| **sections/appendix_table.tex:15–56** | FENs for all main positions | All FENs decode to legal positions (no pawns on rank 1/8, no adjacent kings, no side-not-to-move in check) except Puzzle 3 explicitly marked illegal. | **OK** | — |
| **sections/02_rules.tex:44–56** | e.p. test example W a2 / B b4: value 0 under default settings | `cylcgt` confirms value 0. Caption does not state the value. | **MINOR** | Add "value 0" to Fig. 2 caption. |
| **sections/02_rules.tex:96–101** | W a2 b3 / B b4: "every white move lets black capture on a3 and win the resulting race (count rule)" | `cylcgt`: under count rule, value 0 (P); under opponent rule, value +W (L). The claim is specific to count rule. | **OK** (with context) | Add "under the count rule" to the text. |
| **sections/04_kings.tex:223** | Proposition prop:horizon1: "for T=1 the counter-promotion condition holds in every context" | kings/theory/LOOPY.md: proof only covers counter-promotion, not full decisiveness. Theorem 2.7 (certificate implies V3) has a GAP. | **OVERSTATED** | Restate as "for T=1 the counter-promotion condition of the certificate holds in every non-terminal context [P]; decisiveness then follows from the certificate theorem, whose proof is still incomplete." |
| **sections/13_verify.tex:60–68** | "Each proof was then re-derived... Eight of the nine were confirmed... one gap was found" | REVIEW.md T2: only 9 specific statements were re-derived (L1.6, L2.1, L2.3, L3.3, L5.1–5.3, Thm 1.14(i), Thm 3.4, Thm 2.7, Prop 2.10(b)). Other [P] items (sandwich lemma, prop:horizon1) not among them. | **OVERSTATED** | List the actual statements re-derived; note that Theorem 2.7 still has a gap after later check. |
| **sections/01_intro.tex:32–33** | "The oracle value of the textbook candidate is never ⋆2, however draws are treated [C1]" | Section IX Theorem oracle-cand (b) says this holds only in the e.p.-aware tree. In the textbook tree, ⋆2 is excluded only when draws count as wins for one side. | **OVERSTATED** | "In the e.p.-aware pawn tree, the oracle value of the textbook candidate is never ⋆2 (or 0), however draws are treated." |
| **sections/09_real.tex:67–72** | "The same method applies to ⇑⋆ and Tiny 1: their lower bounds already equal the target values, with 11 and 13 end positions of 8 to 10 men still open" | These numbers appear first in the conclusion, not in Section IX body. | **UNSUPPORTED** | Move this sentence to Section IX-B before the conclusion. |
| **sections/14_conclusion.tex:17–18** | Open problem 5: "Misère Dawson's chess... Is the misère quotient of Dawson's chess infinite? By the ring rule, any answer for strips also answers the cylinder" | Section XI already states the misère ring rule. The conclusion repeats it as an open problem. | **OVERSTATED** | Change to: "Is the misère quotient of Dawson's chess infinite? By the ring rule of Section XI, any answer for strips is also an answer for the cylinder." |
| **sections/14_conclusion.tex:11–13** | Open problem 1: "The same pipeline then applies to ⇑⋆ and Tiny 1 (Section IX-B)" | Section IX-B doesn't mention ⇑⋆ and Tiny 1 end-position counts. | **UNSUPPORTED** | Add the sentence to IX-B as noted above. |

---

## Chess Legality Check

| Diagram / Position | Issue | Status |
|--------------------|-------|--------|
| Puzzle 3 (Fig. 5c) | White pawns on rank 1 (a1, c1, g1, h1) | **FLAGGED** — explicitly marked illegal in paper |
| Trébuchet across seam | Kings on h5/b4, pawns on a4/a5 | OK |
| Trébuchet T | Kings on f5/h4, pawns on g4/g5 | OK |
| King group Puzzle 2 | Kings on e6/d8, pawns on d7/e7 | OK |
| 1/8 position | Kings on f5/h4 (T), pawns on a2,b2,b3/a5,a6,b6 | OK |
| upsecstar | Kings on f5/h4 (T), pawns on a2,b2,b6/a6,b7,c5 | OK |
| Tiny 1 | Kings on f5/h4 (T), pawns on a2,b2,b6/a6,b7,c6 | OK |
| Textbook 1/8 | Kings on f5/h4 (T), pawns on a2,b2,d2/a5,c4,d7 | OK |
| Textbook upsec | Kings on f5/h4 (T), pawns on a3,c5,d4/a7,b7,d7 | OK |
| Candidate | Kings on f5/h4 (T), pawns on a2,c2/b7,d7 | OK |
| Second candidate | Kings on f5/h4 (T), pawns on a3,b3,c2/b5,b7,c6 | OK |
| Position A | Kings on f5/h4 (T), pawns on a4,b3,d2,d3/a7,b7,c5 | OK |
| Position B | Kings on f5/h4 (T), pawns on b4,c2,d2/a6,a7,c6,d5 | OK |
| Five-file ⋆2 | Kings on f5/h4 (T), pawns on a3,b3,c2,e2/a6,c5,d5,e3 | OK |
| KPK rook pawn | Kings on a6/a8, pawn on a5 | OK |

---

## Reproduction Commands

All `cylcgt` recomputations were run with:
```bash
cd /Users/aritro/Downloads/Research/Chessendgames
PYTHONPATH=. .venv/bin/python -c "
from cylcgt.pawns import Board, Pos, value
from cylcgt.cgt import show
import cylcgt.pawns as pawns
pawns.PASSED_RESPECTS_EP = True  # e.p.-aware test
pawns._value.cache_clear()
# ... position-specific code
"
```

Key values verified:
- Textbook candidate (flat, textbook): `*2`
- Textbook candidate (flat, e.p.-aware): `{2±1 | -2±1}`
- Position A (flat, e.p.-aware): `*2`
- Position B (flat, e.p.-aware): `*2`
- C3 ring (6 pawns): `*2`
- C4 ring (7 pawns): `*2`
- 1/8 position: `1/8` (all 9 settings)
- upsecstar: `{0, * | ↓}` (all 9 settings)
- Tiny 1: `tiny(1)` (all race rules, e.p. on)
- Hot3: `±3`
- C3 3/4: `3/4`
- C3 1/4±1/4: `1/4±1/4`
- Dawson g(n): period 34, last exception 51
- Cylinder wins: n=3,7,11,17,23,27,31,37,41,45,57

All match the paper and SPEC.md fact sheet.