# Audit of the June 2025 paper (machine-checked)

Solver: `cylcgt/` (exact canonical forms). Reproduce with
`.venv/bin/python -m cylcgt.verify_paper` (raw output in `verify_paper_output.txt`).

Conventions:
- 8x8 cylinder, en passant on unless stated.
- A passed pawn is worth ±BIG; "+W" means a won (passed-pawn) value.
- Promotion races use the "count" rule.

An independent re-transcription of every diagram, done blind, is in
[`diagram_audit.md`](diagram_audit.md). It found no wrong square, piece or colour. It did correct
three of this audit's explanations: the 7.1 a/h diagnosis, the 7.2 king group, and the 7.3 spare
king moves. The table below includes those corrections.

| Pos. | Paper claims | Computed | Verdict |
|---|---|---|---|
| 2.1 e4/e5 | 0 | 0 | ✅ |
| 2.2 a2,h1 / a3,h4 | 0 | 0 | ✅ value; ⚠️ white pawn on h1 is illegal in chess |
| 2.3 c1,d2 / c4,d3 (flat copy of 2.2) | 0 | 0 | ✅; ⚠️ c1 illegal |
| 3.1 a3,h1 / a4,h5 | 1 | **1 with e.p., 2 without** | ✅ only because of wrap-around en passant, which the paper never mentions; ⚠️ h1 illegal |
| 3.2 a4,h1 / a5,h6 | 2 = {0,1 \| } | 2 | ✅ value, but the option list is wrong: there is no move to 0, because there is no double step from h1. {1 \| } = 2 anyway. ⚠️ h1 illegal |
| 4.1 e4/e6 | * | * | ✅ |
| 4.2 e3/e6 (as drawn) | ↑ | **0** | ❌ the diagram is one rank off. Of five placements tried, only e2/e5 gives the text's {0,\* \| \*} = ↑ |
| 4.3 tiny | {0‖0\|−1} | tiny(1) = {0‖0\|−1} | ✅ |
| 5.1 trebuchet (cylinder) | 0 | every king move drops a pawn | ✅ a mutual zugzwang across the seam |
| 7.1 c-file | ±1 | ±1 | ✅ |
| 7.1 f-file | {{2\|1}\|0} | {{2\|1}\|0}, mean 3/4, temp 3/4 | ✅ |
| 7.1 a/h files | 1 | **{+W \| \*}** (hot) | ❌ The paper does play h6×a5. Its error is to call a position that White wins either way (an L-position) "1". Sum tests in two independent engines refute "= 1" |
| 7.1 total | 1 ± 1 + {{2\|1}\|0} | Left wins either way, but not this value | ❌ (follows from the a/h error) |
| 7.2 pawn part {a,b,h} | ±1 | an infinitesimal-heavy game with ⇑/⇓ parts, mean 0, temp 0; outcome N (R without e.p.) | ❌ |
| 7.2 king group Ke6, d7 / Kd8, e7 | 0 | every king move drops a pawn (White: Kd5/e5/f5/f7 drop d7; Black: ...Kc7 drops e7, then d8=Q) | ✅ under the convention it **is** a mutual zugzwang, though not the 5.1 pattern. Caveat: by the pawn-only definition both d7 and e7 count as "passed", so the king blockade has to be modelled explicitly |
| 7.3 | 2 | already decided: a5 and f7 are passed pawns | ❌ The position is decided at move 0. Four white pawns stand on rank 1 (illegal). The kings have spare moves (Kg8–f8 and Kf6–g6), so the group is not a zugzwang |
| 7.3 {c,d} sub-game | 1 | **tiny(1)** (e.p. on and off; also after shifting to legal ranks) | ❌ sum tests in two independent engines refute "= 1" |
| §1 rules text | knight on h1 "can additionally move to a1 and a2" | the extra knight squares are a3 and b2 | ❌ a1 and a2 are extra *king* squares |
| §8 Dawson's chess | rule "remove a pawn whose neighbours are empty" | no first move is possible from a full row under that rule | ❌ needs restating as octal game 0.137 (Dawson's Kayles); the ring version should then be derived from the 3×n cylinder pawn game directly |

**Caveat on the rank-1 diagrams.** Shifting 2.2, 2.3 and 3.2 up one rank makes them legal, but they then keep
the paper's values only with en passant. Without it the shifted values are 1, 1 and ⇑\*.

**What still stands.** The overall method is right: decompose positions, compute canonical values, and use
numbers, infinitesimals and temperature. The f-file, c-file, tiny, star and trebuchet computations are correct.
