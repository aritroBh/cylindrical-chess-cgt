# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260599 | 10 | `bba368f2ae75c32b4f22c9cc8648c2e81e4ca4341ad3568bf1525b7d7f731570` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 829585 | 106 | `c6ba0346000645ac8f96bf567e90269cd07b0e81a0cf0c16c06ee32bc11ff98f` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous: `tog.tex` contains the author name and the GitHub URL inside the `\else` branches, so do not send sources for review without stripping them. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261176 | 10 | `f1b734d12594a6e5e67e2d9b936c1482fb16f6cb7d329e399de5d4b911c2067d` |
| `dist/tog/supplement.pdf` | 829908 | 106 | `796141aa6767e3133b3aaafe72cbaa9252e673cc66166aa3b19c752ba3809587` |

Maximum upload size per file in ScholarOne for ToG: not verified.
