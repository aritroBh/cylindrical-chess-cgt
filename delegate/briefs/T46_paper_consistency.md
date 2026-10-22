# T46: consistency audit of the finished paper against the evidence files (read-only, light)

**Output directory:** `notes/consistency_t46/` (write `REPORT.md` there; edit nothing else).

The paper is `paper/ieee/sections/*.tex` (IEEE format, 14 pages; build is not needed). Many numbers were edited
in the last two days. Check every number and every claim label in the paper against the evidence:
`RESULTS.md`, `delegate/REVIEW.md` (the latest sections win where they differ from older ones), and the
REPORT files they cite.

**For each section, list:**
- every number in the text or a table that does not match the evidence, or has no evidence you can find;
- every claim whose label (P, AI, C2, C1, Conj; defined in `sections/01_intro.tex`) is stronger than the
  evidence supports;
- statements that contradict each other inside the paper (for example a count stated twice differently);
- broken cross-references (a `\ref` to a label that does not exist).

Give file, line, the quoted text, what the evidence says (with the file path), and a minimal fix. Do not report
style or taste. If a section is clean, say so. Finish with a short count of findings by severity.
