# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260599 | 10 | `f491c371d531106131a8de777241b2f8baffeeea335fb059ed7ea00f1c814475` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 823417 | 106 | `efab418488280dfa077ea4ed119f316d1f36d7e7d167dd49fb0b8f38e121b9f6` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous: `tog.tex` contains the author name and the GitHub URL inside the `\else` branches, so do not send sources for review without stripping them. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261176 | 10 | `9e2ffdf60803dd8517061449c8a9dc6c9e2668e36bbd87f04858e864453a1881` |
| `dist/tog/supplement.pdf` | 823758 | 106 | `45e7b0376d4ed8d1437d3a8948eb2407565fd275a18fb8a3cb66f3222543e0bc` |

Maximum upload size per file in ScholarOne for ToG: not verified.
