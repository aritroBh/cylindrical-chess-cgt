# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260599 | 10 | `f96336fcfbf8d2d514d5640d519907f4019998472dd242f7999ad8294eced5d0` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 829690 | 106 | `20951b098c780afbd4efbc39aace9dd367c5178792864aaf78223a0a766f3e8a` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous: `tog.tex` contains the author name and the GitHub URL inside the `\else` branches, so do not send sources for review without stripping them. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261176 | 10 | `049403d730ce36918ecbaba650a280c18118e04ee65a879851e23380aeaa6314` |
| `dist/tog/supplement.pdf` | 830013 | 106 | `bde29999504022f07379e108838fc971c379ec16f9da2b382244226c89dbf46b` |

Maximum upload size per file in ScholarOne for ToG: not verified.
