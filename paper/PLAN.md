# Paper and remaining research (2026-10-21)

**Target:** one self-contained paper. Results it does not have yet are listed as open problems, not hidden.
Upload `paper/` to Overleaf as a zip; the main file is `main.tex`.

## The niche (checked against our literature notes, `notes/lit_*.md`)

- **CGT on cylinder or torus boards.** No prior work found.
- **Elkies' pawn game without board edges, on cyclic boards.** Never studied.
- **Tablebases for cylinder and torus chess.** None published. Our KBBK result contradicts a published claim
  by Muller.
- **Real-chess certification of Elkies-style values.** Never done: the real-chess oracle value of §6.
- **Exact validity conditions for the frozen-king convention.** Not in the literature; Mäser only warns that it
  is heuristic.

## Section map

| § | Content | Source | Status |
|---|---|---|---|
| 1 | Introduction and contributions | — | written |
| 2 | CGT background and Elkies' conventions | — | written |
| 3 | The model made precise: the e.p.-aware passed test, condition (E), the cut lemma, HSS | `notes/lemmas.md`, `cylcgt/` | written |
| 4 | Audit of the 2025 paper | `notes/audit.md` | written |
| 5 | Value atlases: flat vs cylinder; Elkies targets | `atlas/` | written |
| 6 | The \*2 question; the real-chess oracle value | `realchess/` | written |
| 7 | Explicit kings: when the frozen trébuchet is exact | `kings/` | written |
| 8 | Cylinder and torus tablebases | `tablebase/replica/` | written |
| 9 | Dawson's chess on the cylinder | `dawson/` | written |
| 10 | Engines and learning | `engine/`, `bench/` | written; ML results pending (T5/T6) |
| 11 | Verification protocol and reproducibility | — | written |
| 12 | Open problems | — | written |

## Research still to do, ranked by value to the paper

1. **Real-chess certification of the robust 1/8** (`W a2 b2 b3 / B a5 a6 b6` + trébuchet, 10 men).
   - The ≤7-man end positions are being resolved now (`realchess/targets18/`).
   - If the oracle value is pinned at 1/8 using only exact results, this becomes the headline: the first
     real-chess certified small dyadic value. If not, report the bounds.
2. **Independent non-Claude re-check** of the §5–6 headline numbers (T1, codex, running).
3. **Second-model proof review** (T2: reassign to opencode) and a human read-through by Aritro.
4. **Cylinder atlas under the e.p.-aware test** (T4, opencode, running).
5. **Elkies-target robustness and reachability table** (T3: reassign to opencode or codex).
6. **ML baselines** on ChessSums (T5) and Dawson's chess (T6). Both CLIs were out of quota; reassign. Optional
   for this paper.
7. **5-man cylinder and torus tablebases** (plan B2 extension). Optional; it strengthens §8.
8. **Mentor review** (Prof. Morley), once Aritro decides.
