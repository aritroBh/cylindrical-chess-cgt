# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260336 | 10 | `87f686a6c880bbab23f08b8383811401470b8054afe8de169895e9cd8a488e82` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 760679 | 95 | `42e909f205072e963101e7fb923a24e376d908439d373698a0b6707c8d62afa4` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous: `tog.tex` contains the author name and the GitHub URL inside the `\else` branches, so do not send sources for review without stripping them. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 260911 | 10 | `7d41248b0fcf4ca71b7d6e02f0f6f2b1e35bf44f13fd90a9b80c2037a8cd21a0` |
| `dist/tog/supplement.pdf` | 760935 | 95 | `1d4b179304a6c445fd5943b2d59b41bbf8901690d8c17331a52b053d60567c61` |

Maximum upload size per file in ScholarOne for ToG: not verified.
