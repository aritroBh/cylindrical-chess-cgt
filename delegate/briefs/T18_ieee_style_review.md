# T18: style, flow and IEEE-compliance review of the paper

**Output directory:** `notes/ieee_review/style/`.

**Input:**
- `paper/ieee/` (main.tex, sections, main.pdf), written by T16;
- `paper/ieee/SPEC.md` and `paper/STYLE.md`;
- the author's own 2025 writing in `prior_work/main.tex`, which is the voice to match.

**Task.** Review as a demanding IEEE Transactions on Games referee and copy editor.
1. **Flow.** Does it read easily from start to finish? Point out every repetition, every jump, every term used
   before it is defined, and every paragraph that could be cut.
2. **Voice.** Does it sound like the 2025 author (clear "we", move-by-move walk-throughs), while staying
   professional? Point out sentences that sound generic or machine-written.
3. **IEEE compliance.**
   - abstract of 150–250 words, with no citations or abbreviations in it;
   - Index Terms;
   - section and figure numbering, captions (figures below, tables above);
   - every figure and table referenced in the text;
   - reference style and completeness: authors, title, venue, year, pages;
   - the acknowledgment section;
   - hyphenation, units, math typography.
4. **Layout.** Look at the PDF for overfull lines, figures far from their first mention, widows, unreadable
   diagrams and empty space.
5. Check that there are no placeholders, TODOs, "VERIFY" notes or code listings.

**Deliverable: REPORT.md**
- A prioritized list of concrete edits, each giving file:line, the problem and the replacement text.
- Then an overall verdict: what still keeps it from looking professional.
- Do not edit the paper.
