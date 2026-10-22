# T19 (codex): revise the IEEE paper from the two reviews

**Output directory:** `paper/ieee/`. You own it now.

**Input:**
- `notes/ieee_review/facts/REPORT.md` (T17);
- `notes/ieee_review/style/REPORT.md` (T18);
- `paper/ieee/SPEC.md`.

**Task.**
1. Apply every WRONG / UNSUPPORTED / OVERSTATED fix.
2. Apply the style edits that improve clarity or concision. Do not water down the author's voice.
3. Rebuild with `cd paper/ieee && tectonic -X compile main.tex`: no errors, no undefined references, no overfull
   box over 5pt.

**Deliverable.** Append a "Revision" section to `paper/ieee/REPORT.md`: each review item with applied /
rejected (and why).
