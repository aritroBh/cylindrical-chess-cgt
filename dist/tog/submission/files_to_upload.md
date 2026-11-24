# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260464 | 10 | `9b7b77b3e5662fde34c7b8d4966293099b52b852dda155a19c59a3f8461509ae` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 611040 | 67 | `872e43b86f8c02deace6aa5ab9bfbf8c01cdbe2ebcf79bbe76607b500c5d6a76` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous. These source files hold the author's name or the named GitHub URL (checked with grep on 2026-11-23): `tog.tex` (lines 42, 45, 47, 109-113, 147: GitHub URL, `\studyauthor`, PDF metadata, author block and affiliation, Prof. Morley), `macros.tex` (line 13: `\repourl`, the GitHub URL, unconditional; `sections/13_verify.tex` falls back to it), and `supplement.tex` (lines 34 and 36: GitHub URL and `\studyauthor`; line 79: the author's name). Do not send sources for review without stripping all three files. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 260995 | 10 | `477b18670c9342e10d8ff090477aa50ca504ee36a96a537dded76ce263ed5c3a` |
| `dist/tog/supplement.pdf` | 611221 | 67 | `6e3b40c45830ede1162356558b3cd9b8498af546d431190d4dfe23ddd2e6e78b` |

Maximum upload size per file in ScholarOne for ToG: not verified.
