# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260516 | 10 | `e978ae0a2d549c23ce1c34e791cf17cd05408d6ecb900c74988e4f67daa9b2e6` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 764200 | 95 | `13271d70258e110d727263d678ce7d001d26c1488e7a2741525e501c969f4c10` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous: `tog.tex` contains the author name and the GitHub URL inside the `\else` branches, so do not send sources for review without stripping them. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261098 | 10 | `b323a49aaf52a90134e9b21516d2572dc176588971d3b9ec9688e8528d1578a0` |
| `dist/tog/supplement.pdf` | 764417 | 95 | `b9db616ddf0b94110ddd8e2f187491128080ae8b5b228c2c806f493ce42cc29b` |

Maximum upload size per file in ScholarOne for ToG: not verified.
