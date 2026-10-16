# Audit of the June 2025 paper (machine-checked)

Solver: `cylcgt/` (exact canonical forms). Reproduce with
`.venv/bin/python -m cylcgt.verify_paper` (raw output in `verify_paper_output.txt`).
Conventions: 8x8 cylinder, passed pawn = ±BIG, promotion race rule "count",
en passant on unless stated. "+W" = a won (passed-pawn) value.

| Pos. | Paper claims | Computed | Verdict |
|---|---|---|---|
| 2.1 e4/e5 | 0 | 0 | ✅ |
| 2.2 a2,h1 / a3,h4 | 0 | 0 | ✅ value; ⚠️ white pawn on h1 is illegal in chess |
| 3.1 a3,h1 / a4,h5 | 1 | **1 with e.p., 2 without** | ✅ only because of wrap-around en passant; the paper never mentions this; ⚠️ h1 illegal |
| 3.2 a4,h1 / a5,h6 | 2 | 2 | ✅; ⚠️ h1 illegal |
| 4.1 e4/e6 | * | * | ✅ |
| 4.2 e3/e6 (as drawn) | ↑ | **0** | ❌ diagram is one rank off; e2/e5 gives ↑ as the text argues |
| 4.3 tiny | {0‖0\|−1} | tiny(1) = {0‖0\|−1} | ✅ |
| 7.1 c-file | ±1 | ±1 | ✅ |
| 7.1 f-file | {{2\|1}\|0} | {{2\|1}\|0}, mean 3/4, temp 3/4 | ✅ |
| 7.1 a/h files | 1 | **{+W \| \*}** (hot, temperature ≈ BIG/2) | ❌ misses wrap captures a5×h6 and h6×a5 |
| 7.1 total | 1 ± 1 + {{2\|1}\|0} | Left wins either way, but not this value | ❌ (follows from the a/h error) |
| 7.2 pawn part | ±1 | an infinitesimal-heavy game, mean 0, temp 0, outcome N (R without e.p.) | ❌; also the king/pawn group is **not** a trebuchet: d7 is passed, and ...Kc7 is available |
| 7.3 | 2 | already decided: a5 and f7 are passed pawns | ❌ position is decided at move 0; four white pawns on rank 1 (illegal); the "trebuchet" kings both have spare tempo moves (Kg8–f8/h7, Kf6–g6), so it is not a zugzwang |
| §8 Dawson's chess | rule "remove a pawn whose neighbours are empty" | no first move is possible from a full row under that rule | ❌ needs restating as octal game 0.137 (Dawson's Kayles); ring version is then a one-line consequence and should be derived from the 3×n cylinder pawn game directly |

What still stands: the qualitative program (decompose positions, compute canonical values, use numbers/infinitesimals/temperature) is right, and the f-file, c-file, tiny and star computations are correct.
