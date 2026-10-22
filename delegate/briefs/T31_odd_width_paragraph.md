# T31: draft a paper paragraph on odd-width cylinders (writing; no compute beyond re-reading files)

**Output directory:** `notes/paper_drafts/`.

**Sources** (verified):
- `research/odd_cylinders_verify/REPORT.md`, `summary.txt` and `counterexamples.txt` (T25);
- `delegate/REVIEW.md` (T25 section).

**Write** `odd_width.tex`: one LaTeX paragraph of at most 170 words, plus one small table (booktabs, at most 6
rows), for Section X-A of the paper (`paper/ieee/sections/10_tablebases.tex`, "King and Pawn Against King").
- **Voice:** plain "we", concrete positions, short.
- **Content:** KPK on Cn × 8 for n = 3 to 10:
  - White-to-move win rates;
  - mutual zugzwang counts;
  - the trébuchet is a mutual zugzwang for n ≥ 4 and illegal on C3;
  - two counterexamples, with what each shows: `Ka3 Pa2 ka5` is D/D on the ordinary board but a mutual
    zugzwang on every cylinder, and `Ka1 Pa7 ka3` is a win on C3, by mate on the wrapped diagonal;
  - no odd/even effect.
- **Labels:** `\lab{C2}` and `\lab{C1}`, matching the sources.
- **Format:** use the paper's macros (`\cyl{n}`, `\pos{...}`; see `paper/ieee/macros.tex`).
- **Do not edit `paper/`.** Also write `odd_width_notes.md`, mapping every number to its source line.
