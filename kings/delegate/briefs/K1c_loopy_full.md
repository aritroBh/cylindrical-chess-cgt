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
# Your part: K1c, Sections 3–6 and Appendix A

**Output directory:** `kings/delegate/out/K1c/`.

Items to fix (see REVIEWS.md, especially Review 4 and Review 1 items 5, 10, 11):
- **Theorem 4.2:** the gap.
- **Proposition 4.3:** false as stated (a check counterexample). Correct it, or downgrade it.
- **§4 commentary:** the minor items.
- **§5 labels and wording** (§5.1 "PROVED (diagram audit)", §5.2, §5.5, §5.6, "So Z_onT1 realises on"):
  label every unlabelled claim.
- **§6:**
  - Add kpsolve's result for every prediction, from `kings/results/PREDICTIONS.md`.
  - P4 (a CONJECTURE) is refuted in 3 of its 6 contexts: H\* and H\*2 (White to move draws), and H0 (Black to
    move draws). The mechanism is in `theory_P4_cap2_moves.txt`: the defending king walks to the locked
    context pawns. This is consistent with Proposition 2.10(b).
  - Replace the "naive convention" headline with the honest comparison. Literal cylcgt gets P2, P3 and P10
    right, so those do not separate the theory from cylcgt. The cases that do are P1, P5, P7, P9 and P4.
  - The P2 + H\* note: e3–e4 stalemates Black.
- **Appendix A and Conjecture 4.7:** the pawn-count mismatch.
