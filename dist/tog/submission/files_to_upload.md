# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260466 | 10 | `c8427cfbfc7ee0e1ff8590aa323ac57cc3463d9c1c7a90850e166a8701f96742` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 609391 | 67 | `cf4134052223f17d701343b9eeb6a0b874e0c8e879c84721b991e713ddda971a` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous. These source files hold the author's name or the named GitHub URL (checked with grep on 2026-11-23): `tog.tex` (lines 42, 45, 47, 109-113, 147: GitHub URL, `\studyauthor`, PDF metadata, author block and affiliation, Prof. Morley), `macros.tex` (line 13: `\repourl`, the GitHub URL, unconditional; `sections/13_verify.tex` falls back to it), and `supplement.tex` (lines 34 and 36: GitHub URL and `\studyauthor`; line 79: the author's name). Do not send sources for review without stripping all three files. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261065 | 10 | `0ce3219eb8991fc51b44ecaa597a83dabcdd30d9a6bfdd8c60c4d506d92db245` |
| `dist/tog/supplement.pdf` | 609564 | 67 | `9392549e1bdbe4432a13d5c0edd177c976c14fd3afef6ed0cdee9822e758b47c` |

Maximum upload size per file in ScholarOne for ToG: not verified.
