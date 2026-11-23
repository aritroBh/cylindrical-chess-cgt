# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260519 | 10 | `022185ae040dca0e676a91c0380494fa695119ca93e7fbe7007745473833a7cd` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 761483 | 95 | `865a7631d78713979180acc156a1357072185f093366e6d4b8e7e670c015be7e` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous: `tog.tex` contains the author name and the GitHub URL inside the `\else` branches, so do not send sources for review without stripping them. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261094 | 10 | `7d360d40268cd43e7bca3e7bf8d7dc83a9115f0691decf48bb434809996fff7e` |
| `dist/tog/supplement.pdf` | 761714 | 95 | `a149ff40a05b22b8d47551276fb17b96856930ada63a6f78a859a603560e2b8a` |

Maximum upload size per file in ScholarOne for ToG: not verified.
