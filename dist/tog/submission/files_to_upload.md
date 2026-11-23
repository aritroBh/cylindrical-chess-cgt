# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260516 | 10 | `7a853b09b2ec18b91e51809788971cca45c3b3c8aab0658ba5ef1143ba08c4c8` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 765345 | 95 | `6a3c9bac9ac33cbe2bb880cd35e3814542fc4ddebc6a1c6a1d2cffb162152052` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous: `tog.tex` contains the author name and the GitHub URL inside the `\else` branches, so do not send sources for review without stripping them. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261099 | 10 | `d6b9c11a0d72480a9184336e92526000c0cb28c6855ef7e2dc41e4b11bd778cd` |
| `dist/tog/supplement.pdf` | 765569 | 95 | `aa12793851d976a4c1990363ed026b19f94fd3ffdacbd3a15938c87f2508e61c` |

Maximum upload size per file in ScholarOne for ToG: not verified.
