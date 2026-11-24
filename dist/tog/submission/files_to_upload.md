# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260610 | 10 | `421f416371948402ad136f3c7eca3a8bf83c826e43ba718a5de63e6edc4d1f6b` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 848747 | 108 | `418274ad81a30e6674580382ee792c7bb4bfb60579024a3a414522adfba26fb5` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous. These source files hold the author's name or the named GitHub URL (checked with grep on 2026-11-23): `tog.tex` (lines 42, 45, 47, 109-113, 147: GitHub URL, `\studyauthor`, PDF metadata, author block and affiliation, Prof. Morley), `macros.tex` (line 13: `\repourl`, the GitHub URL, unconditional; `sections/13_verify.tex` falls back to it), and `supplement.tex` (lines 34 and 36: GitHub URL and `\studyauthor`; line 79: the author's name). Do not send sources for review without stripping all three files. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261203 | 10 | `9c97409a74bd75cf4336c8921e8002bcfba0050272d40bef51564c6f16c2dd96` |
| `dist/tog/supplement.pdf` | 848980 | 108 | `bfb914cde231709e1f9ceb446c30a5e7f3d926b2bfa2f74f7a14ef7f5e65ddd7` |

Maximum upload size per file in ScholarOne for ToG: not verified.
