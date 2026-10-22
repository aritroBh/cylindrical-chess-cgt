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
# Your part: K1a, Section 1 and Theorem 2.4

**Output directory:** `kings/delegate/out/K1a/`.

Items to fix (see REVIEWS.md):
- **Definition 1.10 and Theorem 1.11(b).** The threat set must count moves into ⊕ or ⊖ by *either* player
  (Review 1 item 1; Review 2 item 1).
- **Definition 1.5 and the remark after Theorem 1.9.** "S(X) is cylcgt.pawns.value" is false, because
  cylcgt re-splits components at every node (Review 2 item 2). State (V4) hereditarily, on the re-split
  components, with the king group Z deleted (Review 2 item 5).
- **Proposition 1.13** (Review 1 item 2; Review 2 item 3). Use A′ = { | ⊖}, whose translation is −B−1, or
  restate it for {∅ | ⊖}.
- **Theorem 3.3(b):** make it consistent with the corrected 1.13 (Review 1 item 2).
- **Theorem 1.14:** fix (ii), (iii) and the sharp form (Review 2 items 5 and 6).
- **Theorem 2.4:** restrict G to games without draws. The P-game alternative is false: Review 2 item 4
  gives a counterexample.
- **The "each hypothesis is needed" table in §1.5:** fix the (V1a) and (V1b) rows (Review 1 item 4; Review 2
  item 7).
- **(A_Q)** (Review 1 item 6; Review 2 item 8). It is false in general: `Ke2 Pb5 ka5 w -` is a
  promotion-model win and a chess draw. Make it a per-position hypothesis that kpsolve checks.
- **Definitions 1.5 and 1.10, minor items:** Review 2 items 9 and 10.
