# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260465 | 10 | `a74349ce97009cff6b005870f439496e1922f8095942da5181654d5655b2f1f6` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 611041 | 67 | `0a763612f71454c8e69d2702f7cd9efb7c600f30cfe48813673ffe01be75e744` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous. These source files hold the author's name or the named GitHub URL (checked with grep on 2026-11-23): `tog.tex` (lines 42, 45, 47, 109-113, 147: GitHub URL, `\studyauthor`, PDF metadata, author block and affiliation, Prof. Morley), `macros.tex` (line 13: `\repourl`, the GitHub URL, unconditional; `sections/13_verify.tex` falls back to it), and `supplement.tex` (lines 34 and 36: GitHub URL and `\studyauthor`; line 79: the author's name). Do not send sources for review without stripping all three files. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 260980 | 10 | `731feb123a83b33394841c1f13b1f94d94f018547b13e0abbc9773665241e8e2` |
| `dist/tog/supplement.pdf` | 611236 | 67 | `5d38d5886500dc4ab41fa565a65f338e352de49ad7aca96c6c848e8f631017d0` |

Maximum upload size per file in ScholarOne for ToG: not verified.
