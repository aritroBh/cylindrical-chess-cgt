# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260517 | 10 | `56ff07ea6dbabff1986033fe204d0eb1ae3f5bfef5cfbc08d7bf94fecb2fbce0` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 780780 | 99 | `3e294699bc315e8facb612ae80feb2b90df317162693c1e570dee7538d6ffddd` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous: `tog.tex` contains the author name and the GitHub URL inside the `\else` branches, so do not send sources for review without stripping them. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261099 | 10 | `961f511cb0f52b1fb875215c97e8ad071c7449353dbad2939f6a672d34ef5bde` |
| `dist/tog/supplement.pdf` | 781040 | 99 | `06e1c7bad0c40d21e96fdd1f4d2e154c5d6f1e238cfde01dc12d7bb94c31f7e7` |

Maximum upload size per file in ScholarOne for ToG: not verified.
