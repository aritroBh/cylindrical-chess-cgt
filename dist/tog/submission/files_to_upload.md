# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260476 | 10 | `a17251209062a783366d4d504710886712b9f7acaad4e8d07ccf9c7a54a2fb23` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 610536 | 67 | `1ab50c287a8e3ec686c3c28a0dbf5538b60af0ff8f70056a4a76dca36fb5c39d` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous. These source files hold the author's name or the named GitHub URL (checked with grep on 2026-11-23): `tog.tex` (lines 42, 45, 47, 109-113, 147: GitHub URL, `\studyauthor`, PDF metadata, author block and affiliation, Prof. Morley), `macros.tex` (line 13: `\repourl`, the GitHub URL, unconditional; `sections/13_verify.tex` falls back to it), and `supplement.tex` (lines 34 and 36: GitHub URL and `\studyauthor`; line 79: the author's name). Do not send sources for review without stripping all three files. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261069 | 10 | `d3bb4f92493013e897ca25d252cd94d44e6fe1b0145ac03ef7f111445dc79c9c` |
| `dist/tog/supplement.pdf` | 610745 | 67 | `73bb5a4a8b0d47f71a6aef5a6b307ad9cb82ed81c1cae8bed747e19c5bb0b636` |

Maximum upload size per file in ScholarOne for ToG: not verified.
