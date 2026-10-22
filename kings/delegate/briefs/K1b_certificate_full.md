# K1 (split): exact edits to the A8 theory note after four adversarial reviews

The note `kings/theory/LOOPY.md` (labels PROVED / CONJECTURE / KNOWN on every claim) was reviewed by four
referees, whose reports are in `kings/theory/REVIEWS.md` with numbered items. Do **not** edit `LOOPY.md`.
Instead write a list of exact text edits to it, covering only your part (below). They will be checked and
applied by script.

Also read:
- `kings/results/PREDICTIONS.md`: the exact chess solver's results for the §6 predictions;
- `kings/results/theory_P4_cap2_moves.txt`;
- `kings/SPEC.md`: the chess rules.

You may run the solver: build it with `cc -O2 -o <your output dir>/kp kings/kpsolve.c`, then run
`echo "Ka5 Pb4 kc6 pb5 w -" | <your output dir>/kp --board cyl:7x6 --cap 1`. Keep runs small.

## Output format: `EDITS.md` in your output directory

One block per edit, in this exact format (the markers must start their lines):

```
### EDIT <n>: <review item, e.g. R2 item 1>
<<<<<<< OLD
<text copied EXACTLY from LOOPY.md, several full lines, unique in the file>
=======
<the replacement text>
>>>>>>> NEW
```

Rules:
- **OLD** must be copied character for character, including the Markdown and the Unicode symbols (⊕ ⊖ ⊞
  𝓛 𝓡 𝓝 𝓟 ≥ —). It must occur exactly once in the file. Keep it short, 1–8 lines.
- **NEW** keeps the note's style.
  - Mark every change inline with "(revised after review: R<k> item <n>)".
  - Every claim keeps exactly one label: PROVED, PROVED after repair, CONJECTURE, GAP (proof incomplete),
    KNOWN, or FALSE as originally stated (then give the corrected statement).
  - Use PROVED after repair only if NEW contains the complete repaired proof. Otherwise label it GAP or
    CONJECTURE.
- After the edits, add a section `## STATUS ROWS`. It holds one Markdown table row per numbered result in
  your part: `| result | final label | one-line note with review item |`.

Also write `REPORT.md` in your output directory: a 5-line summary, then the list of edits made.
# Your part: K1b, Section 2 from Definition 2.5 on

**Output directory:** `kings/delegate/out/K1b/`.

Items to fix (see REVIEWS.md, especially Review 3 and Review 1 items 3, 7, 8, 9):
- **Definition 2.6 and Theorem 2.7.** The pass-budget step is invalid.
  - Replace it by the argument with an unlimited pass budget (k = ∞) plus (L3): the real defender's options
    are a subset of the k = ∞ game's, and its only gain from fewer options is stalemate, which (L3)
    excludes. Write the repaired proof in full if you can.
  - Drop "every k is needed".
  - Note that (L3′) cannot apply for T ≥ 2 on a 3-file group.
- **Corollary 2.8:** the minor wording point.
- **Lemma 2.9:** state the hidden hypothesis (the defender has no pawns the attacker's pawns can capture).
- **Proposition 2.10(a):** needs H ≥ 5 (4-rank double steps). Proposition 2.10(b): its last sentence is a
  CONJECTURE.
- **Remark 2.11:** label it, and state why the certificate does not apply as written.
- **The (L1) evidence claims in §5.1:** budgets k ≤ 4 and ∞ were checked, not "every budget".
