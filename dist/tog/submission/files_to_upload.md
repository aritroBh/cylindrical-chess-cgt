# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260692 | 10 | `a49eff7aa3cbef7058135a04e9d40bbb0e6c1e7390de2b8ce61dd76f7c7e81fc` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 853702 | 109 | `0d2273a96c5629244a45ecad4b5d90302530d751a4cc9d45814fa7dd962a5e0a` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous. These source files hold the author's name or the named GitHub URL (checked with grep on 2026-11-23): `tog.tex` (lines 42, 45, 47, 109-113, 147: GitHub URL, `\studyauthor`, PDF metadata, author block and affiliation, Prof. Morley), `macros.tex` (line 13: `\repourl`, the GitHub URL, unconditional; `sections/13_verify.tex` falls back to it), and `supplement.tex` (lines 34 and 36: GitHub URL and `\studyauthor`; line 79: the author's name). Do not send sources for review without stripping all three files. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261283 | 10 | `b70a426ad2ae6bff1386e7c4d2ab6d08aa259fe42ff425ca785368a7d74d617e` |
| `dist/tog/supplement.pdf` | 853888 | 109 | `006b9ef2a57d332ce321e87fba3a2040ac803a62ad0070a3b5a59121ffef8ea1` |

Maximum upload size per file in ScholarOne for ToG: not verified.
